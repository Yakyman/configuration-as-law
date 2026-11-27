# SPDX-License-Identifier: MIT
"""External, read-only readers for ConfOS packages and raw disks.

Nothing here runs the system under test or anything taken from it. Packages are read
with Python's tarfile and lzma modules without extraction; disks are read with GPT
parsing in Python, debugfs/e2fsck from e2fsprogs and unsquashfs from squashfs-tools.
The raw disk is only ever opened read-only; journal replay happens on a copy.

Object format: {'kind': 'file'|'dir'|'symlink'|'hardlink'|'special', 'id': '/abs/path',
'value': {'mode': '0755', 'uid': int, 'gid': int, 'sha256': hex (files),
'target': str (symlink/hardlink), 'type': str (special)}}.
Owners and modes always come from the on-disk metadata (debugfs `ls -p`, unsquashfs
`-lln`), never from files written by this process; contents come from dumps.
"""
import base64
import hashlib
import os
import re
import shutil
import stat
import struct
import subprocess
import tarfile
import tempfile
import time
import uuid
import zlib

SECTOR = 512
# INTERFACE.md section 7: partition number -> (first sector, last sector or None for "end")
LAYOUT = {1: (2048, 264191), 2: (264192, 12847103), 3: (12847104, None)}
EXT_LABELS = {2: 'CONFOS-SYSTEM', 3: 'CONFOS-DATA'}
PASSPORT_DIR = '/usr/lib/confpkg'
ROOT_TEXTS = ('/etc/passwd', '/etc/group', '/etc/shadow', '/etc/hostname', '/etc/hosts',
              '/etc/timezone', '/etc/locale.conf', '/etc/network.conf', '/etc/confos/identity',
              '/etc/confos/services.json', '/etc/confos/sysctls.json', '/etc/confos/open.json',
              '/etc/confos/home-files.json', '/etc/confos/rules.nft', '/etc/sudoers')
ROOT_TEXT_DIRS = ('/etc/sudoers.d', '/etc/dropbear/authorized_keys')
ROOT_LINKS = ('/etc/localtime',)
TOOL_DIRS = ('/usr/sbin', '/sbin', '/usr/bin', '/bin')
_HEX64 = re.compile(r'[0-9a-f]{64}')
_NAME = re.compile(r'[a-z0-9][a-z0-9+._-]*')
_MODE = re.compile(r'[0-7]{4}')
_OWNER = re.compile(r'(\d+):(\d+)')


def _sha(data):
    return hashlib.sha256(data).hexdigest()


# ------------------------------------------------------------------ passports
def _rel_path(path, what):
    if (not path or path.startswith('/') or path.endswith('/')
            or any(p in ('', '.', '..') for p in path.split('/'))):
        raise ValueError(f'{what}: unsafe or malformed path {path!r}')
    return path


def parse_passport(text):
    """Strict parser for the passport grammar of FORMAT.md / tools/confpkg.

    Returns name, version, sources [(name, sha)], recipe (name, sha) or None for the
    'recipe - sha256 -' line of the declaration pseudo-package, built_with, entries
    (objects with a leading '/'), sizes {id: size} for file entries.
    """
    if not isinstance(text, str):
        raise ValueError('passport is not text')
    if not text.endswith('\n'):
        raise ValueError('passport does not end with a newline')
    lines = text[:-1].split('\n')
    if lines[0] != 'confpkg 1':
        raise ValueError('passport: first line is not "confpkg 1"')
    out = {'name': None, 'version': None, 'sources': [], 'recipe': None, 'built_with': None,
           'entries': [], 'sizes': {}}
    seen_recipe = False
    paths = {}
    for n, line in enumerate(lines[1:], 2):
        kind, sep, rest = line.partition(' ')
        where = f'passport line {n}'
        if kind in ('name', 'version'):
            if out[kind] is not None:
                raise ValueError(f'{where}: duplicate {kind}')
            if not sep or not rest or ' ' in rest:
                raise ValueError(f'{where}: malformed {kind}')
            if kind == 'name' and not _NAME.fullmatch(rest):
                raise ValueError(f'{where}: bad package name {rest!r}')
            out[kind] = rest
        elif kind == 'source':
            f = rest.split(' ')
            if len(f) != 3 or f[1] != 'sha256' or not f[0] or not _HEX64.fullmatch(f[2]):
                raise ValueError(f'{where}: malformed source line')
            out['sources'].append((f[0], f[2]))
        elif kind == 'recipe':
            if seen_recipe:
                raise ValueError(f'{where}: duplicate recipe')
            seen_recipe = True
            f = rest.split(' ')
            if f == ['-', 'sha256', '-']:
                out['recipe'] = None
            elif len(f) == 3 and f[1] == 'sha256' and f[0] and _HEX64.fullmatch(f[2]):
                out['recipe'] = (f[0], f[2])
            else:
                raise ValueError(f'{where}: malformed recipe line')
        elif kind == 'built-with':
            if out['built_with'] is not None:
                raise ValueError(f'{where}: duplicate built-with')
            words = rest.split(' ') if rest else []
            if any(not w for w in words[:-1]) or (words and words[-1] == '' and len(words) > 1):
                raise ValueError(f'{where}: malformed built-with')
            out['built_with'] = [w for w in words if w]
        elif kind in ('dir', 'file', 'link', 'hardlink'):
            if kind in ('link', 'hardlink'):
                f = rest.split(' ', 2)
                if len(f) != 3 or f[1] != '->' or not f[2]:
                    raise ValueError(f'{where}: malformed {kind} line')
                path = _rel_path(f[0], where)
                if kind == 'link':
                    obj = {'kind': 'symlink', 'id': '/' + path, 'value': {'target': f[2]}}
                else:
                    obj = {'kind': 'hardlink', 'id': '/' + path,
                           'value': {'target': '/' + _rel_path(f[2], where)}}
            else:
                f = rest.split(' ')
                want = 3 if kind == 'dir' else 5
                if len(f) != want:
                    raise ValueError(f'{where}: malformed {kind} line')
                path = _rel_path(f[0], where)
                own = _OWNER.fullmatch(f[2])
                if not _MODE.fullmatch(f[1]) or not own:
                    raise ValueError(f'{where}: malformed mode or owner')
                value = {'mode': f[1], 'uid': int(own.group(1)), 'gid': int(own.group(2))}
                if kind == 'file':
                    if not f[3].isdigit() or not _HEX64.fullmatch(f[4]):
                        raise ValueError(f'{where}: malformed size or sha256')
                    value['sha256'] = f[4]
                    out['sizes']['/' + path] = int(f[3])
                obj = {'kind': kind, 'id': '/' + path, 'value': value}
            if obj['id'] in paths:
                raise ValueError(f'{where}: duplicate path {obj["id"]}')
            paths[obj['id']] = obj
            out['entries'].append(obj)
        else:
            raise ValueError(f'{where}: unknown line kind {kind!r}')
    for k in ('name', 'version', 'built_with'):
        if out[k] is None:
            raise ValueError(f'passport: missing {k.replace("_", "-")}')
    if not seen_recipe:
        raise ValueError('passport: missing recipe')
    for obj in out['entries']:
        if obj['kind'] == 'hardlink':
            t = paths.get(obj['value']['target'])
            if t is None or t['kind'] != 'file':
                raise ValueError(f'passport: hardlink {obj["id"]} names no file entry')
    return out


# ------------------------------------------------------------------ packages
def _file_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


_ALLOWED_TYPES = {tarfile.REGTYPE: 'file', tarfile.AREGTYPE: 'file', tarfile.DIRTYPE: 'dir',
                  tarfile.SYMTYPE: 'symlink', tarfile.LNKTYPE: 'hardlink'}


def read_confpkg(path):
    """Read a .confpkg without extracting it; verify every member against the passport."""
    label = os.path.basename(str(path))
    archive_sha = _file_sha256(path)
    members, seen = [], set()
    passport_bytes = None
    try:
        with tarfile.open(path, mode='r|xz') as tf:
            for index, m in enumerate(tf):
                name = m.name
                where = f'{label}: member {name!r}'
                if index == 0:
                    if name != 'passport' or m.type not in (tarfile.REGTYPE, tarfile.AREGTYPE):
                        raise ValueError(f'{label}: first member is not the regular file passport')
                    passport_bytes = tf.extractfile(m).read()
                    if len(passport_bytes) != m.size:
                        raise ValueError(f'{label}: truncated passport')
                    continue
                if name.startswith('/'):
                    raise ValueError(f'{where}: absolute member name')
                parts = name.split('/')
                if '..' in parts or '.' in parts or '' in parts:
                    raise ValueError(f'{where}: unsafe member name')
                if parts[0] != 'root' or len(parts) < 2:
                    raise ValueError(f'{where}: member outside root/')
                if name in seen:
                    raise ValueError(f'{where}: duplicate member')
                seen.add(name)
                kind = _ALLOWED_TYPES.get(m.type)
                if kind is None:
                    raise ValueError(f'{where}: device, FIFO or unsupported member type {m.type!r}')
                if m.mode & ~0o7777:
                    raise ValueError(f'{where}: mode field has bits beyond 07777')
                rec = {'id': '/' + '/'.join(parts[1:]), 'kind': kind, 'mode': '%04o' % m.mode,
                       'uid': m.uid, 'gid': m.gid, 'size': m.size, 'name': name}
                if kind == 'file':
                    h = hashlib.sha256()
                    n = 0
                    src = tf.extractfile(m)
                    for b in iter(lambda: src.read(1 << 20), b''):
                        h.update(b)
                        n += len(b)
                    if n != m.size:
                        raise ValueError(f'{where}: truncated content')
                    rec['sha256'] = h.hexdigest()
                elif kind == 'symlink':
                    rec['target'] = m.linkname
                elif kind == 'hardlink':
                    ln = m.linkname
                    lp = ln.split('/')
                    if (ln.startswith('/') or lp[0] != 'root' or len(lp) < 2
                            or any(p in ('', '.', '..') for p in lp)):
                        raise ValueError(f'{where}: hard link target outside root/: {ln!r}')
                    rec['target'] = '/' + '/'.join(lp[1:])
                members.append(rec)
    except (tarfile.TarError, EOFError, OSError) as exc:
        if isinstance(exc, FileNotFoundError):
            raise
        raise ValueError(f'{label}: unreadable archive: {exc}') from exc
    except Exception as exc:  # lzma.LZMAError and friends
        if isinstance(exc, ValueError):
            raise
        raise ValueError(f'{label}: unreadable archive: {exc}') from exc
    if passport_bytes is None:
        raise ValueError(f'{label}: empty archive')
    try:
        passport_text = passport_bytes.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError(f'{label}: passport is not UTF-8') from exc
    try:
        passport = parse_passport(passport_text)
    except ValueError as exc:
        raise ValueError(f'{label}: {exc}') from exc
    by_id = {r['id']: r for r in members}
    # Link-then-child: no member may lie below a member that is not a directory.
    for r in members:
        p = r['id']
        while True:
            p = p.rsplit('/', 1)[0]
            if not p:
                break
            parent = by_id.get(p)
            if parent is not None and parent['kind'] != 'dir':
                raise ValueError(f'{label}: member {r["name"]!r} lies below non-directory '
                                 f'member {parent["name"]!r} ({parent["kind"]})')
    order = {r['id']: i for i, r in enumerate(members)}
    for r in members:
        if r['kind'] == 'hardlink':
            t = by_id.get(r['target'])
            if t is None or t['kind'] != 'file' or order[t['id']] > order[r['id']]:
                raise ValueError(f'{label}: hard link {r["name"]!r} names no earlier regular file')
    want = {o['id']: o for o in passport['entries']}
    missing = sorted(set(want) - set(by_id))
    extra = sorted(set(by_id) - set(want))
    if missing:
        raise ValueError(f'{label}: passport entries missing from archive: {", ".join(missing[:5])}'
                         + (f' (+{len(missing) - 5})' if len(missing) > 5 else ''))
    if extra:
        raise ValueError(f'{label}: archive members not in passport: {", ".join(extra[:5])}'
                         + (f' (+{len(extra) - 5})' if len(extra) > 5 else ''))
    for pid, o in want.items():
        r = by_id[pid]
        if r['kind'] != o['kind']:
            raise ValueError(f'{label}: {pid}: type {r["kind"]} in archive, {o["kind"]} in passport')
        v = o['value']
        if o['kind'] in ('file', 'dir'):
            for k in ('mode', 'uid', 'gid'):
                if r[k] != v[k]:
                    raise ValueError(f'{label}: {pid}: {k} {r[k]} in archive, {v[k]} in passport')
        if o['kind'] == 'file':
            if r['size'] != passport['sizes'][pid]:
                raise ValueError(f'{label}: {pid}: size {r["size"]} in archive, '
                                 f'{passport["sizes"][pid]} in passport')
            if r['sha256'] != v['sha256']:
                raise ValueError(f'{label}: {pid}: sha256 differs from passport')
        if o['kind'] in ('symlink', 'hardlink') and r['target'] != v['target']:
            raise ValueError(f'{label}: {pid}: link target {r["target"]!r} in archive, '
                             f'{v["target"]!r} in passport')
    objects = [{'kind': o['kind'], 'id': o['id'], 'value': dict(o['value'])}
               for o in passport['entries']]
    return {'archive_sha256': archive_sha, 'passport_text': passport_text,
            'passport_sha256': _sha(passport_bytes), 'passport': passport, 'objects': objects}


def _source_pairs(value):
    if isinstance(value, str):
        return None, value
    pairs = []
    for item in value:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise ValueError('source_sha256 entries must be [name, sha256]')
        pairs.append((str(item[0]), str(item[1])))
    return pairs, None


def store_package_reader(store_dir, recipes_dir=None):
    """A package reader for core.derive backed by a confpkg store folder."""
    store = os.path.realpath(store_dir)
    recipes = os.path.realpath(recipes_dir) if recipes_dir else None

    def read(line):
        archive = line['archive']
        if (not isinstance(archive, str) or not archive or '/' in archive or '\0' in archive
                or archive in ('.', '..')):
            raise ValueError(f'package {line.get("name")}: archive must be a file name in the store')
        path = os.path.join(store, archive)
        if not os.path.isfile(path) or os.path.islink(path):
            raise ValueError(f'package {line.get("name")}: archive {archive} not in the store')
        got = _file_sha256(path)
        if got != line['archive_sha256']:
            raise ValueError(f'package {line["name"]}: archive hash mismatch '
                             f'(store {got}, declared {line["archive_sha256"]})')
        pkg = read_confpkg(path)
        if pkg['archive_sha256'] != got:
            raise ValueError(f'package {line["name"]}: archive changed while read')
        pp = pkg['passport']
        if pp['name'] != line['name'] or pp['version'] != line['version']:
            raise ValueError(f'package {line["name"]}: passport names {pp["name"]} {pp["version"]}, '
                             f'declared {line["name"]} {line["version"]}')
        if pp['recipe'] is None:
            raise ValueError(f'package {line["name"]}: passport has no recipe')
        rname, rsha = pp['recipe']
        if rsha != line['recipe_sha256']:
            raise ValueError(f'package {line["name"]}: recipe sha256 in passport differs from declared')
        if recipes and '/' not in rname and rname not in ('.', '..'):
            rpath = os.path.join(recipes, rname)
            if os.path.isfile(rpath):
                rgot = _file_sha256(rpath)
                if rgot != rsha:
                    raise ValueError(f'package {line["name"]}: recipe file {rname} has sha256 {rgot}, '
                                     f'passport {rsha}')
        pairs, single = _source_pairs(line['source_sha256'])
        if single is not None:
            if [s for _, s in pp['sources']] != [single]:
                raise ValueError(f'package {line["name"]}: source sha256 differs from passport')
        elif sorted(pairs) != sorted(pp['sources']):
            raise ValueError(f'package {line["name"]}: sources differ from passport')
        # tools/confpkg install_one copies the passport with
        #   with open(os.path.join(db, pp["name"] + ".passport"), "w") as f:
        # and no chmod/chown: mode 0666 & ~umask, owner the installing (root) process; the image
        # builder (files/confos/confos build_root) runs as root with the inherited umask 022, and the
        # unpacked real root lists every usr/lib/confpkg/*.passport as 0644 0:0.
        objects = list(pkg['objects'])
        objects.append({'kind': 'file', 'id': f'{PASSPORT_DIR}/{pp["name"]}.passport',
                        'value': {'mode': '0644', 'uid': 0, 'gid': 0,
                                  'sha256': pkg['passport_sha256']}})
        return objects
    return read


# ------------------------------------------------------------------ GPT
def _guid(b):
    return str(uuid.UUID(bytes_le=bytes(b))).upper()


def gpt_partitions(raw_path):
    """Partitions from the primary GPT (LBA 1), with header and entry CRC32 checked."""
    with open(raw_path, 'rb') as f:
        f.seek(SECTOR)
        hdr = f.read(SECTOR)
        if len(hdr) < 92:
            raise ValueError('GPT: disk too small')
        (sig, rev, hsize, hcrc, _res, my_lba, _alt, first_use, last_use, _dguid, ent_lba, count,
         esize, ecrc) = struct.unpack_from('<8sIIIIQQQQ16sQIII', hdr)
        if sig != b'EFI PART':
            raise ValueError('GPT: no "EFI PART" signature at LBA 1')
        if not 92 <= hsize <= SECTOR:
            raise ValueError(f'GPT: bad header size {hsize}')
        h = bytearray(hdr[:hsize])
        h[16:20] = b'\0\0\0\0'
        if zlib.crc32(bytes(h)) & 0xffffffff != hcrc:
            raise ValueError('GPT: header CRC32 mismatch')
        if my_lba != 1:
            raise ValueError(f'GPT: header names LBA {my_lba}, not 1')
        if esize < 128 or esize % 8 or count * esize > (1 << 20):
            raise ValueError(f'GPT: bad entry array ({count} x {esize})')
        f.seek(ent_lba * SECTOR)
        ents = f.read(count * esize)
        if len(ents) != count * esize:
            raise ValueError('GPT: entry array truncated')
        if zlib.crc32(ents) & 0xffffffff != ecrc:
            raise ValueError('GPT: entry array CRC32 mismatch')
    parts = []
    for i in range(count):
        e = ents[i * esize:(i + 1) * esize]
        tguid = e[0:16]
        if tguid == b'\0' * 16:
            continue
        first, last, attrs = struct.unpack_from('<QQQ', e, 32)
        name = e[56:128].decode('utf-16-le', errors='replace').split('\0', 1)[0]
        parts.append({'number': i + 1, 'first_lba': first, 'last_lba': last,
                      'type_guid': _guid(tguid), 'unique_guid': _guid(e[16:32]),
                      'name': name, 'attributes': attrs,
                      'first_usable_lba': first_use, 'last_usable_lba': last_use})
    return parts


def check_layout(parts):
    """Disagreements between a GPT and INTERFACE.md section 7, as error texts."""
    errs = []
    nums = {p['number']: p for p in parts}
    for n, (first, last) in LAYOUT.items():
        p = nums.get(n)
        if p is None:
            errs.append(f'partition {n} absent (INTERFACE.md 7)')
            continue
        if p['first_lba'] != first:
            errs.append(f'partition {n} starts at sector {p["first_lba"]}, INTERFACE.md 7 says {first}')
        if last is not None and p['last_lba'] != last:
            errs.append(f'partition {n} ends at sector {p["last_lba"]}, INTERFACE.md 7 says {last}')
        if p['last_lba'] < p['first_lba']:
            errs.append(f'partition {n} is empty or inverted')
    for n in sorted(set(nums) - set(LAYOUT)):
        errs.append(f'partition {n} not described by INTERFACE.md 7')
    return errs


def ext_superblock(raw_path, offset):
    """The few ext4 superblock fields that matter here, read in Python."""
    with open(raw_path, 'rb') as f:
        f.seek(offset + 1024)
        sb = f.read(1024)
    if len(sb) < 1024 or struct.unpack_from('<H', sb, 0x38)[0] != 0xEF53:
        return None
    compat, incompat, ro = struct.unpack_from('<III', sb, 0x5C)
    lo = struct.unpack_from('<I', sb, 0x04)[0]
    hi = struct.unpack_from('<I', sb, 0x150)[0] if incompat & 0x80 else 0
    return {'label': sb[0x78:0x88].split(b'\0', 1)[0].decode('latin-1'),
            'block_size': 1024 << struct.unpack_from('<I', sb, 0x18)[0],
            'blocks': (hi << 32) | lo, 'has_journal': bool(compat & 0x4),
            'needs_recovery': bool(incompat & 0x4), 'extents': bool(incompat & 0x40)}


# ------------------------------------------------------------------ helpers for disks
def _tool(name):
    found = shutil.which(name) or shutil.which(name, path=os.pathsep.join(TOOL_DIRS))
    if not found:
        raise FileNotFoundError(f'host tool {name} not found')
    return found


_ENV = {'PATH': os.pathsep.join(('/usr/bin', '/bin') + TOOL_DIRS), 'LC_ALL': 'C', 'TZ': 'UTC',
        'DEBUGFS_PAGER': '__none__', 'PAGER': '__none__'}
_DEBUGFS_NOISE = re.compile(r'^(debugfs [0-9.]+ \(.*\)|catastrophic mode - not reading inode or '
                            r'group bitmaps|.*Operation not permitted while changing ownership of .*)$')


class _Evidence:
    def __init__(self):
        self.commands = []
        self._groups = {}

    def record(self, argv, rc, seconds, stderr=b'', group=None):
        tail = stderr.decode(errors='replace')[-400:] if isinstance(stderr, bytes) else str(stderr)
        if group is None:
            self.commands.append({'argv': [str(a) for a in argv], 'returncode': rc,
                                  'seconds': round(seconds, 3), 'stderr_tail': tail})
            return
        g = self._groups.get(group)
        if g is None:
            g = {'argv': group, 'count': 0, 'nonzero': 0, 'seconds': 0.0}
            self._groups[group] = g
            self.commands.append(g)
        g['count'] += 1
        g['nonzero'] += rc != 0
        g['seconds'] = round(g['seconds'] + seconds, 3)


def _unexpected_stderr(stderr):
    lines = [l for l in stderr.decode(errors='replace').splitlines() if l.strip()]
    return [l for l in lines if not _DEBUGFS_NOISE.match(l)]


def _sparse_copy(raw_path, start, length, dst):
    """Copy a byte range to a sparse file, skipping holes and zero blocks; raw opened read-only."""
    fd = os.open(raw_path, os.O_RDONLY)
    copied = 0
    try:
        with open(dst, 'wb') as out:
            pos, end = start, start + length
            while pos < end:
                try:
                    data = os.lseek(fd, pos, os.SEEK_DATA)
                    hole = os.lseek(fd, data, os.SEEK_HOLE)
                except OSError as exc:
                    if exc.errno == 6:  # ENXIO: no data after pos
                        break
                    data, hole = pos, end   # no hole support: copy everything
                if data >= end:
                    break
                hole = min(hole, end)
                os.lseek(fd, data, os.SEEK_SET)
                cur = data
                while cur < hole:
                    chunk = os.read(fd, min(1 << 20, hole - cur))
                    if not chunk:
                        raise ValueError('raw disk shorter than its partition table')
                    if chunk.count(0) != len(chunk):
                        out.seek(cur - start)
                        out.write(chunk)
                        copied += len(chunk)
                    cur += len(chunk)
                pos = hole
            out.truncate(length)
    finally:
        os.close(fd)
    return copied


_LS_HEAD = re.compile(r'^debugfs: (?:ls -p|stat) <(\d+)>\n', re.M)
_LS_ENTRY = re.compile(r'/(\d+)/([0-7]{6})/(-?\d+)/(-?\d+)/([^/]*)/(\d*)/\n')


class _Ext:
    """An ext4 file system of the disk, read with debugfs (read-only, catastrophic mode)."""

    def __init__(self, dev, ev, errors, label):
        self.dev, self.ev, self.errors, self.label = dev, ev, errors, label
        self.debugfs = _tool('debugfs')

    def err(self, reason):
        self.errors.append({'kind': 'stored', 'reason': f'{self.label}: {reason}'})

    def batch(self, commands, group):
        argv = [self.debugfs, '-c', '-f', '-', self.dev]
        t = time.monotonic()
        p = subprocess.run(argv, input=''.join(c + '\n' for c in commands).encode(),
                           capture_output=True, env=_ENV)
        self.ev.record(argv, p.returncode, time.monotonic() - t, p.stderr, group=group)
        bad = _unexpected_stderr(p.stderr)
        if p.returncode or bad:
            self.err(f'debugfs batch failed (rc {p.returncode}): {"; ".join(bad[:3])}')
        return os.fsdecode(p.stdout)

    def listdirs(self, inos):
        """{ino: [(name, ino, mode, uid, gid, size)]} for directory inodes, or error entries."""
        out = {}
        for i in range(0, len(inos), 2000):
            part = inos[i:i + 2000]
            text = self.batch([f'ls -p <{n}>' for n in part], 'debugfs -c -f - DEV  (ls -p <INO> ...)')
            heads = list(_LS_HEAD.finditer(text))
            for k, h in enumerate(heads):
                body = text[h.end():heads[k + 1].start() if k + 1 < len(heads) else len(text)]
                ino = int(h.group(1))
                rows, pos = [], 0
                for m in _LS_ENTRY.finditer(body):
                    if body[pos:m.start()].strip():
                        break
                    pos = m.end()
                    rows.append((m.group(5), int(m.group(1)), int(m.group(2), 8),
                                 int(m.group(3)) & 0xffffffff, int(m.group(4)) & 0xffffffff,
                                 int(m.group(6)) if m.group(6) else 0))
                if body[pos:].strip():
                    self.err(f'unparsable listing of inode {ino}: {body[pos:pos + 80]!r}')
                out[ino] = rows
            for n in part:
                if n not in out:
                    self.err(f'no listing for directory inode {n}')
        return out

    def walk(self, ino, prefix):
        """Whole subtree below a directory inode: (root_meta, {path: meta}); meta=(ino,mode,uid,gid,size)."""
        entries, root_meta = {}, None
        level, seen = [(ino, prefix)], {ino}
        while level:
            lists = self.listdirs([n for n, _ in level])
            nxt = []
            for dino, dpath in level:
                rows = lists.get(dino)
                if rows is None:
                    continue
                dots = [r for r in rows if r[0] == '.']
                if not dots or dots[0][1] != dino:
                    self.err(f'listing of {dpath or "/"} has no matching "." entry')
                elif dino == ino:
                    root_meta = dots[0][1:]
                for name, cino, mode, uid, gid, size in rows:
                    if name in ('.', '..') or cino == 0:   # ino 0: unused slot (lost+found)
                        continue
                    if not name or '\0' in name:
                        self.err(f'bad name in {dpath or "/"}: {name!r}')
                        continue
                    path = f'{dpath}/{name}'
                    entries[path] = (cino, mode, uid, gid, size)
                    if stat.S_ISDIR(mode):
                        if cino in seen:
                            self.err(f'directory loop at {path}')
                            continue
                        seen.add(cino)
                        nxt.append((cino, path))
            level = nxt
        return root_meta, entries

    def cat(self, ino, size, keep=False):
        """Stream one inode's content through sha256 (debugfs cat). Returns (sha, bytes|None)."""
        argv = [self.debugfs, '-c', '-R', f'cat <{ino}>', self.dev]
        t = time.monotonic()
        h, n, chunks = hashlib.sha256(), 0, []
        with subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=_ENV) as p:
            for b in iter(lambda: p.stdout.read(1 << 20), b''):
                h.update(b)
                n += len(b)
                if keep:
                    chunks.append(b)
            err = p.stderr.read()
            rc = p.wait()
        self.ev.record(argv, rc, time.monotonic() - t, err, group='debugfs -c -R "cat <INO>" DEV')
        bad = _unexpected_stderr(err)
        if rc or bad or n != size:
            self.err(f'cat of inode {ino}: rc {rc}, {n} of {size} bytes; {"; ".join(bad[:2])}')
            return None, None
        return h.hexdigest(), (b''.join(chunks) if keep else None)

    def dump(self, ino, dst, size):
        argv = [self.debugfs, '-c', '-R', f'dump <{ino}> {dst}', self.dev]
        t = time.monotonic()
        p = subprocess.run(argv, capture_output=True, env=_ENV)
        self.ev.record(argv, p.returncode, time.monotonic() - t, p.stderr)
        bad = _unexpected_stderr(p.stderr)
        if p.returncode or bad or not os.path.isfile(dst) or os.path.getsize(dst) != size:
            self.err(f'dump of inode {ino} failed (rc {p.returncode}): {"; ".join(bad[:2])}')
            return False
        return True

    def rdump(self, ino, dst_dir):
        argv = [self.debugfs, '-c', '-R', f'rdump <{ino}> {dst_dir}', self.dev]
        t = time.monotonic()
        p = subprocess.run(argv, capture_output=True, env=_ENV)
        self.ev.record(argv, p.returncode, time.monotonic() - t, p.stderr)
        bad = _unexpected_stderr(p.stderr)
        if p.returncode or bad:
            self.err(f'rdump failed (rc {p.returncode}): {"; ".join(bad[:3])}')
        return os.path.join(dst_dir, f'<{ino}>')

    def devices(self, inos):
        out = {}
        if not inos:
            return out
        text = self.batch([f'stat <{n}>' for n in inos], 'debugfs -c -f - DEV  (stat <INO> ...)')
        heads = list(_LS_HEAD.finditer(text))
        for k, h in enumerate(heads):
            body = text[h.end():heads[k + 1].start() if k + 1 < len(heads) else len(text)]
            m = re.search(r'Device major/minor number: (\d+):(\d+)', body)
            if m:
                out[int(h.group(1))] = (int(m.group(1)), int(m.group(2)))
        return out


def _make_accessible(top):
    """Give the owner (this process) access to a dump tree it created, without following links."""
    try:
        st = os.lstat(top)
    except FileNotFoundError:
        return
    if not stat.S_ISDIR(st.st_mode):
        return
    os.chmod(top, 0o700)
    for e in os.scandir(top):
        if e.is_dir(follow_symlinks=False):
            _make_accessible(e.path)
        elif e.is_file(follow_symlinks=False):
            m = stat.S_IMODE(e.stat(follow_symlinks=False).st_mode)
            if m & 0o600 != 0o600:
                os.chmod(e.path, m | 0o600)


def _rmtree(path):
    if os.path.lexists(path):
        try:
            _make_accessible(path)
        except OSError:
            pass
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path, ignore_errors=True)
        else:
            os.unlink(path)


def _hash_local(path):
    """sha256 of a regular file of a dump tree, never following a symlink."""
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise ValueError('not a regular file')
        h = hashlib.sha256()
        for b in iter(lambda: os.read(fd, 1 << 20), b''):
            h.update(b)
        return h.hexdigest(), st.st_size
    finally:
        os.close(fd)


def _read_local(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError('not a regular file')
        chunks = []
        for b in iter(lambda: os.read(fd, 1 << 20), b''):
            chunks.append(b)
        return b''.join(chunks)
    finally:
        os.close(fd)


def _special_type(mode, dev=None):
    if stat.S_ISCHR(mode):
        return f'char {dev[0]}:{dev[1]}' if dev else 'char ?'
    if stat.S_ISBLK(mode):
        return f'block {dev[0]}:{dev[1]}' if dev else 'block ?'
    if stat.S_ISFIFO(mode):
        return 'fifo'
    if stat.S_ISSOCK(mode):
        return 'socket'
    return 'unknown %o' % stat.S_IFMT(mode)


def _within(path, base):
    real = os.path.realpath(os.path.dirname(path))
    return real == base or real.startswith(base + os.sep)


def _ext_objects(ext, entries, dump_root, prefix, errors):
    """Objects of an ext4 subtree: metadata from debugfs listings, content from an rdump tree."""
    objects = []
    base = os.path.realpath(dump_root)
    groups = {}
    for path, (ino, mode, *_rest) in entries.items():
        if stat.S_ISREG(mode):
            groups.setdefault(ino, []).append(path)
    first = {ino: min(paths) for ino, paths in groups.items()}
    devs = ext.devices(sorted({m[0] for m in entries.values()
                               if stat.S_ISCHR(m[1]) or stat.S_ISBLK(m[1])}))
    for path in sorted(entries):
        ino, mode, uid, gid, size = entries[path]
        oid = prefix + path
        local = dump_root + path
        value = {'mode': '%04o' % stat.S_IMODE(mode), 'uid': uid, 'gid': gid}
        try:
            if stat.S_ISDIR(mode):
                kind = 'dir'
            elif stat.S_ISREG(mode):
                if not _within(local, base):
                    raise ValueError('dump path leaves the dump tree')
                sha, got = _hash_local(local)
                if got != size:
                    raise ValueError(f'dumped size {got}, listed {size}')
                value['sha256'] = sha
                if first[ino] != path:
                    kind, value['target'] = 'hardlink', prefix + first[ino]
                else:
                    kind = 'file'
            elif stat.S_ISLNK(mode):
                kind = 'symlink'
                value['target'] = os.readlink(local)
            else:
                kind = 'special'
                value['type'] = _special_type(mode, devs.get(ino))
                if value['type'].endswith('?'):
                    errors.append({'kind': 'stored', 'reason': f'{oid}: device numbers unread'})
            objects.append({'kind': kind, 'id': oid, 'value': value})
        except (OSError, ValueError) as exc:
            errors.append({'kind': 'stored', 'reason': f'{oid}: {exc}'})
    return objects


# ------------------------------------------------------------------ squashfs
_SQ_LINE = re.compile(r'^([-dlcbps])([-rwxsStT]{9}) +(\d+)/(\d+) +(?:(\d+)|(\d+), *(\d+)) +'
                      r'\d{4}-\d\d-\d\d \d\d:\d\d (squashfs-root(?:/.*)?)$')


_UNSQ_EXPECTED = re.compile(r"could not create (character|block) device .*because you're not "
                            r"superuser|^Parallel unsquashfs: Using \d+ processors?$|"
                            r"^\d+ inodes \(\d+ blocks\) to write$|^created \d+ ")


def _perm_bits(s):
    bits = 0
    for i, (sh, special) in enumerate(((6, 0o4000), (3, 0o2000), (0, 0o1000))):
        r, w, x = s[3 * i:3 * i + 3]
        if r not in 'r-' or w not in 'w-':
            raise ValueError(f'bad permission string {s!r}')
        bits |= (4 << sh if r == 'r' else 0) | (2 << sh if w == 'w' else 0)
        execs = 'xsS' if i < 2 else 'xtT'
        if x == 'x' or x == execs[1]:
            bits |= 1 << sh
        if x in execs[1:]:
            bits |= special
        elif x not in 'x-':
            raise ValueError(f'bad permission string {s!r}')
    return bits


def read_squashfs(sqfs, dest, ev=None, keep_tree=False):
    """{'objects', 'errors', 'root_meta', 'tree'}: metadata from `unsquashfs -lln`, contents and
    symlink targets from an extraction in dest; files hashed without following links."""
    ev = ev or _Evidence()
    objects, errors = [], []
    unsq = _tool('unsquashfs')
    argv = [unsq, '-lln', sqfs]
    t = time.monotonic()
    p = subprocess.run(argv, capture_output=True, env=_ENV)
    ev.record(argv, p.returncode, time.monotonic() - t, p.stderr)
    if p.returncode:
        errors.append({'kind': 'stored', 'reason': f'unsquashfs -lln failed rc {p.returncode}'})
        return {'objects': objects, 'errors': errors, 'root_meta': None, 'tree': None}
    listing = os.fsdecode(p.stdout).split('\n')
    if listing and listing[-1] == '':
        listing.pop()
    argv = [unsq, '-no-xattrs', '-no-progress', '-processors', '2', '-d', dest, sqfs]
    t = time.monotonic()
    p = subprocess.run(argv, capture_output=True, env=_ENV)
    ev.record(argv, p.returncode, time.monotonic() - t, p.stderr)
    if p.returncode and not os.path.isdir(dest):
        errors.append({'kind': 'stored', 'reason': f'unsquashfs extraction failed rc {p.returncode}'})
        return {'objects': objects, 'errors': errors, 'root_meta': None, 'tree': None}
    # As a normal user unsquashfs cannot create device nodes (exit status 2); those come from the
    # listing. Any other complaint is an error. Modes of the extraction are not used (it drops
    # set-user-ID bits); every mode and owner comes from the listing.
    for l in os.fsdecode(p.stderr).splitlines():
        if l.strip() and not _UNSQ_EXPECTED.search(l):
            errors.append({'kind': 'stored', 'reason': f'unsquashfs: {l[:200]}'})
    base = os.path.realpath(dest)
    rows, root_meta = [], None
    for line in listing:
        m = _SQ_LINE.match(line)
        if not m:
            errors.append({'kind': 'stored', 'reason': f'unparsable squashfs listing line {line[:120]!r}'})
            continue
        t_, perms, uid, gid = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
        rest = m.group(8)[len('squashfs-root'):]
        try:
            mode = '%04o' % _perm_bits(perms)
        except ValueError as exc:
            errors.append({'kind': 'stored', 'reason': f'{rest}: {exc}'})
            continue
        if rest == '':
            root_meta = {'mode': mode, 'uid': uid, 'gid': gid}
            continue
        target = None
        if t_ == 'l':
            path = None
            i = rest.find(' -> ')
            while i >= 0:
                cand = rest[:i]
                local = dest + cand
                if os.path.islink(local) and os.readlink(local) == rest[i + 4:]:
                    path, target = cand, rest[i + 4:]
                    break
                i = rest.find(' -> ', i + 1)
            if path is None:
                errors.append({'kind': 'stored', 'reason': f'symlink not resolved in extraction: {rest!r}'})
                continue
        else:
            path = rest
        dev = (int(m.group(6)), int(m.group(7))) if m.group(6) is not None else None
        size = int(m.group(5)) if m.group(5) is not None else None
        rows.append((path, t_, mode, uid, gid, size, dev, target))
    rows.sort()
    groups = {}
    for path, t_, *_ in rows:
        if t_ == '-':
            try:
                st = os.lstat(dest + path)
                if stat.S_ISREG(st.st_mode) and st.st_nlink > 1:
                    groups.setdefault((st.st_dev, st.st_ino), []).append(path)
            except OSError:
                pass
    first = {p: min(ps) for ps in groups.values() for p in ps}
    listed = set()
    for path, t_, mode, uid, gid, size, dev, target in rows:
        if path in listed:
            errors.append({'kind': 'stored', 'reason': f'{path}: listed twice'})
            continue
        listed.add(path)
        value = {'mode': mode, 'uid': uid, 'gid': gid}
        try:
            if t_ == 'd':
                kind = 'dir'
                if not stat.S_ISDIR(os.lstat(dest + path).st_mode):
                    raise ValueError('directory not extracted')
            elif t_ == '-':
                local = dest + path
                if not _within(local, base):
                    raise ValueError('extraction path leaves the extraction tree')
                sha, got = _hash_local(local)
                if size is not None and got != size:
                    raise ValueError(f'extracted size {got}, listed {size}')
                value['sha256'] = sha
                if first.get(path, path) != path:
                    kind, value['target'] = 'hardlink', first[path]
                else:
                    kind = 'file'
            elif t_ == 'l':
                kind, value['target'] = 'symlink', target
            else:
                kind = 'special'
                value['type'] = {'c': f'char {dev[0]}:{dev[1]}' if dev else 'char ?',
                                 'b': f'block {dev[0]}:{dev[1]}' if dev else 'block ?',
                                 'p': 'fifo', 's': 'socket'}[t_]
            objects.append({'kind': kind, 'id': path, 'value': value})
        except (OSError, ValueError) as exc:
            errors.append({'kind': 'stored', 'reason': f'{path}: {exc}'})
    # every extracted path must have been listed
    for dp, dns, fns in os.walk(dest):
        for n in dns + fns:
            rel = os.path.join(dp, n)[len(dest):]
            if rel not in listed:
                errors.append({'kind': 'stored', 'reason': f'{rel}: extracted but not listed'})
    return {'objects': objects, 'errors': errors, 'root_meta': root_meta, 'tree': dest}


def _root_texts(tree, objects, errors):
    """passports, texts and links of an unpacked generation root."""
    by_id = {o['id']: o for o in objects}
    passports, texts, links = {}, {}, {}

    def text_of(oid):
        data = _read_local(tree + oid)
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            errors.append({'kind': 'stored', 'reason': f'{oid}: not UTF-8, decoded with replacement'})
            return data.decode('utf-8', errors='replace')
    for oid, o in sorted(by_id.items()):
        d, _, n = oid.rpartition('/')
        if d == PASSPORT_DIR and n.endswith('.passport') and o['kind'] in ('file', 'hardlink'):
            passports[n[:-len('.passport')]] = text_of(oid)
    wanted = list(ROOT_TEXTS) + sorted(i for i in by_id if i.rpartition('/')[0] in ROOT_TEXT_DIRS)
    for oid in wanted:
        o = by_id.get(oid)
        if o is None:
            continue
        if o['kind'] in ('file', 'hardlink'):
            texts[oid] = text_of(oid)
        elif o['kind'] == 'symlink':
            links[oid] = o['value']['target']
    for oid in ROOT_LINKS:
        o = by_id.get(oid)
        if o is not None and o['kind'] == 'symlink':
            links[oid] = o['value']['target']
    return passports, texts, links


# ------------------------------------------------------------------ the disk
def _open_ext(raw_path, part, number, work, ev, errors, info, force_copy):
    offset = part['first_lba'] * SECTOR
    length = (part['last_lba'] - part['first_lba'] + 1) * SECTOR
    label = f'partition {number}'
    sb = ext_superblock(raw_path, offset)
    rec = {'offset': offset, 'length': length}
    info[f'p{number}'] = rec
    if sb is None:
        errors.append({'kind': 'stored', 'reason': f'{label}: no ext4 superblock'})
        return None
    rec.update(label=sb['label'], needs_recovery=sb['needs_recovery'])
    if sb['label'] != EXT_LABELS[number]:
        errors.append({'kind': 'stored', 'reason': f'{label}: label {sb["label"]!r}, '
                       f'INTERFACE.md 7 says {EXT_LABELS[number]}'})
    if not sb['extents']:
        errors.append({'kind': 'stored', 'reason': f'{label}: not ext4 (no extent feature)'})
    copy = force_copy or sb['needs_recovery']
    dev = None
    if not copy:
        link = os.path.join(work, 'disk')
        if not os.path.lexists(link):
            os.symlink(os.path.abspath(raw_path), link)
        if '?' in link:
            copy = True
        else:
            dev = f'{link}?offset={offset}'
            argv = [_tool('debugfs'), '-c', '-R', 'stats', dev]
            t = time.monotonic()
            p = subprocess.run(argv, capture_output=True, env=_ENV)
            ev.record(argv, p.returncode, time.monotonic() - t, p.stderr)
            if p.returncode or b'Filesystem volume name:' not in p.stdout:
                copy, dev = True, None
            rec['access'] = 'offset'
    if copy:
        dst = os.path.join(work, f'p{number}.ext4')
        t = time.monotonic()
        rec['copied_bytes'] = _sparse_copy(raw_path, offset, length, dst)
        rec['copy_seconds'] = round(time.monotonic() - t, 3)
        rec['access'] = 'sparse copy'
        argv = [_tool('e2fsck'), '-E', 'journal_only', '-p', dst]
        t = time.monotonic()
        p = subprocess.run(argv, capture_output=True, env=_ENV)
        ev.record(argv, p.returncode, time.monotonic() - t, p.stderr + p.stdout)
        rec['e2fsck_returncode'] = p.returncode
        if p.returncode not in (0, 1):
            errors.append({'kind': 'stored', 'reason': f'{label}: journal replay on the copy failed '
                           f'(e2fsck rc {p.returncode})'})
        after = ext_superblock(dst, 0)
        rec['needs_recovery_after'] = bool(after and after['needs_recovery'])
        rec['journal_replayed'] = sb['needs_recovery'] and not rec['needs_recovery_after']
        if rec['needs_recovery_after']:
            errors.append({'kind': 'stored', 'reason': f'{label}: journal still not replayed on the copy'})
        dev = dst
    return _Ext(dev, ev, errors, label)


def _children(entries, path):
    pre = path + '/'
    return {p[len(pre):]: m for p, m in entries.items() if p.startswith(pre) and '/' not in p[len(pre):]}


# ------------------------------------------------------------------ system store (INTERFACE 7)
def archive_passport(data, label='archive'):
    """Name, version, recipe and sources from the passport, the first member of a confpkg
    (FORMAT.md). Only the passport is read; problems are returned, not raised."""
    import io
    try:
        with tarfile.open(fileobj=io.BytesIO(data or b''), mode='r|xz') as tf:
            m = next(iter(tf), None)
            if m is None or m.name != 'passport' or not m.isreg():
                return {'passport_error': f'{label}: first member is not the passport'}
            pp = parse_passport(tf.extractfile(m).read().decode('utf-8'))
    except Exception as exc:                       # unreadable archive: an observed fact
        return {'passport_error': f'{label}: {type(exc).__name__}: {exc}'}
    return {'name': pp['name'], 'version': pp['version'],
            'recipe_sha256': pp['recipe'][1] if pp['recipe'] else None,
            'sources': sorted([list(x) for x in pp['sources']])}


TREE_PARTS = ('recipes/', 'files/', 'tools/')


def _manifest(rows):
    """rows: (relative path, 'file'|'symlink', sha256 or target, executable bool).
    Only recipes/, files/ and tools/ form the tree of a release (INTERFACE 5 and 7);
    returns (digest, rows counted, rows outside those parts)."""
    inside = sorted(r for r in rows if r[0].startswith(TREE_PARTS))
    text = ''.join(f'{p}\0{k}\0{v}\0{"x" if x else "-"}\n' for p, k, v, x in inside)
    return _sha(text.encode()), len(inside), len(rows) - len(inside)


def tree_manifest_local(top):
    """The same manifest for a release tree on this computer (git archive of a tag)."""
    rows = []
    top = os.path.realpath(top)
    for dp, dns, fns in os.walk(top):
        for n in dns + fns:
            full = os.path.join(dp, n)
            rel = os.path.relpath(full, top)
            st = os.lstat(full)
            if stat.S_ISLNK(st.st_mode):
                rows.append((rel, 'symlink', os.readlink(full), False))
            elif stat.S_ISREG(st.st_mode):
                rows.append((rel, 'file', _file_sha256(full), bool(st.st_mode & 0o111)))
    d, n, other = _manifest(rows)
    return {'manifest': d, 'files': n, 'outside_parts': other}


def _version_id(text):
    m = re.search(r'^VERSION_ID="?([^"\n]*)"?$', text or '', re.M)
    return m.group(1) if m else None


def _disk_tree(fs, ino, path, work):
    """Manifest of a tree on the system partition; files are read from a dump, modes and
    kinds from the debugfs listing. The release it carries is read from its own
    files/base-files/etc/os-release (VERSION_ID)."""
    _, ents = fs.walk(ino, '')
    out = os.path.join(work, 'tree-' + uuid.uuid4().hex[:8])
    os.mkdir(out)
    dump = fs.rdump(ino, out)
    _make_accessible(dump)
    rows, vid = [], None
    for p, m in sorted(ents.items()):
        rel = p.lstrip('/')
        if stat.S_ISREG(m[1]):
            try:
                rows.append((rel, 'file', _file_sha256(os.path.join(dump, rel)), bool(m[1] & 0o111)))
            except OSError as exc:
                fs.err(f'system{path}/{rel}: {exc}')
            if rel == 'files/base-files/etc/os-release':
                try:
                    vid = _version_id(_read_local(os.path.join(dump, rel)).decode(errors='replace'))
                except (OSError, ValueError):
                    pass
        elif stat.S_ISLNK(m[1]):
            try:
                rows.append((rel, 'symlink', os.readlink(os.path.join(dump, rel)), False))
            except OSError as exc:
                fs.err(f'system{path}/{rel}: {exc}')
    _rmtree(out)
    d, n, other = _manifest(rows)
    return {'path': path, 'manifest': d, 'files': n, 'outside_parts': other, 'version_id': vid}


def read_disk(raw_path, work_dir, subid=None, keep=False, copy_system=False):
    """External read-only reading of a ConfOS raw disk (INTERFACE.md section 7).

    subid is accepted for callers that pass a subordinate id range; it is not needed, because
    owners and modes come from debugfs and unsquashfs listings, not from extracted files.
    copy_system forces the sparse-copy path for partition 2 as well (partition 3 is always
    copied and its journal replayed on the copy). Problems are reported in 'errors'.
    """
    errors = []
    ev = _Evidence()
    result = {'boot_cfg': None, 'selected': None, 'state_applied': None, 'generations': {},
              'system_store': {'packages': {}, 'archives': {}, 'tree_present': False, 'sources_count': 0,
                               'trees': [], 'sources': {}, 'other_entries': []},
              'data': {'objects': [], 'errors': [], 'root_meta': None, 'candidate': {},
                       'candidate_encoding': 'base64'},
              'system_root_meta': None, 'errors': errors,
              'evidence': {'commands': ev.commands, 'subid': 'not used: owners and modes are '
                           'read from debugfs and unsquashfs listings'}}
    evd = result['evidence']
    os.makedirs(work_dir, exist_ok=True)
    work = tempfile.mkdtemp(prefix='disk-read-', dir=work_dir)
    t0 = time.monotonic()
    try:
        for name in ('debugfs', 'e2fsck', 'unsquashfs'):
            try:
                _tool(name)
            except FileNotFoundError as exc:
                errors.append({'kind': 'stored', 'reason': str(exc)})
        if errors:
            return result
        try:
            parts = gpt_partitions(raw_path)
        except (OSError, ValueError) as exc:
            errors.append({'kind': 'stored', 'reason': f'partition table: {exc}'})
            return result
        evd['partitions'] = parts
        for e in check_layout(parts):
            errors.append({'kind': 'stored', 'reason': e})
        nums = {p['number']: p for p in parts}
        if 2 in nums:
            sysfs = _open_ext(raw_path, nums[2], 2, work, ev, errors, evd, copy_system)
            if sysfs:
                _read_system(sysfs, result, work, keep)
        if 3 in nums:
            dfs = _open_ext(raw_path, nums[3], 3, work, ev, errors, evd, True)
            if dfs:
                _read_data(dfs, result, work)
        return result
    finally:
        evd['seconds'] = round(time.monotonic() - t0, 3)
        if keep:
            evd['work'] = work
        else:
            _rmtree(work)


def _read_system(fs, result, work, keep):
    errors = result['errors']
    root_lists = fs.listdirs([2])
    top = {r[0]: r[1:] for r in root_lists.get(2, [])}
    if '.' in top:
        ino, mode, uid, gid, _ = top['.']
        result['system_root_meta'] = {'mode': '%04o' % stat.S_IMODE(mode), 'uid': uid, 'gid': gid}
    known = {'.', '..', 'lost+found', 'boot.cfg', 'generations', 'state', 'packages', 'tree', 'trees', 'sources'}
    for name in sorted(set(top) - known):
        ino, mode, uid, gid, size = top[name]
        result['system_store']['other_entries'].append(
            {'path': '/' + name, 'mode': '%04o' % stat.S_IMODE(mode), 'uid': uid, 'gid': gid,
             'type': 'dir' if stat.S_ISDIR(mode) else 'file' if stat.S_ISREG(mode) else 'other'})

    def small_text(meta, what):
        if meta is None or not stat.S_ISREG(meta[1]):
            return None
        sha, data = fs.cat(meta[0], meta[4], keep=True)
        if data is None:
            return None
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            fs.err(f'{what} is not UTF-8')
            return data.decode('utf-8', errors='replace')
    result['boot_cfg'] = small_text(top.get('boot.cfg'), 'boot.cfg')
    if result['boot_cfg'] is None:
        fs.err('boot.cfg missing or unreadable')
    else:
        ids = set(re.findall(r'(?:^|\s)confos\.generation=(\S+)', result['boot_cfg']))
        if len(ids) != 1:
            fs.err(f'boot.cfg names {len(ids)} generations')
        else:
            sel = ids.pop()
            result['selected'] = sel
            for kw, f in (('linux', 'vmlinuz'), ('initrd', 'initramfs')):
                if not re.search(rf'^{kw} /generations/{re.escape(sel)}/{f}(\s|$)', result['boot_cfg'], re.M):
                    fs.err(f'boot.cfg {kw} line does not name /generations/{sel}/{f}')
    st = top.get('state')
    if st and stat.S_ISDIR(st[1]):
        _, ents = fs.walk(st[0], '')
        result['state_applied'] = small_text(ents.get('/applied'), 'state/applied')
    pk = top.get('packages')
    if pk and stat.S_ISDIR(pk[1]):
        lists = fs.listdirs([pk[0]])
        for name, ino, mode, uid, gid, size in lists.get(pk[0], []):
            if name in ('.', '..'):
                continue
            if stat.S_ISREG(mode) and name.endswith('.confpkg'):
                sha, data = fs.cat(ino, size, keep=True)
                if sha:
                    result['system_store']['packages'][name] = sha
                    result['system_store']['archives'][name] = dict(archive_passport(data, name), sha256=sha)
            else:
                result['system_store']['other_entries'].append({'path': '/packages/' + name})
    else:
        fs.err('packages/ missing')
    tr = top.get('tree')
    result['system_store']['tree_present'] = bool(tr and stat.S_ISDIR(tr[1]))
    if tr and stat.S_ISDIR(tr[1]):
        sub = {r[0] for r in fs.listdirs([tr[0]]).get(tr[0], [])}
        result['system_store']['tree_parts'] = sorted(sub & {'recipes', 'files', 'tools'})
        result['system_store']['trees'].append(_disk_tree(fs, tr[0], '/tree', work))
    trs = top.get('trees')
    if trs and stat.S_ISDIR(trs[1]):
        for name, ino, mode, uid, gid, size in sorted(fs.listdirs([trs[0]]).get(trs[0], [])):
            if name in ('.', '..'):
                continue
            if stat.S_ISDIR(mode):
                result['system_store']['trees'].append(dict(_disk_tree(fs, ino, '/trees/' + name, work), release=name))
            else:
                result['system_store']['other_entries'].append({'path': '/trees/' + name})
    so = top.get('sources')
    if so and stat.S_ISDIR(so[1]):
        rows = [r for r in fs.listdirs([so[0]]).get(so[0], []) if r[0] not in ('.', '..')]
        result['system_store']['sources_count'] = len(rows)
        for name, ino, mode, uid, gid, size in sorted(rows):
            if stat.S_ISREG(mode):
                sha, _ = fs.cat(ino, size)
                result['system_store']['sources'][name] = sha
            else:
                result['system_store']['other_entries'].append({'path': '/sources/' + name})
    gens = top.get('generations')
    if not gens or not stat.S_ISDIR(gens[1]):
        fs.err('generations/ missing')
        return
    glist = [r for r in fs.listdirs([gens[0]]).get(gens[0], []) if r[0] not in ('.', '..')]
    for k, (gid, gino, gmode, *_r) in enumerate(sorted(glist)):
        g = {'declaration_files': {}, 'declaration_text': {}, 'root': {'objects': [], 'errors': []},
             'kernel_sha256': None, 'initramfs_sha256': None, 'root_sqfs_sha256': None,
             'passports': {}, 'texts': {}, 'links': {}, 'other_entries': []}
        result['generations'][gid] = g
        gerr = g['root']['errors']
        if not stat.S_ISDIR(gmode):
            gerr.append({'kind': 'stored', 'reason': f'generations/{gid} is not a directory'})
            continue
        root_meta, ents = fs.walk(gino, '')
        kids = _children(ents, '')
        for name in sorted(set(kids) - {'root.sqfs', 'vmlinuz', 'initramfs', 'declaration'}):
            g['other_entries'].append(name)
        for key, name in (('kernel_sha256', 'vmlinuz'), ('initramfs_sha256', 'initramfs')):
            m = kids.get(name)
            if m and stat.S_ISREG(m[1]):
                g[key], _ = fs.cat(m[0], m[4])
            else:
                gerr.append({'kind': 'stored', 'reason': f'generations/{gid}/{name} missing'})
        for p, m in sorted(ents.items()):
            if p.startswith('/declaration/') and stat.S_ISREG(m[1]):
                rel = p[len('/declaration/'):]
                sha, data = fs.cat(m[0], m[4], keep=True)
                if data is not None:
                    g['declaration_files'][rel] = sha
                    g['declaration_text'][rel] = data.decode('utf-8', errors='replace')
            elif p.startswith('/declaration/') and not stat.S_ISDIR(m[1]):
                gerr.append({'kind': 'stored', 'reason': f'generations/{gid}{p}: not a regular file'})
        if '/declaration' not in ents:
            gerr.append({'kind': 'stored', 'reason': f'generations/{gid}/declaration missing'})
        m = kids.get('root.sqfs')
        if not m or not stat.S_ISREG(m[1]):
            gerr.append({'kind': 'stored', 'reason': f'generations/{gid}/root.sqfs missing'})
            continue
        sq = os.path.join(work, f'gen{k}.sqfs')
        if not fs.dump(m[0], sq, m[4]):
            gerr.append({'kind': 'stored', 'reason': f'generations/{gid}/root.sqfs not dumped'})
            continue
        g['root_sqfs_sha256'] = _file_sha256(sq)
        tree = os.path.join(work, f'gen{k}-root')
        r = read_squashfs(sq, tree, fs.ev)
        g['root']['objects'] = r['objects']
        gerr.extend(r['errors'])
        g['root']['root_meta'] = r['root_meta']
        if r['tree']:
            _make_accessible(tree)
            g['passports'], g['texts'], g['links'] = _root_texts(tree, r['objects'], gerr)
        if not keep:
            _rmtree(tree)
            os.unlink(sq)


def _read_data(fs, result, work):
    data = result['data']
    root_meta, ents = fs.walk(2, '')
    if root_meta:
        data['root_meta'] = {'mode': '%04o' % stat.S_IMODE(root_meta[1]), 'uid': root_meta[2],
                             'gid': root_meta[3]}
    out = os.path.join(work, 'data-dump')
    os.mkdir(out)
    dump_root = fs.rdump(2, out)
    _make_accessible(dump_root)
    objs = _ext_objects(fs, ents, dump_root, '/data', data['errors'])
    if data['root_meta']:
        objs.insert(0, {'kind': 'dir', 'id': '/data', 'value': dict(data['root_meta'])})
    data['objects'] = objs
    for o in objs:
        oid = o['id']
        if (o['kind'] in ('file', 'hardlink') and oid.startswith('/data/confos/')
                and not (oid == '/data/confos/work' or oid.startswith('/data/confos/work/'))):
            rel = oid[len('/data/confos/'):]
            try:
                data['candidate'][rel] = base64.b64encode(_read_local(dump_root + oid[len('/data'):])).decode()
            except (OSError, ValueError) as exc:
                data['errors'].append({'kind': 'stored', 'reason': f'{oid}: {exc}'})
    _rmtree(out)


# ------------------------------------------------------------------ inventory
def inventory_from_disk(disk_info):
    """Harness inventory (objects, errors, coverage) of the stored state of a disk.

    Root objects of the selected generation keep their ids in the image (e.g. '/usr/bin/bash').
    Partition 3 objects keep their raw ids ('/data/home/<account>/<file>', '/data/root/...', '/data/confos/...');
    the caller maps bind mounts. The root directories of partitions 2 and 3 (mounted at /system
    and /data) are kind 'partition-root', classification 'mount-point', so that they do not
    collide with the mount-point directories /system and /data of the image.
    """
    objects, errors = [], []
    errors.extend(disk_info.get('errors', []))
    sel = disk_info.get('selected')
    gens = disk_info.get('generations', {})
    if sel is None:
        errors.append({'kind': 'stored', 'reason': 'no selected generation'})
    elif sel not in gens:
        errors.append({'kind': 'stored', 'reason': f'selected generation {sel} not on the disk'})
    for gid, g in sorted(gens.items()):
        errors.extend(g.get('root', {}).get('errors', []))
        if gid == sel:
            objects.extend(g['root']['objects'])
            objects.append({'kind': 'system-store', 'id': f'/system/generations/{gid}',
                            'classification': 'system-store', 'question': 'Q-GENERATION',
                            'value': {'selected': True, 'identity': gid, 'declaration_files': g['declaration_files'],
                                      'kernel_sha256': g['kernel_sha256'],
                                      'initramfs_sha256': g['initramfs_sha256'],
                                      'root_sqfs_sha256': g.get('root_sqfs_sha256')}})
        else:
            objects.append({'kind': 'generation', 'id': gid, 'classification': 'inactive-generation',
                            'question': 'Q-GENERATION',
                            'value': {'declaration_files': g['declaration_files'],
                                      'kernel_sha256': g['kernel_sha256'],
                                      'initramfs_sha256': g['initramfs_sha256'],
                                      'root_sqfs_sha256': g.get('root_sqfs_sha256'),
                                      'root_objects': len(g['root']['objects'])}})
    if disk_info.get('system_root_meta'):
        objects.append({'kind': 'partition-root', 'id': '/system', 'classification': 'mount-point',
                        'value': dict(disk_info['system_root_meta'])})
    store = disk_info.get('system_store', {})
    applied = disk_info.get('state_applied')
    boot = disk_info.get('boot_cfg')
    # What a line brings is compared object by object (the archive of a named package, the
    # tree and the sources of the release named by `base`, the generation in force); what no
    # line names stays with QUESTIONS Q-GENERATION (the classification below is used only
    # for objects that the derivation does not expect).
    for oid, value in (('/system/boot.cfg', {'sha256': _sha(boot.encode()) if boot is not None else None,
                                             'selected': sel}),
                       ('/system/state/applied', {'text': applied,
                                                  'identity': applied.strip() if applied is not None else None})):
        objects.append({'kind': 'system-store', 'id': oid, 'classification': 'system-store',
                        'question': 'Q-GENERATION', 'value': value})
    archives = store.get('archives', {})
    for name, sha in sorted(store.get('packages', {}).items()):
        value = dict(archives.get(name, {}), sha256=sha)
        objects.append({'kind': 'system-archive', 'id': '/system/packages/' + name,
                        'classification': 'system-store', 'question': 'Q-GENERATION', 'value': value})
    used = set()
    for t in store.get('trees', []):
        rel = t.get('release') or t.get('version_id') or t['path']
        if rel in used:                       # the same release twice: the second is its own object
            rel = rel + '@/system' + t['path']
        used.add(rel)
        objects.append({'kind': 'release-tree', 'id': rel, 'classification': 'system-store',
                        'question': 'Q-GENERATION',
                        'value': {'manifest': t['manifest'], 'files': t['files'], 'path': '/system' + t['path'],
                                  'outside_parts': t.get('outside_parts'),
                                  'version_id': t.get('version_id')}})
    for name, sha in sorted(store.get('sources', {}).items()):
        objects.append({'kind': 'release-source', 'id': name, 'classification': 'system-store',
                        'question': 'Q-GENERATION', 'value': {'sha256': sha}})
    for e in store.get('other_entries', []):
        objects.append({'kind': 'system-store', 'id': '/system' + e['path'],
                        'classification': 'system-store', 'question': 'Q-GENERATION',
                        'value': dict(e, unexpected=True)})
    data = disk_info.get('data', {})
    errors.extend(data.get('errors', []))
    for o in data.get('objects', []):
        if o['id'] == '/data' and o['kind'] == 'dir':
            objects.append(dict(o, kind='partition-root', classification='mount-point'))
        else:
            objects.append(o)
    seen, unique = set(), []
    for o in objects:
        key = (o['kind'], o['id'])
        if key in seen:
            errors.append({'kind': 'stored', 'reason': f'duplicate object {key}'})
            continue
        seen.add(key)
        unique.append(o)
    n_root = len(gens.get(sel, {}).get('root', {}).get('objects', [])) if sel in gens else 0
    evidence = (f'external read-only raw disk read (GPT, debugfs, unsquashfs); generation {sel}; '
                f'{n_root} root objects, {len(data.get("objects", []))} data objects, '
                f'{len(gens)} generations')
    return {'objects': unique, 'errors': errors,
            'coverage': {'stored': {'status': 'complete' if not errors else 'incomplete',
                                    'evidence': evidence}}}

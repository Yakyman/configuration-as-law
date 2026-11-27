# SPDX-License-Identifier: MIT
"""Native binding of the adapter: ConfOS 0.67, as documented by the builder's INTERFACE.md.

adapter.py, adapter_native.py and adapter_disk.py are the one adapter: the only code
that knows how the system is built, booted, reached and read. engine.py/core.py stay
portable. Nothing here decides a verdict; it returns raw observations with the exact
commands and outputs. A facility that 0.67 does not have raises Unavailable with the
documented reason (an unobserved row), never a refusal. BINDING.md lists every choice.
"""
import base64, fcntl, hashlib, json, os, re, shlex, shutil, socket, subprocess, time, uuid
from pathlib import Path

from adapter import Unavailable

HERE = Path(__file__).resolve().parent
RELEASE = '0.67'
# Same arity table as the release's confos program (files/confos/confos, ARITY).
ARITY = {'base': (2, 4), 'include': (2, 2), 'package': (3, 4), 'account': (7, 7), 'group': (3, 3),
         'authorized-key': (4, 4), 'password': (3, 3), 'file': (5, 6), 'compile': (5, 99),
         'setting': (3, 3), 'network': (3, 4), 'service': (4, 99), 'rule': (3, 3), 'open': (2, 2)}
SECTOR = 512
SYSTEM_FIRST = 264192          # INTERFACE 7: partition 2 (CONFOS-SYSTEM)
DATA_FIRST = 12847104          # INTERFACE 7: partition 3 (CONFOS-DATA)
MAIN = 'declaration.conf'
CANDIDATE_DIR = '/data/confos'
TOKEN = re.compile(r'@[A-Z0-9_]+(?::[A-Za-z0-9._-]+)?@')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canon(fields):
    return ' '.join(shlex.quote(f) for f in fields)


def tool(name):
    found = shutil.which(name) or shutil.which(name, path='/usr/sbin:/sbin')
    if not found:
        raise Unavailable('host tool missing: ' + name)
    return found


# ----------------------------------------------------------------- declarations

def _is_decl_file(rel):
    """A file of the description (main file or include) rather than an input beside it; the
    trees an update brings hold .conf files of their own (declarations/), which are inputs."""
    return rel.endswith('.conf') and '/' not in rel


class NativeDecl:
    """All files of one native description plus the input files beside it."""

    def __init__(self, files, inputs=None, main=MAIN):
        self.files = dict(files)          # rel -> bytes (declaration files)
        self.inputs = dict(inputs or {})  # rel -> bytes (recipes, sources, file sources)
        self.main = main
        self.rows, self.order = self._parse()

    def _parse(self):
        rows, order = [], []
        def read(rel):
            if rel in order or rel.startswith('..') or rel.startswith('/'):
                raise ValueError('include %s: outside the folder or included twice' % rel)
            if rel not in self.files:
                raise ValueError('include %s: no such file' % rel)
            order.append(rel)
            for n, line in enumerate(self.files[rel].decode('utf-8').splitlines(), 1):
                f = shlex.split(line, comments=True)
                if not f:
                    continue
                lo, hi = ARITY.get(f[0], (0, -1))
                if not lo <= len(f) <= hi:
                    raise ValueError('%s:%d: unknown line kind or wrong number of fields' % (rel, n))
                if f[0] == 'include':
                    read(f[1])
                else:
                    rows.append((rel, n, f))
        read(self.main)
        return rows, order

    @property
    def identity(self):
        """INTERFACE 5 "Identity": one file -> SHA-256 of its bytes; several -> of the list."""
        if len(self.order) == 1:
            return sha(self.files[self.order[0]])
        h = hashlib.sha256()
        for rel in self.order:
            h.update(rel.encode() + b'\0' + sha(self.files[rel]).encode() + b'\n')
        return h.hexdigest()

    def lines(self):
        return [canon(f) for _, _, f in self.rows]

    def kind(self, k):
        return [f for _, _, f in self.rows if f[0] == k]

    def replace_text(self, rel, text):
        files = dict(self.files)
        files[rel] = text.encode()
        return NativeDecl(files, self.inputs, self.main)


def whole_tree_digest(top):
    """Every regular file of a release tree (git archive of a tag): SHA-256 of the sorted lines
    `path NUL sha256 NUL x-or-dash`, the file count and the contents. The binding records only
    the digest and the count; the brought folder must be exactly this tree (its checksum, by
    the release's own `confpkg treesum`, is on the base line)."""
    top = Path(top)
    content, lines = {}, []
    for f in sorted(top.rglob('*')):
        if f.is_symlink() or not f.is_file():
            if f.is_symlink():
                raise Unavailable('a link in the release tree is not expected: %s' % f.relative_to(top))
            continue
        rel = str(f.relative_to(top))
        data = f.read_bytes()
        x = bool(f.stat().st_mode & 0o111)
        content[rel] = (data, x)
        lines.append('%s\0%s\0%s\n' % (rel, sha(data), 'x' if x else '-'))
    return {'digest': hashlib.sha256(''.join(lines).encode()).hexdigest(), 'files': len(content), 'content': content}


class Bindings:
    """Frozen binding files plus private values (local.env); token expansion."""

    def __init__(self, private=None, root=HERE):
        self.root = Path(root)
        self.release = json.loads((self.root / 'bindings/release-0.67.json').read_text())
        self.cmd = json.loads((self.root / 'bindings/commands-0.67.json').read_text())
        self.private = dict(private or {})
        self.local = {}                 # private machine paths (local.env native): update trees, sources
        self.exec_inputs = set()        # input files written executable (trees brought by an update)
        for rel, want in self.release['payload_sha256'].items():
            if sha((self.root / 'payloads' / rel).read_bytes()) != want:
                raise ValueError('payload changed after binding freeze: ' + rel)

    def payload(self, rel):
        p = (self.root / rel).resolve()
        if not p.is_relative_to(self.root / 'payloads'):
            raise ValueError('payload outside payloads/: ' + rel)
        return p.read_bytes()

    def slot(self, name):
        s = self.release['lines'].get(name)
        if s is None:
            raise Unavailable('binding slot not defined for 0.67: ' + name)
        if 'unsupported' in s:
            raise Unavailable(s['unsupported'])
        return s

    def variant(self, case, variant):
        if variant is None:
            return {}
        v = self.cmd['variants'].get(case, {}).get(variant)
        if v is None:
            return {}
        if 'unsupported' in v:
            raise Unavailable(v['unsupported'])
        if 'covered_by' in v:
            raise Unavailable('variant is the same route as ' + v['covered_by'] + '; observed there, not here')
        return v

    def expand(self, text, extra=None):
        """Replace tokens; returns (text, preludes). Unknown or unsupported -> Unavailable."""
        table = dict(self.cmd['tokens'])
        table.update(extra or {})
        preludes = []
        for _ in range(6):
            found = TOKEN.findall(text)
            if not found:
                return text, preludes
            for t in found:
                if t.startswith('@SHA:'):
                    value = sha(self.payload('payloads/' + t[5:-1]))
                elif t in table:
                    value = table[t]
                    if isinstance(value, dict):
                        if value.get('prelude') and value['prelude'] not in preludes:
                            preludes.append(value['prelude'])
                        value = value['text']
                elif t in self.private:
                    value = self.private[t]
                elif t in self.cmd['unsupported_tokens']:
                    raise Unavailable('token %s: %s' % (t, self.cmd['unsupported_tokens'][t]))
                elif t in self.cmd['private_tokens']:
                    raise Unavailable('private token %s not set in local.env' % t)
                else:
                    raise Unavailable('unbound token ' + t)
                text = text.replace(t, str(value))
        raise ValueError('token expansion does not terminate: ' + text)

    def shell(self, text, extra=None):
        """Typed shell text with the needed preludes prepended (all typed, nothing saved)."""
        body, preludes = self.expand(text, extra)
        pre = [self.cmd['preludes'][p] for p in preludes]
        if 'case_fetch' in body and self.cmd['preludes']['case_fetch'] not in pre:
            pre.append(self.cmd['preludes']['case_fetch'])
        return '; '.join(pre + [body])

    # semantic line -> native lines and inputs
    def update_inputs(self, s):
        """The tree of an update state and the sources it adds (INTERFACE 9), read from the
        private copies named in local.env and checked against the frozen binding."""
        inputs = {}
        ti = s.get('tree_input')
        if ti:
            host = (self.local.get('update_trees') or {}).get(ti['state'])
            if not host:
                raise Unavailable('local.env names no tree for update state ' + ti['state'])
            whole = whole_tree_digest(host)
            if whole['digest'] != ti['whole_tree_sha256'] or whole['files'] != ti['files']:
                raise Unavailable('tree of %s differs from the binding' % ti['release'])
            for rel, (data, x) in whole['content'].items():
                inputs[ti['folder'] + '/' + rel] = data
                if x:
                    self.exec_inputs.add(ti['folder'] + '/' + rel)
        for fname, fsha in (s.get('source_inputs') or {}).items():
            src = self.local.get('sources')
            data = (Path(src) / fname).read_bytes() if src else b''
            if sha(data) != fsha:
                raise Unavailable('source %s missing or differs from the binding' % fname)
            inputs[fname] = data
        return inputs

    def update_input_names(self):
        names = set()
        for v in self.release['lines'].values():
            if isinstance(v, dict) and v.get('tree_input'):
                names.add(v['tree_input']['folder'])
                names.update(v.get('source_inputs') or {})
        return names

    def native_for(self, line, order=None):
        k = line['kind']
        if k == 'base':
            s = self.slot(line['binding'])
            return [self.expand(n)[0] for n in s['native']], self.update_inputs(s)
        if k == 'binding' or (k == 'package' and 'binding' in line):
            name = line.get('name') if k == 'binding' else line['binding']
            s = self.slot(name)
            if 'order_items' in s:
                native = sum((s['order_items'][i] for i in (order or sorted(s['order_items']))), [])
            else:
                native = list(s['native'])
            inputs = {rel: self.payload(src) for rel, src in s.get('inputs', {}).items()}
            return [self.expand(n)[0] for n in native], inputs
        if k == 'file':
            path = self.expand(line['path'])[0]
            data = line['text'].encode()
            rel = 'files/' + line['id']
            return ['file %s %s %d:%d %s %s' % (path, line['mode'], line['uid'], line['gid'], sha(data), rel)], {rel: data}
        if k == 'open-folder':
            if line.get('scope', 'execute') != 'execute':
                raise Unavailable('0.67 open lines have one scope (execute)')
            return ['open ' + self.expand(line['path'])[0]], {}
        if k == 'radio':
            raise Unavailable('INTERFACE 5: no saved Wi-Fi networks or Bluetooth pairings in 0.67')
        if k == 'external-accounts':
            raise Unavailable('INTERFACE 5: no account server (question 9)')
        if k == 'container':
            raise Unavailable('no container runtime in 0.67 (EXECUTORS.md)')
        if k == 'prohibition':
            raise Unavailable('INTERFACE 5: there is no prohibition line in 0.67')
        raise Unavailable('no native 0.67 line for semantic kind ' + k)

    def render(self, declaration, order=None):
        lines, inputs = [], {}
        for line in declaration['lines']:
            native, ins = self.native_for(line, order)
            lines += native
            for rel, data in ins.items():
                if rel in inputs and inputs[rel] != data:
                    raise ValueError('two inputs with one name: ' + rel)
                inputs[rel] = data
        text = '# Case declaration, rendered from semantic lines by the case party adapter.\n' + \
               '\n'.join(lines) + '\n'
        return NativeDecl({MAIN: text.encode()}, inputs)


# ------------------------------------------------- independent derivation inputs

def recipe_sources(text):
    return [l.split()[1:3] for l in text.splitlines() if l.startswith('source:')]


_MANIFESTS = {}


def _tree_manifest(path):
    import adapter_disk
    key = str(Path(path).resolve())
    if key not in _MANIFESTS:
        _MANIFESTS[key] = adapter_disk.tree_manifest_local(key)['manifest']
    return _MANIFESTS[key]


def release_sources(tree):
    """{file name: sha256} the `base` line brings into /system/sources (INTERFACE 7 of 0.67):
    every source file a recipe of the release names by a plain file name (`source:` lines;
    a folder of the tree such as `tools` or `files/...` is not a source file)."""
    out = {}
    tree = Path(tree)
    for rp in sorted((tree / 'recipes').glob('*.recipe')):
        for name, ssha in recipe_sources(rp.read_text()):
            if '/' not in name and not (tree / name).is_dir():
                if out.get(name, ssha) != ssha:
                    raise ValueError('two recipes name %s with different checksums' % name)
                out[name] = ssha
    return out


def semantic_from_native(decl, tree=None, store=None, layout=None, derivation=None, trees=None):
    """Native rows -> semantic lines for core.derive. Reads no machine.

    tree: the release tree (recipes/); trees: {release: tree} of every release a `base`
    line may name (the update states); store: {archive name: sha256} of the independently
    built package folder. Values the line leaves open (auto UID) are not promised.
    With a layout (a final comparison) the objects the lines bring onto the system
    partition are derived too (INTERFACE 7 and 9): the archive of every named package,
    the tree and the sources of the release named by `base`, the generation in force.
    """
    out, errors = [], []
    trees = dict(trees or {})
    if tree and RELEASE not in trees:
        trees[RELEASE] = tree
    base_rows = [(rel, n, f) for rel, n, f in decl.rows if f[0] == 'base']
    base_release = base_rows[0][2][1] if base_rows else None
    rtree = trees.get(base_release) if base_release else tree
    def obj(lid, kind, oid, value):
        out.append({'id': lid, 'kind': 'object', 'object': {'kind': kind, 'id': oid, 'value': value}})
    for i, (rel, n, f) in enumerate(decl.rows):
        lid = '%s:%d' % (rel, n)
        k = f[0]
        if k == 'base':
            if layout is not None:
                if not rtree:
                    errors.append({'line': lid, 'reason': 'tree of release %s not available to the deriver' % f[1]})
                    continue
                obj('release-tree:' + lid, 'release-tree', f[1], {'manifest': _tree_manifest(rtree)})
                for fname, ssha in sorted(release_sources(rtree).items()):
                    obj('release-source:%s:%s' % (lid, fname), 'release-source', fname, {'sha256': ssha})
            continue
        if k == 'package':
            name, version = f[1], f[2]
            if len(f) == 4:
                rtext = decl.inputs.get(f[3])
            else:
                rp = Path(rtree) / 'recipes' / (name + '.recipe') if rtree else None
                rtext = rp.read_bytes() if rp and rp.is_file() else None
            if rtext is None:
                errors.append({'line': lid, 'reason': 'recipe of package %s not available to the deriver' % name})
                out.append({'id': lid, 'kind': 'binding', 'name': 'recipe:' + name})
                continue
            archive = '%s-%s.confpkg' % (name, version)
            pairs = sorted([x[0].rstrip('/').split('/')[-1], x[1]] for x in recipe_sources(rtext.decode()))
            out.append({'id': lid, 'kind': 'package', 'name': name, 'version': version,
                        'recipe_sha256': sha(rtext), 'source_sha256': pairs,
                        'archive': archive, 'archive_sha256': (store or {}).get(archive)})
            if layout is not None:     # INTERFACE 8: the archive the line brings into the store
                obj('release-store:' + lid, 'system-archive', '/system/packages/' + archive,
                    {'name': name, 'version': version, 'recipe_sha256': sha(rtext), 'sources': pairs})
        elif k == 'account':
            _, name, uid, gid, groups, shell, home = f
            value = {'shell': shell, 'home': home, 'groups': sorted(g for g in groups.split(',') if g != '-')}
            if uid != 'auto':
                value['uid'] = int(uid)
            if gid != 'auto':
                value['gid'] = int(gid)
            obj(lid, 'account', name, value)
            home_value = {k2: value[k2] for k2 in ('uid', 'gid') if k2 in value}
            declared_groups = {g[1] for g in decl.kind('group')}
            base_groups = {o['id'] for o in (layout or []) if o['kind'] == 'group'}
            if name not in declared_groups | base_groups:   # accounts() makes the account's group
                obj(lid + ':group', 'group', name, {'gid': int(gid)} if gid != 'auto' else {})
            if home.startswith('/home/'):     # boot-prepare makes the home on the data partition
                obj(lid + ':home', 'dir', '/data' + home, home_value)
        elif k == 'group':
            obj(lid, 'group', f[1], {'gid': int(f[2])})
        elif k == 'password':
            obj(lid, 'password', f[1], {'set': f[2] not in ('*', '!')})
        elif k == 'authorized-key':
            obj(lid, 'ssh-key', '%s %s %s' % (f[1], f[2], f[3]), {})
        elif k == 'file':
            path, mode = f[1], f[2]
            uid, gid = (map(int, f[3].split(':')) if len(f) == 6 else (0, 0))
            obj(lid, 'file', path, {'sha256': f[-2], 'mode': mode.zfill(4), 'uid': uid, 'gid': gid})
            if path.startswith('/etc/sudoers.d/'):
                obj(lid + ':rights', 'access', path, {'sha256': f[-2]})
        elif k == 'compile':
            obj(lid, 'file', f[1], {'mode': f[2].zfill(4)})
        elif k == 'setting':
            name, value = f[1], f[2]
            if name == 'hostname':
                obj(lid, 'hostname', 'hostname', {'name': value})
            elif name == 'timezone':
                obj(lid, 'time', 'timezone', {'zone': value})
            elif name == 'locale':
                obj(lid, 'locale', 'LANG', {'value': value})
            elif name.startswith('sysctl:'):
                obj(lid, 'sysctl', name[7:], {'value': value})
            else:
                errors.append({'line': lid, 'reason': 'setting not known to the deriver: ' + name})
        elif k == 'network':
            obj(lid, 'network', f[2], {'gateway': f[3]} if len(f) == 4 else {})
        elif k == 'service':
            obj(lid, 'service', f[1], {'state': f[2], 'argv': f[3:]})
        elif k == 'rule':
            # INTERFACE 5: the value adds one statement to chain input of table inet confos; the
            # name is the declaration's label, the statement is what is in force
            stmt = f[2][len('add rule inet confos input '):] if f[2].startswith('add rule inet confos input ') else f[2]
            obj(lid, 'firewall-rule', ' '.join(stmt.split()), {})
        elif k == 'open':
            out.append({'id': lid, 'kind': 'open-folder', 'path': f[1], 'scope': 'execute'})
            obj(lid + ':mount', 'mount', f[1], {'noexec': False, 'ro': False})
        else:
            errors.append({'line': lid, 'reason': 'native kind not known to the deriver: ' + k})
    names = {f[1] for f in decl.kind('setting')}
    for name, kind, oid, value in (('hostname', 'hostname', 'hostname', {'name': 'confos'}),
                                   ('timezone', 'time', 'timezone', {'zone': 'Etc/UTC'}),
                                   ('locale', 'locale', 'LANG', {'value': 'C.UTF-8'})):
        if name not in names:                 # INTERFACE 5: the default of the setting line
            out.append({'id': 'release-default:' + name, 'kind': 'object', 'object': {'kind': kind, 'id': oid, 'value': value}})
    for item in (layout or []):
        out.append({'id': 'release-layout:%s:%s' % (item['kind'], item['id']), 'kind': 'object', 'object': item})
    if layout is not None:   # INTERFACE 7: the generation of this declaration, selected by boot.cfg
        for oid, value in (('/system/generations/' + decl.identity, {'selected': True, 'identity': decl.identity}),
                           ('/system/boot.cfg', {'selected': decl.identity}),
                           ('/system/state/applied', {'identity': decl.identity})):
            out.append({'id': 'selected-generation:' + oid, 'kind': 'object', 'object': {'kind': 'system-store', 'id': oid, 'value': value}})
    seen = {l['id'] for l in out}
    for e in errors:
        if e['line'] not in seen:
            out.append({'id': e['line'], 'kind': 'binding', 'name': e['reason']})
    overlay = rendered_paths(decl, derivation) if derivation else {}
    for path, kind in sorted(overlay.items()):
        if kind == 'file' and path.startswith('/home/'):
            out.append({'id': 'home-file-mount:' + path, 'kind': 'object',
                        'object': {'kind': 'mount', 'id': path, 'value': {'fstype': 'squashfs', 'ro': True}}})
    for f in decl.kind('file'):
        if f[1].startswith('/home/'):
            out.append({'id': 'home-file-mount:' + f[1], 'kind': 'object',
                        'object': {'kind': 'mount', 'id': f[1], 'value': {'fstype': 'squashfs', 'ro': True}}})
    for l in out:
        if l['kind'] == 'package':
            l['overlay'] = sorted(overlay)
    for path, kind in sorted(overlay.items()):
        out.append({'id': 'rendered:' + path, 'kind': 'object', 'object': {'kind': kind, 'id': path, 'value': {}}})
    return {'schema': 1, 'lines': out, 'native_errors': errors, 'identity': decl.identity, 'overlay': sorted(overlay)}


def rendered_paths(decl, d):
    """Paths the release's render() writes for this declaration, with their parent dirs."""
    paths = {p: 'file' for p in d['rendered_files']}
    paths.update({p: 'symlink' for p in d['rendered_links']})
    managed = {f[1] for f in decl.kind('file')} | {f[1] for f in decl.kind('compile')}
    for f in decl.kind('account'):
        if f[6].startswith('/home/'):
            for rel in d['startup_files']:
                if f[6] + '/' + rel not in managed:
                    paths[f[6] + '/' + rel] = 'file'
    for acct in {f[1] for f in decl.kind('authorized-key')}:
        paths['/etc/dropbear/authorized_keys/' + acct] = 'file'
    for rel in decl.order:
        paths['/etc/confos/declaration/' + rel] = 'file'
    for path in list(paths) + sorted(managed):
        parent = str(Path(path).parent)
        while parent != '/':
            paths.setdefault(parent, 'dir')
            parent = str(Path(parent).parent)
    return paths


def overlay_reader(reader, overlay):
    """render() replaces package files of the same path (put() unlinks first): only presence."""
    over = set(overlay)
    def read(line):
        local = over | set(line.get('overlay', []))
        out = []
        for o in reader(line):
            if o['id'] in local:
                o = dict(o, value={})
            elif o['id'].startswith('/usr/lib/confpkg/') and o['id'].endswith('.passport'):
                # its built-with line records the build environment, which a line does not
                # promise (rule 4: source and recipe, not bytes); the package object carries those
                o = dict(o, value={k: v for k, v in o['value'].items() if k != 'sha256'})
            out.append(o)
        return out
    return read


# ---------------------------------------------------------------- the machine

class Machine:
    """One QEMU guest, launched as scripts/boot.sh of the release does, plus a QMP socket.

    The QMP socket is the only addition (power cut and network link need it); the
    command line is recorded with each boot. A machine slot is taken first.
    """

    def __init__(self, config, disk, log_dir):
        self.c, self.disk, self.dir = config, Path(disk), Path(log_dir)
        self.proc = self.slot = None
        self.boots = 0

    def _take_slot(self):
        slots = Path(self.c['slots'])
        slots.mkdir(parents=True, exist_ok=True)
        for n in (1, 2, 3, 4):
            fd = open(slots / ('slot-%d.lock' % n), 'w')
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self.slot = fd
                return n
            except OSError:
                fd.close()
        raise Unavailable('no free machine slot (COMMON: at most 4 machines)')

    def start(self, timeout=300):
        if self.proc and self.proc.poll() is None:
            raise ValueError('machine already running')
        slot = self._take_slot() if self.slot is None else None
        self.boots += 1
        self.serial = self.dir / ('serial-%d.log' % self.boots)
        self.qmp = self.dir / ('qmp-%d.sock' % self.boots)
        vars_ = self.dir / ('vars-%d.fd' % self.boots)
        shutil.copyfile(self.c.get('ovmf_vars', '/usr/share/OVMF/OVMF_VARS_4M.fd'), vars_)
        mem = int(self.c.get('memory_mib', 4096))
        cpus = int(self.c.get('cpus', 2))
        if mem > 8192 or cpus > 4:
            raise ValueError('COMMON ceiling: test machines at most 8 GB and 4 vCPU')
        self.argv = [tool('qemu-system-x86_64'), '-enable-kvm', '-machine', 'q35', '-cpu', 'host',
                     '-smp', str(cpus), '-m', str(mem),
                     '-drive', 'if=pflash,format=raw,readonly=on,file=' + self.c.get('ovmf_code', '/usr/share/OVMF/OVMF_CODE_4M.fd'),
                     '-drive', 'if=pflash,format=raw,file=%s' % vars_,
                     '-drive', 'file=%s,format=raw,if=virtio,cache=unsafe' % self.disk,
                     '-netdev', 'user,id=n,hostfwd=tcp:127.0.0.1:%d-:22' % int(self.c['ssh_port']),
                     '-device', 'virtio-net-pci,netdev=n',
                     '-display', 'none', '-serial', 'file:%s' % self.serial, '-monitor', 'none',
                     '-qmp', 'unix:%s,server=on,wait=off' % self.qmp]
        self.proc = subprocess.Popen(self.argv, stdin=subprocess.DEVNULL,
                                     stdout=open(self.dir / ('qemu-%d.out' % self.boots), 'wb'), stderr=subprocess.STDOUT)
        self.started = time.monotonic()
        return {'argv': self.argv, 'slot': slot, 'serial': str(self.serial), 'started_monotonic': self.started}

    def serial_text(self):
        try:
            return self.serial.read_text(errors='replace')
        except OSError:
            return ''

    def wait_serial(self, pattern, timeout=300, since=0):
        end = time.monotonic() + timeout
        rx = re.compile(pattern, re.M)
        while time.monotonic() < end:
            text = self.serial_text()[since:]
            m = rx.search(text)
            if m:
                return m
            if 'CONFOS BOOT FAILED' in text:
                raise Unavailable('boot failed: ' + text[text.index('CONFOS BOOT FAILED'):][:300])
            if self.proc.poll() is not None:
                return None
            time.sleep(0.5)
        return None

    def qmp_cmd(self, command, **args):
        s = socket.socket(socket.AF_UNIX)
        s.settimeout(10)
        s.connect(str(self.qmp))
        f = s.makefile('rwb')
        def recv():
            while True:
                msg = json.loads(f.readline())
                if 'event' not in msg:
                    return msg
        recv()
        f.write(b'{"execute":"qmp_capabilities"}\n'); f.flush(); recv()
        f.write(json.dumps({'execute': command, 'arguments': args}).encode() + b'\n'); f.flush()
        reply = recv()
        s.close()
        return reply

    def power_cut(self):
        t = time.monotonic()
        self.proc.kill()
        self.proc.wait(timeout=30)
        return {'cut_monotonic': t, 'method': 'SIGKILL of the QEMU process (power cut)'}

    def stop(self, timeout=60):
        if self.proc and self.proc.poll() is None:
            try:
                self.qmp_cmd('quit')
            except OSError:
                pass
            try:
                self.proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                self.proc.kill(); self.proc.wait()
        if self.slot:
            self.slot.close(); self.slot = None


class SSH:
    """Guest commands over the forwarded port. INTERFACE 3: host key made at every boot."""

    def __init__(self, config):
        self.c = config

    def run(self, role, text, stdin=None, timeout=120, env=None, tty=False):
        if role not in ('user', 'root'):
            raise ValueError('unknown guest role ' + role)
        account = 'root' if role == 'root' else self.c.get('account', 'user')
        envtext = ' '.join('%s=%s' % (k, shlex.quote(v)) for k, v in sorted((env or {}).items()))
        remote = (envtext + ' ' if envtext else '') + 'sh -c ' + shlex.quote(text)
        argv = ['ssh', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=no',
                '-o', 'UserKnownHostsFile=/dev/null', '-o', 'LogLevel=ERROR', '-o', 'ConnectTimeout=10',
                '-i', self.c['ssh_key'], '-p', str(int(self.c['ssh_port']))] + (['-tt'] if tty else []) + \
               ['--', account + '@127.0.0.1', remote]
        start = time.monotonic()
        try:
            if tty and stdin is None:
                # A terminal session gets an input that stays open and empty until the session
                # ends: no typed bytes and no early end of input race the remote command.
                rfd, wfd = os.pipe()
                try:
                    proc = subprocess.Popen(argv, stdin=rfd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    os.close(rfd); rfd = None
                    try:
                        out, err = proc.communicate(timeout=timeout)
                    except subprocess.TimeoutExpired:
                        proc.kill(); proc.communicate()
                        raise
                    p = subprocess.CompletedProcess(argv, proc.returncode, out, err)
                finally:
                    if rfd is not None:
                        os.close(rfd)
                    os.close(wfd)
            else:
                io = {'input': stdin} if stdin is not None else {'stdin': subprocess.DEVNULL}
                p = subprocess.run(argv, capture_output=True, timeout=timeout, **io)
        except subprocess.TimeoutExpired as exc:
            raise Unavailable('guest command timeout, not refusal: ' + text[:200]) from exc
        if p.returncode == 255:
            raise Unavailable('SSH transport failed, not policy refusal: ' + p.stderr.decode(errors='replace')[-300:])
        return {'command': text, 'role': role, 'account': account, 'env': env or {}, 'returncode': p.returncode,
                'stdout': p.stdout.decode(errors='replace'), 'stderr': p.stderr.decode(errors='replace'),
                'started_monotonic': start, 'ended_monotonic': time.monotonic()}

    def wait(self, timeout=300):
        end = time.monotonic() + timeout
        last = None
        while time.monotonic() < end:
            try:
                return self.run('user', 'cat /proc/sys/kernel/random/boot_id', timeout=20)
            except Unavailable as exc:
                last = str(exc)
                time.sleep(2)
        raise Unavailable('guest not reachable over SSH: ' + str(last))


# ------------------------------------------------------------ external reading

def debugfs_cat(raw, first_sector, path):
    """Read one file of an ext4 partition of a raw disk, read-only, without the system."""
    argv = [tool('debugfs'), '-R', 'cat ' + path, '%s?offset=%d' % (raw, first_sector * SECTOR)]
    p = subprocess.run(argv, capture_output=True, timeout=120)
    err = p.stderr.decode(errors='replace')
    if p.returncode or 'File not found' in err or 'not found' in err.lower():
        raise ValueError('debugfs could not read %s: %s' % (path, err.strip()[-200:]))
    return p.stdout, argv


def debugfs_ls(raw, first_sector, path):
    argv = [tool('debugfs'), '-R', 'ls -p ' + path, '%s?offset=%d' % (raw, first_sector * SECTOR)]
    p = subprocess.run(argv, capture_output=True, timeout=120)
    names = []
    for line in p.stdout.decode(errors='replace').splitlines():
        parts = line.strip('/').split('/')
        # ls -p: /inode/mode/uid/gid/name/size/
        if len(parts) >= 5 and parts[4] not in ('.', '..', ''):
            names.append((parts[4], parts[1]))
    if p.returncode:
        raise ValueError('debugfs ls failed: ' + p.stderr.decode(errors='replace')[-200:])
    return names, argv


def read_committed(raw):
    """INTERFACE 7: boot.cfg selects the generation; its declaration/ holds the files."""
    evidence = []
    boot, argv = debugfs_cat(raw, SYSTEM_FIRST, '/boot.cfg'); evidence.append(argv)
    m = re.search(r'confos\.generation=([0-9a-f]{64})', boot.decode())
    if not m:
        raise ValueError('boot.cfg names no generation')
    gen = m.group(1)
    try:
        applied, argv = debugfs_cat(raw, SYSTEM_FIRST, '/state/applied'); evidence.append(argv)
        applied = applied.decode().strip()
    except ValueError:
        applied = None
    files = {}
    def walk(rel):
        names, argv = debugfs_ls(raw, SYSTEM_FIRST, '/generations/%s/declaration/%s' % (gen, rel))
        evidence.append(argv)
        for name, mode in names:
            r = (rel + '/' + name).strip('/')
            if mode.startswith('04'):
                walk(r)
            else:
                data, argv = debugfs_cat(raw, SYSTEM_FIRST, '/generations/%s/declaration/%s' % (gen, r))
                files[r] = data
    walk('')
    return gen, applied, boot.decode(), files, evidence


# ----------------------------------------------------------------- the backend

class Native:
    """Performs the operations of FORMATS.md on ConfOS 0.67 for one case execution.

    config (private, from local.env 'native'): release tree, sources, clean package
    store, bootstrap root, subid, slots, ssh_key, ssh_port, work dir, server URL, keys.
    """

    def __init__(self, config, bindings, case, variant=None, guest=None, machine_factory=None):
        self.c, self.b, self.case, self.variant = dict(config), bindings, case, variant
        self.v = bindings.variant(case['id'], variant)          # may raise Unavailable at start
        self.work = Path(self.c['work']) / ('%s-%s' % (case['id'], re.sub(r'[^A-Za-z0-9]+', '_', variant or '-')))
        self.guest = guest or SSH(self.c)
        self.machine_factory = machine_factory or (lambda disk: Machine(self.c, disk, self.work))
        self.machine = None
        self.candidate = None
        self.material = {}
        self.marker = '/tmp/case-marker-' + uuid.uuid4().hex[:12]
        self.markers_used = []
        self.last_attempt = None
        self.pending_apply = None
        self.vtokens = self.v.get('tokens', {})

    # helpers --------------------------------------------------------------
    def tokens(self, extra=None):
        t = dict(self.vtokens)
        t['@MARKER@'] = self.marker
        t['@CHILD_PATHS@'] = self.b.cmd['child_paths'].get(self.case['id'], '')
        t.update(extra or {})
        return t

    def sh(self, role, text, extra=None, stdin=None, timeout=300):
        body = self.b.shell(text, self.tokens(extra))
        r = self.guest.run(role, body, stdin=stdin, timeout=timeout, env={'CASE_MARKER': self.marker})
        r['template'] = text
        return r

    def probe(self, text, extra=None, role='root'):
        r = self.sh(role, text, extra)
        if r['returncode'] not in (0, 1):
            raise Unavailable('probe could not observe (status %d): %s %s' % (r['returncode'], text[:160], r['stderr'][-200:]))
        return r['returncode'] == 0, r

    def boot_id(self):
        r = self.guest.run('user', 'cat /proc/sys/kernel/random/boot_id')
        if r['returncode']:
            raise Unavailable('boot identity unreadable')
        return r['stdout'].strip(), r

    def status(self):
        r = self.guest.run('user', 'confos status')
        return r['stdout'].strip(), r

    def write_candidate(self, decl):
        """Root writes every file of the candidate (one tar on standard input, modes 0644, or
        0755 for executable files of a brought tree); the SHA-256 of every file is read back."""
        import tarfile, io
        names = sorted({**decl.files, **decl.inputs})
        for rel in names:
            if rel.startswith('/') or '..' in rel.split('/'):
                raise ValueError('candidate file outside the folder: ' + rel)
        stale = getattr(self, 'stale_inputs', [])
        if stale:
            r = self.guest.run('root', 'cd %s && rm -rf -- %s' % (CANDIDATE_DIR, ' '.join(shlex.quote(x) for x in stale)))
            if r['returncode']:
                return r
            self.stale_inputs = []
        buf = io.BytesIO()
        data_of = {**decl.inputs, **decl.files}
        with tarfile.open(fileobj=buf, mode='w', format=tarfile.GNU_FORMAT) as t:
            dirs = set()
            for rel in names:
                parts = rel.split('/')[:-1]
                for i in range(1, len(parts) + 1):
                    d = '/'.join(parts[:i])
                    if d not in dirs:
                        dirs.add(d)
                        ti = tarfile.TarInfo(d); ti.type = tarfile.DIRTYPE; ti.mode = 0o755
                        t.addfile(ti)
                ti = tarfile.TarInfo(rel); ti.size = len(data_of[rel])
                ti.mode = 0o755 if rel in self.b.exec_inputs else 0o644
                t.addfile(ti, io.BytesIO(data_of[rel]))
        r = self.guest.run('root', 'mkdir -p %s && tar -x --no-same-owner -C %s' % (CANDIDATE_DIR, CANDIDATE_DIR),
                           stdin=buf.getvalue(), timeout=600)
        if r['returncode']:
            return r
        back = self.guest.run('root', 'cd %s && sha256sum -- %s' % (CANDIDATE_DIR, ' '.join(shlex.quote(n) for n in names)))
        got = {}
        for row in back['stdout'].splitlines():
            h, _, n = row.partition('  ')
            got[n] = h
        out = []
        for rel in names:
            if got.get(rel) != sha(data_of[rel]):
                raise Unavailable('candidate bytes not verified after write: ' + rel)
            out.append({'file': rel, 'sha256': sha(data_of[rel])})
        self.candidate = decl
        return {'returncode': 0, 'written': out, 'identity': decl.identity, 'removed_inputs': stale}

    def read_candidate(self):
        """Reads the files of the candidate back from the guest (root, one tar) and parses them."""
        import tarfile, io
        names = sorted({**self.candidate.files, **self.candidate.inputs}) if self.candidate else [MAIN]
        r = self.guest.run('root', 'cd %s && tar -c -- %s | base64 -w0' % (CANDIDATE_DIR, ' '.join(shlex.quote(n) for n in names)),
                           timeout=600)
        raw = [{k: r[k] for k in ('command', 'returncode', 'stderr')}]
        if r['returncode']:
            raise Unavailable('candidate files unreadable: ' + r['stderr'][-300:])
        files, inputs = {}, {}
        with tarfile.open(fileobj=io.BytesIO(base64.b64decode(r['stdout'])), mode='r:') as t:
            for m in t:
                if m.isreg():
                    data = t.extractfile(m).read()
                    (files if m.name in self.candidate.files or (m.name.endswith('.conf') and '/' not in m.name) else inputs)[m.name] = data
        missing = [n for n in names if n not in files and n not in inputs]
        if missing:
            raise Unavailable('candidate files missing: %r' % missing[:5])
        return NativeDecl(files, inputs), raw, None

    # operations ------------------------------------------------------------
    def perform(self, request):
        op = request['op']
        fn = getattr(self, 'op_' + op.replace('-', '_'), None)
        if fn is None:
            raise Unavailable('operation not bound for 0.67: ' + op)
        return fn(request)

    def finish(self):
        if self.machine and self.case.get('id') == 'OW-2' and getattr(self, 'disk', None):
            try:
                self._keep_sequence()
            except Exception as exc:            # OW-3 then reports that the sequence is missing
                self.sequence_error = repr(exc)
        if self.machine:
            self.machine.stop()
        # Heavy leftovers go at once (COMMON: disk ceiling); logs and serial output stay.
        if self.work.exists() and not self.c.get('keep_work'):
            for p in sorted(self.work.rglob('*'), reverse=True):
                if p.is_file() and (p.suffix in ('.raw', '.confpkg', '.fd', '.sqfs', '.sock') or 'packages' in p.parts
                                    or 'disk-read' in p.parts or 'decl' in p.parts):
                    p.unlink()
            for p in sorted(self.work.rglob('*'), reverse=True):
                if p.is_dir() and not any(p.iterdir()):
                    p.rmdir()

    def _build(self, decl, name):
        """A clean installation (INTERFACE 1): confos-assemble in the bootstrap root."""
        d = self.work / name
        if d.exists():
            shutil.rmtree(d)
        (d / 'decl').mkdir(parents=True)
        for rel, data in {**decl.files, **decl.inputs}.items():
            p = d / 'decl' / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        store = d / 'packages'
        subprocess.run(['cp', '-al', str(self.c['packages']), str(store)], check=True)
        before = {p.name for p in store.iterdir()}
        inner = ['python3', '/confos/tools/confos-assemble', '/decl/' + MAIN, '/packages', '/confos', '/sources', '/out/disk.raw']
        # The root is first made a mount point of itself: confos-assemble builds case packages
        # with `unshare --mount --propagation private`, which fails in a plain chroot (TRIAL-1).
        script = ('set -e; umask 022; R=$1; shift; mount --bind $R $R; '
                  'for m in dev proc sys run tmp sources confos packages decl out; do mkdir -p $R/$m; done; '
                  'mount --rbind /dev $R/dev; mount -t proc proc $R/proc; mount -t sysfs sysfs $R/sys; mount -t tmpfs tmpfs $R/run; '
                  'mount --bind "$SRCDIR" $R/sources; mount -o remount,bind,ro $R/sources; '
                  'mount --bind "$TREE" $R/confos; mount -o remount,bind,ro $R/confos; '
                  'mount --bind "$PKG" $R/packages; mount --bind "$DECL" $R/decl; mount -o remount,bind,ro $R/decl; '
                  'mount --bind "$OUT" $R/out; '
                  'exec /usr/sbin/chroot "$R" /usr/bin/env -i HOME=/root PATH=/usr/bin:/usr/sbin LC_ALL=POSIX "$@"')
        (d / 'out').mkdir()
        sub = str(int(self.c['subid']))
        argv = ['unshare', '--user', '--map-root-user', '--map-users=1:%s:65535' % sub, '--map-groups=1:%s:65535' % sub,
                '--mount', '--pid', '--net', '--uts', '--ipc', '--fork', '--kill-child', '--', 'bash', '-c', script, 'assemble',
                str(self.c['bootstrap_root'])] + inner
        env = dict(os.environ, SRCDIR=str(self.c['sources']), TREE=str(self.c['tree']), PKG=str(store),
                   DECL=str(d / 'decl'), OUT=str(d / 'out'))
        t = time.monotonic()
        with open(str(self.c['bootstrap_root']).rstrip('/') + '.lock', 'w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)     # one user of the bootstrap root at a time
            p = subprocess.run(argv, capture_output=True, env=env, timeout=7200)
        log = p.stdout + p.stderr
        (d / 'assemble.log').write_bytes(log)
        m = re.search(rb'BUILT \S+ identity ([0-9a-f]{64}) packages (\d+)', p.stdout)
        added = sorted({x.name for x in store.iterdir()} - before)
        return {'returncode': p.returncode, 'argv_inside': inner, 'log_sha256': sha(log), 'log_tail': log[-2000:].decode(errors='replace'),
                'identity': m.group(1).decode() if m else None, 'expected_identity': decl.identity,
                'packages_built_by_assemble': added, 'disk': str(d / 'out/disk.raw'), 'work_id': str(d),
                'seconds': round(time.monotonic() - t, 1), 'tree': self.c.get('tree_commit'), 'sources_manifest': self.c.get('sources_manifest')}

    def _boot(self, disk, ready_identity=None):
        if self.machine is None:
            self.machine = self.machine_factory(disk)
        start = self.machine.start()
        pos = 0
        m = self.machine.wait_serial(r'^CONFOS READY ([0-9a-f]{64})', since=pos)
        if not m:
            raise Unavailable('no CONFOS READY line on the serial console: ' + self.machine.serial_text()[-500:])
        reach = self.guest.wait()
        bid = reach['stdout'].strip()
        st, sr = self.status()
        return {'boot': start, 'ready_line': m.group(0), 'ready_identity': m.group(1), 'boot_id': bid, 'status': st, 'status_reply': sr}

    def op_fresh(self, request, name='fresh'):
        decl = self.b.render(self._declaration(request['declaration']))
        built = self._build(decl, name)
        if built['returncode'] or built['identity'] != decl.identity:
            return dict(built, returncode=built['returncode'] or 1, reason='assemble failed or identity differs')
        booted = self._boot(built['disk'])
        self.disk = built['disk']
        self.candidate = decl
        self.fresh_decl = decl
        return dict(built, **booted, returncode=0 if booted['status'] == 'APPLIED ' + decl.identity else 1)

    def _declaration(self, name):
        if isinstance(name, dict):
            return name
        return json.loads((self.b.root / 'declarations' / (name + '.json')).read_text())

    def op_fresh_from_law(self, request):
        gen, applied, boot, files, ev = read_committed(self.disk)
        decl = NativeDecl({k: v for k, v in files.items() if _is_decl_file(k)},
                          {k: v for k, v in files.items() if not _is_decl_file(k)})
        if self.candidate:
            decl.inputs.update({k: v for k, v in self.candidate.inputs.items() if k not in decl.inputs})
        self.finish(); self.machine = None
        built = self._build(decl, 'reproduce')
        booted = self._boot(built['disk'])
        self.disk = built['disk']
        return dict(built, **booted, source_generation=gen, returncode=0 if booted['status'] == 'APPLIED ' + decl.identity else 1)

    def op_read_boot(self, request):
        bid, r = self.boot_id()
        return dict(r, boot_id=bid)

    def step_name(self, request):
        names = [s['name'] for s in self.case['steps'] if s['request'].get('op') == request['op']
                 and s['request'].get('command') == request.get('command')]
        return names[0] if len(names) == 1 else None

    def ensure_material(self, folder=None):
        """Payloads a case names but no put-material step places: saved by the person first."""
        folder = folder or self.b.cmd['tokens']['@HOME@']
        if any(s['request']['op'] == 'put-material' for s in self.case['steps']):
            return
        done = getattr(self, '_material_done', set())
        if folder in done:
            return
        role = 'root' if folder.startswith('/root') else 'user'
        for rel, src in self.b.cmd['material'].get(self.case['id'], {}).items():
            data = self.b.payload(src)
            dest = folder + '/' + rel
            self.guest.run(role, 'mkdir -p %s && cat > %s' % (shlex.quote(folder), shlex.quote(dest)), stdin=data)
            self.material[dest] = {'origin': src, 'sha256': sha(data), 'routes': []}
        done.add(folder); self._material_done = done

    def op_command(self, request):
        self.ensure_material()
        step = self.v.get('steps', {}).get(self.step_name(request)) if self.v else None
        text, role = request['command'], request.get('role', 'user')
        if step:
            text, role = step['command'], step.get('role', role)
        r = self.sh(role, text)
        self.last_attempt = r
        for path, m in self.material.items():
            kind = route_kind(r['command'], path)
            if kind:
                m['routes'].append({'kind': kind, 'observed': r['returncode'] is not None, 'command': r['command'],
                                    **({'executed': None} if kind == 'direct' else {})})
        return r

    def op_put_material(self, request):
        target = self.b.expand(request['target'], self.tokens())[0]
        if request['source'] == 'boundary-fixture':
            return self._boundary(target)
        data = self.b.payload(request['source'])
        r = self.guest.run('user', 'mkdir -p "$(dirname %s)" && cat > %s' % (shlex.quote(target), shlex.quote(target)), stdin=data)
        back = self.guest.run('user', 'sha256sum ' + shlex.quote(target))
        ok = r['returncode'] == 0 and back['stdout'].split()[:1] == [sha(data)]
        self.material[target] = {'origin': request['source'], 'sha256': sha(data), 'routes': []}
        for rel, src in self.b.cmd['material'].get(self.case['id'], {}).items():
            extra = self.b.payload(src)
            dest = str(Path(target).parent / rel)
            self.guest.run('user', 'cat > ' + shlex.quote(dest), stdin=extra)
            self.material[dest] = {'origin': src, 'sha256': sha(extra), 'routes': []}
        return dict(r, returncode=0 if ok else 1, sha256=sha(data), target=target, verified=ok)

    def _boundary(self, home):
        text = ('mkdir -p {h}/opened {h}/opened-sibling {h}/closed && cp {h}/opened/script {h}/opened-sibling/script 2>/dev/null; '
                'printf "printf executed > \\"$CASE_MARKER\\"\\n" > {h}/closed/target && '
                'printf "printf executed > \\"$CASE_MARKER\\"\\n" > {h}/opened-sibling/script && '
                'printf "printf executed > \\"$CASE_MARKER\\"\\n" > {h}/opened/script && '
                'ln -sf {h}/closed/target {h}/opened/link-out').format(h=shlex.quote(home))
        r = self.guest.run('user', text)
        for p in ('/opened/script', '/opened-sibling/script', '/closed/target', '/opened/link-out'):
            self.material[home + p] = {'origin': 'boundary-fixture', 'routes': []}
        return r

    # declarations ----------------------------------------------------------
    def op_edit(self, request):
        before = self.candidate
        decl = self._edited(before, request['action'], request['line'], request.get('file'))
        w = self.write_candidate(decl)
        return dict(w, before_lines=before.lines(), after_lines=decl.lines(),
                    before_identity=before.identity, after_identity=decl.identity,
                    notes=list(getattr(self, 'edit_notes', [])))

    def _edited(self, decl, action, line, file=None):
        if line.get('kind') == 'test-target':
            if not getattr(self, 'removal', None):
                raise ValueError('removal target not prepared')
            line = {'kind': 'binding', 'name': self.removal['slot']}
        rel = (file + '.conf') if file and file != 'main' else MAIN
        if rel not in decl.files:
            raise ValueError('no such declaration file: ' + rel)
        text = decl.files[rel].decode()
        inputs = dict(decl.inputs)
        rows = text.splitlines()
        def drop(pred):
            kept = [r for r in rows if not (shlex.split(r, comments=True) and pred(shlex.split(r, comments=True)))]
            if len(kept) == len(rows):
                raise ValueError('nothing to remove for ' + json.dumps(line))
            return kept
        if action in ('remove', 'replace'):
            if line['kind'] == 'package':
                name = line['name']
                rows = drop(lambda f: f[0] == 'package' and f[1] == name)
            elif line['kind'] == 'open-folder':
                path = self.b.expand(line['path'])[0]
                rows = drop(lambda f: f == ['open', path])
            elif line['kind'] == 'base':
                # INTERFACE 9: the base line and the package lines the update changes are
                # replaced; the tree and sources of an earlier update leave the folder.
                slot = self.b.slot(line['binding'])
                names = set(slot.get('replaces', {}).get('packages', []))
                rows = drop(lambda f: f[0] == 'base')
                rows = [r for r in rows if not (shlex.split(r, comments=True)[:1] == ['package']
                                                and shlex.split(r, comments=True)[1] in names)]
                brought = self.b.update_input_names()
                stale = sorted(k for k in inputs if k in brought or k.split('/')[0] in brought)
                for k in stale:
                    del inputs[k]
                self.stale_inputs = sorted({k.split('/')[0] for k in stale})
            else:
                native, _ = self.b.native_for(line)
                targets = [shlex.split(n) for n in native]
                rows = drop(lambda f: f in targets)
        if action in ('add', 'replace'):
            native, ins = self.b.native_for(line)
            # A package already named at another version: the new line replaces it, since a
            # second line for the same thing is an error (INTERFACE 5). Recorded as a note.
            for n in native:
                f = shlex.split(n)
                if f[0] == 'package':
                    old = [r for r in rows if shlex.split(r, comments=True)[:2] == ['package', f[1]]
                           and shlex.split(r, comments=True) != f]
                    if old:
                        rows = [r for r in rows if r not in old]
                        self.edit_notes = getattr(self, 'edit_notes', []) + [
                            'added line %r replaces %r (one line per package)' % (n, old)]
            present = [shlex.split(r, comments=True) for r in rows]
            for n in native:            # a line that is already there is not written twice
                if shlex.split(n) not in present:
                    rows.append(n)
            inputs.update(ins)
        files = dict(decl.files)
        files[rel] = ('\n'.join(rows) + '\n').encode()
        return NativeDecl(files, inputs, decl.main)

    def op_split_declaration(self, request):
        decl = self.candidate
        main, prog = [], []
        for r in decl.files[MAIN].decode().splitlines():
            f = shlex.split(r, comments=True)
            (prog if f and f[0] == 'package' else main).append(r)
        main.append('include programs.conf')
        new = NativeDecl({MAIN: ('\n'.join(main) + '\n').encode(), 'programs.conf': ('\n'.join(prog) + '\n').encode()}, decl.inputs)
        w = self.write_candidate(new)
        self.before_split = decl
        return dict(w, file_count=len(new.order), files=new.order)

    def op_read_law(self, request):
        if request['scope'] == 'candidate':
            decl, raw, _ = self.read_candidate()
            check = self.guest.run('user', 'confos check ' + CANDIDATE_DIR + '/' + MAIN)
            m = re.match(r'OK ([0-9a-f]{64}) (\d+) lines', check['stdout'].strip())
            return {'scope': 'candidate', 'sha256': decl.identity, 'expected_status': 'APPLIED ' + decl.identity,
                    'files': {k: sha(v) for k, v in decl.files.items()}, 'lines': decl.lines(),
                    'declaration': self._semantic(decl), 'reads': raw, 'confos_check': check,
                    'check_identity': m.group(1) if m else None}
        self.guest.run('root', 'sync')
        gen, applied, boot, files, ev = read_committed(self.disk)
        inputs = dict(self.candidate.inputs) if self.candidate else {}
        inputs.update({k: v for k, v in files.items() if not _is_decl_file(k)})
        decl = NativeDecl({k: v for k, v in files.items() if _is_decl_file(k)}, inputs)
        return {'scope': 'committed', 'sha256': decl.identity, 'selected_generation': gen, 'state_applied': applied,
                'boot_cfg': boot, 'files': {k: sha(v) for k, v in files.items()}, 'lines': decl.lines(),
                'text': {k: v.decode(errors='replace') for k, v in decl.files.items()},
                'declaration': self._semantic(decl), 'evidence': [' '.join(a) for a in ev],
                'consistent': gen == decl.identity == applied}

    def _semantic(self, decl):
        layout = self.b.release.get('layout', [])
        return semantic_from_native(decl, self.c.get('tree'), self.c.get('store_index'), layout,
                                    self.b.release.get('derivation'), trees=self.release_trees())

    def release_trees(self):
        trees = {self.c.get('release', RELEASE): self.c.get('tree')}
        for state, path in (self.c.get('update_trees') or {}).items():
            trees[(self.c.get('update_releases') or {}).get(state, state)] = path
        return {k: v for k, v in trees.items() if v}

    def op_apply(self, request, cut=False):
        old, _ = self.boot_id()
        target = self.candidate.identity
        r = self.guest.run('root', 'confos apply', timeout=3600)
        out = r['stdout']
        restarting = 'SELECTED ' + target in out
        if not restarting:
            st, sr = self.status()
            return dict(r, status=st, old_boot_id=old, new_boot_id=old, restarted=False)
        new, st = self._wait_applied(old, target)
        return dict(r, status=st, old_boot_id=old, new_boot_id=new, restarted=True)

    def _wait_applied(self, old, target, timeout=600):
        end = time.monotonic() + timeout
        st = None
        while time.monotonic() < end:
            try:
                bid, _ = self.boot_id()
                if bid != old:
                    st, _ = self.status()
                    if st == 'APPLIED ' + target or st.startswith('APPLIED'):
                        return bid, st
            except Unavailable:
                pass
            time.sleep(2)
        raise Unavailable('no APPLIED status after the restart within %d s (last %r)' % (timeout, st))

    def op_apply_cut(self, request):
        """Cut power immediately after the documented report of success (INTERFACE 6)."""
        old, _ = self.boot_id()
        target = self.candidate.identity
        r = self.guest.run('root', 'confos apply', timeout=3600)
        success = None
        end = time.monotonic() + 600
        while time.monotonic() < end:
            try:
                st, _ = self.status()
                bid, _ = self.boot_id()
                if bid != old and st.startswith('APPLIED'):
                    t_success = time.monotonic()
                    success = st
                    break
            except Unavailable:
                pass
            time.sleep(0.2)
        if success is None:
            raise Unavailable('no report of success observed before the cut')
        cut = self.machine.power_cut()
        return dict(r, success=success, success_monotonic=t_success, success_observed=True, **cut, old_boot_id=old)

    def op_boot(self, request):
        b = self._boot(self.disk)
        return b

    def op_restart(self, request):
        old, _ = self.boot_id()
        r = self.guest.run('root', 'reboot')
        method = 'reboot as root in a session'
        try:
            new = self._wait_new_boot(old, 120)
        except Unavailable:
            method = 'QMP system_powerdown, then a new start of the same disk'
            self.machine.qmp_cmd('system_powerdown')
            try:
                self.machine.proc.wait(timeout=120)
            except subprocess.TimeoutExpired:
                method = ('power cycle by the case party: the session could not restart (reboot refused, '
                          'power button ignored for 120 s)')
                self.machine.stop()
            self._boot(self.disk)
            new, _ = self.boot_id()
        return {'reboot_reply': r, 'method': method, 'old_boot_id': old, 'boot_id': new}

    def _wait_new_boot(self, old, timeout):
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            try:
                bid, _ = self.boot_id()
                if bid != old:
                    return bid
            except Unavailable:
                pass
            time.sleep(2)
        raise Unavailable('no new boot within %d s' % timeout)

    def op_network(self, request):
        up = request['state'] == 'up'
        t = time.monotonic()
        reply = self.machine.qmp_cmd('set_link', name='n', up=up)
        return {'state': request['state'], 'qmp_reply': reply, 'monotonic': t}

    # queries ----------------------------------------------------------------
    def op_query(self, request):
        subject = request['subject']
        if ':' in subject and subject.split(':')[0] in ('account', 'access', 'service', 'firewall', 'network',
                                                        'saved-network', 'hostname', 'time', 'locale', 'module', 'sysctl', 'mount'):
            return self._setting(subject)
        fn = getattr(self, 'q_' + subject.replace('-', '_'), None)
        if fn is None:
            raise Unavailable('query subject not bound for 0.67: ' + subject)
        return fn(request)

    def _effect_text(self):
        e = self.v.get('effect') if self.v else None
        if not e:
            raise Unavailable('no effect probe bound for this variant')
        return e

    def _setting(self, subject):
        present, r = self.probe(self._effect_text())
        return {'value': present, 'probe': r, 'subject': subject}

    def q_marker(self, request):
        present, r = self.probe(self.b.cmd['probes']['marker'], role='root')
        for m in self.material.values():
            for route in m['routes']:
                if route['kind'] == 'direct' and route.get('executed', False) is None:
                    route['executed'] = present
        return {'value': present, 'probe': r, 'marker': self.marker}

    q_payload_executed = q_marker

    def q_startup_effect(self, request):
        sessions = []
        for s in self.b.cmd['startup_sessions']:
            r = self.guest.run('user', self.b.shell(s, self.tokens()) + '; echo CASE-SESSION-END', env={'CASE_MARKER': self.marker}, tty=True)
            if 'CASE-SESSION-END' not in r['stdout']:
                raise Unavailable('startup session did not run to its end: ' + s)
            sessions.append(r)
        out = self.q_marker(request)
        return dict(out, sessions=sessions)

    def q_persistent_unrecorded_effect(self, request):
        present, r = self.probe(self.b.cmd['probes']['persistent-unrecorded-effect'], role='root')
        return {'value': present, 'probe': r}

    def q_unrecorded_installation(self, request):
        present, r = self.probe(self.b.cmd['probes']['unrecorded-installation'], role='root')
        out = {'value': present, 'probe': r}
        if self.last_attempt and re.search(r'case-small 2', self.last_attempt['stdout']) and self.case['id'] == 'G-INSTALL':
            out.update(value=True, executed_output=self.last_attempt['stdout'])
        return out

    def q_command_present(self, request):
        text = self.b.cmd['command_present'].get(self.case['id'])
        if text is None:
            raise Unavailable('no presence probe bound for ' + self.case['id'])
        role = (self.v.get('steps', {}).get('attempt', {}) if self.v else {}).get('role') or next(
            (s['request'].get('role', 'user') for s in self.case['steps'] if s['name'] == 'attempt'), 'user')
        present, r = self.probe(text, role=role)
        if not present:
            raise Unavailable('tool needed by the attempt is absent; absence is not a refusal: ' + text)
        return {'value': True, 'probe': r}

    def q_positive_control(self, request):
        cid = self.case['id']
        if cid in self.b.cmd['setting_controls']:
            present, r = self.probe(self.b.cmd['setting_controls'][cid])
            return {'value': present, 'probe': r, 'kind': 'the probe reads the declared state'}
        folder = self.b.cmd['control_folder']
        extra = {'@HOME@': folder, '@TARGET@': folder}
        if cid.startswith('OPEN-'):
            folder = self.b.expand('@HOME@/opened', self.tokens())[0]
            extra = {'@HOME@': folder, '@TARGET@': folder}
            text = '@SH@ ' + folder + '/control-script'
            self.guest.run('user', 'mkdir -p %s && cat > %s/control-script' % (folder, folder), stdin=self.b.payload('payloads/unrecorded.sh'))
        else:
            step = self.v.get('steps', {}).get('attempt') if self.v else None
            attempt = next(s for s in self.case['steps'] if s['name'] == 'attempt')['request']
            text = step['command'] if step else attempt['command']
            ctl = self.b.cmd.get('controls', {}).get(cid)
            if ctl:
                text = ctl.get(self.variant, ctl['-'])
            self.ensure_material(folder)
            for s in self.case['steps']:
                if s['request']['op'] == 'put-material':
                    src = s['request']['source']
                    tgt = self.b.expand(s['request']['target'], self.tokens(extra))[0]
                    put_role = 'root' if tgt.startswith('/root/') else 'user'
                    self.guest.run(put_role, 'mkdir -p "$(dirname %s)" && cat > %s' % (shlex.quote(tgt), shlex.quote(tgt)), stdin=self.b.payload(src))
                    for rel, msrc in self.b.cmd['material'].get(cid, {}).items():
                        self.guest.run(put_role, 'cat > ' + shlex.quote(str(Path(tgt).parent / rel)), stdin=self.b.payload(msrc))
        role = (self.v.get('steps', {}).get('attempt', {}) if self.v else {}).get('role', 'user')
        if role == 'root':
            folder = '/root/control'
            extra = {'@HOME@': folder, '@TARGET@': folder}
            text = text.replace('/root/', folder + '/')
        run = self.sh(role, text, extra)
        present, r = self.probe(self.b.cmd['probes']['marker'], role='root')
        clean = self.guest.run('root', 'rm -f ' + shlex.quote(self.marker))
        return {'value': present, 'control_command': run, 'probe': r, 'marker_removed': clean['returncode'] == 0}

    def q_package_version(self, request):
        r = self.guest.run('user', 'confpkg list /')
        if r['returncode']:
            raise Unavailable('confpkg list failed')
        versions = dict(l.split()[:2] for l in r['stdout'].splitlines() if len(l.split()) >= 2)
        if request['package'] not in versions:
            raise Unavailable('package not installed: ' + request['package'])
        return {'value': versions[request['package']], 'listing': r}

    def q_package_present(self, request):
        r = self.guest.run('user', 'confpkg list /')
        if r['returncode']:
            raise Unavailable('confpkg list failed')
        return {'value': any(l.split()[:1] == [request['package']] for l in r['stdout'].splitlines()), 'listing': r}

    def q_capability(self, request):
        raise Unavailable({'container': 'no container runtime in 0.67 (EXECUTORS.md)',
                           'in-guest-vm': 'no hypervisor program in the 0.67 base (base.conf)'}.get(request['capability'], 'capability not in 0.67'))

    def q_opening_line(self, request):
        law = self.op_read_law({'scope': 'committed'})
        opens = [l for l in law['declaration']['lines'] if l['kind'] == 'open-folder']
        home = self.b.cmd['tokens']['@HOME@']
        values = [{'kind': 'open-folder', 'path': o['path'].replace(home, '@HOME@', 1) if o['path'].startswith(home + '/') else o['path'],
                   'scope': o['scope']} for o in opens if o['path'] not in (self.b.cmd['control_folder'], '/root/control')]
        if len(values) != 1:
            return {'value': values, 'law': law}
        return {'value': values[0], 'law': law, 'raw_lines': [l for l in law['lines'] if l.startswith('open ')]}

    def q_description_equivalent(self, request):
        law = self.op_read_law({'scope': 'committed'})
        left = sorted(self.before_split.lines())
        right = sorted(law['lines'])
        return {'left': left, 'right': right, 'evidence': {'committed': law['files'], 'before_split': self.before_split.identity}}

    def q_listening_owner(self, request):
        port = int(self.b.cmd['tokens']['@TEST_PORT@'])
        text = ('i=$(awk -v p=%04X \'NR>1 { split($2,a,":"); if (a[2]==p && $4=="0A") print $10 }\' /proc/net/tcp | head -1); '
                '[ -n "$i" ] || exit 3; for f in /proc/[0-9]*/fd/*; do [ "$(readlink $f 2>/dev/null)" = "socket:[$i]" ] && '
                '{ p=${f#/proc/}; p=${p%%%%/*}; echo "$p $(readlink /proc/$p/exe) $(sha256sum /proc/$p/exe | cut -d" " -f1)"; exit 0; }; done; exit 3') % port
        r = self.guest.run('root', text)
        if r['returncode']:
            raise Unavailable('listener not observed while alive (A19): ' + r['stderr'][-200:])
        pid, exe, digest = r['stdout'].split()[:3]
        self.listener = {'pid': pid, 'exe': exe, 'sha256': digest, 'raw': r}
        return {'value': os.path.basename(exe), 'pid': pid, 'exe': exe, 'exe_sha256': digest, 'raw': r}

    def q_namespace_executable_hash(self, request):
        if not getattr(self, 'listener', None):
            raise Unavailable('no listener observation retained (A19)')
        self.guest.run('root', 'sync')
        law = self.op_read_law({'scope': 'committed'})
        r = self.guest.run('root', 'sha256sum /usr/bin/case-probe')
        return {'left': self.listener['sha256'], 'right': r['stdout'].split()[0] if r['returncode'] == 0 else None,
                'evidence': {'listener': self.listener['raw'], 'image_file': r, 'law': law['sha256']}}

    # X-REC, removals and preparations --------------------------------------------
    def _xrec(self, target):
        x = self.b.cmd['xrec'].get(target)
        if x is None:
            raise Unavailable('no request binding for target ' + target)
        if 'unsupported' in x:
            raise Unavailable(x['unsupported'])
        return x

    def op_tool_request(self, request):
        x = self._xrec(request['target'])
        before, _, _ = self.read_candidate()
        cmd = x.get(request['action'] if request['action'] == 'remove' else 'add')
        if cmd is None:
            r = {'tool': 'absent', 'returncode': None, 'reason': 'no tool for this request in 0.67; only the line can do it'}
        else:
            r = self.sh(request.get('role', 'root'), cmd)
        after, _, _ = self.read_candidate()
        self.xrec_before = before
        return dict(r, before_lines=before.lines(), after_lines=after.lines(), recorded=before.lines() != after.lines())

    def _delta(self, spec):
        added = [canon(shlex.split(self.b.expand(l)[0])) for l in spec.get('lines', [])]
        removed = [canon(shlex.split(self.b.expand(l)[0])) for l in spec.get('remove_lines', [])]
        if 'slot' in spec:
            native, _ = self.b.native_for({'kind': 'binding', 'name': spec['slot']})
            added += [canon(shlex.split(n)) for n in native]
            removed += [l for l in self.candidate.lines() if shlex.split(l)[:2] == ['package', spec['replaces_package']]]
        return added, removed

    def q_request_delta_valid(self, request):
        x = self._xrec(request['target'])
        added, removed = self._delta(x['record_add'])
        before = self.xrec_before.lines()
        after, _, _ = self.read_candidate()
        return {'before_lines': before, 'after_lines': after.lines(), 'expected_added': added, 'expected_removed': removed,
                'binding_evidence': {'target': request['target'], 'binding': x}}

    def q_request_in_force(self, request):
        x = self._xrec(request['target'])
        present, r = self.probe(x['effect'])
        return {'value': present, 'probe': r}

    def _record(self, spec, inputs_spec=None):
        added, removed = self._delta(spec)
        decl = self.candidate
        rows = decl.files[MAIN].decode().splitlines()
        canon_rows = [canon(shlex.split(r, comments=True)) if shlex.split(r, comments=True) else None for r in rows]
        missing = [l for l in removed if l not in canon_rows]
        if missing:
            raise ValueError('lines to remove are not in the candidate: %r' % missing)
        rows = [r for r, c in zip(rows, canon_rows) if c not in removed] + added
        inputs = dict(decl.inputs)
        for rel, src in spec.get('inputs', {}).items():
            inputs[rel] = self.b.payload(src)
        if 'slot' in spec:
            inputs.update(self.b.native_for({'kind': 'binding', 'name': spec['slot']})[1])
        new = NativeDecl({**decl.files, MAIN: ('\n'.join(rows) + '\n').encode()}, inputs)
        return self.write_candidate(new), added, removed

    def op_record_if_refused(self, request):
        x = self._xrec(request['target'])
        cand, _, _ = self.read_candidate()
        if cand.lines() != self.xrec_before.lines():
            return {'returncode': 0, 'recorded_by_tool': True, 'lines': cand.lines()}
        w, added, removed = self._record(x['record_add'])
        return dict(w, recorded_by_tool=False, added=added, removed=removed)

    def op_record_removal_if_refused(self, request):
        x = self._xrec(request['target'])
        cand, _, _ = self.read_candidate()
        if cand.lines() != self.xrec_before.lines():
            return {'returncode': 0, 'recorded_by_tool': True, 'lines': cand.lines()}
        w, added, removed = self._record(x['record_remove'])
        return dict(w, recorded_by_tool=False, added=added, removed=removed)

    def _apply_now(self, label):
        r = self.op_apply({'op': 'apply'})
        if r['status'] != 'APPLIED ' + self.candidate.identity:
            raise Unavailable('precondition %s did not apply: %s' % (label, r['status']))
        return r

    def op_prepare_change(self, request):
        ch = self.b.cmd['changes'].get(request['target'])
        if ch is None or 'unsupported' in ch:
            raise Unavailable((ch or {}).get('unsupported', 'no change binding for ' + request['target']))
        evidence = {}
        if 'precondition_slot' in ch:
            self.write_candidate(self._edited(self.candidate, 'add', {'kind': 'binding', 'name': ch['precondition_slot']}))
            evidence['precondition'] = self._apply_now(ch['precondition_slot'])
        if 'add_slot' in ch:
            new = self._edited(self.candidate, 'add', {'kind': 'binding', 'name': ch['add_slot']})
        elif 'remove_slot' in ch:
            new = self._edited(self.candidate, 'remove', {'kind': 'binding', 'name': ch['remove_slot']})
        elif 'replace_slot' in ch:
            new = self._edited(self._edited(self.candidate, 'remove', {'kind': 'binding', 'name': ch['replace_slot'][0]}),
                               'add', {'kind': 'binding', 'name': ch['replace_slot'][1]})
        else:
            old, newline = ch['replace_line']
            text = self.candidate.files[MAIN].decode()
            if old not in text.splitlines():
                raise ValueError('line to change is not in the candidate: ' + old)
            new = self.candidate.replace_text(MAIN, '\n'.join(newline if l == old else l for l in text.splitlines()) + '\n')
        before = self.candidate.lines()
        w = self.write_candidate(new)
        return dict(w, before_lines=before, after_lines=new.lines(), evidence=evidence)

    def op_prepare_removal(self, request):
        rm = self.b.cmd['removal'][request['thing']]
        evidence = {}
        if not rm.get('already_declared'):
            self.write_candidate(self._edited(self.candidate, 'add', {'kind': 'binding', 'name': rm['slot']}))
            evidence['apply'] = self._apply_now(rm['slot'])
        if rm.get('start'):
            evidence['start'] = self.sh('user', rm['start'])
        self.removal = rm
        return {'returncode': 0, 'evidence': evidence}

    def q_removal_target_present(self, request):
        present, r = self.probe(self.removal['present'])
        return {'value': present, 'probe': r}


    # inventory ------------------------------------------------------------------
    def op_inventory(self, request):
        """Whole stored (external disk read) and live (guest queries) capture."""
        live = self.live_capture()
        self.guest.run('root', 'sync')
        try:
            import adapter_disk
        except ImportError as exc:
            raise Unavailable('external disk reader not available: ' + str(exc))
        info = adapter_disk.read_disk(self.disk, self.work / 'disk-read', self.c.get('subid'))
        stored = adapter_disk.inventory_from_disk(info)
        sel = info.get('selected')
        gen = info.get('generations', {}).get(sel, {})
        kernel = gen.get('kernel_sha256')
        for o in live['objects']:
            if o['kind'] == 'process' and o['value'].get('exe_sha256') == '@KERNEL@':
                o['value']['exe_sha256'] = kernel
                o['value']['exe_evidence'] += '; running kernel = /system/generations/%s/vmlinuz, sha256 %s (external read)' % (sel, kernel)
        packages = []
        import adapter_disk
        for name, text in sorted(gen.get('passports', {}).items()):
            if name == 'declaration':
                continue
            pp = adapter_disk.parse_passport(text)
            packages.append({'kind': 'package', 'id': pp['name'], 'value': {'version': pp['version'],
                             'source_sha256': sorted([x[0], x[1]] for x in pp['sources']), 'recipe_sha256': pp['recipe'][1]}})
        objects = classify(stored['objects'], self.material, live) + \
            [o for o in live['objects'] if o['kind'] != 'volatile'] + packages
        coverage = dict(live['coverage'])
        coverage['stored'] = stored['coverage']['stored']
        return {'objects': objects, 'errors': stored.get('errors', []) + live['errors'], 'coverage': coverage,
                'raw_live': live['raw'], 'disk_evidence': info.get('evidence'), 'selected_generation': info.get('selected')}

    def live_capture(self):
        r = self.guest.run('root', LIVE_SCRIPT, timeout=600)
        if r['returncode']:
            raise Unavailable('live capture failed: ' + r['stderr'][-300:])
        return parse_live(r['stdout'], r)


# One typed script, run as root in a session; one tagged line per observation.
LIVE_SCRIPT = r'''
set -u
for d in /proc/[0-9]*; do p=${d#/proc/}
  st=$(cat $d/stat 2>/dev/null) || continue
  fl=$(printf '%s' "${st##*) }" | cut -d' ' -f7)
  u=$(awk '/^Uid:/{print $2}' $d/status 2>/dev/null)
  e=$(readlink $d/exe 2>/dev/null); h=-; [ -n "$e" ] && h=$(sha256sum $d/exe 2>/dev/null | cut -d' ' -f1)
  c=$(tr '\0' ' ' < $d/cmdline 2>/dev/null | base64 -w0)
  echo "P $p ${fl:-0} ${u:--} ${h:--} ${e:--} ${c:--}"
  for f in $d/fd/*; do l=$(readlink $f 2>/dev/null) || continue; case $l in socket:*) echo "S $p $l";; esac; done
done
for t in tcp tcp6 udp udp6; do [ -r /proc/net/$t ] && awk -v t=$t 'NR>1{print "N",t,$2,$4,$10}' /proc/net/$t; done
while IFS= read -r l; do echo "A $l"; done < /etc/passwd
while IFS= read -r l; do echo "G $l"; done < /etc/group
for f in /etc/sudoers.d/*; do [ -f "$f" ] && echo "R $f $(sha256sum "$f" | cut -d' ' -f1)"; done
for f in /etc/dropbear/authorized_keys/*; do [ -f "$f" ] && while IFS= read -r l; do echo "K ${f##*/} $l"; done < "$f"; done
echo "V $(base64 -w0 /etc/confos/services.json 2>/dev/null || echo -)"
echo "VR $(base64 -w0 /run/confos-services.json 2>/dev/null || echo -)"
echo "W $(confos services 2>&1 | base64 -w0)"
ip -o addr | while IFS= read -r l; do echo "I $l"; done
ip route | while IFS= read -r l; do echo "T4 $l"; done
ip -6 route | while IFS= read -r l; do echo "T6 $l"; done
while IFS= read -r l; do echo "M $l"; done < /proc/self/mountinfo
if [ -e /proc/modules ]; then while IFS= read -r l; do echo "D $l"; done < /proc/modules; else echo "D-ABSENT /proc/modules"; fi
for k in $(cd /proc/sys && find . -type f 2>/dev/null | sed 's|^\./||' | tr / . ); do :; done
python3 -c "import json;[print('Y',k,open('/proc/sys/'+k.replace('.','/')).read().strip()) for k in sorted(json.load(open('/etc/confos/sysctls.json')))]"
echo "Y0 net.ipv4.ip_forward $(cat /proc/sys/net/ipv4/ip_forward)"
echo "L $(cat /etc/locale.conf 2>/dev/null | tr '\n' ' ')"
echo "Z $(readlink /etc/localtime) $(cat /etc/timezone 2>/dev/null)"
echo "H $(hostname) $(cat /proc/sys/kernel/hostname)"
if fw=$(confos rules 2>&1); then printf '%s\n' "$fw" | sed 's/^/FW /'; echo "FW-END"; else echo "FW-ERROR $(printf '%s' "$fw" | tr '\n' ' ')"; fi
for c in ieee80211 bluetooth; do if [ -d /sys/class/$c ] && [ -n "$(ls /sys/class/$c)" ]; then echo "X $c $(ls /sys/class/$c | tr '\n' ' ')"; else echo "X-ABSENT $c"; fi; done
for n in /sys/class/net/*; do [ -d $n/wireless ] && echo "X wireless ${n##*/}"; done
for t in wpa_supplicant iwd iwctl nmcli connmanctl bluetoothctl; do command -v $t >/dev/null && echo "X tool $t"; done
for d in /tmp /var /dev/shm /run; do find $d -xdev \( -type f -o -type l \) -printf "F %p %m %U %G %y %s\n" 2>/dev/null; done
echo "END"
'''


def parse_live(text, raw):
    objs, errors, cov = [], [], {}
    lines = text.splitlines()
    if not lines or lines[-1] != 'END':
        raise Unavailable('live capture incomplete (no END line)')
    procs, sockets = {}, {}
    kthread_exe = None
    def ok(kind, evidence):
        cov[kind] = {'status': 'complete', 'evidence': evidence}
    for l in lines:
        tag, _, rest = l.partition(' ')
        if tag == 'P':
            pid, flags, uid, h, exe, cmd = (rest.split(' ', 5) + ['-'] * 6)[:6]
            procs[pid] = {'flags': int(flags or 0), 'uid': uid, 'sha256': None if h == '-' else h, 'exe': exe,
                          'cmdline': base64.b64decode(cmd).decode(errors='replace') if cmd != '-' else ''}
        elif tag == 'S':
            pid, link = rest.split(' ', 1)
            sockets.setdefault(link[8:-1], pid)
    for pid, p in sorted(procs.items(), key=lambda x: int(x[0])):
        if p['flags'] & 0x00200000:          # PF_KTHREAD: a thread of the running kernel
            objs.append({'kind': 'process', 'id': 'kthread:' + pid, 'value': {'exe_sha256': '@KERNEL@', 'exe_evidence': 'PF_KTHREAD flag in /proc/%s/stat' % pid}})
        elif p['sha256']:
            objs.append({'kind': 'process', 'id': 'pid:' + pid, 'value': {'exe_sha256': p['sha256'], 'exe': p['exe'], 'uid': p['uid'],
                         'exe_evidence': 'sha256sum /proc/%s/exe (through the process root)' % pid, 'cmdline': p['cmdline']}})
        else:
            errors.append({'kind': 'process', 'reason': 'executable of process %s unreadable' % pid})
    ok('process', 'live: /proc/*/stat, status, exe (sha256 through the process), cmdline')
    for l in lines:
        tag, _, rest = l.partition(' ')
        if tag == 'N':
            proto, local, state, inode = rest.split()
            if proto.startswith('tcp') and state != '0A':
                continue
            pid = sockets.get(inode)
            owner = procs.get(pid, {}) if pid else {}
            objs.append({'kind': 'port', 'id': '%s:%s' % (proto, local), 'value': {
                'exe_sha256': owner.get('sha256'), 'exe_evidence': ('socket inode %s held by process %s' % (inode, pid)) if pid else None}})
    ok('port', 'live: /proc/net/{tcp,tcp6,udp,udp6} with socket inodes mapped to processes')
    groups_of = {}
    for l in lines:
        tag, _, rest = l.partition(' ')
        if tag == 'G':
            name, _, gid, members = (rest.split(':') + [''] * 4)[:4]
            objs.append({'kind': 'group', 'id': name, 'value': {'gid': int(gid)}})
            for m in filter(None, members.split(',')):
                groups_of.setdefault(m, []).append(name)
    for l in lines:
        tag, _, rest = l.partition(' ')
        if tag == 'A':
            f = rest.split(':')
            objs.append({'kind': 'account', 'id': f[0], 'value': {'uid': int(f[2]), 'gid': int(f[3]), 'home': f[5], 'shell': f[6],
                                                                  'groups': sorted(groups_of.get(f[0], []))}})
        elif tag == 'R':
            path, digest = rest.split()
            objs.append({'kind': 'access', 'id': path, 'value': {'sha256': digest}})
        elif tag == 'K':
            acct, line = rest.split(' ', 1)
            kt, key = line.split()[:2]
            objs.append({'kind': 'ssh-key', 'id': '%s %s %s' % (acct, kt, key), 'value': {}})
    ok('account', 'live: /etc/passwd'); ok('group', 'live: /etc/group')
    ok('access', 'live: /etc/sudoers.d/* and /etc/dropbear/authorized_keys/*')
    for l in lines:
        tag, _, rest = l.partition(' ')
        if tag == 'V':
            if rest == '-':
                errors.append({'kind': 'service', 'reason': '/run/confos-services.json unreadable'})
                continue
            table = json.loads(base64.b64decode(rest))
            if not isinstance(table, dict) or not all(isinstance(v, dict) for v in table.values()):
                errors.append({'kind': 'service', 'reason': 'unexpected service table format'})
                continue
            for name, sv in table.items():
                objs.append({'kind': 'service', 'id': name, 'value': {'state': sv.get('state'), 'argv': sv.get('argv')}})
        elif tag == 'VR' and rest != '-':
            running = json.loads(base64.b64decode(rest))
            for o in objs:
                if o['kind'] == 'service' and isinstance(running, dict):
                    o['running_pid'] = running.get(o['id'])
    ok('service', 'live: /etc/confos/services.json (table in force) and /run/confos-services.json (process ids)')
    for l in lines:
        tag, _, rest = l.partition(' ')
        if tag == 'I':
            f = rest.split()
            fam, addr, ifc = f[2], f[3], f[1]
            scope = f[f.index('scope') + 1] if 'scope' in f else ''
            if scope == 'link':
                objs.append({'kind': 'network-link-local', 'id': ifc.rstrip(':') + ' ' + addr, 'value': {},
                             'classification': 'kernel-automatic', 'question': 'Q-AUTOMATIC'})
            elif scope == 'host':
                objs.append({'kind': 'network', 'id': addr, 'value': {}})
            else:
                objs.append({'kind': 'network', 'id': addr, 'value': {}})
        elif tag in ('T4', 'T6'):
            f = rest.split()
            if f[0] == 'default' and tag == 'T6':
                objs.append({'kind': 'route', 'id': ' '.join(f[:3]), 'value': {}})
            elif f[0] == 'default':
                for o in objs:
                    if o['kind'] == 'network' and ':' not in o['id'] and not o['id'].startswith('127.'):
                        o['value']['gateway'] = f[2]
            elif 'proto' in f and f[f.index('proto') + 1] == 'kernel':
                continue
            elif f[0].startswith(('fe80', 'multicast', 'local', 'ff00')):
                continue
            else:
                objs.append({'kind': 'route', 'id': ' '.join(f[:3]), 'value': {}})
    ok('network', 'live: ip -o addr, ip route, ip -6 route')
    for l in lines:
        tag, _, rest = l.partition(' ')
        if tag == 'M':
            f = rest.split()
            sep = f.index('-')
            opts = set(f[5].split(','))
            objs.append({'kind': 'mount', 'id': f[4], 'value': {'fstype': f[sep + 1], 'noexec': 'noexec' in opts, 'ro': 'ro' in opts}})
            if 'noexec' not in opts and 'ro' not in opts and f[4] not in ('/', '/sys/kernel/security'):
                objs.append({'kind': 'open-folder', 'id': f[4], 'value': {'scope': 'execute'},
                             'evidence': 'writable mount without noexec: ' + rest})
        elif tag == 'D':
            objs.append({'kind': 'module', 'id': rest.split()[0], 'value': {}})
        elif tag == 'D-ABSENT':
            cov['module'] = {'status': 'not-applicable', 'evidence': 'live: /proc/modules absent', 'reason': 'INTERFACE 5: loadable kernel modules: none'}
        elif tag == 'Y':
            k, _, v = rest.partition(' ')
            objs.append({'kind': 'sysctl', 'id': k, 'value': {'value': v}})
        elif tag == 'Y0':
            k, _, v = rest.partition(' ')
            if v != '0' and not any(o['kind'] == 'sysctl' and o['id'] == k for o in objs):
                objs.append({'kind': 'sysctl', 'id': k, 'value': {'value': v}})
        elif tag == 'L':
            m = re.search(r'LANG=(\S+)', rest)
            objs.append({'kind': 'locale', 'id': 'LANG', 'value': {'value': m.group(1) if m else None}})
        elif tag == 'Z':
            link = rest.split()[0] if rest.split() else ''
            objs.append({'kind': 'time', 'id': 'timezone', 'value': {'zone': link.split('zoneinfo/')[-1] if 'zoneinfo/' in link else link}})
        elif tag == 'H':
            a = rest.split()
            objs.append({'kind': 'hostname', 'id': 'hostname', 'value': {'name': a[0] if a and len(set(a)) == 1 else a}})
        elif tag == 'FW-ERROR':
            errors.append({'kind': 'firewall-rule', 'reason': 'confos rules failed: ' + rest[:200]})
    # Packet filter in force (INTERFACE 6, `confos rules` as the superuser = the live ruleset):
    # every statement of every chain is one firewall-rule object, named by its statement.
    fw = [l[3:] for l in lines if l.startswith('FW ')]
    if 'FW-END' in lines:
        table = chain = None
        for l in fw:
            t = l.strip()
            m = re.match(r'table (\S+ \S+) \{$', t)
            if m:
                table = m.group(1); continue
            m = re.match(r'chain (\S+) \{$', t)
            if m:
                chain = m.group(1); continue
            if t == '}':
                if chain: chain = None
                else: table = None
                continue
            if chain and t and not t.startswith(('type ', 'policy ')):
                rid = t if (table, chain) == ('inet confos', 'input') else '%s %s: %s' % (table, chain, t)
                objs.append({'kind': 'firewall-rule', 'id': rid, 'value': {}})
        cov['firewall-rule'] = {'status': 'complete', 'evidence': 'live: confos rules as the superuser'}
    elif not any(e.get('kind') == 'firewall-rule' for e in errors):
        errors.append({'kind': 'firewall-rule', 'reason': 'packet filter not captured'})
    ok('mount', 'live: /proc/self/mountinfo')
    if 'module' not in cov:
        ok('module', 'live: /proc/modules')
    ok('sysctl', 'live: /proc/sys values of the declared keys and net.ipv4.ip_forward')
    ok('locale', 'live: /etc/locale.conf'); ok('time', 'live: /etc/localtime, /etc/timezone')
    ok('hostname', 'live: hostname and /proc/sys/kernel/hostname')
    radio = [l for l in lines if l.startswith('X ')]
    for kind, cls in (('wifi', 'ieee80211'), ('bluetooth', 'bluetooth')):
        if any(l.startswith('X ' + cls) for l in radio) or (kind == 'wifi' and any(l.startswith('X wireless') for l in radio)):
            ok(kind, 'live: /sys/class/' + cls)
            objs.append({'kind': kind, 'id': 'device', 'value': {}})
        else:
            cov[kind] = {'status': 'not-applicable', 'evidence': 'live: /sys/class/%s absent or empty' % cls,
                         'reason': 'INTERFACE 5: no radio stack in the virtual machine base'}
    tools_ = [l.split()[2] for l in radio if l.startswith('X tool')]
    cov['saved-network'] = ({'status': 'not-applicable', 'evidence': 'live: no wireless device and no network manager program (command -v)',
                             'reason': 'INTERFACE 5: no saved Wi-Fi networks'} if not tools_ else
                            {'status': 'incomplete', 'evidence': 'network manager programs present: ' + ' '.join(tools_)})
    for l in lines:
        if l.startswith('F '):
            _, path, mode, uid, gid, typ, size = l.split(' ')
            objs.append({'kind': 'volatile', 'id': path, 'value': {'mode': mode.zfill(4), 'uid': int(uid), 'gid': int(gid), 'type': typ}})
    return {'objects': objs, 'errors': errors, 'coverage': cov, 'raw': {'command': 'LIVE_SCRIPT', 'returncode': raw['returncode'],
            'stdout_sha256': sha(text.encode()), 'stdout': text}}


NOEXEC_DATA = ('/home/', '/root/', '/data/', '/tmp/', '/var/', '/run/', '/dev/shm/')


def classify(stored, material, live):
    """Data classification of stored/volatile files on noexec places (5.3 'Data').

    Material the case put is 'material' with its observed routes; any other file on a
    place the live mount table shows noexec gets a data route whose evidence is that
    mount entry. Opened folders (exec mounts) are 'opened-material'. Nothing is dropped.
    """
    mounts = {o['id']: o['value'] for o in live['objects'] if o['kind'] == 'mount'}
    def mount_of(path):
        best = max((m for m in mounts if path == m or path.startswith(m.rstrip('/') + '/')), key=len, default=None)
        return best, mounts.get(best)
    out = []
    for o in stored + [x for x in live['objects'] if x['kind'] == 'volatile']:
        o = dict(o)
        path = o['id']
        if o.get('classification') or o['kind'] not in ('file', 'dir', 'symlink', 'hardlink', 'special', 'volatile') \
                or not path.startswith(NOEXEC_DATA):
            out.append(o)
            continue
        live_path = '/' + path[len('/data/'):] if path.startswith(('/data/home/', '/data/root/')) else path
        mp, m = mount_of(path)
        lmp, lm = mount_of(live_path)
        if live_path != path and lm and not lm['noexec'] and not lm.get('ro') and lmp not in ('/', None) and lmp != mp:
            # Seen in the running system below an exec mount of its own (an opened folder):
            # the checking program decides by the declaration's open lines (core.compare).
            o.update(classification='opened-material', value=dict(o.get('value', {}), resolved_path=live_path),
                     route_evidence='exec mount %s (live mountinfo)' % lmp)
        elif live_path in material or path in material:
            mm = material.get(live_path) or material[path]
            o.update(classification='material', origin_evidence=mm['origin'], route_evidence='commands of this case',
                     routes=mm['routes'] or [{'kind': 'data', 'observed': True, 'evidence': 'put by the case; never named by a command'}])
        elif m and m['noexec']:
            o.update(classification='material', origin_evidence='written in a writable place after boot',
                     route_evidence='mount %s is noexec (live mountinfo)' % mp,
                     routes=[{'kind': 'data', 'observed': True, 'evidence': 'noexec mount ' + mp}])
        elif mp == '/' or m is None:
            pass                              # no mount of its own seen: leave it unattributed
        elif m and not m['noexec']:
            o.update(classification='opened-material', value=dict(o.get('value', {}), resolved_path=path),
                     route_evidence='exec mount %s (an opened folder?)' % mp)
        out.append(o)
    return out


def _derive_inputs(self, request):
    """UND-0: derivation from the declaration and named package inputs only; no machine."""
    decl = self.b.render(self._declaration(request['declaration']))
    sem = self._semantic(decl)
    reader = self.package_reader()
    from core import derive
    out = derive(sem, reader)
    return {'machine_reads': list(self.guest.calls) if hasattr(self.guest, 'calls') else [],
            'errors': out['errors'], 'objects': len(out['objects']),
            'inputs': {'tree': str(self.c.get('tree_commit')), 'store_manifest': self.c.get('store_manifest'),
                       'declaration': decl.identity}}


def _package_reader(self):
    """The clean store of the base; case packages from the case party's own independent
    build of their recipes (derive_store), never from an archive the system built."""
    try:
        import adapter_disk
    except ImportError as exc:
        raise Unavailable('package reader not available: ' + str(exc))
    readers = [adapter_disk.store_package_reader(self.c['packages'], Path(self.c['tree']) / 'recipes')]
    if self.c.get('derive_store'):
        readers.append(adapter_disk.store_package_reader(self.c['derive_store']))
    if self.c.get('update_store'):    # own builds of the packages the update states change
        readers.append(adapter_disk.store_package_reader(self.c['update_store']))
    index = dict(self.c.get('store_index') or {})
    index.update(self.c.get('derive_index') or {})
    index.update(self.c.get('update_store_index') or {})
    def read(line):
        line = dict(line)
        if not line.get('archive_sha256'):
            line['archive_sha256'] = index.get(line['archive'])
        last = None
        for r in readers:
            try:
                return r(line)
            except ValueError as exc:
                last = exc
        raise last
    return overlay_reader(read, [])


def _two_clean_builds(self, request):
    """Two clean installations from separately built package stores, lines in two orders."""
    if request.get('source_states'):
        raise Unavailable('INTERFACE 5: no "newest version" selector; source states cannot be resolved')
    stores = self.c.get('repro_stores') or []
    if len(stores) < 2:
        raise Unavailable('two independently built package stores are needed (config repro_stores); one store '
                          'would make the builds share every compiled package')
    d = self._declaration(request['declaration'])
    orders = request.get('orders') or [None, None]
    builds = []
    for i, (store, order) in enumerate(zip(stores, orders)):
        decl = self.b.render(d, order)
        saved = self.c['packages']
        self.c['packages'] = store
        try:
            built = self._build(decl, 'repro-%d' % i)
        finally:
            self.c['packages'] = saved
        if built['returncode'] or built['identity'] != decl.identity:
            raise Unavailable('clean build %d failed: %s' % (i, built['log_tail'][-300:]))
        gen, applied, boot, files, ev = read_committed(built['disk'])
        passwd = None
        try:
            import adapter_disk
            info = adapter_disk.read_disk(built['disk'], self.work / ('repro-read-%d' % i), self.c.get('subid'))
            passwd = info['generations'][info['selected']].get('texts', {}).get('/etc/passwd')
            passports = info['generations'][info['selected']].get('passports', {})
        except ImportError:
            passports = {}
        builds.append({'work_id': built['work_id'], 'log_sha256': built['log_sha256'], 'source_sha256': self.c.get('sources_manifest'),
                       'clean': True, 'cloned': False, 'store': str(store), 'identity': decl.identity, 'order': order,
                       'passwd': passwd, 'passports': passports, 'lines': decl.lines()})
    self.repro = builds
    return {'builds': builds, 'returncode': 0}


def _named_fields(build, decl_lines):
    """Only what lines name: package source/recipe, explicit account fields, settings."""
    named = {}
    for line in decl_lines:
        f = shlex.split(line)
        if f[0] == 'account':
            row = next((l.split(':') for l in (build['passwd'] or '').splitlines() if l.split(':')[0] == f[1]), None)
            if row is None:
                named['account ' + f[1]] = None
                continue
            v = {'shell': row[6], 'home': row[5]}
            if f[2] != 'auto':
                v['uid'] = row[2]
            if f[3] != 'auto':
                v['gid'] = row[3]
            named['account ' + f[1]] = v
        elif f[0] == 'package':
            text = build['passports'].get(f[1], '')
            named['package ' + f[1]] = sorted(l for l in text.splitlines() if l.startswith(('source ', 'recipe ', 'version ')))
    return named


def _q_named_equal(self, request):
    a, b = self.repro
    left, right = _named_fields(a, a['lines']), _named_fields(b, b['lines'])
    return {'left': left, 'right': right, 'evidence': {'a': a['work_id'], 'b': b['work_id']}}


def _q_same_declaration(self, request):
    a, b = self.repro
    return {'left': sorted(a['lines']), 'right': sorted(b['lines']), 'evidence': {'a': a['identity'], 'b': b['identity']}}


def _q_independent(self, request):
    return {'builds': self.repro}


Native.op_derive_inputs = _derive_inputs
Native.package_reader = _package_reader
Native.op_two_clean_builds = _two_clean_builds
Native.q_named_state_equal = _q_named_equal
Native.q_named_account_fields_equal = _q_named_equal
Native.q_same_declaration = _q_same_declaration
Native.q_independent_build_evidence = _q_independent


class PayloadServer:
    """Case-controlled HTTP server on the host loopback (QEMU user networking: 10.0.2.2 in
    the guest). Files are made from the frozen payload sources; each fetch is logged."""

    def __init__(self, directory, port):
        import http.server, threading
        self.dir, self.log = Path(directory), []
        log = self.log
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(s, *a, **k):
                super().__init__(*a, directory=str(directory), **k)
            def log_message(s, fmt, *args):
                log.append({'monotonic': time.monotonic(), 'line': fmt % args})
        self.httpd = http.server.ThreadingHTTPServer(('127.0.0.1', int(port)), Handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def close(self):
        self.httpd.shutdown()


def make_server_files(bindings, out, store=None):
    """Builds the server's files on the host from frozen payload sources (no guest code)."""
    import tarfile, io
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    pl = bindings.root / 'payloads'
    subprocess.run(['gcc', '-static', '-O2', '-o', str(out / 'payload'), str(pl / 'case-marker.c')], check=True)
    with tarfile.open(out / 'payload.tar.gz', 'w:gz') as t:
        t.add(out / 'payload', arcname='case-marker')
    blob = base64.b64encode((out / 'payload').read_bytes()).decode()
    (out / 'selfextract.sh').write_text('#!/bin/sh\nset -e\nd=$(dirname "$0")/se; mkdir -p $d\nbase64 -d > $d/case-marker <<\'EOF\'\n'
                                       + blob + '\nEOF\nchmod +x $d/case-marker\nexec $d/case-marker\n')
    shutil.copy(pl / 'case-input.py', out / 'payload.py')
    shutil.copy(pl / 'persistent.sh', out / 'persistent.sh')
    shutil.copy(pl / 'case-small.c', out / 'case-small.c')
    shutil.copy(pl / 'document.txt', out / 'document')
    subprocess.run(['gcc', '-O2', '-DCASE_FETCH="curl"', '-o', str(out / 'case-probe-2'), str(pl / 'case-probe.c')], check=True)
    if store and (Path(store) / 'case-small-2.confpkg').is_file():
        shutil.copy(Path(store) / 'case-small-2.confpkg', out / 'case-small-2.confpkg')
    return {p.name: sha(p.read_bytes()) for p in sorted(out.iterdir())}


ABSENT_OPS = {
    'container': 'no container runtime in 0.67 (EXECUTORS.md)',
    'guest-system': 'no hypervisor program in the 0.67 base (base.conf)',
    'external-server': 'INTERFACE 5: no account server (question 9)',
    'radio-request': 'INTERFACE 5: no radio stack in the virtual machine base; the laptop cases come later',
    'record-radio-if-needed': 'INTERFACE 5: no saved Wi-Fi networks or Bluetooth pairings',
    'prepare-shared': 'INTERFACE 5 and 8: no run-time dependency between package lines',
    'start-apply': 'INTERFACE 5 and 8: confos apply transfers nothing over the network',
    'finish-apply': 'INTERFACE 5 and 8: confos apply transfers nothing over the network',
    'review-event': 'the decision on a breaking candidate belongs to the review, not to the case party',
}


def _perform(self, request):
    op = request['op']
    if op in ABSENT_OPS:
        raise Unavailable(ABSENT_OPS[op])
    fn = getattr(self, 'op_' + op.replace('-', '_'), None)
    if fn is None:
        raise Unavailable('operation not bound for 0.67: ' + op)
    try:
        return fn(request)
    except (Unavailable, KeyError, ValueError, TypeError, OSError):
        raise
    except Exception as exc:                 # an adapter defect: an unobserved row, never a pass
        import traceback
        raise ValueError('adapter error %s: %s | %s' % (type(exc).__name__, exc, traceback.format_exc()[-600:]))


def _clone(self, request):
    """Every case runs on its own fresh installation: the guest is already disposable."""
    return {'scope': 'owned-guest', 'disk': str(self.disk), 'note': 'the disk of this case only; deleted after it'}


def _raw_root_write(self, request):
    data = self.b.payload(request['source'])
    path = request['path']
    r = self.guest.run('root', 'cat > %s && chmod 0755 %s' % (shlex.quote(path), shlex.quote(path)), stdin=data)
    self.forced = {'path': path, 'reply': r}
    return dict(r, path=path)


def _q_forced_effect(self, request):
    f = getattr(self, 'forced', None)
    if not f:
        raise Unavailable('no breaking candidate was attempted')
    present, r = self.probe('test -e ' + shlex.quote(f['path']))
    if not present:
        raise Unavailable('the superuser in a session could not write past the system tools (INTERFACE 4); '
                          'no breaking event exists to review: ' + f['reply']['stderr'][-200:])
    return {'value': True, 'probe': r, 'write': f['reply']}


Native.perform = _perform
Native.op_clone_disposable = _clone
Native.op_raw_root_write = _raw_root_write
Native.q_forced_effect = _q_forced_effect


ABSENT_QUERIES = {
    'radio-kind': 'INTERFACE 5: no radio stack in the virtual machine base (no wireless or Bluetooth device)',
    'radio-effective': 'INTERFACE 5: no radio stack in the virtual machine base',
    'radio-stored': 'INTERFACE 5: no saved Wi-Fi networks or Bluetooth pairings',
    'account-lookup': 'INTERFACE 5: no account server (question 9)',
    'external-accounts-active': 'INTERFACE 5: no account server (question 9)',
    'container-child': 'no container runtime in 0.67 (EXECUTORS.md)',
    'process-identity': 'no container runtime in 0.67 (EXECUTORS.md)',
    'guest-output': 'no hypervisor program in the 0.67 base',
    'unrecorded-host-effect': 'no hypervisor program in the 0.67 base',
    'download-bytes': 'INTERFACE 5 and 8: confos apply transfers nothing over the network',
    'named-fields-satisfied': 'INTERFACE 5: no "newest version" selector',
    'resolved-versions': 'INTERFACE 5: no "newest version" selector',
}
_orig_query = Native.op_query


def _op_query(self, request):
    if request['subject'] in ABSENT_QUERIES:
        raise Unavailable(ABSENT_QUERIES[request['subject']])
    return _orig_query(self, request)


def _keys(objs):
    return {(o['kind'], o['id']) for o in objs}


def _q_remaining(self, request):
    """Objects contributed only by the removed line that are still observed (5.2(4))."""
    from core import derive
    if not getattr(self, 'removal', None):
        raise Unavailable('removal target not prepared')
    native, inputs = self.b.native_for({'kind': 'binding', 'name': self.removal['slot']})
    removed = NativeDecl({MAIN: ('base 0.67\n' + '\n'.join(native) + '\n').encode()}, inputs)
    sem = self._semantic(removed)
    sem['lines'] = [l for l in sem['lines'] if not l['id'].startswith(('release-', 'rendered:'))]
    reader = self.package_reader()
    contrib = derive(sem, reader)
    current = derive(self._semantic(self.candidate), reader)
    if contrib['errors'] or current['errors']:
        raise Unavailable('contributions not derivable: %r' % (contrib['errors'] + current['errors'])[:3])
    now = self.op_inventory({'op': 'inventory'})
    hashes = {o['value'].get('sha256') for o in contrib['objects'] if o['kind'] == 'file' and o.get('value', {}).get('sha256')}
    keep = _keys(current['objects'])
    still = sorted([list(k) for k in _keys(contrib['objects']) & _keys(now['objects']) if k not in keep])
    still += sorted([['process', o['id']] for o in now['objects']
                     if o['kind'] in ('process', 'port') and o['value'].get('exe_sha256') in hashes - {None}])
    return {'value': still, 'removed_lines': native, 'evidence': {'contributed': len(contrib['objects']),
            'inventory_generation': now.get('selected_generation')}}


Native.op_query = _op_query
Native.q_remaining_unowned_contributions = _q_remaining


def chroot_run(cfg, inner, binds, timeout=7200):
    """Runs INNER in the clean bootstrap root as root of a user namespace (PROCEDURE 3).

    binds: {inside path: (host path, 'ro'|'rw')}. The root is made a mount point first.
    """
    sub = str(int(cfg['subid']))
    names = sorted(binds)
    script = ['set -e; umask 022; R=$1; shift; mount --bind $R $R;',
              'for m in dev proc sys run tmp; do mkdir -p $R/$m; done;',
              'mount --rbind /dev $R/dev; mount -t proc proc $R/proc; mount -t sysfs sysfs $R/sys; mount -t tmpfs tmpfs $R/run;']
    env = dict(os.environ)
    for i, inside in enumerate(names):
        host, mode = binds[inside]
        env['BIND%d' % i] = str(host)
        script.append('mkdir -p $R%s; mount --bind "$BIND%d" $R%s;' % (inside, i, inside))
        if mode == 'ro':
            script.append('mount -o remount,bind,ro $R%s;' % inside)
    script.append('exec /usr/sbin/chroot "$R" /usr/bin/env -i HOME=/root PATH=/usr/bin:/usr/sbin LC_ALL=POSIX "$@"')
    argv = ['unshare', '--user', '--map-root-user', '--map-users=1:%s:65535' % sub, '--map-groups=1:%s:65535' % sub,
            '--mount', '--pid', '--net', '--uts', '--ipc', '--fork', '--kill-child', '--', 'bash', '-c', ' '.join(script),
            'chroot-run', str(cfg['bootstrap_root'])] + inner
    with open(str(cfg['bootstrap_root']).rstrip('/') + '.lock', 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)     # one user of the bootstrap root at a time
        return subprocess.run(argv, capture_output=True, env=env, timeout=timeout)


def build_derive_store(cfg, bindings, out):
    """Independent build of every payload recipe (the case party's own derivation input)."""
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    results = {}
    for recipe in sorted((bindings.root / 'payloads').glob('*.recipe')):
        p = chroot_run(cfg, ['python3', '/confos/tools/confpkg', 'build', '/in/' + recipe.name, '--sources', '/in',
                             '--out', '/out', '--work', '/tmp/w-%d-%s' % (os.getpid(), recipe.stem)],
                       {'/in': (bindings.root / 'payloads', 'ro'), '/out': (out, 'rw'), '/confos': (cfg['tree'], 'ro')})
        results[recipe.name] = {'returncode': p.returncode, 'tail': (p.stdout + p.stderr)[-400:].decode(errors='replace')}
    index = {a.name: sha(a.read_bytes()) for a in sorted(out.glob('*.confpkg'))}
    return index, results


READERS = {'sh', 'bash', '/bin/sh', '/bin/bash', 'python3', 'perl', 'gawk', 'awk', 'sed', 'make', 'm4', 'bc', 'dc',
           '.', 'source', '/lib64/ld-linux-x86-64.so.2'}


def route_kind(command, path):
    """How a typed command uses a saved file: 'direct' when the file is run or handed to a
    reader as code (first word, or the operand of a shell/interpreter/loader, or a `read`
    of the recorded reader); 'data' otherwise (cat, cp, grep, ...); None if not named."""
    if path not in command:
        return None
    try:
        words = shlex.split(command.replace(';', ' ; ').replace('|', ' | ').replace('&&', ' && '))
    except ValueError:
        return 'direct'
    for i, w in enumerate(words):
        if path not in w:
            continue
        prev = words[i - 1] if i else ';'
        if re.search(r'\$\(\s*cat\s+' + re.escape(path) + r'\s*\)', w):
            continue                          # typed command substitution reads the file like `cat FILE |`
        if prev in (';', '|', '&&', '||') or w == path and i == 0:
            return 'direct'
        if prev in READERS or prev.startswith('-') and i > 1 and words[i - 2] in READERS:
            return 'direct'
        if prev in ('read', 'values') and i > 1 and words[i - 2] == 'case-probe':
            # Q4: a recorded program that reads a file and executes it is that program acting;
            # for the file this is a data route; installation/configuration is checked apart
            return 'data' if prev == 'read' else 'values'
        if '<' in prev and i > 1 and words[i - 2] in READERS:
            return 'direct'
    return 'data'


# ------------------------------------------------- the update sequence (OW-2 then OW-3)

SEQUENCE = 'sequence-system-updates'


def _keep_sequence(self):
    """OW-2 hands its installation to OW-3 (CASES.md: one sequence on the same installation).
    The guest is synced and powered down by its power button; disk and candidate are kept."""
    seq = Path(self.c['work']) / SEQUENCE
    if seq.exists():
        shutil.rmtree(seq)
    seq.mkdir(parents=True)
    self.guest.run('root', 'sync')
    if self.machine.proc and self.machine.proc.poll() is None:
        self.machine.qmp_cmd('system_powerdown')
        try:
            self.machine.proc.wait(timeout=120)
        except subprocess.TimeoutExpired:
            pass
    self.machine.stop()
    shutil.move(str(self.disk), str(seq / 'disk.raw'))
    cand = self.candidate
    (seq / 'state.json').write_text(json.dumps({
        'previous_case': self.case['id'], 'identity': cand.identity,
        'files': {k: base64.b64encode(v).decode() for k, v in cand.files.items()},
        'inputs': {k: base64.b64encode(v).decode() for k, v in cand.inputs.items()}}))


def _resume_sequence(self, request):
    seq = Path(self.c['work']) / SEQUENCE
    if not (seq / 'state.json').is_file() or not (seq / 'disk.raw').is_file():
        raise Unavailable('the installation of OW-2 was not handed over (OW-2 did not finish in this run)')
    st = json.loads((seq / 'state.json').read_text())
    d = self.work / 'sequence'
    d.mkdir(parents=True, exist_ok=True)
    shutil.move(str(seq / 'disk.raw'), str(d / 'disk.raw'))
    shutil.rmtree(seq)
    self.disk = str(d / 'disk.raw')
    self.candidate = NativeDecl({k: base64.b64decode(v) for k, v in st['files'].items()},
                                {k: base64.b64decode(v) for k, v in st['inputs'].items()})
    self.fresh_decl = self.candidate
    booted = self._boot(self.disk)
    return dict(booted, previous_case=st['previous_case'], identity=st['identity'],
                returncode=0 if booted['status'] == 'APPLIED ' + st['identity'] else 1)


def _select_update_start(self, request):
    """The installation must stand at the named state: its base line is the one of T0."""
    want = self.b.slot('system-update-state-' + request['state'])['native'][0]
    have = [' '.join(f) for rel, n, f in self.candidate.rows if f[0] == 'base']
    if have != [want]:
        raise Unavailable('the installation is not at %s: base line %r, expected %r' % (request['state'], have, want))
    st, sr = self.status()
    return {'state': request['state'], 'base_line': have[0], 'status': st, 'returncode': 0}


def _state_of_release(self, release):
    for state, rel in (self.c.get('update_releases') or {}).items():
        if rel == release:
            return state
    return None


def _q_system_source_state(self, request):
    """INTERFACE 9: after an update VERSION_ID in /etc/os-release names the release."""
    r = self.guest.run('user', 'cat /etc/os-release')
    if r['returncode']:
        raise Unavailable('/etc/os-release unreadable')
    m = re.search(r'^VERSION_ID="?([^"\n]*)"?$', r['stdout'], re.M)
    release = m.group(1) if m else None
    boot = re.findall(r'CONFOS BOOT DONE (\S+)', self.machine.serial_text()) if self.machine else []
    return {'value': self._state_of_release(release), 'version_id': release, 'os_release': r,
            'boot_done_lines': boot[-3:]}


def _components(self, names):
    """The passports of the named packages on the running system: version and sources."""
    import adapter_disk
    out, raw = {}, {}
    for name in sorted(names):
        r = self.guest.run('user', 'cat /usr/lib/confpkg/%s.passport' % shlex.quote(name))
        raw[name] = {k: r[k] for k in ('command', 'returncode', 'stdout')}
        if r['returncode']:
            continue
        try:
            pp = adapter_disk.parse_passport(r['stdout'])
        except (ValueError, KeyError):
            continue
        out[name] = '%s %s' % (pp['version'], ' '.join('%s:%s' % tuple(x) for x in pp['sources']))
    return out, raw


def _update_names(self, state):
    return sorted(n.split()[1] for n in self.b.slot(state)['native'] if n.startswith('package '))


def _q_system_components_changed(self, request):
    """Raw operands for core.evaluate_query: the passports of the packages the update state
    changes, read before the edit (op_edit) and now; the bound component set (INTERFACE 9)."""
    before = getattr(self, 'before_components', None)
    if before is None:
        raise Unavailable('the components were not read before the update edit')
    after, raw = self._components(before['names'])
    return {'before_components': before['values'], 'after_components': after,
            'system_components': before['names'], 'binding_evidence': {'state': before['state'],
            'native': self.b.slot(before['state'])['native']}, 'before_raw': before['raw'], 'after_raw': raw,
            'source_state': self.q_system_source_state(request)}


_orig_op_edit = Native.op_edit


def _op_edit(self, request):
    line = request.get('line', {})
    if line.get('kind') == 'base':
        names = self._update_names(line['binding'])
        values, raw = self._components(names)
        self.before_components = {'state': line['binding'], 'names': names, 'values': values, 'raw': raw}
    return _orig_op_edit(self, request)


Native._components = _components
Native._update_names = _update_names
Native.op_edit = _op_edit


Native._keep_sequence = _keep_sequence
Native.op_resume_sequence = _resume_sequence
Native.op_select_update_start = _select_update_start
Native._state_of_release = _state_of_release
Native.q_system_source_state = _q_system_source_state
Native.q_system_components_changed = _q_system_components_changed

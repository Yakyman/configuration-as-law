"""Read-only package adapters. Database records, never package code, are executed."""
import base64
import csv
import hashlib
import io
import json
import os
import re
import shlex

MAX_DB = 16 * 1024 * 1024
MAX_HASH = 16 * 1024 * 1024


def text(data):
    return data.decode('utf-8', 'replace') if isinstance(data, bytes) else str(data)


def read(ctx, path, limit=MAX_DB):
    cached = getattr(ctx, '_package_read_cache', {}).get(path)
    data, rc, evidence = cached if cached is not None else ctx.safe_read(path, limit=limit)
    return text(data), rc, evidence


def gap(ctx, message, ownership=False):
    ctx.gaps.append(message)
    if ownership:
        ctx.package_ownership_complete = False


def package(ctx, manager, name, reason, evidence, **extra):
    pid = ctx.add(1, 'package', manager + ':' + name,
                  dict(manager=manager, reason=reason, **extra), evidence)
    if manager in ('dpkg', 'rpm', 'pacman', 'apk', 'xbps', 'portage'):
        ctx._native_package_ids.add(pid)
    return pid


def native_owners(ctx, path):
    return sorted(ctx.owned.get(path, set()) & ctx._native_package_ids)


def file_record(ctx, pid, path, evidence, digest=None, algorithm='md5', size=None):
    if not path.startswith('/'):
        return
    path = os.path.normpath(path)
    ctx.owned.setdefault(path, set()).add(pid)
    result, rule = 'unknown', 'No usable recorded digest; no equality inferred from presence.'
    meta = ctx.entries.get(path)
    if meta and size is not None and str(meta.get('type')) in ('file', 'regular'):
        if int(meta.get('size', -1)) != int(size):
            result, rule = 'changed', 'Recorded installation size differs.'
    record = dict(package=pid, path=path, integrity=result, evidence=evidence, rule=rule)
    ctx.package_files.append(record)
    if digest and not path.startswith(('/proc/', '/sys/', '/dev/')) and path not in ('/proc','/sys','/dev'):
        ctx._package_digest_jobs.append((path, algorithm, digest.lower(), record))


def verify(ctx):
    jobs = ctx._package_digest_jobs
    if hasattr(ctx, 'digests'):
        results = ctx.digests(list(dict.fromkeys((p,a) for p,a,d,r in jobs)), max_bytes=MAX_HASH)
    else:
        results = {}
        for path, alg, expected, record in jobs:
            if (path, alg) in results: continue
            current, rc, ev = ctx.digest(path, alg, max_bytes=MAX_HASH)
            results[(path, alg)] = dict(digest=current, status=rc, evidence=ev)
    for path, alg, expected, record in jobs:
        answer = results.get((path,alg), results.get(path, {}))
        rc = answer.get('status')
        if rc in (0, 'ok'):
            record['integrity'] = 'unchanged' if answer.get('digest') == expected else 'changed'
            record['rule'] = 'Full bounded digest compared with manager installation record.'
        elif rc in (2, 'missing'):
            record['integrity'], record['rule'] = 'missing', 'Absent at bounded verification.'
        record['evidence'] = str(record['evidence']) + ';' + str(answer.get('evidence',''))


def query(ctx, label, command, timeout=60):
    out, rc, evidence = ctx.query(label, command, timeout=timeout)
    return text(out), rc, evidence


def dpkg(ctx):
    out, rc, ev = query(ctx, 'packages-dpkg', "dpkg-query -W -f='${db:Status-Abbrev}\\t${binary:Package}\\t${Version}\\n'")
    if rc:
        gap(ctx, 'dpkg package query failed: ' + ev, True); return
    manual, rm, em = query(ctx, 'package-reasons-apt-manual', 'apt-mark showmanual')
    auto, ra, ea = query(ctx, 'package-reasons-apt-auto', 'apt-mark showauto')
    manual, auto = set(manual.splitlines()), set(auto.splitlines())
    allconf, acr, ace = query(ctx, 'package-conffiles-dpkg', "dpkg-query -W -f='PACKAGE:${binary:Package}\\n${Conffiles}\\n'")
    conffile_map, current = {}, None
    for line in allconf.splitlines():
        if line.startswith('PACKAGE:'): current = line[8:]; conffile_map[current] = {}
        else:
            m = re.match(r'^ (.+) ([0-9a-f]{32})(?: obsolete)?$', line)
            if m and current: conffile_map[current][m[1]] = m[2]
    for row in out.splitlines():
        cols = row.split('\t')
        if len(cols) != 3 or cols[0][1:2] != 'i': continue
        name, version = cols[1:]
        aliases = {name, name.split(':')[0]}
        reason = 'explicit' if not rm and aliases & manual else 'dependency' if not ra and aliases & auto else 'unknown'
        pid = package(ctx, 'dpkg', name, reason, ev + ';' + em + ';' + ea, version=version)
        stem = '/var/lib/dpkg/info/' + name
        if stem + '.list' not in ctx.entries and ':' in name:
            stem = '/var/lib/dpkg/info/' + name.split(':')[0]
        listing, lr, le = read(ctx, stem + '.list')
        if lr:
            gap(ctx, 'dpkg file manifest unavailable for ' + name + ': ' + le, True); continue
        sums, sr, se = read(ctx, stem + '.md5sums')
        hashes = {}
        if sr == 0:
            for line in sums.splitlines():
                m = re.match(r'^([0-9a-fA-F]{32})\s+(.+)$', line)
                if m: hashes['/' + m[2].lstrip('/')] = m[1]
        hashes.update(conffile_map.get(name, {}) if acr == 0 else {})
        ce = ace
        for path in listing.splitlines():
            file_record(ctx, pid, path, le + ';' + se + ';' + ce, hashes.get(path))


def rpm(ctx):
    out, rc, ev = query(ctx, 'packages-rpm', "rpm -qa --qf '%{NAME}\\t%{VERSION}-%{RELEASE}.%{ARCH}\\n'")
    if rc: gap(ctx, 'RPM package query failed: ' + ev, True); return
    # DNF4 and DNF5 expose the stored reason, including weak dependencies.
    # Do not infer a dependency merely from absence in --userinstalled.
    reason_fmt = '%{name}@%{version}-%{release}.%{arch}\t%{reason}\\n'
    reasons_out, rr, er = query(ctx, 'package-reasons-dnf',
        'dnf -C repoquery --installed --qf ' + shlex.quote(reason_fmt), 90)
    auto, ar, ae = read(ctx, '/var/lib/zypp/AutoInstalled')
    auto = set(auto.splitlines())
    reasons = {}
    if rr == 0:
        for row in reasons_out.splitlines():
            fields = row.split('\t')
            if len(fields) == 2:
                reasons[fields[0]] = fields[1].strip().lower().replace('-', ' ')
    selected_groups = {}
    group_evidence = ''
    if 'group' in reasons.values():
        from pathlib import Path
        script = Path(__file__).with_name('rpm-selected-groups.py').read_text()
        selected, gr, group_evidence = query(ctx, 'package-selected-groups-dnf',
            'test -r /var/lib/dnf/history.sqlite || exit 127; '
            'python3 -I -c ' + shlex.quote(script), 90)
        if gr == 0:
            for line in selected.splitlines():
                try:
                    item = json.loads(line)
                    if (isinstance(item, dict) and isinstance(item.get('package'), str)
                            and isinstance(item.get('selection'), list) and item['selection']):
                        selected_groups.setdefault(item['package'], []).append(item)
                except ValueError:
                    gap(ctx, 'DNF selected-group record could not be decoded: ' + group_evidence)
    ids = {}
    for row in out.splitlines():
        cols = row.split('\t')
        if len(cols) != 2: continue
        name, version = cols
        stored_reason = reasons.get(name + '@' + version, 'unknown')
        reason = ('explicit' if stored_reason == 'user' else
                  'dependency' if stored_reason in ('dependency', 'weak dependency') else 'unknown')
        if ar == 0: reason = 'dependency' if name in auto else 'explicit'
        ids[name + '@' + version] = package(ctx, 'rpm', name + '@' + version, reason,
            ev + ';' + er + ';' + ae + ';' + group_evidence, version=version, native_reason=stored_reason,
            selected_group_records=selected_groups.get(name, []),
            reason_rule='Stored user is explicit; stored dependency/weak-dependency is dependency. Group selection provenance is retained separately and does not establish individual package reason; group, external and absent remain unknown.')
    fmt = '[%{=NAME}@%{=VERSION}-%{=RELEASE}.%{=ARCH}\\t%{FILENAMES}\\t%{FILESIZES}\\t%{FILEDIGESTS}\\t%{=FILEDIGESTALGO}\\t%{FILEMODES}\\t%{FILELINKTOS}\\n]'
    files, fr, fe = query(ctx, 'package-files-rpm', 'rpm -qa --qf ' + shlex.quote(fmt), 120)
    if fr: gap(ctx, 'RPM file query failed: ' + fe, True); return
    # RPM documents an absent FILEDIGESTALGO as the legacy MD5 default.
    algorithms = {'(none)': 'md5', '0': 'md5', '1': 'md5', '2': 'sha1',
                  '8': 'sha256', '9': 'sha384', '10': 'sha512'}
    for row in files.splitlines():
        cols = row.split('\t')
        if len(cols) != 7 or cols[0] not in ids: continue
        name, path, size, digest, alg, mode, target = cols
        kind = (int(mode) & 0o170000) if mode.isdigit() else None
        if kind == 0o040000 and path.startswith('/'):
            ctx.owned.setdefault(os.path.normpath(path), set()).add(ids[name])
            continue  # Directory ownership is retained, without a file-integrity row.
        algorithm = algorithms.get(alg)
        usable_digest = (digest if algorithm and re.fullmatch(
            r'[0-9a-fA-F]{%d}' % (hashlib.new(algorithm).digest_size * 2), digest) else None)
        before = len(ctx.package_files)
        file_record(ctx, ids[name], path, fe, usable_digest,
                    algorithm or 'md5', int(size) if size.isdigit() else None)
        if len(ctx.package_files) > before and mode.isdigit():
            kind = int(mode) & 0o170000
            ctx.package_files[-1]['recorded_type'] = {
                0o100000: 'file', 0o040000: 'directory', 0o120000: 'symlink'
            }.get(kind, 'other')
            if kind == 0o120000:
                record = ctx.package_files[-1]
                current = ctx.entries.get(os.path.normpath(path))
                if current and current.get('type') == 'symlink' and 'target' in current:
                    record['integrity'] = 'unchanged' if current['target'] == target else 'changed'
                    record['rule'] = 'Symlink target compared with RPM installation FILELINKTOS record.'
                elif current and current.get('type') != 'symlink':
                    record['integrity'] = 'changed'
                    record['rule'] = 'Installed RPM symlink has been replaced by another file type.'


def pacman(ctx):
    out, rc, ev = query(ctx, 'packages-pacman', 'pacman -Q')
    manual, mr, me = query(ctx, 'package-reasons-pacman', 'pacman -Qqe')
    deps, dr, de = query(ctx, 'package-dependencies-pacman', 'pacman -Qqd')
    if rc: gap(ctx, 'pacman package query failed: ' + ev, True); return
    manual, deps, ids = set(manual.splitlines()), set(deps.splitlines()), {}
    for row in out.splitlines():
        cols = row.split(None, 1)
        if len(cols) != 2: continue
        name, version = cols
        reason = 'explicit' if not mr and name in manual else 'dependency' if not dr and name in deps else 'unknown'
        ids[name] = package(ctx, 'pacman', name, reason, ev + ';' + me + ';' + de, version=version)
    files, fr, fe = query(ctx, 'package-files-pacman', 'pacman -Ql', 120)
    if fr: gap(ctx, 'pacman ownership query failed: ' + fe, True); return
    for row in files.splitlines():
        cols = row.split(' ', 1)
        if len(cols) == 2 and cols[0] in ids: file_record(ctx, ids[cols[0]], cols[1], fe)
    gap(ctx, 'pacman file digest verification not implemented; integrity unknown unless missing.')


def apk(ctx):
    out, rc, ev = read(ctx, '/lib/apk/db/installed')
    world, wr, we = read(ctx, '/etc/apk/world')
    selected = {re.split('[<>=~@]', x)[0] for x in world.splitlines() if x and not x.startswith('#')}
    if rc: gap(ctx, 'apk installed database unavailable: ' + ev, True); return
    for block in out.split('\n\n'):
        fields = [line.split(':', 1) for line in block.splitlines() if ':' in line]
        hdr = dict((k,v) for k,v in fields if k in ('P','V'))
        if 'P' not in hdr: continue
        name = hdr['P']
        reason = ('explicit' if name in selected else 'dependency') if wr == 0 else 'unknown'
        pid = package(ctx, 'apk', name, reason, ev + ';' + we, version=hdr.get('V',''))
        directory, pending = '', None
        for key, value in fields:
            if key in ('F','R') and pending:
                file_record(ctx, pid, pending, ev); pending = None
            if key == 'F': directory = '/' + value.strip('/'); ctx.owned.setdefault(directory,set()).add(pid)
            elif key == 'R': pending = directory.rstrip('/') + '/' + value
            elif key == 'Z' and pending:
                digest = None
                if value.startswith('Q1'):
                    try: digest = base64.b64decode(value[2:]).hex()
                    except ValueError: pass
                file_record(ctx, pid, pending, ev, digest, 'sha1'); pending = None
        if pending: file_record(ctx, pid, pending, ev)


def xbps(ctx):
    # Native database layout: xbps-install(1), lib/pkgdb.c; SHA256 fields:
    # https://github.com/void-linux/xbps/blob/master/bin/xbps-create/main.c
    # Missing automatic-install is manual, as bin/xbps-query/list.c specifies.
    import gzip
    import plistlib
    from xml.parsers.expat import ExpatError

    def plist(blob):
        if blob.startswith(b'\x1f\x8b'):
            with gzip.GzipFile(fileobj=io.BytesIO(blob)) as stream:
                blob = stream.read(MAX_DB + 1)
        if len(blob) > MAX_DB:
            raise ValueError('Expanded XBPS metadata exceeds bound.')
        value = plistlib.loads(blob)
        if not isinstance(value, dict):
            raise ValueError('XBPS dictionary required.')
        return value

    db = '/var/db/xbps/pkgdb-0.38.plist'
    raw, rc, ev = ctx.safe_read(db, limit=MAX_DB)
    if rc:
        gap(ctx, 'XBPS package database unavailable: ' + ev, True); return
    try:
        records = plist(raw)
    except (ValueError, OSError, EOFError, plistlib.InvalidFileException, ExpatError):
        gap(ctx, 'XBPS package database could not be decoded: ' + ev, True); return
    paths = {name: '/var/db/xbps/.' + name + '-files.plist'
             for name, item in records.items()
             if isinstance(item, dict) and 'pkgver' in item and '/' not in name}
    manifests = ctx.safe_reads(list(paths.values()), limit=MAX_DB)
    for name, path in paths.items():
        item = records[name]
        automatic = item.get('automatic-install', False)
        reason = 'dependency' if automatic is True else 'explicit' if automatic is False else 'unknown'
        pid = package(ctx, 'xbps', item['pkgver'], reason, ev)
        blob, fr, fe = manifests[path]
        if fr:
            gap(ctx, 'XBPS file manifest unavailable: ' + fe, True); continue
        try:
            files = plist(blob)
        except (ValueError, OSError, EOFError, plistlib.InvalidFileException, ExpatError):
            gap(ctx, 'XBPS file manifest could not be decoded: ' + fe, True); continue
        for kind in ('files', 'conf_files', 'links', 'dirs'):
            for entry in files.get(kind, []):
                if not isinstance(entry, dict) or not isinstance(entry.get('file'), str):
                    gap(ctx, 'XBPS file manifest entry unsupported: ' + fe, True); continue
                digest = entry.get('sha256') if kind in ('files', 'conf_files') else None
                if digest is not None and not re.fullmatch(r'[0-9a-fA-F]{64}', str(digest)):
                    digest = None
                if kind == 'dirs':
                    if entry['file'].startswith('/'):ctx.owned.setdefault(os.path.normpath(entry['file']),set()).add(pid)
                    continue
                file_record(ctx, pid, entry['file'], fe, digest, 'sha256', entry.get('size'))
                if kind == 'links' and isinstance(entry.get('target'), str):
                    # XBPS records the literal installed link target. Compare the
                    # captured lstat/readlink result, never follow the link.
                    path = os.path.normpath(entry['file'])
                    meta = ctx.entries.get(path, {})
                    if ctx.package_files and ctx.package_files[-1]['path'] == path:
                        record = ctx.package_files[-1]
                        if meta.get('type') == 'symlink' and 'target' in meta:
                            record['integrity'] = 'unchanged' if meta['target'] == entry['target'] else 'changed'
                            record['rule'] = 'Literal symlink target compared with XBPS installation record.'
                        elif meta and meta.get('type') != 'symlink':
                            record['integrity'] = 'changed'
                            record['rule'] = 'Installed XBPS symlink replaced by a different file type.'


def portage(ctx):
    import pathlib
    helper = pathlib.Path(__file__).with_name('portage-reasons.py').read_text()
    data, reason_rc, reason_ev = query(ctx, 'package-reasons-portage', "python3 - <<'C1_PORTAGE_REASONS'\n" + helper + "\nC1_PORTAGE_REASONS", timeout=120)
    reasons = {}
    if reason_rc:
        gap(ctx, 'Portage selected-set reason query failed: ' + reason_ev)
    else:
        for row in data.splitlines():
            if not row.strip(): continue
            try: value = json.loads(row)
            except ValueError:
                gap(ctx, 'Portage reason query emitted a malformed record: ' + reason_ev)
                continue
            if not isinstance(value, dict):
                gap(ctx, 'Portage reason query emitted a non-object record: ' + reason_ev)
                continue
            if isinstance(value.get('cpv'), str) and value.get('reason') in ('explicit', 'dependency', 'unknown'):
                reasons[value['cpv']] = value['reason']
    contents = [p for p in ctx.entries if p.startswith('/var/db/pkg/') and p.endswith('/CONTENTS')]
    if not contents: gap(ctx, 'Portage package database manifests unavailable.', True)
    for path in contents:
        name = path[len('/var/db/pkg/'):-len('/CONTENTS')]
        reason = reasons.get(name, 'unknown')
        pid = package(ctx, 'portage', name, reason, reason_ev,
                      reason_rule='Unique installed-version match in expanded selected records is explicit; unmatched or ambiguous records remain unknown because current dependency edges do not establish installation history.')
        data, rc, ev = read(ctx, path)
        if rc: gap(ctx, 'Portage file manifest unavailable: ' + ev, True); continue
        for row in data.splitlines():
            if row.startswith('obj '):
                cols = row[4:].rsplit(' ', 2)
                if len(cols) == 3: file_record(ctx, pid, cols[0], ev, cols[1])
            elif row.startswith('dir '):
                # Directories establish ownership but are not packaged files.
                if row[4:].startswith('/'):
                    ctx.owned.setdefault(os.path.normpath(row[4:]), set()).add(pid)
            elif row.startswith('sym '):
                body, sep, stamp = row[4:].rpartition(' ')
                if not sep or not stamp.isdigit() or body.count(' -> ') != 1:
                    gap(ctx, 'Portage symlink manifest entry unsupported: ' + ev, True)
                    continue
                link_path, target = body.split(' -> ', 1)
                if not link_path.startswith('/'): continue
                file_record(ctx, pid, link_path, ev)
                record = ctx.package_files[-1]
                meta = ctx.entries.get(os.path.normpath(link_path))
                if meta and meta.get('type') != 'symlink':
                    record['integrity'] = 'changed'
                    record['rule'] = 'Installed symlink replaced with a different observed object type.'
                elif meta and isinstance(meta.get('target'), str) and not meta.get('target_error'):
                    record['integrity'] = 'unchanged' if meta['target'] == target else 'changed'
                    record['rule'] = 'Observed symlink target compared with Portage CONTENTS installation target.'



def applications(ctx, available):
    if 'flatpak' in available:
        scopes = [(None, '--system')] + [(u, '--user') for u in ctx.users]
        for user, scope in scopes:
            for typ, reason in [('app','explicit'), ('runtime','dependency')]:
                command = 'flatpak ' + scope + ' list --' + typ + ' --columns=ref,version,origin'
                if user:
                    # Read only the documented default scope; do not let list
                    # create directories for system accounts or missing homes.
                    command = ('scope="$HOME/.local/share/flatpak"; '
                               'test -d "$scope" || { printf "%s\\n" "Default user Flatpak scope does not exist or is inaccessible" >&2; exit 125; }; '
                               'FLATPAK_USER_DIR="$scope" ' + command)
                    command = ctx.as_user(user, command)
                label = 'packages-flatpak-' + scope[2:] + '-' + str(user.get('uid','') if user else '') + '-' + typ
                out, rc, ev = query(ctx, label, command)
                if rc: gap(ctx, 'Flatpak scope query failed: ' + ev, True); continue
                for row in out.splitlines():
                    cols = row.split('\t')
                    if not cols[0]: continue
                    package(ctx, 'flatpak', cols[0], reason, ev, scope=scope,
                            uid=user.get('uid') if user else None, reason_rule='Application/runtime distinction; not historical user intent.')
        gap(ctx, 'Flatpak deployment file ownership/integrity not collected.', True)
    if 'snap' in available:
        out, rc, ev = query(ctx, 'packages-snap', 'snap list --all')
        if rc: gap(ctx, 'Snap list failed: ' + ev, True)
        else:
            for row in out.splitlines()[1:]:
                cols = row.split()
                if len(cols) >= 3: package(ctx, 'snap', cols[0] + '@' + cols[2], 'unknown', ev, version=cols[1])
        gap(ctx, 'Snap reason and image verification unavailable; image contents not expanded.', True)


def language(ctx):
    paths = list(ctx.entries)
    npm_locations = set()
    for path in sorted(paths, key=lambda p: p.endswith('/node_modules/.package-lock.json')):
        try:
            if path.endswith('.dist-info/METADATA'):
                root = os.path.dirname(path); data, rc, ev = read(ctx, path)
                if rc: gap(ctx, 'Python metadata unavailable: ' + ev, True); continue
                fields = dict(re.findall(r'^(Name|Version): (.*)$', data, re.M))
                native = native_owners(ctx, path)
                requested = root + '/REQUESTED' in ctx.entries
                reason = 'explicit' if requested else 'unknown'
                pid = package(ctx, 'python', fields.get('Name', os.path.basename(root)) + '@' + root, reason, ev,
                              version=fields.get('Version',''), location=root, native_package_ids=native,
                              reason_source='python-requested' if requested else 'unknown',
                              ownership_rule='Only native manager manifest paths count as native ownership; no containment inference.',
                              reason_rule='Python REQUESTED is explicit; absence alone proves nothing. Native metadata ownership records provenance only and does not transfer the native package reason.')
                record, rr, revidence = read(ctx, root + '/RECORD')
                if rr:
                    if native and root + '/RECORD' not in ctx.entries:
                        # Native packaging may deliberately omit Python RECORD.
                        # File provenance remains exactly the native manifest;
                        # user additions are never assigned by containment.
                        continue
                    gap(ctx, 'Python RECORD unavailable: ' + revidence, True)
                    continue
                try:
                    for row in csv.reader(io.StringIO(record)):
                        if not row: continue
                        target = os.path.normpath(os.path.join(os.path.dirname(root), row[0]))
                        alg, digest = 'sha256', None
                        if len(row) > 1 and '=' in row[1]:
                            alg, b64 = row[1].split('=',1)
                            try: digest = base64.urlsafe_b64decode(b64 + '=' * (-len(b64) % 4)).hex()
                            except ValueError: digest = None
                            if alg not in hashlib.algorithms_available: digest = None; alg = 'sha256'
                        file_record(ctx, pid, target, revidence, digest, alg,
                                    int(row[2]) if len(row) > 2 and row[2].isdigit() else None)
                except csv.Error: gap(ctx, 'Malformed Python RECORD: ' + revidence, True)
            elif path.endswith('/node_modules/.package-lock.json') or (path.endswith('/package-lock.json') and '/node_modules/' not in path):
                data, rc, ev = read(ctx, path)
                if rc: gap(ctx, 'npm lock unavailable: ' + ev, True); continue
                try: lock = json.loads(data)
                except ValueError: gap(ctx, 'Malformed npm lock: ' + ev, True); continue
                root = os.path.dirname(path)
                hidden = os.path.basename(path).startswith('.')
                if hidden: root = os.path.dirname(root)
                packages = lock.get('packages', {})
                top = packages.get('', {})
                requested = set(top.get('dependencies',{})) | set(top.get('devDependencies',{})) | set(top.get('optionalDependencies',{}))
                for relative, meta in packages.items():
                    if not relative or meta.get('link'): continue
                    prefix = os.path.normpath(os.path.join(root, relative))
                    # Lock entries without installed directories are not installed packages.
                    if prefix not in ctx.entries and prefix + '/package.json' not in ctx.entries: continue
                    if prefix in npm_locations:
                        continue
                    name = meta.get('name') or relative.rsplit('node_modules/',1)[-1]
                    reason = 'explicit' if relative == 'node_modules/' + name and name in requested else 'unknown' if hidden or not top else 'dependency'
                    native = native_owners(ctx, prefix + '/package.json')
                    reason_source = ('npm-lock-top-level' if reason == 'explicit' else
                                     'npm-lock-transitive' if reason == 'dependency' else 'unknown')
                    pid = package(ctx, 'npm', name + '@' + prefix, reason, ev,
                                  version=meta.get('version',''), location=prefix,
                                  native_package_ids=native, reason_source=reason_source,
                                  reason_rule='Top-level lock request is explicit and an installed transitive lock entry is dependency. Native metadata ownership records provenance only and does not transfer the native package reason.')
                    npm_locations.add(prefix)
                if packages:
                    gap(ctx, 'npm lock records packages but not installed per-file provenance; ownership unresolved: ' + ev, True)
                if not packages: gap(ctx, 'npm legacy lock lacks installed package/file inventory: ' + ev, True)
            elif path.endswith('/.crates2.json'):
                data, rc, ev = read(ctx, path)
                if rc: gap(ctx, 'Cargo manifest unavailable: ' + ev, True); continue
                try: installs = json.loads(data).get('installs',{})
                except ValueError: gap(ctx, 'Malformed Cargo manifest: ' + ev, True); continue
                for name, meta in installs.items():
                    pid = package(ctx, 'cargo', name + '@' + os.path.dirname(path), 'explicit', ev,
                                  reason_source='cargo-install-registry', reason_rule='cargo install registry')
                    for binary in meta.get('bins',[]): file_record(ctx, pid, os.path.join(os.path.dirname(path),'bin',binary), ev)
            elif '/specifications/' in path and path.endswith('.gemspec'):
                package(ctx, 'gem', os.path.basename(path)[:-8], 'unknown', path,
                        reason_rule='Installed gemspec; executable gemspec is never evaluated.')
                gap(ctx, 'Ruby gem file manifest/reason unavailable without evaluating package code: ' + path, True)
        except (ValueError, TypeError, KeyError, AttributeError) as exc:
            gap(ctx, 'Language metadata parse failed: ' + path + ': ' + type(exc).__name__, True)
    # A lock can be absent or stale; discover actual installed package metadata too.
    # Neither containment nor package.json's publish-time files field proves which
    # installed files came from the package, so no ownership is assigned here.
    for path in paths:
        if re.search(r'/node_modules/(?:@[^/]+/)?[^/]+/package\.json$', path):
            location = os.path.dirname(path)
            if location in npm_locations:
                continue
            data, rc, ev = read(ctx, path)
            gap(ctx, 'npm installed package lacks a matching lock record/per-file provenance: ' + ev, True)
            if rc:
                continue
            try:
                meta = json.loads(data)
                if not isinstance(meta, dict):
                    continue
                name = meta.get('name', os.path.basename(location))
                native = native_owners(ctx, path)
                package(ctx, 'npm', str(name) + '@' + location, 'unknown', ev,
                        version=meta.get('version', ''), location=location,
                        native_package_ids=native, reason_source='unknown',
                        reason_rule='Unmatched npm metadata has unknown reason. Native metadata ownership records provenance only and does not transfer the native package reason.')
            except (ValueError, TypeError):
                continue
        elif path.endswith('.dist-info') and path + '/METADATA' not in ctx.entries:
            gap(ctx, 'Python distribution metadata missing or outside scan coverage: ' + path, True)
    # Detect manager formats not yet safely interpreted; never silently call them unowned.
    unsupported = [p for p in paths if p.endswith(('/conda-meta/history','/.crates.toml','/installed.packages')) or p.endswith(('.egg-info/PKG-INFO', '.egg-info', '.egg', '/composer/installed.json', '/composer/installed.php')) or ('/conda-meta/' in p and p.endswith('.json')) or ('/rocks-' in p and p.endswith('/manifest'))]
    for p in unsupported:
        if p.endswith('/.crates.toml') and os.path.dirname(p) + '/.crates2.json' in ctx.entries: continue
        if p.endswith('.egg-info') and p + '/PKG-INFO' in ctx.entries:
            continue  # The actual metadata file is handled independently.
        if p.endswith(('.egg-info/PKG-INFO', '.egg-info')) and native_owners(ctx, p):
            data, rc, ev = read(ctx, p)
            if rc == 0:
                fields = dict(re.findall(r'^(Name|Version): (.*)$', data, re.M))
                package(ctx, 'python', fields.get('Name', os.path.basename(p)) + '@' + p,
                        'unknown', ev, version=fields.get('Version', ''),
                        native_package_ids=native_owners(ctx, p),
                        reason_source='unknown',
                        ownership_rule='Native metadata ownership; file provenance remains native manifest only.',
                        reason_rule='No Python requested record; native package reason remains on the native object and is not transferred.')
                continue
        gap(ctx, 'Language package database not interpreted: ' + p, True)


def collect(ctx):
    ctx._package_digest_jobs = []
    ctx._native_package_ids = set()
    if hasattr(ctx, 'safe_reads'):
        metadata = [p for p in ctx.entries if (p.startswith('/var/lib/dpkg/info/') and p.endswith(('.list','.md5sums'))) or p.endswith(('.dist-info/METADATA','.dist-info/RECORD','/package-lock.json','/node_modules/.package-lock.json','/.crates2.json')) or (p.startswith('/var/db/pkg/') and p.endswith('/CONTENTS')) or re.search(r'/node_modules/(?:@[^/]+/)?[^/]+/package\.json$', p)]
        ctx._package_read_cache = ctx.safe_reads(metadata, limit=MAX_DB)
    # Homebrew's documented Linux prefix need not be in the caller's PATH.
    # Discover only: command -v never executes the manager or its package code.
    brew_bins = sorted({'/home/linuxbrew/.linuxbrew/bin'} | {
        os.path.dirname(path) for path in ctx.entries if path.endswith('/bin/brew')})
    available, rc, ev = query(ctx, 'package-manager-discovery',
        'PATH=' + shlex.quote(':'.join(brew_bins)) + ':"$PATH"; export PATH; '
        'for p in dpkg-query rpm pacman apk xbps-query emerge flatpak snap npm pip pip3 pipx poetry uv pnpm yarn bun gem cargo conda composer luarocks go brew; do command -v "$p" >/dev/null 2>&1 && printf "%s\\n" "$p"; done; :')
    if rc: gap(ctx, 'Package manager discovery failed: ' + ev, True)
    available = set(available.splitlines())
    user_managers = 'npm pip pip3 pipx poetry uv pnpm yarn bun gem cargo conda composer luarocks go brew'
    for user in ctx.users:
        if str(user.get('uid')) == '0' or os.path.basename(user.get('shell', '')) in ('nologin', 'false', ''):
            continue
        home = user.get('home', '')
        if not home.startswith('/'):
            continue
        candidates = [home + suffix for suffix in ('/.local/bin', '/.cargo/bin', '/.npm-global/bin',
                     '/.volta/bin', '/.bun/bin', '/.local/share/pnpm', '/.pyenv/shims',
                     '/.rbenv/shims', '/miniconda3/bin', '/anaconda3/bin', '/.linuxbrew/bin')]
        candidates += brew_bins
        candidates += [os.path.dirname(path) for path in ctx.entries
                       if path.startswith(home.rstrip('/') + '/') and path.endswith('/bin/npm')]
        prefix = ':'.join(dict.fromkeys(candidates))
        script = 'PATH=' + shlex.quote(prefix) + ':"$PATH"; export PATH; for p in ' + user_managers + '; do command -v "$p" >/dev/null 2>&1 && printf "%s\\n" "$p"; done; :'
        found, urc, uev = query(ctx, 'package-manager-discovery-user-' + str(user.get('uid')), ctx.as_user(user, script))
        if urc:
            gap(ctx, 'User package manager discovery failed: ' + uev, True)
        else:
            available.update(found.splitlines())
    native = [('dpkg-query', dpkg), ('rpm', rpm), ('pacman', pacman), ('apk', apk), ('xbps-query', xbps), ('emerge', portage)]
    found = False
    for command, adapter in native:
        if command in available:
            found = True
            try: adapter(ctx)
            except Exception as exc: gap(ctx, command + ' adapter failed: ' + type(exc).__name__ + ': ' + str(exc), True)
    if not found: gap(ctx, 'No supported native package database discovered; ownership complement unavailable.', True)
    applications(ctx, available)
    language(ctx)
    for manager in ('conda','composer','luarocks','go','pipx','poetry','uv','pnpm','yarn','bun','brew'):
        if manager in available: gap(ctx, manager + ' manager present but complete installed package manifest adapter unavailable.', True)

    verify(ctx)

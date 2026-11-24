#!/usr/bin/python3 -B
"""Independent native readback; collects evidence and never decides a hypothesis outcome."""
import argparse, base64, grp, hashlib, json, os, pathlib, pwd, stat, subprocess, sys
P = pathlib.Path
COMMANDS = []


def digest(data):
    return hashlib.sha256(data).hexdigest()


def command(*argv):
    try:
        p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True, timeout=90,
                           env={**os.environ, 'LC_ALL': 'C', 'SYSTEMD_COLORS': '0'})
        result = {'argv': list(argv), 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
    except (OSError, subprocess.TimeoutExpired) as e:
        result = {'argv': list(argv), 'error': type(e).__name__}
    COMMANDS.append(result)
    return result


def read(path):
    try:
        return P(path).read_text()
    except OSError as e:
        return {'error': type(e).__name__, 'errno': e.errno}


def file_value(path, full=False):
    try:
        s = os.lstat(path)
        result = {'path': str(path), 'mode': stat.S_IMODE(s.st_mode), 'uid': s.st_uid, 'gid': s.st_gid, 'size': s.st_size}
        result['xattrs'] = {k: base64.b64encode(os.getxattr(path, k, follow_symlinks=False)).decode()
                            for k in sorted(os.listxattr(path, follow_symlinks=False))}
        if stat.S_ISLNK(s.st_mode):
            result.update(kind='symlink', target=os.readlink(path))
        elif stat.S_ISREG(s.st_mode):
            with open(path, 'rb') as f:
                result.update(kind='file', sha256=hashlib.file_digest(f, 'sha256').hexdigest())
        elif stat.S_ISDIR(s.st_mode):
            result['kind'] = 'directory'
        else:
            result['kind'] = 'other'
        if full:
            result.update({k: getattr(s, k) for k in ('st_mode', 'st_uid', 'st_gid', 'st_size', 'st_atime', 'st_mtime', 'st_ctime', 'st_nlink')})
        return result
    except OSError as e:
        return {'path': str(path), 'error': type(e).__name__, 'errno': e.errno}


def account(name):
    try:
        p = pwd.getpwnam(name)
        gids = sorted(set(os.getgrouplist(name, p.pw_gid)))
        names = []
        for gid in gids:
            try:
                names.append(grp.getgrgid(gid).gr_name)
            except KeyError:
                names.append('UNRESOLVED_GID:' + str(gid))
        return {'name': p.pw_name, 'uid': p.pw_uid, 'gid': p.pw_gid,
                'groups': sorted(names), 'group_ids': gids, 'shell': p.pw_shell,
                'home': p.pw_dir, 'gecos': p.pw_gecos}
    except KeyError:
        return {'missing': True, 'name': name}


def package(identity):
    if identity['backend'] == 'dpkg':
        p = command('/usr/bin/dpkg-query', '-W', '-f=${Package}\t${Version}\t${Architecture}\t${db:Status-Status}\n', identity['name'])
        return {k: p.get(k) for k in ('exit', 'stdout', 'stderr', 'error') if k in p}
    try:
        ledger = json.loads(P('/var/lib/stand/objects.json').read_text())
        # This installer has no separate native package database. Return its actual
        # registration, never manufacture installation from the requested line.
        return [e for e in ledger if e.get('kind') == 'package' and e.get('identity', {}).get('name') == identity['name'] and e.get('identity', {}).get('backend') == identity['backend']]
    except (OSError, ValueError) as e:
        return {'error': type(e).__name__}


def kernel_policy():
    result = {}
    root = P('/sys/kernel/security/apparmor/policy/profiles')
    if not root.exists():
        return {'error': 'kernel policy export unavailable'}
    for namefile in sorted(root.rglob('name')):
        try:
            name = namefile.read_text().strip()
            raw = (namefile.parent / 'raw_data').read_bytes()
            result.setdefault(name, []).append({'mode': read(namefile.parent / 'mode'),
                                                'raw_sha256': digest(raw),
                                                'raw_base64': base64.b64encode(raw).decode()})
        except OSError as e:
            result.setdefault('errors', []).append(type(e).__name__)
    return result


def observe(row, directory, bundle_files):
    t = row['type']
    if t in ('program', 'base', 'code'):
        files = row.get('files', [])
        manifest = None
        if 'files_manifest' in row:
            name = row['files_manifest']
            text = bundle_files.get('/var/lib/stand/current/' + name)
            if text is None:
                text = (directory / name).read_text()
            manifest = {'name': name, 'sha256': digest(text.encode())}
            files = json.loads(text)
        out = {'files': [file_value(f['path']) for f in files]}
        if manifest:
            out['manifest'] = manifest
        if row.get('package_identity'):
            out['package_registration'] = package(row['package_identity'])
        if row.get('package_dependencies'):
            out['dependency_registrations'] = {d['name']: package(d) for d in row['package_dependencies']}
        return out
    if t == 'account':
        return account(row['name'])
    if t == 'group':
        try:
            g = grp.getgrnam(row['name'])
            return {'name': g.gr_name, 'gid': g.gr_gid, 'members': sorted(g.gr_mem)}
        except KeyError:
            return {'missing': True, 'name': row['name']}
    if t in ('service', 'timer', 'socket'):
        global_scope = row.get('scope') == 'user-global'
        enabled = command('/usr/bin/systemctl', *(['--global'] if global_scope else []), 'is-enabled', row['unit'])
        out = {'unit': row['unit'], 'enabled': enabled.get('stdout', '').strip(), 'enabled_exit': enabled.get('exit')}
        if global_scope:
            path = row['unit_path']
        else:
            q = command('/usr/bin/systemctl', 'show', row['unit'], '-p', 'FragmentPath', '-p', 'LoadState', '-p', 'ActiveState')
            props = dict(s.split('=', 1) for s in q.get('stdout', '').splitlines() if '=' in s)
            out['load_state'] = props.get('LoadState')
            path = props.get('FragmentPath', '')
            if 'active' in row:
                out['active'] = props.get('ActiveState') == 'active'
        out['unit_file'] = file_value(path) if path else {'missing': True}
        out['unit_text'] = read(path) if path else None
        # Effective manager text includes drop-ins; retain it even when none was stated.
        out['effective_unit'] = command('/usr/bin/systemctl', *(['--global'] if global_scope else []), 'cat', row['unit']).get('stdout') if not global_scope else read(path)
        return out
    if t in ('privilege', 'login-key'):
        return {'file': file_value(row['path']), 'text': read(row['path'])}
    if t == 'password-login':
        q = command('/usr/sbin/sshd', '-T')
        values = dict(s.split(None, 1) for s in q.get('stdout', '').splitlines() if ' ' in s)
        return {k: values.get(k) for k in ('passwordauthentication', 'kbdinteractiveauthentication')}
    if t == 'rule':
        backend = row.get('backend', 'nft')
        if backend == 'dac':
            return {'paths': [file_value(p['path']) for p in row['paths']]}
        if backend == 'mount':
            q = command('/usr/bin/findmnt', '-n', '-o', 'OPTIONS', '--target', row['path'])
            return {'path': row['path'], 'effective': ','.join(sorted(q.get('stdout', '').strip().split(','))), 'query_exit': q.get('exit')}
        if backend == 'code-boundary':
            return {'kernel_profiles': read('/sys/kernel/security/apparmor/profiles'),
                    'kernel_enabled': read('/sys/module/apparmor/parameters/enabled'),
                    'kernel_exported_policy': kernel_policy(),
                    'policy_sources': {str(p): read(p) for p in sorted(P('/etc/apparmor.d').glob('stand-*')) if p.is_file()},
                    'launch_table': read('/etc/stand/launch.tsv'),
                    'limitation': 'Kernel profile names/enforcement and exact policy inputs do not prove the semantic prose requirement.'}
        q = command('/usr/sbin/nft', 'list', 'table', 'inet', 'stand')
        j = command('/usr/sbin/nft', '-j', 'list', 'table', 'inet', 'stand')
        try:
            entities = json.loads(j['stdout']).get('nftables', [])
        except (KeyError, ValueError):
            entities = []
        if backend == 'nft-chain':
            actual = [e['chain'] for e in entities if 'chain' in e and e['chain'].get('name') == row['chain']['name']]
            return {'chain': [{k: v for k, v in e.items() if k not in ('handle', 'index')} for e in actual],
                    'effective_text': q.get('stdout'), 'query_exit': q.get('exit')}
        return {'effective': [s.strip() for s in q.get('stdout', '').splitlines() if 'comment "' + row['id'] + '"' in s],
                'rules': [{k: v for k, v in e['rule'].items() if k not in ('handle', 'index')}
                          for e in entities if 'rule' in e and e['rule'].get('comment') == row['id']], 'query_exit': q.get('exit')}
    if t == 'port':
        q = command('/usr/bin/ss', '-H', '-ln' + ('t' if row['protocol'] == 'tcp' else 'u'))
        addresses = sorted({s.split()[3] for s in q.get('stdout', '').splitlines() if len(s.split()) >= 4})
        return {'protocol': row['protocol'], 'port': row['port'], 'local': row['local'], 'listening': row['local'] in addresses, 'all_addresses': addresses}
    if t == 'setting':
        if 'path' in row:
            data = P(row['path']).read_bytes()
            return {'path': row['path'], 'value': base64.b64encode(data).decode(), 'sha256': digest(data)}
        return {'name': row['name'], 'value': command('/usr/sbin/sysctl', '-n', row['name']).get('stdout', '').strip()}
    if t == 'boot':
        return {'guest_cmdline': read('/proc/cmdline'), 'limitation': 'Boot order and fixed firmware must also be checked in committed host VM argv; guest observations do not prove them.'}
    if t == 'wifi':
        return {'profile': read('/etc/NetworkManager/system-connections/stand-' + row['id'] + '.nmconnection'),
                'manager': command('/usr/bin/nmcli', '-g', 'all', 'connection', 'show', row['uuid'])}
    if t == 'bluetooth':
        return {'profile': read('/var/lib/bluetooth/' + row['adapter'] + '/' + row['address'] + '/info'),
                'manager': command('/usr/bin/bluetoothctl', 'info', row['address'])}
    return {'UNQUERIED_TYPE': t}


def leaves(value, prefix=''):
    if isinstance(value, dict):
        return [x for k in sorted(value) for x in leaves(value[k], prefix + '/' + k)] or [(prefix, {})]
    if isinstance(value, list):
        return [x for i, v in enumerate(value) for x in leaves(v, prefix + '/' + str(i))] or [(prefix, [])]
    return [(prefix, value)]


def snapshot(args):
    bundle = json.loads(P(args.bundle).read_text()) if args.bundle else None
    files = bundle['files'] if bundle else {}
    directory = P(args.declaration)
    source = files.get('/var/lib/stand/current/machine.jsonl')
    if source is None:
        source = (directory / 'machine.jsonl').read_text()
    rows = [json.loads(s) for s in source.splitlines() if s.strip()]
    current = read('/var/lib/stand/current/machine.jsonl')
    result = {'format': 'bc4-native-readback-v1', 'requested_machine_sha256': digest(source.encode()),
              'current_machine_sha256': digest(current.encode()) if isinstance(current, str) else current,
              'current_machine_byte_identical': current == source,
              'rows': {}, 'filesystems': {}, 'primary_files': {}, 'declaration_values': dict(leaves(bundle or {'machine': rows}))}
    for name, expected in sorted(files.items()):
        actual = read(name)
        result['primary_files'][name] = {'required_sha256': digest(expected.encode()),
                                         'actual_sha256': digest(actual.encode()) if isinstance(actual, str) else actual,
                                         'byte_identical': actual == expected, 'actual_text': actual}
    for row in rows:
        try:
            value = observe(row, directory, files)
        except Exception as e:
            value = {'QUERY_ERROR': type(e).__name__, 'message': str(e)}
        result['rows'][row['id']] = {'required': row, 'observed': value}
    designation_text = files.get('/etc/stand/bc3-primary.json') or read('/etc/stand/bc3-primary.json')
    if isinstance(designation_text, str):
        designation = json.loads(designation_text)
        for key, mount in designation['filesystem_mounts'].items():
            name = '/var/lib/stand-fs/' + key + '/current/declaration.json'
            actual_before = P(name).read_bytes()
            declared = json.loads(files.get(name, actual_before))
            observed = {}
            aliases = {}
            for path, ino in sorted(declared['paths'].items()):
                fullpath = mount + path
                required = declared['objects'][ino]
                actual = file_value(fullpath, full=True)
                observed[path] = {'required': required, 'actual': actual,
                                  'declared_field_differences': {k: {'required': v, 'actual': actual.get(k, {'UNQUERIED_FIELD': k})}
                                                                 for k, v in required.items() if actual.get(k) != v}}
                try:
                    s = os.lstat(fullpath)
                    aliases.setdefault((s.st_dev, s.st_ino), []).append(path)
                except OSError:
                    pass
            accounts = {}
            for row in declared.get('account_rows', []):
                try:
                    value = observe(row, directory, files)
                except Exception as e:
                    value = {'QUERY_ERROR': type(e).__name__, 'message': str(e)}
                accounts[row['id']] = {'required': row, 'observed': value}
            result['filesystems'][key] = {'requested': declared, 'live_declaration_sha256': digest(actual_before),
                                          'selected_declaration_byte_identical': not files or files.get(name, '').encode() == actual_before,
                                          'selected_declaration_text': actual_before.decode(),
                                          'success_report': read(P(name).parent / 'success.json'),
                                          'paths': observed, 'account_rows': accounts,
                                          'hardlink_groups': sorted(sorted(v) for v in aliases.values() if len(v) > 1),
                                          'stable_during_readback': actual_before == P(name).read_bytes()}
    result['evidence'] = {'commands': COMMANDS, 'last_success': read('/var/lib/stand/last-success.json'),
                          'objects_ledger': read('/var/lib/stand/objects.json')}
    return result


def processes(executable):
    result = []
    for proc in sorted(P('/proc').glob('[0-9]*'), key=lambda p: int(p.name)):
        if int(proc.name) == os.getpid():
            continue
        try:
            exe = os.readlink(proc / 'exe')
            cmdline = (proc / 'cmdline').read_bytes().split(b'\0')
            maps = (proc / 'maps').read_text()
            if exe.removesuffix(' (deleted)') == executable or os.fsencode(executable) in cmdline or executable in maps:
                fields = (proc / 'stat').read_text().rsplit(') ', 1)[1].split()
                result.append({'pid': int(proc.name), 'starttime': fields[19], 'state': fields[0], 'exe': exe,
                               'argv': [s.decode(errors='replace') for s in cmdline if s], 'maps': maps})
        except (FileNotFoundError, ProcessLookupError):
            continue
        except OSError as e:
            result.append({'pid': int(proc.name), 'scan_error': type(e).__name__})
    return {'executable': executable, 'file': file_value(executable), 'holders': result}


def diff(a, b, path=''):
    if type(a) is not type(b):
        return [{'path': path, 'left': a, 'right': b}]
    if isinstance(a, dict):
        return [x for k in sorted(set(a) | set(b)) for x in
                ([{'path': path + '/' + k, 'left': a.get(k), 'right': b.get(k)}] if k not in a or k not in b else diff(a[k], b[k], path + '/' + k))]
    if isinstance(a, list):
        return [] if a == b else [{'path': path, 'left': a, 'right': b}]
    return [] if a == b else [{'path': path, 'left': a, 'right': b}]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='operation', required=True)
    p = sub.add_parser('snapshot'); p.add_argument('--declaration', default='/var/lib/stand/current'); p.add_argument('--bundle')
    p = sub.add_parser('processes'); p.add_argument('executable')
    p = sub.add_parser('package'); p.add_argument('name'); p.add_argument('--backend', default='stand', choices=['stand', 'dpkg'])
    p = sub.add_parser('diff'); p.add_argument('left'); p.add_argument('right')
    args = parser.parse_args()
    if args.operation == 'snapshot':
        result = snapshot(args)
    elif args.operation == 'processes':
        result = processes(args.executable)
    elif args.operation == 'package':
        result = package({'backend': args.backend, 'name': args.name})
    else:
        left = json.loads(P(args.left).read_text()); right = json.loads(P(args.right).read_text())
        # Compare every field, including required values, raw commands and runtime
        # diagnostics. Never silently drop a difference or label it hardware-related.
        result = {'all_differences': diff(left, right), 'hypothesis_outcome': 'not decided'}
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()

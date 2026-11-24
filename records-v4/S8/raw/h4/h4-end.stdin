#!/usr/bin/python3 -B
"""Read-only step-8 observations. Run as typed Python stdin, never install it.

No hypothesis verdict is computed. collect() is also used while the NIC is down.
"""
import base64
import collections
import datetime
import grp
import hashlib
import importlib.util
import json
import os
import pathlib
import pwd
import stat
import subprocess
import sys
import traceback

sys.dont_write_bytecode = True
P = pathlib.Path
MOUNTS = {'home': '/home/stand', 'tmp': '/tmp', 'vartmp': '/var/tmp',
          'shm': '/dev/shm', 'etc': '/etc'}
PRIMARY = ['/var/lib/stand/current/machine.jsonl',
           '/var/lib/stand/current/base-files.json', '/etc/stand/bc3-primary.json'] + [
    '/var/lib/stand-fs/' + k + '/current/declaration.json' for k in MOUNTS]


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    try:
        return P(path).read_text()
    except (OSError, UnicodeError) as e:
        return {'error': type(e).__name__, 'errno': getattr(e, 'errno', None)}


def query(argv, timeout=45):
    result = {'argv': argv, 'started_utc': utc()}
    try:
        p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=timeout, env={**os.environ, 'LC_ALL': 'C',
                           'SYSTEMD_COLORS': '0', 'SYSTEMD_PAGER': 'cat'})
        result.update(exit=p.returncode, stdout=p.stdout.decode(errors='replace'),
                      stderr=p.stderr.decode(errors='replace'))
    except subprocess.TimeoutExpired as e:
        result.update(error='TimeoutExpired', stdout=(e.stdout or b'').decode(errors='replace'),
                      stderr=(e.stderr or b'').decode(errors='replace'))
    except OSError as e:
        result.update(error=type(e).__name__, errno=e.errno)
    result['ended_utc'] = utc()
    return result


def identity():
    result = {'utc': utc(), 'boot_id': read('/proc/sys/kernel/random/boot_id'),
              'files': {}, 'reports': {}, 'pointers': {}}
    for name in PRIMARY:
        text = read(name)
        result['files'][name] = {'text': text,
                                 'sha256': digest(text.encode()) if isinstance(text, str) else None}
    for name in ['/var/lib/stand/last-success.json', '/var/lib/stand/complete-last-success.json',
                 '/var/lib/stand/pending.json', '/run/stand-ready'] + [
            '/var/lib/stand-fs/' + k + '/current/success.json' for k in MOUNTS]:
        result['reports'][name] = read(name)
    for name in ['/var/lib/stand/current'] + ['/var/lib/stand-fs/' + k + '/current' for k in MOUNTS]:
        try:
            result['pointers'][name] = str(P(name).resolve(strict=True))
        except OSError as e:
            result['pointers'][name] = {'error': type(e).__name__}
    return result


def file_state(path):
    """No paths are obtained from the declaration during the census."""
    try:
        st = os.lstat(path)
        out = {k: getattr(st, k) for k in ('st_mode', 'st_uid', 'st_gid', 'st_size',
                                          'st_atime', 'st_mtime', 'st_ctime', 'st_nlink', 'st_ino', 'st_dev')}
        out.update(path=str(path), mode=stat.S_IMODE(st.st_mode), uid=st.st_uid, gid=st.st_gid)
        try:
            out['xattrs'] = {k: base64.b64encode(os.getxattr(path, k, follow_symlinks=False)).decode()
                            for k in sorted(os.listxattr(path, follow_symlinks=False))}
        except OSError as e:
            out['xattrs'] = {'QUERY_ERROR': type(e).__name__, 'errno': e.errno}
        if stat.S_ISREG(st.st_mode):
            out['kind'] = 'file'
            with open(path, 'rb') as stream:
                head = stream.read(128)
                stream.seek(0)
                out['sha256'] = hashlib.file_digest(stream, 'sha256').hexdigest()
            out['head_base64'] = base64.b64encode(head).decode()
            end = os.lstat(path)
            out['stable_while_reading'] = (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns) == (
                end.st_dev, end.st_ino, end.st_size, end.st_mtime_ns, end.st_ctime_ns)
        elif stat.S_ISLNK(st.st_mode):
            out.update(kind='symlink', target=os.readlink(path))
        elif stat.S_ISDIR(st.st_mode):
            out['kind'] = 'directory'
        else:
            out['kind'] = 'special'
        return out
    except OSError as e:
        return {'path': str(path), 'QUERY_ERROR': type(e).__name__, 'errno': e.errno}


def independent_census():
    out = {'started_utc': utc(), 'files': {}, 'scan_errors': [], 'queries': [],
           'accounts': [], 'groups': [], 'processes': [], 'installer_records': {}}
    def error(e):
        out['scan_errors'].append({'path': e.filename, 'error': type(e).__name__, 'errno': e.errno})
    # Walk all persistent/runtime filesystems in the root namespace, excluding
    # only kernel pseudo files. /dev/shm is included separately. No declaration use.
    for top in ('/', '/dev/shm'):
        for root, dirs, names in os.walk(top, followlinks=False, onerror=error):
            dirs[:] = sorted(d for d in dirs if os.path.join(root, d) not in ('/proc', '/sys', '/dev'))
            out['files'][root] = file_state(root)
            for name in sorted(names + [d for d in dirs if os.path.islink(os.path.join(root, d))]):
                path = os.path.join(root, name)
                out['files'][path] = file_state(path)
    for account in pwd.getpwall():
        row = dict(zip(('name', 'password', 'uid', 'gid', 'gecos', 'home', 'shell'), account))
        try:
            row['group_ids'] = sorted(set(os.getgrouplist(account.pw_name, account.pw_gid)))
            row['groups'] = [grp.getgrgid(g).gr_name for g in row['group_ids']]
        except (OSError, KeyError) as e:
            row['group_error'] = type(e).__name__
        out['accounts'].append(row)
    out['groups'] = [{'name': g.gr_name, 'gid': g.gr_gid, 'members': sorted(g.gr_mem)} for g in grp.getgrall()]
    commands = [
        ['/usr/bin/dpkg-query', '-W', '-f=${binary:Package}\t${Version}\t${Architecture}\t${db:Status-Status}\n'],
        ['/usr/bin/systemctl', 'list-unit-files', '--all', '--no-pager', '--no-legend', '--plain'],
        ['/usr/bin/systemctl', 'list-units', '--all', '--no-pager', '--no-legend', '--plain'],
        ['/usr/bin/systemctl', '--global', 'list-unit-files', '--all', '--no-pager', '--no-legend', '--plain'],
        ['/usr/bin/systemctl', 'list-timers', '--all', '--no-pager'],
        ['/usr/sbin/sysctl', '-a'], ['/usr/sbin/nft', '-j', 'list', 'ruleset'],
        ['/usr/sbin/ip', '-j', '-details', 'address', 'show'],
        ['/usr/sbin/ip', '-j', 'route', 'show', 'table', 'all'],
        ['/usr/sbin/ip', '-j', '-6', 'route', 'show', 'table', 'all'],
        ['/usr/sbin/ip', '-j', 'rule', 'show'], ['/usr/sbin/ip', '-j', '-6', 'rule', 'show'],
        ['/usr/bin/findmnt', '--json', '-o', 'TARGET,SOURCE,FSTYPE,OPTIONS'],
        ['/usr/bin/lsblk', '--json', '-O'], ['/usr/bin/ss', '-H', '-lntup'],
        ['/usr/bin/nmcli', '-g', 'all', 'connection', 'show'],
        ['/usr/bin/nmcli', '-g', 'all', 'device', 'show'],
        ['/usr/bin/bluetoothctl', 'show'], ['/usr/bin/bluetoothctl', 'devices'],
        ['/usr/bin/busctl', '--system', '--auto-start=no', '--allow-interactive-authorization=no',
         'call', 'org.freedesktop.timedate1', '/org/freedesktop/timedate1',
         'org.freedesktop.DBus.Properties', 'GetAll', 's', 'org.freedesktop.timedate1'],
        ['/usr/bin/busctl', '--system', '--auto-start=no', '--allow-interactive-authorization=no',
         'call', 'org.freedesktop.locale1', '/org/freedesktop/locale1',
         'org.freedesktop.DBus.Properties', 'GetAll', 's', 'org.freedesktop.locale1'],
        ['/usr/bin/loginctl', 'list-users', '--no-legend', '--no-pager'],
        ['/usr/sbin/sshd', '-T'],
        ['/usr/bin/systemctl', 'show', 'stand-replay.service', '-p', 'ActiveState', '-p', 'Result'],
    ]
    out['queries'] = [query(c) for c in commands]
    units = out['queries'][1]
    if units.get('exit') == 0:
        for line in units['stdout'].splitlines():
            fields = line.split()
            if len(fields) >= 2 and fields[1] in ('enabled', 'enabled-runtime', 'linked', 'linked-runtime', 'alias'):
                out['queries'].append(query(['/usr/bin/systemctl', 'show', fields[0]]))
                out['queries'].append(query(['/usr/bin/systemctl', 'cat', fields[0], '--no-pager']))
    for account in out['accounts']:
        out['queries'].append(query(['/usr/bin/sudo', '-n', '-ll', '-U', account['name']]))
        out['queries'].append(query(['/usr/sbin/sshd', '-T', '-C',
            'user='+account['name']+',addr=127.0.0.1,host=localhost,laddr=127.0.0.1,lport=22']))
        if P('/run/user', str(account['uid']), 'bus').exists():
            out['queries'].append(query(['/usr/sbin/runuser', '-u', account['name'], '--',
                '/usr/bin/env', 'XDG_RUNTIME_DIR=/run/user/'+str(account['uid']),
                '/usr/bin/systemctl', '--user', 'list-unit-files', '--all', '--no-pager', '--no-legend']))
    # Keep installer receipt bytes; membership alone never establishes unchanged receipt.
    for p in sorted(P('/var/lib/dpkg/info').glob('*')):
        if p.suffix in ('.list', '.md5sums', '.conffiles'):
            out['installer_records'][str(p)] = read(p)
    out['installer_records']['/var/lib/stand/objects.json'] = read('/var/lib/stand/objects.json')
    for proc in sorted(P('/proc').glob('[0-9]*')):
        try:
            row = {'pid': int(proc.name), 'exe': os.readlink(proc/'exe'),
                   'cmdline_base64': base64.b64encode((proc/'cmdline').read_bytes()).decode(),
                   'stat': read(proc/'stat'), 'maps': read(proc/'maps'), 'status': read(proc/'status'),
                   'mountinfo': read(proc/'mountinfo'), 'descriptors': {}}
            for fd in (proc/'fd').iterdir():
                try:
                    row['descriptors'][fd.name] = os.readlink(fd)
                except OSError as e:
                    row['descriptors'][fd.name] = {'error': type(e).__name__}
            out['processes'].append(row)
        except OSError as e:
            out['processes'].append({'pid': int(proc.name), 'QUERY_ERROR': type(e).__name__, 'errno': e.errno})
    out['kernel'] = {p: read(p) for p in ('/proc/cmdline', '/proc/self/mountinfo',
        '/sys/kernel/security/apparmor/profiles', '/sys/module/apparmor/parameters/enabled')}
    out['time_language_configuration'] = {p: {'text': read(p), 'file': file_state(p)}
        for p in ('/etc/timezone', '/etc/locale.conf', '/etc/default/locale',
                  '/etc/vconsole.conf', '/etc/adjtime')}
    out['time_language_configuration']['/etc/localtime'] = file_state('/etc/localtime')
    out['ended_utc'] = utc()
    return out


_PARTIAL = {}


def _collect():
    global _PARTIAL
    _PARTIAL = {'format': 'step8-partial-observation-v1', 'started_utc': utc()}
    before = identity()  # Identity only; never provides census paths or queries.
    _PARTIAL['identity_before'] = before
    census = independent_census()
    _PARTIAL['independent_census'] = census
    selected = identity()
    files = {p: v['text'] for p, v in selected['files'].items()}
    authority = {'machine': {}, 'filesystems': {}}
    # The last success report, not the current symlink by itself, selects the
    # machine declaration. A failed application can leave different pointers.
    try:
        receipt = json.loads(selected['reports']['/var/lib/stand/last-success.json'])
        if receipt.get('status') != 'SUCCESS':
            raise ValueError('not a successful application report')
        name = receipt['declaration']
        if not isinstance(name, str) or P(name).name != name:
            raise ValueError('unsafe generation name')
        directory = P('/var/lib/stand/generations') / name
        authority['machine'] = {'receipt': receipt, 'directory': str(directory),
            'selected_pointer_matches': selected['pointers']['/var/lib/stand/current'] == str(directory)}
        for basename in ('machine.jsonl', 'base-files.json'):
            files['/var/lib/stand/current/'+basename] = (directory/basename).read_text()
        machine_rows = [json.loads(s) for s in files[PRIMARY[0]].splitlines() if s.strip()]
        names = sorted({'machine.jsonl'} | {r['files_manifest'] for r in machine_rows if 'files_manifest' in r})
        if any(P(n).name != n for n in names):
            raise ValueError('unsafe manifest name')
        content = {n: (directory/n).read_bytes() for n in names}
        for n, data in content.items():
            files['/var/lib/stand/current/'+n] = data.decode()
        authority['machine']['content_identity_matches_receipt'] = digest(b''.join(n.encode()+b'\0'+content[n] for n in names)) == name
    except (OSError, ValueError, KeyError, TypeError) as e:
        authority['machine'] = {'FACT_UNKNOWN': type(e).__name__,
            'reason': 'Last successful machine declaration could not be resolved; current texts are diagnostic only.'}
    for key in MOUNTS:
        prefix = '/var/lib/stand-fs/'+key+'/current/'
        try:
            receipt = json.loads(selected['reports'][prefix+'success.json'])
            valid = receipt.get('status') == 'success' and receipt.get('declaration_sha256') == digest(files[prefix+'declaration.json'].encode())
            authority['filesystems'][key] = {'receipt': receipt, 'hash_matches': valid,
                'authority': 'shared atomic selected generation' if valid else 'FACT_UNKNOWN'}
        except (ValueError, TypeError, KeyError) as e:
            authority['filesystems'][key] = {'FACT_UNKNOWN': type(e).__name__}
    required = {'format': 'bc3-complete-declaration-v1', 'files': files}
    result = {'format': 'step8-observation-v1', 'started_utc': before['utc'],
              'identity_before': before, 'identity_at_comparison': selected,
              'independent_census': census, 'complete_declaration': required,
              'declaration_authority': authority,
              'p1_file_relations': {}, 'p1_package_relations': [], 'p2_rows': {},
              'p2_filesystems': {}, 'collection_errors': [], 'outcome': 'not assigned'}
    _PARTIAL = result
    path = '/usr/local/lib/stand/bc4-compare.py'
    spec = importlib.util.spec_from_file_location('step8_native_queries', path)
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    result['native_query_source_sha256'] = digest(P(path).read_bytes())
    claims = collections.defaultdict(list)
    rows = [json.loads(line) for line in files[PRIMARY[0]].splitlines() if line.strip()]
    for row in rows:
        try:
            actual = native.observe(row, P('/var/lib/stand/current'), files)
        except Exception as e:
            actual = {'QUERY_ERROR': type(e).__name__, 'message': str(e)}
        result['p2_rows'][row['id']] = {'required': row, 'observed': actual,
                                      'review_all_fields': list(row)}
        members = row.get('files', [])
        if 'files_manifest' in row:
            members = json.loads(files['/var/lib/stand/current/' + row['files_manifest']])
        if row['type'] in ('privilege', 'login-key'):
            members = [{'path': row['path'], 'kind': 'file', 'mode': row['mode'],
                        'uid': row['uid'], 'gid': row['gid'], 'sha256': digest(row['text'].encode())}]
        if row['type'] == 'rule' and row.get('backend') == 'dac':
            members = row['paths']
        for want in members:
            claims[want['path']].append({'line': row['id'], 'relation': 'own', 'required': want})
    for key, mount in MOUNTS.items():
        text = files['/var/lib/stand-fs/'+key+'/current/declaration.json']
        decl = json.loads(text)
        paths = {}
        for path, ino in sorted(decl['paths'].items()):
            full = str(P(mount) / path.lstrip('/'))
            want = decl['objects'][ino]
            actual = file_state(full)
            paths[path] = {'inode': ino, 'required': want, 'observed': actual,
                          'differences': {k: {'required': v, 'observed': actual.get(k, {'UNQUERIED': k})}
                                          for k, v in want.items() if actual.get(k) != v}}
            claims[full].append({'line': key+':/objects/'+ino, 'path_line': key+':/paths/'+path,
                                'relation': 'own', 'required': want})
        accounts = {}
        for row in decl.get('account_rows', []):
            try:
                actual = native.observe(row, P('/var/lib/stand/current'), files)
            except Exception as e:
                actual = {'QUERY_ERROR': type(e).__name__, 'message': str(e)}
            accounts[row['id']] = {'required': row, 'observed': actual, 'review_all_fields': list(row)}
        linked = set(decl['paths'].values())
        result['p2_filesystems'][key] = {'required': decl, 'paths': paths, 'account_rows': accounts,
            'unreachable_objects': {ino: obj for ino, obj in decl['objects'].items() if ino not in linked},
            'structural_fields': {k: v for k, v in decl.items() if k not in ('objects', 'paths', 'account_rows')}}
    for path, actual in census['files'].items():
        comparisons = []
        for claim in claims.get(path, []):
            want = claim['required']
            mismatches = {k: {'required': v, 'observed': actual.get(k, {'UNQUERIED': k})}
                          for k, v in want.items() if k not in ('content_b64',) and actual.get(k) != v}
            comparisons.append({'line': claim['line'], 'relation': claim['relation'],
                                'state_matches': not mismatches, 'differences': mismatches})
        result['p1_file_relations'][path] = {'own_line_comparisons': comparisons,
            'mandatory_classification': 'FACT_UNKNOWN unless ordered facts are established by the record',
            'package_or_derivation_relation': 'review receipts and action evidence; never infer from pathname'}
    package_query = census['queries'][0]
    if package_query.get('exit') == 0:
        for line in package_query['stdout'].splitlines():
            parts = line.split('\t')
            if len(parts) != 4 or parts[3] != 'installed':
                continue
            name, version, architecture, status = parts
            matching = [r['id'] for r in rows if r.get('package_identity', {}).get('backend') == 'dpkg'
                and r['package_identity'].get('name') in (name, name.split(':')[0])
                and r['package_identity'].get('version') == version
                and r['package_identity'].get('architecture') == architecture]
            result['p1_package_relations'].append({'actual': parts, 'own_lines': matching,
                'classification': 'installed package: S8.2-7/S8.2-8',
                'other_covering_relation': 'not inferred; inspect dependency/derivation receipts'})
    result['native_queries'] = native.COMMANDS
    after = identity()
    result['identity_after'] = after
    result['declaration_stable'] = before['files'] == selected['files'] == after['files']
    result['success_reports_stable'] = before['reports'] == selected['reports'] == after['reports']
    result['ended_utc'] = utc()
    result['limits'] = [
        'Root namespace files only; arbitrary semantic settings, encrypted data and other mount namespaces are not exhaustive.',
        'No automatic code-executability, unchanged-package-receipt or arbitrary derivation inference.',
        'Anonymous executable memory, all login contexts, firmware and universal policy prose are not proved.',
        'A live census is not atomic. Changed generations/files, denied queries and vanished processes remain unavailable.',
        'All literal required values need review. Source/version metadata require committed provenance; equality of text alone does not prove realization.',
        'Runtime processes/ports/mounts belong to their creators under S8.2-5; they are not automatically separate installed objects.',
    ]
    return result


def collect():
    try:
        return _collect()
    except Exception:
        _PARTIAL['collection_error'] = traceback.format_exc()
        _PARTIAL['ended_utc'] = utc()
        _PARTIAL['outcome'] = 'not assigned; collection incomplete'
        return _PARTIAL


if __name__ == '__main__':
    print(json.dumps(collect(), sort_keys=True, separators=(',', ':')))

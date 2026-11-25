#!/usr/bin/python3
"""Assemble an empty root from package payloads and person-written lines."""
import hashlib
import fcntl
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tarfile
import time
from archive_sources import sources

HERE = Path(__file__).resolve().parent
EPOCH = 1795392000
os.environ['LC_ALL'] = 'C'
os.umask(0o022)

def run(*args, **kw):
    env = dict(os.environ)
    if str(args[0]) == 'mksquashfs':
        env.pop('SOURCE_DATE_EPOCH', None)
    elif str(args[0]) == 'grub-mkstandalone':
        env['SOURCE_DATE_EPOCH'] = str(EPOCH)
    kw.setdefault('env', env)
    if str(args[0]) == 'guestfish':
        slots = Path.home()/'VMs/confos/slots'
        slots.mkdir(parents=True, exist_ok=True)
        attempt = 0
        while True:
            for number in range(1, 7):
                lock = open(slots/f'slot-{number}.lock', 'w')
                try:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    lock.close()
                    continue
                try:
                    return subprocess.run([str(a) for a in args], check=True, **kw)
                finally:
                    lock.close()
            if attempt % 6 == 0:
                print('Waiting for a shared disk-appliance slot', flush=True)
            attempt += 1
            time.sleep(5)
    return subprocess.run([str(a) for a in args], check=True, **kw)

def put(root, path, data, mode=0o644):
    p = root / path.lstrip('/')
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.is_symlink() or p.is_file():
        p.unlink()
    p.write_text(data)
    p.chmod(mode)

def compatibility_links(root):
    # libc6-i386's shipped postinst specifies these exact usr-merge links.
    # Materialize them deterministically without running maintainer scripts.
    if (root/'usr/lib32/ld-linux.so.2').is_file():
        for name, target in (('lib32', 'usr/lib32'), ('usr/lib/ld-linux.so.2', '../lib32/ld-linux.so.2')):
            path = root/name
            if not path.is_symlink():
                path.symlink_to(target)

def declared_hostname(rows):
    values = [r[2] for r in rows if r[:2] in (
        ['setting', 'hostname'], ['setting', 'sysctl:kernel.hostname'])]
    for value in values:
        if not re.fullmatch('[A-Za-z0-9][A-Za-z0-9.-]{0,63}', value):
            raise ValueError('hostname requires 1..64 ASCII letters, digits, dots or hyphens, starting with a letter or digit')
    if len(set(values)) > 1:
        raise ValueError('hostname and sysctl:kernel.hostname conflict')
    return values[0] if values else 'confos'

def validate_groups(rows):
    """`group NAME GID`: a group of its own, usable as a supplementary group by later account lines."""
    names = {'root', '_apt', 'wheel', 'nogroup'} | {row[1] for row in rows if row[0] == 'account'}
    gids = {0, 10, 42, 65534} | {int(row[3]) for row in rows if row[0] == 'account' and row[3].isdigit()}
    for row in rows:
        if row[0] != 'group':
            continue
        _, name, gid = row
        if not re.fullmatch('[a-z_][a-z0-9_-]*', name) or name in names:
            raise ValueError('invalid, duplicate or reserved account/group name: '+name)
        if not re.fullmatch('[0-9]+', gid) or not 1 <= int(gid) <= 4294967294 or int(gid) in gids:
            raise ValueError('group GID must be an unused integer in 1..4294967294: '+gid)
        names.add(name)
        gids.add(int(gid))

def declared_modules(rows):
    """`setting module:NAME loaded`: a kernel module of the pinned kernel loaded at every start."""
    modules = []
    for row in rows:
        if row[0] == 'setting' and row[1].startswith('module:'):
            if not re.fullmatch('[a-z0-9][a-z0-9_-]*', row[1][7:]) or row[2] != 'loaded':
                raise ValueError('module setting needs the form: setting module:NAME loaded')
            modules.append(row[1][7:].replace('-', '_'))
    if len(modules) != len(set(modules)):
        raise ValueError('duplicate module setting')
    return sorted(modules)

def validate_accounts(rows):
    validate_groups(rows)
    names = {'root', '_apt', 'wheel', 'nogroup'}
    uids = {0, 42}
    for row in rows:
        if row[0] != 'account':
            continue
        _, name, uid, gid, supplementary, shell, home = row
        if not re.fullmatch('[a-z_][a-z0-9_-]*', name) or name in names:
            raise ValueError('invalid, duplicate or reserved account/group name: '+name)
        if any(not re.fullmatch('[0-9]+', value) or int(value) > 4294967294 for value in (uid, gid)):
            raise ValueError('account UID/GID require ASCII integers in 0..4294967294')
        if int(uid) in uids:
            raise ValueError('duplicate or reserved account UID: '+uid)
        if any(':' in value or any(ord(c) < 32 for c in value) for value in (shell, home)):
            raise ValueError('account shell/home cannot contain passwd field separators or controls')
        if not shell.startswith('/') or '..' in Path(shell).parts:
            raise ValueError('account shell must be an absolute path without ..')
        if Path(home).parent != Path('/home') or '..' in Path(home).parts:
            raise ValueError('account home must be an immediate child of /home')
        names.add(name)
        uids.add(int(uid))

def parse(path):
    rows = []
    seen = set()
    arities = {'base': 2, 'snapshot': 2, 'radio-fixture': 4, 'network': 4, 'bluetooth-pair': 5, 'package': 3, 'account': 7,
               'authorized-key': 4, 'file': None, 'pip': 5, 'npm': 5, 'flatpak': 5, 'appimage': 5,
               'container': 6, 'user-unit': 6, 'linuxgsm': 6, 'setting': 3, 'rule': 3, 'service': None, 'compile': None,
               'group': 3}
    for n, line in enumerate(path.read_text().splitlines(), 1):
        row = shlex.split(line, comments=True)
        if not row:
            continue
        if row[0] not in arities or (arities[row[0]] is not None and len(row) != arities[row[0]]):
            raise ValueError(f'line {n}: unsupported kind or wrong field count')
        if row[0] == 'service' and (len(row) < 4 or row[2] not in ('enabled', 'disabled')):
            raise ValueError(f'line {n}: service needs name, state and absolute executable with arguments')
        if row[0] == 'compile' and len(row) < 5:
            raise ValueError(f'line {n}: compile needs path, mode, source SHA256, source and optional gcc flags')
        if row[0] == 'file':
            if len(row) not in (5, 6):
                raise ValueError(f'line {n}: file needs path, mode, optional UID:GID, checksum and source')
            if len(row) == 6:
                owner = row[3]
                if not re.fullmatch('[0-9]+:[0-9]+', owner) or any(int(value) > 4294967294 for value in owner.split(':')):
                    raise ValueError(f'line {n}: file owner needs valid numeric UID:GID')
                # Keep checksum/source indices stable for input freezing and disk copying.
                row = row[:3]+row[4:]+[owner]
        if row[0] == 'package' and (not re.fullmatch('[a-z0-9][a-z0-9+.-]*(?::(?:amd64|all))?', row[1])
                                     or not re.fullmatch('[0-9][A-Za-z0-9.+:~_-]*', row[2])):
            raise ValueError(f'line {n}: invalid Debian package name or version')
        identity = tuple(row[:2]) if row[0] not in ('base', 'snapshot') else (row[0],)
        if row[0] in ('compile', 'appimage'):
            identity = ('file', row[1])
        if row[0] == 'flatpak':
            if not re.fullmatch(r'(?:app|runtime)/[A-Za-z0-9_.-]+/x86_64/[A-Za-z0-9_.-]+', row[1]):
                raise ValueError('flatpak requires a complete app/runtime x86_64 ref')
            identity = ('flatpak', row[1].split('/')[1])
        if row[0] in ('container', 'user-unit', 'linuxgsm', 'bluetooth-pair'):
            identity = tuple(row[:3])
        if identity in seen:
            raise ValueError(f'line {n}: duplicate identity')
        seen.add(identity)
        rows.append(row)
    version = (HERE/'VERSION').read_text().strip()
    if ['base', version] not in rows:
        raise ValueError('base '+version+' is required by this source release')
    snapshots = [r[1] for r in rows if r[0] == 'snapshot']
    if len(snapshots) != 1 or not re.fullmatch(r'\d{8}T\d{6}Z', snapshots[0]):
        raise ValueError('one snapshot timestamp is required')
    declared_hostname(rows)
    validate_accounts(rows)
    return rows, snapshots[0]

def base_package(name='confos-runtime', snapshot=None):
    version = (HERE/'VERSION').read_text().strip()
    architecture = {'confos-runtime': 'all', 'confos-boot': 'amd64', 'confos-initramfs': 'amd64',
                    'confos-code-readers': 'amd64'}[name]
    if name == 'confos-initramfs':
        if snapshot not in ('20260801T000000Z', '20261001T000000Z', '20261123T000000Z'):
            raise ValueError('initramfs package requires a supported snapshot')
        version += '+'+snapshot
    directory = Path('/system/base-packages') if HERE == Path('/usr/lib/confos') else HERE/'packages'
    archive = directory/(name+'_'+version+'_'+architecture+'.deb')
    if not archive.exists() and HERE != Path('/usr/lib/confos'):
        directory.mkdir(parents=True, exist_ok=True)
        with (directory/'.build.lock').open('w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if not archive.exists():
                if name == 'confos-runtime':
                    run(sys.executable, HERE/'package-base.py', archive)
                elif name == 'confos-boot':
                    run(sys.executable, HERE/'package-boot.py', 'build', version, archive)
                elif name == 'confos-code-readers':
                    run('bash', HERE/'build-busybox-vi-component.sh', version)
                else:
                    run(sys.executable, HERE/'package-initramfs.py', version.split('+')[0], snapshot, archive)
    expected = archive.with_suffix('.deb.sha256').read_text().strip()
    if hashlib.sha256(archive.read_bytes()).hexdigest() != expected:
        raise ValueError(name+' package checksum mismatch')
    control = subprocess.check_output(['dpkg-deb', '-f', str(archive)], text=True)
    fields = dict(line.split(': ', 1) for line in control.splitlines() if ': ' in line and not line.startswith(' '))
    if fields.get('Package') != name or fields.get('Version') != version or fields.get('Architecture') != architecture:
        raise ValueError(name+' package release/architecture mismatch')
    return archive

def packages(work, rows, snapshot):
    apt = work / 'apt'
    for sub in ('lists/partial', 'archives/partial', 'etc', 'log'):
        (apt / sub).mkdir(parents=True, exist_ok=True)
    (apt / 'status').write_text('')
    (apt / 'etc/sources.list').write_text(sources(snapshot))
    opts = ['-o', f'Dir::State::status={apt}/status', '-o', f'Dir::State::lists={apt}/lists',
            '-o', f'Dir::Cache::archives={apt}/archives', '-o', f'Dir::Etc::sourcelist={apt}/etc/sources.list',
            '-o', 'Dir::Etc::sourceparts=-', '-o', 'APT::Install-Recommends=false',
            '-o', 'APT::Install-Suggests=false', '-o', 'APT::Sandbox::User=root',
            '-o', 'Acquire::Check-Valid-Until=false', '-o', 'Acquire::Retries=3',
            '-o', 'Acquire::http::Timeout=30', '-o', f'Dir::Log={apt}/log',
            '-o', 'Dir::Cache::pkgcache=', '-o', 'Dir::Cache::srcpkgcache=',
            '-o', 'Acquire::Languages=none', '-o', 'Dir::Etc::parts=-', '-o', 'Dir::Etc::main=-']
    lock = HERE/'components'/(snapshot+'.txt')
    if not lock.is_file():
        raise ValueError('no base component lock for snapshot '+snapshot)
    requested = dict(line.split('=', 1) for line in lock.read_text().split())
    for row in rows:
        if row[0] == 'package':
            if row[1] in requested and requested[row[1]] != row[2]:
                raise ValueError('package release conflicts with the base snapshot: '+row[1])
            requested[row[1]] = row[2]
    version = (HERE/'VERSION').read_text().strip()
    for name in ('confos-boot', 'confos-runtime', 'confos-initramfs', 'confos-code-readers'):
        expected = version+'+'+snapshot if name == 'confos-initramfs' else version
        if requested.pop(name, None) != expected:
            raise ValueError('component lock must name this '+name+' release')
    apt_command = '/usr/bin/apt-get' if HERE == Path('/usr/lib/confos') else 'apt-get'
    run(apt_command, *opts, 'update')
    arguments = [name+'='+release for name, release in sorted(requested.items())]
    solver = []
    try:
        resolution = subprocess.check_output([apt_command, *opts, '--simulate', 'install', *arguments], text=True)
    except subprocess.CalledProcessError as error:
        print('Native default dependency resolution failed (exit '+str(error.returncode)+'); retrying all available dependency versions', flush=True)
        solver = ['--solver', '3.0', '--no-strict-pinning']
        resolution = subprocess.check_output([apt_command, *opts, *solver, '--simulate', 'install', *arguments], text=True)
    resolved = {(name.split(':')[0], release) for name, release in re.findall(r'^Inst (\S+) \((\S+) ', resolution, re.M)}
    if not resolved:
        raise ValueError('empty native package resolution')
    required = set(requested.items())
    if not required <= resolved or any(name in requested and requested[name] != release for name, release in resolved):
        raise ValueError('native dependency resolution changed an explicit package request')
    run(apt_command, *opts, *solver, '--yes', '--download-only', 'install',
        *arguments)
    selected = {}
    for archive in sorted((apt/'archives').glob('*.deb')):
        if archive.name.startswith(('confos-runtime_', 'confos-boot_', 'confos-initramfs_', 'confos-code-readers_')):
            continue
        control = subprocess.check_output(['dpkg-deb', '-f', str(archive)], text=True)
        fields = dict(line.split(': ', 1) for line in control.splitlines() if ': ' in line and not line.startswith(' '))
        identity = (fields.get('Package'), fields.get('Version'))
        if identity in resolved:
            if identity in selected and hashlib.sha256(selected[identity].read_bytes()).digest() != hashlib.sha256(archive.read_bytes()).digest():
                raise ValueError('conflicting cached archive bytes for '+str(identity))
            selected[identity] = archive
    if set(selected) != resolved:
        raise ValueError('resolved package archives absent: '+str(sorted(resolved-set(selected))))
    own = []
    for name in ('confos-boot', 'confos-runtime', 'confos-initramfs', 'confos-code-readers'):
        archive = base_package(name, snapshot)
        target = apt/'archives'/archive.name
        shutil.copyfile(archive, target)
        own.append(target)
    return sorted(selected.values())+own

def payload(root, debs):
    controls = []
    ownership = {}
    for deb in debs:
        run('dpkg-deb', '-x', deb, root)
        process = subprocess.Popen(['dpkg-deb', '--fsys-tarfile', str(deb)], stdout=subprocess.PIPE)
        links = []
        with tarfile.open(fileobj=process.stdout, mode='r|') as archive:
            for member in archive:
                name = member.name.removeprefix('./').rstrip('/')
                if not name:
                    continue
                if member.islnk():
                    links.append((name, member.linkname.removeprefix('./')))
                    continue
                checksum = hashlib.file_digest(archive.extractfile(member), 'sha256').hexdigest() if member.isfile() else None
                kind = 'file' if member.isfile() else 'dir' if member.isdir() else 'link' if member.issym() else 'other'
                ownership[name] = (member.uid, member.gid, member.mode, kind, checksum, member.linkname)
        if process.wait():
            raise RuntimeError('package metadata extraction failed')
        for name, target in links:
            ownership[name] = ownership[target]
        control = subprocess.check_output(['dpkg-deb', '-f', str(deb)], text=True)
        controls.append(control.rstrip() + '\nStatus: install ok installed\n')
    put(root, '/var/lib/dpkg/status', '\n'.join(controls))
    return ownership

def squashfs_ownership(root, ownership, target, game_entries=(), file_owners=None):
    """Preserve archive owners of unchanged payloads without host chown privileges."""
    lines = []
    for path in sorted(root.rglob('*')):
        name = path.relative_to(root).as_posix()
        metadata = path.lstat()
        mode = stat.S_IMODE(metadata.st_mode)
        uid = gid = 0
        original = ownership.get(name)
        if original and original[:2] != (0, 0) and mode == original[2]:
            kind = 'link' if path.is_symlink() else 'file' if path.is_file() else 'dir' if path.is_dir() else 'other'
            same = kind == original[3]
            if same and kind == 'file':
                with path.open('rb') as stream:
                    same = hashlib.file_digest(stream, 'sha256').hexdigest() == original[4]
            elif same and kind == 'link':
                same = os.readlink(path) == original[5]
            if same:
                uid, gid = original[:2]
        for game in game_entries:
            prefix = game['path'].lstrip('/')
            if name == prefix or name.startswith(prefix+'/'):
                uid, gid = game['uid'], game['gid']
        uid, gid = (file_owners or {}).get('/'+name, (uid, gid))
        if any(ord(c) < 32 for c in name):
            raise ValueError('unsupported control character in image pathname')
        escaped = ''.join('\\'+c if c in '\\ \"' else c for c in name)
        lines.append(f'{escaped} m {mode:04o} {uid} {gid}\n')
    target.write_text(''.join(lines))

def configure(root, rows, declaration, digest):
    for d in ('proc', 'sys', 'dev', 'run', 'tmp', 'var', 'home', 'state', 'system', 'root', 'etc/ssh'):
        (root/d).mkdir(parents=True, exist_ok=True)
    for name, target in [('bin', 'usr/bin'), ('sbin', 'usr/sbin'), ('lib', 'usr/lib'), ('lib64', 'usr/lib64')]:
        p = root / name
        if not p.exists():
            p.symlink_to(target)
    compatibility_links(root)
    import recording
    recording.configure(root)
    # Debian package payloads do not include all alternatives or installation-generated files.
    for name in ('sh', 'mount', 'umount', 'mkdir', 'cat', 'sleep', 'sync', 'reboot', 'poweroff',
                 'ip', 'hostname', 'ps', 'ls', 'chmod', 'chown', 'cp', 'mv', 'rm', 'vi', 'grep',
                 'sed', 'head', 'tail', 'sha256sum', 'find', 'xargs', 'sort', 'wc', 'dd', 'touch',
                 'readlink', 'stat', 'true', 'false', 'dmesg', 'tar', 'wget', 'awk', 'which'):
        p = root / 'usr/bin' / name
        if not p.exists():
            p.symlink_to('/usr/bin/busybox')
    passwd = ['root:x:0:0:root:/root:/bin/bash', '_apt:x:42:65534:apt:/nonexistent:/usr/sbin/nologin']
    groups = {'root': (0, []), 'wheel': (10, []), 'nogroup': (65534, [])}
    accounts = {'root', '_apt'}
    validate_groups(rows)
    # A `group` line may stand anywhere in the text, also after an account that names it.
    for r in rows:
        if r[0] == 'group':
            groups[r[1]] = (int(r[2]), [])
    for r in rows:
        if r[0] == 'account':
            _, name, uid, gid, supplementary, shell, home = r
            if not re.fullmatch(r'[a-z_][a-z0-9_-]*', name) or name in accounts:
                raise ValueError('invalid or duplicate account')
            if not uid.isdigit() or not gid.isdigit() or int(uid) == 0:
                raise ValueError('invalid numeric account identity')
            if Path(home).parent != Path('/home') or '..' in Path(home).parts:
                raise ValueError('account home must be an immediate child of /home')
            passwd.append(f'{name}:x:{uid}:{gid}:{name}:{home}:{shell}')
            accounts.add(name)
            groups[name] = (int(gid), [])
            for group in supplementary.split(','):
                if group != '-':
                    if group not in groups:
                        raise ValueError('unknown supplementary group '+group)
                    groups[group][1].append(name)
    put(root, '/etc/passwd', '\n'.join(passwd)+'\n')
    # Locked passwords; public-key login only.
    put(root, '/etc/shadow', '\n'.join(f'{name}:*:19000:0:99999:7:::' for name in sorted(accounts))+'\n', 0o600)
    put(root, '/etc/group', '\n'.join(f'{n}:x:{g}:{",".join(m)}' for n,(g,m) in sorted(groups.items()))+'\n')
    # Fixed native defaults are received from the genuine confos-runtime package.
    put(root, '/etc/confos/declaration.conf', declaration.read_text())
    put(root, '/etc/confos/identity', digest+'\n')
    keys = {}
    services = {}
    rules = {}
    sysctls = {}
    hostname = declared_hostname(rows)
    put(root, '/etc/hostname', hostname+'\n')
    put(root, '/etc/hosts', '127.0.0.1 localhost '+hostname+'\n')
    for r in rows:
        if r[0] == 'authorized-key':
            _, user, kind, key = r
            if user not in accounts:
                raise ValueError('key for undeclared account')
            keys[user] = f'{kind} {key}\n'
        elif r[0] == 'setting':
            _, name, value = r
            if name == 'hostname':
                pass  # Validated with its sysctl alias before assembly.
            elif name == 'timezone' and value in ('UTC', 'Etc/UTC'):
                put(root, '/etc/timezone', value+'\n')
            elif name.startswith('sysctl:') and re.fullmatch('[A-Za-z0-9_.]+', name[7:]) and '\n' not in value:
                sysctls[name[7:]] = value
            elif name.startswith('module:'):
                pass  # Validated and written as one list below.
            else:
                raise ValueError('unsupported setting '+name)
        elif r[0] == 'service':
            _, name, state, *argv = r
            if not re.fullmatch('[A-Za-z0-9_-]+', name) or not argv[0].startswith('/'):
                raise ValueError('invalid service name or executable')
            services[name] = {'state': state, 'argv': argv}
            put(root, '/etc/confos/units/'+name+'.json', json.dumps(services[name], sort_keys=True)+'\n')
        elif r[0] == 'rule':
            _, name, value = r
            if not re.fullmatch('[A-Za-z0-9_-]+', name) or not value.startswith('add rule inet confos input '):
                raise ValueError('rules must add one named rule to inet confos input')
            if any(c in value for c in '\n;{}') or 'include' in shlex.split(value):
                raise ValueError('rule text must be one statement without includes')
            rules[name] = value
        elif r[0] == 'file':
            _, path, mode, checksum, source = r[:5]
            owner = tuple(map(int, r[5].split(':'))) if len(r) == 6 else (0, 0)
            if Path(source).is_absolute() or '..' in Path(source).parts:
                raise ValueError('file sources must be relative paths below the declaration directory')
            if not path.startswith('/') or '..' in Path(path).parts or path.startswith(('/state/', '/proc/', '/sys/', '/dev/')):
                raise ValueError('invalid immutable file path')
            sudo_rule = path.startswith('/etc/sudoers.d/')
            if not path.startswith(('/home/', '/usr/local/', '/etc/confos/user/')) and not sudo_rule:
                raise ValueError('file targets must be in /home, /usr/local, /etc/confos/user or /etc/sudoers.d')
            if sudo_rule and (not re.fullmatch('/etc/sudoers.d/[A-Za-z0-9_-]+', path) or int(mode, 8) != 0o440):
                raise ValueError('sudo rule needs an immediate filename without dots and mode 0440')
            if sudo_rule and owner != (0, 0):
                raise ValueError('sudo rule owner must be 0:0')
            if path.startswith('/home/') and len(Path(path).parts) < 4:
                raise ValueError('a home file must be below an account home directory')
            data = (declaration.parent/source).read_bytes()
            if hashlib.sha256(data).hexdigest() != checksum:
                raise ValueError('file checksum mismatch')
            if sudo_rule and re.search(rb'(?m)^\s*[@#]include', data):
                raise ValueError('sudo rule may not include additional configuration files')
            dest = root / path.lstrip('/')
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.parent.resolve().is_relative_to(root.resolve()):
                raise ValueError('file parent escapes the assembled root')
            if dest.is_symlink() or dest.is_file():
                dest.unlink()
            dest.write_bytes(data)
            dest.chmod(int(mode, 8))
    put(root, '/etc/confos/keys.json', json.dumps(keys, sort_keys=True)+'\n')
    certroot = root/'usr/share/ca-certificates'
    certificates = sorted(certroot.rglob('*.crt'))
    put(root, '/etc/ca-certificates.conf', ''.join(str(p.relative_to(certroot))+'\n' for p in certificates))
    certificates += sorted((root/'usr/local/share/ca-certificates').rglob('*.crt'))
    put(root, '/etc/ssl/certs/ca-certificates.crt', ''.join(p.read_text().rstrip()+'\n' for p in certificates))
    # libreoffice-common ships this exact default behind a dangling conffile link;
    # its postinst would copy it with ucf. No script or registration is needed.
    lo_default = root/'usr/lib/libreoffice/share/.registry/main.xcd'
    if lo_default.is_file():
        put(root, '/etc/libreoffice/registry/main.xcd', lo_default.read_text())
    put(root, '/etc/confos/services.json', json.dumps(services, sort_keys=True)+'\n')
    put(root, '/etc/confos/sysctls.json', json.dumps(sysctls, sort_keys=True)+'\n')
    modules = declared_modules(rows)
    if modules:
        # Every declared module is a file of the pinned kernel package; nothing is built.
        present = {path.name.split('.ko')[0].replace('-', '_') for path in (root/'usr/lib/modules').rglob('*.ko*')}
        missing = [name for name in modules if name not in present]
        if missing:
            raise ValueError('module is not a loadable module of the pinned kernel: '+', '.join(missing))
        put(root, '/etc/confos/modules.json', json.dumps(modules)+'\n')
    ruletext = 'flush ruleset\nadd table inet confos\nadd chain inet confos input { type filter hook input priority 0; policy accept; }\n'
    ruletext += ''.join(value+'\n' for name, value in sorted(rules.items()))
    put(root, '/etc/confos/rules.nft', ruletext)
    for name, key in keys.items():
        put(root, '/etc/confos/authorized-keys/'+name, key)
        if name == 'root':
            put(root, '/root/.ssh/authorized_keys', key, 0o600)
    managed = {r[1] for r in rows if r[0] in ('file', 'compile', 'appimage') and r[1].startswith('/home/')}
    import games
    games.configure(root, rows)
    managed.update(game['path']+'/wetserver' for game in games.entries(rows))
    for entry in passwd:
        name, _, _, _, _, home, _ = entry.split(':')
        if not home.startswith('/home/'):
            continue
        # Automatic shell/SSH startup is immutable even when its default is empty.
        for relative in ('.bashrc', '.profile', '.bash_profile', '.bash_login',
                         '.bash_logout', '.inputrc', '.gitconfig', '.ssh/rc'):
            path = home+'/'+relative
            if path not in managed:
                put(root, path, '')
            managed.add(path)
        if name in keys:
            path = home+'/.ssh/authorized_keys'
            put(root, path, keys[name])
            managed.add(path)
    mounts = sorted({'/'+ '/'.join(Path(path).parts[1:4]) for path in managed})
    put(root, '/etc/confos/home-mounts.json', json.dumps(mounts)+'\n')
    put(root, '/etc/confos/flatpaks.json', json.dumps({r[1].split('/')[1]: r[1] for r in rows if r[0] == 'flatpak'}, sort_keys=True)+'\n')
    (root/'usr/lib/confos/flatpak-user').mkdir(parents=True, exist_ok=True)
    import containers
    containers.configure(root, rows, declaration)
    import user_units
    user_units.configure(root, rows, declaration)
    # Query/run entries are original confos-runtime files, linked in /usr/local/bin.
    # Native package executables remain at their original paths with original bytes.
    for command in ('flatpak', 'podman', 'pip', 'pip3', 'npm', 'npx'):
        if (root/'usr/bin'/command).exists() or (root/'usr/bin'/command).is_symlink():
            entry = root/'usr/local/bin'/command
            if not entry.exists() and not entry.is_symlink():
                entry.symlink_to('/usr/lib/confos/commands/'+command)

def execution_policy(root):
    policy = '''profile confos-session flags=(attach_disconnected,mediate_deleted) {
  capability chown,
  capability fowner,
  capability fsetid,
  capability setgid,
  capability setuid,
  capability setpcap,
  capability net_bind_service,
  capability audit_write,
  capability dac_read_search,
  capability sys_ptrace,
  network,
  signal (send, receive) peer=confos-session,
  signal (send, receive) peer=confos-flatpak,
  signal (receive) peer=unconfined,
  ptrace (read, readby) peer=confos-session,
  ptrace (read, readby) peer=unconfined,
  # Reading only (which file a process executes, /proc/PID/exe), towards every label:
  # the kernel still requires the same account or the superuser's capability.
  ptrace (read),
  / r,
  /** r,
  /usr/** mr,
  /lib/** mr,
  /lib64/** mr,
  /opt/** mr,
  /home/** rwkl,
  /state/** rwkl,
  /tmp/** rwkl,
  /var/** rwkl,
  deny /var/lib/dpkg{,/**} wkl,
  deny /var/lib/apt{,/**} wkl,
  deny /var/spool/cron{,/**} wkl,
  deny /run/host/var/lib/dpkg{,/**} wkl,
  deny /run/host/var/lib/apt{,/**} wkl,
  deny /run/host/var/spool/cron{,/**} wkl,
  deny /proc/*/root/var/lib/dpkg{,/**} wkl,
  deny /proc/*/root/var/lib/apt{,/**} wkl,
  deny /proc/*/root/var/spool/cron{,/**} wkl,
  /run/** rwkl,
  deny /state/staging{,/**} wkl,
  deny /run/confos-installer-root{,/**} rwklmx,
  deny /usr/sbin/nft x,
  deny /usr/bin/flatpak x,
  deny /usr/bin/podman x,
  deny /usr/bin/systemctl x,
  deny /usr/bin/{hostnamectl,timedatectl} x,
  deny /usr/sbin/{sysctl,useradd,usermod,userdel,groupadd,groupdel} x,
  deny /usr/bin/apt{,-get} x,
  deny /usr/bin/pip{,3} rmx,
  deny /usr/lib/python3/dist-packages/pip/_internal/** rmx,
  deny /usr/lib/python3/dist-packages/pip/_vendor/** rmx,
  deny /usr/lib/python3.*/venv/** rmx,
  deny /usr/share/python-wheels/pip-* r,
  deny /usr/share/nodejs/npm/** rmx,
  deny /usr/lib/systemd/systemd x,
  deny /run/systemd/private rw,
  deny /run/user/*/systemd/private rw,
  deny /run/user/*/systemd{,/**} wklmx,
  deny /run/confos-containers{,/**} wklmx,
  deny /run/confos-container-ro{,/**} wklmx,
  deny /run/user/*/confos-podman*{,/**} wklmx,
  /usr/lib/confos/flatpak/** ix,
  /dev/null rw,
  /dev/zero rw,
  /dev/tty rw,
  /dev/ptmx rw,
  /dev/pts/** rw,
  /dev/random rw,
  /dev/urandom rw,
  /dev/shm/** rwkl,
'''
    executables = set()
    game_prefixes = [entry['path']+'/' for entry in json.loads((root/'etc/confos/games.json').read_text())]
    for prefix in game_prefixes:
        policy += '  "'+prefix+'**" mrix,\n'
    for entry in root.rglob('*'):
        if entry.is_symlink() or (entry.is_file() and entry.stat().st_mode & 0o111):
            path = '/'+str(entry.relative_to(root))
            if path.startswith('/usr/lib/confos/flatpak/') or any(path.startswith(prefix) for prefix in game_prefixes):
                continue  # One immutable subtree rule avoids an oversized DFA.
            if '"' in path or '\n' in path:
                raise ValueError('unsupported executable pathname')
            executables.add(path)
    for path in sorted(executables):
        escaped = ''.join('\\'+c if c in '\\[]{}*?^' else c for c in path)
        policy += '  "'+escaped+'" '+('Ux' if path in ('/usr/bin/confos', '/usr/lib/confos/systemctl-query') or path.startswith('/usr/lib/confos/commands/') else 'ix')+',\n'
    policy += (HERE/'radio-control-denials.apparmor').read_text()+'\n'
    import flatpak_profile
    import flatpak_readers
    policy += flatpak_readers.policy(root)
    put(root, '/etc/confos/session.apparmor', policy+'}\n'+flatpak_profile.render(root, executables)+'\n'+(HERE/'radio-trusted-profile.apparmor').read_text())

def root_image(declaration, work, keep_archives=True):
    rows, snapshot = parse(declaration)
    digest = hashlib.sha256(declaration.read_bytes()).hexdigest()
    root = work/'root'
    if root.exists():
        shutil.rmtree(root)
    root.mkdir()
    debs = packages(work, rows, snapshot)
    ownership = payload(root, debs)
    if not keep_archives:
        # An application on the machine needs the downloaded archives only until they are unpacked.
        for deb in debs:
            deb.unlink()
    import optional_readers
    package_names = {line[9:] for line in (root/'var/lib/dpkg/status').read_text().splitlines()
                     if line.startswith('Package: ')}
    optional_readers.apply(root, package_names)
    configure(root, rows, declaration, digest)
    import radio_integration, radio_systemd
    radio_integration.install(root, rows, declaration)
    radio_systemd.configure(root)
    import installers
    installers.run_in_root(root, '/usr/sbin/visudo', '-c')
    installers.install(root, rows, declaration)
    import games
    games.install(root, rows, declaration)
    execution_policy(root)
    # Module indexes are native bytes received from the pinned initramfs package.
    packaged_kernel(root)
    file_owners = {r[1]: tuple(map(int, r[5].split(':'))) if len(r) == 6 else (0, 0)
                   for r in rows if r[0] == 'file'}
    squashfs_ownership(root, ownership, work/'ownership.pseudo', games.entries(rows), file_owners)
    run('mksquashfs', root, work/'root.sqfs', '-noappend', '-root-uid', '0', '-root-gid', '0',
        '-pf', work/'ownership.pseudo', '-processors', '2',
        '-mkfs-time', str(EPOCH), '-all-time', str(EPOCH), '-no-progress')
    return digest, root

def packaged_kernel(root):
    release = (root/'usr/lib/confos/initramfs/kernel-release').read_text().strip()
    releases = sorted(path.name for path in (root/'usr/lib/modules').iterdir())
    if releases != [release] or not (root/'boot'/('vmlinuz-'+release)).is_file():
        raise ValueError('kernel payload differs from pinned initramfs release')
    return release

def initramfs(root, target):
    release = packaged_kernel(root)
    shutil.copyfile(root/'usr/lib/confos/initramfs/initramfs', target/'initramfs')
    (target/'initramfs').chmod(0o644)
    return release

def boot_config(digest):
    if not re.fullmatch('[0-9a-f]{64}', digest):
        raise ValueError('invalid generation identity')
    base = '/generations/'+digest
    return (f'linux {base}/vmlinuz console=ttyS0 quiet security=apparmor apparmor=1 confos.generation={digest}\n'
            f'initrd {base}/initramfs\nboot\n')

def disk(declaration, output):
    if output.exists():
        raise ValueError('output already exists')
    work = output.parent/(output.stem+'.work')
    work.mkdir(exist_ok=True)
    for name in ('initroot', 'system', 'efi', 'data'):
        if (work/name).exists():
            shutil.rmtree(work/name)
    digest, root = root_image(declaration, work)
    release = initramfs(root, work)
    system = work/'system'
    package_directory = system/'base-packages'
    package_directory.mkdir(parents=True)
    archives = [base_package(name) for name in ('confos-boot', 'confos-runtime', 'confos-code-readers')]
    archives += [base_package('confos-initramfs', stamp) for stamp in
                 ('20260801T000000Z', '20261001T000000Z', '20261123T000000Z')]
    for archive in archives:
        for source in (archive, archive.with_suffix('.deb.sha256')):
            target = package_directory/source.name
            shutil.copyfile(source, target)
            target.chmod(0o644)
    gen = system/'generations'/digest
    gen.mkdir(parents=True)
    shutil.copy2(work/'root.sqfs', gen/'root.sqfs')
    shutil.copyfile(declaration, gen/'declaration.conf')
    (gen/'declaration.conf').chmod(0o644)
    (system/'boot.cfg').write_text(boot_config(digest))
    shutil.copy2(root/'boot'/('vmlinuz-'+release), gen/'vmlinuz')
    shutil.copy2(work/'initramfs', gen/'initramfs')
    efi = work/'efi/EFI/BOOT'
    efi.mkdir(parents=True)
    shutil.copyfile(root/'usr/lib/confos/boot/BOOTX64.EFI', efi/'BOOTX64.EFI')
    (efi/'BOOTX64.EFI').chmod(0o644)
    data = work/'data'
    data.mkdir()
    shutil.copyfile(declaration, data/'declaration.conf')
    (data/'declaration.conf').chmod(0o644)
    rows, _ = parse(declaration)
    for row in rows:
        if row[0] in ('radio-fixture', 'network', 'bluetooth-pair'):
            import radio_declaration
            data_bytes = radio_declaration.read_input(declaration.parent, row[-2], row[-1])
            dest = data/row[-1]
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data_bytes)
            dest.chmod(0o600)
        if row[0] in ('file', 'pip', 'npm', 'compile', 'flatpak', 'appimage'):
            dest = data/row[4]
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(declaration.parent/row[4], dest)
            dest.chmod(0o644)
        if row[0] in ('container', 'user-unit', 'linuxgsm'):
            dest = data/row[5]
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(declaration.parent/row[5], dest)
            dest.chmod(0o644)
    for label, tree in [('efi', work/'efi'), ('system', system), ('data', data)]:
        run('tar', '--sort=name', '--mtime=@'+str(EPOCH), '--owner=0', '--group=0',
            '-cf', work/(label+'.tar'), '-C', tree, '.')
    # 6 GiB for the system partition (two generations during an application); the rest is the
    # data partition, which holds the inputs, the staging of an application and material.
    run('qemu-img', 'create', '-f', 'qcow2', output, '20G')
    commands = '\n'.join([
        'run', 'part-init /dev/sda gpt', 'part-add /dev/sda p 2048 264191',
        'part-add /dev/sda p 264192 12847103', 'part-add /dev/sda p 12847104 -34',
        'part-set-gpt-type /dev/sda 1 c12a7328-f81f-11d2-ba4b-00a0c93ec93b',
        'mkfs vfat /dev/sda1', 'mkfs ext4 /dev/sda2', 'set-label /dev/sda2 CONFOS-SYSTEM',
        'mkfs ext4 /dev/sda3', 'set-label /dev/sda3 CONFOS-DATA',
        'mount /dev/sda1 /', f'tar-in {work}/efi.tar /', 'umount-all',
        'mount /dev/sda2 /', f'tar-in {work}/system.tar /', 'umount-all',
        'mount /dev/sda3 /', f'tar-in {work}/data.tar /', 'umount-all', 'sync', ''])
    run('guestfish', '--rw', '-a', output, input=commands, text=True)
    print('BUILT', output.name, digest, flush=True)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: assemble.py DECLARATION OUTPUT.qcow2')
    disk(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())

"""Person-authored native user units with immutable search paths."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

def configure(root, rows, declaration):
    from assemble import put
    from installers import source_bytes
    accounts = {r[1]: r for r in rows if r[0] == 'account'}
    managers = {}
    for row in rows:
        if row[0] != 'user-unit':
            continue
        _, user, name, state, digest, source = row
        if user not in accounts or int(accounts[user][2]) == 0:
            raise ValueError('user-unit requires a declared ordinary account')
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*\.(service|timer)', name):
            raise ValueError('user-unit name must end in .service or .timer')
        if state not in ('enabled', 'disabled'):
            raise ValueError('user-unit state must be enabled or disabled')
        data = source_bytes(declaration, source, digest).decode('utf-8')
        directory = '/etc/confos/user-units/'+user+'/systemd/user'
        put(root, directory+'/'+name, data)
        extra = '[Install]\nWantedBy=default.target\n'
        if name.endswith('.service'):
            extra += '[Service]\nAppArmorProfile=confos-session\n'
        put(root, directory+'/'+name+'.d/99-confos.conf', extra)
        if state == 'enabled':
            link = root/(directory.lstrip('/')+'/default.target.wants')/name
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(directory+'/'+name)
        managers.setdefault(user, {})[name] = state
    put(root, '/etc/confos/user-units.json', json.dumps(managers, sort_keys=True)+'\n')
    if not managers:
        return
    for path in ('usr/lib/systemd/systemd', 'usr/bin/systemctl', 'usr/bin/setpriv'):
        if not (root/path).exists():
            raise ValueError('user-unit requires systemd and util-linux packages: '+path)
    put(root, '/etc/machine-id', hashlib.sha256(b'ConfOS declared native managers v1').hexdigest()[:32]+'\n')
    system = '/etc/confos/systemd-system/'
    names = []
    for user in sorted(managers):
        account = accounts[user]
        name = 'confos-user-'+account[2]+'.service'
        names.append(name)
        directory = '/etc/confos/user-units/'+user+'/systemd/user'
        put(root, system+name, '[Unit]\nDefaultDependencies=no\n[Service]\n'
            'Type=notify\nDelegate=yes\nUser='+user+'\nGroup='+account[3]+'\n'
            'Environment=PATH=/usr/local/bin:/usr/bin:/usr/sbin HOME='+account[6]+' XDG_RUNTIME_DIR=/run/user/'+account[2]+
            ' XDG_CONFIG_HOME=/etc/confos/user-units/'+user+
            ' SYSTEMD_UNIT_PATH='+directory+' SYSTEMD_GENERATOR_PATH=/dev/null'
            ' SYSTEMD_ENVIRONMENT_GENERATOR_PATH=/dev/null\n'
            'ExecStart=/usr/lib/systemd/systemd --user --unit=default.target --log-target=console\n'
            'StandardOutput=tty\nStandardError=tty\nTTYPath=/dev/console\n')
        put(root, directory+'/default.target',
            '[Unit]\nDefaultDependencies=no\nWants=basic.target\nAfter=basic.target\n')
        for target in ('basic', 'sysinit', 'sockets', 'timers', 'paths', 'shutdown'):
            put(root, directory+'/'+target+'.target', '[Unit]\nDefaultDependencies=no\n')
    put(root, system+'confos.target', '[Unit]\nDefaultDependencies=no\n'
        'Requires=confos-ready.service\nAfter=confos-ready.service\n')
    put(root, system+'confos-ready.service', '[Unit]\nDefaultDependencies=no\n'
        'Requires='+' '.join(names)+'\nAfter='+' '.join(names)+'\n[Service]\n'
        'Type=oneshot\nRemainAfterExit=yes\nExecStart=/usr/bin/confos systemd-ready\n'
        'StandardOutput=tty\nStandardError=tty\nTTYPath=/dev/console\n')

def environment(person):
    return {'PATH': '/usr/bin:/usr/sbin', 'HOME': person.pw_dir, 'LC_ALL': 'C',
        'XDG_RUNTIME_DIR': '/run/user/'+str(person.pw_uid),
        'SYSTEMD_UNIT_PATH': '/etc/confos/user-units/'+person.pw_name+'/systemd/user',
        'XDG_CONFIG_HOME': '/etc/confos/user-units/'+person.pw_name,
        'SYSTEMD_PAGER': '', 'SYSTEMD_COLORS': '0'}

def ready():
    import pwd
    if os.geteuid() != 0:
        raise SystemExit('readiness requires root')
    managers = json.loads(Path('/etc/confos/user-units.json').read_text())
    Path('/run/systemd/private').chmod(0)
    for user, units in managers.items():
        person = pwd.getpwnam(user)
        Path('/run/user/'+str(person.pw_uid)+'/systemd/private').chmod(0)
        prefix = ['/usr/bin/setpriv', '--reuid', str(person.pw_uid), '--regid', str(person.pw_gid),
                  '--init-groups', '--inh-caps=-all,+dac_override', '--ambient-caps=+dac_override',
                  '/usr/bin/systemctl', '--user', '--no-pager']
        for attempt in range(60):
            jobs = subprocess.run([*prefix, 'list-jobs', '--no-legend'], env=environment(person),
                                  capture_output=True, text=True)
            if jobs.returncode == 0 and not jobs.stdout.strip():
                break
            time.sleep(0.5)
        else:
            raise RuntimeError('native user manager did not finish startup: '+user)
        for name, state in units.items():
            if state != 'enabled':
                continue
            subprocess.run([*prefix, 'is-enabled', name], env=environment(person), check=True)
            result = subprocess.check_output([*prefix, 'show', name, '-p', 'ActiveState',
                '-p', 'Result', '-p', 'Type'], env=environment(person), text=True)
            properties = dict(line.split('=', 1) for line in result.splitlines() if '=' in line)
            if properties.get('ActiveState') != 'active' and not (
                properties.get('Type') == 'oneshot' and properties.get('Result') == 'success'):
                raise RuntimeError('enabled user unit did not start: '+user+'/'+name+' '+result)
    ssh = subprocess.Popen(['/usr/bin/aa-exec', '-p', 'confos-session', '--',
        '/usr/sbin/dropbear', '-F', '-E', '-e', '-s', '-r', '/run/ssh_host_ed25519_key'],
        stdin=subprocess.DEVNULL, start_new_session=True,
        env={'PATH': '/usr/local/bin:/usr/bin:/usr/sbin', 'LC_ALL': 'C.UTF-8', 'HOME': '/root'})
    time.sleep(1)
    if ssh.poll() is not None:
        raise RuntimeError('SSH did not start after native manager readiness')
    os.sync()
    Path('/run/confos-ready').write_bytes(Path('/etc/confos/identity').read_bytes())
    print('READY '+Path('/etc/confos/identity').read_text().strip(), flush=True)

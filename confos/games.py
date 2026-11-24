"""Native pinned LinuxGSM installation; no declaration records are generated."""
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess
import tarfile

def entries(rows):
    accounts = {r[1]: r for r in rows if r[0] == 'account'}
    result = []
    for row in rows:
        if row[0] != 'linuxgsm':
            continue
        _, user, path, release, digest, source = row
        if user not in accounts:
            raise ValueError('linuxgsm needs a declared ordinary account')
        account = accounts[user]
        if not 1 <= int(account[2]) <= 60000:
            raise ValueError('linuxgsm account UID must be in 1..60000')
        if Path(path).parent != Path(account[6]) or not re.fullmatch('/home/[A-Za-z0-9_-]+/[A-Za-z0-9_-]+', path):
            raise ValueError('linuxgsm workspace must be an immediate child of its account home')
        if any(r[0] in ('file', 'compile', 'appimage') and (r[1] == path or r[1].startswith(path+'/')) for r in rows):
            raise ValueError('linuxgsm workspace conflicts with another declared file')
        if release not in ('26.5.0', '26.6.0'):
            raise ValueError('supported native launcher releases are 26.5.0 and 26.6.0')
        identity = hashlib.sha256((user+':'+path).encode()).hexdigest()[:16]
        result.append({'user': user, 'path': path, 'release': release, 'sha256': digest,
            'source': source, 'uid': int(account[2]), 'gid': int(account[3]), 'home': account[6],
            'runtime': '/run/confos-games/'+identity})
    return sorted(result, key=lambda item: item['path'])

def configure(root, rows):
    from assemble import put
    put(root, '/etc/confos/games.json', json.dumps(entries(rows), sort_keys=True)+'\n')

def source_tree(archive_path, destination, commit):
    destination.mkdir()
    with tarfile.open(archive_path) as archive:
        archive.extractall(destination, filter='data')
    tree = destination/('LinuxGSM-'+commit)
    if not (tree/'linuxgsm.sh').is_file():
        raise ValueError('launcher source root does not match its commit')
    return tree

def install(root, rows, declaration):
    from installers import run_in_root, source_bytes
    from assemble import put
    for entry in entries(rows):
        temporary = root/'tmp/confos-game-install'
        temporary.mkdir()
        temporary_before = {directory: set((root/directory).iterdir()) if (root/directory).exists() else set()
                            for directory in ('tmp', 'var/tmp')}
        resolver = root/'etc/resolv.conf'
        previous_dns = resolver.read_bytes()
        resolver.write_bytes(Path('/etc/resolv.conf').read_bytes())
        try:
            bundle = temporary/'bundle.tar'
            bundle.write_bytes(source_bytes(declaration, entry['source'], entry['sha256']))
            names = {'manifest.json', 'initial.tar.gz', 'target.tar.gz', 'game.tar.xz', 'common.cfg', 'wetserver.cfg'}
            with tarfile.open(bundle) as archive:
                members = archive.getmembers()
                if len(members) != len(names) or {m.name for m in members} != names or not all(m.isfile() for m in members):
                    raise ValueError('invalid native game bundle layout')
                archive.extractall(temporary, members=members, filter='data')
            manifest = json.loads((temporary/'manifest.json').read_text())
            if manifest['schema'] != 1 or manifest['release'] != entry['release'] or manifest['game_release'] != '2.60b':
                raise ValueError('game bundle release mismatch')
            for name in ('initial_commit', 'target_commit'):
                if not re.fullmatch('[0-9a-f]{40}', manifest[name]):
                    raise ValueError('game bundle needs full source commits')
            for name in ('initial.tar.gz', 'target.tar.gz', 'game.tar.xz'):
                with (temporary/name).open('rb') as stream:
                    if hashlib.file_digest(stream, 'sha256').hexdigest() != manifest['sha256'][name]:
                        raise ValueError('game bundle inner input mismatch')
            initial = source_tree(temporary/'initial.tar.gz', temporary/'initial', manifest['initial_commit'])
            target = source_tree(temporary/'target.tar.gz', temporary/'target', manifest['target_commit'])
            workspace = root/entry['path'].lstrip('/')
            if workspace.exists():
                raise ValueError('native game workspace already exists')
            workspace.mkdir(parents=True)
            shutil.copy2(initial/'linuxgsm.sh', workspace/'linuxgsm.sh')
            user_script = 'set -euo pipefail\nexport PATH=/usr/bin:/usr/sbin LC_ALL=C.UTF-8 TERM=xterm\n'
            user_script += 'export HOME='+shlex.quote(entry['home'])+'\ncd '+shlex.quote(entry['path'])+'\n'
            user_script += 'export LGSM_GITHUBBRANCH='+manifest['initial_commit']+'\n'
            user_script += 'bash linuxgsm.sh wetserver\nbash wetserver auto-install\n'
            if manifest['initial_commit'] != manifest['target_commit']:
                user_script += 'export LGSM_GITHUBBRANCH='+manifest['target_commit']+'\nbash wetserver update-lgsm\n'
            put(root, '/tmp/confos-game-install/user.sh', user_script)
            entry_script = 'set -euo pipefail\nchmod 1777 /tmp\nmkdir -p /var/tmp\nchmod 1777 /var/tmp\n'
            entry_script += 'trap '+shlex.quote('chown -R 0:0 /tmp /var/tmp '+shlex.quote(entry['path']))+' EXIT\n'
            entry_script += f'chown -R {entry["uid"]}:{entry["gid"]} '+shlex.quote(entry['path'])+'\n'
            entry_script += f'setpriv --reuid {entry["uid"]} --regid {entry["gid"]} --init-groups --no-new-privs --bounding-set=-all --inh-caps=-all /bin/bash /tmp/confos-game-install/user.sh\n'
            put(root, '/tmp/confos-game-install/entry.sh', entry_script)
            run_in_root(root, '/usr/bin/timeout', '480', '/bin/bash', '/tmp/confos-game-install/entry.sh', system_mounts=True, multiple_ids=True)
            generated = (workspace/'wetserver').read_text()
            normalized = re.sub(r'^shortname="wet"$', 'shortname="core"', generated, flags=re.M)
            normalized = re.sub(r'^gameservername="wetserver"$', 'gameservername="core"', normalized, flags=re.M)
            normalized = normalized.replace('githubbranch="'+manifest['target_commit']+'"', 'githubbranch="master"')
            if normalized.encode() != (target/'linuxgsm.sh').read_bytes():
                raise ValueError('native launcher output differs from pinned target source')
            verify_game(workspace/'serverfiles', temporary/'game.tar.xz')
            for item in workspace.iterdir():
                if item.name not in ('wetserver', 'serverfiles'):
                    if item.is_dir() and not item.is_symlink(): shutil.rmtree(item)
                    else: item.unlink()
            shutil.copy2(target/'linuxgsm.sh', workspace/'linuxgsm.sh')
            modules = workspace/'lgsm/modules'
            modules.mkdir(parents=True)
            for module in sorted((target/'lgsm/modules').glob('*.sh')):
                shutil.copy2(module, modules/module.name)
                (modules/module.name).chmod(0o755)
            config = workspace/'lgsm/config-lgsm/wetserver'
            config.mkdir(parents=True)
            default = target/'lgsm/config-default/config-lgsm/wetserver/_default.cfg'
            cache = workspace/'lgsm/config-default/config-lgsm/wetserver'
            cache.mkdir(parents=True)
            shutil.copy2(default, cache/'_default.cfg')
            shutil.copy2(default, config/'_default.cfg')
            shutil.copy2(temporary/'common.cfg', config/'common.cfg')
            templates = target/'lgsm/config-default/config-lgsm'
            for source, name in (('instance-template.cfg', 'wetserver.cfg'),
                                 ('secrets-common-template.cfg', 'secrets-common.cfg'),
                                 ('secrets-instance-template.cfg', 'secrets-wetserver.cfg')):
                shutil.copy2(templates/source, config/name)
            shutil.copy2(temporary/'wetserver.cfg', workspace/'serverfiles/etmain/wetserver.cfg')
            data = workspace/'lgsm/data'
            data.mkdir()
            for name in ('serverlist.csv', 'debian-13.csv'):
                shutil.copy2(target/'lgsm/data'/name, data/name)
            (data/'wetserver.uid').write_text(hashlib.sha256((entry['path']+entry['sha256']).encode()).hexdigest()[:8]+'\n')
            for path, name in (('log', 'log'), ('lgsm/lock', 'lock'), ('lgsm/tmp', 'tmp')):
                (workspace/path).symlink_to(entry['runtime']+'/'+name)
            (workspace/'serverfiles/Logs').symlink_to(entry['runtime']+'/log/game')
            (workspace/'wetserver').chmod(0o755)
            print('NATIVE GAME INSTALLED', entry['release'], entry['path'], flush=True)
        finally:
            resolver.write_bytes(previous_dns)
            shutil.rmtree(temporary)
            for directory, before in temporary_before.items():
                if (root/directory).exists():
                    for item in set((root/directory).iterdir()) - before:
                        if item.is_dir() and not item.is_symlink(): shutil.rmtree(item)
                        else: item.unlink()

def verify_game(server, archive_path):
    expected = set()
    with tarfile.open(archive_path) as archive:
        for member in archive:
            name = member.name.removeprefix('./').rstrip('/')
            if not name: continue
            if Path(name).is_absolute() or '..' in Path(name).parts:
                raise ValueError('invalid game archive path')
            expected.add(name)
            path = server/name
            if member.isfile():
                source = archive.extractfile(member)
                if name == 'etmain/server.cfg':
                    path.write_bytes(source.read())  # Restore the package default overwritten by native setup.
                    path.chmod(member.mode)
                else:
                    checksum = hashlib.file_digest(source, 'sha256').hexdigest()
                    with path.open('rb') as installed:
                        if hashlib.file_digest(installed, 'sha256').hexdigest() != checksum:
                            raise ValueError('native game payload mismatch: '+name)
                if stat.S_IMODE(path.stat().st_mode) != member.mode:
                    raise ValueError('native game mode mismatch: '+name)
            elif member.isdir():
                if not path.is_dir(): raise ValueError('game directory absent: '+name)
            elif member.issym():
                if not path.is_symlink() or os.readlink(path) != member.linkname:
                    raise ValueError('game link mismatch: '+name)
            else:
                raise ValueError('unsupported native game archive member')
    log_directory = server/'Logs'
    if log_directory.is_dir() and 'Logs' not in expected:
        log_directory.rmdir()  # Native setup's empty record directory is moved to volatile storage.
    extras = {p.relative_to(server).as_posix() for p in server.rglob('*')} - expected - {'etmain/wetserver.cfg'}
    if extras:
        raise ValueError('unexpected native game outputs: '+', '.join(sorted(extras)))

def prepare():
    for entry in json.loads(Path('/etc/confos/games.json').read_text()):
        directory = Path(entry['runtime'])
        directory.mkdir(parents=True)
        for name in ('log', 'log/game', 'lock', 'tmp'):
            path = directory/name
            path.mkdir()
            os.chown(path, entry['uid'], entry['gid'])
            path.chmod(0o700)
        cache = directory/'tmp/linuxgsm.sh'
        cache.touch()
        subprocess.run(['mount', '--bind', entry['path']+'/linuxgsm.sh', str(cache)], check=True)
        subprocess.run(['mount', '-o', 'remount,bind,ro,nosuid,nodev,noexec', str(cache)], check=True)

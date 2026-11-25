"""Declared OCI inputs and native rootless Podman preparation before readiness."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile

def configure(root, rows, declaration):
    accounts = {r[1]: r for r in rows if r[0] == 'account'}
    result = {}
    for row in rows:
        if row[0] != 'container':
            continue
        _, user, name, image_id, digest, source = row
        if user not in accounts or not 1 <= int(accounts[user][2]) <= 60000:
            raise ValueError('container requires a declared ordinary account with UID <= 60000')
        if not re.fullmatch(r'[a-z0-9][a-z0-9./:_-]+', name):
            raise ValueError('invalid fully qualified container image name')
        if not re.fullmatch('[0-9a-f]{64}', image_id):
            raise ValueError('container requires the full image configuration digest')
        import installers
        data = installers.source_bytes(declaration, source, digest)
        target = root/'usr/lib/confos/container-images'/(digest+'.oci.tar')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        with tarfile.open(target) as archive:
            config = archive.extractfile('blobs/sha256/'+image_id)
            config_data = config.read() if config is not None else b''
            if hashlib.sha256(config_data).hexdigest() != image_id:
                raise ValueError('container archive lacks the declared image configuration')
        description = json.loads(config_data)
        if description.get('os') != 'linux' or description.get('architecture') != 'amd64':
            raise ValueError('container requires a Linux amd64 OCI image')
        defaults = description['config']
        result.setdefault(user, {})[name] = {'id': image_id,
            'archive': '/usr/lib/confos/container-images/'+target.name,
            'entrypoint': defaults.get('Entrypoint') or [], 'command': defaults.get('Cmd') or [],
            'environment': defaults.get('Env') or [], 'workdir': defaults.get('WorkingDir') or '/',
            'user': defaults.get('User') or '0'}
    (root/'etc/confos/containers.json').write_text(json.dumps(result, sort_keys=True)+'\n')
    (root/'usr/lib/confos/containers-user').mkdir(exist_ok=True)
    (root/'usr/lib/confos/containers.conf').write_text(
        '[engine]\nruntime="crun"\nconmon_path=["/usr/bin/conmon"]\n')
    for kind in ('subuid', 'subgid'):
        (root/'etc'/kind).write_text(''.join(
            f'{user}:{100000+int(accounts[user][2])*65536}:65536\n' for user in sorted(result)))
    if result:
        for path in ('usr/bin/podman', 'usr/bin/setpriv', 'usr/bin/newuidmap', 'usr/bin/newgidmap'):
            if not (root/path).is_file():
                raise ValueError('container requires Podman, uidmap and util-linux packages: '+path)

def arguments(user, uid):
    return ['/usr/bin/podman', '--root', '/run/confos-containers/'+user+'/store',
        '--runroot', '/run/user/'+str(uid)+'/confos-podman-run', '--storage-driver', 'vfs',
        '--cgroup-manager', 'cgroupfs', '--events-backend', 'file',
        '--tmpdir', '/run/user/'+str(uid)+'/confos-podman-tmp']

def environment(person):
    return {'PATH': '/usr/bin:/usr/sbin', 'HOME': person.pw_dir,
            'USER': person.pw_name, 'LOGNAME': person.pw_name, 'LC_ALL': 'C', 'TZ': 'UTC',
            'XDG_CONFIG_HOME': '/usr/lib/confos/containers-user',
            'CONTAINERS_CONF': '/usr/lib/confos/containers.conf',
            'XDG_RUNTIME_DIR': '/run/user/'+str(person.pw_uid)}

def prepare():
    import pwd
    declared = json.loads(Path('/etc/confos/containers.json').read_text())
    if not declared:
        return
    access = 'rw' if Path('/etc/confos/systemd-system').exists() else 'ro'
    subprocess.run(['mount', '-t', 'cgroup2', '-o', access+',nosuid,nodev,noexec',
                    'cgroup2', '/sys/fs/cgroup'], check=True)
    base = Path('/run/confos-containers')
    base.mkdir()
    subprocess.run(['mount', '-t', 'tmpfs', '-o', 'nosuid,nodev,exec', 'tmpfs', str(base)], check=True)
    for user, images in sorted(declared.items()):
        person = pwd.getpwnam(user)
        directory = base/user
        directory.mkdir(mode=0o700)
        os.chown(directory, person.pw_uid, person.pw_gid)
        prefix = ['/usr/bin/setpriv', '--reuid', str(person.pw_uid), '--regid', str(person.pw_gid),
                  '--init-groups', *arguments(user, person.pw_uid)]
        for name, image in sorted(images.items()):
            subprocess.run([*prefix, 'load', '--input', image['archive']],
                           env=environment(person), check=True)
            actual = subprocess.check_output([*prefix, 'image', 'inspect', '--format', '{{.Id}}', name],
                                            env=environment(person), text=True).strip()
            if actual != image['id']:
                raise RuntimeError('loaded container identity differs from declaration')
            source = subprocess.check_output([*prefix, 'unshare', *arguments(user, person.pw_uid),
                                            'image', 'mount', name],
                                            env=environment(person), text=True).strip()
            if not Path(source).is_relative_to(directory/'store'):
                raise RuntimeError('unexpected native container mount path')
            # Native runtime mount targets must exist before making this view read-only.
            # These fixed empty additions are part of the base recipe, never observed settings.
            # An image may lack the folders the runtime mounts on (busybox:1.36.1 has no
            # /proc and no /sys: `crun: cannot mkdir proc: Read-only file system`).
            for relative in ('proc', 'sys', 'dev', 'run', 'etc'):
                target = Path(source)/relative
                if not target.exists() and not target.is_symlink():
                    target.mkdir(mode=0o755)
                    os.chown(target, person.pw_uid, person.pw_gid)
            for relative in ('etc/hosts', 'etc/hostname', 'etc/resolv.conf', 'run/.containerenv'):
                target = Path(source)/relative
                parent = target.parent.resolve()
                if not parent.is_relative_to(Path(source).resolve()):
                    raise RuntimeError('container runtime mount target escapes its image')
                if not parent.exists():
                    parent.mkdir(mode=0o755)
                    os.chown(parent, person.pw_uid, person.pw_gid)
                try:
                    fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
                except FileExistsError:
                    continue
                os.fchown(fd, person.pw_uid, person.pw_gid)
                os.close(fd)
            # The native runtime links /etc/mtab to /proc/mounts when an image has none
            # (busybox:1.36.1); on the read-only view that failed with `creating
            # /etc/mtab symlink: read-only file system` (case X-REC-PODMAN on 0.43).
            # The same link is made here, before the view becomes read-only.
            mtab = Path(source)/'etc/mtab'
            if not mtab.exists() and not mtab.is_symlink():
                os.symlink('/proc/mounts', mtab)
                os.lchown(mtab, person.pw_uid, person.pw_gid)
            destination = Path('/run/confos-container-ro')/user/image['id']
            if destination.exists():
                continue
            destination.mkdir(parents=True)
            subprocess.run(['mount', '--bind', source, str(destination)], check=True)
            subprocess.run(['mount', '-o', 'remount,bind,ro,nosuid,nodev,exec', str(destination)], check=True)
        # The loader's rootless pause namespace predates these host bind mounts.
        # Retire it so the first run inherits the completed read-only mount view.
        subprocess.run([*prefix, 'system', 'migrate'], env=environment(person), check=True)

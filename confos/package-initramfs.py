#!/usr/bin/python3
"""Worker-only package build from original pinned Debian archives and authored init.

No declaration, installed ConfOS root or runtime file manifest is an input.
APT authenticates archive checksums using the fixed snapshot's signed metadata.
"""
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
EPOCH = 1795392000
SNAPSHOTS = ('20260801T000000Z', '20261001T000000Z', '20261123T000000Z')

def run(*args, **kwargs):
    return subprocess.run([str(x) for x in args], check=True, **kwargs)

def build(version, snapshot, destination):
    if not re.fullmatch(r'[0-9]+\.[0-9]+', version) or snapshot not in SNAPSHOTS:
        raise ValueError('numeric source release and supported snapshot required')
    pins = dict(line.split('=', 1) for line in (HERE/'components'/(snapshot+'.txt')).read_text().splitlines())
    pins = {name: release for name, release in pins.items() if not name.startswith('confos-')}
    destination = Path(destination).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='initramfs-build-', dir=destination.parent) as temporary:
        work = Path(temporary)
        apt = work/'apt'
        for sub in ('lists/partial', 'archives/partial', 'etc', 'log'):
            (apt/sub).mkdir(parents=True)
        (apt/'status').write_text('')
        (apt/'etc/sources.list').write_text(
            f'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/{snapshot}/ trixie main\n')
        values = {'Dir::State::status': apt/'status', 'Dir::State::lists': apt/'lists',
            'Dir::Cache::archives': apt/'archives', 'Dir::Etc::sourcelist': apt/'etc/sources.list',
            'Dir::Etc::sourceparts': '-', 'Dir::Etc::parts': '-', 'Dir::Etc::main': '-',
            'APT::Install-Recommends': 'false', 'APT::Install-Suggests': 'false',
            'APT::Sandbox::User': 'root', 'Acquire::Check-Valid-Until': 'false',
            'Acquire::Retries': '3', 'Acquire::http::Timeout': '30', 'Acquire::Languages': 'none',
            'Dir::Log': apt/'log', 'Dir::Cache::pkgcache': '', 'Dir::Cache::srcpkgcache': ''}
        options = [value for key, setting in values.items() for value in ('-o', f'{key}={setting}')]
        run('apt-get', *options, 'update')
        requested = [name+'='+release for name, release in sorted(pins.items())]
        resolution = subprocess.check_output(['apt-get', *options, '--simulate', 'install', *requested], text=True)
        if dict(re.findall(r'^Inst (\S+) \((\S+) ', resolution, re.M)) != pins:
            raise ValueError('native input closure differs from committed snapshot lock')
        run('apt-get', *options, '--yes', '--download-only', 'install', *requested)
        root = work/'root'
        root.mkdir()
        seen = {}
        for archive in sorted((apt/'archives').glob('*.deb')):
            control = subprocess.check_output(['dpkg-deb', '-f', str(archive)], text=True)
            fields = dict(line.split(': ', 1) for line in control.splitlines()
                          if ': ' in line and not line.startswith(' '))
            name, release = fields['Package'], fields['Version']
            if name in seen or pins.get(name) != release:
                raise ValueError('unexpected original archive: '+archive.name)
            seen[name] = release
            run('dpkg-deb', '-x', archive, root)
        if seen != pins:
            raise ValueError('missing original archives')
        for name, target in [('bin', 'usr/bin'), ('sbin', 'usr/sbin'), ('lib', 'usr/lib'), ('lib64', 'usr/lib64')]:
            if not (root/name).exists():
                (root/name).symlink_to(target)
        init = root/'initroot'
        for name in ('bin', 'proc', 'sys', 'dev', 'system', 'newroot', 'lib/modules'):
            (init/name).mkdir(parents=True, exist_ok=True)
        (init/'sbin').symlink_to('bin')
        shutil.copyfile(root/'usr/bin/busybox', init/'bin/busybox')
        (init/'bin/busybox').chmod(0o755)
        for name in ('sh', 'mount', 'mkdir', 'sleep', 'cat', 'modprobe', 'switch_root', 'mdev'):
            (init/'bin'/name).symlink_to('busybox')
        shutil.copytree(root/'usr/lib/modules', init/'lib/modules', dirs_exist_ok=True)
        releases = sorted(path.name for path in (init/'lib/modules').iterdir())
        if len(releases) != 1:
            raise ValueError('expected exactly one original kernel')
        release = releases[0]
        def native(*args):
            return run('unshare', '--user', '--map-root-user', '--', 'chroot', root,
                       '/usr/bin/env', '-i', 'PATH=/usr/bin:/usr/sbin', 'LC_ALL=C', 'TZ=UTC', *args)
        native('/usr/sbin/depmod', '-b', '/initroot', release)
        metadata = sorted((init/'lib/modules'/release).glob('modules.*'))
        for path in metadata:
            path.chmod(0o644)
        (init/'init').write_bytes((HERE/'early-init').read_bytes())
        (init/'init').chmod(0o755)
        for path in [*init.rglob('*'), init]:
            if path.is_dir(): path.chmod(0o755)
            os.utime(path, (EPOCH, EPOCH), follow_symlinks=False)
        (root/'tmp').mkdir(exist_ok=True)
        (root/'tmp/names').write_bytes(b'.\0'+b''.join(
            ('./'+str(path.relative_to(init))).encode()+b'\0' for path in sorted(init.rglob('*'))))
        (root/'tmp/make-initramfs').write_text(
            'set -eu\ncd /initroot\n/usr/bin/cpio --null -o -H newc --owner=0:0 --reproducible </tmp/names >/tmp/initramfs\n')
        native('/usr/bin/bash', '/tmp/make-initramfs')
        package = work/'package'
        def put(name, data, mode=0o644):
            path = package/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            path.chmod(mode)
        initramfs = (root/'tmp/initramfs').read_bytes()
        put('usr/lib/confos/initramfs/initramfs', initramfs)
        put('usr/lib/confos/initramfs/kernel-release', (release+'\n').encode())
        for path in metadata:
            put('usr/lib/modules/'+release+'/'+path.name, path.read_bytes())
        put('usr/share/doc/confos-initramfs/build-inputs.txt', ''.join(
            name+'='+release+'\n' for name, release in sorted(pins.items())).encode())
        put('usr/share/doc/confos-initramfs/snapshot', (snapshot+'\n').encode())
        put('usr/share/doc/confos-initramfs/early-init', (HERE/'early-init').read_bytes())
        put('DEBIAN/control', (
            f'Package: confos-initramfs\nVersion: {version}+{snapshot}\nArchitecture: amd64\n'
            'Maintainer: ConfOS project\nSection: admin\nPriority: required\n'
            f'Replaces: linux-image-{release}\n'
            'Description: Pinned ConfOS initramfs and kernel module indexes\n'
            ' Built from original Debian archives with pinned native depmod and cpio.\n'
            ' No maintainer scripts or installed-system snapshot.\n').encode())
        for path in [*package.rglob('*'), package]:
            if path.is_dir(): path.chmod(0o755)
            os.utime(path, (EPOCH, EPOCH), follow_symlinks=False)
        artifact = work/'initramfs.deb'
        run('dpkg-deb', '--root-owner-group', '--uniform-compression', '-Zgzip', '-z9',
            '--build', package, artifact,
            env=dict(os.environ, SOURCE_DATE_EPOCH=str(EPOCH), LC_ALL='C', TZ='UTC'))
        digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
        checksum = work/'checksum'
        checksum.write_text(digest+'\n')
        os.replace(artifact, destination)
        os.replace(checksum, destination.with_suffix('.deb.sha256'))
        print('INITRAMFS SHA256', snapshot, hashlib.sha256(initramfs).hexdigest(), flush=True)
        print('PINNED TOOLS', snapshot, pins['cpio'], pins['kmod'], flush=True)
        print('INITRAMFS PACKAGE SHA256', digest, destination.name, flush=True)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit('usage: package-initramfs.py VERSION SNAPSHOT OUTPUT.deb')
    build(*sys.argv[1:])

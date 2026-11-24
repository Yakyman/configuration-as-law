#!/usr/bin/python3
"""Build EFI package from pinned original GRUB archives and authored configuration.

Worker-only. No declaration or installed ConfOS output is read. `lock` prepares
build-input metadata; `build VERSION OUTPUT.deb` consumes the committed lock.
"""
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
EPOCH = 1795392000
SNAPSHOT = '20261123T000000Z'
ROOTS = ['grub-common', 'grub-efi-amd64-bin',
         'coreutils=9.7-3', 'bash=5.2.37-2+b10']

def call(*args, **kwargs):
    return subprocess.run([str(a) for a in args], check=True, **kwargs)

def apt_options(work):
    for sub in ('lists/partial', 'archives/partial', 'etc', 'log'):
        (work/sub).mkdir(parents=True)
    (work/'status').write_text('')
    (work/'etc/sources.list').write_text(
        f'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/{SNAPSHOT}/ trixie main\n')
    values = {'Dir::State::status': work/'status', 'Dir::State::lists': work/'lists',
        'Dir::Cache::archives': work/'archives', 'Dir::Etc::sourcelist': work/'etc/sources.list',
        'Dir::Etc::sourceparts': '-', 'Dir::Etc::parts': '-', 'Dir::Etc::main': '-',
        'APT::Install-Recommends': 'false', 'APT::Install-Suggests': 'false',
        'APT::Sandbox::User': 'root', 'Acquire::Check-Valid-Until': 'false',
        'Acquire::Retries': '3', 'Acquire::Languages': 'none', 'Dir::Log': work/'log',
        'Dir::Cache::pkgcache': '', 'Dir::Cache::srcpkgcache': ''}
    return [value for key, setting in values.items() for value in ('-o', f'{key}={setting}')]

def resolve(options, requested):
    text = subprocess.check_output(['apt-get', *options, '--simulate', 'install', *requested], text=True)
    return dict(re.findall(r'^Inst (\S+) \((\S+) ', text, re.M))

def main():
    mode = sys.argv[1]
    if mode not in ('lock', 'build') or (mode == 'build' and len(sys.argv) != 4):
        raise SystemExit('usage: package-boot.py lock | build VERSION OUTPUT.deb')
    output_dir = HERE/'packages'
    output_dir.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='boot-build-', dir=output_dir) as temporary:
        work = Path(temporary)
        options = apt_options(work/'apt')
        call('apt-get', *options, 'update')
        if mode == 'lock':
            pins = resolve(options, ROOTS)
            assert all(item.split('=')[0] in pins for item in ROOTS)
            (HERE/'boot-components.txt').write_text(''.join(
                name+'='+version+'\n' for name, version in sorted(pins.items())))
            print('LOCKED BOOT BUILD INPUTS', SNAPSHOT, len(pins))
            return
        version, destination = sys.argv[2:]
        if not re.fullmatch(r'[0-9]+\.[0-9]+', version):
            raise ValueError('numeric boot package release required')
        pins = dict(line.split('=', 1) for line in (HERE/'boot-components.txt').read_text().splitlines())
        requested = [name+'='+release for name, release in sorted(pins.items())]
        if resolve(options, requested) != pins:
            raise ValueError('build-input dependency closure differs from committed lock')
        call('apt-get', *options, '--yes', '--download-only', 'install', *requested)
        root = work/'root'
        root.mkdir()
        grub_source = None
        for archive in sorted((work/'apt/archives').glob('*.deb')):
            call('dpkg-deb', '-x', archive, root)
            if archive.name.startswith('grub-common_'):
                source = subprocess.check_output(['dpkg-deb', '-f', str(archive), 'Source'], text=True).strip()
                match = re.fullmatch(r'([a-z0-9.+-]+)(?: \(([^)]+)\))?', source)
                if not match:
                    raise ValueError('GRUB source identity absent')
                grub_source = match[1]+' (= '+(match[2] or pins['grub-common'])+')'
        if grub_source is None:
            raise ValueError('GRUB source archive metadata absent')
        for name, target in [('bin', 'usr/bin'), ('sbin', 'usr/sbin'),
                             ('lib', 'usr/lib'), ('lib64', 'usr/lib64')]:
            if not (root/name).exists():
                (root/name).symlink_to(target)
        if not (root/'usr/bin/sh').exists():
            (root/'usr/bin/sh').symlink_to('bash')
        (root/'tmp').mkdir(exist_ok=True)
        configuration = root/'tmp/grub.cfg'
        configuration.write_bytes((HERE/'boot-grub.cfg').read_bytes())
        os.utime(configuration, (EPOCH, EPOCH))
        argv = ['chroot', str(root), '/usr/bin/env', '-i',
            'PATH=/usr/bin:/usr/sbin', 'LC_ALL=C', 'TZ=UTC', f'SOURCE_DATE_EPOCH={EPOCH}',
            '/usr/bin/grub-mkstandalone', '-O', 'x86_64-efi',
            '--modules=part_gpt ext2 search search_label linux configfile normal',
            '-o', '/tmp/BOOTX64.EFI', 'boot/grub/grub.cfg=/tmp/grub.cfg']
        call('unshare', '--user', '--map-root-user', '--', *argv)
        package = work/'package'
        def put(name, data, mode=0o644):
            path = package/name.lstrip('/')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            path.chmod(mode)
        efi = (root/'tmp/BOOTX64.EFI').read_bytes()
        put('usr/lib/confos/boot/BOOTX64.EFI', efi)
        put('usr/share/doc/confos-boot/copyright',
            (root/'usr/share/doc/grub-efi-amd64-bin/copyright').read_bytes())
        put('usr/share/doc/confos-boot/build-inputs.txt', (HERE/'boot-components.txt').read_bytes())
        put('usr/share/doc/confos-boot/grub.cfg', configuration.read_bytes())
        put('DEBIAN/control', (
            f'Package: confos-boot\nVersion: {version}\nArchitecture: amd64\n'
            'Maintainer: ConfOS project\nSection: admin\nPriority: required\n'
            f'Built-Using: {grub_source}\n'
            'Description: Pinned standalone ConfOS EFI boot program\n'
            ' Built from original Debian GRUB archives and fixed authored configuration.\n'
            ' No maintainer scripts or installed-system snapshot.\n').encode())
        for path in [*package.rglob('*'), package]:
            if path.is_dir(): path.chmod(0o755)
            os.utime(path, (EPOCH, EPOCH), follow_symlinks=False)
        output = Path(destination).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        artifact = work/'boot.deb'
        environment = dict(os.environ, SOURCE_DATE_EPOCH=str(EPOCH), TZ='UTC', LC_ALL='C')
        call('dpkg-deb', '--root-owner-group', '--uniform-compression', '-Zgzip', '-z9',
            '--build', package, artifact, env=environment)
        digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
        checksum = work/'checksum'
        checksum.write_text(digest+'\n')
        os.replace(artifact, output)
        os.replace(checksum, output.with_suffix('.deb.sha256'))
        print('BOOT EFI SHA256', hashlib.sha256(efi).hexdigest())
        print('BOOT PACKAGE SHA256', digest, output.name)

if __name__ == '__main__':
    main()

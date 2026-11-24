"""Install declared immutable language packages using their native installers.

No declaration is written. Inputs and dependencies are pinned before installation.
"""
import email.parser
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import zipfile

def run_in_root(root, *argv, system_mounts=True, multiple_ids=False):
    # Code readers consult kernel confinement state via /proc. Even ordinary
    # staged Python/Bash commands need the private kernel-context mounts; no
    # environment flag bypasses the code-input policy.
    mounted = None
    execution_root = root
    if os.geteuid() == 0 and Path('/etc/confos/identity').is_file():
        # Mutable storage stays noexec. Only the privileged application uses this
        # temporary executable view of its frozen candidate, denied to sessions.
        mounted = Path('/run/confos-installer-root')
        mounted.mkdir(exist_ok=True)
        subprocess.run(['mount', '--bind', str(root), str(mounted)], check=True)
        try:
            subprocess.run(['mount', '-o', 'remount,bind,rw,nosuid,nodev,exec', str(mounted)], check=True)
        except BaseException:
            subprocess.run(['umount', str(mounted)], check=True)
            mounted.rmdir()
            raise
        execution_root = mounted
    command = ['chroot', str(execution_root), '/usr/bin/env', '-i',
               'PATH=/usr/local/bin:/usr/bin:/usr/sbin:/bin:/sbin', 'LC_ALL=C',
               'PYTHONDONTWRITEBYTECODE=1', 'SOURCE_DATE_EPOCH=1795392000', 'TZ=UTC', *argv]
    if system_mounts:
        command = ['unshare', '--mount', '--pid', '--fork', '--', '/bin/bash',
                   str(Path(__file__).with_name('installer-chroot')), str(execution_root), *argv]
        if os.geteuid() != 0:
            command[1:1] = ['--user', *(['--map-auto'] if multiple_ids else []), '--map-root-user']
    elif os.geteuid() != 0:
        command = ['unshare', '--user', '--map-root-user', '--', *command]
    try:
        subprocess.run(command, check=True)
    finally:
        if mounted is not None:
            subprocess.run(['umount', str(mounted)], check=True)
            mounted.rmdir()

def source_bytes(declaration, source, digest):
    if Path(source).is_absolute() or '..' in Path(source).parts:
        raise ValueError('installer inputs must be below the declaration directory')
    data = (declaration.parent/source).read_bytes()
    if not re.fullmatch('[0-9a-f]{64}', digest) or hashlib.sha256(data).hexdigest() != digest:
        raise ValueError('installer input checksum mismatch')
    return data

def link(root, name, target):
    dest = root/'usr/local/bin'/name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() or dest.is_symlink():
        raise ValueError('installer command collision: '+name)
    dest.symlink_to(target)

def install(root, rows, declaration):
    rows = sorted((row for row in rows if row[0] in ('pip', 'npm', 'compile', 'flatpak', 'appimage')),
                  key=lambda row: (row[0], 0 if row[1].startswith('runtime/') else 1, row[1:]))
    if not rows:
        return
    temporary = root/'tmp/confos-install'
    temporary.mkdir(parents=True)
    resolver = root/'etc/resolv.conf'
    guest_dns = resolver.read_bytes()
    resolver.write_bytes(Path('/etc/resolv.conf').read_bytes())
    try:
        wheels = []
        for row in rows:
            if row[0] == 'appimage':
                _, path, mode, digest, source = row
                if (not path.startswith(('/home/', '/usr/local/', '/etc/confos/user/')) or
                    '..' in Path(path).parts or
                    (path.startswith('/home/') and len(Path(path).parts) < 4)):
                    raise ValueError('invalid AppImage launcher path')
                if not re.fullmatch('0?[0-7]{3}', mode) or not int(mode, 8) & 0o111:
                    raise ValueError('AppImage launcher needs executable mode without special bits')
                data = source_bytes(declaration, source, digest)
                if len(data) < 64 or data[:6] != b'\x7fELF\x02\x01' or data[8:11] != b'AI\x02':
                    raise ValueError('AppImage must be type 2 with a little-endian ELF64 runtime')
                section_offset = struct.unpack_from('<Q', data, 40)[0]
                section_size, section_count = struct.unpack_from('<HH', data, 58)
                offset = section_offset + section_size * section_count
                if not section_count or data[offset:offset+4] != b'hsqs':
                    raise ValueError('AppImage has no supported embedded squashfs at the ELF end')
                prefix = '/opt/confos/appimages/'+digest
                appdir = root/prefix.lstrip('/')
                if not appdir.exists():
                    appdir.parent.mkdir(parents=True, exist_ok=True)
                    image = temporary/'input.appimage'
                    image.write_bytes(data)
                    subprocess.run(['unsquashfs', '-no-progress', '-no-xattrs', '-processors', '2',
                                    '-offset', str(offset), '-dest', str(appdir), str(image)], check=True)
                    import appimage_readers
                    appimage_readers.apply(root, appdir, digest)
                if not (appdir/'AppRun').exists():
                    raise ValueError('AppImage lacks AppRun')
                target = root/path.lstrip('/')
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.parent.resolve().is_relative_to(root.resolve()):
                    raise ValueError('AppImage launcher parent escapes root')
                if target.exists() or target.is_symlink():
                    raise ValueError('AppImage launcher conflicts with another installed object')
                target.write_text('#!/bin/sh\nAPPDIR='+prefix+'\nexport APPDIR\nexec "$APPDIR/AppRun" "$@"\n')
                target.chmod(int(mode, 8))
                continue
            if row[0] == 'flatpak':
                _, ref, commit, digest, source = row
                if not re.fullmatch(r'(?:app|runtime)/[A-Za-z0-9_.-]+/x86_64/[A-Za-z0-9_.-]+', ref):
                    raise ValueError('flatpak requires a complete app/runtime x86_64 ref')
                if not re.fullmatch('[0-9a-f]{64}', commit):
                    raise ValueError('flatpak requires the full OSTree commit')
                bundle = temporary/'input.flatpak'
                bundle.write_bytes(source_bytes(declaration, source, digest))
                run_in_root(root, '/usr/bin/flatpak', 'install', '--system',
                    '--bundle', '--no-deps', '--no-related', '--noninteractive', '-y',
                    '/tmp/confos-install/input.flatpak', system_mounts=True)
                deployments = root/'var/lib/flatpak'/ref
                if not (deployments/commit/'files').is_dir() or (deployments/'active').readlink() != Path(commit):
                    raise ValueError('Flatpak bundle installed a different ref/commit')
                import flatpak_readers
                flatpak_readers.apply(root, root/'var/lib/flatpak', ref, commit, digest)
                continue
            if row[0] == 'compile':
                _, path, mode, digest, source, *flags = row
                if (not path.startswith(('/home/', '/usr/local/', '/etc/confos/user/')) or
                    '..' in Path(path).parts or
                    (path.startswith('/home/') and len(Path(path).parts) < 4)):
                    raise ValueError('invalid compiled output path')
                if not re.fullmatch('0?[0-7]{3}', mode) or not int(mode, 8) & 0o111:
                    raise ValueError('compiled output needs executable mode without special bits')
                for flag in flags:
                    if not re.fullmatch(r'-O[0123sgz]|-std=(?:c|gnu)(?:89|99|11|17|23)|-W(?:all|extra|error)|-pedantic', flag):
                        raise ValueError('unsupported gcc flag: '+flag)
                (temporary/'source.c').write_bytes(source_bytes(declaration, source, digest))
                target = root/path.lstrip('/')
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.parent.resolve().is_relative_to(root.resolve()):
                    raise ValueError('compiled output parent escapes root')
                if target.exists() or target.is_symlink():
                    raise ValueError('compiled output conflicts with another installed object')
                run_in_root(root, '/usr/bin/gcc', *flags, '-o', path, '/tmp/confos-install/source.c')
                target.chmod(int(mode, 8))
                continue
            kind, name, version, digest, source = row
            if not re.fullmatch('[A-Za-z0-9][A-Za-z0-9_.-]*', name):
                raise ValueError('unsupported language package name')
            data = source_bytes(declaration, source, digest)
            if kind == 'pip':
                filename = Path(source).name
                if not filename.endswith('.whl'):
                    raise ValueError('pip inputs must be wheels; source builds are unsupported')
                target = temporary/filename
                target.write_bytes(data)
                with zipfile.ZipFile(target) as wheel:
                    metadata = [p for p in wheel.namelist() if p.endswith('.dist-info/METADATA')]
                    if len(metadata) != 1:
                        raise ValueError('wheel needs one distribution metadata file')
                    meta = email.parser.BytesParser().parsebytes(wheel.read(metadata[0]))
                    normalize = lambda value: re.sub('[-_.]+', '-', value).lower()
                    if normalize(meta['Name']) != normalize(name) or meta['Version'] != version:
                        raise ValueError('wheel name/version differs from declaration')
                wheels.append('/tmp/confos-install/'+filename)
            else:
                lock = json.loads(data)
                packages = lock.get('packages', {})
                if lock.get('lockfileVersion') not in (2, 3):
                    raise ValueError('npm requires a version 2 or 3 package-lock.json')
                if packages.get('', {}).get('dependencies') != {name: version}:
                    raise ValueError('npm lock must name exactly the declared root dependency/release')
                for path, package in packages.items():
                    if not path:
                        continue
                    if not path.startswith('node_modules/') or '..' in Path(path).parts:
                        raise ValueError('unsupported npm lock package path')
                    if (not package.get('resolved', '').startswith('https://') or
                        not package.get('integrity', '').startswith(('sha512-', 'sha256-'))):
                        raise ValueError('npm dependencies require HTTPS sources and integrity hashes')
                prefix = '/opt/confos/npm/'+name
                installroot = root/prefix.lstrip('/')
                installroot.mkdir(parents=True)
                (installroot/'package-lock.json').write_bytes(data)
                (installroot/'package.json').write_text(json.dumps({
                    'name': lock.get('name', 'confos-package'), 'version': lock.get('version', '1.0.0'),
                    'private': True, 'dependencies': {name: version}}, sort_keys=True)+'\n')
                run_in_root(root, '/usr/bin/node', '/usr/share/nodejs/npm/bin/npm-cli.js', 'ci', '--prefix', prefix,
                    '--ignore-scripts', '--no-audit', '--no-fund', '--cache', '/tmp/confos-install/npm-cache',
                    '--userconfig', '/dev/null', '--globalconfig', '/tmp/confos-install/npmrc')
                actual = json.loads((installroot/'node_modules'/name/'package.json').read_text())
                if actual.get('name') != name or actual.get('version') != version:
                    raise ValueError('npm installed a different root release')
                bins = actual.get('bin', {})
                if isinstance(bins, str):
                    bins = {name: bins}
                for binary in sorted(bins):
                    if not re.fullmatch('[A-Za-z0-9_.-]+', binary):
                        raise ValueError('unsupported npm command name')
                    link(root, 'npm-'+binary, prefix+'/node_modules/.bin/'+binary)
        if wheels:
            versions = sorted((root/'usr/lib').glob('python3.[0-9]*'))
            versions = [p.name for p in versions if p.is_dir() and re.fullmatch(r'python3\.[0-9]+', p.name)]
            if len(versions) != 1:
                raise ValueError('one Python minor release is required for pip')
            target = '/usr/local/lib/'+versions[0]+'/dist-packages'
            run_in_root(root, '/usr/bin/python3', '-IB', '/usr/bin/pip3', 'install', '--no-index', '--no-deps',
                '--no-compile', '--no-cache-dir', '--disable-pip-version-check', '--target', target, *wheels)
            bindir = root/target.lstrip('/')/'bin'
            if bindir.is_dir():
                for binary in sorted(bindir.iterdir()):
                    link(root, binary.name, target+'/bin/'+binary.name)
        flatpak_store = root/'var/lib/flatpak'
        if any(row[0] == 'flatpak' for row in rows):
            shutil.move(flatpak_store, root/'usr/lib/confos/flatpak')
            flatpak_store.symlink_to('/usr/lib/confos/flatpak')
    finally:
        resolver.write_bytes(guest_dns)
        shutil.rmtree(temporary)

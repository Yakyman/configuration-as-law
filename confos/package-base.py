#!/usr/bin/python3
"""Build a genuine runtime data package from source, never an installed snapshot.

Worker-only release preparation. This does not read a declaration or write its lines.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
EPOCH = 1795392000
RUNTIME = ('nmcli-command', 'visudo-command', 'radio_inspect.py', 'radio_declaration.py', 'radio_runtime.py', 'radio_integration.py', 'radio_systemd.py', 'radio-control-denials.apparmor', 'radio-trusted-profile.apparmor', 'assemble.py', 'archive_sources.py', 'archive-sources.json', 'recording.py', 'language_recording.py', 'flatpak_recording.py', 'podman_recording.py', 'configuration_recording.py', 'configuration-command', 'apt-command', 'optional_readers.py', 'appimage_readers.py', 'flatpak_readers.py', 'flatpak_profile.py', 'flatpak-profile.apparmor', 'installers.py', 'containers.py', 'user_units.py', 'games.py',
    'installer-chroot', 'nft-query', 'flatpak-command', 'podman-command',
    'systemctl-query', 'language-query', 'components.txt', 'runtime-init', 'confos',
    'early-init', 'VERSION')

def build(output):
    version = (HERE/'VERSION').read_text().strip()
    if not re.fullmatch(r'[0-9]+\.[0-9]+', version):
        raise ValueError('runtime package needs the numeric source release')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='base-package-', dir=output.parent) as directory:
        root = Path(directory)/'root'
        root.mkdir()
        def put(path, data, mode=0o644):
            target = root/path.lstrip('/')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            target.chmod(mode)
        for name in RUNTIME:
            put('/usr/lib/confos/'+name, (HERE/name).read_bytes(), 0o755 if name == 'systemctl-query' else 0o644)
        for lock in sorted((HERE/'components').glob('*Z.txt')):
            put('/usr/lib/confos/components/'+lock.name, lock.read_bytes())
        put('/usr/bin/confos', (HERE/'confos').read_bytes(), 0o755)
        put('/usr/sbin/init', (HERE/'runtime-init').read_bytes(), 0o755)
        for command, source in {'nmcli': 'nmcli-command', 'visudo': 'visudo-command', 'apt': 'apt-command', 'apt-get': 'apt-command', 'nft': 'nft-query', 'flatpak': 'flatpak-command',
                'podman': 'podman-command', 'systemctl': 'systemctl-query',
                'pip': 'language-query', 'pip3': 'language-query',
                'npm': 'language-query', 'npx': 'language-query', **{name: 'configuration-command' for name in ('hostnamectl', 'timedatectl', 'sysctl', 'useradd', 'usermod', 'userdel')}}.items():
            put('/usr/lib/confos/commands/'+command, (HERE/source).read_bytes(), 0o755)
            if command in ('apt', 'apt-get', 'nmcli', 'visudo', 'nft', 'systemctl', 'hostnamectl', 'timedatectl', 'sysctl', 'useradd', 'usermod', 'userdel'):
                entry = root/'usr/local/bin'/command
                entry.parent.mkdir(parents=True, exist_ok=True)
                entry.symlink_to('/usr/lib/confos/commands/'+command)
        put('/usr/lib/python3/dist-packages/pip/__main__.py',
            b'import os, sys\nos.execv("/usr/local/bin/pip3", ["pip3", *sys.argv[1:]])\n')
        put('/etc/confos/npm-query.conf', b'')
        for path, value in json.loads((HERE/'base-defaults.json').read_text()).items():
            put(path, value['text'].encode(), int(value['mode'], 8))
        for name in ('etc/sudoers.d', 'etc/confos', 'usr/lib/confos/flatpak-user', 'usr/lib/confos/npm-query-cache'):
            (root/name).mkdir(parents=True, exist_ok=True)
        put('/DEBIAN/control', (
            'Package: confos-runtime\nVersion: '+version+'\nArchitecture: all\n'
            'Maintainer: ConfOS project\nSection: admin\nPriority: required\n'
            'Replaces: base-files, bash, libc-bin, libpam-runtime, sudo, python3-pip\n'
            'Description: ConfOS fixed application runtime and native defaults\n'
            ' Source-built runtime files and literal default configuration payloads.\n'
            ' No maintainer scripts; installed by the ConfOS declaration assembler.\n').encode())
        for path in [*root.rglob('*'), root]:
            if path.is_dir(): path.chmod(0o755)
            os.utime(path, (EPOCH, EPOCH), follow_symlinks=False)
        environment = dict(os.environ, SOURCE_DATE_EPOCH=str(EPOCH), TZ='UTC', LC_ALL='C')
        artifact = Path(directory)/'payload.deb'
        subprocess.run(['dpkg-deb', '--root-owner-group', '--uniform-compression',
            '-Zgzip', '-z9', '--build', str(root), str(artifact)], env=environment, check=True)
        checksum = hashlib.sha256(artifact.read_bytes()).hexdigest()
        manifest = Path(directory)/'checksum'
        manifest.write_text(checksum+'\n')
        os.replace(artifact, output)
        os.replace(manifest, output.with_suffix('.deb.sha256'))
    with output.open('rb') as stream:
        print(hashlib.file_digest(stream, 'sha256').hexdigest(), output.name)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: package-base.py OUTPUT.deb')
    build(Path(sys.argv[1]).resolve())

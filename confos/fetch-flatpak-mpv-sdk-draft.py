#!/usr/bin/python3
"""Private worker SDK store using retained native tooling; no host installation."""
from pathlib import Path
import subprocess

root = Path.cwd()
work = root/'interpreter-inputs/flatpak-mpv-lua-candidate'
native = root/'interpreter-inputs/flatpak-analysis/root'
for name in ('sdk-store', 'sdk-var-tmp', 'sdk-home'):
    (work/name).mkdir(exist_ok=True)
base = ['bwrap', '--unshare-user', '--uid', '0', '--gid', '0', '--unshare-pid',
        '--unshare-ipc', '--unshare-uts', '--die-with-parent', '--clearenv',
        '--ro-bind', str(native), '/', '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp',
        '--tmpfs', '/run', '--bind', str(work/'sdk-store'), '/usr/lib/confos/flatpak',
        '--bind', str(work/'sdk-var-tmp'), '/var/tmp', '--bind', str(work/'sdk-home'), '/root',
        '--ro-bind', '/etc/resolv.conf', '/etc/resolv.conf',
        '--setenv', 'PATH', '/usr/bin:/usr/sbin', '--setenv', 'HOME', '/root',
        '--setenv', 'LC_ALL', 'C.UTF-8', '/usr/bin/flatpak']
commands = [
    ['remote-add', '--system', '--no-gpg-verify', '--if-not-exists', 'sdk-source', 'https://dl.flathub.org/repo/'],
    ['install', '--system', '--noninteractive', '--no-related', '--no-deps', 'sdk-source',
     'runtime/org.freedesktop.Sdk/x86_64/26.08'],
    ['info', '--system', '--show-commit', 'org.freedesktop.Sdk//26.08'],
]
for arguments in commands:
    print('NATIVE_FLATPAK', ' '.join(arguments), flush=True)
    subprocess.run(base+arguments, check=True)
active = work/'sdk-store/runtime/org.freedesktop.Sdk/x86_64/26.08/active'
expected = 'a1b744b072d9f55d061e35382547ae80dad8d92abecc1da7dc1818de2daabfd3'
if active.resolve().name != expected:
    raise ValueError('SDK deployment changed; do not use a different source identity')
print('PINNED_SDK_READY', expected, flush=True)

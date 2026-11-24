"""Root-only native read queries through the private radio mount namespace.

No caller command, address, path, bus, environment or program is accepted.
The output comes from native interfaces/files, not the readiness report.
"""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

def inspect(arguments):
    if os.getuid() != 0 or os.geteuid() != 0:
        raise SystemExit('radio inspection requires an authorized root invocation')
    if arguments not in (['wifi'], ['bluetooth'], ['files']):
        raise SystemExit('usage: confos radio-inspect wifi|bluetooth|files')
    if Path('/proc/self/attr/current').read_text().strip() != 'unconfined':
        raise SystemExit('radio inspection requires the trusted confos entry')
    pid_text = Path('/run/confos-radio.pid').read_text().strip()
    if not pid_text.isascii() or not pid_text.isdecimal() or int(pid_text) < 2:
        raise RuntimeError('invalid radio supervisor identifier')
    process = Path('/proc')/pid_text
    if process.joinpath('attr/current').read_text().strip() != 'confos-radio (enforce)':
        raise RuntimeError('radio supervisor context differs')
    # Hold the namespace descriptor, so PID reuse cannot redirect setns later.
    descriptor = os.open(process/'ns/mnt', os.O_RDONLY | os.O_CLOEXEC)
    try:
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.setns(descriptor, 0x00020000) != 0:
            error = ctypes.get_errno()
            raise OSError(error, os.strerror(error))
    finally:
        os.close(descriptor)
    environment = {'PATH': '/usr/bin:/usr/sbin', 'HOME': '/root', 'LC_ALL': 'C'}
    if arguments == ['wifi']:
        commands = [
            ['/usr/sbin/iw', 'dev'],
            ['/usr/sbin/iw', 'dev', 'wlan1', 'link'],
            ['/usr/sbin/ip', '-j', 'addr', 'show', 'dev', 'wlan1'],
            ['/usr/sbin/ip', 'netns', 'exec', 'confos-radio-ap', '/usr/sbin/iw', 'dev'],
        ]
        results = []
        for command in commands:
            result = subprocess.run(command, env=environment, capture_output=True, text=True, timeout=10)
            results.append({'argv': command, 'exit': result.returncode,
                            'stdout': result.stdout, 'stderr': result.stderr})
        print(json.dumps(results, sort_keys=True))
    elif arguments == ['bluetooth']:
        # The trusted confos entry uses -IS; explicitly add only the immutable
        # distribution module directory, never caller-controlled site paths.
        sys.path.append('/usr/lib/python3/dist-packages')
        import dbus
        bus = dbus.bus.BusConnection('unix:path=/run/confos-radio/bus')
        bus.set_exit_on_disconnect(False)
        objects = dbus.Interface(bus.get_object('org.bluez', '/'),
                                 'org.freedesktop.DBus.ObjectManager').GetManagedObjects(timeout=10)
        print(json.dumps(objects, sort_keys=True))
    else:
        results = []
        for root in (Path('/run/confos-radio'), Path('/var/lib/bluetooth')):
            for path in [root, *sorted(root.rglob('*'))]:
                info = path.lstat()
                kind = ('file' if stat.S_ISREG(info.st_mode) else
                        'dir' if stat.S_ISDIR(info.st_mode) else
                        'symlink' if stat.S_ISLNK(info.st_mode) else
                        'socket' if stat.S_ISSOCK(info.st_mode) else 'other')
                results.append({'path': str(path), 'kind': kind,
                    'mode': format(stat.S_IMODE(info.st_mode), '04o'),
                    'uid': info.st_uid, 'gid': info.st_gid, 'size': info.st_size,
                    'target': os.readlink(path) if kind == 'symlink' else None,
                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest() if kind == 'file' else None})
        print(json.dumps(results, sort_keys=True))

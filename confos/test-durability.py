#!/usr/bin/python3
"""Builder power-cut/network regressions on a disposable released disk."""
import hashlib
import json
from pathlib import Path
import shutil
import socket
import subprocess
import time

HERE = Path(__file__).resolve().parent
VERSION = (HERE/'VERSION').read_text().strip()
IMAGE = HERE/'images/durability.qcow2'
UNIT = 'confos-durability-vm'
SERIAL = HERE/'logs/durability.serial'
QMP = Path(str(SERIAL)+'.qmp')

def guest(command, check=True):
    print('COMMAND:', command, flush=True)
    result = subprocess.run(['ssh', '-F', '/dev/null', '-o', 'StrictHostKeyChecking=no',
        '-o', 'UserKnownHostsFile=/dev/null', '-o', 'LogLevel=ERROR', '-o', 'ConnectTimeout=3',
        '-o', 'ServerAliveInterval=2', '-o', 'ServerAliveCountMax=3', '-i', 'private/login',
        '-p', '22406', 'user@127.0.0.1', command], text=True, capture_output=True)
    print(result.stdout, end='', flush=True)
    print(result.stderr, end='', flush=True)
    if check and result.returncode:
        raise RuntimeError('guest exit '+str(result.returncode))
    return result.stdout.strip()

def boot():
    subprocess.run(['systemd-run', '--user', '--unit='+UNIT, '--property=MemoryMax=4G',
        '--working-directory='+str(HERE), './boot.sh', str(IMAGE), '22406', '3072', str(SERIAL)], check=True)

def wait_ready(expected):
    for attempt in range(90):
        result = subprocess.run(['ssh', '-F', '/dev/null', '-o', 'StrictHostKeyChecking=no',
            '-o', 'UserKnownHostsFile=/dev/null', '-o', 'LogLevel=ERROR', '-o', 'ConnectTimeout=2',
            '-i', 'private/login', '-p', '22406', 'user@127.0.0.1', 'confos status'],
            capture_output=True, text=True, timeout=6)
        if result.returncode == 0 and result.stdout.strip() == 'APPLIED '+expected:
            print(result.stdout, end='', flush=True)
            return
        time.sleep(2)
    raise RuntimeError('readiness timeout')

def qmp(command, arguments=None):
    with socket.socket(socket.AF_UNIX) as client:
        client.connect(str(QMP))
        stream = client.makefile('rwb', buffering=0)
        json.loads(stream.readline())
        for obj in ({'execute': 'qmp_capabilities'}, {'execute': command, 'arguments': arguments or {}}):
            stream.write(json.dumps(obj).encode()+b'\n')
            while True:
                reply = json.loads(stream.readline())
                if 'error' in reply:
                    raise RuntimeError(reply)
                if 'return' in reply:
                    break
    print('QMP:', command, arguments, flush=True)

def stop():
    subprocess.run(['systemctl', '--user', 'stop', UNIT], check=False)

def main():
    if IMAGE.exists():
        raise RuntimeError('disposable image already exists')
    shutil.copyfile(HERE/f'images/confos-{VERSION}-clean.qcow2', IMAGE)
    original = (HERE/'examples/development.conf').read_bytes()
    try:
        boot()
        wait_ready(hashlib.sha256(original).hexdigest())
        for repetition in range(1, 4):
            for label, edit, check in (
                ('add', 'printf "package tree 2.2.1-1\\n" | sudo -n tee -a /state/declaration.conf',
                 '/usr/bin/tree --version'),
                ('change', 'sudo -n sed -i "s/^package tree 2.2.1-1$/package ed 1.21.1-1/" /state/declaration.conf',
                 'test ! -e /usr/bin/tree && /usr/bin/ed --version'),
                ('remove', 'sudo -n sed -i "/^package ed /d" /state/declaration.conf',
                 'test ! -e /usr/bin/tree && test ! -e /usr/bin/ed')):
                guest(edit)
                expected = guest('sha256sum /state/declaration.conf').split()[0]
                guest('sudo -n confos apply', check=False)
                wait_ready(expected)
                qmp('quit')
                stop()
                boot()
                wait_ready(expected)
                guest(check)
                print('PASS power cut', repetition, label, flush=True)
        guest('printf "package fonts-noto-cjk 1:20240730+repack1-1\\n" | sudo -n tee -a /state/declaration.conf')
        expected = guest('sha256sum /state/declaration.conf').split()[0]
        # Cut after the application enters its package acquisition phase, then
        # restore before the documented APT retry budget expires.
        with open(HERE/'logs/network-apply.log', 'w') as log:
            proc = subprocess.Popen(['ssh', '-F', '/dev/null', '-o', 'StrictHostKeyChecking=no',
                '-o', 'UserKnownHostsFile=/dev/null', '-o', 'LogLevel=ERROR',
                '-o', 'ServerAliveInterval=2', '-o', 'ServerAliveCountMax=20',
                '-i', 'private/login', '-p', '22406', 'user@127.0.0.1', 'sudo -n confos apply'],
                stdout=log, stderr=subprocess.STDOUT)
            try:
                for attempt in range(100):
                    if 'snapshot.debian.org' in (HERE/'logs/network-apply.log').read_text():
                        break
                    if proc.poll() is not None:
                        raise RuntimeError('apply ended before network cut')
                    time.sleep(0.1)
                else:
                    raise RuntimeError('package acquisition not observed')
                qmp('set_link', {'name': 'n', 'up': False})
                time.sleep(10)
                qmp('set_link', {'name': 'n', 'up': True})
                proc.wait(timeout=300)
            finally:
                if proc.poll() is None:
                    proc.terminate()
                    proc.wait(timeout=10)
        wait_ready(expected)
        guest("dpkg-query -W fonts-noto-cjk; test -s /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
        print('PASS installation after network loss and restoration', flush=True)
        print('DURABILITY PASS', flush=True)
    finally:
        stop()
        IMAGE.unlink(missing_ok=True)

if __name__ == '__main__':
    main()

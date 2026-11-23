#!/usr/bin/env python3
"""Disposable stand VM lifecycle; deploy beside base/ and keys/."""
import argparse
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import socket
import stat
import subprocess
import sys
import tarfile
import tempfile
import time

ROOT = Path(os.environ.get('STAND_ROOT', Path(__file__).resolve().parent)).resolve()

def call(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)

def save(path, data):
    tmp = path.with_suffix('.tmp')
    with tmp.open('w') as out:
        json.dump(data, out, indent=2)
        out.flush()
        os.fsync(out.fileno())
    tmp.replace(path)

def meta(vm):
    return json.loads((vm / 'meta.json').read_text())

def live(vm):
    try:
        pid = int((vm / 'qemu.pid').read_text())
        args = Path('/proc', str(pid), 'cmdline').read_bytes().split(b'\0')
        # Match the unique pidfile argument, not merely a process name or old PID.
        if os.fsencode(str(vm / 'qemu.pid')) not in args:
            return None
        if not any(b'qemu-system' in arg for arg in args[:1]):
            return None
        return pid
    except (OSError, ValueError):
        return None

def ssh(vm, root=False):
    info = meta(vm)
    key = (ROOT / info['key']).resolve()
    if not key.is_relative_to(ROOT):
        raise RuntimeError('key must be inside stand root')
    return ['ssh', '-F', '/dev/null', '-i', str(key), '-p', str(info['port']),
            '-o', 'BatchMode=yes', '-o', 'IdentitiesOnly=yes', '-o', 'StrictHostKeyChecking=no',
            '-o', 'UserKnownHostsFile=/dev/null', '-o', 'GlobalKnownHostsFile=/dev/null',
            '-o', 'LogLevel=ERROR', '-o', 'ConnectTimeout=3',
            (info.get('operator_user',info['user']) if root else info['user']) + '@127.0.0.1']

def ready(vm):
    deadline = time.monotonic() + int(os.environ.get('STAND_BOOT_TIMEOUT', '180'))
    while time.monotonic() < deadline:
        if live(vm):
            p = subprocess.run(ssh(vm, root=True) + ["if test -e /var/lib/stand/current; then sudo -n /usr/bin/systemctl is-active --quiet stand-replay.service || exit 1; fi; printf stand-ready"], stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            if p.returncode == 0 and p.stdout == b'stand-ready':
                return
        time.sleep(1)
    raise RuntimeError('SSH readiness timeout; inspect console.log and transient unit')

def start(vm):
    if live(vm):
        ready(vm)
        return
    info = meta(vm)
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        info['port'] = sock.getsockname()[1]
    info['unit'] = 'stand-' + hashlib.sha256(str(vm).encode()).hexdigest()[:16] + '-' + str(time.time_ns())
    save(vm / 'meta.json', info)
    for stale in ('qemu.pid', 'qmp.sock'):
        (vm / stale).unlink(missing_ok=True)
    slots = Path.home() / 'VMs/cal-1122/slots'
    slots.mkdir(parents=True, exist_ok=True)
    # The transient service owns flock and QEMU; no process belongs to this controller.
    # Each flock attempt is nonblocking. QEMU -pidfile records its own PID.
    cmd = ['qemu-system-x86_64', '-enable-kvm', '-m', '4096', '-smp', '2',
           '-display', 'none', '-monitor', 'none', '-serial', 'file:' + str(vm / 'console.log'),
           '-drive', 'file=' + str(vm / 'disk.qcow2') + ',format=qcow2,if=virtio',
           '-netdev', 'user,id=net0,hostfwd=tcp:127.0.0.1:' + str(info['port']) + '-:22',
           '-device', 'virtio-net-pci,netdev=net0,mac=<MAC>',
           '-qmp', 'unix:' + str(vm / 'qmp.sock') + ',server=on,wait=off',
           '-pidfile', str(vm / 'qemu.pid')] + info.get('qemu_args', [])
    # Exit 75 only for an occupied lock; other QEMU failures are not retried.
    launcher = 'for n in $(seq 1 12); do flock -n -E 75 "' + str(slots) + '/slot-$n.lock" ' + shlex.join(cmd) + '; r=$?; [ "$r" = 75 ] || exit "$r"; done; echo "all VM slots occupied" >&2; exit 75'
    call(['systemd-run', '--user', '--collect', '--unit=' + info['unit'],
          '--property=KillMode=control-group', '--property=TimeoutStopSec=120',
          '--property=MemoryMax=4608M', '--property=CPUQuota=200%',
          '--property=WorkingDirectory=' + str(ROOT),
          'sh', '-c', launcher], stdout=subprocess.DEVNULL)
    ready(vm)

def qmp(vm, command):
    with socket.socket(socket.AF_UNIX) as sock:
        sock.settimeout(10)
        sock.connect(str(vm / 'qmp.sock'))
        stream = sock.makefile('rwb')
        json.loads(stream.readline())
        for name in ('qmp_capabilities', command):
            stream.write((json.dumps({'execute': name}) + '\n').encode())
            stream.flush()
            while True:
                response = json.loads(stream.readline())
                if 'error' in response:
                    raise RuntimeError(str(response['error']))
                if 'return' in response:
                    break

def stop(vm):
    if not live(vm):
        return
    qmp(vm, 'system_powerdown')
    deadline = time.monotonic() + 120
    while live(vm) and time.monotonic() < deadline:
        time.sleep(0.5)
    if live(vm):
        raise RuntimeError('graceful shutdown timed out; no power cut performed')

@contextlib.contextmanager
def locked(name):
    (ROOT / 'locks').mkdir(parents=True, exist_ok=True)
    with (ROOT / 'locks' / (name + '.lock')).open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['new','run','start','stop','kill','destroy','copy-out','list'])
    parser.add_argument('name', nargs='?')
    parser.add_argument('args', nargs='*')
    parser.add_argument('--root', action='store_true')
    a = parser.parse_args()
    if a.command == 'list':
        for vm in sorted((ROOT / 'vms').glob('*')):
            if vm.is_dir():
                print(vm.name, 'running' if live(vm) else 'stopped')
        return
    if not a.name or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,47}', a.name):
        parser.error('a safe VM name is required')
    vm = ROOT / 'vms' / a.name
    with locked(a.name):
        if a.command == 'new':
            if a.args not in ([], ['stand']):
                parser.error('only system stand is supported')
            base = ROOT / 'base' / 'stand.qcow2'
            if base.stat().st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH):
                raise RuntimeError('base image must be read-only')
            info = json.loads((ROOT / 'base' / 'stand.json').read_text())
            if info.get('system') != 'stand' or info.get('transport') != 'ssh':
                raise RuntimeError('stand SSH base metadata required')
            info = {'system':'stand', 'transport':'ssh', 'user':info.get('user','stand'),
                    'key':info.get('key','keys/guest'), 'qemu_args':info.get('qemu_args', []), **({'operator_user':info['operator_user']} if 'operator_user' in info else {})}
            if not isinstance(info['qemu_args'], list) or not all(isinstance(x, str) for x in info['qemu_args']):
                raise RuntimeError('qemu_args must be an argument array')
            vm.mkdir(parents=True, exist_ok=False)
            save(vm / 'meta.json', info)
            call(['qemu-img','create','-f','qcow2','-F','qcow2','-b',str(base),str(vm / 'disk.qcow2')],stdout=subprocess.DEVNULL)
            start(vm)
            print('CREATED '+a.name+' system=stand')
        elif not vm.is_dir():
            raise RuntimeError('VM does not exist')
        elif a.command == 'start':
            start(vm)
        elif a.command == 'stop':
            stop(vm)
        elif a.command == 'kill':
            pid = live(vm)
            if pid:
                os.kill(pid, signal.SIGKILL)
                deadline = time.monotonic() + 10
                while live(vm) and time.monotonic() < deadline:
                    time.sleep(0.1)
                if live(vm):
                    raise RuntimeError('QEMU did not exit after SIGKILL')
        elif a.command == 'destroy':
            stop(vm)
            shutil.rmtree(vm)
        elif a.command == 'run':
            # The local controller receives the full script before invoking SSH.
            script = sys.stdin.buffer.read()
            interpreter = shlex.split(script.split(b'\n',1)[0][2:].decode()) if script.startswith(b'#!') else ['sh']
            if not interpreter:
                raise RuntimeError('empty shebang')
            remote = (['sudo','-n'] if a.root and not meta(vm).get('operator_user') else []) + interpreter
            result = subprocess.run(ssh(vm, root=a.root) + [shlex.join(remote)], input=script,
                                    timeout=int(os.environ.get('LAB_RUN_TIMEOUT','3600')))
            raise SystemExit(result.returncode)
        elif a.command == 'copy-out':
            if len(a.args) != 2:
                parser.error('copy-out requires guest path and host output directory')
            guest = Path(a.args[0])
            dest = Path(a.args[1]).resolve()
            if not dest.is_relative_to(ROOT):
                raise RuntimeError('copy-out destination must be inside stand root')
            dest.mkdir(parents=True, exist_ok=True)
            remote = ([] if meta(vm).get('operator_user') else ['sudo','-n']) + ['tar','-C',str(guest.parent),'-cf','-', '--',guest.name]
            with tempfile.TemporaryFile(dir=ROOT) as output:
                call(ssh(vm, root=True) + [shlex.join(remote)], stdout=output)
                output.seek(0)
                with tarfile.open(fileobj=output) as archive:
                    archive.extractall(dest, filter='data')

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print('stand lab:', str(error).replace(str(ROOT),'<stand-root>'), file=sys.stderr)
        raise SystemExit(1)

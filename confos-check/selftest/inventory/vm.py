#!/usr/bin/env python3
"""Throw-away virtual machines of a stock cloud image for the inventory self-test (runs on the server).

vm.py up NAME --stock IMAGE --slots DIR --work DIR     boot a fresh overlay under a free slot lock, wait for SSH
vm.py ssh NAME --work DIR -- CMD...                    run a command in the guest as the test account
vm.py down NAME --work DIR                             stop the machine and delete its overlay
"""
import argparse
import json
import os
import shlex
import signal
import socket
import subprocess
import sys
import time

USER = 'user'


def keypath(work):
    k = os.path.join(work, 'key')
    if not os.path.exists(k):
        subprocess.run(['ssh-keygen', '-q', '-t', 'ed25519', '-N', '', '-C', 'selftest', '-f', k], check=True)
    return k


def free_port(base):
    for p in range(base, base + 200):
        s = socket.socket()
        try:
            s.bind(('127.0.0.1', p))
            s.close()
            return p
        except OSError:
            s.close()
    raise RuntimeError('no free port')


def ssh_cmd(st, cmd):
    return ['ssh', '-i', st['key'], '-p', str(st['port']), '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=no',
            '-o', 'UserKnownHostsFile=/dev/null', '-o', 'LogLevel=ERROR', '-o', 'ConnectTimeout=10',
            f'{USER}@127.0.0.1', cmd]


def state(work, name):
    with open(os.path.join(work, name, 'state.json')) as f:
        return json.load(f)


def run_ssh(st, cmd, check=True, timeout=900):
    p = subprocess.run(ssh_cmd(st, cmd), capture_output=True, text=True, timeout=timeout)
    if check and p.returncode != 0:
        raise RuntimeError(f'guest command failed ({p.returncode}): {cmd}\n{p.stdout}\n{p.stderr}')
    return p


def up(name, stock, slots, work, mem=4096, cpus=2, wait_until=None):
    d = os.path.join(work, name)
    os.makedirs(d, exist_ok=True)
    key = keypath(work)
    pub = open(key + '.pub').read().strip()
    with open(os.path.join(d, 'user-data'), 'w') as f:
        f.write('#cloud-config\n'
                f'users:\n  - name: {USER}\n    sudo: "ALL=(ALL) NOPASSWD:ALL"\n    shell: /bin/bash\n'
                f'    lock_passwd: true\n    ssh_authorized_keys:\n      - {pub}\n'
                'ssh_pwauth: false\npackage_update: false\npackage_upgrade: false\n')
    with open(os.path.join(d, 'meta-data'), 'w') as f:
        f.write(f'instance-id: {name}\nlocal-hostname: casevm\n')
    seed = os.path.join(d, 'seed.img')
    subprocess.run(['cloud-localds', seed, os.path.join(d, 'user-data'), os.path.join(d, 'meta-data')], check=True)
    disk = os.path.join(d, 'disk.qcow2')
    if os.path.exists(disk):
        os.unlink(disk)
    subprocess.run(['qemu-img', 'create', '-q', '-f', 'qcow2', '-F', 'qcow2', '-b', os.path.abspath(stock), disk,
                    '8G'], check=True)
    os.makedirs(slots, exist_ok=True)
    for n in range(1, 7):
        port = free_port(22400 + 20 * n)
        lock = os.path.join(slots, f'slot-{n}.lock')
        pidf = os.path.join(d, 'qemu.pid')
        serial = os.path.join(d, 'serial.log')
        cmd = ['flock', '-n', '-E', '75', lock, 'qemu-system-x86_64', '-name', name, '-enable-kvm', '-cpu', 'host',
               '-m', str(mem), '-smp', str(cpus), '-drive', f'file={disk},if=virtio,format=qcow2',
               '-drive', f'file={seed},if=virtio,format=raw,readonly=on',
               '-nic', f'user,model=virtio-net-pci,hostfwd=tcp:127.0.0.1:{port}-:22',
               '-display', 'none', '-serial', f'file:{serial}', '-pidfile', pidf]
        p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=open(os.path.join(d, 'qemu.out'), 'w'),
                             stderr=subprocess.STDOUT, start_new_session=True)
        time.sleep(3)
        rc = p.poll()
        if rc == 75:
            continue
        if rc is not None:
            raise RuntimeError(f'qemu exited {rc}: ' + open(os.path.join(d, 'qemu.out')).read())
        st = {'name': name, 'slot': n, 'port': port, 'key': key, 'disk': disk, 'dir': d, 'flock_pid': p.pid,
              'user': USER}
        with open(os.path.join(d, 'state.json'), 'w') as f:
            json.dump(st, f)
        t0 = time.time()
        while time.time() - t0 < 600:
            if subprocess.run(ssh_cmd(st, 'true'), capture_output=True, timeout=30).returncode == 0:
                break
            time.sleep(3)
        else:
            raise RuntimeError('ssh did not come up')
        run_ssh(st, 'cloud-init status --wait >/dev/null; systemctl is-system-running --wait; true', timeout=900)
        print(f'vm {name}: slot {n}, port {port}, up after {time.time() - t0:.0f}s', flush=True)
        return st
    # no free slot now: wait for one (CASES_SLOT_WAIT seconds, default 7200), as the runner's machines do
    if wait_until is None:
        wait_until = time.time() + float(os.environ.get('CASES_SLOT_WAIT', '7200'))
    if time.time() < wait_until:
        time.sleep(30)
        return up(name, stock, slots, work, mem, cpus, wait_until)
    raise RuntimeError('no free slot')


def down(name, work):
    d = os.path.join(work, name)
    try:
        st = state(work, name)
    except OSError:
        st = None
    pidf = os.path.join(d, 'qemu.pid')
    if os.path.exists(pidf):
        try:
            pid = int(open(pidf).read().strip())
            os.kill(pid, signal.SIGTERM)
            for _ in range(30):
                os.kill(pid, 0)
                time.sleep(1)
            os.kill(pid, signal.SIGKILL)
        except (ProcessLookupError, ValueError):
            pass
    for f in ('disk.qcow2', 'seed.img', 'qemu.pid'):
        p = os.path.join(d, f)
        if os.path.exists(p):
            os.unlink(p)
    print(f'vm {name}: down', flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('action', choices=['up', 'down', 'ssh'])
    ap.add_argument('name')
    ap.add_argument('--stock')
    ap.add_argument('--slots')
    ap.add_argument('--work', required=True)
    ap.add_argument('cmd', nargs='*')
    a = ap.parse_args()
    if a.action == 'up':
        up(a.name, a.stock, a.slots, a.work)
    elif a.action == 'down':
        down(a.name, a.work)
    else:
        cmd = a.cmd[1:] if a.cmd and a.cmd[0] == '--' else a.cmd
        p = run_ssh(state(a.work, a.name), ' '.join(cmd), check=False)
        sys.stdout.write(p.stdout)
        sys.stderr.write(p.stderr)
        sys.exit(p.returncode)


if __name__ == '__main__':
    main()

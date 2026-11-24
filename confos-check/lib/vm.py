"""Virtual machines of the cases on the server: overlays, boot, SSH, QMP, power cut, cleanup.

Two kinds of machine:
- `confos`: booted with the builder's documented script `boot.sh DISK SSH_PORT MEMORY_MIB SERIAL_LOG QMP_SOCKET`
  (it takes one of the common slot locks itself and execs QEMU, so the process started is the QEMU process);
- `stock`: a stock Debian 13 cloud image booted by our own QEMU command under a slot lock of COMMON.md, with a
  NoCloud seed (only for testing the runner).
"""
import fcntl
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import socket
import subprocess
import threading
import time

from .common import Evidence, RunnerError, utc, load_env, home_path

ENV = load_env()
SLOTS_DIR = home_path(ENV.get('SLOTS_DIR', 'VMs/confos/slots'))
SSH_BASE = ['ssh', '-F', '/dev/null', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null',
            '-o', 'LogLevel=ERROR', '-o', 'ConnectTimeout=5', '-o', 'BatchMode=yes', '-o', 'IdentitiesOnly=yes',
            '-o', 'ServerAliveInterval=10', '-o', 'ServerAliveCountMax=30']
MARK = re.compile(rb'__CASES_EXIT=(\d+)')

# ---------------------------------------------------------------- registry and cleanup

_REGISTRY = set()
_REG_LOCK = threading.Lock()


def register(machine):
    with _REG_LOCK:
        _REGISTRY.add(machine)


def unregister(machine):
    with _REG_LOCK:
        _REGISTRY.discard(machine)


def cleanup_all():
    """Stop every machine this process started and delete its throw-away disks."""
    with _REG_LOCK:
        machines = list(_REGISTRY)
    for m in machines:
        try:
            m.destroy()
        except Exception:
            pass


# ---------------------------------------------------------------- ports and slots

_PORT_LOCK = threading.Lock()
_PORTS_USED = set()


def free_port():
    with _PORT_LOCK:
        for _ in range(200):
            s = socket.socket()
            s.bind(('127.0.0.1', 0))
            port = s.getsockname()[1]
            s.close()
            if port not in _PORTS_USED:
                _PORTS_USED.add(port)
                return port
    raise RunnerError('no free port')


def free_slots():
    """Number of the common slots that nobody holds right now (try each lock and release it)."""
    SLOTS_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    for slot in range(1, 7):
        with open(SLOTS_DIR / f'slot-{slot}.lock', 'a') as f:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                fcntl.flock(f, fcntl.LOCK_UN)
                n += 1
            except OSError:
                pass
    return n


def take_slot():
    """Take a free slot lock; returns (slot number, open file) or (None, None)."""
    SLOTS_DIR.mkdir(parents=True, exist_ok=True)
    for slot in range(1, 7):
        f = open(SLOTS_DIR / f'slot-{slot}.lock', 'a')
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return slot, f
        except OSError:
            f.close()
    return None, None


# ---------------------------------------------------------------- QMP

def qmp(sock_path, command, arguments=None, timeout=10):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect(str(sock_path))
    stream = s.makefile('rwb')

    def read_reply():
        while True:
            line = stream.readline()
            if not line:
                raise RunnerError('QMP connection closed')
            msg = json.loads(line)
            if 'return' in msg or 'error' in msg:
                return msg

    greeting = json.loads(stream.readline())
    stream.write(json.dumps({'execute': 'qmp_capabilities'}).encode() + b'\n')
    stream.flush()
    read_reply()
    body = {'execute': command}
    if arguments:
        body['arguments'] = arguments
    stream.write(json.dumps(body).encode() + b'\n')
    stream.flush()
    reply = read_reply()
    s.close()
    return greeting, reply


# ---------------------------------------------------------------- the machine

class Machine:
    """One virtual machine with its own work directory (overlay, serial logs, QMP socket)."""

    def __init__(self, kind, name, workdir, disk, key, user, evidence, memory=4096, source=None, seed=None,
                 slot_wait=None):
        self.kind = kind                  # 'confos' or 'stock'
        self.name = name
        self.dir = Path(workdir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.disk = Path(disk)
        self.key = str(key)
        self.user = user
        self.ev = evidence
        self.memory = memory
        self.source = Path(source) if source else None
        self.seed = seed
        # a machine waits for a free common slot (also at every restart); CASES_SLOT_WAIT seconds, default 1800
        self.slot_wait = slot_wait if slot_wait is not None else int(os.environ.get('CASES_SLOT_WAIT', '1800'))
        self.port = None
        self.proc = None
        self.slot_file = None
        self.boots = 0
        self.qmp_sock = self.dir / 'qmp.sock'
        self.netdev = 'n'                 # build/INTERFACE.md: "Network backend ID `n`"; the stock command uses the same
        self.lock = threading.Lock()
        register(self)

    # -- disks
    @staticmethod
    def overlay(base, path, ev):
        code, out, err = ev.host(['qemu-img', 'create', '-f', 'qcow2', '-F', 'qcow2', '-b', str(Path(base).resolve()),
                                  str(path)], timeout=120)
        if code:
            raise RunnerError('overlay could not be made: ' + err.decode(errors='replace'))
        return Path(path)

    # -- power
    def serial_log(self):
        return self.dir / f'serial-{self.boots}.log'

    def start(self):
        """Boot the disk. Waits for a free slot (never more machines than free slots)."""
        self.boots += 1
        if self.port is None:
            self.port = free_port()
        if self.qmp_sock.exists():
            self.qmp_sock.unlink()
        deadline = time.time() + self.slot_wait
        while True:
            if self.kind == 'confos':
                argv = [str(self.source / 'boot.sh'), str(self.disk), str(self.port), str(self.memory),
                        str(self.serial_log()), str(self.qmp_sock)]
                start = utc()
                errfile = open(self.dir / f'boot-{self.boots}.err', 'wb')
                self.proc = subprocess.Popen(argv, cwd=str(self.source), stdin=subprocess.DEVNULL,
                                             stdout=errfile, stderr=errfile, start_new_session=True)
                errfile.close()
            else:
                slot, f = take_slot()
                if slot is None:
                    if time.time() > deadline:
                        raise RunnerError('no free slot within the wait')
                    time.sleep(15)
                    continue
                self.slot_file = f
                argv = ['qemu-system-x86_64', '-enable-kvm', '-cpu', 'host', '-smp', '2', '-m', str(self.memory),
                        '-drive', f'file={self.disk},format=qcow2,if=virtio,cache=none',
                        '-drive', f'file={self.seed},format=raw,if=virtio,readonly=on',
                        '-netdev', f'user,id={self.netdev},hostfwd=tcp:127.0.0.1:{self.port}-:22',
                        '-device', f'virtio-net-pci,netdev={self.netdev}',
                        '-display', 'none', '-serial', f'file:{self.serial_log()}', '-monitor', 'none',
                        '-qmp', f'unix:{self.qmp_sock},server=on,wait=off']
                start = utc()
                errfile = open(self.dir / f'boot-{self.boots}.err', 'wb')
                self.proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=errfile, stderr=errfile,
                                             pass_fds=(f.fileno(),), start_new_session=True)
                errfile.close()
                f.close()            # QEMU holds the lock through the inherited descriptor
                self.slot_file = None
                argv = argv + [f'(slot {slot}, lock held by the QEMU process)']
            time.sleep(3)
            if self.proc.poll() is None:
                self.ev.record('H', argv, start, utc(), None, b'', b'',
                               {'pid': self.proc.pid, 'boot': self.boots, 'port': self.port})
                return
            err = (self.dir / f'boot-{self.boots}.err').read_bytes()
            self.ev.record('H', argv, start, utc(), self.proc.returncode, b'', err, {'boot': self.boots})
            if b'No VM slot available' in err and time.time() < deadline:
                time.sleep(15)
                continue
            if b'No VM slot available' in err:
                raise RunnerError('no free slot within the wait')
            raise BootFailed('the boot command exited: ' + err.decode(errors='replace')[-500:])

    def alive(self):
        return self.proc is not None and self.proc.poll() is None

    def qemu_pid(self):
        return self.proc.pid if self.proc else None

    def kill9(self):
        """Cut the power: SIGKILL of the QEMU process."""
        if not self.alive():
            return False
        start = utc()
        pid = self.proc.pid
        os.kill(pid, signal.SIGKILL)
        self.proc.wait()
        gone = not Path(f'/proc/{pid}').exists() or self.proc.poll() is not None
        self.ev.record('H', ['kill', '-9', str(pid)], start, utc(), 0, b'', b'',
                       {'qemu_exit': self.proc.returncode, 'gone': gone})
        return True

    def stop(self):
        if self.alive():
            try:
                os.kill(self.proc.pid, signal.SIGTERM)
                self.proc.wait(timeout=20)
            except Exception:
                try:
                    os.kill(self.proc.pid, signal.SIGKILL)
                    self.proc.wait(timeout=20)
                except Exception:
                    pass

    def destroy(self, keep_logs_in=None):
        """Stop the machine, keep the serial logs as evidence, delete the overlay and the work directory."""
        self.stop()
        keep = Path(keep_logs_in) if keep_logs_in else self.ev.dir
        try:
            for log in sorted(self.dir.glob('serial-*.log')) + sorted(self.dir.glob('boot-*.err')):
                shutil.copy2(log, keep / f'{self.name}-{log.name}')
        except Exception:
            pass
        shutil.rmtree(self.dir, ignore_errors=True)
        unregister(self)

    # -- link
    def set_link(self, up):
        start = utc()
        try:
            _, reply = qmp(self.qmp_sock, 'set_link', {'name': self.netdev, 'up': bool(up)})
        except Exception as e:
            self.ev.record('H', f'QMP set_link {self.netdev} up={up}', start, utc(), 1, b'', str(e).encode())
            raise RunnerError('QMP set_link failed: ' + str(e))
        ok = 'return' in reply
        self.ev.record('H', f'QMP set_link name={self.netdev} up={str(bool(up)).lower()}', start, utc(),
                       0 if ok else 1, json.dumps(reply).encode(), b'')
        if not ok:
            raise RunnerError('QMP set_link refused: ' + json.dumps(reply))

    # -- SSH
    def _ssh_argv(self, remote=None, user=None, key=None):
        argv = SSH_BASE + ['-i', key or self.key, '-p', str(self.port), f'{user or self.user}@127.0.0.1']
        if remote is not None:
            argv.append(remote)
        return argv

    def ssh(self, command, root=False, timeout=900, stdin=None, login=False, record=True, user=None, key=None,
            where=None):
        """Run CMD as the ordinary account (U:) or as root by the documented means `sudo -n` (R:).

        The remote side prints a marker with the exit status of CMD on stderr; when it has arrived the session is
        closed after a short grace even if a background process started by CMD still holds its output.
        Returns (exit, stdout, stderr). Exit 255 = the connection failed; 124 = timeout."""
        if login:
            script = (command + '\necho "__CASES_EXIT=$?" >&2\nexit\n').encode()
            argv = self._ssh_argv(None, user, key)
            stdin = script
        else:
            inner = command if not root else 'sudo -n bash -c ' + shlex.quote(command)
            remote = inner + '\necho "__CASES_EXIT=$?" >&2'
            argv = self._ssh_argv(remote, user, key)
        start = utc()
        p = subprocess.Popen(argv, stdin=subprocess.PIPE if stdin is not None else subprocess.DEVNULL,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        out, err = [], []
        marker = {}
        seen = threading.Event()

        def pump(stream, sink, watch):
            for chunk in iter(lambda: stream.readline(), b''):
                sink.append(chunk)
                if watch:
                    m = MARK.search(chunk)
                    if m:
                        marker['code'] = int(m.group(1))
                        seen.set()
            stream.close()

        threads = [threading.Thread(target=pump, args=(p.stdout, out, False), daemon=True),
                   threading.Thread(target=pump, args=(p.stderr, err, True), daemon=True)]
        for t in threads:
            t.start()
        if stdin is not None:
            try:
                p.stdin.write(stdin)
                p.stdin.close()
            except BrokenPipeError:
                pass
        deadline = time.time() + timeout
        timed_out = False
        held = False
        while p.poll() is None:
            if seen.is_set():
                try:
                    p.wait(timeout=4)
                except subprocess.TimeoutExpired:
                    held = True
                    p.kill()
                break
            if time.time() > deadline:
                timed_out = True
                p.kill()
                break
            time.sleep(0.1)
        p.wait()
        for t in threads:
            t.join(timeout=5)
        stdout = b''.join(out)
        stderr_raw = b''.join(err)
        stderr = MARK.sub(b'', stderr_raw).replace(b'\n\n', b'\n') if seen.is_set() else stderr_raw
        if 'code' in marker:
            code = marker['code']
        elif timed_out:
            code = 124
        else:
            code = p.returncode
        if record:
            extra = {'ssh_exit': p.returncode, 'marker': marker.get('code'), 'timed_out': timed_out,
                     'session_held_by_background_process': held}
            self.ev.record(where or ('R' if root else 'U'), command, start, utc(), code, stdout, stderr, extra)
        return code, stdout, stderr

    def u(self, command, **kw):
        return self.ssh(command, root=False, **kw)

    def r(self, command, **kw):
        return self.ssh(command, root=True, **kw)

    def boot_id(self, record=False):
        code, out, _ = self.ssh('cat /proc/sys/kernel/random/boot_id', timeout=20, record=record)
        return out.decode().strip() if code == 0 else None

    def wait_ssh(self, timeout=600, not_boot_id=None):
        """Wait until SSH answers (with a boot id other than NOT_BOOT_ID). Returns the boot id or None."""
        start = utc()
        deadline = time.time() + timeout
        tries = 0
        last = b''
        while time.time() < deadline:
            if not self.alive():
                self.ev.record('H', 'wait for SSH', start, utc(), 1, b'', b'the QEMU process ended\n' + last)
                return None
            tries += 1
            code, out, err = self.ssh('cat /proc/sys/kernel/random/boot_id', timeout=20, record=False)
            bid = out.decode().strip()
            if code == 0 and bid and bid != not_boot_id:
                self.ev.record('H', 'wait for SSH (boot id)', start, utc(), 0, out, b'',
                               {'tries': tries, 'not_boot_id': not_boot_id})
                return bid
            last = err[-300:]
            time.sleep(2)
        self.ev.record('H', 'wait for SSH (boot id)', start, utc(), 124, b'', last, {'tries': tries})
        return None

    def net_device(self):
        code, out, _ = self.u('ls /sys/class/net', record=True)
        devs = [d for d in out.decode().split() if d != 'lo']
        return devs[0] if devs else None

    def restart(self):
        """RESTART: `systemctl reboot` as root, wait for SSH, require a new boot id. Falls back to `reboot` if the
        system has no systemctl (both commands are in the evidence). Returns (old, new) boot ids."""
        old = self.boot_id(record=True)
        code, _, _ = self.r('systemctl reboot', timeout=30)
        new = self.wait_ssh(timeout=120 if code in (0, 255, None) else 5, not_boot_id=old)
        if new is None and self.alive():
            code, _, _ = self.r('reboot', timeout=30)
            new = self.wait_ssh(timeout=600 if code in (0, 255, None) else 60, not_boot_id=old)
        if new is None and self.alive():
            # No command of the system restarts it as root (both refused or without effect): the person presses
            # the reset button. `sync` first; a reset is harder on the system than an orderly restart.
            self.ev.note('restart: no restart command worked as root; sync, then the reset of the machine (QMP '
                         'system_reset)')
            self.r('sync', timeout=120)
            start = utc()
            try:
                _, reply = qmp(self.qmp_sock, 'system_reset')
                self.ev.record('H', 'QMP system_reset', start, utc(), 0 if 'return' in reply else 1,
                               json.dumps(reply).encode(), b'')
            except Exception as e:
                self.ev.record('H', 'QMP system_reset', start, utc(), 1, b'', str(e).encode())
            new = self.wait_ssh(timeout=600, not_boot_id=old)
        return old, new


class BootFailed(Exception):
    """The machine did not start (a failure of the implementation when it is a ConfOS machine)."""


def make_seed(directory, pubkey, instance, ev):
    """NoCloud seed for the stock image: the account `person`, its key, sudo without password."""
    directory = Path(directory)
    user_data = directory / 'user-data'
    meta = directory / 'meta-data'
    user_data.write_text('#cloud-config\nusers:\n  - name: person\n    shell: /bin/bash\n'
                         '    sudo: "ALL=(ALL) NOPASSWD:ALL"\n    groups: [sudo]\n'
                         f'    ssh_authorized_keys:\n      - {pubkey.strip()}\nssh_pwauth: false\n'
                         'package_update: false\npackage_upgrade: false\n')
    meta.write_text(f'instance-id: cases-{instance}\nlocal-hostname: stock\n')
    seed = directory / 'seed.img'
    code, out, err = ev.host(['cloud-localds', str(seed), str(user_data), str(meta)], timeout=60)
    if code:
        raise RunnerError('cloud-localds failed: ' + err.decode(errors='replace'))
    return seed

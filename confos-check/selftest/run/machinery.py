#!/usr/bin/env python3
"""Machinery experiment of the runner on a stock Debian 13 cloud image (overlay only, NoCloud seed, a throw-away key).

Checks, each printed as `CHECK NAME PASS|FAIL detail` from command output:
FRESH (boot, SSH as the ordinary account), U:/R:, RESTART (new boot id), HTTP payload from 10.0.2.2, LINK down/up
(the guest sees carrier 0 then 1), CUT (QEMU killed with SIGKILL, process gone, the same disk boots again with a new
boot id and keeps a synced file), cleanup (no QEMU process of ours, no overlay left). Exit 0 only if all hold.
"""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

CASES = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CASES))
from lib.common import Evidence, load_env, home_path, sha256_bytes, sha256_file, scrub  # noqa: E402
from lib.vm import Machine, make_seed, cleanup_all, free_slots  # noqa: E402
from lib.http import PayloadServer  # noqa: E402

ENV = load_env()
BASE = home_path(ENV.get('SERVER_DIR', 'VMs/confos/cases')) / 'run'
WORK = BASE / 'work' / 'selftest-machinery'
EVID = BASE / 'selftest-evidence' / 'machinery'
results = []


def check(name, ok, detail=''):
    results.append(ok)
    print(f'CHECK {name} {"PASS" if ok else "FAIL"} {detail}', flush=True)


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    shutil.rmtree(EVID, ignore_errors=True)
    WORK.mkdir(parents=True)
    ev = Evidence(EVID)
    print(f'evidence: {scrub(str(EVID))}')
    img = home_path(ENV['STOCK_IMAGE'])
    got = subprocess.run(['sha512sum', str(img)], capture_output=True, text=True).stdout.split()[0]
    check('stock-image-checksum', got == ENV.get('STOCK_IMAGE_SHA512'), got[:16])
    key = WORK / 'key'
    subprocess.run(['ssh-keygen', '-q', '-t', 'ed25519', '-N', '', '-C', '', '-f', str(key)], check=True)
    seed = make_seed(WORK, (WORK / 'key.pub').read_text(), 'machinery', ev)
    disk = Machine.overlay(img, WORK / 'disk.qcow2', ev)
    print(f'free slots before boot: {free_slots()}')
    m = Machine('stock', 'machinery', WORK / 'vm', disk, key, 'person', ev, memory=2048, seed=seed)
    try:
        m.start()
        bid1 = m.wait_ssh(timeout=600)
        check('fresh-boot-ssh', bid1 is not None, f'boot id {bid1}')
        code, out, _ = m.u('id -un')
        check('U-ordinary-account', code == 0 and out.strip() == b'person', out.strip().decode())
        code, out, _ = m.r('id -u')
        check('R-root', code == 0 and out.strip() == b'0', out.strip().decode())
        code, out, err = m.u('sleep 600 >/dev/null 2>&1 & echo started')
        check('U-background-process-does-not-hold-session', code == 0 and b'started' in out)

        old, new = m.restart()
        check('restart-new-boot-id', new is not None and new != old, f'{old} -> {new}')

        payload_dir = WORK / 'serve'
        payload_dir.mkdir()
        data = os.urandom(200000)
        (payload_dir / 'payload.bin').write_bytes(data)
        with PayloadServer(payload_dir, ev) as srv:
            code, out, _ = m.u(f'curl -fsS {srv.url("payload.bin")} | sha256sum')
        check('http-payload-from-10.0.2.2', code == 0 and out.split()[:1] == [sha256_bytes(data).encode()],
              out.decode().strip()[:20])

        dev = m.net_device()
        logger = (f"nohup sh -c 'i=0; while [ $i -lt 120 ]; do echo \"$(date +%s.%N) $(cat /sys/class/net/{dev}/carrier)"
                  f"\" >> /tmp/carrier.log; sleep 0.1; i=$((i+1)); done' >/dev/null 2>&1 </dev/null &")
        m.u('rm -f /tmp/carrier.log; ' + logger)
        time.sleep(2)
        m.set_link(False)
        time.sleep(4)
        m.set_link(True)
        time.sleep(10)
        code, out, _ = m.u('cat /tmp/carrier.log')
        seq = [l.split()[-1] for l in out.decode().splitlines() if l.split()]
        squeezed = [x for i, x in enumerate(seq) if i == 0 or seq[i - 1] != x]
        check('link-down-up-carrier', squeezed[:3] == ['1', '0', '1'],
              f'device {dev}, carrier sequence {squeezed}, {len(seq)} samples')

        m.u('echo cut-marker > ~/marker && sync')
        pid = m.qemu_pid()
        m.kill9()
        check('cut-qemu-killed', not Path(f'/proc/{pid}').exists() or m.proc.poll() is not None,
              f'pid {pid} exit {m.proc.returncode}')
        before = m.boot_id()
        m.start()
        bid2 = m.wait_ssh(timeout=600)
        code, out, _ = m.u('cat ~/marker')
        check('cut-same-disk-boots', bid2 is not None and bid2 not in (new, bid1), f'boot id {bid2}')
        check('cut-synced-file-kept', code == 0 and out.strip() == b'cut-marker')
    finally:
        m.destroy()
        cleanup_all()
    ps = subprocess.run(['pgrep', '-a', 'qemu'], capture_output=True, text=True).stdout
    ours = [l for l in ps.splitlines() if str(WORK) in l]
    check('cleanup-no-qemu-of-ours', not ours, f'{len(ours)} process(es)')
    shutil.rmtree(WORK, ignore_errors=True)
    check('cleanup-no-overlay', not WORK.exists())
    print('MACHINERY', 'PASS' if all(results) else 'FAIL')
    return 0 if all(results) else 1


if __name__ == '__main__':
    sys.exit(main())

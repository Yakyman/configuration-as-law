#!/usr/bin/env python3
"""Planted-object test of `inventory` and `compare --baseline` (runs on the server).

1. Boot a fresh overlay of the stock Debian 13 cloud image; install nftables if the image lacks it.
2. Inventory A; wait; inventory B of the untouched machine; compare B with A: must report nothing.
3. Plant known objects; inventory C; compare C with B: must report every planted object and nothing else.
4. Compare C with B again with --questions (the four questions of S8.2-6 for the writable area): the enabled unit is
   reported through question 3, the plain note is decided by question 4, home executables without routes are UNROUTED.
Prints PASS/FAIL per planted object and per check; exit 0 only if all pass. The machine and its overlay are
removed at the end, also on failure.

test.py --stock IMAGE --slots DIR [--work DIR] [--out DIR]
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
import vm  # noqa: E402

INVENTORY = os.path.join(CASES, 'inventory')
COMPARE = os.path.join(CASES, 'compare')
DECIDE = os.path.join(CASES, 'decide.tsv')
H = '/home/user'


def pub(s):
    """Published output names no path of the server: paths are given relative to the cases folder."""
    s = s.replace(CASES + '/', '')
    return s.replace(os.path.expanduser('~'), '~')


def say(msg):
    print(time.strftime('%H:%M:%SZ', time.gmtime()) + ' ' + pub(msg), flush=True)


def inventory(st, out):
    t0 = time.time()
    p = subprocess.run([sys.executable, INVENTORY, '--disk', st['disk'], '--ssh-port', str(st['port']),
                        '--ssh-key', st['key'], '--user', st['user'], '--root-cmd', 'sudo -n', '--out', out],
                       capture_output=True, text=True)
    say(f'inventory {os.path.basename(out)}: exit {p.returncode} in {time.time() - t0:.0f}s')
    sys.stdout.write(''.join('    ' + pub(l) + '\n' for l in p.stderr.splitlines()))
    if p.returncode != 0:
        raise RuntimeError('inventory failed')
    errs = [json.loads(l) for f in ('stored.jsonl', 'force.jsonl') for l in open(os.path.join(out, f))
            if '"kind": "error"' in l]
    for e in errs:
        say(f'    inventory error object: {e["id"]}: {str(e.get("detail"))[:200]}')
    return errs


def compare(cur, base, out):
    p = subprocess.run([sys.executable, COMPARE, '--inventory', cur, '--baseline', base, '--decide', DECIDE,
                        '--out', out], capture_output=True, text=True)
    say(f'compare {os.path.basename(out)}: exit {p.returncode}: {p.stderr.strip()}')
    if p.returncode == 2:
        raise RuntimeError('compare error')
    rows = []
    for line in open(out, encoding='utf-8'):
        f = line.rstrip('\n').split('\t')
        rows.append((f[0], f[1], f[2], f[3] if len(f) > 3 else ''))
    return p.returncode, rows


# Each planted object: the action, the lines it must produce (required) and the lines its action may also produce
# (allowed: direct consequences of the same action). A line is (VERDICT, KIND, ID-regex).
def planted(img_name):
    q = re.escape
    return [
        {'name': 'file outside every package',
         'do': ["printf 'planted note\\n' | sudo -n tee /usr/local/share/planted-note.txt >/dev/null"],
         'required': [('UNRECORDED', 'file', q('/usr/local/share/planted-note.txt'))],
         'allowed': []},
        {'name': 'changed file of a package (/etc/issue of base-files)',
         'pre': 'dpkg-query -S /etc/issue',
         'do': ["printf 'planted line\\n' | sudo -n tee -a /etc/issue >/dev/null"],
         'required': [('DIFFERS', 'file', q('/etc/issue'))],
         'allowed': []},
        {'name': 'added account',
         'do': ['sudo -n useradd -m -d /srv/planted -s /bin/bash planted'],
         'required': [('UNRECORDED', 'account', 'planted'), ('UNRECORDED', 'group', 'planted'),
                      ('UNRECORDED', 'shadow', 'planted'), ('UNRECORDED', 'dir', q('/srv/planted')),
                      ('DIFFERS', 'file', '/etc/(passwd|group|shadow|gshadow)')],
         'allowed': [('UNRECORDED', 'access', q('sudo-l/planted')),
                     ('UNRECORDED|DIFFERS', 'file', '/etc/(passwd|group|shadow|gshadow|subuid|subgid)-?'),
                     ('UNRECORDED', 'file', q('/srv/planted/') + r'\.(bashrc|profile|bash_logout)')]},
        {'name': 'enabled unit',
         'do': ["printf '[Unit]\\nDescription=planted\\n[Service]\\nExecStart=/usr/bin/sleep 86401\\n"
                "[Install]\\nWantedBy=multi-user.target\\n' | sudo -n tee /etc/systemd/system/planted.service"
                " >/dev/null",
                'sudo -n systemctl daemon-reload', 'sudo -n systemctl enable --now planted.service'],
         'required': [('UNRECORDED', 'unit', q('system/planted.service')),
                      ('UNRECORDED', 'file', q('/etc/systemd/system/planted.service')),
                      ('UNRECORDED', 'symlink', q('/etc/systemd/system/multi-user.target.wants/planted.service'))],
         'allowed': []},
        {'name': 'firewall rule',
         'do': ['sudo -n nft add table inet planted',
                "sudo -n nft add chain inet planted input '{ type filter hook input priority 0; policy accept; }'",
                'sudo -n nft add rule inet planted input tcp dport 8099 accept'],
         'required': [('UNRECORDED', 'firewall', q('nft/rule inet planted/input/') + '.*8099.*')],
         'allowed': [('UNRECORDED', 'firewall', q('nft/table inet planted')),
                     ('UNRECORDED', 'firewall', q('nft/chain inet planted/input'))]},
        {'name': 'executable in the home directory',
         'do': [f"printf '#!/bin/sh\\necho planted\\n' > {H}/planted-tool.sh", f'chmod 0755 {H}/planted-tool.sh'],
         'required': [('UNRECORDED', 'file', q(f'{H}/planted-tool.sh'))],
         'allowed': []},
        {'name': 'running program from the home directory',
         'do': [f'cp /usr/bin/sleep {H}/planted-sleep',
                f'setsid -f {H}/planted-sleep 86402 </dev/null >/dev/null 2>&1'],
         'required': [('UNRECORDED', 'file', q(f'{H}/planted-sleep')),
                      ('UNRECORDED', 'process', q(f'{H}/planted-sleep'))],
         # the login session that started it stays while it runs; its scope is decided with its members
         'allowed': [('UNRECORDED', 'unit', r'system/session-\d+\.scope')]},
        {'name': 'file on a volatile filesystem',
         'do': ["printf 'planted volatile\\n' > /dev/shm/planted-volatile.txt"],
         'required': [('UNRECORDED', 'vfile', q('/dev/shm/planted-volatile.txt'))],
         'allowed': []},
        {'name': 'filesystem image with an executable inside, loop-mounted',
         'host': img_name,
         'do': [f'sudo -n mount -o loop,ro {H}/planted.sqfs /mnt'],
         'required': [('UNRECORDED', 'file', q(f'{H}/planted.sqfs')),
                      ('UNRECORDED', 'file', q(f'{H}/planted.sqfs!/bin/planted-in-image.sh')),
                      ('UNRECORDED', 'mount', q('/mnt'))],
         'allowed': [('UNRECORDED', 'dir', q(f'{H}/planted.sqfs!/') + '(bin)?'),
                     ('UNRECORDED', 'file', q(f'{H}/planted.sqfs!/data.txt')),
                     ('UNRECORDED', 'module', '(squashfs|loop)'),
                     # the service managers' units for the new loop devices and the new mount point
                     ('UNRECORDED', 'unit', r'(system|user/user)/(mnt\.mount|blockdev@dev-loop\d+\.target|'
                                            r'dev-loop\d+\.device|sys-devices-virtual-block-loop\d+\.device|'
                                            r'dev-disk-by\\x2d(diskseq-\d+|loop\\x2d\S+)\.device)')],
         'check_runtime': (f'{H}/planted.sqfs!/bin/planted-in-image.sh', '/mnt/bin/planted-in-image.sh')},
    ]


def match(row, spec):
    v, k, i = spec
    return re.fullmatch(v, row[0]) and k == row[1] and re.fullmatch(i, row[2])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stock', required=True)
    ap.add_argument('--slots', required=True)
    ap.add_argument('--work', default=os.path.join(CASES, 'work'))
    ap.add_argument('--out', default=os.path.join(HERE, 'out'))
    ap.add_argument('--wait', type=int, default=180, help='seconds between the two untouched inventories')
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    os.makedirs(a.out, exist_ok=True)
    for fn in ('untouched-compare.tsv', 'untouched-compare-excluded.tsv', 'planted-compare.tsv',
               'planted-compare-excluded.tsv', 'inventory-A-meta.json', 'inventory-B-meta.json',
               'inventory-C-meta.json'):
        if os.path.exists(os.path.join(a.out, fn)):
            os.unlink(os.path.join(a.out, fn))
    name ='invtest-' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    inv = {t: os.path.join(a.work, name, 'inv-' + t) for t in 'ABC'}
    results = []
    st = None
    try:
        say(f'stock image {os.path.basename(a.stock)}; machine {name}')
        st = vm.up(name, a.stock, a.slots, a.work)
        r = vm.run_ssh(st, 'command -v nft || test -x /usr/sbin/nft', check=False)
        if r.returncode != 0:
            say('the image lacks nftables: installing it before the baseline')
            vm.run_ssh(st, 'sudo -n env DEBIAN_FRONTEND=noninteractive apt-get -q update >/dev/null && '
                           'sudo -n env DEBIAN_FRONTEND=noninteractive apt-get -q -y install nftables >/dev/null',
                       timeout=900)
        say(vm.run_ssh(st, '/usr/sbin/nft --version; cat /etc/debian_version; uname -r').stdout.strip())
        # the untouched comparison needs a machine that does not change itself: wait until boot has finished and
        # no job is queued and no unit is activating for 30 s in a row (first-boot jobs of the stock image, e.g.
        # apt-listchanges disabling its own timer, made the run of 2026-11-24 04:55 report 3 lines)
        vm.run_ssh(st, 'systemctl is-system-running --wait', check=False, timeout=900)
        quiet, t0 = 0, time.time()
        while quiet < 3 and time.time() - t0 < 1200:
            r = vm.run_ssh(st, 'systemctl list-jobs --no-legend; systemctl list-units --state=activating,deactivating '
                               '--no-legend --plain; now=$(date +%s); systemctl list-timers --all --output=json | '
                               'python3 -c "import json,sys; n=int(sys.argv[1])*10**6; [print(\'timer due:\', t[\'unit\']) '
                               'for t in json.load(sys.stdin) if t.get(\'next\') and 0 < t[\'next\'] - n < 600*10**6]" $now',
                           check=False)
            quiet = quiet + 1 if not r.stdout.strip() else 0
            if r.stdout.strip():
                say('not settled: ' + ' | '.join(r.stdout.strip().splitlines()[:5]))
            time.sleep(10)
        say(f'settled after {time.time() - t0:.0f}s' if quiet >= 3 else 'did not settle within 1200s')
        inventory(st, inv['A'])
        say(f'untouched machine: waiting {a.wait}s')
        time.sleep(a.wait)
        inventory(st, inv['B'])
        rc, rows = compare(inv['B'], inv['A'], os.path.join(a.out, 'untouched-compare.tsv'))
        for row in rows:
            say('    untouched: ' + '\t'.join(row)[:300])
        ok = rc == 0 and not rows
        results.append(('untouched machine: compare --baseline reports nothing', ok,
                        f'{len(rows)} lines'))

        # plant
        img_dir = os.path.join(a.work, name, 'img')
        os.makedirs(os.path.join(img_dir, 'bin'))
        with open(os.path.join(img_dir, 'bin', 'planted-in-image.sh'), 'w') as f:
            f.write('#!/bin/sh\necho planted in image\n')
        os.chmod(os.path.join(img_dir, 'bin', 'planted-in-image.sh'), 0o755)
        with open(os.path.join(img_dir, 'data.txt'), 'w') as f:
            f.write('planted data\n')
        sq = os.path.join(a.work, name, 'planted.sqfs')
        subprocess.run(['mksquashfs', img_dir, sq, '-quiet', '-noappend', '-all-root'], check=True)
        objs = planted(sq)
        for o in objs:
            if o.get('pre'):
                r = vm.run_ssh(st, o['pre'], check=False)
                say(f'precondition of "{o["name"]}": {o["pre"]} -> {r.stdout.strip()} (exit {r.returncode})')
            if o.get('host'):
                subprocess.run(['scp', '-q', '-i', st['key'], '-P', str(st['port']), '-o', 'BatchMode=yes',
                                '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null',
                                '-o', 'LogLevel=ERROR', o['host'], f'user@127.0.0.1:{H}/planted.sqfs'], check=True)
            for cmd in o['do']:
                vm.run_ssh(st, cmd)
            say(f'planted: {o["name"]}')
        time.sleep(10)
        inventory(st, inv['C'])
        rc, rows = compare(inv['C'], inv['B'], os.path.join(a.out, 'planted-compare.tsv'))
        used = set()
        for o in objs:
            missing = [s for s in o['required'] if not any(match(r, s) for r in rows)]
            for i, r in enumerate(rows):
                if any(match(r, s) for s in o['required'] + o['allowed']):
                    used.add(i)
            detail = 'all required lines present' if not missing else 'missing ' + '; '.join(' '.join(m) for m in missing)
            ok = not missing
            if o.get('check_runtime'):
                oid, rt = o['check_runtime']
                found = [json.loads(l) for l in open(os.path.join(inv['C'], 'stored.jsonl')) if oid in l]
                found = [x for x in found if x['id'] == oid]
                rok = bool(found) and rt in (found[0].get('runtime') or [])
                ok = ok and rok
                detail += f'; runtime path of {oid}: {found[0].get("runtime") if found else None}'
            results.append((f'planted: {o["name"]}', ok, detail))
        extra = [r for i, r in enumerate(rows) if i not in used]
        for r in extra:
            say('    not planted: ' + '\t'.join(r)[:300])
        results.append(('planted machine: nothing reported that was not planted', not extra, f'{len(extra)} lines'))
        ex = os.path.join(a.out, 'planted-compare-excluded.tsv')
        n_ex = sum(1 for _ in open(ex))
        say(f'excluded by decide.tsv (kept in {os.path.basename(ex)}): {n_ex} objects')
        # executables are never excluded
        execs = set()
        for t in 'BC':
            for l in open(os.path.join(inv[t], 'executables.jsonl')):
                o = json.loads(l)
                execs.add((o['kind'], o['id']))
        bad = []
        for fn in ('untouched-compare-excluded.tsv', 'planted-compare-excluded.tsv'):
            for l in open(os.path.join(a.out, fn), encoding='utf-8'):
                f = l.split('\t')
                if (f[0], f[1]) in execs:
                    bad.append(l)
        for l in bad:
            say('    executable excluded: ' + l.strip()[:300])
        results.append(('no executable object excluded', not bad, f'{len(bad)} lines'))
        # [n3-A] on a machine where the person can put a setting in force: the same two inventories
        # compared with --questions (the whole stock disk is writable). The enabled unit and its symlink must be
        # reported through question 3 (the service manager loaded it), the plain note must be decided by question 4
        # (excluded, rule four-questions), the executables in the home directory (no routes in this test) must be
        # UNROUTED, and the running program from the home directory must stay reported.
        qout = os.path.join(a.out, 'planted-compare-questions.tsv')
        p = subprocess.run([sys.executable, COMPARE, '--inventory', inv['C'], '--baseline', inv['B'], '--decide',
                            DECIDE, '--questions', '--out', qout], capture_output=True, text=True)
        say(f'compare --questions: exit {p.returncode}: {p.stderr.strip()}')
        qrows = [l.rstrip('\n').split('\t') for l in open(qout, encoding='utf-8')]
        qex = [l.rstrip('\n').split('\t') for l in open(qout[:-4] + '-excluded.tsv', encoding='utf-8')]

        def qhas(rows_, verdict, kind, rid, text):
            return any(r[0] == verdict and r[1] == kind and re.fullmatch(rid, r[2]) and text in '\t'.join(r[3:])
                       for r in rows_)
        q = re.escape
        for qname, ok in (
                ('unit file in force by question 3',
                 qhas(qrows, 'UNRECORDED', 'file', q('/etc/systemd/system/planted.service'), 'question 3')),
                ('enabling symlink in force by question 3',
                 qhas(qrows, 'UNRECORDED', 'symlink', q('/etc/systemd/system/multi-user.target.wants/planted.service'),
                      'question 3')),
                ('plain note decided by question 4', any(r[1] == '/usr/local/share/planted-note.txt'
                                                         and 'four-questions' in '\t'.join(r) for r in qex)),
                ('executable in the home directory UNROUTED',
                 qhas(qrows, 'UNROUTED', 'file', q(f'{H}/planted-tool.sh'), 'question 2')),
                ('running program from the home directory still reported',
                 qhas(qrows, 'UNRECORDED', 'process', q(f'{H}/planted-sleep'), ''))):
            results.append((f'questions: {qname}', ok, 'planted-compare-questions.tsv'))
        for t in 'ABC':
            m = [json.loads(l) for l in open(os.path.join(inv[t], 'force.jsonl')) if '"kind": "meta"' in l][0]
            with open(os.path.join(a.out, f'inventory-{t}-meta.json'), 'w') as f:
                json.dump(m, f, indent=1, sort_keys=True)
    except Exception as e:
        results.append(('test ran to the end', False, f'{type(e).__name__}: {e}'))
    finally:
        if st:
            vm.down(name, a.work)
        shutil.rmtree(os.path.join(a.work, name), ignore_errors=True)
        say(f'removed machine {name}, its overlay and its inventories')
    print()
    for n, ok, d in results:
        print(pub(f'{"PASS" if ok else "FAIL"}  {n}  ({d})'))
    allok = bool(results) and all(ok for _, ok, _ in results)
    print('RESULT: ' + ('PASS' if allok else 'FAIL'))
    return 0 if allok else 1


if __name__ == '__main__':
    sys.exit(main())

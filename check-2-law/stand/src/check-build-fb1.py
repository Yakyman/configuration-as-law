#!/usr/bin/env python3
"""VM-only supplementary Check 2: compiler denial, successful build exception,
then revocation of both compiler and the resulting executable. No hypothesis verdict.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

assert os.geteuid() == 0 and Path('/run/cal.sock').exists(), 'disposable stand VM only'
root = Path('/etc/cal/root.json')
base = dict(archive='keep', programs={}, policies={}, allow_channels={}, shared={})
failures = []

def snapshot():
    binary = Path('/home/alice/built')
    return dict(root=json.loads(root.read_text()),
                current_sha256=hashlib.sha256(Path('/var/lib/cal/current.json').read_bytes()).hexdigest(),
                binary=None if not binary.exists() else dict(sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),
                    mode=oct(binary.stat().st_mode), uid=binary.stat().st_uid, gid=binary.stat().st_gid, inode=binary.stat().st_ino))

def run(label, command, user='alice', rc=0, contains=None, predicate=None):
    argv=['runuser','-u',user,'--','/usr/local/bin/cal-login','-c',command] if user!='root' else ['/bin/bash','-c',command]
    before=snapshot()
    p=subprocess.run(argv,capture_output=True,text=True,timeout=180)
    checks=dict(returncode=p.returncode==rc, output=contains is None or contains in p.stdout)
    if predicate is not None: checks['state']=bool(predicate())
    if not all(checks.values()): failures.append(label)
    print(json.dumps(dict(event=label, utc=time.strftime('%FT%TZ', time.gmtime()), command=argv,
        expected_rc=rc, returncode=p.returncode, stdout=p.stdout, stderr=p.stderr,
        assertions=checks,before=before,after=snapshot())),flush=True)
    return all(checks.values())

def apply(doc,label):
    root.write_text(json.dumps(doc))
    if not run(label,'calctl apply',user='root'): raise RuntimeError(label)

for user in ('alice','bob'):
    (Path('/home')/user/'declaration.json').write_text('{"programs":{}}\n')
apply(base,'empty-no-exceptions')
run('source-and-identity', 'set -e; id; cat /proc/self/attr/current; rm -f "$HOME/built"; printf \'#include <stdio.h>\nint main(void){puts("BUILT_BY_ALICE");return 0;}\n\' > "$HOME/probe.c"; cat "$HOME/probe.c"')
run('compiler-denied-no-artifact','gcc "$HOME/probe.c" -o "$HOME/built"',rc=126,predicate=lambda:not Path('/home/alice/built').exists())
apply({**base,'allow_channels':{'alice':['build']}},'allow-build')
built=run('allowed-compile-and-launch','set -e; gcc "$HOME/probe.c" -o "$HOME/built"; "$HOME/built"',contains='BUILT_BY_ALICE',predicate=lambda:Path('/home/alice/built').exists())
apply(base,'revoke-build')
if built:
    fingerprint=snapshot()['binary']
    run('compiled-artifact-launch-denied','"$HOME/built"',rc=126,predicate=lambda:snapshot()['binary']==fingerprint)
    run('compiler-denied-after-revocation','gcc "$HOME/probe.c" -o "$HOME/built-again"',rc=126,predicate=lambda:not Path('/home/alice/built-again').exists())
run('audit', "journalctl -k --no-pager | grep -E 'apparmor=|DENIED'",user='root')
print(json.dumps(dict(event='SUMMARY',failures=failures,failure_count=len(failures),note='Mechanism assertions only; Check 2 remains incomplete.')),flush=True)
raise SystemExit(bool(failures))

#!/usr/bin/env python3
"""[x1] Test of the repair of run-extra: the effect of an X-REC step is judged as p4_decide of the frozen `run` judges
the effect of an attempt. With the effects recorded in dev-15-extra (X-REC-PODMAN steps 3 and 5) and dev-16-new
(P4-S-054): step 3 (two `error` objects, UNRECORDED) → fail; step 5 (two objects whose route was not taken,
UNROUTED) → unobserved, not fail; the QUESTION objects → undecided, not fail. Before the repair run-extra appended
every non-empty effect to the failures (it has no judge_effect): the test fails there.
usage: check-judge-effect.py RUN_EXTRA FIXTURE_DIR"""
import importlib.machinery
import importlib.util
import sys
from pathlib import Path

prog, fx = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
sys.path.insert(0, str(prog.parent))
sys.argv = [str(prog)]
loader = importlib.machinery.SourceFileLoader('runextra', str(prog))
spec = importlib.util.spec_from_loader('runextra', loader)
mod = importlib.util.module_from_spec(spec)
loader.exec_module(mod)


def rows(name):
    return [l.split('\t') for l in (fx / name).read_text().splitlines() if l.strip()]


class Stub:
    xrec = {}


ok = True
judge = getattr(mod.XCtx, 'judge_effect', None)
if judge is None:
    print('CHECK judge-effect-exists FAIL run-extra has no judge_effect: every non-empty effect is a failure')
    ok = False
else:
    for name, want in (('podman-3-attempt-effect.tsv', 'fail'), ('podman-5-attempt-effect.tsv', 'unobserved'),
                       ('question-attempt-effect.tsv', 'undecided')):
        s, fails, unobs = Stub(), [], []
        s.xrec = {}
        judge(s, rows(name), 'step N: @N@ object(s)', unobs, fails)
        got = 'fail' if fails else 'unobserved' if unobs else 'undecided' if s.xrec.get('undec') else 'none'
        good = got == want
        ok &= good
        print(f'CHECK {name} {"PASS" if good else "FAIL"} want {want}, got {got}: {(fails + unobs + s.xrec.get("undec", []))}')
print('RESULT: PASS' if ok else 'RESULT: FAIL')
sys.exit(0 if ok else 1)

#!/usr/bin/env python3
"""Check of the rule of `run` for rows written after a stop signal ([f3] of CORRECTIONS.md), in-process.

A live stop (selftest.sh step 3b) cannot be made to write a row after the signal on purpose: the runner cleans up and
exits at once, and a row after the signal appears only when cleaning up takes long (dev-13: 12 rows). So `Ctx.row`
of the frozen `run` is called directly, once with a stop signal noted and once without, on a throw-away folder.
Usage: check-stop-row.py [PATH-OF-run]"""
import importlib.machinery
from pathlib import Path
import sys
import tempfile

run_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / 'run'
R = importlib.machinery.SourceFileLoader('runmod', str(run_path)).load_module()
status = 0


class FakeRun:
    def __init__(self, runs_dir, stopping):
        self.runs_dir = Path(runs_dir)
        self.stopping = stopping
        self.rows = []

    def add_row(self, case_id, row_id, part, outcome, evidence_file):
        self.rows.append((case_id, row_id, part, outcome, evidence_file))


def check(name, ok, detail=''):
    global status
    print(f'CHECK {name} {"PASS" if ok else "FAIL"} {detail}')
    status |= not ok


with tempfile.TemporaryDirectory() as tmp:
    case = {'id': 'OW-9', 'part': 'OW', 'family': 'netloss'}
    for stopping, want in (('signal 15 at 2026-11-24T00:00:00Z', 'unobserved'), (False, 'fail')):
        run = FakeRun(Path(tmp) / ('stopped' if stopping else 'running'), stopping)
        ctx = R.Ctx(run, case)
        ctx.row('OW-9', 'fail', ['second application applied: False'])
        got = run.rows[-1][3]
        text = (run.runs_dir / run.rows[-1][4]).read_text()
        named = 'the run was stopped' in text and 'outcome the interrupted steps gave, not used: fail' in text
        if stopping:
            check('row-after-stop-is-unobserved', got == want and named, f'outcome {got}; stop named: {named}')
        else:
            check('row-without-stop-keeps-its-outcome', got == want and not named, f'outcome {got}')
print('RESULT:', 'PASS' if status == 0 else 'FAIL')
sys.exit(status)

#!/usr/bin/env python3
"""Check of [f5-c] of CORRECTIONS.md (review R6), in-process: the P1 and Understanding comparisons of the inventory
before the restart of a P4-PIPE case are written as records in the evidence and to no row of results.tsv; every other
row of the same case, and the rows of another case, are written as before.
`Ctx.row` of the given `run` is called directly on a throw-away folder. Fails on the fourth freeze (it writes the
rows `P1:P4-PIPE-1-before` and `UND:P4-PIPE-1-before`).
Usage: check-before-record.py [PATH-OF-run]"""
import importlib.machinery
from pathlib import Path
import sys
import tempfile

run_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / 'run'
R = importlib.machinery.SourceFileLoader('runmod', str(run_path)).load_module()
status = 0


class FakeRun:
    def __init__(self, runs_dir):
        self.runs_dir = Path(runs_dir)
        self.stopping = False
        self.rows = []

    def add_row(self, case_id, row_id, part, outcome, evidence_file):
        self.rows.append((case_id, row_id, part, outcome, evidence_file))


def check(name, ok, detail=''):
    global status
    print(f'CHECK {name} {"PASS" if ok else "FAIL"} {detail}')
    status |= not ok


with tempfile.TemporaryDirectory() as tmp:
    run = FakeRun(tmp)
    ctx = R.Ctx(run, {'id': 'P4-PIPE-1', 'part': 'P4', 'family': 'steps'})
    ctx.dir.mkdir(parents=True, exist_ok=True)
    for rid, part in (('P1:P4-PIPE-1-before', 'P1'), ('UND:P4-PIPE-1-before', 'UND'), ('P1:P4-PIPE-1', 'P1'),
                      ('UND:P4-PIPE-1', 'UND'), ('P4-PIPE-1', 'P4')):
        ctx.row(rid, 'fail', ['planted reason'], part=part)
    ids = [r[1] for r in run.rows]
    check('no-row-for-before', not any(i.endswith('-before') for i in ids), f'rows written: {ids}')
    check('rows-after-restart-kept', ids == ['P1:P4-PIPE-1', 'UND:P4-PIPE-1', 'P4-PIPE-1'], f'rows written: {ids}')
    recs = sorted(p.name for p in ctx.dir.glob('*.record.txt'))
    check('records-in-evidence', recs == ['P1_P4-PIPE-1-before.record.txt', 'UND_P4-PIPE-1-before.record.txt']
          or recs == sorted(R.safe(i) + '.record.txt' for i in ('P1:P4-PIPE-1-before', 'UND:P4-PIPE-1-before')),
          f'record files: {recs}')
    text = ''.join((ctx.dir / r).read_text() for r in recs)
    check('record-names-R6-and-result', 'R6' in text and 'the comparison gave: fail' in text and 'planted reason' in text,
          f'{len(text)} bytes of records')
    run2 = FakeRun(Path(tmp) / 'other')
    ctx2 = R.Ctx(run2, {'id': 'OW-1', 'part': 'OW', 'family': 'steps'})
    ctx2.dir.mkdir(parents=True, exist_ok=True)
    ctx2.row('P1:OW-1-before', 'fail', ['x'], part='P1')
    check('other-case-unchanged', [r[1] for r in run2.rows] == ['P1:OW-1-before'], f'{[r[1] for r in run2.rows]}')
print('RESULT:', 'PASS' if status == 0 else 'FAIL')
sys.exit(status)

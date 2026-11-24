#!/usr/bin/env python3
"""Check of [f5-a] of CORRECTIONS.md, in-process: the account lines that `run` writes in REPRO-2a and REPRO-2b, put
into the implementation's format by `adapter.py`, are accepted by the account check of the release's own `assemble.py`
(`validate_accounts`, the check that refused REPRO-2a in complete run 1). `Ctx.fam_repro2` of the given `run` is
called with its machine steps replaced by stubs that only record the lines it adds; nothing is built or booted.
Fails on the fourth freeze (`home=/nonexistent`: “account home must be an immediate child of /home”).
Usage: check-repro2-accounts.py PATH-OF-run RELEASE-SOURCE-DIR"""
import importlib.machinery
from pathlib import Path
import shlex
import sys
import tempfile

run_path, release = Path(sys.argv[1]), Path(sys.argv[2])
R = importlib.machinery.SourceFileLoader('runmod', str(run_path)).load_module()
AD = importlib.machinery.SourceFileLoader('adaptermod', str(run_path.parent / 'adapter.py')).load_module()
sys.path.insert(0, str(release))
AS = importlib.machinery.SourceFileLoader('assemblemod', str(release / 'assemble.py')).load_module()
status = 0


def check(name, ok, detail=''):
    global status
    print(f'CHECK {name} {"PASS" if ok else "FAIL"} {detail}')
    status |= not ok


class Done(Exception):
    pass


class FakeMachine:
    def __init__(self, name):
        self.name = name
        self.lines = []
        self.written_text = ''


class FakeRun:
    def __init__(self, runs_dir):
        self.runs_dir = Path(runs_dir)
        self.stopping = False

    def add_row(self, *a):
        raise Done(f'a row was written before the four applications: {a}')


for with_ids, cid in ((True, 'REPRO-2a'), (False, 'REPRO-2b')):
    with tempfile.TemporaryDirectory() as tmp:
        ctx = R.Ctx(FakeRun(tmp), {'id': cid, 'part': 'REPRO', 'family': 'repro2', 'with_ids': with_ids})
        ctx.dir.mkdir(parents=True, exist_ok=True)
        made, applied = [], []
        ctx.fresh = lambda name, build=False, decl=None: made.append(FakeMachine(name)) or made[-1]

        def change(m, op, text, machine_build=False):
            m.lines.append((op, text))

        def apply(m, cut=False, during=None, inventory=True):
            applied.append(m.name)
            if len(applied) == 4:
                raise Done('four applications')
            return {'applied': True}
        ctx.change, ctx.apply = change, apply
        try:
            ctx.fam_repro2()
        except Done:
            pass
        acc = [t for m in made for op, t in m.lines if t.startswith('account ')]
        check(f'{cid}-account-lines-written', len(acc) == 4, f'{acc}')
        rd = AD.Renderer(Path(tmp) / 'cache', '0.43', 'ssh-ed25519 AAAAplanted planted')
        for text in sorted(set(acc)):
            try:
                rows = [shlex.split(l) for l in rd.render_spec(AD.Spec(text), AD.Rendered(), None)]
            except AD.NotExpressible as e:
                # REPRO-2b without identifiers: the case is `unobserved: not expressible` by CASES.md; nothing to check
                check(f'{cid}-{text.split()[1]}-not-expressible', not with_ids, f'{e}')
                continue
            try:
                AS.validate_accounts(rows)
                check(f'{cid}-{text.split()[1]}-accepted', True, f'{rows}')
            except ValueError as e:
                check(f'{cid}-{text.split()[1]}-accepted', False, f'{rows}: {e}')
print('RESULT:', 'PASS' if status == 0 else 'FAIL')
sys.exit(status)

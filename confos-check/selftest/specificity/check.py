"""Checks of selftest/specificity/test.sh on runs/NAME: prints `CHECK NAME PASS|FAIL detail`, exit 0 if all pass."""
import sys
from pathlib import Path

run = Path(sys.argv[1])
rows = [l.split('\t') for l in (run / 'results.tsv').read_text().splitlines() if l.strip()]
ok = []


def check(name, cond, detail=''):
    ok.append(bool(cond))
    print(f'CHECK {name} {"PASS" if cond else "FAIL"} {detail}')


def rows_of(case):
    return [r for r in rows if r[3].split('/')[0] == case]


spec = rows_of('P4-T-SPEC')
check('spec-rows-present', any(r[0] == 'P4-T-SPEC' for r in spec) and any(r[1] == 'P2' for r in spec)
      and any(r[0] == 'P1:P4-T-SPEC' for r in spec), f'{len(spec)} rows')
for r in spec:
    if r[1] in ('P1', 'P2', 'P4'):
        check(f'spec-not-fail {r[0]}', r[2] != 'fail', f'{r[1]} {r[2]} {r[3]}')
        if r[2] == 'fail':
            print((run / r[3]).read_text()[:3000])
            cmp = run / 'P4-T-SPEC' / 'inv-P4-T-SPEC' / 'compare-p1.tsv'
            if cmp.exists():
                print('compare-p1.tsv (not UNDERIVED):')
                print(''.join(l + '\n' for l in cmp.read_text().splitlines() if not l.startswith('UNDERIVED'))[:4000])

plant = {r[0]: r for r in rows_of('P4-T-PLANT')}
eff = run / 'P4-T-PLANT' / 'attempt-effect.tsv'
effect = eff.read_text() if eff.exists() else ''
check('plant-fail', plant.get('P4-T-PLANT', ['', '', ''])[2] == 'fail', str(plant.get('P4-T-PLANT')))
check('plant-file-in-effect', 'planted-by-test' in effect)
# the planted process runs /usr/bin/sleep, a program the declaration records: S8.2-5 decides it with that program. The
# delta must see it (attempt-delta.tsv, or attempt-delta-excluded.tsv decided with its executable), and the effect
# must hold it only if its executable is not recorded
delta = ''
for n in ('attempt-delta.tsv', 'attempt-delta-excluded.tsv'):
    p = run / 'P4-T-PLANT' / n
    delta += p.read_text() if p.exists() else ''
proc = [l for l in delta.splitlines() if 'process\t' in l and '/sleep' in l and ('86499' in l or 'decided with' in l)]
check('plant-process-seen-by-the-delta', bool(proc), proc[0][:250] if proc else '')
check('plant-process-decided-with-its-program', any('decided with' in l and '/usr/bin/sleep' in l for l in proc) or
      ('\tprocess\t' in effect and 'sleep' in effect), 'S8.2-5')

check('plant-P1-fail', plant.get('P1:P4-T-PLANT', ['', '', ''])[2] == 'fail', str(plant.get('P1:P4-T-PLANT')))

code = {r[0]: r for r in rows_of('P4-T-CODE')}
rt = run / 'P4-T-CODE' / 'inv-P4-T-CODE' / 'routes.tsv'
routes = rt.read_text() if rt.exists() else ''
print('P4-T-CODE routes.tsv:\n' + routes)
executes = any(l.split('\t')[1] == 'executes' for l in routes.splitlines()
               if l.count('\t') >= 1 and l.split('\t')[0].endswith(('/code.sh', '/code.js', '/tru2')))
check('code-routes-tried', 'code.sh' in routes and 'code.js' in routes and 'tru2' in routes)
check('code-fail-iff-executes', (code.get('P4-T-CODE', ['', '', ''])[2] == 'fail') == executes,
      f'row {code.get("P4-T-CODE")}, a direct route executes: {executes}')
check('plant-file-by-question-1', any('planted-by-test' in l and 'question 1' in l for l in effect.splitlines()),
      '[n3-A]')


# [n3-A]: one planted object per question must make its row fail through that question; a file that a
# recorded program writes into its own working folder must not
def effect_of(case):
    p = run / case / 'attempt-effect.tsv'
    return p.read_text() if p.exists() else ''


import json


def q3_in_force():
    """Whether the service manager loaded a unit of P4-T-Q3 (the force level of its last inventory)."""
    p = run / 'P4-T-Q3' / 'inv-P4-T-Q3' / 'inventory' / 'force.jsonl'
    if not p.exists():
        return None
    units = [o for o in map(json.loads, p.read_text().splitlines()) if o.get('kind') == 'unit'
             and o['id'].rsplit('/', 1)[-1] in ('cases-q3.service', 'cases-q3r.service')]
    return [u['id'] for u in units if (u.get('value') or {}).get('load') == 'loaded']


for case, q, needle in (('P4-T-Q1', 'question 1 (S8.2-7)', 'cases_planted'), ('P4-T-Q3', 'question 3 (S8.2-11)', 'cases-q3')):
    r = {x[0]: x for x in rows_of(case)}
    e = effect_of(case)
    hit = [l for l in e.splitlines() if needle in l and q in l]
    print(f'{case} attempt-effect.tsv:\n' + e[:3000])
    if case == 'P4-T-Q3':
        loaded = q3_in_force()
        print(f'P4-T-Q3: units of the attempt loaded by the service manager: {loaded}')
        if loaded == []:
            # the system refused every way open to the person (the outputs of the attempt say how): nothing is in
            # force, so question 3 is answered no and the row must not be `fail` because of the unit files;
            # question 3 answered yes is shown on the stock image (selftest/inventory, step 4)
            check('P4-T-Q3-not-in-force-not-counted', r.get(case, ['', '', 'fail'])[2] != 'fail' and not hit,
                  f'{r.get(case)}; question 3 answered yes is tested by selftest/inventory step 4')
            continue
    check(f'{case}-fail', r.get(case, ['', '', ''])[2] == 'fail', str(r.get(case)))
    check(f'{case}-by-{q.split(" (")[0].replace(" ", "-")}', bool(hit), hit[0][:250] if hit else 'no line of the effect names it')
    check(f'{case}-P1-fail', r.get(f'P1:{case}', ['', '', ''])[2] == 'fail', str(r.get(f'P1:{case}')))
work = {x[0]: x for x in rows_of('P4-T-WORK')}
for rid in ('P4-T-WORK', 'P1:P4-T-WORK'):
    check(f'work-not-fail {rid}', work.get(rid, ['', '', 'fail'])[2] != 'fail', str(work.get(rid)))
wx = run / 'P4-T-WORK' / 'inv-P4-T-WORK' / 'compare-p1-excluded.tsv'
wl = [l for l in (wx.read_text().splitlines() if wx.exists() else []) if '/.gnupg/' in l]
check('work-files-decided-by-question-4', wl and all('four-questions' in l for l in wl),
      f'{len(wl)} object(s) under ~/.gnupg in compare-p1-excluded.tsv' + (': ' + wl[0][:200] if wl else ''))
print(f'{sum(ok)}/{len(ok)} checks pass')
sys.exit(0 if all(ok) else 1)

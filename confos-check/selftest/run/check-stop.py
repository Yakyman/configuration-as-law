#!/usr/bin/env python3
"""Check of a run that was stopped by a signal while a case was in progress (found when dev-13 was stopped).

Every row whose outcome file was written after the stop signal must be `unobserved` and name the stop. If none was
written (the runner exited at once), this says so; the rule itself is checked by check-stop-row.py. Usage:
check-stop.py RUNDIR"""
import sys
from pathlib import Path

rundir = Path(sys.argv[1])
signal_time = None
for line in (rundir / '_run' / 'log.txt').read_text(errors='replace').splitlines():
    if 'NOTE signal ' in line and 'stopping' in line:
        signal_time = line.split()[0]
if signal_time is None:
    print('CHECK stop-signal-noted FAIL (no signal line in _run/log.txt)')
    sys.exit(1)
print(f'signal noted at {signal_time}')
after, bad = 0, 0
for f in sorted(rundir.glob('*/*.outcome.txt')):
    lines = f.read_text(errors='replace').splitlines()
    t = lines[1].split()[1] if len(lines) > 1 and lines[1].startswith('time ') else ''
    if t < signal_time:
        print(f'  before the stop: {lines[0]}')
        continue
    after += 1
    outcome = lines[0].split('\t')[2]
    named = any('the run was stopped' in x for x in lines)
    ok = outcome == 'unobserved' and named
    bad += not ok
    print(f'  after the stop: {lines[0]}  {"ok" if ok else "WRONG"}')
results = (rundir / 'results.tsv').read_text().splitlines()
print(f'results.tsv rows: {len(results)}')
if after == 0:
    print('CHECK rows-after-stop-unobserved NONE (no row was written after the stop: the runner exited first; the rule is '
          'checked in-process by check-stop-row.py)')
    sys.exit(0)
if bad:
    print(f'CHECK rows-after-stop-unobserved FAIL ({bad} of {after} rows after the stop are not unobserved)')
    sys.exit(1)
print(f'CHECK rows-after-stop-unobserved PASS ({after} rows after the stop, all unobserved and naming the stop)')

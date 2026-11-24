#!/usr/bin/env python3
"""Check the results of `run --backend stock` on the self-test subset, from its own files.

  check-results.py RUN_DIR

Expected on a stock Debian 13 image (where nothing restricts the person):
  P4-SHELL pass; P4-C9-4 fail (the saved script ran); P4-PIPE-1 fail (what the payload left is in force after the
  restart, which had a new boot id; the payload was fetched from 10.0.2.2); OW-1 unobserved (NotAvailable: no
  declaration); OW-10 unobserved (real hardware); P1-0 unobserved (no derivation on a stock image) with the
  inventory program called and exiting 0 when it exists. Every row has a valid outcome and an existing evidence file.
"""
import json
from pathlib import Path
import sys

run = Path(sys.argv[1])
cases = Path(__file__).resolve().parents[2]
ok_all = []


def check(name, ok, detail=''):
    ok_all.append(ok)
    print(f'CHECK {name} {"PASS" if ok else "FAIL"} {detail}', flush=True)


rows = [l.split('\t') for l in (run / 'results.tsv').read_text().splitlines() if l.strip()]
check('results-rows-well-formed', all(len(r) == 4 and r[2] in ('pass', 'fail', 'unobserved', 'undecided')
                                      for r in rows), f'{len(rows)} rows')
check('evidence-files-exist', all((run / r[3]).exists() for r in rows))
out = {r[0]: r[2] for r in rows}
for cid, want in (('P4-SHELL', 'pass'), ('P4-C9-4', 'fail'), ('P4-PIPE-1', 'fail'), ('OW-1', 'unobserved'),
                  ('OW-10', 'unobserved'), ('P1-0', 'unobserved')):
    check(f'outcome-{cid}', out.get(cid) == want, f'{out.get(cid)} (expected {want})')


def commands(cid):
    p = run / cid / 'commands.jsonl'
    return [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else []


pipe = commands('P4-PIPE-1')
waits = [c for c in pipe if c['command'] == 'wait for SSH (boot id)' and c['exit'] == 0]
bids = [(run / 'P4-PIPE-1' / c['stdout']).read_text().strip() for c in waits]
check('pipe-restart-new-boot-id', len(bids) >= 2 and bids[-1] != bids[0], f'{bids}')
log = run / 'P4-PIPE-1' / 'http-requests.log'
text = log.read_text() if log.exists() else ''
check('pipe-payload-fetched-from-host', 'GET /payload.sh' in text and 'GET /jq' in text,
      f'{text.count("GET")} request(s)')
reason = (run / 'P4-PIPE-1' / 'P4-PIPE-1.outcome.txt').read_text()
check('pipe-decided-by-probes-after-restart', 'counts against' in reason)

p10 = commands('P1-0')
inv = [c for c in p10 if c['where'] == 'H' and isinstance(c['command'], list) and any(str(x).endswith('/inventory') for x in c['command'][:2])]
if (cases / 'inventory').exists():
    check('inventory-called-exit-0', bool(inv) and inv[-1]['exit'] == 0,
          f'exit {inv[-1]["exit"] if inv else None}')
    stored = run / 'P1-0' / 'inv-P1-0' / 'inventory' / 'stored.jsonl'
    check('inventory-stored-level-nonempty', stored.exists() and stored.stat().st_size > 0)
    cmp = [c for c in p10 if c['where'] == 'H' and isinstance(c['command'], list) and any(str(x).endswith('/compare') for x in c['command'][:2])]
    if (cases / 'compare').exists():
        check('compare-called', bool(cmp), f'exit {cmp[-1]["exit"] if cmp else None}')
    else:
        print('CHECK compare-called UNOBSERVED cases/compare not present')
else:
    print('CHECK inventory-called UNOBSERVED cases/inventory not present; P1-0 must say so')
    check('inventory-absent-recorded', 'inventory program' in (run / 'P1-0' / 'P1-0.outcome.txt').read_text())
print('RESULTS', 'PASS' if all(ok_all) else 'FAIL')
sys.exit(0 if all(ok_all) else 1)

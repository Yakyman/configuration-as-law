#!/usr/bin/env python3
"""Verify revised instrument hashes and separation from rehearsal records."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
prefix = HERE.relative_to(ROOT).as_posix() + '/'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--report',type=Path,help='New verification report; must not exist')
parser.add_argument('--records',action='store_true',help='Also verify the separate full record set')
args = parser.parse_args()

def listing(name):
    rows = (HERE/name).read_text().splitlines()
    assert len(rows) == len(set(rows)), name
    for name in rows:
        path = Path(name)
        assert not path.is_absolute() and '..' not in path.parts and path.parts[0] == 'S4'
    return set(rows)

instrument = listing('PUBLISH.list')
classification = listing('CLASSIFICATION-INPUTS.list')
assert classification <= instrument
expected = instrument - {prefix+'input-files.sha256.tsv'}
with (HERE/'input-files.sha256.tsv').open() as f:
    rows = list(csv.DictReader(f,delimiter='\t'))
assert len(rows) == len(expected) and {r['path'] for r in rows} == expected
for row in rows:
    assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest() == row['sha256'], row['path']
for path in instrument:
    assert not path.startswith(('S4/rehearsal/','S4/parts/','S4/raw/')), path
    assert not any(Path(path).name == name for name in ('READY.md','REVIEW.md','FIX-S4-P-1.md','fact-status.tsv','STATUS.md')), path
assert classification == {prefix+p for p in ('COLLECT.md','MATCH.md','tables/MISSING.tsv',
                                             'tables/missing-row-map.tsv','checks/match-scope.tsv')}
result = {'date_utc':'2026-11-23','instrument_files':len(instrument),
          'hashes_verified':len(rows),'classification_documents':len(classification),
          'rehearsal_and_status_records_excluded':True,
          'independent_acceptance':'not performed by this verification'}
if args.records:
    records = listing('RECORDS.list')
    assert not records & instrument
    pending = {str(args.report.relative_to(ROOT))} if args.report and args.report.is_absolute() else ({str(args.report)} if args.report else set())
    actual = {str(p.relative_to(ROOT)) for p in (ROOT/'S4').rglob('*') if p.is_file()}
    assert records | instrument == actual | pending
    for name in records-pending: assert (ROOT/name).is_file(), name
    assert {name for name in actual if name.startswith(('S4/rehearsal/','S4/parts/'))} <= records
    prior = set((ROOT/'S4/PUBLISH.list').read_text().splitlines())
    assert prior <= records | instrument
    assert (ROOT/'S4/READY.md').read_bytes() == (HERE/'READY.md').read_bytes()
    result['records_files'] = len(records)
    result['prior_list_entries_retained'] = len(prior)
    result['disjoint_complete_publication_sets'] = True
if args.report:
    with args.report.open('x') as f: f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,sort_keys=True))

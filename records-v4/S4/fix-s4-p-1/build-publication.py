#!/usr/bin/env python3
"""Create separate instrument and record publication sets for this revision."""
import csv
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
prefix = HERE.relative_to(ROOT).as_posix() + '/'

def save(name, values):
    (HERE/name).write_text(''.join(p+'\n' for p in sorted(values)))

classification = {prefix+p for p in (
    'COLLECT.md', 'MATCH.md', 'tables/MISSING.tsv',
    'tables/missing-row-map.tsv', 'checks/match-scope.tsv')}
instrument = {'S4/collect.sh'} | classification
instrument |= {str(p.relative_to(ROOT)) for p in (ROOT/'S4/collector').iterdir() if p.is_file()}
instrument |= {prefix+p for p in ('COMMANDS.md','PUBLISH.list','CLASSIFICATION-INPUTS.list',
                                'input-files.sha256.tsv','verify-inputs.py')}
save('CLASSIFICATION-INPUTS.list', classification)
save('PUBLISH.list', instrument)
with (HERE/'input-files.sha256.tsv').open('w', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['path','sha256'])
    for name in sorted(instrument-{prefix+'input-files.sha256.tsv'}):
        w.writerow([name, hashlib.sha256((ROOT/name).read_bytes()).hexdigest()])

records = {str(p.relative_to(ROOT)) for p in (ROOT/'S4').rglob('*') if p.is_file()} - instrument
# This report is created by the immediately following read-only verification.
records |= {prefix+'RECORDS.list',prefix+'raw/publication-verification.json'}
save('RECORDS.list', records)
print(f'Instrument files: {len(instrument)}; classification documents: {len(classification)}; record files: {len(records)}')

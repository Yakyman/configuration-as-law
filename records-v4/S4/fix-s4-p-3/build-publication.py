#!/usr/bin/env python3
"""Finalize active instrument and separate record lists, then hash final inputs."""
import csv
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
S4 = ROOT / 'S4'
PREFIX = HERE.relative_to(ROOT).as_posix() + '/'


def write_list(path, values):
    path.write_text(''.join(name + '\n' for name in sorted(values)))


classification = {'S4/' + name for name in ('COLLECT.md', 'MATCH.md', 'MISSING.tsv', 'HANDOFF.md')}
classification |= {PREFIX + name for name in ('tables/missing-row-map.tsv', 'checks/match-scope.tsv')}
instrument = classification | {'S4/collect.sh', 'S4/COMMANDS.md', 'S4/PUBLISH.list',
                                'S4/CLASSIFICATION-INPUTS.list', 'S4/input-files.sha256.tsv'}
instrument |= {p.relative_to(ROOT).as_posix() for p in (S4 / 'collector').iterdir() if p.is_file()}
instrument |= {PREFIX + name for name in ('neutralize.py', 'neutral-literals.tsv', 'verify-inputs.py')}
extra = HERE / 'ADDED-INPUTS.list'
if extra.exists():
    instrument |= set(extra.read_text().splitlines())
write_list(S4 / 'CLASSIFICATION-INPUTS.list', classification)
write_list(S4 / 'PUBLISH.list', instrument)
records = {p.relative_to(ROOT).as_posix() for p in S4.rglob('*') if p.is_file()} - instrument
records |= {PREFIX + 'RECORDS.list', PREFIX + 'checks/publication-verification.json'}
write_list(HERE / 'RECORDS.list', records)
# Last mutation: every listed input is final before this digest pass.
with (S4 / 'input-files.sha256.tsv').open('w', newline='') as stream:
    writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
    writer.writerow(['path', 'sha256'])
    for name in sorted(instrument - {'S4/input-files.sha256.tsv'}):
        writer.writerow([name, hashlib.sha256((ROOT / name).read_bytes()).hexdigest()])
print(f'{len(instrument)} instrument files; {len(classification)} classification documents; {len(records)} records')

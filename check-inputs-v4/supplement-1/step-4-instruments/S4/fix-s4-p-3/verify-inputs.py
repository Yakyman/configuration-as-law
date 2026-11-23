#!/usr/bin/env python3
"""Read-only verification of the active instrument set and handoff separation."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
S4 = ROOT / 'S4'
PREFIX = HERE.relative_to(ROOT).as_posix() + '/'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--report', type=Path, help='New audit file, outside the instrument list')
parser.add_argument('--records', action='store_true')
args = parser.parse_args()


def listing(path):
    lines = path.read_text().splitlines()
    assert len(lines) == len(set(lines)), path.name
    for name in lines:
        p = Path(name)
        assert not p.is_absolute() and '..' not in p.parts and p.parts[0] == 'S4', name
    return set(lines)


instrument = listing(S4 / 'PUBLISH.list')
classification = listing(S4 / 'CLASSIFICATION-INPUTS.list')
with (S4 / 'input-files.sha256.tsv').open() as stream:
    hashes = list(csv.DictReader(stream, delimiter='\t'))
assert len(hashes) == len(instrument) - 1
assert {r['path'] for r in hashes} == instrument - {'S4/input-files.sha256.tsv'}
for row in hashes:
    assert hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest() == row['sha256'], row['path']
assert classification <= instrument
for name in instrument:
    assert not any(part in ('rehearsal', 'parts', 'systems', 'raw') for part in Path(name).parts), name
    assert Path(name).name not in ('READY.md', 'fact-status.tsv', 'STATUS.md', 'FIX-S4-P-3.md'), name
for name in classification:
    assert Path(name).suffix in ('.md', '.tsv')
    assert Path(name).name not in ('neutral-literals.tsv', 'fact-status.tsv')
    data = (ROOT / name).read_text()
    for literal in ('lock-receipt-reference', 'directory-receipt', 'unowned-with-receipt-',
                    'cache-identity-reference-not-install-receipt', 'no-surviving-receipt',
                    'unknown:no-original-image-manifest', 'unknown: no creation event established by current file'):
        assert literal not in data, (name, literal)
rule = 'If the handoff copy of a machine fails, nothing is repaired and no observation is repeated; the objects of that machine are listed by id as not delivered, receive no decision in this step, and the machine gives “?”.'
assert all(rule in (S4 / name).read_text() for name in ('HANDOFF.md', 'COMMANDS.md'))
result = {'date_utc': '2026-11-23', 'instrument_files': len(instrument), 'hashes_verified': len(hashes),
          'classification_documents': len(classification), 'failure_procedure_identical': True,
          'rehearsal_records_excluded': True, 'independent_acceptance': 'pending separate review'}
if args.records:
    records = listing(HERE / 'RECORDS.list')
    pending = {args.report.resolve().relative_to(ROOT).as_posix()} if args.report else set()
    actual = {p.relative_to(ROOT).as_posix() for p in S4.rglob('*') if p.is_file()}
    assert not records & instrument
    assert records | instrument == actual | pending
    result['record_files'] = len(records)
    result['disjoint_complete_publication_sets'] = True
if args.report:
    with args.report.open('x') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, sort_keys=True))

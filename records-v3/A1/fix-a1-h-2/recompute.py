"""Apply only review-2 finding 1 to frozen round-1 records."""
import collections
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / 'A1/fix-a1-h-1'
OUT = Path(__file__).resolve().parent

def read(path):
    with path.open() as f:
        return list(csv.DictReader(f, delimiter='\t'))

def write(name, rows):
    with (OUT / name).open('w') as f:
        writer = csv.DictWriter(f, list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)

def counts(rows, key):
    return dict(sorted(collections.Counter(r[key] for r in rows).items()))

checks = read(OLD / 'unit-file-reader-check.tsv')
affected = {r['id']: r for r in checks if r['second_applier'].startswith('ESTABLISHED')}
assert len(affected) == 21
outcomes = []
for rid, r in affected.items():
    assert r['kind'] in ('system-unit', 'user-unit')
    assert r['membership'] == 'READING-DEPENDENT'
    hits = []
    for hit in r['available_inventory_matches'].split(' | '):
        match = re.fullmatch(r'(A1/in/raw/[^:]+):(\d+): (.*)', hit)
        if not match:
            continue
        path, number, saved_line = match.groups()
        assert (ROOT / path).read_text().splitlines()[int(number)-1] == saved_line
        fields = saved_line.split()
        expected = 'user-list-unit-files.txt' if r['kind'] == 'user-unit' else 'unit-files.txt'
        if Path(path).name == expected and fields[:2] == [r['name'], 'disabled']:
            hits.append(f'{path}:{number}: {saved_line}')
    assert hits, rid
    outcomes.append({
        'id': rid, 'kind': r['kind'], 'name': r['name'],
        'managed_unit_reading': 'OUTSIDE-H1: the managed unit and its state are not the backing settings file; this H1 claim needs that substitution.',
        'backing_file_reading': 'OUTSIDE-H1: disabled state establishes installation instructions for systemctl, in addition to runtime manager values; single-program premise fails.',
        'membership': 'EXCLUDED-BOTH-READINGS',
        'disabled_evidence': ' | '.join(hits),
        'documentation': 'A1/fix-a1-h-1/raw/systemctl-v260.xml:1116-1117; A1/fix-a1-h-1/raw/systemd.unit-v260.xml:2241-2246',
    })

extent = read(OLD / 'hole-1-extent.tsv')
changes = []
for r in extent:
    if r['id'] not in affected:
        continue
    assert r['extent_status'] == 'READING-DEPENDENT'
    r['extent_status'] = 'EXCLUDED-BOTH-READINGS'
    r['qualification'] = ('Outside H1 under both recorded readings: the managed unit/state is not its backing settings file; '
                          'under the file reading, saved disabled state establishes installation instructions for systemctl '
                          'in addition to runtime manager values, so the single-program premise fails. '
                          'This excludes H1 membership only; it assigns no overall MUST/NOT decision and selects neither object reading.')
    r['evidence'] += '; A1/fix-a1-h-2/reading-outcomes.tsv; A1/fix-a1-h-2/unit-boundaries.md'
    changes.append({'id': r['id'], 'kind': r['kind'], 'name': r['name'], 'before': 'READING-DEPENDENT',
                    'after': r['extent_status'], 'reason': r['qualification'], 'evidence': r['evidence']})
for r in checks:
    if r['id'] in affected:
        r['membership'] = 'EXCLUDED-BOTH-READINGS'
scan = read(OLD / 'hole-1-scan.tsv')
for r in scan:
    if r['id'] in affected:
        r['scope_disposition'] = 'EXCLUDED-BOTH-READINGS; see A1/fix-a1-h-2/hole-1-extent.tsv'

for sample in ('agreed', 'resolved'):
    assert not set(affected).intersection(r['id'] for r in read(OLD / f'{sample}-audit.tsv'))
assert len(changes) == 21
assert len(extent) == len({r['id'] for r in extent}) == 914
assert len(scan) == len({r['id'] for r in scan}) == 5200
assert sum(r['extent_status'].startswith('CONFIRMED') for r in extent) == 114
summary = json.loads((OLD / 'counts.json').read_text())
summary.update(h1_status=counts(extent, 'extent_status'), membership_changes=21,
               all_changed_records=21, h1_excluded_total=56,
               summary_basis='Round-1 counts retained except H1 status counts and this-round delta counts; samples not rerun.',
               previous_round_delta_counts={'membership_changes': 607, 'all_changed_records': 614})
assert summary['h1_status']['READING-DEPENDENT'] == 501
assert summary['h1_status']['FACTUAL-UNKNOWN'] == 243
for name, rows in [('hole-1-extent.tsv', extent), ('unit-file-reader-check.tsv', checks),
                   ('hole-1-scan.tsv', scan), ('reading-outcomes.tsv', outcomes), ('changes.tsv', changes)]:
    write(name, rows)
(OUT / 'counts.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))

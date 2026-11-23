"""Merge c1 part-4 shards and validate the completed classification."""
import csv
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[2]
folder = root / 'A1/c1'
header = ['id', 'decision', 'sentences', 'what_it_does', 'basis', 'reason']
allowed = ['MUST', 'NOT', 'HOLE', 'UNKNOWN', 'MIXED']
inputs = list(csv.DictReader((root / 'A1/in/part-4.tsv').open(encoding='utf-8'), delimiter='\t'))
input_ids = [row['id'] for row in inputs]
assert len(input_ids) == len(set(input_ids)), 'Duplicate input IDs'
output = folder / 'part-4.tsv'
with output.open(encoding='utf-8') as stream:
    reader = csv.DictReader(stream, delimiter='\t')
    assert reader.fieldnames == header
    existing = list(reader)
assert len(existing) == len({row['id'] for row in existing}), 'Duplicate existing output IDs'
merged = {row['id']: row for row in existing}
shard_ids = set()
for part in [1, 2, 3]:
    with (folder / f'part-4.{part}.tsv').open(encoding='utf-8') as stream:
        reader = csv.DictReader(stream, delimiter='\t')
        assert reader.fieldnames == header
        for row in reader:
            assert row['id'] not in shard_ids, 'Duplicate shard ID'
            shard_ids.add(row['id'])
            merged[row['id']] = row
# Supplemental public documentation resolves previously missing package roles.
with (folder / 'part-4.packages.tsv').open(encoding='utf-8') as stream:
    reader = csv.DictReader(stream, delimiter='\t')
    assert reader.fieldnames == header
    supplemental_ids = set()
    for row in reader:
        assert row['id'] in merged and row['id'] not in supplemental_ids
        assert merged[row['id']]['decision'] in ['UNKNOWN', row['decision']], row
        supplemental_ids.add(row['id'])
        merged[row['id']] = row
assert set(merged) == set(input_ids), ('IDs differ', set(input_ids) - set(merged), set(merged) - set(input_ids))
assert len(merged) == len(input_ids)
for row in merged.values():
    assert set(row) == set(header), row
    assert row['decision'] in allowed, row
    assert len(row['what_it_does'].split()) <= 15, row
    assert len(row['reason'].split()) <= 30, row
    assert all(isinstance(value, str) and '\t' not in value and '\n' not in value and '\r' not in value for value in row.values()), row
    assert row['basis'] in ['evidence', 'none'] or row['basis'].startswith(('raw:', 'doc:https://', 'doc:http://')), row
    if row['basis'].startswith('raw:'):
        assert (root / 'A1/in/raw' / row['basis'][4:]).exists(), row
# All completed shard revisions have been validated before synchronizing the main file.
with output.open('w', encoding='utf-8', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=header, delimiter='\t', lineterminator='\n')
    writer.writeheader()
    for identifier in input_ids:
        writer.writerow(merged[identifier])
# Re-read the delivered file, rather than validating only in-memory rows.
with output.open(encoding='utf-8') as stream:
    reader = csv.DictReader(stream, delimiter='\t')
    assert reader.fieldnames == header
    final = list(reader)
final_ids = [row['id'] for row in final]
assert Counter(final_ids) == Counter(input_ids)
assert all(count == 1 for count in Counter(final_ids).values())
assert all(row['decision'] in allowed for row in final)
counts = Counter(row['decision'] for row in final)
text = ''.join(f'{decision}\t{counts[decision]}\n' for decision in allowed)
(folder / 'part-4.done').write_text(text, encoding='utf-8')
print(text, end='')

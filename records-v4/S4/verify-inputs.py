#!/usr/bin/env python3
"""Check the published S4 file set before staging or observation."""
import csv
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parent.parent
listed = (root / 'S4/PUBLISH.list').read_text().splitlines()
assert len(listed) == len(set(listed)), 'Duplicate publication path'
expected = set(listed) - {'S4/input-files.sha256.tsv'}
rows = list(csv.DictReader((root / 'S4/input-files.sha256.tsv').open(), delimiter='\t'))
assert {row['path'] for row in rows} == expected, 'Manifest/publication set mismatch'
assert len(rows) == len(expected), 'Duplicate manifest path'
for row in rows:
    path = Path(row['path'])
    assert not path.is_absolute() and '..' not in path.parts and path.parts[0] == 'S4'
    assert hashlib.sha256((root / path).read_bytes()).hexdigest() == row['sha256'], row['path']
print(f'PASS: {len(rows)} published inputs match their hashes (manifest excluded from its own hash)')

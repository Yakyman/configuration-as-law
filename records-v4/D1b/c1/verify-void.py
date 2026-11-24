"""Merge completed individual rows and verify the final table without rewriting it."""
import collections
import csv
import hashlib
import json
from pathlib import Path

csv.field_size_limit(10000000)
base = Path(__file__).resolve().parents[2]
folder = base / 'D1b/c1'
handoff = base / 'D1b/handoff/void'
header = ['id', 'decision', 'sentences', 'what_it_does', 'basis', 'reason']
decisions = ['INSTALLED-OWN', 'INSTALLED-PACKAGE', 'INSTALLED-DERIVED',
             'PROGRAM-OWN', 'PROGRAM-DERIVED', 'SETTING-OWN', 'SETTING-DEFAULT',
             'RECORD', 'MATERIAL', 'RUNTIME', 'ACTION', 'GAP-NONE', 'GAP-TWO',
             'UNKNOWN', 'MIXED']

def read(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))

inputs = read(base / 'D1b/in/part-void.tsv')
input_ids = [r['id'] for r in inputs]
selected = {}
for row in inputs:
    meta = json.loads(row['members'])
    while isinstance(meta, str):
        meta = json.loads(meta)
    if 'file' in meta:
        members = read(handoff / meta['file'])
        assert len(members) == meta['count'] and meta['complete']
    elif 'path' in meta:
        members = [meta]
    elif 'metadata' in meta:
        members = [meta['metadata']]
    else:
        members = []
    for member in members:
        selected[member['path']] = member

# Read the whole saved scan and check every selected stored object's backing.
seen = set()
with (handoff / 'raw/0004-filesystem.out').open() as f:
    for line in f:
        item = json.loads(line)
        if item.get('path') in selected:
            original = selected[item['path']]
            assert item['persistence'] == original['persistence'] == 'persistent'
            assert item['type'] == original['type']
            seen.add(item['path'])
assert set(selected) == seen, sorted(set(selected) - seen)

path = folder / 'part-void.tsv'
existing = read(path)
done = {r['id'] for r in existing}
assert len(done) == len(existing)
append_rows = []
for shard in ['part-void.settings.tsv', 'part-void.stores-revised.tsv']:
    append_rows.extend(read(folder / shard))
append_rows.append(dict(zip(header, [
    'd1b-void-e2eaf799995627549514724b', 'UNKNOWN',
    'S8.2-6,S8.2-7,S8.2-9,S8.2-15,S8.2-16',
    'Older kernel files, three initramfs images, and a GRUB directory',
    'raw:D1b/handoff/void/old-package-member-integrity.tsv',
    'All six listed members lack original references or generating-source evidence; newer verified kernel files indexed nearby are not members of this group.'
])))
with path.open('a', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, header, delimiter='\t', lineterminator='\n')
    for row in append_rows:
        assert row['id'] in input_ids
        if row['id'] not in done:
            writer.writerow(row)
            f.flush()
            done.add(row['id'])

with path.open(encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f, delimiter='\t')
    assert reader.fieldnames == header
    rows = list(reader)
ids = [r['id'] for r in rows]
assert len(ids) == len(input_ids) == len(set(ids)) == len(set(input_ids))
assert set(ids) == set(input_ids)
sentence_ids = set()
for line in (base / 'SENTENCES.md').read_text().splitlines():
    if line.startswith('- **S8.'):
        sentence_ids.add(line.split('**')[1])
for row in rows:
    assert set(row) == set(header) and all(row.values())
    assert row['decision'] in decisions
    assert set(row['sentences'].split(',')) <= sentence_ids
    assert len(row['what_it_does'].split()) <= 15
    assert len(row['reason'].split()) <= 30
    assert all('\t' not in v and '\n' not in v and '\r' not in v for v in row.values())
    if row['basis'].startswith('raw:'):
        assert (base / row['basis'].removeprefix('raw:')).is_file()
    else:
        assert row['basis'] in ['evidence', 'none'] or row['basis'].startswith('doc:')
counts = collections.Counter(r['decision'] for r in rows)
with (folder / 'part-void.done').open('w', encoding='utf-8') as f:
    for decision in decisions:
        f.write(f'{decision}\t{counts[decision]}\n')
with (folder / 'part-void.verification.json').open('w', encoding='utf-8') as f:
    json.dump({'rows': len(rows), 'unique_ids': len(set(ids)), 'id_set_equal': True,
               'allowed_decisions': True, 'word_limits': True,
               'stored_paths_checked_against_scan': len(seen),
               'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
               'counts': dict(counts)}, f, indent=2)
    f.write('\n')
print(dict(counts))
print('Verified exact ID set/count, uniqueness, decisions, sentence IDs, word limits, evidence paths and saved persistence observations.')

"""Recount only card 9 from frozen evidence, preserving cards 1 and 7."""
import collections
import csv
import hashlib
import json
import re
from pathlib import Path

csv.field_size_limit(100000000)
out = Path('A3R/fix-a3r-h-2')


def read(path):
    with open(path) as stream:
        return list(csv.DictReader(stream, delimiter='\t'))


def write(name, rows):
    with (out / name).open('x') as stream:
        writer = csv.DictWriter(stream, list(rows[0]), delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)


baseline = json.loads((out / 'frozen-inputs.sha256.json').read_text())
for filename, digest in baseline.items():
    with open(filename, 'rb') as stream:
        assert hashlib.file_digest(stream, 'sha256').hexdigest() == digest, filename

joined = read('A3R/compare/joined.tsv')
previous = read('A3R/fix-a3r-h-1/code_extent.tsv')
extent = [row for row in previous if row['card'] != '9']
data = Path('A3R/in/raw/lived/raw/160-filesystem.out').read_bytes().split(b'\0')
assert data[-1] == b'' and (len(data) - 1) % 6 == 0
paths = {data[i].decode(): data[i+1].decode() for i in range(0, len(data)-1, 6)}
roots = {
    'system': '/var/lib/systemd/deb-systemd-helper-enabled/',
    'user': '/var/lib/systemd/deb-systemd-user-helper-enabled/',
}
markers = {}
for instance, prefix in roots.items():
    for path, kind in paths.items():
        if kind == 'f' and path.startswith(prefix) and not path.endswith('.dsh-also'):
            assert path.rsplit('/', 1)[0].endswith('.wants') or '/' not in path[len(prefix):]
            markers[path] = instance
source = 'A3R/fix-a3r-h-2/raw/helper-source.txt:100-110,354-375,576-580'
inventory = 'A3R/in/raw/lived/raw/160-filesystem.out'
write('helper-witnesses.tsv', [dict(path=path, type=paths[path], instance=markers[path],
      evidence=source + '; ' + inventory) for path in sorted(markers)])

search = []
for row in joined:
    members = []
    if row['kind'].startswith('stored'):
        members = ([row['name']] if ':subtree' in row['kind'] else
                   [p for p in re.findall(r'/[^\\"\],]+', row['members']) if p != row['name']])
    hits = sorted(p for p in markers if any(p == m or p.startswith(m + '/') for m in members))
    named = bool(re.search(r'deb-systemd-(?:user-)?helper', row['name']))
    search.append(dict(id=row['id'], kind=row['kind'], name=row['name'],
                       name_match=str(named).lower(), member_witnesses='|'.join(hits),
                       confirmed=str(bool(hits)).lower()))
    if hits:
        extent.append(dict(id=row['id'], card='9', kind=row['kind'], name=row['name'],
                           reason='Past enablement marker gates subsequent service-link creation: ' + hits[0],
                           evidence=inventory + '; ' + source))
write('helper-search.tsv', search)
write('code_extent.tsv', extent)
old9 = {r['id'] for r in previous if r['card'] == '9'}
new9 = {r['id'] for r in extent if r['card'] == '9'}
assert old9 <= new9
added = [r for r in extent if r['card'] == '9' and r['id'] not in old9]
write('added-memberships.tsv', added)
assert [r for r in extent if r['card'] != '9'] == [r for r in previous if r['card'] != '9']
assert len({(r['card'], r['id']) for r in extent}) == len(extent)
sets = {c: {r['id'] for r in extent if r['card'] == c} for c in ['1', '7', '9']}
summary = {
    'rows_searched': len(search),
    'card_rows': {c: len(s) for c, s in sets.items()},
    'card_9_kinds': dict(collections.Counter(r['kind'] for r in extent if r['card'] == '9')),
    'card_1_7_overlap': len(sets['1'] & sets['7']),
    'card_1_7_distinct': len(sets['1'] | sets['7']),
    'card_9_overlap_with_1_7': len(sets['9'] & (sets['1'] | sets['7'])),
    'distinct_rows_all_cards': len(set.union(*sets.values())),
    'helper_markers': len(markers),
    'helper_markers_by_instance': dict(collections.Counter(markers.values())),
    'card_9_added_ids': sorted(new9 - old9),
    'card_9_removed_ids': sorted(old9 - new9),
    'unchanged_cards': ['1', '7'],
    'sample_audit': 'unchanged; A3R/fix-a3r-h-1/sample_audit.tsv',
    'frozen_files_checked': len(baseline),
    'frozen_inputs_unchanged': True,
}
with (out / 'counts.json').open('x') as stream:
    stream.write(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))

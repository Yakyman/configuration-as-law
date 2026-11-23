"""Check revised records against frozen inputs and the reported aggregates."""
import collections
import csv
import hashlib
import json
import re
from pathlib import Path

P = Path('D1/fix-d1-h-2')
def read(path, frozen=False):
    with Path(path).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE if frozen else csv.QUOTE_MINIMAL))

hashes = json.loads((P / 'input-sha256.json').read_text())
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in hashes.items())
print('Frozen input files unchanged:', len(hashes))
joined = {r['id']: r for r in read('D1/compare/joined.tsv', True)}
adjudicated = read('D1/adjudication/rows.tsv', True)
summary = json.loads((P / 'summary.json').read_text())
confirmed = read(P / 'confirmed-rows.tsv')
scan = read(P / 'extent-search.tsv')
unknown = read(P / 'final-unknown.tsv')
changes = read(P / 'script-evidence-changes.tsv')
prior = read('D1/fix-d1-h-1/confirmed-rows.tsv')
prior_unknown = read('D1/fix-d1-h-1/final-unknown.tsv')
ids = lambda rows: {r['id'] for r in rows}
card6_ids = {r['id'] for r in adjudicated if r['hole'] == '6'}
assert len(card6_ids) == 20
assert ids(confirmed) == (ids(prior) - ids(changes)) | card6_ids
assert ids(unknown) == ids(prior_unknown) | ids(changes)
assert not ids(confirmed) & ids(unknown)
assert len(confirmed) == len(ids(confirmed)) == 1028
assert len(unknown) == len(ids(unknown)) == 224
assert len(changes) == 127
for row in confirmed + scan + changes:
    actual = joined[row['id']]
    assert all(row[k] == actual[k] for k in ('machine', 'kind', 'name'))
for h, lower, unresolved in [('1',303,466), ('2',131,226), ('3',319,46), ('5',255,309), ('6',20,21)]:
    assert sum(r['card'] == h for r in confirmed) == lower
    assert sum(r['card'] == h and r['status'] == 'UNRESOLVED_MEMBERSHIP' for r in scan) == unresolved
assert dict(collections.Counter(r['status'] for r in scan)) == summary['extent_search']
print('Membership delta: 1135 - 110 - 17 + 20 = 1028 distinct established rows.')
print('Unresolved memberships: 920 + 110 + 17 + 21 = 1068; factual UNKNOWN: 97 + 110 + 17 = 224.')

result = Path('D1/RESULT.md').read_text()
assert result.splitlines()[:2] == ['CHECK 1: 5 confirmed holes', 'OUTCOME: 0']
for h in ('1','2','3','5','6'):
    lower = sum(summary['by_card'][h].values())
    unresolved = summary['unresolved_memberships_by_card'][h]
    assert f'**At least {lower} rows**' in result
    assert f'**{unresolved} further row/card memberships remain unresolved**' in result
machine_lines = [l for l in result.splitlines() if l.startswith('| ') and len(l.split('|')) == 11]
for m in ('fedora','tumbleweed','mint','flatcar','talos'):
    cells = next([x.strip() for x in l.split('|')[1:-1]] for l in machine_lines if l.startswith('| '+m+' |'))
    assert int(cells[6]) == summary['confirmed_by_machine_lower_bound'].get(m, 0)
    assert int(cells[7]) == summary['unresolved_memberships_by_machine'].get(m, 0)
    assert cells[8] == summary['outcomes'][m]

# Preserve the original inventory/agreement/adjudication columns exactly.
before = (P / 'RESULT.before.md').read_text()
for m in ('fedora','tumbleweed','mint','flatcar','talos','TOTAL'):
    old = next(l for l in before.splitlines() if l.startswith('| '+m+' |'))
    new = next(l for l in result.splitlines() if l.startswith('| '+m+' |'))
    old_cells = [x.strip() for x in old.split('|')[1:-1]]
    new_cells = [x.strip() for x in new.split('|')[1:-1]]
    assert old_cells[:6] == new_cells[:6]
    assert old_cells[-1] == new_cells[-1]
for label, size in [('resolved',40), ('agreed',60)]:
    sample = read('D1/fix-d1-h-1/' + label + '-sample.tsv')
    assert len(sample) == size
    assert not ids(sample) & (ids(changes) | card6_ids)
    assert dict(collections.Counter(r['status'] for r in sample)) == summary['samples'][label]['counts']
print('Reported totals, per-card lower bounds, machine metrics/outcomes and preserved sample counts agree.')

# Check sentence-ID association as well as the separate required quote checker.
sentences = {}
for line in Path('SENTENCES.md').read_text().splitlines():
    match = re.match(r'- \*\*(S\d(?:\.\d)?-\d+)\*\* (.*)', line)
    if match:
        sentences[match[1]] = match[2]
count = 0
for line in result.splitlines():
    match = re.match(r'(S\d(?:\.\d)?-\d+): “(.*)”$', line)
    if match:
        assert sentences[match[1]] == match[2]
        count += 1
assert count == 13
print('Exact sentence-ID associations checked:', count)
print('Internal consistency only; independent acceptance remains a subsequent review.')

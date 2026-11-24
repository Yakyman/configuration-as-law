"""Audit only the changed failure-condition accounting, card 4 extent, and GAP ledger.

Run from the night folder. No new observations or resampling.
"""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / 'D1/fix-d1-h-1/raw'
csv.field_size_limit(10_000_000)


def read(path):
    with (ROOT / path).open() as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))


def decode(value):
    value = value.replace('\\"', '"')
    for _ in range(3):
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('""', '"')
        try:
            return json.loads(value)
        except ValueError:
            pass
    raise ValueError('Unrecognized member encoding')


def write(name, rows):
    with (OUT / name).open('x') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


joined = read('D1/compare/joined.tsv')
adj = read('D1/adjudication/rows.tsv')
by_id = {r['id']: r for r in joined}
gaps = [r for r in adj if r['verdict'] == 'GAP']
additional = {r['id']: r for r in read('D1/review/additional-unknown-rows.tsv')}
failure = []
for a in gaps:
    r = by_id[a['id']]
    if r['c1_decision'] != r['c2_decision']:
        failure.append({k: r[k] for k in ('id', 'machine', 'kind', 'name', 'c1_decision', 'c2_decision')} | {'hole': a['hole'], 'verdict': a['verdict']})
write('failure-condition-rows.tsv', failure)

# Search every kind/name and available L2 member path, independently of verdict.
# This is the changed card's observed initramfs/initrd extent, not a suffix-only
# claim that every .img file is an archive, or that all archives execute code.
extent = []
scanned = []
for r in joined:
    paths = [(r['name'], 'row')]
    member_source = ''
    if r['kind'].startswith('L2:'):
        members = decode(r['members'])
        if 'file' in members:
            member_source = 'D1/in/raw/' + r['machine'].removeprefix('d1-') + '/' + members['file']
            paths += [(m['path'], m.get('type', '')) for m in read(member_source)]
    matches = sorted({p for p, t in paths if t != 'symlink' and re.search(r'/boot/(?:initramfs-.*\.img|initrd-[^/]+)$', p)})
    scanned.append({'id': r['id'], 'kind': r['kind'], 'name': r['name'], 'member_source': member_source, 'paths_examined': len(paths), 'matched': bool(matches)})
    if matches:
        extent.append({k: r[k] for k in ('id', 'machine', 'kind', 'name')} | {'matching_members': ' | '.join(matches), 'member_source': member_source, 'status': 'CONFIRMED:archive-of-code'})
write('card4-search.tsv', scanned)
write('card4-extent.tsv', extent)
confirmed = {r['id'] for r in extent}
assert confirmed == {a['id'] for a in gaps if a['hole'] == '4'}

ledger = []
for a in gaps:
    r = by_id[a['id']]
    facts = additional.get(a['id'], {}).get('missing_facts', '')
    if a['id'] in confirmed:
        status = 'CONFIRMED:archive-of-code'
        why = 'S8.2-9/23 do not decide whether execution after extraction makes the stored archive code; S8.2-15 gives the alternative record reading.'
    elif a['id'] in additional:
        status = 'FACT_UNKNOWN'
        why = facts
    elif a['hole'] == '5':
        status = 'RESOLVED:INSTALLED-OWN'
        why = 'Permanently installed XPI package: S8.1-5/6 and S8.2-7/8/16; evidence D1/review/extension-evidence.json and saved installation action.'
    else:
        assert a['hole'] in ('1', '2')
        status = 'UNDECIDED:row-audit'
        why = 'Card-level refutation does not establish a final class for every member of this row; no final row verdict is claimed. Original GAP is retained for failure-condition accounting.'
    ledger.append({k: r[k] for k in ('id', 'machine', 'kind', 'name')} | {'original_hole': a['hole'], 'fix_status': status, 'additional_missing_facts': facts, 'reason': why})
write('gap-row-dispositions.tsv', ledger)
summary = {
    'objects_searched': len(scanned),
    'frozen_gap_rows': len(gaps),
    'disagreeing_gap_rows': len(failure),
    'disagreeing_gap_by_machine': dict(Counter(r['machine'] for r in failure)),
    'confirmed_card4_rows': len(extent),
    'confirmed_card4_by_machine': dict(Counter(r['machine'] for r in extent)),
    'exclusive_row_dispositions': dict(Counter(r['fix_status'] for r in ledger)),
    'undecided_by_card': dict(Counter(r['original_hole'] for r in ledger if r['fix_status'].startswith('UNDECIDED'))),
    'gap_and_fact_unknown_overlap': sorted(confirmed & additional.keys()),
}
assert sum(summary['exclusive_row_dispositions'].values()) == 1364
with (OUT / 'changed-counts.json').open('x') as f:
    json.dump(summary, f, indent=2)
    f.write('\n')
print(json.dumps(summary, indent=2))

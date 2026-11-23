"""Fix round 2: recompute changed memberships only; no probes or sample redraw."""
import collections
import csv
import hashlib
import json
from pathlib import Path

P = Path('D1/fix-d1-h-2')
OLD = Path('D1/fix-d1-h-1')

def read(path):
    with Path(path).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t'))

def write(name, rows, fields=None):
    with (P / name).open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields or list(rows[0]), delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)

baseline = json.loads((P / 'input-sha256.json').read_text())
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in baseline.items())
confirmed = read(OLD / 'confirmed-rows.tsv')
scan = read(OLD / 'extent-search.tsv')
unknown = read(OLD / 'final-unknown.tsv')
metadata = {r['id']: r for r in read('D1/review/cards14-raw/metadata-audit.tsv')}
prior_unknown = read('D1/review/final-unknown.tsv')
unknown_ids = {r['id'] for r in unknown}
members = {r['id']: r for r in confirmed}

# Missing script facts are not proof of either executable code or its absence.
# Retain all existing direct-script exclusions. Do not infer MUST from Requires.
changes = {}
for row in confirmed:
    m = metadata.get(row['id'], {})
    if row['card'] in ('1', '2') and row['kind'] == 'L1:package:rpm' and '/bin/sh' in m.get('requirements', ''):
        changes[row['id']] = dict(row, finding='2', previous_status='CONFIRMED', status='UNRESOLVED_MEMBERSHIP',
            reason='RPM shell-interpreter requirement is a scriptlet warning; actual scriptlets were not examined. File lists alone do not establish absence of executable scriptlets.',
            evidence='D1/review/cards14-raw/metadata-audit.tsv#' + row['id'] + '; D1/fix-d1-h-2/raw/rpm-scriptlets-source.md')
assert len(changes) == 110

retained_controls = []
mint_removed = [r for r in prior_unknown if r['machine'] == 'mint' and r['id'] not in unknown_ids]
assert len(mint_removed) == 19
for row in mint_removed:
    member = members[row['id']]
    package = row['name'].split(':', 1)[-1]
    control = Path('D1/review/cards14-raw/mint-' + package + '-control.json')
    if control.exists():
        facts = json.loads(control.read_text())
        assert facts['scripts'] == {}
        assert facts['version'] == metadata[row['id']]['installed_version']
        retained_controls.append(dict(id=row['id'], name=row['name'], version=facts['version'], evidence=str(control)))
    else:
        changes[row['id']] = dict(member, finding='3', previous_status='CONFIRMED', status='UNRESOLVED_MEMBERSHIP',
            reason='Previously unresolved whole-package facts: no saved installed-version maintainer-script control record. Dropping the metadata ground does not establish script absence.',
            evidence='D1/review/final-unknown.tsv#' + row['id'] + '; D1/review/cards14-raw/ (saved control-record inventory)')
assert len(changes) == 127 and len(retained_controls) == 2
write('script-evidence-changes.tsv', list(changes.values()))
write('retained-mint-controls.tsv', retained_controls)
confirmed = [r for r in confirmed if r['id'] not in changes]
for row in scan:
    change = changes.get(row['id'])
    if change and row['card'] == change['card']:
        assert row['status'] == 'CONFIRMED'
        row['status'] = 'UNRESOLVED_MEMBERSHIP'
        row['reason'] = change['reason']
for row in changes.values():
    assert row['id'] not in unknown_ids
    unknown.append({k: row[k] for k in ('id', 'machine', 'kind', 'name')} | {'source': row['reason'] + ' Evidence: ' + row['evidence']})

# The independent bounded card audit supplies the newly affected card only.
card6 = read(P / 'card6-extent.tsv')
assert all(r['card'] == '6' for r in card6)
for row in card6:
    if row['status'] == 'CONFIRMED':
        confirmed.append({k: row[k] for k in ('id', 'machine', 'kind', 'name', 'card', 'status', 'reason', 'evidence')})
    scan.append({k: row[k] for k in ('id', 'machine', 'kind', 'name', 'card', 'status', 'reason')})
assert len([r for r in confirmed if r['card'] == '6']) == 20
assert len({r['id'] for r in confirmed}) == len(confirmed)
assert len({(r['id'], r['card']) for r in scan}) == len(scan)
assert {(r['id'], r['card']) for r in confirmed} == {(r['id'], r['card']) for r in scan if r['status'] == 'CONFIRMED'}
assert not ({r['id'] for r in confirmed} & {r['id'] for r in unknown})
write('confirmed-rows.tsv', confirmed)
write('extent-search.tsv', scan)
write('final-unknown.tsv', unknown)

# Only validate preserved sample membership/counts; do not rerun the sampling procedure.
samples = {}
for label in ('resolved', 'agreed'):
    sample = read(OLD / (label + '-sample.tsv'))
    assert not ({r['id'] for r in sample} & set(changes))
    assert not ({r['id'] for r in sample} & {r['id'] for r in card6 if r['status'] == 'CONFIRMED'})
    samples[label] = dict(counts=dict(collections.Counter(r['status'] for r in sample)),
                          ordered_ids_unchanged=True, source=str(OLD / (label + '-sample.tsv')))

cards = ['1', '2', '3', '5', '6']
summary = dict(
    confirmed_cards=cards,
    confirmed_unique_rows_lower_bound=len(confirmed),
    by_card={h: dict(collections.Counter(r['machine'] for r in confirmed if r['card'] == h)) for h in cards},
    confirmed_by_machine_lower_bound=dict(collections.Counter(r['machine'] for r in confirmed)),
    unresolved_memberships_by_card={h: sum(r['card'] == h and r['status'] == 'UNRESOLVED_MEMBERSHIP' for r in scan) for h in cards},
    unresolved_memberships_by_machine=dict(collections.Counter(r['machine'] for r in scan if r['status'] == 'UNRESOLVED_MEMBERSHIP')),
    extent_search=dict(collections.Counter(r['status'] for r in scan)),
    unknown_total=len(unknown),
    unknown_by_machine=dict(collections.Counter(r['machine'] for r in unknown)),
    unknown_by_kind=dict(collections.Counter(r['kind'] for r in unknown)),
    changed_script_memberships_by_card_machine={h: dict(collections.Counter(r['machine'] for r in changes.values() if r['card'] == h)) for h in ('1', '2')},
    samples=samples,
    outcomes={m: '?' if m == 'talos' else '0' for m in ['fedora', 'tumbleweed', 'mint', 'flatcar', 'talos']},
    frozen_input_files=len(baseline))
(P / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in baseline.items())
print(json.dumps(summary, indent=2))
print('Frozen inputs unchanged; no experiment, sample redraw, inventory or failure-condition change.')

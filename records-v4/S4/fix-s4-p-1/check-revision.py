#!/usr/bin/env python3
"""Check changed accounting from named saved inputs; no inventory or guest access."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('output', type=Path, help='New output directory, must not exist')
out = parser.parse_args().output
out.mkdir(parents=True, exist_ok=False)

def read(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))

def write(name, fields, rows):
    with (out/name).open('x', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(fields)
        w.writerows(rows)

old = []
for filename in ('unknown-rows.tsv', 'additional-unknown-rows.tsv'):
    old.extend({key:r[key] for key in ('id','machine','kind','name')}
               for r in read(ROOT/'D1/review'/filename))
by_id = {r['id']:r for r in old}
assert len(old) == len(by_id) == 2007
keys = collections.Counter((r['machine'],r['kind'],r['name']) for r in old)
duplicates = {r['id'] for r in old if keys[(r['machine'],r['kind'],r['name'])] > 1}
assert len(duplicates) == 7
facts = read(HERE/'tables/MISSING.tsv')
links = read(HERE/'tables/missing-row-map.tsv')
status = read(HERE/'tables/fact-status.tsv')
assert list(facts[0]) == ['machine','fact','objects','why_not_recorded','how_recorded_now']
counts = collections.Counter(r['status'] for r in status)
assert dict(counts) == {'partial':12,'recordable':18,'not-obtainable':15}
assert len(facts) == len(status) == 45
assert {r['fact'].split(':')[0] for r in facts} == {r['fact_id'] for r in status}
deps = collections.defaultdict(set)
for r in links: deps[r['fact_id']].add(r['first_id'])
assert len(links) == len({tuple(r.values()) for r in links})
all_ids = {r['first_id'] for r in links}
assert set(by_id) <= all_ids
assert len(all_ids) == 2014 and len(all_ids-set(by_id)) == 7
assert deps['V09'] == {'void-f2e5d5edfa5902c8aee7bace'}
assert deps['M14'] == {'microos-dcce813055fa256ed012c87a'}
scope = []
for fact in facts:
    key = fact['fact'].split(':')[0]
    ids = deps[key]
    assert len(ids) == int(fact['objects'])
    fixed = ids & set(by_id)
    dup = fixed & duplicates
    scope.append([key,len(ids),len(fixed),len(ids-fixed),len(dup),len(fixed-dup)])
scope_by_id = {r[0]:r for r in scope}
assert scope_by_id['M04'][1:] == [8,8,0,7,1]
assert scope_by_id['M05'][1:] == [7,7,0,6,1]
for key in ('A14','V08','M12','M13','V09','M14'):
    assert scope_by_id[key][2] == scope_by_id[key][5] == 0
assert all(next(r for r in status if r['fact_id']==key)['status']=='recordable'
           for key in ('A14','V08','M12','M13'))
write('match-scope.tsv', ['fact_id','dependent_objects','fixed_input_ids','result_only_ids',
                        'duplicate_old_key_ids','max_potential_matches'], scope)
write('sudo-scope.tsv', ['first_id','machine','kind','name','old_key_count','M04','M05'],
      [[r['id'],r['machine'],r['kind'],r['name'],keys[(r['machine'],r['kind'],r['name'])],
        int(r['id'] in deps['M04']),int(r['id'] in deps['M05'])]
       for r in old if r['id'] in deps['M04']])

# This is only evidence preservation, not a new collector or matching test.
changed = []
baseline = read(HERE/'raw/before.sha256.tsv')
for row in baseline:
    p = ROOT/row['path']
    if hashlib.sha256(p.read_bytes()).hexdigest() != row['sha256']:
        changed.append(row['path'])
assert set(changed) <= {'S4/READY.md'}, changed
original_checks = read(ROOT/'S4/raw/original-inputs.sha256.tsv')
for row in original_checks:
    assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest() == row['sha256']
result = {
    'date_utc':'2026-11-23', 'fact_groups':len(facts), 'recordable':counts['recordable'],
    'partial':counts['partial'], 'not_obtainable':counts['not-obtainable'],
    'fixed_input_ids':len(by_id), 'result_only_ids':7, 'total_ids':len(all_ids),
    'old_duplicate_key_ids':len(duplicates), 'M04_max_potential_matches':1,
    'M05_max_potential_matches':1, 'recordable_groups_outside_matching_inputs':4,
    'baseline_files_checked':len(baseline), 'baseline_files_changed':changed,
    'prior_original_input_hashes_checked':len(original_checks),
    'runtime_changed':False, 'live_probes_or_machine_runs':0,
    'independent_acceptance':'not performed by this correction',
}
(out/'accounting.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,sort_keys=True))

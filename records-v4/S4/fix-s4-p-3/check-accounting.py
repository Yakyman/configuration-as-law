#!/usr/bin/env python3
"""Verify changed fact accounting and preservation of earlier records."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(path):
    with path.open(newline='') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('report', type=Path)
args = parser.parse_args()
assert not args.report.exists()
facts = read(HERE / 'tables/MISSING.tsv')
states = read(HERE / 'tables/fact-status.tsv')
links = read(HERE / 'tables/missing-row-map.tsv')
prior_states = read(ROOT / 'S4/fix-s4-p-2/tables/fact-status.tsv')
prior_facts = read(ROOT / 'S4/fix-s4-p-2/tables/MISSING.tsv')
target = set('A03 A04 A07 A09 A11 V03 V07 V09 M03 M05 M11 M14 T03 T05'.split())
assert list(facts[0]) == ['machine', 'fact', 'objects', 'why_not_recorded', 'how_recorded_now']
assert len(facts) == len(states) == 45
state_by_id = {r['fact_id']: r for r in states}
assert len(state_by_id) == 45
assert all(state_by_id[f]['status'] in ('recordable', 'not-obtainable') for f in target)
for before in prior_states:
    if before['fact_id'] not in target:
        assert before == state_by_id[before['fact_id']], before['fact_id']
for old, new in zip(prior_facts, facts):
    assert all(old[key] == new[key] for key in ('machine', 'fact', 'objects', 'why_not_recorded'))
    if new['fact'].split(':')[0] not in target:
        assert old == new
deps = collections.defaultdict(set)
for row in links:
    deps[row['fact_id']].add(row['first_id'])
assert len(links) == len({tuple(r.values()) for r in links})
assert len({r['first_id'] for r in links}) == 2014
for row in facts:
    assert int(row['objects']) == len(deps[row['fact'].split(':')[0]])
for name in ('tables/missing-row-map.tsv', 'checks/match-scope.tsv', 'checks/sudo-scope.tsv'):
    assert (HERE / name).read_bytes() == (ROOT / 'S4/fix-s4-p-2' / name).read_bytes()
attempts = read(HERE / 'checks/attempt-basis.tsv')
assert {r['fact_id'] for r in attempts} == target
for fact in target:
    rows = [r for r in attempts if r['fact_id'] == fact]
    if state_by_id[fact]['status'] == 'not-obtainable':
        failed = [r for r in rows if r['status'] == 'failed-to-record-complete-fact']
        assert len({r['method'] for r in failed}) >= 3, fact
    else:
        assert any(r['status'] == 'recorded' for r in rows), fact
    for row in rows:
        for name in row['evidence'].split(';'):
            assert (ROOT / name.split('#')[0]).is_file(), name
for name in ('MISSING.tsv', 'fact-status.tsv'):
    assert (ROOT / 'S4' / name).read_bytes() == (HERE / 'tables' / name).read_bytes()
for name in ('READY.md', 'COLLECT.md', 'MATCH.md', 'COMMANDS.md', 'HANDOFF.md'):
    assert (ROOT / 'S4' / name).read_bytes() == (HERE / name).read_bytes()
allowed = {'S4/' + name for name in ('READY.md', 'MISSING.tsv', 'fact-status.tsv', 'COLLECT.md',
                                    'MATCH.md', 'COMMANDS.md', 'PUBLISH.list', 'input-files.sha256.tsv')}
baseline = read(HERE / 'raw/before.sha256.tsv') + read(HERE / 'raw/fixed-inputs.before.sha256.tsv')
changed = set()
for row in baseline:
    path = ROOT / row['path']
    assert path.is_file(), row['path']
    if hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
        changed.add(row['path'])
assert changed <= allowed, sorted(changed - allowed)
counts = collections.Counter(r['status'] for r in states)
assert not {'attempt evidence incomplete', 'not rehearsed'} & counts.keys()
expected = f'STEP 4 INPUTS: 4 of 5 systems ready; {counts["recordable"]} of 45 missing facts can be recorded'
assert (HERE / 'READY.md').read_text().splitlines()[0] == expected
result = {'date_utc': '2026-11-23', 'fact_groups': 45, 'statuses': dict(counts),
          'completed_target_groups': sorted(target), 'dependent_ids': 2014,
          'matching_scope_files_preserved': True, 'baseline_files_checked': len(baseline),
          'allowed_active_files_changed': sorted(changed), 'earlier_rounds_preserved': True,
          'collector_and_matcher_preserved': True, 'independent_acceptance': 'pending separate review'}
with args.report.open('x') as stream:
    stream.write(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))

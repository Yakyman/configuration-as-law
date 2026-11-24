#!/usr/bin/env python3
"""Check changed statuses, count preservation, action citation and frozen bytes."""
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
parser.add_argument('report', type=Path, help='Must not exist')
args = parser.parse_args()
if args.report.exists():
    raise SystemExit('report already exists')
facts = read(HERE / 'tables/MISSING.tsv')
status = read(HERE / 'tables/fact-status.tsv')
links = read(HERE / 'tables/missing-row-map.tsv')
old_status = read(ROOT / 'S4/fix-s4-p-1/tables/fact-status.tsv')
audit = read(HERE / 'checks/status-basis.tsv')
assert list(facts[0]) == ['machine', 'fact', 'objects', 'why_not_recorded', 'how_recorded_now']
assert len(status) == len(facts) == 45
counts = collections.Counter(row['status'] for row in status)
assert counts == {'recordable': 18, 'partial': 12, 'not-obtainable': 1,
                  'attempt evidence incomplete': 12, 'not rehearsed': 2}
assert {r['fact_id'] for r in audit} == {r['fact_id'] for r in old_status if r['status'] == 'not-obtainable'}
assert len(audit) == 15
by_fact = {r['fact_id']: r for r in status}
assert {r['fact_id'] for r in status if r['status'] == 'not-obtainable'} == {'V02'}
assert {r['fact_id'] for r in status if r['status'] == 'not rehearsed'} == {'V09', 'M14'}
for row in audit:
    assert row['basis'] and row['status'] == by_fact[row['fact_id']]['status']
for row in old_status:
    if row['status'] != 'not-obtainable':
        assert row == by_fact[row['fact_id']]
deps = collections.defaultdict(set)
for row in links:
    deps[row['fact_id']].add(row['first_id'])
assert len(links) == len({tuple(r.values()) for r in links})
assert {r['fact'].split(':')[0] for r in facts} == set(by_fact)
for row in facts:
    assert int(row['objects']) == len(deps[row['fact'].split(':')[0]])
assert len({r['first_id'] for r in links}) == 2014
# Existing scope calculations are copied, not rerun or changed.
for name in ('tables/missing-row-map.tsv', 'checks/match-scope.tsv', 'checks/sudo-scope.tsv', 'MATCH.md'):
    assert (HERE/name).read_bytes() == (ROOT/'S4/fix-s4-p-1'/name).read_bytes()

void_root = ROOT / 'S4/rehearsal/void/round3'
with (void_root / 'actions.tsv').open(newline='') as stream:
    actions = list(csv.reader(stream, delimiter='\t'))
assert len(actions) == 12 and all(row[1] == '0' for row in actions)
transport = read(void_root / 'status.tsv')
named = ['action-language_install_node', 'action-language_npm_install', 'action-language_cowsay']
assert all(next(r for r in transport if r['operation'] == name)['exit_status'] == '1' for name in named)
runner = (ROOT/'S4/rehearsal/void/run-round3.py').read_text().splitlines()
assert 'for name in ' in runner[38] and "'cat " in runner[39] and "'.stderr" in runner[39]

baseline = read(HERE / 'raw/before.sha256.tsv')
changed = [r['path'] for r in baseline
           if hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest() != r['sha256']]
assert changed == ['S4/READY.md'], changed
assert (ROOT/'S4/READY.md').read_bytes() == (HERE/'READY.md').read_bytes()
ready = (HERE/'READY.md').read_text()
assert ready.splitlines()[0] == 'STEP 4 INPUTS: 4 of 5 systems ready; 18 of 45 missing facts can be recorded'
assert 'all twelve action-status rows passed (actions.tsv)' in ready
assert '18 recordable, 12 partial, 1 not-obtainable, 12 attempt evidence incomplete, 2 not rehearsed' in ready
result = {'date_utc': '2026-11-23', 'fact_groups': len(facts), 'statuses': dict(counts),
          'all_15_previous_not_obtainable_groups_audited': True,
          'distinct_dependent_ids': 2014, 'matching_scope_files_byte_identical': True,
          'void_action_rows': 12, 'void_action_zero_exits': 12, 'stderr_read_exit_1_rows': named,
          'baseline_files_checked': len(baseline), 'baseline_files_changed': changed,
          'collector_runtime_changed': False, 'live_queries': 0,
          'independent_acceptance': 'not performed by this check'}
with args.report.open('x') as stream:
    stream.write(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))

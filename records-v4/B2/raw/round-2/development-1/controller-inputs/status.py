#!/usr/bin/env python3
"""Read existing baseline logs only; starts no guest or test."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
raw = root/'raw/round-0'
suite = raw/'round-4/baseline'
if not suite.exists():
    suite = root/'raw/round-4/baseline'
result = {}
regressions = suite/'regressions'
if not regressions.exists():
    regressions = root/'raw/round-3/bc4-baseline'
paths = {n:suite/(n+'.jsonl') for n in ('language','applications','system','ordinary')}
paths.update({n:regressions/(n+'.jsonl') for n in ('round1','round2','round3','powercuts','inventory')})
for name, path in paths.items():
    if not path.exists():
        continue
    count = 0
    failed = []
    latest = None
    with path.open() as stream:
        for text in stream:
            try:
                row = json.loads(text)
            except (ValueError, TypeError):
                continue
            if not isinstance(row, dict):
                continue
            latest = row.get('id', latest)
            passed = row.get('passed', row.get('ok'))
            if 'id' in row and isinstance(passed, bool):
                count += 1
                if not passed:
                    failed.append(row.get('id'))
    result[name] = {'observed_assertions':count,'failed':failed,'latest':latest}
for name in ('summary.json','steps.json'):
    if (raw/name).exists():
        result[name] = json.loads((raw/name).read_text())
for name in ('events.jsonl',):
    if (suite/name).exists():
        lines = (suite/name).read_text().splitlines()
        if lines:
            result['latest_controller_event'] = json.loads(lines[-1])
for name, path in (
    ('latest_regression_event', suite/'regressions-console.jsonl'),
    ('latest_original_stage', regressions/'original-console.log'),
    ('latest_combined_event', raw/'round-4/combined/events.jsonl'),
    ('latest_combined_event', root/'raw/round-4/combined/events.jsonl'),
):
    if path.is_file():
        lines = path.read_text().splitlines()
        if lines:
            try:
                result[name] = json.loads(lines[-1])
            except ValueError:
                result[name] = lines[-1]
print(json.dumps(result, sort_keys=True))

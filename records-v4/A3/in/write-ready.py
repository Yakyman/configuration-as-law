#!/usr/bin/env python3
"""Assemble factual summaries from saved inventories and operator records."""
import collections
import csv
import datetime
import json
from pathlib import Path
root = Path(__file__).resolve().parent
machines = ['developer', 'gaming', 'server']
complete = [m for m in machines if (root / ('counts-' + m + '.json')).exists()]
lines = [f'INVENTORY: {len(complete)} of 3 machines', '', '# A3-I operator record', '',
         'This investigation is beyond the published plan, reported separately under PROTOCOL.md Section 5. It is not an outcome of any of the four checks. Inventory count denotes collected lived/base pairs and completed derived tables, not universal fact coverage or a hypothesis result.', '',
         'Inputs: gate commit `3e0207b104f9718793c5b2678810936c7c3c14d2`. Required action/helper/collector checksums passed before execution; see [INPUTS.md](INPUTS.md) and [input-verification.tsv](input-verification.tsv). The PUBLISH.list self-checksum differs from its recorded checksum; the actual named executable inputs match. Outer SSH used the existing user configuration explicitly after the system configuration was rejected; no host configuration was changed.', '',
         'Method: [REDUCTION.md](REDUCTION.md), [reduce.py](reduce.py). Fact locations and uncertainty: [FACTS.md](FACTS.md). Synthetic reduction checks: [reduction-test.txt](reduction-test.txt). Independent review: [REVIEW.md](REVIEW.md). All raw collector files are retained unchanged, including nonzero query outputs and incomplete/unknown facts. No failed action is repaired, replaced or repeated.', '']
for machine in machines:
    lines += ['## ' + machine, '']
    op = root / 'operator' / machine
    if machine not in complete:
        lines += ['Operation or transfer/reduction is still in progress.', '']
        continue
    counts = json.loads((root / ('counts-' + machine + '.json')).read_text())
    action_paths = [p for p in op.rglob('actions-status.tsv') if p.is_file()]
    if not action_paths:
        raise RuntimeError('Missing actions status: ' + machine)
    action_path = min(action_paths, key=lambda p: len(p.parts))
    with action_path.open(newline='') as stream:
        actions = list(csv.reader(stream, delimiter='\t'))
    lines += [f"Objects: **{counts['before']} before → {counts['after']} after**; {counts['dropped']} base-equal rows removed. Untouched base: {counts['base_objects']} objects. Table: [part-{machine}.tsv](part-{machine}.tsv); row-level comparison: [reduction-{machine}.tsv](reduction-{machine}.tsv).", '',
              f"Actions: {sum(r[1] == '0' for r in actions)}/{len(actions)} succeeded. Exact statuses: [{action_path.relative_to(root)}]({action_path.relative_to(root)}). Separate stdout/stderr and lifecycle/restart/destruction records: [operator/{machine}/REPORT.md](operator/{machine}/REPORT.md).", '',
              '| Action | Exit status | Seconds |', '|---|---:|---:|']
    lines += ['| ' + ' | '.join(row) + ' |' for row in actions]
    lines += ['', '| Inventory | Filesystem complete | Ownership complete | Recorded gaps | Nonzero queries |', '|---|---|---|---:|---:|']
    for name in (machine, machine + '-base'):
        folder = root / 'raw' / name
        metadata = json.loads((folder / 'metadata.json').read_text())
        with (folder / 'coverage.tsv').open(newline='') as stream:
            coverage = list(csv.DictReader(stream, delimiter='\t'))
        failures = sum(r['exit_status'] != '0' for r in coverage)
        lines += [f"| [{name}](raw/{name}/metadata.json) | {str(metadata['filesystem_complete']).lower()} | {str(metadata['package_ownership_complete']).lower()} | {len(metadata['gaps'])} | {failures} |"]
    lines += ['', 'The collector metadata retains `ready_for_observation=false`; the operator does not override it. Coverage includes missing or unavailable interfaces; precise status, stderr and gap references remain in each raw inventory. A zero collector exit is not a claim that every fact was collected.', '',
              '| Level:kind | Before | After |', '|---|---:|---:|']
    for kind, values in counts['by_kind'].items():
        lines += [f"| {kind} | {values['before']} | {values['after']} |"]
    lines += ['', f"Execution details and every machine-specific deviation are recorded in [operator/{machine}/REPORT.md](operator/{machine}/REPORT.md). The following operator record is reproduced to keep this report self-contained; paths within that record are relative to operator/{machine}/:", '']
    report = (op / 'REPORT.md').read_text().splitlines()
    lines += [line for line in report if not line.startswith('#')]
    lines += ['']
lines += ['Recorded in UTC: ' + datetime.datetime.now(datetime.timezone.utc).isoformat(), '']
(root / 'READY.md').write_text('\n'.join(lines))

#!/usr/bin/env python3
"""Print every case ID of CASES.md in its order: the first cell of every table row (ranges expanded).

`P4-C6-1..4` -> P4-C6-1 … P4-C6-4; `P2-ADD-1, -2, -3` -> P2-ADD-1 P2-ADD-2 P2-ADD-3. Rows of the Notation table
(first cell in backticks) and header rows are skipped."""
import re
import sys

ids = []
for line in open(sys.argv[1], encoding='utf-8'):
    if not line.startswith('| '):
        continue
    cell = line.split('|')[1].strip()
    if not cell or cell.startswith('`') or cell in ('ID', 'Step') or set(cell) <= set('-: '):
        continue
    m = re.fullmatch(r'(.*-)(\d+)\.\.(\d+)', cell)
    if m:
        ids += [f'{m.group(1)}{n}' for n in range(int(m.group(2)), int(m.group(3)) + 1)]
        continue
    if ',' in cell:
        parts = [p.strip() for p in cell.split(',')]
        stem = re.fullmatch(r'(.*-)(\d+)', parts[0])
        ids.append(parts[0])
        ids += [stem.group(1) + p[1:] for p in parts[1:]]
        continue
    ids.append(cell)
print('\n'.join(ids))

#!/usr/bin/env python3
"""Print the rpm package (if any) whose file list (raw/0017-package-files-rpm.out) contains each path given,
also trying the /lib64 alias of /usr/lib64."""
import sys
RAW = '<HOME>/Projects/ideas/cal-paper/night-1123/A3/in/raw/developer/raw/0017-package-files-rpm.out'
want = {}
for p in sys.argv[1:]:
    want[p] = p
    if p.startswith('/usr/lib64/'):
        want['/lib64/' + p[len('/usr/lib64/'):]] = p
found = {}
with open(RAW, errors='replace') as f:
    for line in f:
        parts = line.rstrip('\n').split('\t')
        if len(parts) > 1 and parts[1] in want:
            found.setdefault(want[parts[1]], []).append(parts[0])
for p in sys.argv[1:]:
    print(p, '\t', ','.join(sorted(set(found.get(p, [])))) or '-')

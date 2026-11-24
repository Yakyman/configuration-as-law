#!/usr/bin/env python3
"""For each gem package row, find a gemspec path in the rpm file list (raw/0017) and its package."""
import csv, json, re, collections
IN = '<HOME>/Projects/ideas/cal-paper/night-1123/A3/in/'
csv.field_size_limit(10**9)
gems = [x['name'][4:] for x in csv.DictReader(open(IN + 'part-developer.tsv'), delimiter='\t') if x['name'].startswith('gem:')]
spec = collections.defaultdict(list)
with open(IN + 'raw/developer/raw/0017-package-files-rpm.out', errors='replace') as f:
    for line in f:
        p = line.split('\t')
        if len(p) > 1 and p[1].endswith('.gemspec'):
            spec[p[1].rsplit('/', 1)[1][:-8]].append((p[0], p[1]))
for g in gems:
    print(g, spec.get(g, '-')[:1])

#!/usr/bin/env python3
"""Dump every member of every stored group of part-developer with its group id and ctime (from configuration-origin.tsv)."""
import csv, json, sys

IN = '<HOME>/Projects/ideas/cal-paper/night-1123/A3/in/'
RAW = IN + 'raw/developer/'
csv.field_size_limit(10**9)
ctime = {}
for row in csv.DictReader(open(RAW + 'configuration-origin.tsv'), delimiter='\t'):
    ctime[row['path']] = row['ctime']
out = csv.writer(open(sys.argv[1], 'w'), delimiter='\t', lineterminator='\n')
out.writerow(['gid', 'group', 'path', 'type', 'mode', 'owner', 'size', 'mtime', 'exec', 'signature', 'persistence', 'ctime'])
for x in csv.DictReader(open(IN + 'part-developer.tsv'), delimiter='\t'):
    if not x['kind'].startswith('2:stored'):
        continue
    m = json.loads(x['members'])
    rows = list(csv.reader(open(RAW + m['file']), delimiter='\t'))[1:]
    assert len(rows) == m['count'], x['id']
    for f in rows:
        out.writerow([x['id'], x['name']] + f + [ctime.get(f[0], '')])

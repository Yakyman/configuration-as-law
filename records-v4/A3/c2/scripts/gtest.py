#!/usr/bin/env python3
"""Apply member rules to every member; report unmatched members and counts per label."""
import collections, csv, sys
sys.path.insert(0, '<HOME>/Projects/ideas/cal-paper/night-1123/A3/c2/scripts')
from gclassify import classify

N = '<HOME>/Projects/ideas/cal-paper/night-1123/A3/c2/raw/gaming-members.tsv'
c = collections.Counter()
none = []
for x in csv.DictReader(open(N), delimiter='\t'):
    m = dict(path=x['path'], type=x['type'], exec=x['exec'], ctime=x['ctime'], pkg=x['pkg'], integrity=x['integrity'],
             target=x['target'], size=x['size'], persistence=x['persistence'], shebang=x['shebang'])
    r = classify(m)
    if r is None:
        none.append(x['path'])
    else:
        c[(r[0], r[5])] += 1
for k, v in sorted(c.items()):
    print(v, k)
print('UNMATCHED', len(none))
for p in none[:80]:
    print('  ', p)

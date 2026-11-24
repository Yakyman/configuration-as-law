#!/usr/bin/env python3
import csv, sys, collections
sys.path.insert(0, '<HOME>/Projects/ideas/cal-paper/night-1123/A3/c2/scripts')
from members_rules import classify
csv.field_size_limit(10**9)
cnt = collections.Counter()
none = []
labels = collections.Counter()
for m in csv.DictReader(open('/tmp/c2dev/members.tsv'), delimiter='\t'):
    if not m['group'].startswith('/home'):
        continue
    r = classify(m)
    if r is None:
        none.append(m['path'])
        continue
    cnt[r[0]] += 1
    labels[(r[0], r[1])] += 1
print(cnt)
for k, v in sorted(labels.items()):
    print(v, k)
print('NONE', len(none))
for p in none[:80]:
    print('  ', p)

#!/usr/bin/env python3
"""For every member rule (label), pick up to 10 rows of part-gaming whose decision rests on that rule
(code rows directly, group rows through a member) and print id, path, type, ctime, pkg, integrity, decision."""
import collections, csv, random, sys
sys.path.insert(0, '<HOME>/Projects/ideas/cal-paper/night-1123/A3/c2/scripts')
from gmain import members, mclass

random.seed(1123)
by = collections.defaultdict(list)
for gid, ms in members.items():
    for x in ms:
        r = mclass(x)
        by[r[5]].append((gid, x, r))
out = open('<HOME>/Projects/ideas/cal-paper/night-1123/A3/c2/raw/gaming-rule-checks.tsv', 'w')
out.write('rule\tdecision\trow_id\tpath\ttype\tctime\tpkg\tintegrity\ttarget\n')
for lab, lst in sorted(by.items()):
    seen, pick = set(), []
    random.shuffle(lst)
    for gid, x, r in lst:
        if gid in seen:
            continue
        seen.add(gid)
        pick.append((gid, x, r))
        if len(pick) == 10:
            break
    for gid, x, r in pick:
        out.write('\t'.join([lab, r[0], gid, x['path'], x['type'], x['ctime'][:19], x['pkg'], x['integrity'], x['target']]) + '\n')
print(len(by), 'rules')

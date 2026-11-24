#!/usr/bin/env python3
"""Verify A3/c2/part-developer.tsv against the input and write part-developer.done with counts per decision."""
import csv, collections, sys
NIGHT = '<HOME>/Projects/ideas/cal-paper/night-1123/'
csv.field_size_limit(10**9)
DEC = ['INSTALLED-OWN', 'INSTALLED-PACKAGE', 'INSTALLED-DERIVED', 'PROGRAM-OWN', 'PROGRAM-DERIVED', 'SETTING-OWN',
       'SETTING-DEFAULT', 'RECORD', 'MATERIAL', 'RUNTIME', 'ACTION', 'GAP-NONE', 'GAP-TWO', 'UNKNOWN', 'MIXED']
inp = [r['id'] for r in csv.DictReader(open(NIGHT + 'A3/in/part-developer.tsv'), delimiter='\t')]
lines = open(NIGHT + 'A3/c2/part-developer.tsv', encoding='utf-8').read().split('\n')
assert lines[-1] == ''
header = lines[0]
assert header == 'id\tdecision\tsentences\twhat_it_does\tbasis\treason', header
out_ids, decs, errors = [], collections.Counter(), []
for ln in lines[1:-1]:
    f = ln.split('\t')
    if len(f) != 6:
        errors.append('fields: ' + ln[:80])
        continue
    out_ids.append(f[0])
    if f[1] not in DEC:
        errors.append('decision: ' + f[1])
    decs[f[1]] += 1
    if len(f[3].split()) > 15 or len(f[5].split()) > 30:
        errors.append('length: ' + f[0])
    if not f[2] or not f[4]:
        errors.append('empty: ' + f[0])
dup = [k for k, v in collections.Counter(out_ids).items() if v > 1]
missing = set(inp) - set(out_ids)
extra = set(out_ids) - set(inp)
print('input rows', len(inp), 'output rows', len(out_ids), 'unique', len(set(out_ids)))
print('duplicates', len(dup), 'missing', len(missing), 'extra', len(extra), 'errors', len(errors))
for e in errors[:10]:
    print('  ', e)
ok = not dup and not missing and not extra and not errors and len(inp) == len(out_ids)
print('OK' if ok else 'FAIL')
if ok and '--done' in sys.argv:
    with open(NIGHT + 'A3/c2/part-developer.done', 'w') as f:
        f.write('rows\t%d\n' % len(out_ids))
        for d in DEC:
            f.write('%s\t%d\n' % (d, decs.get(d, 0)))
    print(open(NIGHT + 'A3/c2/part-developer.done').read())

#!/usr/bin/env python3
"""Verify A3/c2/part-gaming.tsv against the input and write A3/c2/part-gaming.done."""
import collections, csv, sys
N = '<HOME>/Projects/ideas/cal-paper/night-1123/'
csv.field_size_limit(10**9)
WORDS = {'INSTALLED-OWN', 'INSTALLED-PACKAGE', 'INSTALLED-DERIVED', 'PROGRAM-OWN', 'PROGRAM-DERIVED', 'SETTING-OWN',
         'SETTING-DEFAULT', 'RECORD', 'MATERIAL', 'RUNTIME', 'ACTION', 'GAP-NONE', 'GAP-TWO', 'UNKNOWN', 'MIXED'}
HEAD = ['id', 'decision', 'sentences', 'what_it_does', 'basis', 'reason']
inp = [x['id'] for x in csv.DictReader(open(N + 'A3/in/part-gaming.tsv'), delimiter='\t')]
lines = open(N + 'A3/c2/part-gaming.tsv', encoding='utf-8').read().split('\n')
assert lines[-1] == ''
lines = lines[:-1]
assert lines[0].split('\t') == HEAD, lines[0]
ids, dec, bad = [], collections.Counter(), []
for i, l in enumerate(lines[1:], 2):
    f = l.split('\t')
    if len(f) != 6:
        bad.append((i, 'fields', len(f)))
        continue
    ids.append(f[0])
    dec[f[1]] += 1
    if f[1] not in WORDS:
        bad.append((i, 'decision', f[1]))
    if len(f[3].split()) > 15:
        bad.append((i, 'what>15'))
    if len(f[5].split()) > 30:
        bad.append((i, 'reason>30'))
    if not f[2] or not f[4]:
        bad.append((i, 'empty sentences/basis'))
c = collections.Counter(ids)
dup = [k for k, v in c.items() if v > 1]
print('input rows', len(inp), 'output rows', len(ids), 'same set', set(inp) == set(ids), 'duplicates', len(dup),
      'input duplicates', len(inp) - len(set(inp)), 'problems', len(bad))
for b in bad[:20]:
    print(b)
ok = set(inp) == set(ids) and len(ids) == len(inp) and not dup and not bad
if ok:
    with open(N + 'A3/c2/part-gaming.done', 'w') as f:
        for k, v in sorted(dec.items()):
            f.write('%s\t%d\n' % (k, v))
        f.write('TOTAL\t%d\n' % len(ids))
    print('done file written')
else:
    sys.exit(1)

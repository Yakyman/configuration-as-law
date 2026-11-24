import csv, sys
from collections import Counter
csv.field_size_limit(10**9)
IN, OUT, DONE = sys.argv[1:4]
WORDS = {'INSTALLED-OWN', 'INSTALLED-PACKAGE', 'INSTALLED-DERIVED', 'PROGRAM-OWN', 'PROGRAM-DERIVED', 'SETTING-OWN',
         'SETTING-DEFAULT', 'RECORD', 'MATERIAL', 'RUNTIME', 'ACTION', 'GAP-NONE', 'GAP-TWO', 'UNKNOWN', 'MIXED'}
inp = [r['id'] for r in csv.DictReader(open(IN), delimiter='\t')]
lines = open(OUT, encoding='utf-8').read().splitlines()
assert lines[0] == 'id\tdecision\tsentences\twhat_it_does\tbasis\treason', 'header'
rows = [l.split('\t') for l in lines[1:]]
assert all(len(r) == 6 for r in rows), 'field count'
out = [r[0] for r in rows]
assert len(out) == len(set(out)), 'duplicate ids'
assert len(inp) == len(set(inp)) and set(inp) == set(out) and len(inp) == len(out), 'id sets differ'
bad = [r for r in rows if r[1] not in WORDS]
assert not bad, bad
c = Counter(r[1] for r in rows)
with open(DONE, 'w') as f:
    for k in sorted(c):
        f.write(f'{k}\t{c[k]}\n')
    f.write(f'TOTAL\t{len(rows)}\n')
print('OK', len(rows), dict(c))

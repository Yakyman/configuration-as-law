import csv, sys
from collections import Counter
inp = [r['id'] for r in csv.DictReader(open('../in/part-mint.tsv', encoding='utf-8'), delimiter='\t')]
lines = open('part-mint.tsv', encoding='utf-8').read().split('\n')
assert lines[0] == 'id\tdecision\tsentences\twhat_it_does\tbasis\treason', 'header'
body = [l.split('\t') for l in lines[1:] if l]
assert all(len(b) == 6 for b in body), 'field count'
out = [b[0] for b in body]
ok = sorted(inp) == sorted(out) and len(out) == len(set(out)) == len(inp)
bad = [b for b in body if b[1] not in ('MUST', 'NOT', 'HOLE', 'UNKNOWN', 'MIXED')]
c = Counter(b[1] for b in body)
print('ids_equal', ok, 'in', len(inp), 'out', len(out), 'unique', len(set(out)), 'bad_decisions', len(bad))
print(dict(c))
if not ok or bad: sys.exit(1)

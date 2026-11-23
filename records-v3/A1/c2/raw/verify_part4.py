import csv, sys, collections
inp, out, done = sys.argv[1:4]
ins = [r['id'] for r in csv.DictReader(open(inp, encoding='utf-8'), delimiter='\t')]
f = open(out, encoding='utf-8')
header = f.readline().rstrip('\n')
assert header == 'id\tdecision\tsentences\twhat_it_does\tbasis\treason', header
rows = [l.rstrip('\n').split('\t') for l in f]
assert all(len(r) == 6 for r in rows), 'field count'
outs = [r[0] for r in rows]
assert len(outs) == len(set(outs)), 'duplicate ids'
assert sorted(outs) == sorted(ins) and len(outs) == len(ins), 'id sets differ'
words = {'MUST', 'NOT', 'HOLE', 'UNKNOWN', 'MIXED'}
assert all(r[1] in words for r in rows), 'bad decision'
long_what = [r[0] for r in rows if len(r[3].split()) > 15]
long_reason = [r[0] for r in rows if len(r[5].split()) > 30]
print('rows', len(rows), 'long what', long_what, 'long reason', sorted(set(long_reason)))
c = collections.Counter(r[1] for r in rows)
if not long_what and not long_reason:
    with open(done, 'w') as g:
        for k in ['MUST', 'NOT', 'HOLE', 'UNKNOWN', 'MIXED']:
            g.write(f'{k}\t{c[k]}\n')
        g.write(f'TOTAL\t{len(rows)}\n')
print(dict(c))

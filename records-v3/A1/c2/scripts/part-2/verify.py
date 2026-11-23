"""Verify c2/part-2.tsv against in/part-2.tsv and write c2/part-2.done. Run from A1/."""
import csv, collections, sys
inp = [r for r in csv.reader(open('in/part-2.tsv', encoding='utf-8'), delimiter='\t')]
lines = open('c2/part-2.tsv', encoding='utf-8').read().rstrip('\n').split('\n')
hdr = lines[0].split('\t')
assert hdr == ['id', 'decision', 'sentences', 'what_it_does', 'basis', 'reason'], hdr
out = [l.split('\t') for l in lines[1:]]
ok = True
for r in out:
    if len(r) != 6:
        print('bad field count', r[0]); ok = False
ids_in = [r[0] for r in inp[1:]]
ids_out = [r[0] for r in out]
if collections.Counter(ids_out) != collections.Counter(ids_in):
    print('id mismatch'); ok = False
dup = [k for k, v in collections.Counter(ids_out).items() if v > 1]
if dup:
    print('duplicates', dup); ok = False
if len(ids_out) != len(ids_in) or set(ids_out) != set(ids_in):
    print('count/set mismatch', len(ids_out), len(ids_in)); ok = False
bad = [r[0] for r in out if r[1] not in ('MUST', 'NOT', 'HOLE', 'UNKNOWN', 'MIXED')]
if bad:
    print('bad decisions', bad); ok = False
long_ = [r[0] for r in out if len(r[3].split()) > 15 or len(r[5].split()) > 30]
if long_:
    print('too long', long_); ok = False
if not ok:
    sys.exit(1)
c = collections.Counter(r[1] for r in out)
with open('c2/part-2.done', 'w', encoding='utf-8') as f:
    f.write('rows %d\n' % len(out))
    for k in ('MUST', 'NOT', 'HOLE', 'UNKNOWN', 'MIXED'):
        f.write('%s %d\n' % (k, c.get(k, 0)))
print(open('c2/part-2.done').read())

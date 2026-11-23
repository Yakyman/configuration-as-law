import csv,sys,collections
csv.field_size_limit(10**9)
a=[r['id'] for r in csv.DictReader(open(sys.argv[1]),delimiter='\t')]
rows=list(csv.reader(open(sys.argv[2]),delimiter='\t'))
assert rows[0]==['id','decision','sentences','what_it_does','basis','reason'], rows[0]
b=[r[0] for r in rows[1:]]
assert all(len(r)==6 for r in rows), 'field count'
assert len(b)==len(set(b)), 'duplicate ids'
assert len(a)==len(b) and set(a)==set(b), 'id set differs'
c=collections.Counter(r[1] for r in rows[1:])
assert set(c)<= {'MUST','NOT','HOLE','UNKNOWN','MIXED'}, c
for d in ('MUST','NOT','HOLE','UNKNOWN','MIXED'): print(d, c.get(d,0))
print('TOTAL', len(b))

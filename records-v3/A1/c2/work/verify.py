import csv,collections
inp=[r[0] for r in csv.reader(open('in/part-1.tsv'),delimiter='\t')][1:]
out=list(csv.reader(open('c2/part-1.tsv'),delimiter='\t'))
assert out[0]==['id','decision','sentences','what_it_does','basis','reason'], out[0]
ids=[r[0] for r in out[1:]]
c=collections.Counter(ids)
print('in',len(inp),'out',len(ids),'dups',[k for k,v in c.items() if v>1][:5])
print('missing',sorted(set(inp)-set(ids))[:20],len(set(inp)-set(ids)))
print('extra',sorted(set(ids)-set(inp))[:5])
bad=[r for r in out[1:] if len(r)!=6 or r[1] not in ('MUST','NOT','HOLE','UNKNOWN','MIXED')]
print('bad',len(bad))
ok = len(inp)==len(ids) and set(inp)==set(ids) and not bad and all(v==1 for v in c.values())
print('OK' if ok else 'FAIL')
print(collections.Counter(r[1] for r in out[1:]))

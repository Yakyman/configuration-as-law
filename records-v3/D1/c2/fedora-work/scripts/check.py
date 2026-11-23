import csv,sys,collections
csv.field_size_limit(10**9)
inp=[r['id'] for r in csv.DictReader(open(sys.argv[1]),delimiter='\t')]
lines=open(sys.argv[2]).read().split('\n')
assert lines[0]=='id\tdecision\tsentences\twhat_it_does\tbasis\treason', 'header'
out=[l.split('\t') for l in lines[1:] if l]
bad=[o for o in out if len(o)!=6]; print('bad field counts',len(bad))
ids=[o[0] for o in out]
print('input rows',len(inp),'unique',len(set(inp)),'output rows',len(ids),'unique',len(set(ids)))
print('same set',set(inp)==set(ids),'dupes',[i for i,c in collections.Counter(ids).items() if c>1][:5])
dec=collections.Counter(o[1] for o in out); print(dict(dec))
print('invalid decisions',[d for d in dec if d not in ('MUST','NOT','HOLE','UNKNOWN','MIXED')])
print('what>15',sum(len(o[3].split())>15 for o in out),'reason>30',sum(len(o[5].split())>30 for o in out))
for o in out:
    if len(o[3].split())>15 or len(o[5].split())>30: print('  LONG',o[0],len(o[3].split()),len(o[5].split()),o[3][:60],'|',o[5][:80])

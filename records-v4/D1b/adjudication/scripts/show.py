import csv,sys,random
csv.field_size_limit(sys.maxsize)
rows=list(csv.DictReader(open('D1b/compare/to-adjudicate.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE))
kind,d1,d2=sys.argv[1],sys.argv[2],sys.argv[3]
n=int(sys.argv[4]) if len(sys.argv)>4 else 2
w=int(sys.argv[5]) if len(sys.argv)>5 else 700
sel=[r for r in rows if (kind=='*' or r['kind']==kind) and (d1=='*' or r['c1_decision']==d1) and (d2=='*' or r['c2_decision']==d2)]
random.seed(1)
for r in random.sample(sel,min(n,len(sel))):
    print('=====')
    for k,v in r.items(): print(f'{k}: {v[:w]}')

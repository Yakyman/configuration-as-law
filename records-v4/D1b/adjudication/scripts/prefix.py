import csv,sys,collections
csv.field_size_limit(sys.maxsize)
rows=list(csv.DictReader(open('D1b/compare/to-adjudicate.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE))
depth=int(sys.argv[1])
c=collections.Counter()
for r in rows:
    if not r['kind'].startswith('L2'): continue
    p='/'.join(r['name'].split('/')[:depth+1])
    c[(r['machine'],p,r['c1_decision'],r['c2_decision'])]+=1
for k,v in sorted(c.items()): print(v,k)

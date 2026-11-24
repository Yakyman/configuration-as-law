import csv,sys,collections
csv.field_size_limit(sys.maxsize)
rows=list(csv.DictReader(open('D1b/compare/to-adjudicate.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE))
print(len(rows), list(rows[0].keys()))
c=collections.Counter((r['machine'],r['kind'],r['c1_decision'],r['c2_decision']) for r in rows)
for k,v in sorted(c.items(),key=lambda x:-x[1]): print(v,k)

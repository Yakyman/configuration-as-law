import csv,sys
csv.field_size_limit(sys.maxsize)
rows=list(csv.DictReader(open('D1b/compare/to-adjudicate.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE))
out=open('D1b/adjudication/raw/other-rows.txt','w')
n=0
for r in rows:
    nm=r['name']
    if nm.startswith('/var/db/repos/') or nm.startswith('/var/db/pkg/'): continue
    n+=1
    out.write(f"{r['id'][4:]}|{r['kind']}|{nm[:110]}\n  C1 {r['c1_decision']}: {r['c1_what'][:120]} || {r['c1_reason'][:260]}\n  C2 {r['c2_decision']}: {r['c2_what'][:120]} || {r['c2_reason'][:260]}\n")
print(n)

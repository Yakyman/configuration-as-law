import csv,sys,collections
csv.field_size_limit(sys.maxsize)
rows=list(csv.DictReader(open('D1b/compare/to-adjudicate.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE))
parts={'A':[], 'B':[], 'C':[], 'SELF':[]}
for r in rows:
    nm=r['name']; k=r['kind']
    if nm.startswith('/var/db/repos/gentoo/') or nm.startswith('/var/db/pkg/'): parts['SELF'].append(r); continue
    if k.startswith('L1:'): parts['A'].append(r)
    elif nm.startswith('/home') or nm.startswith('/var') or nm.startswith('/tmp') or nm.startswith('/opt') or 'container' in k or k in ('L2:image','L2:snapshot'): parts['C'].append(r)
    else: parts['B'].append(r)
for p,rs in parts.items():
    print(p,len(rs),collections.Counter(r['machine'] for r in rs))
    if p!='SELF':
        with open(f'D1b/adjudication/raw/part-{p}.tsv','w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0].keys()),delimiter='\t',quoting=csv.QUOTE_NONE,escapechar=None,quotechar=None)
            w.writeheader(); w.writerows(rs)

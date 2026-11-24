import csv,sys,json,collections,os
csv.field_size_limit(sys.maxsize)
rows=list(csv.DictReader(open('D1b/compare/to-adjudicate.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE))
H='D1b/handoff/gentoo/'
def members(r):
    m=r['members'].replace('\\"','"').strip('"').replace('""','"')
    try: d=json.loads(m)
    except Exception as e: return None
    if isinstance(d,str): d=json.loads(d)
    return d
vc=collections.Counter(); dec=collections.Counter(); bad=0
rc=collections.Counter()
for r in rows:
    nm=r['name']
    if nm.startswith('/var/db/pkg/'):
        dec[(r['c1_decision'],r['c2_decision'])]+=1
        d=members(r)
        if not d or 'file' not in d: bad+=1; print('NOFILE',nm,r['members'][:100]); continue
        for line in list(csv.reader(open(H+d['file']),delimiter='\t'))[1:]:
            b=os.path.basename(line[0])
            if b.endswith('.ebuild'): b='*.ebuild'
            vc[(b,line[1])]+=1
    elif nm.startswith('/var/db/repos/gentoo/'):
        rc[(r['kind'],r['c1_decision'],r['c2_decision'])]+=1
        if r['c2_decision'] in ('SETTING-OWN',): print(r['id'],nm,r['c2_reason'][:300])
print(dec, bad); print(sorted(vc.items(),key=lambda x:-x[1])[:60]); print(rc)

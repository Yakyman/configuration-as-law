"""Whole-table discovery for changed cards; saved data only, no observations."""
import csv, json, re, hashlib
from pathlib import Path
from collections import defaultdict
OUT=Path('D1/fix-d1-h-2/raw')
csv.field_size_limit(10_000_000)
hashes={}
def read(path):
    p=Path(path); hashes[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
    with p.open() as f: return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))
def decode(v):
    v=v.replace('\\"','"')
    for _ in range(3):
        if v.startswith('"') and v.endswith('"'): v=v[1:-1].replace('""','"')
        try: return json.loads(v)
        except ValueError: pass
    raise ValueError('Invalid encoding')
def write(name, rows):
    with (OUT/name).open('x') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
joined=read('D1/compare/joined.tsv'); adj={r['id']:r for r in read('D1/adjudication/rows.tsv')}
tags=defaultdict(list)
for r in read('D1/adjudication/raw/l2o_member_classes.tsv'): tags[r['id']].append(r)
patterns={
'generated': re.compile(r'(?:/mime(?:/|$)|/modules\.[^/]+$|\.lst$|cache|index\.db$|mandoc\.db$|/certs(?:/|$)|ca-certificates|dconf/db|selinux/.*/active(?:/|$)|gschemas\.compiled$|hwdb\.bin$|locale-archive$|/etc/shells$|\.hmac$|swcatalog|loaders|immodules|\.xb$)',re.I),
'archive':re.compile(r'(?:initramfs|initrd|\.xpi$|\.zip$|\.jar$|\.tar(?:\.[^/]*)?$|\.cpio(?:\.[^/]*)?$|\.squashfs$|\.img$|extension|container|L2:image|opaque)',re.I),
}
scanned=[]; candidates=[]; boot=[]; xpi=[]
for r in joined:
    members=[]; source=''
    if r['kind'].startswith('L2:'):
        m=decode(r['members'])
        if 'file' in m:
            source='D1/in/raw/'+r['machine'].removeprefix('d1-')+'/'+m['file']; members=read(source)
    paths=[(r['name'],'row')]+[(m['path'],m.get('type','')) for m in members]
    hits={k: sorted({p for p,t in paths if pat.search(p)}) for k,pat in patterns.items()}
    b=sorted({p for p,t in paths if t!='symlink' and re.search(r'/boot/(?:initramfs-.*\.img|initrd-[^/]+)$',p)})
    x=sorted({p for p,t in paths if p.endswith('.xpi')})
    base={k:r[k] for k in ('id','machine','kind','name')}
    scanned.append(base|{'member_source':source,'paths_examined':len(paths),'generated_match':bool(hits['generated']),'archive_match':bool(hits['archive'] or patterns['archive'].search(r['kind']))})
    for card,match in hits.items():
        if match or (card=='archive' and patterns['archive'].search(r['kind'])) or (card=='generated' and adj.get(r['id'],{}).get('hole')=='2'):
            candidates.append(base|{'family':card,'matching_members':' | '.join(match),'member_source':source,'hole':adj.get(r['id'],{}).get('hole',''),'verdict':adj.get(r['id'],{}).get('verdict','agreement'),'c1':r['c1_decision'],'c2':r['c2_decision'],'member_tags':json.dumps(tags[r['id']],ensure_ascii=False)})
    if b: boot.append(base|{'matching_members':' | '.join(b),'member_source':source})
    if x: xpi.append(base|{'matching_members':' | '.join(x),'member_source':source})
write('whole-table-search.tsv',scanned);write('candidates.tsv',candidates);write('card4-boot-extent.tsv',boot);write('xpi-search.tsv',xpi)
(OUT/'scan-input-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
print(json.dumps({'searched':len(scanned),'candidates':len(candidates),'boot_rows':len(boot),'xpi_rows':len(xpi)}))
for r in candidates:
    if r['family']=='generated' and ('cache' not in r['name'].lower() or '/var/cache/' in r['name'] or r['hole']=='2'):
        print(r['id'],r['hole'],r['verdict'],r['name'])

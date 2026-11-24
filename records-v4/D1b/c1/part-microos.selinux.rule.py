import csv,json,base64
from pathlib import Path
csv.field_size_limit(10000000)
p=Path('D1b/handoff/microos')
read=lambda f:list(csv.DictReader(open(p/f),delimiter='\t'))
rows=[r for r in csv.DictReader(open('D1b/in/part-microos.tsv'),delimiter='\t') if '/selinux/targeted/active/modules/100/' in r['name']]
sf={v['path']:v for v in read('s4-microos-snapshot-files.tsv')}
sc={v['snapshot_path']:v for v in read('s4-microos-snapshot-current.tsv')}
src={v['path']:v for v in read('s4-microos-sources.tsv')}
native={v.split()[1]:v.split() for v in (p/'raw/0157-s4-selinux-modules.out').read_text().splitlines() if v.split()[0]=='100'}
out=Path('D1b/c1/part-microos.selinux.tsv')
header=['id','decision','sentences','what_it_does','basis','reason']
prior=list(csv.DictReader(open(out),delimiter='\t')) if out.exists() else []
seen={r['id'] for r in prior}
with out.open('a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not prior and out.stat().st_size==0:w.writerow(header)
 for row in rows:
  metadata=json.loads(row['members']); members=read(metadata['file'])
  assert metadata['complete'] and metadata['count']==len(members)==3
  assert {v['path'].split('/')[-1] for v in members}=={'cil','hll','lang_ext'}
  assert native[row['name'].split('/')[-1]][2]=='pp'
  for v in members:
   a=sf[v['path']];b=sc[v['path']]
   assert v['persistence']=='persistent'
   assert a['comparison']=='equal' and a['expected']==a['observed'] and len(a['expected'])==64
   assert a['package']=='<REDACTED>' and a['manifest_exit']=='0'
   assert b['comparison']=='equal' and b['snapshot_sha256']==b['current_sha256']==a['expected']
  assert base64.b64decode(src[row['name']+'/lang_ext']['content_base64'])==b'pp'
  if row['id'] not in seen:
   w.writerow([row['id'],'INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16','SELinux policy module representations and format marker retained in the filesystem snapshot.','raw:D1b/handoff/microos/s4-microos-snapshot-files.tsv','All three persistent members match the snapshot RPM manifest unchanged; the first question decides, and the selinux-policy-targeted package line covers them.'])
   f.flush()
result=list(csv.DictReader(open(out),delimiter='\t'))
assert len(result)==len(rows)==441 and len({r['id'] for r in result})==441
assert {r['id'] for r in result}=={r['id'] for r in rows}
assert all(r['decision']=='INSTALLED-PACKAGE' and len(r['what_it_does'].split())<=15 and len(r['reason'].split())<=30 for r in result)
print('INSTALLED-PACKAGE 441')

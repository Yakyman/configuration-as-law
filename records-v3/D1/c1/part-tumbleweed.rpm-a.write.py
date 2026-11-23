import runpy,csv,collections
from pathlib import Path
x=runpy.run_path('D1/c1/part-tumbleweed.rpm-a.classify.py',run_name='read');out=Path('D1/c1/part-tumbleweed.rpm-a.tsv');header=['id','decision','sentences','what_it_does','basis','reason'];seen=set()
if out.exists():seen={r['id'] for r in csv.DictReader(out.open(),delimiter='\t')}
with out.open('a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not seen:w.writerow(header)
 for r in x['rows']:
  if r['id'] in seen:continue
  n=r['name'].split(':',1)[1];z=x['decide'](n,x['m'].get(n,{}))
  if n=='hicolor-icon-theme':continue
  dec,sent,what,reason,rule=z
  url=x['fmeta']['url'] if n in x['files'] else 'https://rpm.org/docs/6.0.x/man/rpmkeys.8'
  if rule=='introspection' or n=='girepository-1_0':url='https://gi.readthedocs.io/en/latest/'
  assert len(what.split())<=15,(n,what)
  assert len(reason.split())<=30,(n,reason)
  w.writerow([r['id'],dec,sent,what,'doc:'+url,reason]);f.flush()
print('written',sum(1 for _ in csv.DictReader(out.open(),delimiter='\t')))

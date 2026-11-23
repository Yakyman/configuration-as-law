import csv,sys,json,collections,pathlib
csv.field_size_limit(sys.maxsize)
a={x['id']:x for x in csv.DictReader(open('D1/adjudication/rows.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE)}
r=list(csv.DictReader(open('D1/compare/joined.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE));d=json.load(open('D1/adjudication/work/A/deps-A.json'));tw=json.load(open('D1/review/cards14-raw/tw-primary-selected.json'));mi=json.load(open('D1/review/cards14-raw/mint-main-metadata.json'))|json.load(open('D1/review/cards14-raw/mint-universe-metadata.json'))
installed={}
for machine,fn in [('fedora','004-packages-root-rpm.out'),('tumbleweed','004-packages-root-rpm.out'),('mint','003-packages-root-dpkg-query.out')]:
 installed[machine]={x.split('\t')[0].split(':')[0]:x.split('\t')[1] for x in open('D1/in/raw/'+machine+'/raw/'+fn) if '\t' in x}
outs=[]
for x in r:
 if a.get(x['id'],{}).get('hole') not in ['1','2']:continue
 n=x['name'].split(':',1)[-1].split(':')[0];m=x['machine'];status='';req=[];version=''
 if m=='fedora':
  v=d.get(n,{});version=v.get('ver','');req=v.get('req',[])+v.get('rec',[])
 elif m=='tumbleweed':
  v=tw.get(n,{});vv=v.get('version',{});version=vv.get('ver','')+'-'+vv.get('rel','');req=[i['name'] for i in v.get('requires',[])+v.get('recommends',[])]
 elif m=='mint':
  v=mi.get(n,{});version=v.get('Version','');req=[v[k] for k in ['Depends','Pre-Depends','Recommends'] if v.get(k)]
 req=[t for t in req if not t.startswith('rpmlib(')]
 match=version==installed.get(m,{}).get(n)
 if not match:status='VERSION-MISSING' if not version.strip('-') else 'VERSION-DIFFERENT'
 elif req:status='MUST-METADATA'
 else:status='NO-REQ'
 outs.append([x['id'],m,n,installed.get(m,{}).get(n,''),version,status,'; '.join(req)])
with open('D1/review/cards14-raw/metadata-audit.tsv','w') as f:
 w=csv.writer(f,delimiter='\t');w.writerow(['id','machine','package','installed_version','evidence_version','metadata_status','requirements']);w.writerows(outs)
print(collections.Counter((x[1],x[5]) for x in outs))
for m in ['fedora','mint','tumbleweed']:
 print(m, sorted({(x[2],x[5],x[3],x[4]) for x in outs if x[1]==m and x[5]!='MUST-METADATA'}))

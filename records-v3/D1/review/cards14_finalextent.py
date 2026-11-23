import csv,sys,json,pathlib,collections,re
csv.field_size_limit(sys.maxsize)
rows=list(csv.DictReader(open('D1/compare/joined.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE));old={x['id']:x for x in csv.DictReader(open('D1/adjudication/rows.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE)}
prior={x['id']:x for x in csv.DictReader(open('D1/review/cards-1-4-extent.tsv'),delimiter='\t')}
installed={}
for m,f in [('fedora','004-packages-root-rpm.out'),('tumbleweed','004-packages-root-rpm.out'),('mint','003-packages-root-dpkg-query.out')]:installed[m]={l.split('\t')[0].split(':')[0]:l.split('\t')[1] for l in open('D1/in/raw/'+m+'/raw/'+f) if '\t' in l}
d=json.load(open('D1/adjudication/work/A/deps-A.json'));tw=json.load(open('D1/review/cards14-raw/tw-primary-selected.json'));mi={}
for p in pathlib.Path('D1/review/cards14-raw').glob('mint-*-metadata.json'):
 for n,v in json.load(open(p)).items():mi.setdefault(n,[]).append(v)
for p in pathlib.Path('D1/review/cards14-raw').glob('mint-*-versions.json'):
 for n,vs in json.load(open(p)).items():mi.setdefault(n,[]).extend(vs)
meta={}
for m in installed:
 for n,iv in installed[m].items():
  req=[];prov=[n];exact=False;src=''
  if m=='fedora':
   v=d.get(n,{});exact=v.get('ver')==iv;req=v.get('req',[])+v.get('rec',[]);prov+=v.get('prov',[]);src='D1/adjudication/work/A/deps-A.json'
  elif m=='tumbleweed':
   v=tw.get(n,{});vv=v.get('version',{});exact=vv.get('ver','')+'-'+vv.get('rel','')==iv;req=[q['name'] for q in v.get('requires',[])+v.get('recommends',[])];prov += [q['name'] for q in v.get('provides',[])];src='cards14-raw/tw-primary-selected.json'
  else:
   v=next((v for v in mi.get(n,[]) if v.get('Version')==iv),{});exact=bool(v)
   for field in ['Depends','Pre-Depends','Recommends']:
    for q in v.get(field,'').split(','):
     if q.strip() and '|' not in q:req.append(re.split(r'[ (]',q.strip())[0].split(':')[0])
   prov+=v.get('Provides','').split(', ');src='cards14-raw/mint-*-metadata.json and mint-*-versions.json'
  req=[q for q in req if not q.startswith('rpmlib(')]
  meta[(m,n)]={'exact':exact,'req':req,'prov':set(prov),'source':src,'version':iv}
out=[]
for x in rows:
 if x['id'] not in prior:continue
 m=x['machine'];n=x['name'].split(':',1)[-1].split(':')[0] if x['name'].startswith(('root:','user:')) else x['name'];o=old.get(x['id'],{});v=meta.get((m,n),{});status='';reason=''
 if m=='flatcar':status='EXCLUDED:MUST' if n=='/etc/ssl' else 'UNKNOWN';reason='Trust controls govern acceptance independently of reference-content exemption.' if n=='/etc/ssl' else 'Mixed hwdb operational properties and data: actual contents not inventoried.'
 elif n in ['gpg-pubkey','ca-certificates-mozilla','libtirpc-common']:status='EXCLUDED:MUST';reason='Operational trust or transport settings independently satisfy S2.2-1.'
 elif not v.get('exact'):status='UNKNOWN';reason='Exact installed-version metadata not found; cannot rule out operational package dependencies.'
 elif v['req']:status='EXCLUDED:MUST';reason='Whole package has operational requirement(s): '+', '.join(v['req'])+'; '+v['source']
 else:
  rev=[]
  for (mm,nn),w in meta.items():
   if mm==m and nn!=n and w['exact'] and set(w['req'])&v['prov']:rev.append(nn)
  if rev:status='EXCLUDED:MUST';reason='Installed reverse requirements depend on package metadata: '+', '.join(sorted(rev))+'; '+v['source']
  elif prior[x['id']]['membership']=='CONFIRMED':status='CANDIDATE';reason='No forward or installed reverse requirement found in exact metadata; payload gap survives these refutations. Scriptlets not yet excluded. '+v['source']
  else:status='UNKNOWN';reason='No metadata refutation; payload/reader facts not established.'
 out.append([x['id'],m,x['kind'],x['name'],o.get('hole',''),status,reason])
with open('D1/review/cards-1-4-extent.tsv','w') as f:
 w=csv.writer(f,delimiter='\t');w.writerow(['id','machine','kind','name','source_card','membership','evidence']);w.writerows(out)
print(collections.Counter((x[1],x[5]) for x in out))
print('CANDIDATES',[(x[1],x[3]) for x in out if x[5]=='CANDIDATE'])
print('UNKNOWNS',[(x[1],x[3]) for x in out if x[5]=='UNKNOWN'])

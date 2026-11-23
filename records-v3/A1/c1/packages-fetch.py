import csv,json,urllib.request,concurrent.futures,pathlib
rows=[r for r in csv.DictReader(open('A1/in/part-1.tsv'),delimiter='\t') if r['kind']=='package']
p=pathlib.Path('A1/c1/package-docs.jsonl'); known={}
if p.exists():
 for l in p.read_text().splitlines():
  x=json.loads(l);known[x['id']]=x

def get(r):
 u='https://mdapi.fedoraproject.org/f44/pkg/'+urllib.parse.quote(r['name'])
 try:
  d=json.load(urllib.request.urlopen(u,timeout=15))
  return {'id':r['id'],'name':r['name'],'url':u,'summary':d['summary'],'description':d['description'],'provides':[x['name'] for x in d['provides']]}
 except Exception as e:return {'id':r['id'],'name':r['name'],'url':u,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex, p.open('a') as f:
 for i,x in enumerate(ex.map(get,[r for r in rows if r['id'] not in known])):
  f.write(json.dumps(x)+'\n');f.flush()
print('Retrieved',len(p.read_text().splitlines()))

import csv,json,urllib.request,urllib.parse,concurrent.futures,pathlib
rows=[r for r in csv.DictReader(open('A1/in/part-1.tsv'),delimiter='\t') if r['kind']=='package']
p=pathlib.Path('A1/c1/package-filechecks.jsonl');done=set()
if p.exists():done={json.loads(x)['id'] for x in p.read_text().splitlines()}
def get(r):
 u='https://mdapi.fedoraproject.org/f44/files/'+urllib.parse.quote(r['name']);d={'id':r['id'],'url':u,'name':r['name']}
 try:
  z=json.load(urllib.request.urlopen(u,timeout=15))['files']
  d['files']=None if z is None else [x for x in z if not any(s in x['dirname'] for s in ['/locale/','/licenses/','/doc/','/man/','/.build-id','/zoneinfo/','/firmware/','/pki/'])]
 except Exception as e:d['error']=str(e)
 return d
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex,p.open('a') as f:
 for d in ex.map(get,[r for r in rows if r['id'] not in done]):f.write(json.dumps(d)+'\n');f.flush()
print('Done')

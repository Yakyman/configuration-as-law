import csv,json,urllib.request,urllib.parse,concurrent.futures
p='A1/c1/package-docs.jsonl'; ds={d['id']:d for d in map(json.loads,open(p))}
rows=[r for r in csv.DictReader(open('A1/in/part-1.tsv'),delimiter='\t') if r['kind']=='package'];done={r['id'] for r in csv.DictReader(open('A1/c1/part-1.packages.tsv'),delimiter='\t')}
def get(d):
 try:
  if 'error' in d:
   z=json.load(urllib.request.urlopen(d['url'],timeout=15)); d={k:v for k,v in d.items() if k!='error'};d.update({k:z[k] for k in ['summary','description']});d['provides']=[x['name'] for x in z['provides']]
  if d['id'] not in done:
   d['files']=json.load(urllib.request.urlopen(d['url'].replace('/pkg/','/files/'),timeout=15))
 except Exception as e:d['detail_error']=str(e)
 return d
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e,open(p,'a') as f:
 for d in e.map(get,[d for d in ds.values() if d['id'] not in done]):f.write(json.dumps(d)+'\n');f.flush()

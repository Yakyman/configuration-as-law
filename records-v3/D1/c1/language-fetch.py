import csv,json,urllib.request,concurrent.futures
rows=list(csv.DictReader(open('D1/in/part-tumbleweed.tsv'),delimiter='\t'))
keys=sorted(set((r['kind'].split(':')[-1].replace('pip3','pip'),r['name'].split(':',1)[1]) for r in rows if r['kind'] in ['L1:package:pip','L1:package:pip3','L1:package:gem']))
def get(k):
 typ,name=k;url=f'https://pypi.org/pypi/{name}/json' if typ=='pip' else f'https://rubygems.org/api/v1/gems/{name}.json'
 try:
  d=json.load(urllib.request.urlopen(url,timeout=20));s=d['info']['summary'] if typ=='pip' else d['info'];return [typ,name,url,' '.join(s.split())]
 except Exception as e:return [typ,name,url,'ERROR '+str(e)]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex: data=list(ex.map(get,keys))
json.dump(data,open('D1/c1/language-docs.json','w'),indent=2)
for x in data:print(x[0],x[1],x[3][:220])

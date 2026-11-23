import urllib.request,gzip,json,pathlib,concurrent.futures
names={l.split('\t')[0].split(':')[0] for l in open('D1/in/raw/mint/raw/003-packages-root-dpkg-query.out')}
def go(c):
 u='https://mirrors.edge.kernel.org/linuxmint-packages/dists/zena/'+c+'/binary-amd64/Packages.gz'
 try:
  s=gzip.decompress(urllib.request.urlopen(u,timeout=15).read()).decode();out={}
  for b in s.split('\n\n'):
   f={line.split(': ',1)[0]:line.split(': ',1)[1] for line in b.splitlines() if ': ' in line and not line.startswith(' ')}
   n=f.get('Package')
   if n in names:out.setdefault(n,[]).append({x:f[x] for x in ['Version','Depends','Pre-Depends','Recommends','Provides'] if x in f})
  pathlib.Path('D1/review/cards14-raw/mint-'+c+'-versions.json').write_text(json.dumps(out,indent=2));print(c,len(out))
 except Exception as e:print(c,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:list(e.map(go,['main','upstream','import','backport']))

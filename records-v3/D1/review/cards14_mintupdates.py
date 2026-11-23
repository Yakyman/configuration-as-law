import urllib.request,lzma,gzip,pathlib,json,concurrent.futures
names={l.split('\t')[0].split(':')[0] for l in open('D1/in/raw/mint/raw/003-packages-root-dpkg-query.out')}
urls={**{c:'https://packages.linuxmint.com/dists/zena/'+c+'/binary-amd64/Packages.gz' for c in ['main','upstream','import','backport']},**{'updates-'+c:'https://archive.ubuntu.com/ubuntu/dists/noble-updates/'+c+'/binary-amd64/Packages.xz' for c in ['main','universe']},**{'security-'+c:'https://security.ubuntu.com/ubuntu/dists/noble-security/'+c+'/binary-amd64/Packages.xz' for c in ['main','universe']}}
def go(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(u,timeout=20).read();s=(gzip.decompress(b) if u.endswith('.gz') else lzma.decompress(b)).decode();out={}
  for b in s.split('\n\n'):
   f={line.split(': ',1)[0]:line.split(': ',1)[1] for line in b.splitlines() if ': ' in line and not line.startswith(' ')}
   n=f.get('Package')
   if n in names:out.setdefault(n,[]).append({x:f[x] for x in ['Version','Depends','Pre-Depends','Recommends'] if x in f})
  pathlib.Path('D1/review/cards14-raw/mint-'+k+'-versions.json').write_text(json.dumps(out,indent=2));print(k,len(out),flush=True)
 except Exception as e:print(k,str(e),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:list(e.map(go,urls.items()))

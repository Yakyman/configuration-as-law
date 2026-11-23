import csv,urllib.request,lzma,json
from pathlib import Path
rows=[r for r in csv.DictReader(open('D1/in/part-mint.tsv'),delimiter='\t') if r['kind']=='L1:package:dpkg-query'][:635]
wanted={r['name'].split(':')[1] for r in rows}; out={}
for comp in ['main','universe','restricted','multiverse']:
 u=f'https://archive.ubuntu.com/ubuntu/dists/noble/{comp}/binary-amd64/Packages.xz'
 data=lzma.decompress(urllib.request.urlopen(u,timeout=60).read()).decode()
 for p in data.split('\n\n'):
  lines=p.splitlines(); name=next((l[9:] for l in lines if l.startswith('Package: ')),None)
  if name in wanted:
   desc=next((l[13:] for l in lines if l.startswith('Description: ')),None)
   out[name]={'description':desc,'url':u}
 print(comp,len(out),flush=True)
Path('D1/c1/part-mint.1.sources.json').write_text(json.dumps(out,indent=2))
print('Missing:',sorted(wanted-out.keys()))

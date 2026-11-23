import urllib.request,concurrent.futures,json,re
from pathlib import Path
names='at-spi2-common brasero-common cinnamon-common colord-data cups-common cups-server-common evolution-data-server-common gcc-13-base gcc-14-base hplip-data ibus-data libavahi-common-data libcaribou-common libclutter-1.0-common libcogl-common libdjvulibre-text libdrm-common'.split()
def get(n):
 u=f'https://packages.ubuntu.com/noble/amd64/{n}/filelist'
 try:
  t=urllib.request.urlopen(u,timeout=25).read().decode();paths=re.findall(r'<pre>(.*?)</pre>',t,re.S);return n,{'url':u,'paths':paths[0] if paths else 'Unavailable'}
 except Exception as e:return n,{'url':u,'error':str(e)}
out=dict(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(get,names));Path('D1/c1/part-mint.1.filelists.json').write_text(json.dumps(out,indent=2));print({n:len(x.get('paths','')) for n,x in out.items()})

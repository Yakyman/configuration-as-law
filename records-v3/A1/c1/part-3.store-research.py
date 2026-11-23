import csv,re,urllib.request,concurrent.futures,json
rows=[r for r in csv.DictReader(open('A1/in/part-3.tsv'),delimiter='\t') if r['kind']=='system-closure-store-object']
names={re.split(r'-(?=\d)',r['name'].split('-',1)[1],maxsplit=1)[0] for r in rows if re.search(r'-\d',r['name'].split('-',1)[1])}
translate={'coreutils-full':'coreutils','util-linux-minimal':'util-linux','bash-interactive':'bash','gmp-with-cxx':'gmp','systemd-minimal':'systemd','systemd-minimal-libs':'systemd','getent-glibc':'glibc','libpng-apng':'libpng','linux-headers-static':'linuxHeaders','dejavu-fonts-minimal':'dejavu_fonts','hostname-debian':'hostname','nss-cacert':'cacert','fontconfig':'fontconfig','xgcc':'gcc','texinfo-interactive':'texinfo'}
def get(n):
 a=translate.get(n,n); u=f'https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/{a[:2]}/{a}/package.nix'
 try:
  s=urllib.request.urlopen(u,timeout=15).read().decode();d=re.search(r'description\s*=\s*"([^"\n]+)',s);o=re.search(r'outputs\s*=\s*\[([^]]+)',s)
  return n,{'url':u,'description':d.group(1) if d else '', 'outputs':o.group(1).strip() if o else '', 'excerpt':s[-2500:] if not d else ''}
 except Exception:return n,{'url':u,'missing':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: data=dict(ex.map(get,sorted(names)))
json.dump(data,open('A1/c1/part-3.store-research.json','w'),indent=2)
for k,v in data.items():print(k,':',v.get('description','MISSING'))

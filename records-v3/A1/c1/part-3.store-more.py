import json,urllib.request,re,concurrent.futures
p='A1/c1/part-3.store-research.json';d=json.load(open(p));base='https://raw.githubusercontent.com/NixOS/nixpkgs/master/'
s=urllib.request.urlopen(base+'pkgs/top-level/all-packages.nix').read().decode()
extra={'bash-interactive':'bash','boehm-gc':'boehmgc','gmp-with-cxx':'gmp','getent-glibc':'glibc','gnupg':'gnupg24','gpm-unstable':'gpm','libffi':'libffiReal','libmicrohttpd':'libmicrohttpd_1_0','libtool':'libtool_2','mdadm':'mdadm4','patch':'gnupatch','perl':'perl5','python3':'python313','openssl':'openssl_3_5','systemd-minimal':'systemd','systemd-minimal-libs':'systemd','texinfo-interactive':'texinfo','libusb':'libusb1','icu4c':'icu','cyrus-sasl':'cyrus_sasl','libcap-ng':'libcap_ng','db':'db5','fuse':'fuse3','hostname-debian':'hostname-debian','zlib':'zlib'}
def fetch(n):
 a=extra.get(n,n);urls=[]
 m=re.search(r'^  '+re.escape(a)+r'\s*=.*?(?=\n  [\w"#]|\Z)',s,re.M|re.S)
 if m:
  t=re.search(r'(?:callPackage|import)\s+\.\./([^\s;)]+)',m.group(0))
  if t:
   path='pkgs/'+t.group(1);urls.append(base+path+('' if path.endswith('.nix') else '/default.nix'))
 urls.append(base+f'pkgs/by-name/{a[:2]}/{a}/package.nix')
 for u in urls:
  try:
   txt=urllib.request.urlopen(u,timeout=15).read().decode();mt=re.search(r'description\s*=\s*"([\s\S]*?)";',txt);o=re.search(r'outputs\s*=\s*\[([^]]+)',txt)
   if mt:return n,{'url':u,'description':' '.join(mt.group(1).split()),'outputs':o.group(1).strip() if o else ''}
  except Exception:pass
 return n,d[n]
keys=[k for k,v in d.items() if v.get('missing') or not v.get('description','').strip()]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for k,v in ex.map(fetch,keys):d[k]=v
json.dump(d,open(p,'w'),indent=2)
for k,v in d.items():
 if k in keys:print(k,':',v.get('description','MISSING'))

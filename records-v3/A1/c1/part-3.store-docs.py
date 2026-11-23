import urllib.request,json,concurrent.futures,re
sources={
'nix':'https://raw.githubusercontent.com/NixOS/nix/master/README.md',
'c-rbtree':'https://raw.githubusercontent.com/c-util/c-rbtree/main/README.md',
'c-dvar':'https://raw.githubusercontent.com/c-util/c-dvar/main/README.md',
'c-ini':'https://raw.githubusercontent.com/c-util/c-ini/main/README.md',
'c-shquote':'https://raw.githubusercontent.com/c-util/c-shquote/main/README.md',
'c-utf8':'https://raw.githubusercontent.com/c-util/c-utf8/main/README.md',
'curl':'https://raw.githubusercontent.com/curl/curl/master/README.md',
'libfido2':'https://raw.githubusercontent.com/Yubico/libfido2/main/README.adoc',
'libressl':'https://raw.githubusercontent.com/libressl/portable/master/README.md',
'fuse':'https://raw.githubusercontent.com/libfuse/libfuse/master/README.md',
'openssl':'https://raw.githubusercontent.com/openssl/openssl/master/README.md',
'openssh':'https://raw.githubusercontent.com/openssh/openssh-portable/master/README',
'json-c':'https://raw.githubusercontent.com/json-c/json-c/master/README.md',
'libxml2':'https://raw.githubusercontent.com/GNOME/libxml2/master/README.md',
'icu4c':'https://raw.githubusercontent.com/unicode-org/icu/main/README.md',
'python3':'https://raw.githubusercontent.com/python/cpython/main/README.rst',
'perl':'https://raw.githubusercontent.com/Perl/perl5/blead/pod/perlintro.pod',
'boost':'https://www.boost.org/',
'gmp-with-cxx':'https://gmplib.org/',
'nettle':'https://www.lysator.liu.se/~nisse/nettle/',
'lvm2':'https://sourceware.org/lvm2/',
'db':'https://www.oracle.com/database/technologies/related/berkeleydb.html',
'grub':'https://www.gnu.org/software/grub/',
'linux':'https://docs.kernel.org/admin-guide/README.html',
'libmicrohttpd':'https://www.gnu.org/software/libmicrohttpd/',
}
def get(kv):
 k,u=kv
 try:
  s=urllib.request.urlopen(u,timeout=15).read().decode()
  if '<html' in s.lower():
   from bs4 import BeautifulSoup
   s=BeautifulSoup(s,'html.parser').get_text(' ',strip=True)
  return k,{'url':u,'text':s}
 except Exception as e:return k,{'url':u,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:d=dict(ex.map(get,sources.items()))
# Save only selected short passages after inspection, not source documents.
for k,v in d.items():print('\n'+k+' '+v['url']+'\n'+v.get('text',v.get('error'))[:1500])
json.dump({k:{'url':v['url'],'text':'Research passages must be curated before saving.'} for k,v in d.items()},open('A1/c1/part-3.store-docs.json','w'),indent=2)

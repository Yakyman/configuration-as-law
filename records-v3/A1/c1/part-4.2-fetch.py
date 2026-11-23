import urllib.request,concurrent.futures,re,json
mods='linux glib databases base guile authentication xdisorg tls networking backup webkit image graphics gnome disk admin freedesktop package-management pulseaudio commencement'.split()
old=json.load(open('A1/c1/part-4.2-package-docs.json'))
unused='xorg linux video audio compression tls ssh gnupg gnome gtk glib guile guile-xyz xfce perl perl-web web xml databases gcc base bash fontutils fonts freedesktop xdisorg pulseaudio gl image glibc ncurses acl attr cups samba dns networking ntp polkit admin cryptsetup pkg-config libffi libusb libidn libcanberra libdaemon libunwind mp3 music maths protobuf scanner sdl enchant avahi graphviz readline bash shells man texinfo'.split()
def fetch(m):
 u=f'https://raw.githubusercontent.com/Millak/guix/d58da8a56b75af73a7b5466f7ef8a81679713aa3/gnu/packages/{m}.scm'
 try:
  t=urllib.request.urlopen(u,timeout=25).read().decode();result={}
  for block in re.split(r'\n\(define(?:-public)? ',t)[1:]:
   name=block.split()[0];syn=re.search(r'\(synopsis\s+"((?:\\.|[^"\\])*)"',block);nm=re.search(r'\(name\s+"([^"]+)"',block)
   if syn:
    ent={'url':u,'synopsis':syn.group(1).replace('\n',' '),'symbol':name}
    result[name]=ent
    if nm:result[nm.group(1)]=ent
  return result
 except Exception as e:return {'!'+m:str(e)}
out=old
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for result in ex.map(fetch,mods):out.update(result)
json.dump(out,open('A1/c1/part-4.2-package-docs.json','w'),indent=2)
print('entries',len(out));print({k:v for k,v in out.items() if k.startswith('!')})

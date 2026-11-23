import urllib.request,concurrent.futures,re,json,csv
mods='compression xorg xfce linux glib gtk gnome video audio maths image xiph cups fontutils fonts guile guile-xyz guix ssh networking tls security polkit freedesktop bash base web curl wget pkg-config perl python commencement disk databases multiprecision xml serialization enchant aspell hunspell music mp3 pulseaudio sdl openldap kerberos cryptsetup gnupg libevent libffi libusb photo scanner imagemagick pdf icu pciutils gettext check admin bootloaders gcc llvm virtualization suckless xdisorg gl texinfo file ed gawk less textutils ncurses pcre disk hurd libbsd password-utils openexr version-control libedit libidn libunwind rdf speech samba tcl'.split()
def get(m):
 u=f'https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/{m}.scm'
 try:
  s=urllib.request.urlopen(u,timeout=25).read().decode()
  out=[]
  for chunk in re.split(r'\n\(define(?:-public)? ',s)[1:]:
   var=chunk.split()[0]; n=re.search(r'\(name "([^"]+)"\)',chunk); syn=re.search(r'\(synopsis "((?:[^"\\]|\\.)*)"\)',chunk)
   par=re.search(r'\(inherit ([^()\s]+)\)',chunk)
   if syn: out.append((var,n.group(1) if n else var,' '.join(syn.group(1).split()),u))
   elif par: out.append((var,n.group(1) if n else var,'INHERIT:'+par.group(1),u))
  return out
 except Exception:return []
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: a=sum(ex.map(get,mods),[])
for _ in range(8):
 for i,x in enumerate(a):
  if x[2].startswith('INHERIT:'):
   par=next((v for v in a if v[0]==x[2][8:] and not v[2].startswith('INHERIT:')),None)
   if par:a[i]=(*x[:2],par[2],x[3])
json.dump(a,open('A1/c1/part-4.1-metadata.json','w'))
rows=[r for r in csv.DictReader(open('A1/in/part-4.tsv'),delimiter='\t') if r['kind']=='system-closure-store-object'][:431]
for i,r in enumerate(rows):
 n=r['name'][44:]; pkg=re.split(r'-(?=\d)',n)[0]; matches=[x for x in a if pkg in x[:2]]
 if matches: print(i,n,matches[0][2])
 else: print('MISSING',i,n)

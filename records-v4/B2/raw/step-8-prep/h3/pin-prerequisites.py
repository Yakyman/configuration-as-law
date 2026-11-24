import urllib.request,lzma,json,pathlib,hashlib,re
root=pathlib.Path('raw/step-8-prep/h3'); installed=json.loads((root/'installed-packages.json').read_text())
u='https://deb.debian.org/debian/dists/trixie/main/binary-amd64/Packages.xz'
raw=urllib.request.urlopen(u).read();data=lzma.decompress(raw).decode();packages={}
for para in data.split('\n\n'):
 row={};last=None
 for line in para.splitlines():
  if line.startswith(' '):
   if last: row[last]+=' '+line.strip()
  elif ': ' in line:last,v=line.split(': ',1);row[last]=v
 if 'Package' in row:packages[row['Package']]=row
required='bc binutils bsdmainutils bzip2 ca-certificates cpio curl distro-info file gzip hostname jq lib32gcc-s1 lib32stdc++6 netcat-openbsd pigz procps python3 tar tmux unzip util-linux uuid-runtime wget xz-utils'.split()
selected={};obligations=[]
def choose(name):
 if name in installed or name in selected:return
 r=packages[name];selected[name]=r
 for field in ['Pre-Depends','Depends']:
  for group in r.get(field,'').split(','):
   if not group.strip():continue
   alts=[re.split(r'\s|:',x.strip())[0] for x in group.split('|')]
   chosen=next((x for x in alts if x in installed),None) or next((x for x in alts if x in packages),None)
   if not chosen:raise ValueError((name,group))
   obligations.append({'requiring':name,'field':field,'requirement':group.strip(),'selected':chosen,'installed_version':installed.get(chosen),'candidate_version':packages.get(chosen,{}).get('Version')})
   choose(chosen)
for name in required:choose(name)
inputs=pathlib.Path('cases-8/h3/prerequisites');inputs.mkdir(parents=True,exist_ok=True);out=[]
for name,r in sorted(selected.items()):
 url='https://deb.debian.org/debian/'+r['Filename'];b=urllib.request.urlopen(url).read();assert hashlib.sha256(b).hexdigest()==r['SHA256'];f=inputs/pathlib.Path(r['Filename']).name;f.write_bytes(b)
 out.append({'package':name,'version':r['Version'],'architecture':r['Architecture'],'source':url,'sha256':r['SHA256'],'filename':f.name,'bytes':len(b),'depends':r.get('Depends',''),'pre_depends':r.get('Pre-Depends','')})
(inputs.parent/'prerequisites.json').write_text(json.dumps({'index_source':u,'index_sha256':hashlib.sha256(raw).hexdigest(),'required':required,'packages':out,'dependency_obligations':obligations},indent=2)+'\n')
print(json.dumps(out,indent=2))

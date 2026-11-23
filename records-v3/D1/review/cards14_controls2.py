import urllib.request,io,tarfile,json,concurrent.futures,pathlib,re
versions={l.split('\t')[0]:l.split('\t')[1] for l in open('D1/in/raw/mint/raw/003-packages-root-dpkg-query.out') if '\t' in l}
sources={'fonts-noto-color-emoji':'fonts-noto-color-emoji','ncurses-base':'ncurses','mint-common':'mint-common','plymouth-label':'plymouth','mint-l-theme':'mint-l-theme'}
def go(kv):
 n,s=kv;v=versions[n].split(':')[-1];base='https://mirrors.edge.kernel.org/linuxmint-packages/' if n.startswith('mint-') else 'https://archive.ubuntu.com/ubuntu/';u=base+'pool/main/'+s[0]+'/'+s+'/'+n+'_'+v+('_amd64.deb' if n=='plymouth-label' else '_all.deb')
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'Range':'bytes=0-262143'}),timeout=15) as f:b=f.read(262144)
  assert b[:8]==b'!<arch>\n';off=8;control=None
  while off+60<=len(b):
   hdr=b[off:off+60];name=hdr[:16].decode().strip('/ ');sz=int(hdr[48:58]);off+=60
   if name.startswith('control.tar'):control=b[off:off+sz];break
   off+=sz+(sz%2)
  assert control
  tf=tarfile.open(fileobj=io.BytesIO(control));scripts={};controltext=''
  for member in tf:
   short=member.name.lstrip('./')
   if short=='control':controltext=tf.extractfile(member).read().decode()
   if short in ['preinst','postinst','prerm','postrm','triggers']:
    body=tf.extractfile(member).read().decode();scripts[short]=[l for l in body.splitlines() if l.strip() and not l.strip().startswith('#')]
  match=re.search(r'^Version: (.+)$',controltext,re.M);result={'url':u,'version':match.group(1) if match else '', 'scripts':scripts,'fields':{line.split(': ',1)[0]:line.split(': ',1)[1] for line in controltext.splitlines() if ': ' in line and line.split(': ',1)[0] in ['Depends','Pre-Depends','Recommends','Suggests','Conflicts','Breaks','Replaces','Provides','Essential','Protected']}};pathlib.Path('D1/review/cards14-raw/mint-'+n+'-control.json').write_text(json.dumps(result,indent=2));print(n,result,flush=True)
 except Exception as e:print(n,str(e),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:list(e.map(go,sources.items()))

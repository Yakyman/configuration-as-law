import urllib.request,struct,json,pathlib,concurrent.futures
base='https://download.opensuse.org/tumbleweed/repo/oss/noarch/'
tw=json.load(open('D1/review/cards14-raw/tw-primary-selected.json'))
urls={'fedora-qt6-qttranslations':'https://dl.fedoraproject.org/pub/fedora/linux/releases/45/Everything/x86_64/os/Packages/q/qt6-qttranslations-6.11.2-1.fc45.noarch.rpm'}
for n in ['desktop-translations','kImageAnnotator-lang','libksane-lang','libqt5-qttranslations','libstorage-ng-lang','ocean-sound-theme6','openal-soft-data','publicsuffix','qt6-translations','snapper-lang','poppler-data']:
 v=tw[n]['version'];urls['tumbleweed-'+n]=base+n+'-'+v['ver']+'-'+v['rel']+'.noarch.rpm'
def go(kv):
 k,u=kv
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'Range':'bytes=0-1048575'}),timeout=20) as f:b=f.read(1048576)
  def hdr(off):
   assert b[off:off+3]==b'\x8e\xad\xe8',b[off:off+4]
   cnt,sz=struct.unpack('>II',b[off+8:off+16]);entries=[struct.unpack('>IIII',b[off+16+i*16:off+32+i*16]) for i in range(cnt)];start=off+16+16*cnt;assert len(b)>=start+sz
   out={}
   for tag,ty,o,n in entries:
    if ty in [6,8,9]:out[tag]=b[start+o:].split(b'\0',n)[:n]
   return start+sz,out
  off,_=hdr(96);off=(off+7)//8*8;_,d=hdr(off)
  tags=[1023,1024,1025,1026,1079,1151,1152,5103,5104,1065,5066,5076,1054,1090,5046,5049,5052,5055]
  out={'url':u,'name':d.get(1000,[])[0].decode(),'version':d.get(1001,[])[0].decode()+'-'+d.get(1002,[])[0].decode(),'operational_tags':{str(t):[v.decode(errors='replace') for v in d[t]] for t in tags if t in d}}
  pathlib.Path('D1/review/cards14-raw/'+k+'-header.json').write_text(json.dumps(out,indent=2));print(k,out['operational_tags'],flush=True)
 except Exception as e:print(k,str(e),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:list(e.map(go,urls.items()))

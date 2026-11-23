import csv,json,urllib.request,concurrent.futures,re,html
r=[r for r in csv.DictReader(open('D1/in/part-mint.tsv'),delimiter='\t') if r['kind']=='L1:package:dpkg-query'][635:1270]
names=[x['name'].split(':')[1] for x in r]
special=[n for n in names if any(t in n for t in ['common','-data','-config','-l10n','-help','-style','-uiconfig']) or n in ['libjpeg8','libjs-mathjax','libmagic-mgc','libinput-bin','libpam-runtime','libpython3-stdlib','libtag1v5','libproxy1-plugin-gsettings','libproxy1-plugin-networkmanager','libgcc-13-dev','libstdc++-13-dev','libsnmp-base','libhtml-tagset-perl']]
def fetch(n):
 url=f'https://packages.ubuntu.com/noble/amd64/{n}/filelist'
 try:
  data=urllib.request.urlopen(url,timeout=30).read().decode();match=re.search(r'<pre>(.*?)</pre>',data,re.S)
  return n,{'url':url,'files':html.unescape(match[1]).strip().splitlines() if match else [],'error':'' if match else 'No file list returned'}
 except Exception as e:return n,{'url':url,'files':[],'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=dict(pool.map(fetch,special))
json.dump(out,open('D1/c1/part-mint.2.filelists.json','w'),indent=2)
print('Fetched',len(out))

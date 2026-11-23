import urllib.request,xml.etree.ElementTree as E,pathlib,subprocess,csv,sys,json,lzma
csv.field_size_limit(sys.maxsize)
r=list(csv.DictReader(open('D1/compare/joined.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE));names={x['name'].split(':',1)[-1].split(':')[0] for x in r if x['kind'].startswith('L1:package')}
p=pathlib.Path('D1/review/cards14-raw');base='https://download.opensuse.org/tumbleweed/repo/oss/'
rep=urllib.request.urlopen(base+'repodata/repomd.xml').read();root=E.fromstring(rep);ns={'r':'http://linux.duke.edu/metadata/repo'};href=root.find("r:data[@type='primary']/r:location",ns).get('href');(p/'tw-primary-source.txt').write_text(base+href+'\n')
z=p/'temporary-primary.zst';urllib.request.urlretrieve(base+href,z)
proc=subprocess.Popen(['zstd','-dc',str(z)],stdout=subprocess.PIPE);out={};C='{http://linux.duke.edu/metadata/common}';R='{http://linux.duke.edu/metadata/rpm}'
for event,el in E.iterparse(proc.stdout,events=['end']):
 if el.tag!=C+'package':continue
 n=el.findtext(C+'name');arch=el.findtext(C+'arch')
 if n in names and arch in ['noarch','x86_64']:
  v=el.find(C+'version');fmt=el.find(C+'format');out[n]={'version':v.attrib,'arch':arch,'requires':[e.attrib for e in fmt.findall(R+'requires/'+R+'entry')],'recommends':[e.attrib for e in fmt.findall(R+'recommends/'+R+'entry')]}
 el.clear()
proc.wait();z.unlink();(p/'tw-primary-selected.json').write_text(json.dumps(out,indent=2));print('TW metadata',len(out))
for component in ['main','universe']:
 u='https://archive.ubuntu.com/ubuntu/dists/noble/'+component+'/binary-amd64/Packages.xz'
 s=lzma.decompress(urllib.request.urlopen(u,timeout=30).read()).decode();out={}
 for b in s.split('\n\n'):
  fields={};last=''
  for line in b.splitlines():
   if line.startswith(' '):continue
   if ': ' in line:k,val=line.split(': ',1);fields[k]=val
  n=fields.get('Package')
  if n in names:out[n]={k:fields[k] for k in ['Version','Depends','Pre-Depends','Recommends'] if k in fields}
 (p/('mint-'+component+'-metadata.json')).write_text(json.dumps(out,indent=2));print(component,len(out),flush=True)

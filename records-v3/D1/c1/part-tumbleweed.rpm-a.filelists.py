import urllib.request,xml.etree.ElementTree as E,subprocess,json
from pathlib import Path
base='https://download.opensuse.org/tumbleweed/repo/oss/';m=json.load(open('D1/c1/part-tumbleweed.rpm-a.metadata.json'))['packages']
r=E.fromstring(urllib.request.urlopen(base+'repodata/repomd.xml').read()); ns={'r':'http://linux.duke.edu/metadata/repo'}
p=next(d.find('r:location',ns).attrib['href'] for d in r if d.attrib.get('type')=='filelists')
f=Path('D1/c1/part-tumbleweed.rpm-a.filelists.zst');f.write_bytes(urllib.request.urlopen(base+p).read())
proc=subprocess.Popen(['zstd','-dc',str(f)],stdout=subprocess.PIPE);n='{http://linux.duke.edu/metadata/filelists}';data={}
for ev,el in E.iterparse(proc.stdout,events=['end']):
 if el.tag==n+'package':
  name=el.attrib['name']
  if name in m and el.attrib.get('arch') in ['x86_64','noarch']:data[name]=[x.text for x in el.findall(n+'file') if x.attrib.get('type')!='dir']
  el.clear()
Path('D1/c1/part-tumbleweed.rpm-a.filelists.json').write_text(json.dumps({'url':base+p,'packages':data},indent=2))
print(len(data))

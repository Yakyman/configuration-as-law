import urllib.request,xml.etree.ElementTree as E,json
from compression import zstd
path='D1/c1/raw/rpm-documentation.json';d=json.load(open(path));P=d['packages'];base=d['source'].split('repodata/')[0];root=E.fromstring(urllib.request.urlopen(base+'repodata/repomd.xml').read());ns={'r':'http://linux.duke.edu/metadata/repo'};url=base+root.find("r:data[@type='filelists']/r:location",ns).attrib['href'];d['file_source']=url
with urllib.request.urlopen(url) as response,zstd.ZstdFile(response) as stream:
 for _,p in E.iterparse(stream,events=['end']):
  if p.tag!='{http://linux.duke.edu/metadata/filelists}package':continue
  name=p.attrib['name']
  if name in P and p.attrib['arch'] in ['x86_64','noarch']:
   P[name]['all_files']=[x.text for x in p if x.tag.endswith('}file')]
  p.clear()
json.dump(d,open(path,'w'),indent=2)
print('file listings extracted',sum('all_files' in v for v in P.values()))

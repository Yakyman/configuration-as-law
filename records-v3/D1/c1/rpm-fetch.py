import urllib.request,xml.etree.ElementTree as E,csv,json
from compression import zstd
base='https://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/'
index=urllib.request.urlopen(base+'repodata/repomd.xml').read()
root=E.fromstring(index); n={'r':'http://linux.duke.edu/metadata/repo'}
href=root.find("r:data[@type='primary']/r:location",n).attrib['href'];url=base+href
wanted={r['name'].split(':',1)[1] for r in csv.DictReader(open('D1/in/part-fedora.tsv'),delimiter='\t') if r['kind']=='L1:package:rpm'}
ns={'c':'http://linux.duke.edu/metadata/common','rpm':'http://linux.duke.edu/metadata/rpm'}
found={}
with urllib.request.urlopen(url) as response, zstd.ZstdFile(response) as stream:
 for event,p in E.iterparse(stream,events=['end']):
  if p.tag!='{http://linux.duke.edu/metadata/common}package':continue
  name=p.findtext('c:name',namespaces=ns)
  if name in wanted and p.findtext('c:arch',namespaces=ns) in ['x86_64','noarch']:
   found[name]={'summary':p.findtext('c:summary',namespaces=ns),'description':p.findtext('c:description',namespaces=ns),'files':[x.text for x in p.findall('c:format/c:file',ns)],'url':p.findtext('c:url',namespaces=ns)}
  p.clear()
json.dump({'source':url,'packages':found},open('D1/c1/raw/rpm-documentation.json','w'),indent=2)
print('matched',len(found),'missing',sorted(wanted-found.keys()))

import urllib.request,xml.etree.ElementTree as E,subprocess,csv,json
base='https://download.opensuse.org/tumbleweed/repo/oss/'
r=E.fromstring(urllib.request.urlopen(base+'repodata/repomd.xml').read()); n={'r':'http://linux.duke.edu/metadata/repo','c':'http://linux.duke.edu/metadata/common'}
loc=next(x.find('r:location',n).attrib['href'] for x in r if x.attrib.get('type')=='primary'); url=base+loc
rows=[x for x in csv.DictReader(open('D1/in/part-tumbleweed.tsv'),delimiter='\t') if x['kind']=='L1:package:rpm'][2390:]; names={x['name'].split(':',1)[1] for x in rows}
p='D1/c1/rpm-b-primary.xml.zst';urllib.request.urlretrieve(url,p)
proc=subprocess.Popen(['zstd','-dc',p],stdout=subprocess.PIPE)
found={}
for event,e in E.iterparse(proc.stdout,events=['end']):
 if e.tag=='{'+n['c']+'}package':
  name=e.findtext('c:name',namespaces=n)
  if name in names:
   found[name]={'summary':e.findtext('c:summary',namespaces=n),'description':e.findtext('c:description',namespaces=n),'url':e.findtext('c:url',namespaces=n),'files':[f.text for f in e.findall('c:format/c:file',n)]}
  e.clear()
proc.wait();json.dump({'source':url,'packages':found},open('D1/c1/rpm-b-metadata.json','w'),indent=2)
print('matched',len(found),'missing',sorted(names-found.keys()))

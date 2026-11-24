import csv,json,pathlib
root=pathlib.Path('D1/in/raw/talos')
rows=list(csv.DictReader(open('D1/in/part-talos.tsv'),delimiter='\t'))
out=pathlib.Path('D1/c1/part-talos.2.tsv')
fields=['id','decision','sentences','what_it_does','basis','reason']
seen={r['id'] for r in csv.DictReader(out.open(),delimiter='\t')} if out.exists() else set()
stateurl='https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/internal/app/machined/pkg/runtime/v1alpha2/v1alpha2_state.go'
consturl='https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/pkg/machinery/constants/constants.go'
def stream(path):
 s=path.read_text(); dec=json.JSONDecoder(); data=[]
 while s.strip():
  s=s.lstrip(); o,n=dec.raw_decode(s);data.append(o);s=s[n:]
 return data
with out.open('a') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n')
 if not seen:w.writeheader()
 for i in range(92,213):
  r=rows[i]
  if r['id'] in seen:continue
  basis='raw:'+r['evidence']
  if i<=144:
   obj=next(o for o in stream(root/r['evidence']) if o['metadata']['id']==r['name'])
   owner=obj['metadata']['owner']; typ=obj['metadata']['type'].split('.')[0]
   what='In-memory '+typ+' resource maintained by network controllers.'
   reason=f"Runtime resource created by machined ({owner}); machined decision UNKNOWN because packaged-file integrity is unestablished."
   basis='doc:'+stateurl
  elif i<=210:
   port=r['name'].rsplit(':',1)[-1]
   creator={'2379':'etcd','2380':'etcd','2383':'etcd','10250':'kubelet','50000':'apid','50001':'trustd','7445':'KubePrism'}.get(port)
   if creator:
    reason=f"Runtime socket created by {creator}; creator decision UNKNOWN because installed provenance/integrity and derived-line coverage are unestablished."
    basis='doc:'+consturl
   elif port=='53':
    creator='host DNS resolver'
    reason='Runtime socket created by host DNS resolver; creator decision UNKNOWN because packaged-file integrity is unestablished.'
    basis='doc:https://docs.siderolabs.com/talos/v1.14/networking/host-dns'
   else:
    reason='Runtime socket; creating program and inherited decision UNKNOWN because inventory omits socket owners. Every possible owner leaves this socket RUNTIME.'
   what='Live network socket for listening or communicating.'
  else:
   what=f"Running {r['name']} container instance with a live process identifier."
   reason=f"Runtime container process created by containerd to run {r['name']}; containerd decision UNKNOWN because packaged-file integrity is unestablished."
  item=dict(zip(fields,[r['id'],'RUNTIME','S8.2-5',what,basis,reason]))
  assert len(what.split())<=15
  assert len(reason.split())<=30
  w.writerow(item);f.flush()
print('Appended; total',sum(1 for _ in csv.DictReader(out.open(),delimiter='\t')))

import csv,json,pathlib,collections
rows=list(csv.DictReader(open('D1/in/part-talos.tsv'),delimiter='\t'))[:92]
path=pathlib.Path('D1/c1/part-talos.1.tsv')
fields=['id','decision','sentences','what_it_does','basis','reason']
existing=list(csv.DictReader(path.open(),delimiter='\t')) if path.exists() else []
seen={r['id'] for r in existing}
f=path.open('a'); w=csv.DictWriter(f,fields,delimiter='\t',lineterminator='\n')
if not existing: w.writeheader();f.flush()
for i,r in enumerate(rows):
 if r['id'] in seen: continue
 m=json.loads(r['members']);m=json.loads(m) if isinstance(m,str) else m
 d='RUNTIME';s='S8.2-5,S8.2-7,S8.2-16';b='raw:D1/in/raw/talos/'+r['evidence']
 if i<17 or i==34:
  what='Current mount status for '+m['spec']['target']
  why='Created by machined mount controllers; machined decision UNKNOWN because executable package integrity is unestablished. Mount status exists only during operation.'
 elif i<30:
  what='Active filesystem mount at '+r['name']
  creator='containerd' if i in [28,29] else 'machined startup'
  why=f'Created by {creator}; creator decision UNKNOWN because executable package integrity is unestablished. The active mount is not a separate object.'
 elif i<34:
  what='Runtime block-device discovery resource for '+r['name']
  why='Created by machined block.DisksController; machined decision UNKNOWN because executable package integrity is unestablished. This discovery resource describes a device during operation.'
 elif i==35:
  d='INSTALLED-OWN';s='S8.1-6,S8.2-7,S8.2-8,S8.2-16';what='Installed operating-system image'
  why='The whole installed image is a package; its recorded installation reason is explicit, not dependency. It requires its own line.'
 elif i<48:
  d='UNKNOWN';s='S8.2-7,S8.2-11,S8.2-13,S8.2-17';what=r['name']+' system service'
  why='Service status does not establish whether its configuration is an unchanged package value, installation default, or separately chosen value; the applicable recording line remains unknown.'
 elif i<82:
  cmd=m['COMMAND'].split()[0];program='systemd-udevd' if cmd=='(udev-worker)' else cmd.rsplit('/',1)[-1]
  what='Running '+program+' process'
  why=f'Execution instance of {program}; program decision UNKNOWN because package provenance or unchanged integrity is unestablished. The process is not a separate object.'
 else:
  what='Runtime loaded-module status for '+r['name']
  why='Created by machined KernelModuleStatusController; machined decision UNKNOWN because executable package integrity is unestablished. This reports loaded code, not a stored module file.'
 assert len(what.split())<=15,(i,what)
 assert len(why.split())<=30,(i,why)
 w.writerow(dict(zip(fields,[r['id'],d,s,what,b,why])));f.flush()
f.close()
out=list(csv.DictReader(path.open(),delimiter='\t'))
assert len(out)==len(rows)==len({r['id'] for r in out}) and {r['id'] for r in out}=={r['id'] for r in rows}
print(collections.Counter(r['decision'] for r in out))

import csv,re
from pathlib import Path
root=Path('A1/c1')
rows=[r for r in csv.DictReader(open('A1/in/part-2.tsv'),delimiter='\t') if r['kind'] in {'system-unit','system-units','user-unit','user-units'}]
p=root/'part-2.units.tsv'
fields=['id','decision','sentences','what_it_does','basis','reason']
seen=set()
if p.exists(): seen={r['id'] for r in csv.DictReader(p.open(),delimiter='\t')}
groups={
'debian-a3f2270221':('MUST','Expose device availability for dependency-based activation.','device','Removing device dependency objects removes their availability-driven activation capability.'),
'debian-88335c6c87':('MUST','Expose device availability to the user service manager.','device','Removing device dependency objects removes their availability-driven activation capability.'),
'debian-18fb2985ed':('MUST','Mount root, boot, credential, and runtime filesystems.','mount','All members expose mounted filesystems; removal removes their filesystem access.'),
'debian-565df89b5f':('MUST','Represent mounted storage and kernel interface filesystems.','mount','All members represent mounts; removing those mounts removes filesystem or kernel-interface access.'),
'debian-9994d7ebc4':('NOT','Reference unavailable unit definitions without running their services.','systemctl','Every member is not-found and inactive; removing absent-unit references removes no existing unit capability.'),
'debian-97fdaec6aa':('NOT','Reference an unavailable block-device preparation target.','systemctl','The target definition is absent and inactive; removing this reference removes no existing target capability.'),
'debian-0ff15b2741':('MUST','Manage manager and login-session process groups.','scope','Both scopes manage active process groups; removing them removes that process-management capability.'),
'debian-3bc8c8458c':('MUST','Manage the user service manager process group.','scope','The active scope manages processes; removal removes its process-management capability.'),
'debian-253d752b01':('MUST','Organize system and user processes into resource-control groups.','slice','Every member supplies a node in the process-resource hierarchy; removal changes process resource management.'),
'debian-b855166ba5':('MUST','Provide the root user process-resource group.','slice','Removing the root resource-management object removes its process-group resource-management function.')}
with p.open('a',newline='') as f:
 w=csv.DictWriter(f,fields,delimiter='\t',lineterminator='\n')
 if not p.stat().st_size:w.writeheader()
 for r in rows:
  if r['id'] in seen:continue
  if r['id'] in groups:
   dec,what,doc,reason=groups[r['id']]
   url='https://www.freedesktop.org/software/systemd/man/latest/'+('systemctl' if doc=='systemctl' else 'systemd.'+doc)+'.html'
   basis='doc:'+url
  else:
   dec='MUST'
   description=re.split(r' loaded \S+ \S+ ',r['evidence'],maxsplit=1)[1].split(';')[0]
   what=description.rstrip('.')+'.'
   reason='Removing this unit removes its described managed action or activation capability; its effects extend beyond the service manager.'
   basis='evidence'
  out=dict(zip(fields,[r['id'],dec,'S2.2-1,S2.2-2',what,basis,reason]))
  assert len(what.split())<=15,(r['id'],what)
  assert len(reason.split())<=30
  w.writerow(out);f.flush()
result=list(csv.DictReader(p.open(),delimiter='\t'))
assert len(result)==len(rows)==len({r['id'] for r in result})
assert {r['id'] for r in result}=={r['id'] for r in rows}
from collections import Counter
print(Counter(r['decision'] for r in result))

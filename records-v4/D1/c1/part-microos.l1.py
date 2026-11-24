import csv,json,re,collections,pathlib
csv.field_size_limit(10000000)
BASE=pathlib.Path('D1/in/raw/microos')
rows=list(csv.DictReader(open('D1/in/part-microos.tsv'),delimiter='\t'))
pfiles=list(csv.DictReader(open(BASE/'package-files.tsv'),delimiter='\t'))
pi=collections.defaultdict(list)
for p in pfiles: pi[p['path']].append(p)
fs={}
for line in open(BASE/'raw/0004-filesystem.out'):
 p=json.loads(line)
 if 'path' in p: fs[p['path']]=p
out=pathlib.Path('D1/c1/part-microos.tsv')
fields=['id','decision','sentences','what_it_does','basis','reason']
seen=set()
if out.exists(): seen={x['id'] for x in csv.DictReader(open(out),delimiter='\t')}
f=open(out,'a'); w=csv.writer(f,delimiter='\t',lineterminator='\n')
if out.stat().st_size==0:w.writerow(fields)
results=[]
def emit(x,d,s,what,b,reason,rule):
 assert len(what.split())<=15,(x['id'],what)
 assert len(reason.split())<=30,(x['id'],reason)
 results.append((x,rule,d,reason))
 if x['id'] not in seen:
  w.writerow([x['id'],d,s,what,b,reason]);f.flush();seen.add(x['id'])
def unchanged(path): return any(p['integrity']=='unchanged' for p in pi[path])
policy={}
for x in rows:
 if x['kind']=='L1:access-rule':
  content=json.loads(x['members'])['content'].replace('\\"','"')
  for a in re.findall(r'<action\s+id="([^"]+)"',content):policy[a]=x['name']
for x in rows:
 k=x['kind']; m=json.loads(x['members']); name=x['name']; rec=m.get('record','')
 if not k.startswith('L1:'):continue
 b='raw:D1/in/raw/microos/'+x['evidence'].split(';')[0]
 if k=='L1:package':
  dep=m['reason']=='dependency'
  emit(x,'INSTALLED-DERIVED' if dep else 'INSTALLED-OWN','S8.1-6,S8.2-7,S8.2-8,S8.2-16','Installed RPM package','raw:D1/in/raw/microos/objects.tsv','Installed package; retained installation reason is dependency, covered by its requesting package line.' if dep else 'Installed package; retained installation reason is explicit, requiring its own line.','packages')
 elif k=='L1:access-rule' or k=='L1:polkit-action':
  path=name if k=='L1:access-rule' else policy.get(name)
  assert path and unchanged(path),(name,path)
  emit(x,'INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16','Packaged authorization definition or supporting file','raw:D1/in/raw/microos/package-files.tsv','Unchanged packaged content; the first question decides before program or setting questions.','packaged-policy')
 elif k in ['L1:account','L1:group']:
  emit(x,'UNKNOWN','S8.2-11,S8.2-12,S8.2-13,S8.2-17','System account' if k=='L1:account' else 'System group defining account identity and access',b,'Account or rights setting; missing whether this value was created as an installation default or subsequently chosen, deciding SETTING-DEFAULT versus SETTING-OWN.','identity-origin')
 elif k in ['L1:service','L1:user-service','L1:timer','L1:user-timer']:
  # These queries expose units currently held in memory; classify the observation, not inferred persistent settings.
  emit(x,'RUNTIME','S8.2-5,S8.2-7,S8.2-16','In-memory service unit state' if 'service' in k else 'In-memory timer schedule and activation relationship',b,'systemd creates this in-memory unit state (systemd executable: INSTALLED-PACKAGE); persistent unit definitions and enablement values are separate objects.','manager-runtime')
 elif k in ['L1:unit-file','L1:user-unit-file']:
  if 'masked-runtime' in rec:
   emit(x,'RUNTIME','S8.2-5,S8.2-7,S8.2-16','Runtime service mask',b,'systemd creates this runtime mask; its unchanged packaged executable is INSTALLED-PACKAGE.','individual')
  else:
   emit(x,'UNKNOWN','S8.2-7,S8.2-11,S8.2-13,S8.2-16,S8.2-17','Listed unit definition and enablement state',b,'Missing selected definition path and enablement provenance: packaged defaults, local definitions and overrides require different lines; matching package basenames do not resolve precedence.','unit-origin')
 elif k=='L1:process':
  exe=rec.split('\t',1)[-1]
  if exe=='unknown':
   emit(x,'UNKNOWN','S8.2-5','Process with unresolved executable',b,'Runtime process is established, but its creating program and that program\'s recording decision are unavailable; failed executable lookup does not prove a kernel thread.','process-unresolved')
  elif unchanged(exe):
   emit(x,'RUNTIME','S8.2-5,S8.2-7,S8.2-16','Running process',b,f'{exe} creates this process; that unchanged packaged executable is INSTALLED-PACKAGE.','process-known')
  else:
   emit(x,'RUNTIME','S8.2-5,S8.2-9,S8.2-16','Running inventory probe process',b,'Inventory probe creates this process; probe decision UNKNOWN because its installation or derivation provenance is not retained.','individual')
 elif k in ['L1:module-name','L1:driver']:
  emit(x,'RUNTIME','S8.2-5,S8.2-7,S8.2-9,S8.2-16','Kernel module registration in sysfs' if k=='L1:module-name' else 'Kernel driver registration in sysfs',b,'Linux kernel creates this runtime registration; kernel program decision UNKNOWN because its packaged image integrity is unknown.','kernel-runtime')
 elif k=='L1:port':
  emit(x,'UNKNOWN','S8.2-5','Listening network socket',b,'Socket is runtime-only; missing owning program and its recording decision. A conventional port number does not establish ownership.','individual')
 elif k=='L1:saved-network':
  fname=('Wired connection 1' if '0d0487e3' in rec else 'Wired connection 2' if '21ab6a9a' in rec else 'lo')
  assert fs['/run/NetworkManager/system-connections/'+fname+'.nmconnection']['persistence']=='runtime'
  emit(x,'RUNTIME','S8.2-5,S8.2-7,S8.2-16','Network connection profile stored on runtime filesystem','raw:D1/in/raw/microos/raw/0004-filesystem.out','NetworkManager creates this runtime connection profile; its unchanged packaged executable is INSTALLED-PACKAGE.','individual')
 elif k=='L1:sudo-access':
  if rec.lstrip().startswith(('Matching Defaults','Runas and Command-specific','User ')):
   emit(x,'RECORD','S8.2-15','Sudo query report heading',b,'This row is a report heading emitted by sudo, not an access value or executable command.','individual')
  else:
   emit(x,'UNKNOWN','S8.2-11,S8.2-13,S8.2-17','Effective sudo access policy or environment defaults',b,'Policy values are established, but installation-default versus later-choice provenance is absent; this determines SETTING-DEFAULT versus SETTING-OWN.','individual')
 else:raise AssertionError(k)
f.close()
with open('D1/c1/part-microos.l1.rules.json','w') as f:json.dump([{'id':x['id'],'rule':r,'decision':d,'reason':s} for x,r,d,s in results],f,indent=2)
print(collections.Counter(d for x,r,d,s in results))
print('rows',len(results))

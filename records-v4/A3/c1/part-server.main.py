import csv,json,pathlib,collections,re
ROOT=pathlib.Path('A3/in/raw/server')
OUT=pathlib.Path('A3/c1/part-server.main.tsv')
FIELDS=['id','decision','sentences','what_it_does','basis','reason']
rows=list(csv.DictReader(open('A3/in/part-server.tsv'),delimiter='\t'))
packages=list(csv.DictReader(open(ROOT/'package-files.tsv'),delimiter='\t'))
by_path=collections.defaultdict(list)
for p in packages: by_path[p['path']].append(p)
existing=set()
if OUT.exists(): existing={r['id'] for r in csv.DictReader(open(OUT),delimiter='\t')}
f=open(OUT,'a',newline=''); w=csv.DictWriter(f,fieldnames=FIELDS,delimiter='\t',lineterminator='\n')
if not OUT.stat().st_size: w.writeheader();f.flush()
def emit(r,d,s,what,b,reason):
 if r['id'] in existing:return
 assert len(what.split())<=15,(r['id'],what)
 assert len(reason.split())<=30,(r['id'],reason)
 w.writerow(dict(zip(FIELDS,[r['id'],d,s,what,b,reason])));f.flush();existing.add(r['id'])
for r in rows:
 if r['kind']!='1:package':continue
 m=json.loads(r['members']); reason=m['reason']; assert reason in ('explicit','dependency')
 emit(r,'INSTALLED-OWN' if reason=='explicit' else 'INSTALLED-DERIVED','S8.1-6,S8.2-6,S8.2-7,S8.2-8,S8.2-16','Installed '+r['name'].removeprefix('dpkg:')+' package','evidence',
 'The installed package answers question one; explicit installation requires its own line.' if reason=='explicit' else 'The installed package answers question one; its recorded dependency installation is covered by the requesting package line.')
f.close()
f=open(OUT,'a',newline='');w=csv.DictWriter(f,fieldnames=FIELDS,delimiter='\t',lineterminator='\n')
for r in rows:
 k=r['kind'];m=json.loads(r['members'])
 if k=='1:process':
  path=m['record'].split('\t')[-1];name=path.rsplit('/',1)[-1]
  s='S8.2-5,S8.2-7,S8.2-16';basis='raw:server/package-files.tsv'
  if path=='unknown':
   reason='Process is runtime only. Creating program and its decision: UNKNOWN; executable identity was unavailable. Every possible creator still gives RUNTIME.';basis='raw:server/raw/0086-process-executables.out'
  elif by_path[path]:
   intact=all(x['integrity']=='unchanged' for x in by_path[path])
   reason=f'Runtime process of {name} (INSTALLED-PACKAGE); executable remains as supplied by its package.' if intact else f'Runtime process of {name} (UNKNOWN); package executable integrity is unverified, so its own recording decision cannot be established.'
  elif '/k3s/data/' in path:
   reason=f'Runtime process of extracted {name} (PROGRAM-DERIVED); K3s obtains the executable from its bundled binaries.';basis='doc:https://docs.k3s.io/blog/2025/03/25/K3s-initialization';s='S8.2-5,S8.2-9,S8.2-10,S8.2-16'
  elif path=='/usr/local/bin/node_exporter':
   reason='Runtime process of node_exporter (PROGRAM-OWN), a standalone executable outside package ownership.';basis='raw:server/raw/0004-filesystem.out';s='S8.2-5,S8.2-9,S8.2-10,S8.2-16'
  elif path=='/tmp/c1-collector/probe':
   reason='Runtime process of the inventory probe (PROGRAM-OWN); separately supplied executable code has no established covering package or generating line.';basis='raw:server/raw/0086-process-executables.out';s='S8.2-5,S8.2-9,S8.2-10,S8.2-16'
  else:
   reason=f'Runtime process of {name} (UNKNOWN); container executable provenance and integrity are unmeasured, preventing a definite recording-line decision.';basis='raw:server/raw/0086-process-executables.out'
  emit(r,'RUNTIME',s,'Running process '+r['name'],basis,reason)
 elif k=='1:module-name':
  matches=[p for p in packages if '.ko' in p['path'] and pathlib.PurePosixPath(p['path']).name.split('.ko')[0].replace('-','_')==r['name']]
  assert len(matches)==1 and matches[0]['integrity']=='unchanged',r
  emit(r,'RUNTIME','S8.2-5,S8.2-7,S8.2-8,S8.2-16','Kernel module '+r['name']+' present in running kernel','raw:server/package-files.tsv',f"Runtime module instance belongs to {r['name']} (INSTALLED-PACKAGE); its persistent module file is verified unchanged within the kernel package.")
 elif k=='1:port':
  emit(r,'RUNTIME','S8.2-5','Open '+m['record'].split()[0]+' socket '+m['record'].split()[4],'raw:server/raw/0076-port.out','Open socket is runtime only. Creating program and its decision: UNKNOWN; socket ownership was not collected. Every possible owner still gives RUNTIME.')
 elif k.startswith('1:firewall-'):
  rec=m.get('record','');serialized=json.dumps(m)
  if rec.startswith('#') or rec=='COMMIT':
   emit(r,'RECORD','S8.2-6,S8.2-15','Firewall dump comment' if rec.startswith('#') else 'Firewall dump table terminator','evidence','The dump tool generated this output marker; it is neither a firewall rule nor a command typed by a person.')
   continue
  if m.get('table')=='cal_filter' or m.get('name')=='cal_filter':
   parent='nft (INSTALLED-PACKAGE)';extra='It applies the cal-firewall rules.'
  elif 'KUBE-' in serialized or 'FLANNEL-' in serialized:
   parent='k3s (PROGRAM-DERIVED)';extra='Its controllers generate these kernel network objects.'
  elif 'DOCKER' in serialized or 'docker0' in serialized or 'br-91deedb1c880' in serialized or '172.18.' in serialized or '18081' in serialized:
   parent='dockerd (UNKNOWN: executable integrity unverified)';extra='Docker creates the kernel networking objects.'
  else:
   parent='nf_tables kernel subsystem (INSTALLED-PACKAGE)';extra='The unchanged kernel module maintains these tables and base chains.'
  emit(r,'RUNTIME','S8.2-5,S8.2-7,S8.2-16','Active kernel firewall '+k.split('-')[-1],'evidence',f'Runtime state belongs to {parent}. {extra}')
f.close()

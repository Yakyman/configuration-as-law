import csv,json,pathlib,collections,re
csv.field_size_limit(20000000)
ROOT=pathlib.Path('A3/in/raw/developer')
rows=[r for r in csv.DictReader(open('A3/in/part-developer.tsv'),delimiter='\t') if r['kind'].startswith('1:')]
pf={r['path']:r for r in csv.DictReader(open(ROOT/'package-files.tsv'),delimiter='\t')}
out=pathlib.Path('A3/c1/part-developer.runtime.tsv')
header=['id','decision','sentences','what_it_does','basis','reason']
existing={r['id'] for r in csv.DictReader(open(out),delimiter='\t')} if out.exists() else set()
f=open(out,'a'); w=csv.writer(f,delimiter='\t',lineterminator='\n')
if not out.stat().st_size:w.writerow(header)
rules=collections.defaultdict(list)
def emit(r,rule,d,s,what,basis,why):
 assert len(what.split())<=15 and len(why.split())<=30,(r['id'],what,why)
 rules[rule].append(r['id'])
 if r['id'] not in existing:w.writerow([r['id'],d,s,what,basis,why]);f.flush()
for r in rows:
 k=r['kind'];m=json.loads(r['members']); name=r['name']; ev='raw:developer/'+r['evidence'].split('; ')[-1].split(';')[0]
 if k=='1:package':
  q=m['reason']; manager=m['manager'];s='S8.2-6,S8.2-7,S8.2-8,S8.2-16'
  if '.cache/uv/' in name:
   emit(r,'cache-metadata','RECORD','S8.2-6,S8.2-15','Cached distribution metadata retained by the dependency installer.','doc:https://docs.astral.sh/uv/concepts/cache/','This metadata is inside the download cache, not an installed distribution; it records cached package information and is not executable code.')
  elif q=='explicit':emit(r,'packages-explicit','INSTALLED-OWN',s,'Explicitly installed software package.','evidence','Installed package answers the first question; explicit installation has no recorded dependency derivation and needs its own line.')
  elif q=='dependency':emit(r,'packages-dependency','INSTALLED-DERIVED',s,'Software package installed as a dependency.','evidence','Installed package answers the first question; dependency installation is explicitly covered by the originating package line.')
  else:emit(r,'packages-unknown','UNKNOWN',s,'Software package with unestablished installation provenance.','evidence','Installation reason is unknown: explicit installation needs INSTALLED-OWN, while dependency installation permits INSTALLED-DERIVED; recorded metadata does not establish which.')
 elif k.startswith('1:firewall-'):
  rec=m.get('record','')
  if rec.startswith('#') or rec=='COMMIT':
   emit(r,'dump-markers','RECORD','S8.2-15','Firewall export comment or serialization delimiter.',ev,'The export program generated this textual marker; it is neither a kernel access rule nor a command typed by a person.')
  else:
   fw=m.get('table')=='firewalld' or (k=='1:firewall-table' and name.startswith('inet/'))
   creator='firewalld (INSTALLED-PACKAGE)' if fw else 'dockerd (UNKNOWN: executable integrity)'
   emit(r,'firewall-live','RUNTIME','S8.2-5,S8.2-7,S8.2-16','Active kernel firewall '+k.split('firewall-')[1]+'.',ev,creator+' creates these volatile kernel objects; their runtime status does not depend on whether the creator requires its own line.')
 elif k=='1:process':
  path=m['record'].split('\t')[-1]; base=path.split('/')[-1]
  integ=pf.get(path,{}).get('integrity')
  if integ=='unchanged':why=base+' (INSTALLED-PACKAGE) is the unchanged packaged executable creating this process; the process is not a separate object.'
  elif path=='unknown':why='Creator executable is unidentified (UNKNOWN); every possible creator still makes this observed process runtime, so its category is determined.'
  else:why=base+' (UNKNOWN: origin or integrity unresolved) creates this process; the process remains runtime for every possible executable classification.'
  emit(r,'process-live','RUNTIME','S8.2-5,S8.2-7,S8.2-16','Running process instance.', 'raw:developer/package-files.tsv' if integ=='unchanged' else ev,why)
 elif k=='1:port':
  # Network addresses identify sockets but do not prove process ownership.
  if ':18080 ' in m['record']:
   why='docker-proxy (INSTALLED-PACKAGE) publishes the container port; the socket exists only at runtime and follows its creating executable.'
  else:why='Socket-owning program is unidentified (UNKNOWN); port numbers alone do not prove ownership. Every possible owner still makes this open socket runtime.'
  emit(r,'ports-live','RUNTIME','S8.2-5','Open listening network socket.',ev,why)
 elif k=='1:module-name':
  matches=[x for path,x in pf.items() if path.endswith('/'+name+'.ko.xz')]
  assert matches and all(x['integrity']=='unchanged' for x in matches)
  emit(r,'modules-live','RUNTIME','S8.2-5,S8.2-7,S8.2-16','Loaded kernel module instance.','raw:developer/package-files.tsv',name+'.ko.xz (INSTALLED-PACKAGE) supplies this loaded code; its unchanged stored file is distinct from the volatile loaded instance.')
 elif k in ('1:timer','1:user-timer'):
  timer=next(t for t in m['record'].split() if t.endswith('.timer'))
  emit(r,'timer-observation','RUNTIME','S8.2-5,S8.2-7,S8.2-16','Current timer schedule and service activation relationship.',ev,'systemd (INSTALLED-PACKAGE) computes '+timer+' activation times; this in-memory schedule and service relationship are not separate stored settings.')
 elif k=='1:unit-file':
  path='/usr/lib/systemd/system/'+name
  assert pf[path]['integrity']=='unchanged'
  emit(r,'unit-files','INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16','Packaged service unit definition.','raw:developer/package-files.tsv','The named unit file remains unchanged from its package; question one precedes interpreting its service parameters as settings.')
 elif k=='1:user-unit-file':
  emit(r,'user-unit-files','SETTING-OWN','S8.2-11,S8.2-13,S8.2-14,S8.2-17,S8.2-23','User service or timer definition launching project summary generation.','raw:developer/members/8eec9396036ab3dbdc3aa47b.tsv','Persistent user unit values launch the project summary program; no package supplies these custom unit files, so the setting needs its own line.')
 elif k=='1:user-service':
  emit(r,'user-service','SETTING-OWN','S8.2-13,S8.2-14,S8.2-17','User service launching a project summary program.',ev,'The enabled user service launches a program; its custom launch setting needs its own line even when currently inactive.')
 elif k=='1:service':
  emit(r,'service-provenance','UNKNOWN','S8.1-11,S8.2-13,S8.2-17','System service with observed activation state.',ev,'Services are settings, but evidence does not establish whether this service state is installation-created default or separately selected: SETTING-DEFAULT versus SETTING-OWN.')
 elif k=='1:group':
  emit(r,'group-provenance','UNKNOWN','S8.2-13,S8.2-17','Local group defining container-management access.',ev,'The group is an access setting; whether it was created during package installation or separately is unknown, preventing SETTING-DEFAULT versus SETTING-OWN.')
 elif k=='1:saved-network':
  emit(r,'network-provenance','UNKNOWN','S8.2-5,S8.2-11,S8.2-13,S8.2-17','NetworkManager connection profile for a local interface.',ev,'The listing lacks profile storage and generated/external flags; a persistent chosen network setting and a generated runtime profile cannot be distinguished.')
 elif k=='1:docker-image':
  emit(r,'container-image','UNKNOWN','S8.1-6,S8.2-7,S8.2-9,S8.2-16','Local container image supplying a runnable web server.',ev,'The image supplies executable software, but its installation or build source is unrecorded; own-line versus source-derived coverage cannot be established.')
 elif k=='1:docker-container':
  emit(r,'container-object','UNKNOWN','S8.2-5,S8.2-9,S8.2-16,S8.2-22','Runnable web-server container with filesystem and published port.',ev,'The persistent runnable container is more than its process; image provenance and relationship to a recorded source are unknown, preventing a recording-line decision.')
 else:raise RuntimeError(k)

f.close()
pathlib.Path('A3/c1/part-developer.runtime.rules.json').write_text(json.dumps(rules,indent=2))
print(collections.Counter(r['decision'] for r in csv.DictReader(open(out),delimiter='\t')))

import csv,json,collections,pathlib
ROOT=pathlib.Path('D1b/handoff/gentoo')
rows=[r for r in csv.DictReader(open('D1b/in/part-gentoo.tsv'),delimiter='\t') if r['kind'].startswith('L1:')]
files=collections.defaultdict(list)
for p in csv.DictReader(open(ROOT/'package-files.tsv'),delimiter='\t'):files[p['path']].append(p)
header=['id','decision','sentences','what_it_does','basis','reason']
out=pathlib.Path('D1b/c1/part-gentoo.1.tsv')
seen={r['id'] for r in csv.DictReader(open(out),delimiter='\t')} if out.exists() else set()
rules=collections.defaultdict(list)
def emit(r,rule,d,s,w,b,reason):
 assert len(w.split())<=15 and len(reason.split())<=30,(w,reason)
 rules[rule].append(r['id'])
 if r['id'] in seen:return
 with out.open('a') as f:
  writer=csv.writer(f,delimiter='\t',lineterminator='\n')
  if f.tell()==0:writer.writerow(header)
  writer.writerow([r['id'],d,s,w,b,reason]);f.flush()
 seen.add(r['id'])
for r in rows:
 k=r['kind'][3:];m=json.loads(r['members']);b='raw:D1b/handoff/gentoo/'+r['evidence'];rec=m.get('record','')
 if k=='package':
  if m['reason']=='explicit':emit(r,'explicit-package','INSTALLED-OWN','S8.1-6,S8.2-7,S8.2-8,S8.2-16','Explicitly selected installed package',b,'Installed package explicitly selected; no containing package or recorded dependency source establishes another covering line.')
  else:emit(r,'unknown-package','UNKNOWN','S8.2-7,S8.2-8,S8.2-16','Installed package with unresolved installation reason',b,'Package installation reason is unknown; explicit selection requires INSTALLED-OWN, installation as a dependency permits INSTALLED-DERIVED. Metadata ownership alone does not establish whole-package provenance.')
 elif k in ['account','group']:
  emit(r,'identity-origin','UNKNOWN','S8.2-11,S8.2-13,S8.2-17','Local account or group defining identity and rights','raw:D1b/handoff/gentoo/configuration-origin.tsv','Account or rights setting is present; creation history does not distinguish personal selection from a default created during package installation, changing its covering line.')
 elif k in ['module-name','driver']:
  emit(r,'sysfs-runtime','RUNTIME','S8.2-5','Live kernel module or driver registration','doc:https://docs.kernel.org/filesystems/sysfs.html','Linux kernel creates this RAM-only sysfs registration; kernel decision UNKNOWN because the running kernel is not matched to an installed file in this inventory.')
 elif k=='process':
  exe=rec.split('\t')[-1]
  aliases=[exe]
  if exe.startswith('/usr/bin/'):aliases += ['/bin/'+exe.rsplit('/',1)[-1],'/sbin/'+exe.rsplit('/',1)[-1],'/usr/sbin/'+exe.rsplit('/',1)[-1]]
  hit=[p for path in aliases for p in files[path] if p['integrity']=='unchanged']
  if hit:reason=exe+' creates this process; its unchanged package executable is INSTALLED-PACKAGE. This process exists only while the computer runs.'
  elif exe=='unknown':reason='The executing program creates this process; its identity and decision are UNKNOWN because executable lookup failed. Transience is established independently.'
  else:reason='The collector probe creates this process; its covering-line provenance is UNKNOWN. The process itself exists only while the computer runs.'
  emit(r,'process-runtime','RUNTIME','S8.2-5,S8.2-7,S8.2-16','Running process identified by process number',b,reason)
 elif k=='access-rule':
  hit=[p for p in files[r['name']] if p['integrity']=='unchanged']
  if hit:emit(r,'unchanged-access','INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16','Package-supplied authentication or authorization policy','raw:D1b/handoff/gentoo/package-files.tsv','Exact file matches its installed package reference; question one decides before its authorization-setting function, and the supplying package covers it.')
  elif r['name']=='/etc/sudoers':emit(r,'changed-sudoers','SETTING-OWN','S8.2-11,S8.2-13,S8.2-17,S8.2-23','Modified system privilege policy','raw:D1b/handoff/gentoo/package-files.tsv','Changed package comparison rules out the original default; sudo reads authorization values, requiring a setting line of its own.')
  else:emit(r,'unowned-access','UNKNOWN','S8.2-11,S8.2-13,S8.2-17','Additional system privilege grant','raw:D1b/handoff/gentoo/configuration-origin.tsv','Privilege rule is present, but historical creation is unknown: personal choice requires SETTING-OWN, installation-created default requires SETTING-DEFAULT.')
 elif k=='openrc-service':
  if rec.startswith(('Runlevel:','Dynamic Runlevel:')):
   emit(r,'report-heading','RECORD','S8.2-15','Generated runlevel heading in service status report',b,'The status command generated a report heading; this text is neither executable code nor a selected configuration value.')
  else:emit(r,'service-origin','UNKNOWN','S8.1-11,S8.2-13,S8.2-17','System service with observed running or stopped status',b,'Service is a setting; status output does not establish whether its selection is an installation default or a later choice, so the covering line remains unknown.')
 elif k=='openrc-runlevel':
  emit(r,'service-origin','UNKNOWN','S8.1-11,S8.2-13,S8.2-17','System service runlevel membership or absence',b,'Runlevel membership describes service configuration; inventory does not establish installation-default versus subsequently chosen membership, determining SETTING-DEFAULT versus SETTING-OWN.')
 elif k=='sudo-access':
  if rec.lstrip().startswith(('Matching ','Runas ','User ')):
   emit(r,'report-heading','RECORD','S8.2-15','Generated heading in effective privilege report',b,'The privilege query generated a report heading; the heading itself grants no access and selects no setting.')
  else:emit(r,'sudo-value-origin','UNKNOWN','S8.2-11,S8.2-13,S8.2-17','Effective sudo privilege or execution-environment value',b,'Effective privilege values are settings; this query does not establish whether each value remains an installation default or was chosen later.')
 elif k=='port':
  emit(r,'port-runtime','RUNTIME','S8.2-5','Currently open listening network socket',b,'Socket-owning program creates this port; its identity and decision are UNKNOWN because the socket query omitted owners. Every possible owner still makes this runtime state.')
 elif k.startswith('firewall-'):
  if rec.startswith(('#','*')) or rec=='COMMIT':
   emit(r,'report-heading','RECORD','S8.2-15','Generated firewall dump annotation or serialization delimiter',b,'Dump annotation or delimiter was produced by iptables-save; it does not itself specify a separate installed object or selected policy value.')
  elif 'DOCKER' in rec or 'docker0' in rec:
   emit(r,'docker-firewall-runtime','RUNTIME','S8.2-5,S8.2-7,S8.2-16','Active Docker bridge firewall chain or rule','doc:https://docs.docker.com/engine/network/firewall-iptables/','Docker daemon creates these live bridge rules; unchanged dockerd is INSTALLED-PACKAGE. The current in-kernel chain or rule is runtime state.')
  else:
   emit(r,'firewall-policy-runtime','RUNTIME','S8.2-5,S8.2-13,S8.2-17','Current kernel firewall chain policy and counters',b,'Firewall configuration creates this live kernel policy; source setting decision UNKNOWN because creator and default-versus-chosen provenance are unrecorded. Counters also exist only at runtime.')
 elif k=='docker-image':
  emit(r,'docker-image','UNKNOWN','S8.1-4,S8.1-6,S8.2-7,S8.2-16','Stored BusyBox image available for container creation','doc:https://docs.docker.com/reference/cli/docker/image/pull/','Docker obtains and removes the image as a whole; inventory omits whether it was explicitly selected or obtained from another recorded source, determining its covering line.')
 elif k=='docker-container':
  emit(r,'docker-container','PROGRAM-DERIVED','S8.2-9,S8.2-10,S8.2-16,S8.2-22','Stopped BusyBox container prepared to run an echo command','doc:https://docs.docker.com/reference/cli/docker/container/create/','Docker prepared this executable container from the identified BusyBox image; its program is covered by that image line. Exited status does not prevent restarting it.')
with open('D1b/c1/gentoo_l1.rules.json','w') as f:json.dump(rules,f,indent=2)
print(collections.Counter(r['decision'] for r in csv.DictReader(open(out),delimiter='\t')))

import csv,json,pathlib,collections
root=pathlib.Path('A3/c1'); inp=list(csv.DictReader(open('A3/in/part-server.tsv'),delimiter='\t'))
kinds={'2:executable-code-outside-packages','1:service','1:unit-file','1:timer','1:user-service','1:user-unit-file','1:account','1:group','1:sudo-access','1:access-rule','1:docker-container','1:docker-image'}
rows=[r for r in inp if r['kind'] in kinds]; pf=list(csv.DictReader(open('A3/in/raw/server/package-files.tsv'),delimiter='\t'))
header=['id','decision','sentences','what_it_does','basis','reason'];out=root/'part-server.code.tsv';done=set()
if out.exists():done={r['id'] for r in csv.DictReader(out.open(),delimiter='\t')}
f=out.open('a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
if not out.stat().st_size:w.writerow(header)
ruleids=collections.defaultdict(list)
for r in rows:
 k=r['kind'];n=r['name'];m=json.loads(r['members']);rec=m.get('record','');b='evidence';rule='individual'
 if k=='2:executable-code-outside-packages':
  s='S8.2-7,S8.2-9,S8.2-10,S8.2-16';what='Persistent executable code.'
  if '/var/lib/dpkg/info/' in n:
   rule='maintainer';d='UNKNOWN';why='Package metadata script; original installed bytes were not recorded for comparison. Unchanged package coverage versus modified program classification cannot be decided.';b='raw:server/package-files.tsv';what='Maintainer script executed during package configuration or removal.'
  elif '/var/lib/rancher/k3s/data/' in n:
   rule='extracted';d='PROGRAM-DERIVED';why='Executable helper extracted by the system from the K3s executable; its originating line covers this derived copy.';b='doc:https://docs.k3s.io/blog/2025/03/25/K3s-initialization';what='Bundled executable supporting cluster operation.'
  elif n.endswith('/lock'):
   d='RECORD';s='S8.2-9,S8.2-15';why='Zero-byte persistent network-allocation lock contains no code; executable permission does not make it code.';what='Persistent network-allocation lock file.'
  elif '/.bash' in n or n.endswith('/.profile'):
   d='UNKNOWN';why='Shell executes this startup code, but inventory does not establish whether a system-created copy remains derived or was independently supplied.';what='Shell startup or logout commands.'
  elif n.endswith('/node_exporter'):
   d='PROGRAM-OWN';why='Standalone local executable runs as its own process; no package owner or recorded generating source is identified.';what='Exports system metrics.'
  elif n.endswith('/k3s'):
   d='UNKNOWN';why='Standalone cluster launcher exists; installation method and unchanged package provenance are not established, leaving installed-package versus program coverage unresolved.';what='Starts the cluster control plane and node services.'
  else:
   d='PROGRAM-DERIVED';why='Installation generates this helper script; its source installation line covers the generated executable.';what='Generated cluster stop or removal script.';b='doc:https://docs.k3s.io/installation/uninstall'
 elif k in ['1:unit-file','1:user-unit-file']:
  s='S8.2-7,S8.2-8,S8.2-16';what='Service-manager unit file controlling launches.'
  base=n.split(':')[-1];hits=[x for x in pf if x['path'].endswith('/'+base) and '/systemd/' in x['path'] and x['integrity']=='unchanged']
  if hits:
   rule='unit-package';d='INSTALLED-PACKAGE';why='Unit file is owned by an installed package and its full installation digest matches; question one precedes setting classification.';b='raw:server/package-files.tsv'
  elif base=='k3s.service':
   d='UNKNOWN';s='S8.2-11,S8.2-13,S8.2-17';why='Service parameters are settings; inventory does not establish whether installation generated these values as package defaults.';b='raw:server/configuration-origin.tsv'
  else:
   d='SETTING-OWN';s='S8.2-11,S8.2-13,S8.2-17,S8.2-23';why='Local service or timer definition controls system launches; no package supplies this custom value.'
 elif k in ['1:service','1:user-service']:
  what='Loaded service state in the service manager.'
  if 'not-found' in rec:
   d='RUNTIME';s='S8.2-5,S8.2-7,S8.2-16';why='Missing-unit reference exists in systemd memory only; created by systemd, INSTALLED-PACKAGE.';b='doc:https://www.freedesktop.org/software/systemd/man/256/systemctl.html'
  elif n.startswith('cal-'):
   d='SETTING-OWN';s='S8.1-11,S8.2-13,S8.2-17';why='Custom system service governs launches and requires its own setting line, whether active or inactive.'
  else:
   rule='service-origin';d='UNKNOWN';s='S8.1-11,S8.2-13,S8.2-17';why='Service state is a setting; inventory does not establish whether its current selection is an installation default or a later choice.';b='raw:server/configuration-origin.tsv'
 elif k=='1:timer':
  what='Timer activation schedule and observed firing times.';s='S8.2-13,S8.2-17'
  if 'cal-maintenance.timer' in rec:d='SETTING-OWN';why='Custom timer schedules a system maintenance service and requires its own setting line.'
  else:
   rule='service-origin';d='UNKNOWN';why='Timer activation is a launch setting; inventory does not establish installation-default versus later chosen activation.';b='raw:server/configuration-origin.tsv'
 elif k in ['1:account','1:group']:
  what='Account identity and login rights.' if k=='1:account' else 'Group identity and membership rights.';s='S8.2-13,S8.2-17'
  if n in ['calops','users']:d='SETTING-OWN';why='Local account or added group membership determines identity and rights; no installed package provides this chosen account membership.'
  else:d='UNKNOWN';why='Identity is a setting, but package-created default versus separately created account or group is not established.';b='raw:server/configuration-origin.tsv'
 elif k=='1:sudo-access':
  if n in ['Matching','User']:
   d='RECORD';s='S8.2-15';what='Heading in a generated privilege query report.';why='This row contains a report heading, not an access permission; it is program-generated output.'
  else:d='SETTING-OWN';s='S8.2-13,S8.2-17';what='Allows privileged restart of the metrics service.';why='Specific local privilege grant is a system access rule with its own line.'
 elif k=='1:access-rule':
  what='System authentication or privilege rule.'
  if n=='/etc/pam.d/cron':d='INSTALLED-PACKAGE';s='S8.2-7,S8.2-8,S8.2-16';why='Package-provided authentication file matches its installation digest; the first question decides before the setting question.';b='raw:server/package-files.tsv'
  else:d='SETTING-OWN';s='S8.2-13,S8.2-17';why='Local privilege grant controls access; generated configuration is still a setting requiring its own line unless an installation default.'
 elif k=='1:docker-container':
  d='PROGRAM-DERIVED';s='S8.2-9,S8.2-10,S8.2-16,S8.2-22';what='Containerized server program instantiated from its image.';why='Container program runs as its own process; compose labels identify the source configuration and image from which the system obtained it.'
 elif k=='1:docker-image':
  d='UNKNOWN';s='S8.1-4,S8.1-6,S8.2-7,S8.2-16';what='Stored application image used to instantiate a server.';why='Image is installer-managed as a whole, but inventory does not establish explicit acquisition versus derivation from a recorded deployment source.'
 ruleids[rule].append(r['id'])
 if r['id'] not in done:
  assert len(what.split())<=15 and len(why.split())<=30,(r['id'],why)
  w.writerow([r['id'],d,s,what,b,why]);f.flush()
f.close()
(root/'part-server.code-rules.json').write_text(json.dumps(ruleids,indent=2))
print(len(rows),collections.Counter(r['decision'] for r in csv.DictReader(out.open(),delimiter='\t')))

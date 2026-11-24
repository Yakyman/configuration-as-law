import csv,json,re,os,collections
from pathlib import Path
csv.field_size_limit(10**8)
base=Path('D1/in/raw/alma'); rows=[r for r in csv.DictReader(open('D1/in/part-alma.tsv'),delimiter='\t') if r['kind'].startswith('L1:') and r['kind']!='L1:package']
packages=collections.defaultdict(list)
for p in csv.DictReader(open(base/'package-files.tsv'),delimiter='\t'):packages[p['path']].append(p)
fs={}
for l in open(base/'raw/0004-filesystem.out'):
 a=json.loads(l)
 if 'path' in a:fs[a['path']]=a
polkit={}
for r in rows:
 if r['kind']=='L1:access-rule':
  for a in re.findall(r'<action\s+id="([^"]+)"',json.loads(r['members']).get('content','')):polkit.setdefault(a,[]).append(r['name'])
def intact(p):return any(x['integrity']=='unchanged' for x in packages[p])
def creator(p):return 'INSTALLED-PACKAGE' if intact(p) else 'UNKNOWN'
def unitpath(n,user=False):
 paths=[p for p in fs if p.endswith('/'+n) and '/systemd/'+('user' if user else 'system')+'/' in p and '.wants/' not in p and '.requires/' not in p]
 paths.sort(key=lambda p:(0 if '/.config/' in p else 1 if p.startswith('/etc/') else 2 if p.startswith('/run/') else 3,p))
 return paths[0] if paths else next((p for p in fs if p.endswith('/'+n) and '/systemd/generator' in p),None)
out=Path('D1/c1/part-alma.2.tsv');head=['id','decision','sentences','what_it_does','basis','reason'];existing=set()
if out.exists():existing={r['id'] for r in csv.DictReader(open(out),delimiter='\t')}
f=open(out,'a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
if not out.stat().st_size:w.writerow(head)
samples=collections.defaultdict(list)
for r in rows:
 k=r['kind'][3:]; m=json.loads(r['members']);n=r['name'];rec=m.get('record','');rule='individual';d='UNKNOWN';s='S8.2-7,S8.2-13,S8.2-17';what=k.replace('-',' ')+' object';b='raw:D1/in/raw/alma/'+r['evidence'].split(';')[0];why='Default installation provenance versus later choice is not established; the required recording line depends on that fact.'
 if k in ['account','group','service','user-service']:
  rule='setting-origin';what={'account':'Existing account controlling identity and login','group':'Group identity and recorded access membership','service':'System service and activation configuration','user-service':'User service that launches programs'}[k]
  if 'not-found' in rec:d='RUNTIME';s='S8.2-5';why='systemd (INSTALLED-PACKAGE) retains a missing-unit reference only in manager memory.';rule='runtime-manager'
  if 'cal-user.service' in rec:d='SETTING-OWN';s='S8.2-13,S8.2-14,S8.2-17';why='Locally stored service selects an authentication agent to launch; its own line records that choice.';rule='individual'
 elif k=='process':
  rule='runtime-process';d='RUNTIME';s='S8.2-5';what='Process executing during the current boot';p=rec.split('\t')[-1]
  if p=='unknown':why='Unidentified executable (UNKNOWN creator decision); process is runtime-only, but executable identity was not captured.'
  else:why=f'{os.path.basename(p)} ({creator(p)} creator decision) executes this runtime-only process.'
 elif k in ['module-name','driver']:
  rule='runtime-kernel';d='RUNTIME';s='S8.2-5';what='Kernel module registration in sysfs' if k=='module-name' else 'Kernel driver registration in sysfs';why='Linux kernel (UNKNOWN creator decision: installed-image integrity unknown) creates this runtime-only sysfs registration.'
 elif k.startswith('firewall-'):
  rule='runtime-firewall';d='RUNTIME';s='S8.2-5';what='Live kernel firewall '+k.split('-')[-1];prog='netavark' if m.get('table',m.get('name'))=='netavark' else 'firewalld';why=f'{prog} (INSTALLED-PACKAGE) creates this live kernel firewall object; persistent configuration is a separate object.'
 elif k=='port':
  rule='individual';d='RUNTIME';s='S8.2-5';what='Open network socket';why='Unidentified listening program (UNKNOWN creator decision); socket listing omits the owning program, but an open port is explicitly runtime-only.'
 elif k in ['timer','user-timer']:
  rule='individual';d='RUNTIME';s='S8.2-5';what='Next runtime activation of a service timer';why='systemd (INSTALLED-PACKAGE) computes this live timer schedule from timer configuration.'
 elif k in ['unit-file','user-unit-file']:
  n=rec.split()[0];p=unitpath(n,k=='user-unit-file');what='Unit file describing service or timer behavior';rule='unit-origin'
  if p and fs[p].get('persistence')=='runtime' or rec.split()[1]=='generated':
   d='RUNTIME';s='S8.2-5';rule='runtime-manager';what='Generated unit file existing only during this boot';prog='systemd-xdg-autostart-generator' if '@autostart' in n else 'sshd socket generator';cd='INSTALLED-PACKAGE' if '@autostart' in n else 'UNKNOWN';why=f'{prog} ({cd} creator decision) creates this runtime unit; filesystem metadata establishes runtime persistence.'
  elif p and intact(p):d='INSTALLED-PACKAGE';s='S8.2-6,S8.2-7,S8.2-8,S8.2-16';why='Unit file remains as received with its package; the first question decides before settings.';rule='unchanged-package';b='raw:D1/in/raw/alma/package-files.tsv'
  elif n=='cal-user.service':d='SETTING-OWN';s='S8.2-14,S8.2-17,S8.2-23';why='Locally stored user unit selects an authentication agent to launch; systemd reads its values.';rule='individual'
  elif p and packages[p]:why='Package ownership is known, but installation integrity is unknown; unchanged package content and later settings require different decisions.'
 elif k=='polkit-action':
  rule='polkit-origin';what='Declared authorization action and its default policy';ps=polkit[n]
  if any(intact(p) for p in ps):d='INSTALLED-PACKAGE';s='S8.2-6,S8.2-7,S8.2-8,S8.2-16';why='Action declaration occurs in an unchanged packaged policy file; the first question decides before access settings.';rule='unchanged-package';b='raw:D1/in/raw/alma/package-files.tsv'
 elif k in ['access-rule','saved-network-file']:
  what='Access policy file' if k=='access-rule' else 'Stored network configuration file'
  if intact(n):d='INSTALLED-PACKAGE';s='S8.2-6,S8.2-7,S8.2-8,S8.2-16';why='File remains as received with its package; the first question decides even for code or default settings.';rule='unchanged-package';b='raw:D1/in/raw/alma/package-files.tsv'
  elif n.endswith('/lab-access'):d='SETTING-OWN';s='S8.2-13,S8.2-17,S8.2-23';why='Local sudoers value grants passwordless administrative access and is read as values, requiring its own line.'
  elif 'cal-secondary' in n or 'cal-test' in n:d='SETTING-OWN';s='S8.2-13,S8.2-17';why='Persistently stored local connection profile chooses network behavior and needs its own setting line.'
 elif k=='saved-network':
  what='NetworkManager connection profile';
  if n.startswith(('cal-secondary:','cal-test:')):d='SETTING-OWN';s='S8.2-13,S8.2-17';why='The matching persistent local connection profile configures a saved network and needs its own line.'
  elif n.startswith('lo:'):why='Listing does not establish whether the loopback profile is persistent, automatically generated, or personally selected.'
 elif k=='sudo-access':
  what='Reported sudo authorization result';
  if rec.startswith(('Matching','User ')):d='RECORD';s='S8.2-15';why='Collector retained a sudo report heading, not an access rule or an executable command.'
  elif 'NOPASSWD' in rec:d='SETTING-OWN';s='S8.2-13,S8.2-17';why='Matches local lab-access sudoers grant of passwordless administrative access.'
  elif '!visiblepw' in rec or '(ALL) ALL' in rec:d='INSTALLED-PACKAGE';s='S8.2-7,S8.2-8,S8.2-16';why='Reported default values or permission match the unchanged packaged sudoers policy.';b='raw:D1/in/raw/alma/package-files.tsv'
 elif k=='container':
  d='PROGRAM-DERIVED';s='S8.2-9,S8.2-10,S8.2-16,S8.2-22';what='Stopped restartable container executing the image command';why='Container remains startable and was created from the identified image; its executable copy is covered by that source line.'
 elif k=='container-image':
  d='PROGRAM-OWN';s='S8.2-9,S8.2-10,S8.2-16,S8.2-22';what='Stored executable container image';why='Image supplies code already executed in a container; no recorded generating source is established, so its own line is required.'
 assert len(what.split())<=15 and len(why.split())<=30,(r['id'],why)
 result=[r['id'],d,s,what,b,why]
 samples[rule].append((r,result))
 if r['id'] not in existing:w.writerow(result);f.flush()
f.close()
json.dump({k:[{'id':r['id'],'kind':r['kind'],'name':r['name'],'decision':v[1],'reason':v[5]} for r,v in vs[:10]] for k,vs in samples.items()},open('D1/c1/part-alma.2.samples.json','w'),indent=2)
print(collections.Counter(x['decision'] for x in csv.DictReader(open(out),delimiter='\t')))
print({k:len(v) for k,v in samples.items()})

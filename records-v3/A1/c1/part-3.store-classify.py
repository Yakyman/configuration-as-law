import csv,re,json,os,collections
P='A1/c1/part-3.store.tsv';N='A1/c1/part-3.store.rules.json'
rows=[r for r in csv.DictReader(open('A1/in/part-3.tsv'),delimiter='\t') if r['kind']=='system-closure-store-object']
meta=json.load(open('A1/c1/part-3.store-research.json'))
header=['id','decision','sentences','what_it_does','basis','reason']
existing={r['id'] for r in csv.DictReader(open(P),delimiter='\t')} if os.path.exists(P) else set()
rulelog=json.load(open(N)) if os.path.exists(N) else {}
doc='https://nixos.org/manual/nixpkgs/stable/#multiple-output-file-type-groups'
excluded={'dns-root-data','iana-etc','mailcap','publicsuffix-list','shared-mime-info','nss-cacert','sound-theme-freedesktop','hicolor-icon-theme','tzdata','dejavu-fonts-minimal','kmod-blacklist','kmod-debian-aliases.conf','linux-headers-static'}
with open(P,'a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not existing:w.writerow(header)
 for r in rows:
  if r['id'] in existing:continue
  n=r['name'].split('-',1)[1]; b=re.split(r'-(?=\d)',n,maxsplit=1)[0]; m=meta.get(b,{})
  out=None;rule=None
  if re.search(r'-(man|doc|info)$',n):
   rule='documentation';out=['NOT','S2.2-4','Supplies documentation for reading.','doc:'+doc,'Removing documentation removes its content; program functionality remains available.']
  elif n.endswith('-bin'):
   rule='binary-output';out=['MUST','S2.2-1,S2.2-2,S2.2-9','Provides executable commands.','doc:'+doc,'Removing this executable output removes commands the computer can run.']
  elif n.endswith(('-lib','-libgcc')):
   rule='library-output';out=['MUST','S2.2-1,S2.2-2,S2.2-10','Provides library code executed by dependent programs.','doc:'+doc,'Dependent programs execute library code with their rights; removing it removes those functions.']
  elif m.get('description','').strip() and b not in excluded:
   rule='documented-code-package';out=['MUST','S2.2-1,S2.2-2,S2.2-9,S2.2-10','Provides executable or library code for '+b+'.','doc:'+m['url'],'Documented executable or library code supplies functionality; removal makes its commands or dependent operations unavailable.']
  elif n.startswith('security-wrapper-'):
   rule='security-wrapper';out=['MUST','S2.2-9,S2.2-15','Executes a wrapped command with configured privilege transitions.','doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/security/wrappers/default.nix','Privilege wrappers execute commands and implement account rights; both must be recorded.']
  elif n.startswith('unit-script-'):
   rule='unit-script';out=['MUST','S2.2-10','Executes service lifecycle actions as shell code.','doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/lib/systemd-lib.nix','The service shell executes this script with its own rights; code must be recorded.']
  elif n.startswith('X-Restart-Triggers-'):
   rule='restart-trigger';out=['MUST','S2.2-1,S2.2-2','Determines whether configuration changes restart a service.','doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/lib/systemd-lib.nix','These inputs control service restart decisions and therefore externally running system processes.']
  elif n.endswith('.pam'):
   rule='pam-policy';out=['MUST','S2.2-1,S2.2-15','Controls authentication, account access, and session establishment.','doc:https://www.linux-pam.org/Linux-PAM-html/sag-configuration-file.html','PAM policies govern access to accounts and privileged operations, which must be recorded.']
  elif n.startswith('unit-') and not n.startswith('unit-script-'):
   rule='service-unit';out=['MUST','S2.2-1,S2.2-2','Defines service, activation, scheduling, mount, or resource-management behavior.','doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html','These unit definitions control system processes and resources; removing them removes the defined activation or management behavior.']
  if out:
   w.writerow([r['id']]+out);f.flush();rulelog[r['id']]=rule
json.dump(rulelog,open(N,'w'),indent=2)
print('Written',len(rulelog));print(collections.Counter(rulelog.values()))
for i,r in enumerate(rows):
 if r['id'] not in rulelog:print(i,r['id'],r['name'].split('-',1)[1])

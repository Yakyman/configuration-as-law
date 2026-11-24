import csv,json,collections,pathlib,re
ROOT=pathlib.Path('A3/in/raw/gaming')
OUT=pathlib.Path('A3/c1/part-gaming.code.tsv')
H=['id','decision','sentences','what_it_does','basis','reason']
rows=[r for r in csv.DictReader(open('A3/in/part-gaming.tsv'),delimiter='\t') if r['kind']=='2:code-ownership-unresolved']
pf={r['path']:r for r in csv.DictReader(open(ROOT/'package-files.tsv'),delimiter='\t')}
# Join only observed filesystem aliases, not assumed distribution conventions.
fs={}
for line in open(ROOT/'raw/0004-filesystem.out'):
 x=json.loads(line)
 if 'device' in x:fs[x['path']]=x
aliases={k:'/'+fs[k]['target'] for k in ['/bin','/sbin','/lib','/lib64'] if fs[k]['type']=='symlink'}
def norm(p):
 for a,b in aliases.items():
  if p.startswith(a+'/'):return b+p[len(a):]
 return p
natives={norm(p):v for p,v in pf.items()}
inodes=collections.defaultdict(list)
for p,x in fs.items():
 if p in pf:inodes[(x['device'],x['inode'])].append(pf[p])
# Decisions below are conditional on inventory facts, never on its class-like kind string.
rules=collections.defaultdict(list)
existing={r['id'] for r in csv.DictReader(open(OUT),delimiter='\t')} if OUT.exists() else set()
def emit(r,rule,d,s,w,b,why):
 assert len(w.split())<=15 and len(why.split())<=30
 rules[rule].append(r)
 if r['id'] not in existing:
  writer.writerow([r['id'],d,s,w,b,why]);handle.flush();existing.add(r['id'])
with OUT.open('a') as handle:
 writer=csv.writer(handle,delimiter='\t',lineterminator='\n')
 if not handle.tell():writer.writerow(H)
 for r in rows:
  p=r['name'];m=json.loads(r['members']);assert m['persistence']=='persistent' and m['type']=='file'
  match=natives.get(p)
  links=inodes[(m['device'],m['inode'])]
  if match and match['integrity']=='unchanged' or any(z['integrity']=='unchanged' for z in links):
   emit(r,'C1','INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16','AppArmor or printing code supplied unchanged by its package.','raw:gaming/package-files.tsv','Observed path aliases or identical device/inode identify unchanged packaged files; the first question decides and their package line covers them.')
  elif p.startswith('/var/lib/dpkg/info/'):
   emit(r,'C2','UNKNOWN','S8.2-6,S8.2-7,S8.2-9,S8.2-16','Package maintainer script executed during package management.','raw:gaming/package-files.tsv','Missing fact: whether this package control script remains as received. The inventory has no installation integrity record for it; questions one and two differ.')
  elif '/wine-tools/' in p:
   emit(r,'C3','UNKNOWN','S8.2-6,S8.2-7,S8.2-9,S8.2-16','Windows executable in the Wine compatibility prefix.','raw:gaming/raw/0004-filesystem.out','Missing fact: whether this executable is the unchanged packaged original, a system-created copy, or a replacement. Prefix signatures do not establish that provenance.')
  elif '/cal-7zip-tool/' in p:
   emit(r,'individual','UNKNOWN','S8.2-6,S8.2-7,S8.2-9,S8.2-16','Linux archive utility installed through the game launcher.','raw:../operator/gaming/actions-logs/actions-logs/gaming_launcher_tool.log','Lutris installation is established; whether this executable remains as received is unmeasured. That fact distinguishes the first and second questions.')
  elif '/logs/' in p and p.endswith('.txt'):
   emit(r,'C4','RECORD','S8.2-6,S8.2-15','Steam diagnostic log written during execution.','evidence','Diagnostic output is recorded by Steam as it runs; filesystem execute permission alone does not make log text executable code.')
  elif '/package/' in p and '.zip.' in p:
   emit(r,'C5','RECORD','S8.2-6,S8.2-15','Downloaded compressed update archive retained by Steam.','evidence','This cached download is not an installed package or executable file; Steam retained it while updating, so it is a program record.')
  elif p.endswith('/steam_client_metrics.bin') or p.endswith('/steam_cmd_metrics.bin'):
   emit(r,'individual','RECORD','S8.2-6,S8.2-15','Steam updater metrics saved to disk.','raw:../operator/gaming/actions-logs/actions-logs/gaming_store_runtime.log','Updater measurements are generated working records, not installed payloads, executable code, or values chosen by a person.')
  elif '/appcache/' in p:
   emit(r,'individual','RECORD','S8.2-6,S8.2-15','Cached application or package metadata retrieved by Steam.','doc:https://github.com/SteamDatabase/SteamAppInfo','Downloaded application metadata is Steam working state, not a person-selected launch command or installed payload.')
  elif '/config/' in p or p.endswith('/registry.vdf') or p.endswith('/libraryfolder.vdf') or p.endswith('/libraryfolders.vdf'):
   emit(r,'individual','UNKNOWN','S8.2-7,S8.2-11,S8.2-14,S8.2-15','Steam configuration or library-location values.','evidence','Missing fact: the stored values and whether any person-selected value launches something or grants access. Metadata alone cannot distinguish settings from records.')
  else:
   assert '/.steam/' in p or '/steamcmd/' in p,p
   emit(r,'C6','UNKNOWN','S8.2-6,S8.2-7,S8.2-8,S8.2-9,S8.2-15,S8.2-16','Steam client or compatibility-runtime resource.','raw:gaming/package-files.tsv','Missing fact: whether this resource remains as received with its installed package. No installation-integrity comparison covers it; file permissions and prefix hashes cannot decide question one.')
# Audit selection lists are written separately; the prose notes record manual examination.
with open('A3/c1/part-gaming.code.audit.json','w') as f:
 json.dump({k:[r['id'] for r in v] for k,v in rules.items()},f,indent=2)
print(collections.Counter(r['decision'] for r in csv.DictReader(open(OUT),delimiter='\t')))
print({k:len(v) for k,v in rules.items()})

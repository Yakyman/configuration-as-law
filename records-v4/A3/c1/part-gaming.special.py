import csv,json,collections,pathlib
base=pathlib.Path('A3/in/raw/gaming')
rows=[r for r in csv.DictReader(open('A3/in/part-gaming.tsv'),delimiter='\t') if r['kind'] not in ['2:stored-ownership-unresolved','2:code-ownership-unresolved']]
files={r['path']:r for r in csv.DictReader(open(base/'package-files.tsv'),delimiter='\t')}
header=['id','decision','sentences','what_it_does','basis','reason']
out=pathlib.Path('A3/c1/part-gaming.special.tsv')
seen={r['id'] for r in csv.DictReader(open(out),delimiter='\t')} if out.exists() else set()
f=open(out,'a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
if not out.stat().st_size:w.writerow(header)
def emit(r,d,s,what,basis,reason):
 if r['id'] in seen:return
 assert len(what.split())<=15 and len(reason.split())<=30,(what,reason)
 w.writerow([r['id'],d,s,what,basis,reason]);f.flush();seen.add(r['id'])
for r in rows:
 m=json.loads(r['members']);k=r['kind'];n=r['name']
 if k=='1:package':
  reason=m['reason'];manager=m['manager'];s='S8.1-4,S8.1-6,S8.2-7,S8.2-8,S8.2-16'
  if reason=='unknown':
   emit(r,'UNKNOWN',s,'Installed Python distribution','evidence','Installation reason is unknown; native metadata ownership does not establish explicit versus dependency installation of this package.')
  elif manager=='flatpak' and reason=='dependency':
   emit(r,'UNKNOWN',s,'Installed Flatpak runtime or extension','doc:https://docs.flatpak.org/en/latest/dependencies.html','Runtime classification does not establish installation reason; runtimes can be installed manually. Missing fact: explicit installation versus dependency acquisition.')
  else:
   d='INSTALLED-OWN' if reason=='explicit' else 'INSTALLED-DERIVED'
   emit(r,d,s,'Installed '+manager+' package '+n.split(':',1)[1],'evidence','Installed package; explicit installation requires its own line.' if reason=='explicit' else 'Installed dependency; covered by the recorded package from which the system obtained it.')
 elif k=='1:process':
  path=m['record'].split('\t')[-1]
  if path in files and files[path]['integrity']=='unchanged':
   emit(r,'RUNTIME','S8.2-5,S8.2-7,S8.2-16','Running process for '+path,'raw:A3/in/raw/gaming/package-files.tsv',path+' creates this process; executable is INSTALLED-PACKAGE because package ownership and unchanged installation digest are established.')
f.close()
print('Appended',len(seen),'rows')
f=open(out,'a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
for r in rows:
 if r['id'] in seen:continue
 m=json.loads(r['members']);k=r['kind'];n=r['name'];rec=m.get('record','')
 if k in ('1:service','1:user-service','1:timer','1:user-timer'):
  if k in ('1:timer','1:user-timer'):
   unit=next(x for x in rec.split() if x.endswith('.timer'));ud='/usr/lib/systemd/'+('user/' if k=='1:user-timer' else 'system/')
   assert files[ud+unit]['integrity']=='unchanged'
   what='Current in-memory timer schedule for '+unit
  else:
   unit=n if k=='1:service' else 'fluidsynth.service';ud='/usr/lib/systemd/'+('user/' if k=='1:user-service' else 'system/')
   assert files[ud+unit]['integrity']=='unchanged'
   what='Current in-memory service state for '+unit
  emit(r,'RUNTIME','S8.2-5,S8.2-7,S8.2-16',what,'raw:A3/in/raw/gaming/package-files.tsv',unit+' creates this runtime state; unchanged packaged unit definition is INSTALLED-PACKAGE.')
 elif k=='1:process':
  path=rec.split('\t')[-1]
  reason=('Collector probe creates this process; its program decision is UNKNOWN because independent acquisition versus system derivation is not established.' if path!='unknown' else 'Creator program is unidentified; its decision is UNKNOWN. Missing executable identity does not change that this observed process exists only at runtime.')
  emit(r,'RUNTIME','S8.2-5','Running process with incompletely established executable provenance','evidence',reason)
 elif k=='1:port':
  emit(r,'RUNTIME','S8.2-5','Open '+n+' socket observed by socket inventory','evidence','Creator program or socket setting is unidentified; its decision is UNKNOWN. Every possible owner still creates an ephemeral socket, not a separate stored object.')
 elif k=='1:saved-network':
  emit(r,'UNKNOWN','S8.2-5,S8.2-11,S8.2-13,S8.2-17','NetworkManager loopback connection profile','doc:https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/NetworkManager.conf.html','Missing facts: whether this profile is persistent or an automatically generated in-memory connection, and whether any persistent value was chosen or installed by default.')
 elif k=='1:user-unit-file' and 'fluidsynth' in n:
  emit(r,'INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16','Packaged FluidSynth user service unit file','raw:A3/in/raw/gaming/package-files.tsv','The named unit file is package-owned and unchanged; first question decides before considering service parameters.')
 elif k=='1:user-unit-file':
  emit(r,'RUNTIME','S8.2-5,S8.2-14,S8.2-17','Generated service unit for Lutris desktop autostart','doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.generator.html','Lutris autostart entry creates this generated runtime unit through systemd-xdg-autostart-generator; its launch choice is SETTING-OWN.')
 elif k=='2:image-container-store':
  emit(r,'UNKNOWN','S8.2-7,S8.2-9,S8.2-15,S8.2-16','Persistent Flatpak installation directory, not expanded by inventory','evidence','Complete contents and provenance are absent; installed package payloads, generated repository records and configuration cannot be separated from this unexpanded directory observation.')
 else:raise ValueError(r)
f.close()
print('Total',len(seen))

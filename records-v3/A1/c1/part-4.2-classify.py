import csv,json,re,os
from pathlib import Path
root=Path('A1/c1');rows=[x for x in csv.DictReader(open('A1/in/part-4.tsv'),delimiter='\t') if x['kind']=='system-closure-store-object'][431:862]
D=json.load(open(root/'part-4.2-package-docs.json'))
alias={'v4l-utils-minimal':'v4l-utils','colord':'colord-minimal','rest':'librest','json-glib':'json-glib-minimal','ghostscript-with-cups':'ghostscript','libinput-minimal':'libinput','fftwf':'fftw','python-wrapper':'python','libsoup':'libsoup-minimal','util-linux-with-udev':'util-linux','jack2':'jack'}
header=['id','decision','sentences','what_it_does','basis','reason'];out=root/'part-4.2.tsv'
finished={r['id'] for r in csv.DictReader(open(out),delimiter='\t')} if out.exists() else set()
f=open(out,'a');w=csv.DictWriter(f,fieldnames=header,delimiter='\t',lineterminator='\n');
if not finished:w.writeheader();f.flush()
log=json.load(open(root/'part-4.2-rules.json')) if (root/'part-4.2-rules.json').exists() else []
def emit(x,decision,sentences,what,basis,reason,rule):
 if x['id'] in finished:return
 assert len(what.split())<=15,(what,len(what.split()))
 assert len(reason.split())<=30
 w.writerow(dict(zip(header,[x['id'],decision,sentences,what,basis,reason])));f.flush();finished.add(x['id']);log.append((x['id'],rule))
for i,x in enumerate(rows):
 n=x['name'].split('-',1)[1];p=re.split(r'-\d',n)[0]
 if re.search(r'-\d',n) and not n.endswith(('.scm','.go')):
  d=D.get(alias.get(p,p))
  if not isinstance(d,dict):continue
  if p in {'xorgproto','wayland-protocols','font-bitstream-vera','font-misc-misc','font-alias','gnome-backgrounds','elementary-xfce-icon-theme','sound-theme-freedesktop','shared-mime-info','alsa-ucm-conf','xkeyboard-config','guix-icons','glibc-utf8-locales'}:continue
  what=re.sub(r'@\w+\{([^}]+)\}',r'\1',d['synopsis']).replace('\\','')
  if len(what.split())>15:what='Provides '+p+' program or library functionality'
  if n.endswith('-lib'):what='Provides runtime libraries for '+p
  emit(x,'MUST','S2.2-1,S2.2-2,S2.2-9,S2.2-10',what,'doc:'+d['url'],'Executable programs or library code provide capabilities; removal prevents their execution or dependent operations.','P')
 elif n=='activate-service.scm':
  t=open('A1/in/raw/guix/configuration/run/current-system/activate').read()
  if x['name'] in t:emit(x,'MUST','S2.2-10,S2.2-13','Executes a system activation action with the activation interpreter’s rights.','raw:guix/configuration/run/current-system/activate','The activation program explicitly primitive-loads this file; executable settings count as code.','A')
 elif n.startswith('shepherd-') and n.endswith('.go'):
  emit(x,'MUST','S2.2-2,S2.2-10','Executes compiled service registration and lifecycle code in the service manager.','doc:https://codeberg.org/guix/guix/raw/commit/d58da8a56b75af73a7b5466f7ef8a81679713aa3/gnu/services/shepherd.scm','The service manager directly loads compiled service files; removing one prevents registration, rather than merely slowing execution.','G')
f.close()
json.dump(log,open(root/'part-4.2-rules.json','w'))
print('Written total',len(finished),'missing',len(rows)-len(finished))
for i,x in enumerate(rows):
 if x['id'] not in finished:print(i,x['name'].split('-',1)[1])

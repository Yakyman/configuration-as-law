import csv,json,collections,pathlib,base64,glob
csv.field_size_limit(10000000)
B=pathlib.Path('D1/in/raw/alma'); O=pathlib.Path('D1/c1'); OUT=O/'part-alma.1.tsv'
def read(p):return list(csv.DictReader(open(p),delimiter='\t'))
def canon(p):
 for x in ['lib','lib64','bin','sbin']:
  if p.startswith('/'+x+'/'):return '/usr'+p
 return p
pf=collections.defaultdict(list)
for r in read(B/'package-files.tsv'):pf[canon(r['path'])].append(r)
fs={x['path']:x for x in map(json.loads,open(B/'raw/0004-filesystem.out')) if 'path' in x}
rows=[r for r in read('D1/in/part-alma.tsv') if r['kind']=='L2:stored-ownership-unresolved']
header=['id','decision','sentences','what_it_does','basis','reason']
if not OUT.exists():OUT.write_text('\t'.join(header)+'\n')
done={r['id'] for r in read(OUT)}
S={'package':'S8.2-6,S8.2-7,S8.2-8,S8.2-16','unknown':'S8.2-6,S8.2-7,S8.2-9,S8.2-11,S8.2-15,S8.2-16','record':'S8.2-6,S8.2-15','runtime':'S8.2-5','setting':'S8.2-11,S8.2-12,S8.2-13,S8.2-17'}
docs={'pip':'https://pip.pypa.io/en/stable/topics/caching/','npm':'https://docs.npmjs.com/cli/v8/commands/npm-cache/','dnf':'https://dnf.readthedocs.io/en/latest/conf_ref.html','font':'https://xorg.freedesktop.org/archive/X11R7.0/doc/html/fc-cache.1.html','runtime':'https://www.freedesktop.org/software/systemd/man/253/file-hierarchy.html'}
docs.update({'man':'https://manpages.debian.org/bookworm/man-db/mandb.8.en.html','python':'https://docs.python.org/3/faq/programming.html','telemetry':'https://firefox-source-docs.mozilla.org/toolkit/components/telemetry/concepts/archiving.html','logs':docs['runtime']})
def runtime_creator(p):
 mapping=[('/run/udev','systemd-udevd','INSTALLED-PACKAGE'),('/run/systemd','systemd','INSTALLED-PACKAGE'),('/run/user/1000/systemd','systemd','INSTALLED-PACKAGE'),('/run/user/1000/pulse','pipewire-pulse','INSTALLED-PACKAGE'),('/run/NetworkManager','NetworkManager','INSTALLED-PACKAGE'),('/run/containers','podman','UNKNOWN'),('/run/libpod','podman','UNKNOWN'),('/run/crun','crun','INSTALLED-PACKAGE'),('/run/chrony','chronyd','INSTALLED-PACKAGE'),('/run/cups','cupsd','INSTALLED-PACKAGE'),('/run/dbus','dbus-broker','INSTALLED-PACKAGE'),('/run/lvm','lvm','INSTALLED-PACKAGE'),('/run/lock/lvm','lvm','INSTALLED-PACKAGE'),('/run/irqbalance','irqbalance','INSTALLED-PACKAGE'),('/run/sudo','sudo','INSTALLED-PACKAGE'),('/run/tuned','tuned','INSTALLED-PACKAGE'),('/run/log','systemd-journald','INSTALLED-PACKAGE'),('/run/credentials','systemd','INSTALLED-PACKAGE')]
 for pre,a,b in mapping:
  if p==pre or p.startswith(pre+'/'):return a,b
 return 'runtime filesystem setting','UNKNOWN'
def md(p):return p.replace('/home/user','$USER_HOME').replace('/root','$ROOT_HOME')
# Every member is evaluated; directory executable bits are traversal permissions, not code.
def classify_member(m):
 p=m['path']; typ=m['type']; records=pf[canon(p)]
 if m['persistence']=='runtime':return ('RUNTIME','runtime','Runtime object disappears with its backing filesystem.')
 if any(x['integrity']=='unchanged' for x in records):return ('INSTALLED-PACKAGE','package','Unchanged package member after verified filesystem alias resolution.')
 if '/.cache/pip/' in p or p.endswith('/.cache/pip'):
  return ('RECORD','pip','Pip HTTP cache or cache directory, stored as working data.')
 if '/.npm/_cacache' in p:return ('RECORD','npm','Npm content cache or its directory, not an installed package.')
 if p.startswith('/var/cache/dnf/') or p=='/var/cache/dnf':return ('RECORD','dnf','DNF cache metadata or cache directory.')
 if (('/fontconfig/' in p or p.endswith('/fontconfig')) and ('cache' in p)):
  return ('RECORD','font','Generated font lookup cache or its directory.')
 if p.startswith('/var/cache/man/') or p=='/var/cache/man':return ('RECORD','man','Manual-page index cache, cache tag, or cache directory.')
 if typ=='directory' and p.endswith('/__pycache__'):return ('RECORD','python','Python-generated cache directory; the directory itself is not bytecode.')
 if '/datareporting/archived' in p:return ('RECORD','telemetry','Firefox telemetry archive data or archive directories.')
 if p.startswith('/var/log/'):return ('RECORD','logs','Persistent system or installer logs and their directories.')
 if p=='/etc/sudoers.d/lab-access':return ('SETTING-OWN','setting','Captured sudo access rule is locally selected and not a packaged default.')
 if records:return ('UNKNOWN','unknown','Whether this package member remains as received is unrecorded.')
 if typ=='directory':return ('UNKNOWN','unknown','Directory installation integrity and creation provenance are not established.')
 return ('UNKNOWN','unknown','Package origin, unchangedness, and source of this object are not established.')
results=[];details=[];rules=collections.defaultdict(list)
for r in rows:
 ms=read(B/json.loads(r['members'])['file']);assert len(ms)==json.loads(r['members'])['count']
 ds=[classify_member(m) for m in ms]; unique={x[0] for x in ds}; keys={x[1] for x in ds}
 basis='raw:'+str(B/json.loads(r['members'])['file'])
 if len(unique)>1:
  dec='MIXED';sent=','.join(dict.fromkeys(','.join(S.get(x[1],S['record']) for x in ds).split(',')))
  groups=collections.defaultdict(list)
  for m,d in zip(ms,ds):groups[d[0]].append(m['path'].rsplit('/',1)[-1])
  reason='; '.join(k+': '+','.join(v) for k,v in sorted(groups.items()))
  if len(reason.split())>30 or len(reason)>1000:reason='Member decisions differ: '+', '.join(sorted(unique))+'. Exact member split: part-alma.1.notes.md, '+r['id']+'.'
  what='Stored immediate members with different recording requirements.';rule='mixed'
 elif unique=={'INSTALLED-PACKAGE'}:
  dec='INSTALLED-PACKAGE';sent=S['package'];what='Unchanged packaged kernel modules or library files.';reason='Every member matches an unchanged package record through verified filesystem aliases; the package line covers each.';rule='package'
 elif unique=={'RUNTIME'}:
  dec='RUNTIME';sent=S['runtime'];a,b=runtime_creator(r['name']);what='Volatile files, links, directories, or communication endpoints.';reason=f'All members have runtime backing; created by {a} ({b}); none is a separate stored object.';rule='runtime'
 elif unique=={'RECORD'}:
  dec='RECORD';sent=S['record'];what='Program cache, log, archive, or generated cache directory.';reason='Members are documented working data or generated data directories recorded during program operation, not code or selected settings.';rule='cache';
  if len(keys)==1:basis='doc:'+docs[next(iter(keys))]
 elif unique=={'SETTING-OWN'}:
  dec='SETTING-OWN';sent=S['setting'];what='Local sudo rule grants passwordless administrative access.';reason='Captured local rule grants access to this computer and requires its own line.';basis='raw:D1/in/raw/alma/raw/0226-metadata-read-0.out';rule='sudo'
 else:
  dec='UNKNOWN';sent=S['unknown'];rule='unknown'
  if all(m['type']=='directory' for m in ms):what='Stored directory members organizing files.';reason='Missing facts: directory installation integrity and whether directories were created by installation, another program, or a person.'
  elif '/node_modules/' in r['name']:what='Installed JavaScript package directory members.';reason='Missing fact: per-member unchangedness and provenance; npm inventory explicitly lacks matching lock records and per-file provenance.'
  elif '/systemd/' in r['name']:what='Service configuration links or directories.';reason='Missing facts: installation default versus selected value, and directory provenance; these determine package coverage or an own line.'
  else:what='Stored files or directory members with unresolved provenance.';reason='Missing facts: package origin and unchangedness, or otherwise member creation provenance and executable content; these determine classification and recording line.'
 out=dict(zip(header,[r['id'],dec,sent,what,basis,reason]));results.append(out);rules[rule].append(r['id'])
 details.append((r,ms,ds,rule))
 if r['id'] not in done:
  with open(OUT,'a') as f:csv.DictWriter(f,fieldnames=header,delimiter='\t',lineterminator='\n').writerow(out)
# Details are independently reproducible from raw immediate-member rows, not recursive expansion.
with open(O/'part-alma.1.details.json','w') as f:json.dump([{'id':r['id'],'rule':rule,'directory':md(r['name']),'members':[{'member':md(m['path']),'type':m['type'],'persistence':m['persistence'],'decision':d[0],'rule':d[1],'reason':d[2]} for m,d in zip(ms,ds)]} for r,ms,ds,rule in details],f,indent=2)
with open(O/'part-alma.1.rules.json','w') as f:json.dump(rules,f,indent=2)
print(collections.Counter(r['decision'] for r in read(OUT)))

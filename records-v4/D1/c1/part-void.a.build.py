import csv,json,collections,pathlib
csv.field_size_limit(10000000)
base=pathlib.Path('D1/in/raw/void'); out=pathlib.Path('D1/c1/part-void.a.tsv')
rows=[x for x in csv.DictReader(open('D1/in/part-void.tsv'),delimiter='\t') if x['kind']=='L2:stored-ownership-unresolved'][:1015]
pkg=collections.defaultdict(list)
for x in csv.DictReader(open(base/'package-files.tsv'),delimiter='\t'):pkg[x['path']].append(x)

# Every row and every member is inspected by the predicate; absent integrity never implies unchanged.
S='S8.2-6,S8.2-7,S8.2-15,S8.2-16'
U=('UNKNOWN',S,'Package provenance, installation integrity, and creator are unestablished; these facts distinguish installed objects, programs, settings, records, and material.')
def runtime(p):
 if '/runit/' in p: who='/usr/bin/runsv (INSTALLED-PACKAGE)'
 elif '/udev/' in p or p=='/run/udev':who='/usr/bin/udevd (INSTALLED-PACKAGE)'
 elif '/NetworkManager' in p:who='/usr/bin/NetworkManager (INSTALLED-PACKAGE)'
 elif '/chrony' in p:who='/usr/bin/chronyd (INSTALLED-PACKAGE)'
 elif '/dbus' in p:who='/usr/bin/dbus-daemon (INSTALLED-PACKAGE)'
 elif '/blkid' in p:who='/usr/bin/blkid (INSTALLED-PACKAGE)'
 elif '/docker' in p:who='dockerd program (UNKNOWN)'
 elif '/containerd' in p:who='containerd program (UNKNOWN)'
 elif '/dhcpcd' in p:who='dhcpcd program (INSTALLED-PACKAGE)'
 elif '/mdadm' in p:who='mdadm program (INSTALLED-PACKAGE)'
 elif '/initramfs' in p:who='dracut program (INSTALLED-PACKAGE)'
 elif '/node-compile-cache' in p:who='node program (UNKNOWN)'
 elif '/mozrunner' in p:who='mozrunner program (UNKNOWN)'
 elif '/resolvconf' in p:who='resolvconf program (INSTALLED-PACKAGE)'
 elif '/lvm' in p:who='LVM program (UNKNOWN)'
 elif '/mount' in p:who='mount program (UNKNOWN)'
 else:who='runtime filesystem setting (UNKNOWN)'
 return ('RUNTIME','S8.2-5',f'Runtime-only object belongs to {who}; its filesystem is explicitly runtime.')
def member(v):
 p=v['path'];name=p.rsplit('/',1)[-1]
 if v['persistence']=='runtime':return runtime(p)
 if any(z['integrity']=='unchanged' for z in pkg[p]):return ('INSTALLED-PACKAGE','S8.2-7,S8.2-8,S8.2-16','Unchanged packaged member is covered by its package line.')
 if '/.cache/pip/' in p or p.endswith('/.cache/pip'):
  return ('RECORD','S8.2-15','Pip generated cache storage and response or wheel records; these are persistent cache data, not installed package contents.')
 if '/.npm/_cacache' in p or '/.npm/_logs' in p or p.endswith('/.npm/_update-notifier-last-checked'):
  return ('RECORD','S8.2-15','Npm generated persistent cache, index, or log storage while operating; no earlier question applies to these working records.')
 if '/supervise/' in p or p.endswith('/supervise'):
  return ('RECORD','S8.2-15','Runsv records supervision state here; persistence prevents treating the stored status and control paths as runtime-only objects.')
 if p in ['/etc/NetworkManager/system-connections/cal-secondary.nmconnection','/etc/NetworkManager/system-connections/cal-test.nmconnection']:
  return ('SETTING-OWN','S8.2-11,S8.2-12,S8.2-13,S8.2-17','Action log confirms newly added network choices; saved connections govern the computer and require their own lines.')
 if '/cal-check/datareporting' in p or '/cal-check/storage' in p or '/firefox/Profile Groups' in p:
  return ('RECORD','S8.2-15','Browser-generated telemetry or database working storage records operation; it is persistent data rather than executable code or chosen system settings.')
 return U
existing=set()
if out.exists():existing={x['id'] for x in csv.DictReader(open(out),delimiter='\t')}
side=open('D1/c1/part-void.a.members.tsv','w'); sw=csv.writer(side,delimiter='\t',lineterminator='\n');sw.writerow(['id','member','decision','sentences','reason'])
with open(out,'a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not out.exists() or out.stat().st_size==0:w.writerow(['id','decision','sentences','what_it_does','basis','reason'])
 for i,r in enumerate(rows):
  meta=json.loads(r['members']);m=list(csv.DictReader(open(base/meta['file']),delimiter='\t'));assert len(m)==meta['count'] and meta['complete']
  z=[(v,member(v)) for v in m]
  for v,(d,s,re) in z:sw.writerow([r['id'],v['path'].replace('/home/user/','~/'),d,s,re])
  decisions={v[1][0] for v in z};sentences=','.join(dict.fromkeys(s for v in z for s in v[1][1].split(',')))
  if len(decisions)==1:
   d=next(iter(decisions));reason=z[0][1][2]
   if d=='RUNTIME' and len({v[1][2] for v in z})>1:reason='Runtime members belong to creators and decisions individually listed in part-void.a.members.tsv; all exist only on runtime filesystems.'
  else:
   d='MIXED';summary='; '.join(k+': '+','.join(v['path'].rsplit('/',1)[-1] or '/' for v,dec in z if dec[0]==k) for k in sorted(decisions))
   reason=summary if len(summary.split())<=27 and len(summary)<500 else 'Member assignments: '+', '.join(sorted(decisions))+'. Exact member-to-decision mapping appears in part-void.a.members.tsv under this id.'
  what='Stored immediate children provide filesystem content and structure.'
  if '/.cache/pip' in r['name']:what='Pip cache directories, HTTP responses, and locally cached wheels.'
  elif '/.npm/' in r['name']:what='Npm cache content, indexes, or operation logs.'
  elif '/lib/modules/' in r['name']:what='Kernel module files and directories provide loadable kernel functionality.'
  elif '/node_modules' in r['name']:what='JavaScript package contents and directories support installed Node applications.'
  elif '/cal-marionette' in r['name']:what='Python package contents support browser automation.'
  elif '/run/' in r['name']:what='Runtime service state and communication paths.'
  elif '/.mozilla/' in r['name']:what='Browser profile storage, installed extensions, and working data.'
  if r['id'] not in existing:w.writerow([r['id'],d,sentences,what,'raw:D1/in/raw/void/'+meta['file'],reason]);f.flush()
side.close()
print(collections.Counter(x['decision'] for x in csv.DictReader(open(out),delimiter='\t')))

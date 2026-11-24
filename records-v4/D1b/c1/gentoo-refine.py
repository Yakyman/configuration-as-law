import csv,pathlib,json,collections
base=pathlib.Path('D1b/c1')
def read(p):return list(csv.DictReader(open(p),delimiter='\t'))
def write(p,rows):
 with open(p,'w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
inputs={r['id']:r for r in read('D1b/in/part-gentoo.tsv')};out=read(base/'part-gentoo.tsv');ledger=read(base/'gentoo-member-decisions.tsv')
# Direct directory members are not recursively substituted with their separately inventoried contents.
changed=set()
for a in ledger:
 p=a['member']
 if p=='/var/lib/docker' and a['rule']=='individual-overlap':
  a.update(decision='UNKNOWN',rule='directory-origin',reason='Directory creator and original package metadata are unrecorded; package-supplied, program-created and personal directories have different decisions.');changed.add(a['id'])
 if a['rule']=='opaque-browser-database':
  r=inputs[a['id']];ms=read('D1b/handoff/gentoo/'+json.loads(r['members'])['file']);m=next(m for m in ms if m['path']==p)
  if m['type']=='directory':a.update(decision='RECORD',rule='browser-profile-record',reason='Firefox creates storage directory structure as working state; this member is the directory, not its separately inventoried contents.');changed.add(a['id'])
# Runtime evidence establishes lifetime irrespective of parent uncertainty. Supply the actual parent where known.
def parent(p):
 if '/openrc' in p:return 'OpenRC','INSTALLED-PACKAGE'
 if p.startswith('/run/udev'):return 'systemd-udevd','INSTALLED-PACKAGE'
 if p.startswith('/run/dhcpcd'):return 'dhcpcd','INSTALLED-PACKAGE'
 if p.startswith(('/run/containerd','/run/nri')):return 'containerd','INSTALLED-PACKAGE'
 if p.startswith('/run/docker'):return 'dockerd','INSTALLED-PACKAGE'
 if p.startswith('/run/agetty'):return 'agetty','INSTALLED-PACKAGE'
 if p.startswith('/run/sshd'):return 'sshd','INSTALLED-PACKAGE'
 if p.startswith('/run/sudo'):return 'sudo','INSTALLED-PACKAGE'
 if p.startswith('/run/initramfs'):return 'initramfs boot scripts','UNKNOWN'
 if p=='/run/initctl':return 'init','INSTALLED-PACKAGE'
 if p.startswith('/run/user/1000'):return 'cal-user service','UNKNOWN'
 if p=='/run/xtables.lock':return 'iptables','INSTALLED-PACKAGE'
 if p=='/run/runlevel':return 'OpenRC','INSTALLED-PACKAGE'
 if p=='/run/utmp':return 'init/login','INSTALLED-PACKAGE'
 return 'boot/session setup','UNKNOWN'
for a in ledger:
 if a['decision']=='RUNTIME':
  n,d=parent(a['member']);a['reason']=f'{n} creates this transient member; parent decision {d}.'
by=collections.defaultdict(list)
for a in ledger:by[a['id']].append(a)
for r in out:
 if r['id'] in changed:
  ds={a['decision'] for a in by[r['id']]};r['decision']=next(iter(ds)) if len(ds)==1 else 'MIXED'
  if r['decision']=='MIXED':r['reason']='Member decisions: '+', '.join(sorted(ds))+'. Exact per-member partition and missing facts: gentoo-member-decisions.tsv, keyed by this id.'
  elif r['decision']=='RECORD':r['reason']='Firefox creates these directory entries as storage working state; directory contents are separate inventory members.'
  elif r['decision']=='UNKNOWN':r['reason']='Directory creator and original package metadata are unrecorded; package-supplied, program-created and personal directories have different decisions.'
 if r['decision']=='RUNTIME' and r['id'] in by:
  pp=sorted(set(parent(a['member']) for a in by[r['id']]))
  r['sentences']='S8.2-5,S8.2-7,S8.2-16'
  if len(pp)<=3:r['reason']='Creators: '+', '.join(n+' ('+d+')' for n,d in pp)+'. Every member is transient.'
  else:r['reason']='OpenRC, systemd-udevd, dockerd, containerd, dhcpcd, init, login, sudo, sshd, agetty, iptables: INSTALLED-PACKAGE; boot/session setup: UNKNOWN. Exact member-parent mapping: gentoo-member-decisions.tsv.'
for r in out:assert len(r['reason'].split())<=30
write(base/'part-gentoo.tsv',out);write(base/'gentoo-member-decisions.tsv',ledger)
print('Refined direct-directory interpretation',len(changed),'and runtime parent descriptions')

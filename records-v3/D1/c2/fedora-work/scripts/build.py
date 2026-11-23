# Build D1/c2/part-fedora.tsv rows from the input table. Rules documented in part-fedora.notes.md.
import csv,json,re,sys,os
csv.field_size_limit(10**9)
INP='../../in/part-fedora.tsv'; OUT='../part-fedora.tsv'
rpm={}
for l in open('tables/rpm-decisions.tsv'):
    f=l.rstrip('\n').split('\t'); rpm[f[0]]=f   # name,dec,sent,what,reason,src,basis
done=set()
if os.path.exists(OUT):
    for r in csv.DictReader(open(OUT),delimiter='\t'): done.add(r['id'])
skip=set(sys.argv[1:])  # ids left for manual rows
def clean(s): return re.sub(r'[\t\r\n]+',' ',s).strip()
def W(s,n): return ' '.join(s.split()[:n])
def basis_raw(ev): return 'raw:'+ev.split(':')[0] if ev.startswith('raw/') else 'evidence'
FLAT={}
for l in open('tables/flatpak.tsv'):
    f=l.rstrip('\n').split('\t'); FLAT[f[0]]=f[1:]
def decide(r):
    k=r['kind']; n=r['name']; m=json.loads(r['members']); ev=r['evidence']; b=basis_raw(ev)
    m0=m[0] if m and isinstance(m[0],str) else json.dumps(m[0]) if m else ''
    if k=='L1:package:rpm':
        nm=n.split(':',1)[1]; f=rpm[nm]
        return f[1],f[2],f[3],f[6],f[4]
    if k=='L1:account':
        u=m0.split(':')
        return 'MUST','S2.2-15','Account %s (uid %s, shell %s)'%(u[0],u[2],u[6]),b,'S2.2-15 states that accounts must be recorded.'
    if k=='L1:group':
        g=m0.split(':')
        return 'MUST','S2.2-15','Group account %s (gid %s)%s'%(g[0],g[2],(' with members '+g[3]) if g[3] else ''),'doc:https://man7.org/linux/man-pages/man8/groupadd.8.html','groupadd(8) calls a group a group account; S2.2-15 states that accounts must be recorded.'
    if k=='L1:access-rule':
        return 'MUST','S2.2-15','sudo rule letting the account run any command as any user','raw:'+ev.split(':')[0],'Grants the right to become superuser; S2.2-15 states that this right must be recorded.'
    if k=='L1:port':
        prog=re.search(r'users:\(\("([^"]+)"',m0); p=prog.group(1) if prog else '?'
        return 'MUST','S2.2-15','Socket %s open for connections, held by %s'%(n.split()[-1],p),b,'S2.2-15 states that ports open for connection must be recorded.'
    if k in ('L1:firewall-rule',):
        return 'MUST','S2.2-15','nftables rule in firewalld table, chain %s'%json.loads(r['members'])[0].get('chain','?'),b,'S2.2-15 states that firewall rules must be recorded.'
    if k in ('L1:firewall-chain','L1:firewall-table','L1:firewall-ct helper'):
        o=json.loads(r['members'])[0]
        what={'L1:firewall-chain':'nftables chain %s of firewalld table holding rules%s'%(o.get('name'),', hook '+o['hook'] if 'hook' in o else ''),
              'L1:firewall-table':'nftables table firewalld holding all firewall chains and rules',
              'L1:firewall-ct helper':'nftables conntrack helper for NetBIOS name service replies'}[k]
        return 'MUST','S2.2-15,S2.2-2',what,b,'Part of the firewall rule set (S2.2-15); removing it removes its rules or its effect on traffic, so filtering changes (S2.2-2).'
    if k=='L1:process':
        parts=m0.split('\t'); exe=parts[-1]; extra=len(parts)-2
        w='Running process %s'%exe+(' plus %d pids without readable exe link'%extra if extra>0 else '')
        return 'MUST','S2.2-9,S2.2-12',W(w,15),b,'A program that runs on the computer must be recorded (S2.2-9); pids lacking an exe link are other running processes or kernel threads, also running code.'
    if k=='L1:module':
        return 'MUST','S2.2-10,S2.2-2','Loaded kernel module %s, code running with kernel rights'%n,b,'Code the kernel executes with its own rights must be recorded (S2.2-10); unloading it removes the function it provides.'
    if k=='L1:driver':
        drv=m0.split('\t')[1].split('/')[-1]
        return 'MUST','S2.2-10,S2.2-2',W('Kernel driver %s bound to device %s'%(drv,n.replace('/driver','').split('/')[-1]),15),b,'Driver code runs with kernel rights (S2.2-10); unbinding it makes the device unusable (S2.2-2).'
    if k=='L1:polkit-actions':
        return 'MUST','S2.2-1,S2.2-2,S2.2-15','Polkit action %s: declares who may perform this privileged operation'%n,'doc:https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html','Declares implicit authorizations for a privileged operation, i.e. users\' rights; without the declaration the mechanism cannot authorize it, so the operation becomes impossible.'
    if k in ('L1:service','L1:user-service'):
        st=m0.split(); st=st[1:] if st[0]=='*' else st
        unit=st[0]; load,act,sub=st[1],st[2],st[3]
        scope='user ' if k=='L1:user-service' else ''
        if load=='not-found':
            return 'NOT','S2.2-1,S2.2-2','Name of %sunit %s referenced elsewhere; no unit file exists'%(scope,unit),b,'Nothing exists behind the name, so removing it changes nothing the computer does or can do; the removal test fails.'
        return 'MUST','S2.1-3,S2.2-1,S2.2-2','Loaded %sservice %s (%s/%s) started by the service manager'%(scope,unit,act,sub),b,'A service the service manager can start or runs; after removal it cannot be started, so something becomes impossible.'
    if k in ('L1:unit-file','L1:user-unit-file'):
        st=m0.split(); unit,state=st[0],st[1]
        scope='user ' if k=='L1:user-unit-file' else ''
        if state=='masked':
            return 'HOLE','S2.2-1,S2.2-2','Masked %sunit %s'%(scope,unit),b,'Behaviour depends on the mask (S2.2-1) but removing it makes something possible, not impossible (S2.2-2).'
        what={'alias':'Alias name %s pointing to another unit, used for activation by that name',
              'generated':'Unit %s generated at login from an autostart entry; starts a program',
              'static':'Static unit file %s, started by dependency or activation',
              'indirect':'Unit file %s enabled through another unit (Also=)',
              'enabled-runtime':'Unit file %s enabled for this boot only',
              'enabled':'Enabled unit file %s, started automatically',
              'disabled':'Disabled unit file %s, can be started on demand'}[state]%unit
        return 'MUST','S2.1-3,S2.2-1,S2.2-2',W(scope.capitalize()+what if scope else what,15),b,'The unit file lets the service manager start the unit; after removal starting it (by this name) becomes impossible.'
    if k in ('L1:timer','L1:user-timer'):
        t=m0.split()[-2]
        return 'MUST','S2.1-3,S2.2-1,S2.2-2','Active %stimer %s that starts its service on schedule'%('user ' if k=='L1:user-timer' else '',t),b,'An enabled timer starts its service; after removal the scheduled runs stop.'
    if k=='L1:network':
        nm=m0.split(':')
        if nm[2]=='802-11-wireless':
            return 'MUST','S2.2-14','Saved Wi-Fi network profile %s (autoconnect off)'%nm[0],b,'S2.2-14 states that a saved Wi-Fi network must be recorded.'
        return 'MUST','S2.1-3,S2.2-1,S2.2-2','Saved NetworkManager %s profile %s%s'%(nm[2],nm[0],(' active on '+nm[3]) if nm[3] else ', not active'),b,'Addressing and routing of its interface depend on this saved network (S2.2-1); after removal it can no longer be activated with these settings.'
    if k=='L1:network-link':
        f=m0.split()
        return 'MUST','S2.2-1,S2.2-2','Network interface %s (%s), not managed by systemd-networkd'%(f[1],f[2]),b,'Network traffic over this interface depends on it; if it is removed, communication over it becomes impossible.'
    if k=='L1:container':
        return 'MUST','S2.2-9,S2.2-12','Stopped Podman container cal-container from alpine:3.22 running /bin/echo',b,'A program in a container must be recorded (S2.2-9, S2.2-12); after removal the container can no longer be started.'
    if k=='L1:container-image':
        return 'MUST','S2.2-9,S2.2-2','Podman image alpine:3.22 holding the programs of cal-container',b,'Programs in containers must be recorded (S2.2-9); without the image the container\'s programs cannot run.'
    if k=='L1:package:flatpak':
        f=FLAT[n]; return f[0],f[1],f[2],f[3],f[4]
    raise Exception('no rule '+k)
rows=list(csv.DictReader(open(INP),delimiter='\t'))
new=not os.path.exists(OUT)
o=open(OUT,'a')
if new: o.write('id\tdecision\tsentences\twhat_it_does\tbasis\treason\n')
c=0
for r in rows:
    if r['id'] in done or r['id'] in skip: continue
    d=decide(r)
    o.write('\t'.join([r['id']]+[clean(x) for x in d])+'\n'); c+=1; o.flush()
print('wrote',c)

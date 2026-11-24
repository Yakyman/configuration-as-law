import csv,json,re,collections,posixpath
from pathlib import Path
csv.field_size_limit(20000000)
ROOT=Path('A3/in/raw/gaming')
OUT=Path('A3/c1')
def read(p):
    return list(csv.DictReader(open(p),delimiter='\t'))
rows=[r for r in read('A3/in/part-gaming.tsv') if r['kind']=='2:stored-ownership-unresolved']
members={r['id']:read(ROOT/json.loads(r['members'])['file']) for r in rows}
norm=lambda p:'/usr'+p if p.split('/')[1] in ['bin','sbin','lib','lib64'] else p
pf=collections.defaultdict(list)
for p in read(ROOT/'package-files.tsv'):pf[norm(p['path'])].append(p)
paths={m['path'] for ms in members.values() for m in ms}
fs={}; inodes=collections.defaultdict(list)
for ln in open(ROOT/'raw/0004-filesystem.out'):
    try:d=json.loads(ln)
    except ValueError:continue
    p=d.get('path')
    if not p:continue
    if p in paths:fs[p]=d
    if norm(p) in pf and 'device' in d and 'inode' in d:
        inodes[(d['device'],d['inode'])].extend(pf[norm(p)])
for p,d in fs.items():
    for f in inodes.get((d.get('device'),d.get('inode')),[]):
        if f not in pf[norm(p)]:pf[norm(p)].append(f)
packages={r['id']:r for r in read(ROOT/'objects.tsv') if r['kind']=='package'}
origins={r['path']:r for r in read(ROOT/'configuration-origin.tsv')}
def present(pkg):
    return next((r for r in packages.values() if r['name']=='dpkg:'+pkg),None)
def package_decision(pkg):
    r=present(pkg)
    if not r:return 'UNKNOWN'
    return {'explicit':'INSTALLED-OWN','dependency':'INSTALLED-DERIVED'}.get(json.loads(r['members']).get('reason'),'UNKNOWN')
def runtime_creator(p):
    if p in ['/run/user/1000','/run/user/113','/run/user']:return 'systemd'
    if p.startswith('/run/log/'):return 'systemd'
    if p.startswith('/run/lvm/'):return 'lvm2'
    if p.startswith('/run/console-setup/'):return 'console-setup'
    if p.startswith('/run/initramfs/'):return 'initramfs-tools'
    if p=='/run/tmpfiles.d/static-nodes.conf':return 'kmod'
    if re.match(r'/run/user/\d+/pulse/',p):return 'pipewire-pulse'
    if p.startswith('/run/udev/'):return 'udev'
    if p.startswith('/run/systemd/'):return 'systemd'
    if '/systemd/' in p and p.startswith('/run/user/'):return 'systemd'
    if 'systemd-private-' in p:return 'systemd'
    for prefix,pkg in [('/run/NetworkManager/','network-manager'),('/run/avahi-daemon/','avahi-daemon'),('/run/blkid/','util-linux'),('/run/cups/','cups-daemon'),('/run/dbus/','dbus'),('/run/fsck/','util-linux'),('/run/irqbalance/','irqbalance'),('/run/lightdm/','lightdm'),('/run/speech-dispatcher/','speech-dispatcher'),('/run/uuidd/','uuid-runtime'),('/tmp/.X11-unix/','xserver-xorg-core')]:
        if p.startswith(prefix) or p==prefix.rstrip('/'):return pkg
    if p.startswith('/run/user/'):
        for component,pkg in [('/gnupg/','gpg-agent'),('/keyring/','gnome-keyring'),('/dbus-1/','dbus'),('/dconf/','dconf-service'),('/gcr/','gcr4'),('/speech-dispatcher/','speech-dispatcher'),('/at-spi/','at-spi2-core')]:
            if component in p:return pkg
    return None

def classify(m):
    p=m['path'];base=p.rsplit('/',1)[-1]; facts=pf.get(norm(p),[])
    if m['persistence']=='runtime':
        creator=runtime_creator(p)
        if creator:
            cd=package_decision(creator)
            return ('RUNTIME','S8.2-5,S8.2-7,S8.2-16','Transient runtime state',f'{creator} ({cd}) creates these runtime objects; filesystem evidence establishes their transient lifetime.','runtime')
        return ('UNKNOWN','S8.2-5','Transient filesystem object','Runtime lifetime is established, but the creating program or setting and its recording decision are not established.','runtime-unknown')
    if any(f['integrity']=='unchanged' for f in facts):
        return ('INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16','Unchanged installed package member','The manifest verifies unchanged package content, including observed aliases or identical inodes; its package line covers it.','package')
    if p.startswith('/usr/lib/python3/dist-packages/') and '/__pycache__/' in p and base.endswith('.cpython-312.pyc'):
        source=p.split('/__pycache__/')[0]+'/'+base.split('.cpython-')[0]+'.py'
        if any(f['integrity']=='unchanged' for f in pf.get(source,[])):
            return ('PROGRAM-DERIVED','S8.2-9,S8.2-10,S8.2-16','Compiled Python module cache','Python bytecode is compiled from an unchanged installed source module; the source package line covers the compiled program.','bytecode')
    # This rule is restricted to observed logging locations, not arbitrary executable-bit files.
    if m['type']=='file' and ((p.startswith('/var/log/') and base!='README') or '/actions-logs/' in p or '/.steam/debian-installation/logs/' in p or '/steamcmd/linux32/logs/' in p or p.endswith('/.cache/lutris/lutris.log')):
        return ('RECORD','S8.2-15,S8.2-2','Program diagnostic or activity log','Programs write these diagnostics and activity histories while running; they are records, not executable code.','logs')
    if p.startswith('/var/lib/dpkg/info/') and base.endswith('.list'):
        return ('RECORD','S8.2-15,S8.2-2','Package manager installed-file list','The package manager records installed paths as operational state; this list is not code or a person-chosen setting.','dpkg-lists')
    if facts:
        return ('UNKNOWN','S8.2-7,S8.2-9,S8.2-16','Package-associated stored object','Package association is established, but integrity is unknown; unchanged installed content and altered content may receive different decisions.','integrity')
    if m['type']=='directory':
        return ('UNKNOWN','S8.2-7,S8.2-15,S8.2-16','Persistent directory entry','Missing fact: whether this directory was obtained unchanged with a package, created by a program, or created by a person.','provenance')
    if p in origins:
        return ('UNKNOWN','S8.2-7,S8.2-11,S8.2-14,S8.2-17','Stored configuration or state file','Missing facts: package provenance and integrity, or whether its effective value was person-chosen versus created during installation.','provenance')
    return ('UNKNOWN','S8.2-7,S8.2-9,S8.2-15,S8.2-16','Persistent file or link','Missing facts: package provenance and unchanged status; absent provenance also leaves code derivation or record/material origin unestablished.','provenance')

def assemble(r):
    ms=members[r['id']]; desc=json.loads(r['members'])
    assert desc['complete'] and len(ms)==desc['count']
    ds=[classify(m) for m in ms]
    decisions=set(d[0] for d in ds)
    sent=','.join(dict.fromkeys(s for d in ds for s in d[1].split(',')))
    if len(decisions)==1:
        dec=ds[0][0]
        if len(set(d[3] for d in ds))==1:what,reason=ds[0][2:4]
        elif dec=='UNKNOWN':what='Stored objects with unresolved provenance';reason='Missing member-specific facts: package provenance, integrity, derivation, configuration origin, or runtime creator; exact missing facts are in the member map.'
        elif dec=='RUNTIME':what='Transient service and session state';reason='Runtime creators and their decisions are named for every member in part-gaming.groups.members.tsv; all members exist only during operation.'
        else:what='Stored objects sharing one decision';reason='Every member receives this decision; individual evidence and reasoning appear in part-gaming.groups.members.tsv.'
    else:
        dec='MIXED';what='Stored members with different recording decisions'
        reason='; '.join(sorted(decisions))+'. Exact member assignments: part-gaming.groups.members.tsv, this id.'
        reasons={
            'gaming-2dac226320b6f354608c3b7b':'lutris.log: RECORD; all other members: UNKNOWN because package or creation provenance is missing.',
            'gaming-d6e7cd8207d135165f0e39be':'NetworkManager, avahi-daemon, blkid, cups, dbus, fsck, irqbalance, lightdm, speech-dispatcher, user, uuidd: RUNTIME; other members: UNKNOWN creator. Creator decisions: part-gaming.groups.members.tsv.',
            'gaming-fc557f3125938f34d3727148':'34 unchanged manifest files: INSTALLED-PACKAGE; remaining files and links: UNKNOWN provenance or integrity. Exact assignments: part-gaming.groups.members.tsv.',
            'gaming-7045b2cfb39b6919d6cbb076':'alsa-utils.service, saned.service, sound.target.wants: UNKNOWN integrity; all other members: INSTALLED-PACKAGE, verified unchanged through manifest aliases.',
            'gaming-b5b399a1952d145cba092894':'11 unchanged manifest files: INSTALLED-PACKAGE; nine symlinks and hwdb.bin: UNKNOWN integrity or provenance. Exact assignments: part-gaming.groups.members.tsv.',
            'gaming-4b2f118928192eae89e5ccb0':'78 unchanged manifest files: INSTALLED-PACKAGE; remaining files and links: UNKNOWN provenance or integrity. Exact assignments: part-gaming.groups.members.tsv.',
            'gaming-3c49d8ede866731e9d36a16a':'All .list inventories: RECORD; remaining metadata and maintainer scripts: UNKNOWN package integrity or provenance. Exact assignments: part-gaming.groups.members.tsv.',
            'gaming-ef0828c6f747894897b5efe1':'Regular log/history files: RECORD; README and directories: UNKNOWN package or creation provenance. Exact assignments: part-gaming.groups.members.tsv.'}
        reason=reasons[r['id']]
    return [r['id'],dec,sent,what,'raw:A3/in/raw/gaming/'+desc['file'],reason],ds

if __name__=='__main__':
    import sys
    if '--inspect' in sys.argv:
        selection=collections.defaultdict(list)
        for r in rows:
            o,ds=assemble(r)
            for rule in set(d[-1] for d in ds):
                if len(selection[rule])<10:selection[rule].append((r,ds))
        for rule,rs in selection.items():
            print('\nRULE',rule)
            for r,ds in rs:
                print(r['id'],r['name'],len(ds),collections.Counter(d[0] for d in ds))
                print(' | '.join(m['path'].rsplit('/',1)[-1]+':'+d[0] for m,d in zip(members[r['id']],ds))[:1600])
    else:
        output=OUT/'part-gaming.groups.tsv';existing={r['id'] for r in read(output)} if output.exists() else set()
        with open(output,'a') as f,open(OUT/'part-gaming.groups.members.tsv','w') as mf:
            w=csv.writer(f,delimiter='\t',lineterminator='\n');mw=csv.writer(mf,delimiter='\t',lineterminator='\n')
            if not existing:w.writerow(['id','decision','sentences','what_it_does','basis','reason'])
            mw.writerow(['id','member_index','member','decision','sentences','reason','rule'])
            for r in rows:
                o,ds=assemble(r)
                if r['id'] not in existing:w.writerow(o);f.flush()
                for i,(m,d) in enumerate(zip(members[r['id']],ds),1):
                    # Index and basename identify the exact entry in the cited complete member table.
                    mw.writerow([r['id'],i,m['path'].rsplit('/',1)[-1],d[0],d[1],d[3],d[4]])
        got=read(output)
        assert collections.Counter(r['id'] for r in got)==collections.Counter(r['id'] for r in rows)
        assert all(len(r['what_it_does'].split())<=15 and len(r['reason'].split())<=30 for r in got)
        print(collections.Counter(r['decision'] for r in got))

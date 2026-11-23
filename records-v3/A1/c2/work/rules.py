import sys,json,re
sys.path.insert(0,'c2/work')
from emit import emit,inrows
pc=json.load(open('c2/work/pkgclass.json'))
rows=[]
for r in inrows():
    i,_,m,k,name,mem,ev=r
    if k=='account':
        rows.append([i,'MUST','S2.2-15',f'Account {name} in the user database'[:200],'raw:raw/coreos/accounts.txt',
          'S2.2-15 states accounts must be recorded; no sentence exempts system accounts.'])
    elif k=='kernel-module':
        rows.append([i,'MUST','S2.2-10,S2.2-2',f'Loaded kernel module {name}: driver code running inside the kernel','raw:raw/coreos/modules.txt',
          'Module code runs with the kernel\'s own rights, so it can do whatever the kernel can (S2.2-10); unloading removes its driver function.'])
    elif k=='process':
        what='Kernel threads: the running kernel\'s own execution contexts' if name=='kernel threads' else f'Running process of program {name}'
        rows.append([i,'MUST','S2.2-9,S2.2-2',what,'raw:raw/coreos/processes.txt',
          'A program that runs on the computer must be recorded regardless of how it was installed (S2.2-9); stopping it stops what it does.'])
    elif k in ('system-unit','user-unit'):
        st=ev.split(': ',1)[1].split(' ')
        masked = st[1]=='masked'
        if masked:
            rows.append([i,'MUST','S2.2-1,S2.2-2',f'Masked unit {name}: mask prevents systemd from starting it','raw:raw/coreos/units.txt',
              'Removing the mask makes the unit startable at boot, changing what the computer does; behaviour depends on it (S2.2-1, S2.2-2).'])
        else:
            u = 'systemd user-manager unit' if k=='user-unit' else 'systemd unit'
            rows.append([i,'MUST','S2.2-1,S2.2-2',f'{u} {name} defined by a unit file'[:120],'raw:raw/coreos/'+('user-list-units.txt' if k=='user-unit' else 'units.txt'),
              'Removing the unit file makes starting the unit impossible and stops what it starts, mounts or listens on (S2.2-2).'])
    elif k=='package':
        v=pc[name]
        if v['nex']>0:
            ex=v['ex'][0]
            rows.append([i,'MUST','S2.2-2,S2.2-9',f'Package shipping programs or libraries, e.g. {ex}','doc:https://mdapi.fedoraproject.org/f44/files/'+name,
              'Removing it removes executables or libraries, so running them becomes impossible (S2.2-2); programs are recorded however installed (S2.2-9).'])
print(len(rows), emit(rows))

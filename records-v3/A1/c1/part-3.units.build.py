import csv,re,os
from collections import Counter
src=list(csv.DictReader(open('A1/in/part-3.tsv'),delimiter='\t'))
rows=[r for r in src if r['kind'] in ('system-unit','system-units','user-unit','user-units')]
out='A1/c1/part-3.units.tsv'
header=['id','decision','sentences','what_it_does','basis','reason']
existing=list(csv.DictReader(open(out),delimiter='\t')) if os.path.exists(out) else []
seen={r['id'] for r in existing}
reasons={
'service':'Controls execution of a separate process; removing this definition removes its managed execution, which is computer behavior under S2.2-1/2.',
'socket':'Controls an IPC endpoint and service activation; removing it removes connection or activation behavior beyond the service manager.',
'mount':'Controls filesystem mounting; removal removes the configured mount capability and access behavior, not merely stored content.',
'target':'Groups and orders other units; removing it removes a named activation or synchronization capability affecting system services.',
'slice':'Controls resource grouping of separate processes; this affects their execution and is not confined to one program interface.',
'timer':'Schedules another unit; removal removes timed execution, a computer behavior, rather than merely historical data.',
'path':'Watches paths to activate another unit; removal removes automatic process activation, a computer behavior.'}
with open(out,'a',newline='') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not existing: w.writerow(header)
 for r in rows:
  if r['id'] in seen: continue
  typ=r['name'].rsplit('.',1)[-1]
  basis='raw:A1/in/raw/nixos/'+('user-list-units.txt' if r['kind'].startswith('user') else 'units.txt')
  decision='MUST'; sentences='S2.2-1,S2.2-2'
  if r['kind'].endswith('units'):
   what,reason={
    'device':('Exposes kernel devices as dependency and activation units.','Device units participate in mount, socket and service dependencies; removing this mechanism removes device-dependent activation behavior.'),
    'mount':('Represents mounted filesystems and their management dependencies.','All listed members provide filesystem mounts; removing those mounts removes filesystem access or kernel-interface capabilities.'),
    'scope':('Groups existing processes for lifecycle and resource management.','All members organize running processes and resource control; removing this management removes operational behavior.'),
    'slice':('Groups system or user processes for hierarchical resource management.','All members establish process resource groups; those groups control execution beyond the service manager itself.'),
    'socket':('Listens for local SSH connections and activates service processes.','Removing the local SSH socket removes that connection path and its service activation behavior.'),
    'not-found':('Retains references to absent units; operational dependency effects are unestablished.','Not-found proves missing definitions, not harmless references. Inventory omits dependency relationships needed to establish what these retained unit objects do.')
   }[typ]
   if typ=='not-found': decision='UNKNOWN'; sentences='S3-1,S3-2'
  else:
   desc=r['evidence'].split(';')[0].split(' loaded ',1)[1].split(' ',2)[2]
   prefix={'service':'Manages','socket':'Provides','target':'Groups and orders','slice':'Groups processes for','timer':'Schedules','path':'Monitors','mount':'Mounts'}[typ]
   what=prefix+' '+desc.rstrip('.')+'.'
   assert len(what.split())<=15,(r['id'],what)
   reason=reasons[typ]
   if r['name']=='linger-users.service':
    what='Configures whether user service managers persist beyond login sessions.'
    basis='doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/config/users-groups.nix'
   if r['name']=='network-local-commands.service':
    what='Runs networking commands during network initialization.'
    basis='doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/tasks/network-interfaces.nix'
   if r['name']=='post-boot.service':
    what='Runs configured boot and shutdown command hooks.'
    basis='doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/config/power-management.nix'
   if r['name']=='logrotate.timer': what='Schedules log rotation service execution.'
  assert len(reason.split())<=30,(r['id'],reason)
  w.writerow([r['id'],decision,sentences,what,basis,reason]);f.flush()
check=list(csv.DictReader(open(out),delimiter='\t'))
assert len(check)==len(rows)==len({r['id'] for r in check})
assert {r['id'] for r in check}=={r['id'] for r in rows}
assert all(r['decision'] in {'MUST','NOT','HOLE','UNKNOWN','MIXED'} for r in check)
print(Counter(r['decision'] for r in check))

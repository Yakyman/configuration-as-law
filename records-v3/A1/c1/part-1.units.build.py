import csv,pathlib,collections,re
root=pathlib.Path('A1/c1')
rows=[r for r in csv.DictReader(open('A1/in/part-1.tsv'),delimiter='\t') if r['kind'] in ('system-unit','user-unit','system-units','user-units')]
out=root/'part-1.units.tsv'
fields=['id','decision','sentences','what_it_does','basis','reason']
existing=list(csv.DictReader(open(out),delimiter='\t')) if out.exists() else []
seen={r['id'] for r in existing}
functions={
 'service':'Controls service process execution',
 'socket':'Provides socket activation and communication endpoints',
 'target':'Groups and orders activation of other units',
 'timer':'Schedules activation of another unit',
 'path':'Triggers another unit from filesystem events',
 'slice':'Organizes process groups and their resource management',
 'mount':'Controls filesystem mount availability',
 'automount':'Triggers filesystem mounting on access'}
reasons={
 'service':'Removing this service definition prevents its managed invocation; its effect reaches a separate process, not only manager-internal settings.',
 'socket':'Removing this definition removes its managed communication or activation endpoint, changing capabilities beyond the service manager.',
 'target':'Removing this synchronization and grouping definition changes how other units can be activated and ordered.',
 'timer':'Removing this schedule stops the corresponding timed activation; the effect reaches the activated service.',
 'path':'Removing this watch stops its event-triggered activation; the effect reaches the activated unit.',
 'slice':'Removing this resource-management definition changes grouping and control of independent processes.',
 'mount':'Removing this mount definition prevents its managed filesystem access, changing capabilities outside the manager.',
 'automount':'Removing this definition stops automatic mounting on access, changing filesystem availability outside the manager.'}
manual={
 'coreos-ca040c10df':('MUST','S2.2-1','Blocks activation of the repartitioning service','raw:coreos/unit-realpaths.tsv','The mask determines what can be started. Its restriction changes computer behaviour even though removing it permits more activity.'),
 'coreos-a3f2270221':('MUST','S2.2-1,S2.2-2','Exposes devices to unit dependency and activation management','doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.device.html','All members expose device availability for dependent units; removing these dependency objects changes service and mount activation capabilities.'),
 'coreos-88335c6c87':('MUST','S2.2-1,S2.2-2','Exposes devices to user-manager dependency and activation management','doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.device.html','All members expose device availability for dependent units; removing these dependency objects changes managed activation capabilities.'),
 'coreos-18fb2985ed':('MUST','S2.2-1,S2.2-2','Represents active system filesystem mounts and their dependencies','raw:coreos/units.txt','All listed mounts provide filesystem access and participate in mount management; removing the mounts loses those capabilities.'),
 'coreos-565df89b5f':('MUST','S2.2-1,S2.2-2','Represents active filesystem mounts visible to the user manager','raw:coreos/user-list-units.txt','All listed mounts provide filesystem access and participate in mount management; removing the mounts loses those capabilities.'),
 'coreos-9994d7ebc4':('NOT','S2.2-1,S2.2-2','Lists names of absent unit definitions','raw:coreos/units.txt','Every member is not-found and inactive; no implemented unit functionality exists to remove or declare.'),
 'coreos-97fdaec6aa':('NOT','S2.2-1,S2.2-2','Lists two absent block-device target definitions','raw:coreos/user-list-units.txt','Both targets are not-found and inactive; no implemented target functionality exists to remove or declare.'),
 'coreos-0ff15b2741':('MUST','S2.2-1,S2.2-2','Groups the service manager and login-session processes for resource management','doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.scope.html','Both scopes group running processes for lifecycle and resource management; removing those controls changes what the computer does.'),
 'coreos-3bc8c8458c':('MUST','S2.2-1,S2.2-2','Groups the service manager process for resource management','doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.scope.html','The scope groups a running process for lifecycle and resource management; removing those controls changes what the computer does.'),
 'coreos-253d752b01':('MUST','S2.2-1,S2.2-2','Organizes system and user process groups in the resource hierarchy','doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.slice.html','All members establish process-resource hierarchy; removing this management changes the computer’s control of independent processes.'),
 'coreos-b855166ba5':('MUST','S2.2-1,S2.2-2','Provides the root of the process-resource hierarchy','doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.slice.html','The root slice organizes process-resource management; removing this hierarchy changes management of processes beyond internal program settings.'),
 'coreos-eb57ff0e5c':('MUST','S2.2-1,S2.2-2,S2.2-15','Provides local and virtual-machine socket endpoints for remote-login service activation','raw:coreos/units.txt','Both members are listening login sockets; removing them loses connection endpoints and their service activation.')}
with open(out,'a',newline='') as f:
 w=csv.DictWriter(f,fields,delimiter='\t',lineterminator='\n')
 if not existing:w.writeheader()
 for r in rows:
  if r['id'] in seen:continue
  if r['id'] in manual:
   d,s,fun,b,why=manual[r['id']]
  else:
   assert r['kind'] in ('system-unit','user-unit') and ' loaded ' in r['evidence'],r
   typ=r['name'].rsplit('.',1)[1]
   d,s,fun,b,why='MUST','S2.2-1,S2.2-2',functions[typ],'evidence',reasons[typ]
   # The service descriptor is identification evidence; the decision uses the unit control function.
  result=dict(zip(fields,[r['id'],d,s,fun,b,why]))
  assert len(fun.split())<=15 and len(why.split())<=30,result
  w.writerow(result);f.flush()
print(collections.Counter(x['decision'] for x in csv.DictReader(open(out),delimiter='\t')))

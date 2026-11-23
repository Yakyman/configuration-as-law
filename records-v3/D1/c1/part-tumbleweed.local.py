import csv,json,re,collections,pathlib
base=pathlib.Path('D1/c1')
rows=list(csv.DictReader(open('D1/in/part-tumbleweed.tsv'),delimiter='\t'))
header=['id','decision','sentences','what_it_does','basis','reason']
units='https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html'
ctl='https://www.freedesktop.org/software/systemd/man/latest/systemctl.html'
polkit='https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html'
nft='https://netfilter.org/projects/nftables/manpage.html'
rules={
'accounts':('MUST','S2.2-15','Defines an operating-system account.','evidence','Accounts are explicitly required, including accounts without interactive login.'),
'groups':('MUST','S2.2-1,S2.2-2','Defines a system group identity and its supplementary membership.','doc:https://www.man7.org/linux/man-pages/man5/group.5.html','Removal eliminates the named group identity and membership mapping used across programs for credentials and access.'),
'services':('MUST','S2.2-1,S2.2-2,S2.2-9','Provides a service that executes a program under the service manager.','evidence','The loaded service runs or can start its program; removing it removes that service activation capability.'),
'missing_services':('UNKNOWN','S3-1,S3-2','Names a service whose unit definition was not found.','evidence','The definition is missing; the listing cannot establish commands, retained effects, or dependencies of this particular object.'),
'units':('MUST','S2.2-1,S2.2-2,S2.2-13','Controls activation of services, sockets, or scheduled programs.','doc:'+units,'Removal changes service activation capability. Its effects govern other processes, so the single-program settings exemption does not apply.'),
'masked':('MUST','S2.2-1','Prevents activation of a named service.','doc:'+ctl,'The mask determines which service can start; removing it changes that restriction on computer behavior.'),
'timers':('MUST','S2.2-1,S2.2-2','Schedules activation of a service.','doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html','Removing the timer removes its scheduled activation of another program; this is behavior, not merely past execution history.'),
'processes':('MUST','S2.2-9,S2.2-12','Runs the executable identified by the process inventory.','evidence','The executable is observed as a running process; programs running on the computer must be recorded.'),
'bad_processes':('UNKNOWN','S3-1,S3-2','Identifies a PID without establishing its executable.','raw:D1/in/raw/tumbleweed/raw/076-process.sh','The collector concatenated multiple PIDs before one executable; that executable belongs to the last PID, not the named object.'),
'modules':('MUST','S2.2-1,S2.2-10','Runs loaded module code within the kernel.','doc:https://man7.org/linux/man-pages/man2/init_module.2.html','Loaded module code executes in kernel space with kernel privileges, rather than confinement to an application interface.'),
'drivers':('MUST','S2.2-1,S2.2-2','Binds a device to the driver controlling it.','doc:https://docs.kernel.org/driver-api/driver-model/binding.html','The binding supplies driver control of the device; removing that binding removes this device-control path.'),
'firewall_rules':('MUST','S2.2-15','Applies a packet-processing match, verdict, or control-flow rule.','evidence','Firewall rules are explicitly required, including jump rules and rules without a currently matching packet.'),
'firewall_chains':('MUST','S2.2-1,S2.2-2,S2.2-15','Provides a hooked chain, rule container, or referenced firewall jump target.','doc:'+nft,'Every inventoried chain contains rules, has a hook, or is referenced by rules; its removal removes or invalidates required firewall behavior.'),
'polkit':('MUST','S2.2-1,S2.2-2','Defines an authorization action for requests between programs.','doc:'+polkit,'Removing the action removes its registered authorization operation. Effects concern requesting and privileged programs, not settings confined to one program.')}
def classify(x):
 k=x['kind']; m=json.loads(x['members'])[0]
 if k.startswith('L1:package:'):return None
 simple={'L1:account':'accounts','L1:group':'groups','L1:module':'modules','L1:driver':'drivers','L1:firewall-rule':'firewall_rules','L1:firewall-chain':'firewall_chains','L1:polkit-actions':'polkit'}
 if k in simple:return simple[k],rules[simple[k]]
 if k in ['L1:service','L1:user-service']:
  q='missing_services' if 'not-found' in m else 'services';assert q=='missing_services' or 'loaded' in m
  return q,rules[q]
 if k in ['L1:unit-file','L1:user-unit-file']:
  q='masked' if 'masked' in m else 'units';return q,rules[q]
 if k in ['L1:timer','L1:user-timer']:return 'timers',rules['timers']
 if k=='L1:process':
  q='processes' if len(m.replace('\\t','\t').split('\t'))==2 else 'bad_processes';return q,rules[q]
 if k=='L1:access-rule':return 'individual',('MUST','S2.2-15','Permits running commands with superuser privileges.','evidence','The displayed sudo permission grants the right to become superuser, explicitly required by the text.')
 if k=='L1:port':
  if '631' in m:what='Accepts printing connections on a loopback TCP port.'
  elif '5353' in m:what='Receives multicast DNS traffic on a UDP port.'
  else:what='Receives time-service control requests on a loopback UDP port.'
  return 'individual',('MUST','S2.2-1,S2.2-2,S2.2-15',what,'evidence','The listening socket enables communication; removing it removes that endpoint. Open ports are explicitly required.')
 if k=='L1:network':
  if '802-11-wireless' in m:return 'individual',('MUST','S2.2-14','Stores a saved Wi-Fi connection profile.','evidence','Saved Wi-Fi networks are explicitly required; this object is the profile, not just its password.')
  return 'individual',('MUST','S2.2-1,S2.2-2','Defines a saved Ethernet or loopback network configuration.','doc:https://networkmanager.dev/docs/api/latest/nm-settings-nmcli.html','Removing the profile removes that stored network activation configuration, which configures networking used beyond the managing program.')
 if k=='L1:firewall-table':return 'individual',('MUST','S2.2-1,S2.2-2,S2.2-15','Contains the active IPv4 and IPv6 firewall chains and rules.','doc:'+nft,'Removing this populated table removes its firewall rules; the rules and their behavior must be recorded.')
 if k=='L1:container':return 'individual',('MUST','S2.2-2,S2.2-9,S2.2-12','Stores a restartable container executing an echo command.','doc:https://docs.podman.io/en/latest/markdown/podman-start.1.html','The exited container remains startable; its program executes as a separate process, explicitly included rather than exempted as confined code.')
 if k=='L1:container-image':return 'individual',('MUST','S2.2-2,S2.2-9,S2.2-12','Supplies the Alpine filesystem and programs for starting containers.','doc:https://docs.podman.io/en/latest/markdown/podman-run.1.html','This installed image supplies container programs that run as separate processes. Removing it removes that local program source.')
 raise ValueError(k)
out=base/'part-tumbleweed.tsv'
seen={x['id'] for x in csv.DictReader(out.open(),delimiter='\t')} if out.exists() else set()
groups=collections.defaultdict(list)
with out.open('a',encoding='utf-8',newline='') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not seen:w.writerow(header);f.flush()
 for x in rows:
  got=classify(x)
  if got is None:continue
  label,v=got;groups[label].append(x)
  if x['id'] in seen:continue
  assert len(v[2].split())<=15 and len(v[4].split())<=30
  w.writerow([x['id'],*v]);f.flush()
print('Local decisions appended:',sum(map(len,groups.values())))
print({k:len(v) for k,v in groups.items()})
# Explicitly record inspected sample IDs. These evenly spread rows were read from the input,
# with separate examination of malformed process lines, missing definitions and masked units.
with (base/'part-tumbleweed.local-checks.json').open('w') as f:
 json.dump({k:[x['id'] for x in (a if k in ['individual','masked'] else [a[round(i*(len(a)-1)/9)] for i in range(10)])] for k,a in groups.items()},f,indent=2)

import csv,json,re
from pathlib import Path
ROOT=Path('D1/c1')
rows=list(csv.DictReader(open('D1/in/part-fedora.tsv'),delimiter='\t'))
HEADER=['id','decision','sentences','what_it_does','basis','reason']
K={'L1:account','L1:package:flatpak','L1:process','L1:module','L1:driver','L1:port','L1:network','L1:network-link','L1:access-rule','L1:container','L1:container-image'}
selected=[r for r in rows if r['kind'] in K]
out=ROOT/'part-fedora.tsv'
seen={r['id'] for r in csv.DictReader(out.open(),delimiter='\t')} if out.exists() else set()
rules={}
def result(r,d,s,w,b,why,rule=None):
 if rule:rules.setdefault(rule,[]).append((r,w,why))
 return dict(zip(HEADER,[r['id'],d,s,w,b,why]))
with out.open('a',encoding='utf8',newline='') as f:
 wr=csv.DictWriter(f,HEADER,delimiter='\t',lineterminator='\n')
 if not seen:wr.writeheader()
 for r in selected:
  k=r['kind']; name=r['name']; member=json.loads(r['members'])[0].replace('\\t','\t')
  raw='raw:D1/in/'+r['evidence']
  if k=='L1:account':
   x=result(r,'MUST','S2.2-15','Defines a local account and its user identity.',raw,'Accounts are explicitly required, including service accounts without interactive login.','accounts')
  elif k=='L1:module':
   x=result(r,'MUST','S2.2-10',f'Runs {name} code inside the kernel.',raw,'Loaded kernel modules execute with kernel rights; the same-rights code requirement applies.','modules')
  elif k=='L1:driver':
   driver=member.split('\t')[-1].split('/')[-1]
   x=result(r,'MUST','S2.2-1,S2.2-2,S2.2-10',f'Binds {driver} kernel driver code to a device.',raw,'The binding exposes executing driver code; removing that driver removes its device operations.','drivers')
  elif k=='L1:port':
   addr=member.split()[4]; proto=member.split()[0].upper()
   x=result(r,'MUST','S2.2-1,S2.2-2,S2.2-15',f'Accepts {proto} traffic at {addr}.',raw,'Removing this socket prevents traffic reception there; open connection ports are explicitly required.','ports')
  elif k=='L1:process':
   parts=member.split('\t')
   if len(parts)==2:
    x=result(r,'MUST','S2.2-9,S2.2-12',f'Runs {parts[-1].split("/")[-1]} as a process.',raw,'The executable is observed running as its own process; programs must be recorded.','processes')
   else:
    x=result(r,'UNKNOWN','S3-1,S3-2','Process function is unidentified because the inventory joins several PIDs.',raw,'The row names the first PID; its executable lookup failed. The trailing executable belongs to another PID, so its function cannot be assigned.','unidentified_processes')
  elif k=='L1:access-rule':
   x=result(r,'MUST','S2.2-15','Authorizes all commands as any target account through sudo.',raw,'This explicit sudo grant includes the right to become superuser, which must be recorded.')
  elif k=='L1:network':
   if '802-11-wireless' in member:
    x=result(r,'MUST','S2.2-14','Stores a Wi-Fi connection profile.',raw,'A saved Wi-Fi network is explicitly required; this row identifies the profile, not its password.')
   elif 'loopback' in member:
    x=result(r,'MUST','S2.2-1,S2.2-2','Configures the loopback network connection.',raw,'The profile configures a system network interface used across programs; it is not confined to one program.')
   else:
    x=result(r,'MUST','S2.2-1,S2.2-2','Stores an Ethernet network connection profile.',raw,'This profile determines system networking available to other programs; removing it removes that configured connection.')
  elif k=='L1:network-link':
   link=member.split()[1]
   x=result(r,'MUST','S2.2-1,S2.2-2',f'Provides the {link} network interface for packet communication.',raw,'Removing the interface removes communication through it. Unmanaged means unmanaged by networkd, not absent or without function.')
  elif k=='L1:container':
   x=result(r,'MUST','S2.2-9,S2.2-12','Runs an echo command as a restartable container process.',raw,'The stored container executes a program as its own process; container isolation is explicitly not an exemption.')
  elif k=='L1:container-image':
   x=result(r,'MUST','S2.2-1,S2.2-9,S2.2-12','Supplies the executable filesystem used to create the inventoried container.',raw,'This image supplies container programs that run as their own processes; the container-program requirement applies.')
  elif k=='L1:package:flatpak':
   if 'org.gnome.Platform.Locale/' in name:
    x=result(r,'MUST','S2.2-1,S2.2-2','Supplies runtime locale rules for sorting, character handling, parsing and formatting.','doc:https://gitlab.com/freedesktop-sdk/freedesktop-sdk/-/raw/master/elements/integration/split-locales.bst','Runtime locale definitions change library behavior across applications; removing them removes locale-specific operations, beyond merely losing translated text.')
   elif '.Locale/' in name:
    x=result(r,'NOT','S2.2-3,S2.2-4','Supplies translated interface text for the calculator application.','doc:https://docs.flatpak.org/en/latest/flatpak-builder-command-reference.html','Calculator translations supply interface content; removing them loses translated text while calculator operations remain available.')
   elif 'org.gnome.Calculator/' in name:
    x=result(r,'MUST','S2.2-9,S2.2-12','Performs arithmetic and mathematical calculations.','doc:https://apps.gnome.org/Calculator/','This is an executable application; Flatpak installation is explicitly included in the program requirement.')
   elif 'org.gnome.Platform/' in name:
    x=result(r,'MUST','S2.2-1,S2.2-2,S2.2-10','Provides runtime dependencies needed by installed applications.','doc:https://docs.flatpak.org/en/latest/basic-concepts.html','Applications require this runtime to run; its libraries execute with the consuming application rights.')
   elif '.GL.default/' in name:
    extra='-extra' in name
    x=result(r,'MUST','S2.2-10','Provides graphics driver code'+(' and additional codec support.' if extra else '.'),'doc:https://docs.flatpak.org/en/latest/extension.html','Runtime driver libraries execute with the consuming application rights, satisfying the same-rights code requirement.')
   elif '.codecs-extra/' in name:
    x=result(r,'MUST','S2.2-10','Provides additional multimedia codec code.','doc:https://docs.flatpak.org/en/latest/extension.html','Codec libraries execute with application rights and add media decoding capabilities; they are code, not interface settings.')
   else:raise AssertionError(name)
  else:raise AssertionError(k)
  assert len(x['what_it_does'].split())<=15,x
  assert len(x['reason'].split())<=30,x
  assert all('\t' not in v and '\n' not in v for v in x.values()),x
  if r['id'] not in seen:
   wr.writerow(x);f.flush();seen.add(r['id'])

notes=ROOT/'part-fedora.main.notes.md'
intro='''# Fedora c1: accounts, execution, devices, networking and application formats

Only the assigned input and its raw Fedora inventory were read. No removal was performed. Classification applies S2.2 and S3-1/S3-2. Inventory labels from an earlier definition are disregarded. Rows identify logical inventory objects: a driver link evidences its bound driver, a socket line evidences its socket, and a process line evidences its identified process. The saved inventory text itself is not the object being classified.

The process collector in `D1/in/raw/fedora/raw/076-process.sh` prints the PID and a tab before `readlink`, but prints no newline when `readlink` fails. Consequently, several PIDs occur on one physical line. The name in each input row is the first PID. Only a two-field line establishes that PID's executable. The later executable cannot be assigned to an earlier PID. This is missing observational information, not a defect in the definition. No public documentation can recover the missing historical PID identity.

The output is an independent classification, not acceptance of the hypothesis or of another classification.

## Primary documentation

- https://docs.kernel.org/filesystems/proc.html — “Link to the executable of this process”; “List of loaded modules”. These describe `/proc/PID/exe` and `/proc/modules`, the actual inventory sources.
- https://docs.kernel.org/driver-api/driver-model/binding.html — “Driver binding is the process of associating a device with a device driver that can control it.” The document also describes driver initialization and removal.
- https://docs.kernel.org/kbuild/modules.html — “The module foo.ko, consist of bar.o and baz.o”. Modules are compiled kernel objects, not interpreted interface content.
- https://networkmanager.dev/docs/api/latest/nmcli.html — “nmcli is used to create, display, edit, delete, activate, and deactivate network connections”. `083-network.sh` requests connection name, UUID, type and device.
- https://www.freedesktop.org/software/systemd/man/latest/networkctl.html — “Show a list of existing links and their status.” `084-networkd.sh` inventories links; unmanaged is networkd's management status.
- https://docs.flatpak.org/en/latest/basic-concepts.html — “this runtime must be installed on the host system for the application to run.” This establishes runtime dependency, not merely archive storage.
- https://docs.flatpak.org/en/latest/extension.html — “Extension for graphics drivers”; “This is the successor to `org.freedesktop.Platform.ffmpeg-full`”. The extension list identifies GL.default, its extra branch and codecs-extra; library-path mounting makes these runtime code.
- https://docs.flatpak.org/en/latest/flatpak-builder-command-reference.html — “Separate out locale files and translations to an extension runtime.” The application Locale extension supplies translated interface content; the runtime extension also supplies library locale rules, as established by the source chain below.
- https://apps.gnome.org/Calculator/ — “Calculator is an application that solves mathematical equations.”
- https://docs.podman.io/en/latest/markdown/podman-start.1.html — “Start one or more containers using container IDs or names as input.” An exited container can be started again.
- https://docs.podman.io/en/latest/markdown/podman-run.1.html — “Run a process in a new container.” Its filesystem comes from the image; this is executable container backing, not merely an unrelated downloaded archive.

## Sentence text

'''
used=['S2.2-1','S2.2-2','S2.2-3','S2.2-4','S2.2-9','S2.2-10','S2.2-12','S2.2-14','S2.2-15','S3-1','S3-2']
sentences=Path('SENTENCES.md').read_text().splitlines()
intro+='\n'.join(line for line in sentences if any(line.startswith('- **'+s+'**') for s in used))+'\n'
descriptions={
'accounts':'Every row is a parsed local account entry. Apply the explicit account requirement S2.2-15, including service accounts. No password is recorded by this decision.',
'modules':'Every row is a Live kernel module from /proc/modules. Apply S2.2-10 to code loaded into and executed with the kernel rights. Usage counts do not turn executable code into content.',
'drivers':'Every row supplies a device-to-driver symlink. Treat the listed object as the bound driver evidenced by that link. Kernel driver code executes with kernel rights (S2.2-10); its binding supplies device operations (S2.2-1/2). This does not classify the link as a separately installed program.',
'ports':'Every row is a bound receiving UDP socket or listening TCP socket. S2.2-1/2 require its communication capability; S2.2-15 explicitly includes open ports. Loopback scope does not negate that capability.',
'processes':'A two-field line associates one PID with its executable. Such a running program is required by S2.2-9/12, independently of the details of its command-line workload.',
'unidentified_processes':'A line with multiple numeric fields establishes no executable for its first PID. S3-2 requires UNKNOWN; do not substitute the final PID executable. This homogeneous rule is about the identical evidence failure, not guessed process roles.'}
sample_indices={'accounts':[0,1,2,13,14,16,20,40,50,53], 'modules':[0,1,2,19,24,26,30,37,49,50], 'drivers':[0,1,2,3,6,7,42,47,55,60], 'ports':list(range(10)), 'processes':list(range(10)), 'unidentified_processes':list(range(10))}
with notes.open('w') as f:
 f.write(intro)
 for rule,items in rules.items():
  f.write('\n## Rule: '+rule+'\n\n'+descriptions[rule]+'\n\nTen manually inspected rows (input and corresponding raw lines were checked):\n\n')
  for i in sample_indices[rule]:
   r,w,why=items[i]
   f.write('- `'+r['id']+'`: '+w+' Source `D1/in/'+r['evidence']+'`.\n')
 f.write('\n## Individual decisions\n\nThe seven Flatpak entries, five connection profiles, three network links, three sudo grants, container and image were examined individually. Their row-specific decisions and sources are in the TSV. The Wi-Fi exception is explicit. Ethernet and loopback profiles control networking for other programs, so they are not settings confined to NetworkManager. The inactive Ethernet profile still supplies a saved connection that can be activated. The image is the executable root filesystem source for the observed container, whose echo command ran and remains restartable. Calculator.Locale supplies localized interface content. Platform.Locale supplies library locale definitions, affecting operations across applications. GL/codecs and platform runtimes supply executable capabilities.\n')
print('Appended/retained',len(selected),'main rows')

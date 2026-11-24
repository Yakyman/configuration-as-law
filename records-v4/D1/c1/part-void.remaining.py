exec(open('D1/c1/part-void.main.py').read().split('for x in rows:\n')[0])
# Resume records and preserve the first pass rule registry.
rules.update(json.load(open('D1/c1/part-void.main-rules.json')))
SYSFS='https://www.kernel.org/doc/html/latest/filesystems/sysfs.html'
for x in rows:
 if x['id'] in existing or x['kind']=='L2:stored-ownership-unresolved':continue
 k=x['kind'];m=json.loads(x['members']);name=x['name'];record=m.get('record','');ev='raw:D1/in/raw/void/'+x['evidence']
 if k in ['L1:module-name','L1:driver']:
  emit(x,'RUNTIME','S8.2-5','Kernel-exported runtime module or driver registration.','doc:'+SYSFS,'Linux kernel creates this sysfs registration; kernel recording decision UNKNOWN because running-image provenance is not established. The registration has no independent lifetime.','sysfs-runtime')
 elif k=='L1:process':
  exe=record.split('\t')[-1]; label=exe.rsplit('/',1)[-1]
  if exe=='unknown':why='Creating program is unidentified (UNKNOWN); missing executable identity does not alter that the observed process exists only while running.'
  elif exe.endswith(' (deleted)'):why=f'{label} creates the process; its recording decision UNKNOWN because the deleted executable is not verified against current package files.'
  elif any(p['integrity']=='unchanged' for p in pfs[exe]):why=f'{label} (INSTALLED-PACKAGE) creates this process; unchanged executable integrity establishes package coverage. The process is not separately recorded.'
  elif exe=='/tmp/c1-collector/probe':why='Inventory probe (PROGRAM-OWN) creates this process; bootstrap decodes the supplied executable. The process is not separately recorded.'
  else:why=f'{label} creates this process; executable recording decision UNKNOWN because package integrity is unknown. The process is not separately recorded.'
  emit(x,'RUNTIME','S8.2-5,S8.2-7,S8.2-16','Observed running process.',ev,why,'process-runtime')
 elif k=='L1:port':
  emit(x,'RUNTIME','S8.2-5','Open network socket listening for incoming traffic.',ev,'Creating program UNKNOWN: the socket query omits process ownership. Regardless of that identity, an open port is explicitly not a separate object.','individual')
 elif k.startswith('L1:firewall-'):
  if record.startswith('#') or record.startswith('*') or record=='COMMIT':
   emit(x,'RECORD','S8.2-15,S8.2-2','Firewall dump comment or serialization delimiter.',ev,'The query program emitted this dump syntax; it is neither an access rule nor a command typed by a person.','dump-record')
  else:
   creator='Docker daemon' if 'DOCKER' in record or 'docker0' in record else 'netfilter kernel code'
   emit(x,'RUNTIME','S8.2-5,S8.2-13','Live firewall chain, policy, counter, or packet rule.',ev,f'{creator} creates this live firewall object; creator decision UNKNOWN because executable provenance or integrity is unresolved. The dump does not establish a persistent rule file.','firewall-runtime')
 elif k in ['L1:account','L1:group']:
  origins={'_tss':('tpm2-tss','application_package'),'polkitd':('polkit','application_package'),'_flatpak':('flatpak','application_package'),'dbus':('dbus','network_connection'),'docker':('docker','container_run')}
  if name in origins:
   pkg,log=origins[name]
   emit(x,'SETTING-DEFAULT','S8.2-13,S8.2-17','Account or group controlling local identity and access.','raw:D1/in/control/void/actions-logs/actions-logs/'+log+'.log',f'Installation log records creation of this system identity. It is an installation-created default covered by the {pkg} package line.','individual')
  else:
   emit(x,'UNKNOWN','S8.2-11,S8.2-13,S8.2-17','Account or group controlling local identity and access.',ev,'The identity exists, but the evidence does not establish whether this value was chosen separately or created unchanged during package installation.','identity-origin')
 elif k=='L1:runit-service':
  emit(x,'UNKNOWN','S8.1-11,S8.2-13,S8.2-17','Enabled runit service selected by a service-directory link.',ev,'Enabled service is a setting; the link inventory does not establish separate selection versus an unchanged installation-created default, which determines its recording line.','service-origin')
 elif k=='L1:saved-network':
  if name.startswith('cal-secondary:') or name.startswith('cal-test:'):
   emit(x,'SETTING-OWN','S8.2-11,S8.2-13,S8.2-17','Saved network profile defining connection parameters.','raw:D1/in/control/void/actions-logs/actions-logs/network_connection.log','The action log explicitly adds this connection after installation; saved networks are settings requiring their own line.','individual')
  else:
   emit(x,'UNKNOWN','S8.2-5,S8.2-11,S8.2-13,S8.2-17','NetworkManager connection profile reported by the query.',ev,'The query lacks persistence and origin: a saved chosen profile, installation default, or generated transient connection can require different decisions.','individual')
 elif k=='L1:sudo-access':
  if record.strip().startswith(('Matching ','Runas ','User ')):
   emit(x,'RECORD','S8.2-15,S8.2-2','Heading emitted by the sudo permission listing.',ev,'This line labels query output rather than defining a permission; it is a program record.','individual')
  elif 'secure_path=' in record or 'Defaults!' in record or (name=='(ALL' and 'NOPASSWD' not in record and 'root' in x['evidence']):
   emit(x,'INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-16','Packaged sudo default or root permission value.','raw:D1/in/raw/void/package-files.tsv','The corresponding value is present in unchanged packaged sudoers; its package line covers it under the first question.','individual')
  else:
   emit(x,'UNKNOWN','S8.2-7,S8.2-13,S8.2-17','Sudo authorization granted to the local user.',ev,'Effective authorization is established; provenance of its supplemental sudoers rule, including installation-default versus separate selection, is not.','individual')
 elif k=='L1:access-rule':
  emit(x,'UNKNOWN','S8.2-7,S8.2-13,S8.2-17','Supplemental sudoers rule granting command execution privileges.',ev,'Access function is explicit, but package provenance and installation-default versus separately chosen origin are not established.','individual')
 elif k=='L1:saved-network-file':
  emit(x,'SETTING-OWN','S8.2-11,S8.2-13,S8.2-17','Persistent file storing an explicitly added network profile.','raw:D1/in/control/void/actions-logs/actions-logs/network_connection.log','The corresponding connection was explicitly added after installation; its persistent profile stores a chosen network setting.','individual')
 elif k=='L2:code-ownership-unresolved':
  if name.endswith('/times.json'):
   emit(x,'RECORD','S8.2-9,S8.2-15,S8.2-23','Firefox profile creation timestamp record.','doc:https://docs.telemetry.mozilla.org/concepts/profile/profile_creation','Firefox creates times.json to store profile timestamps. Executable permission alone does not make these JSON values executed code.','individual')
  else:
   emit(x,'UNKNOWN','S8.2-6,S8.2-7,S8.2-9,S8.2-16,S8.2-23','Persistent shell or language code executable through an interpreter.',ev,'Code function is established, but package provenance, unchanged receipt, and derivation from another recorded object are not established; the required recording line depends on them.','code-origin')
 elif k=='L2:image':
  if name in ['/boot/initramfs-6.12.118_1.img','/boot/initramfs-6.18.64_1.img']:
   emit(x,'GAP-TWO','S8.2-7,S8.2-9,S8.2-15,S8.2-16','Generated initial filesystem archive containing early-boot programs and data.','raw:D1/in/control/void/actions-logs/actions-logs/package_program.stderr','PROGRAM-DERIVED if archived payload counts as code; RECORD if the archive is generated storage. No sentence defines whether an enclosing archive itself counts as code.','individual')
  else:
   emit(x,'UNKNOWN','S8.2-7,S8.2-9,S8.2-16','Persistent boot image used by the bootloader or kernel.',ev,'The inventory lacks packaged-file integrity and generation provenance for this image; package coverage, generated-copy coverage, and independent origin remain unresolved.','individual')
 elif k=='L2:image-container-store':
  emit(x,'UNKNOWN','S8.2-7,S8.2-9,S8.2-15','Persistent opaque application or container storage directory.',ev,'Contents are unexpanded: installed deployments, executable payloads, configuration, and program records cannot be assigned to members from the retained directory metadata.','individual')
 elif k=='L1:docker-image':
  emit(x,'GAP-NONE','S8.1-4,S8.1-6,S8.2-7,S8.2-9,S8.2-15','BusyBox container image containing a filesystem with executable programs.',ev,'The text does not determine whether this container image is an installed package, executable code itself, or stored filesystem material containing separately executable files.','individual')
 elif k=='L1:docker-container':
  emit(x,'UNKNOWN','S8.2-5,S8.2-9,S8.2-15,S8.2-22','Stopped container retaining filesystem changes and execution metadata.',ev,'The container has exited and retains a writable layer; its unexpanded contents could include executable code or only program records. Contents are not established.','individual')
 else:raise ValueError(x)
f.close()
pathlib.Path('D1/c1/part-void.main-rules.json').write_text(json.dumps(rules,indent=2))
print('Current rows',len(existing))

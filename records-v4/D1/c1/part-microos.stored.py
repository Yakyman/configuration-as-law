import csv,json,pathlib,collections
csv.field_size_limit(100000000)
base=pathlib.Path('D1/in/raw/microos')
rows=[r for r in csv.DictReader(open('D1/in/part-microos.tsv'),delimiter='\t') if r['kind']=='L2:stored-outside-packages']
files=list(csv.DictReader(open(base/'package-files.tsv'),delimiter='\t'))
package_paths={r['path']:r for r in files}
fs={r['path']:r for r in map(json.loads,open(base/'raw/0004-filesystem.out')) if 'path' in r}
member={r['id']:list(csv.DictReader(open(base/json.loads(r['members'])['file']),delimiter='\t')) for r in rows}
for r in rows:
 assert len(member[r['id']])==json.loads(r['members'])['count']
 assert json.loads(r['members'])['complete']
out=pathlib.Path('D1/c1/part-microos.stored.tsv')
header=['id','decision','sentences','what_it_does','basis','reason']
seen={r['id'] for r in csv.DictReader(open(out),delimiter='\t')} if out.exists() else set()
f=open(out,'a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
if not seen:w.writerow(header);f.flush()
def write(r,d,s,what,reason):
 if r['id'] in seen:return
 assert len(what.split())<=15 and len(reason.split())<=30,(what,reason)
 w.writerow([r['id'],d,s,what,'raw:D1/in/raw/microos/'+json.loads(r['members'])['file'],reason]);f.flush();seen.add(r['id'])
for r in rows:
 if r['name'].startswith('/.snapshots/1/snapshot'):
  ms=member[r['id']]
  assert all(m['persistence']=='persistent' and m['path'] not in package_paths for m in ms)
  write(r,'UNKNOWN','S8.2-6,S8.2-7,S8.2-9,S8.2-15,S8.2-16','Stored members of a retained filesystem snapshot','Snapshot members lack package provenance and installation-integrity facts; active-root manifests do not establish whether these copies remain package contents or later generated/modified objects.')
f.close()
f=open(out,'a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
for r in rows:
 if r['id'] in seen:continue
 n=r['name'];ms=member[r['id']]
 if all(m['persistence']=='runtime' for m in ms):
  creator='systemd'
  for prefix,program in [('/run/NetworkManager','NetworkManager'),('/run/udev','systemd-udevd'),('/run/chrony','chronyd'),('/run/blkid','blkid'),('/run/dbus','dbus-broker'),('/run/fsck','systemd-fsck'),('/run/lvm','LVM'),('/run/lock','LVM'),('/run/mount','mount'),('/run/polkit','polkitd'),('/run/rebootmgr','rebootmgrd'),('/run/sysextmgr','sysextmgrd'),('/run/wtmpdb','wtmpdbd'),('/run/initramfs','dracut and systemd'),('/run/log','systemd-journald'),('/run/tmpfiles.d','kmod and systemd-tmpfiles')]:
   if n.startswith(prefix):creator=program
  if n=='/run':creator='systemd, NetworkManager, auditd, agetty, dmeventd, blkid, chronyd, fsck, LVM, polkitd, rebootmgrd, sysextmgrd, wtmpdbd'
  if n.startswith('/tmp'):creator='systemd and systemd-tmpfiles'
  write(r,'RUNTIME','S8.2-5,S8.2-7,S8.2-16','Volatile service state, communication endpoints, or generated runtime configuration',f'Exists only during execution; creators: {creator} (INSTALLED-PACKAGE); unchanged packaged executables cover the creating programs.')
 elif n.startswith('/var/cache/zypp'):
  write(r,'RECORD','S8.2-6,S8.2-15','Repository metadata cache and solver working data','ZYpp records repository metadata and solver caches while running; no member is installed code or a chosen system setting.')
 elif n.startswith('/usr/share/mime'):
  write(r,'RECORD','S8.2-6,S8.2-15,S8.2-23','Generated MIME classification database and type descriptions','update-mime-database generates data consumed as values; these outside-package outputs are program records, not executable code or person-chosen settings.')
f.close()
f=open(out,'a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
# Individually assessed residual groups; member numbers are one-based TSV data rows.
manual={}
def add(ids,d,what,reason,s='S8.2-6,S8.2-15'):
 for i in ids.split():manual['microos-'+i]=(d,s,what,reason)
add('4e547bbfff8b6a90a75081b4','MIXED','Root directory, snapshot storage, and partition metadata','Member 2: RECORD, snapshot-manager storage; members 1,3: UNKNOWN, creation provenance and configuration role not retained.','S8.2-7,S8.2-11,S8.2-15')
add('96429a72151028bd6318f4fe','MIXED','Snapshot storage directories and boot menu code','Members 1-2: RECORD, snapshot-manager storage; member 3: UNKNOWN, executable boot configuration generation source not retained.','S8.2-9,S8.2-15,S8.2-16')
add('4fd0021f912a438523a614a7 42d6faabe4f568e398d746ff','MIXED','Snapshot metadata, stored tree directory, and boot menu code','Members 2-3: RECORD, snapshot-manager metadata/storage; member 1: UNKNOWN, executable boot configuration generation source not retained.','S8.2-9,S8.2-15,S8.2-16')
add('1e6140153fd85054d1613c91','UNKNOWN','Boot filesystem directories, kernel authentication link, and boot identifier','Creation provenance and installation or generation sources of these outside-package boot objects are not retained.','S8.2-7,S8.2-11,S8.2-15,S8.2-16')
add('f79f605cdb912792656b45a8 069f1aacebd9aea16c5dd80f','UNKNOWN','EFI boot directory','Inventory establishes persistent directory existence, but not whether a program created it or a person brought it.')
add('0df5e895df804ac9c7d66b20','UNKNOWN','EFI bootloaders, machine owner key manager, and boot configuration','Executable objects are outside package manifests; their actual installation or generation sources are absent, preventing own-line versus derived-line decisions.','S8.2-9,S8.2-16,S8.2-23')
add('d799bd9be28a74ddd1b4fdc1','UNKNOWN','GRUB support directories and saved boot environment','Creation provenance and boot-environment values are absent; records, chosen settings, and generated objects cannot be distinguished.','S8.2-11,S8.2-15,S8.2-17')
add('47efcf878b603ac8f7d69824 40a34b9ae42fdfe223450b6a','UNKNOWN','GRUB font or translated message data','Outside-package data provenance is absent: generated/copied by a program versus brought by a person determines RECORD versus MATERIAL.')
add('bba0a165a3107d2172772e90','UNKNOWN','GRUB modules, images, scripts, and generated lookup lists','Actual generation sources and installation history are absent; code line coverage and data provenance remain unresolved for these boot support members.','S8.2-9,S8.2-15,S8.2-16')
add('1a6267884f7ab2f53a5d9b6a','UNKNOWN','GRUB theme images, fonts, text, and activation script','Source lineage of activation code and provenance of noncode theme data are absent; own-line, derived-line, record, and material alternatives depend on facts.','S8.2-9,S8.2-15,S8.2-16')
add('9b1fbc813c5876fd618e71f2 7e85ee24d5a79ba81acd55bf 10f3f32ef128ab5c54608484 13a878fb75c30087a0c945f2 f259b60aca1fd13da7a98094 fb60b6412ee79d20c1e490c3 20f675737a015be831213148 c3584b79f29f4bed45c410e1 cbf1329980f813598d30e154 1c25959e8ab1f682fdbeb3a3 969555e54dece5af5ca71a6b 3be1be4e03465b7c00128c76 41501ec114e30e06c76bee61','UNKNOWN','Persistent outside-package storage directories','Directory creation provenance is absent: program-created working storage gives RECORD; person-created or brought storage gives MATERIAL.')
add('7ff23ea65ce9ac475d341726','UNKNOWN','Account shell startup files and application storage directories','Startup-file generation sources and directory creators are not retained; own/derived program lines and record/material distinctions depend on those facts.','S8.2-9,S8.2-15,S8.2-16')
add('a8975833887ea3b6547e9d8e','SETTING-OWN','Authorized public keys granting login to this computer','Authorized keys specify permitted login credentials; outside-package authorization requires its own setting line.','S8.2-11,S8.2-13,S8.2-17')
add('26589cb9ed52782be3a8594c','RECORD','RPM package database and persistent database lock','RPM records installed-package metadata and database locking state while running; the database is not itself a package or executable code.')
add('345288f4431645eff7dac2dd','RECORD','System update completion timestamp','The update marker records completed system maintenance; it is persistent working state, not a chosen configuration value.')
add('073f8fb7799a7076b0d7700b','RECORD','Dynamic linker auxiliary cache','ldconfig records auxiliary library cache data while running; this cache is outside packages and contains values, not executed code.')
add('aac239c4bba88d008a47f08d','MIXED','NetworkManager saved state, leases, identity seed, and connection histories','Members 1-2: UNKNOWN, chosen/default configuration origin absent; members 3-9: RECORD, DHCP leases, generated identity seed, and observed histories.','S8.2-11,S8.2-15,S8.2-17')
add('7b851b26fa99c2a7ca64763f dcce813055fa256ed012c87a 3aecc583b26d47be2c87f514','UNKNOWN','Generated certificate trust stores and certificate lookup links','Inventory omits whether trust contents reflect chosen access policy or installation defaults; generated storage alone cannot settle setting classification and package coverage.','S8.2-11,S8.2-13,S8.2-15,S8.2-17')
add('0e07702152057a02faa47630','RECORD','Directory reconstruction completion cookie','The directory reconstruction program records its completion cookie as persistent working state.')
add('a4cc147018605138aecdf2f3','RECORD','Last login database','Login accounting records past account activity; these timestamps are program records, not account configuration.')
add('68bbeee8c7f6b29e0404c21b','RECORD','Health check and transactional update state','Both files record service operational state; no executable code or person-chosen setting is represented.')
add('5a0c95d64858e88286cfeced','MIXED','System service state directories and persisted random seed','Members 1,6,7: RECORD, generated catalog/seed/timer storage; members 2-5: UNKNOWN, directory creation provenance absent.','S8.2-11,S8.2-15')
add('a192180c3d10540a68eae9cb','RECORD','Generated journal message catalog database','The service manager generates a lookup database for journal message descriptions; it records computed values, not code.')
add('c0ca1933cbf00ee240ad0137','RECORD','Timer last-trigger timestamps','All nine timestamps record when timers fired; they do not set whether the timers are enabled.')
add('508cac328a497cc5b691ad00','RECORD','Login session accounting database','The login accounting program records session events as persistent history.')
add('157107a19ef8cc91a60fa35f','MIXED','Package manager identity, dependency marks, and distribution history','Members 1,3: RECORD, generated identity/history; member 2: UNKNOWN, dependency-mark values and chosen-versus-automatic origin not retained.','S8.2-11,S8.2-15,S8.2-17')
add('2eea0ada45cc7783be9a67ac','MIXED','Service logs and supporting log storage directories','Members 1,3,5: RECORD, service log storage/output; members 2,4: UNKNOWN, link and private-directory creation provenance absent.')
add('1fcea30613a61e6b4310584d','RECORD','System configuration difference log','The configuration utility recorded observed differences in its log; logging configuration changes does not make the log a setting.')
add('5f125bab705e750a5bbebbae','RECORD','Journal storage directory for the system identity','The journal service creates its identity-specific directory to store event records.')
add('38cd890dce90cad0e1c07d40','RECORD','System and account journal event files','Both persistent files record runtime events; logs need not be recorded in the declaration.')
add('d63ebc44732c3673cbfbfd20','RECORD','Package transaction history','Package manager history records completed transactions, not the desired installed state.')
add('ad0c1957e5808aa74374f433','RECORD','Image-builder, service-private, and package-manager temporary working directories','All ten directories hold program working state; their filesystem is persistent, so temporary names alone do not establish runtime-only existence.')
add('8d255e1c755e2be296f8321f db54b0144a52820b73833ce3 4b389fb0d10545d8a98d8ecd 7cb966fe23288c6e57070aea 0892f7bf4b9a6582a88fb9cd 373fb22e2c267422873a2d24 e9cffe3712ba771d52503194 554e9b5ed8539dfd6511436e','RECORD','Private temporary working directory for a service','The service manager creates private temporary storage as program working state; persistent backing does not establish runtime-only lifetime.')
for r in rows:
 if r['id'] not in seen:
  d,s,what,reason=manual[r['id']];write(r,d,s,what,reason)
f.close()

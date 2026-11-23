import csv
from pathlib import Path
rows=[r for r in csv.DictReader(open('A1/in/part-5.tsv'),delimiter='\t') if r['machine'] in ('alpine','arch') and r['kind'] in ('stored','stored-directory-skeleton')]
D={}
def put(i,d,s,w,b,r):D[i]=(d,s,w,b,r)
def doc(x):return 'doc:'+x
sys='https://wiki.archlinux.org/title/Syslinux'
apk='https://github.com/alpinelinux/apk-tools/blob/master/doc/apk.8.scd'
fd='https://www.freedesktop.org/software/systemd/man/latest/'
bash='https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files'
openrc='https://github.com/OpenRC/openrc/blob/master/sh/openrc-run.sh.in'
# These entries were individually assessed; repeated strings merely serialize those decisions.
put(0,'UNKNOWN','S3-2','Aliases the boot directory; consuming boot paths are unavailable.','evidence','The symlink target is known, but no evidence establishes whether booting depends on this alias.')
put(1,'MUST','S2.2-1,S2.2-2','Selects boot entries and kernel arguments.',doc(sys),'Removing boot selection settings changes how the operating system starts; their effects extend beyond the bootloader.')
put(2,'MUST','S2.2-1,S2.2-9','Provides executable early userspace for boot.',doc('https://github.com/alpinelinux/mkinitfs'),'Early boot programs execute on the computer and support starting the installed system.')
put(3,'MUST','S2.2-9,S2.2-10','Executes the Syslinux core bootloader module.',doc(sys),'Bootloader code executes directly and is required to load boot configuration.')
put(4,'MUST','S2.2-9','Loads the Syslinux bootloader core.',doc(sys),'This executable bootloader starts the next stage; removal prevents that boot path.')
put(5,'MUST','S2.2-10','Provides native routines used by Syslinux modules.',doc(sys),'The bootloader executes these library routines with its own rights.')
put(6,'MUST','S2.2-10','Provides native utility routines for Syslinux menus.',doc(sys),'These routines execute with bootloader rights and enable its menu modules.')
put(7,'UNKNOWN','S3-2','Bootloader module whose specific operation was not established.','evidence','Available inventory names the module but provides no contents; the primary documentation search did not establish its function.')
put(8,'MUST','S2.2-10','Executes a text boot selection menu.',doc(sys),'Native bootloader code executes with bootloader rights, not within a restricted interface.')
put(9,'MUST','S2.2-10','Executes the graphical Syslinux boot selection menu.',doc('https://kernel.googlesource.com/pub/scm/boot/syslinux/syslinux/+/master/doc/menu.txt'),'This native graphical menu module executes with bootloader rights and controls boot selection.')
put(10,'MUST','S2.2-1,S2.2-2','Selects package architecture, repositories, and required installed packages.',doc(apk),'All three named files govern which software can be installed or retained, affecting the computer beyond apk.')
put(11,'MUST','S2.2-10,S2.2-13','Executes shell assignments configuring console login services.',doc(openrc),'Both service configuration files are sourced as shell code with the service runner rights.')
put(12,'MUST','S2.2-15','Controls permission to run commands as another user.',doc('https://man.archlinux.org/man/doas.conf.5.en'),'The named privilege policy governs superuser access, explicitly requiring recording.')
put(13,'NOT','S2.2-6','Preserves the previous group database.','evidence','A backup records past group information rather than defining current accounts.')
put(14,'MUST','S2.2-10','Executes the console login service startup script.',doc(openrc),'The service script is sourced and executed with the service runner rights.')
put(15,'MUST','S2.2-1,S2.2-2','Selects kernel drivers included in generated boot images.',doc('https://github.com/alpinelinux/mkinitfs/blob/master/mkinitfs.in'),'Both module lists govern generated boot capabilities, which take effect outside the image generator.')
put(16,'NOT','S2.2-6','Preserves the previous account database.',doc('https://man7.org/linux/man-pages/man5/passwd.5%40%40shadow-utils.html'),'A backup is a record of past accounts, not their active definition.')
put(17,'MUST','S2.2-10,S2.2-13','Executes shell startup commands setting locale.','evidence','The inventory identifies a shell startup script; such code is explicitly required even when it holds settings.')
put(18,'MUST','S2.2-1,S2.2-2','Supplies DNS resolver settings to applications.',doc('https://man.archlinux.org/man/dhcpcd.8.en'),'Name resolution settings govern network access across programs.')
put(20,'NOT','S2.2-6','Preserves previous account authentication information.',doc('https://man7.org/linux/man-pages/man5/shadow.5.html'),'The backup records previous authentication data rather than active login rules.')
put(22,'UNKNOWN','S3-2','Stores a package-delivered replacement configuration.','evidence','The inventory does not establish whether any program reads this replacement; its exact activation and contents are unavailable.')
put(23,'MUST','S2.2-15','Defines user privilege escalation policy.',doc('https://man.archlinux.org/man/sudoers.5.en'),'The single identified sudoers policy controls superuser privileges, an explicit requirement.')
put(25,'HOLE','S2.2-1,S2.2-7,S2.2-13','Configures Readline editing and key bindings in client programs.',doc('https://ftp.gnu.org/old-gnu/Manuals/bash-2.05a/html_mono/bashref.html'),'Settings are applied separately inside each Readline client, yet one shared file affects multiple programs; the text does not define which scope counts.')
put(27,'MIXED','S2.2-1,S2.2-2,S2.2-10,S3-2','Stores package metadata, scripts, trigger rules, and a transaction lock.',doc(apk),'scripts.tar.gz, installed, triggers: MUST for execution or package management; lock: UNKNOWN because current locking state and removal consequences are not established.')
put(29,'NOT','S2.2-5','Caches two downloadable repository indexes.',doc(apk),'Both listed members are repository index caches; they replace repeated downloads without defining installed software.')
put(31,'UNKNOWN','S3-2','Stores DHCP identity, a lease message, and a secret.',doc('https://man.archlinux.org/man/dhcpcd.8.en'),'Documentation identifies all files, but exact secret use and last-lease activation on this installation remain unestablished.')
put(41,'MUST','S2.2-1,S2.2-9','Provides executable early userspace for kernel boot.',doc('https://man.archlinux.org/man/mkinitcpio.8.en'),'Early userspace executes programs to prepare the root filesystem and start the system.')
put(42,'MUST','S2.2-1,S2.2-9','Provides the Linux operating system kernel.','evidence','Removing the executable kernel removes that operating system boot capability.')
put(43,'UNKNOWN','S3-2','Coordinates updates to the shadow password database.',doc('https://www.man7.org/linux/man-pages/man3/getspnam.3.html'),'The lock purpose is documented, but inventory gives no active locking state or dependence on this stored inode.')
put(44,'HOLE','S2.2-1,S2.2-6','Records completed updates and controls conditional update services.',doc(fd+'systemd-update-done.service.html'),'The stamp is a record of past updates exempted by S2.2-6, but also gates future services under S2.2-1; precedence is unspecified.')
put(46,'NOT','S2.2-6','Preserves the previous group database.','evidence','A backup records prior group information rather than configuring current membership.')
put(47,'NOT','S2.2-6','Preserves previous protected group authentication data.','evidence','This backup preserves historical group authentication information, which is exempt as a record of the past.')
put(48,'MUST','S2.2-1','Sets the system identity used across programs.',doc(fd+'hostname.html'),'The configured system name affects the operating system and applications, not only one program.')
put(49,'UNKNOWN','S3-2','Caches paths used to locate shared libraries.',doc('https://man7.org/linux/man-pages/man8/ld.so.8.html'),'Removal can lose nondefault library paths or merely slow loading; inventory lacks cache contents and dependent binaries.')
put(50,'MUST','S2.2-1','Sets locale defaults inherited by services and users.',doc(fd+'locale.conf.html'),'System-wide locale settings govern behavior across programs and do not meet the one-program exemption.')
put(51,'NOT','S2.2-2','Selects UTC as the system timezone.',doc(fd+'localtime.html'),'The observed target is UTC and documentation specifies UTC when absent; removing this link preserves timezone behavior.')
put(52,'MUST','S2.2-1,S2.2-2','Provides machine identity and determines first-boot initialization.',doc(fd+'machine-id.html'),'Its absence activates first-boot handling and changes system identity; its role extends beyond one program.')
put(53,'MUST','S2.2-1,S2.2-2','Specifies generated Linux boot images.',doc('https://man.archlinux.org/man/mkinitcpio.8.en'),'The preset determines generation of executable boot images, affecting boot capabilities beyond the generator.')
put(54,'UNKNOWN','S3-2','Exposes operating-system identification through a compatibility symlink.',doc(fd+'os-release.html'),'Conforming readers have a fallback, but compatibility-only readers may depend on this link; the inventory identifies no readers.')
put(56,'NOT','S2.2-6','Preserves the previous account database.',doc('https://man7.org/linux/man-pages/man5/passwd.5%40%40shadow-utils.html'),'This backup is a record of prior accounts rather than their current definition.')
put(57,'NOT','S2.2-6','Preserves previous password and account aging information.',doc('https://man7.org/linux/man-pages/man5/shadow.5.html'),'Historical authentication information in a backup is exempt as a record of the past.')
put(60,'NOT','S2.2-6','Preserves prior subordinate group identifier allocations.','evidence','The backup records past allocations, not current delegation.')
put(61,'NOT','S2.2-6','Preserves prior subordinate user identifier allocations.',doc('https://man.archlinux.org/man/subuid.5.en'),'The documented backup is a record of previous allocations.')
put(62,'MUST','S2.2-15','Defines privilege escalation policies for two users.',doc('https://man.archlinux.org/man/sudoers.5.en'),'Both listed sudoers files govern superuser rights, which are explicitly required.')
put(64,'MUST','S2.2-1','Configures console keyboard mapping and display font.',doc(fd+'vconsole.conf.html'),'The settings apply to the system console and affect input or presentation across console programs.')
put(65,'MUST','S2.2-10','Executes commands when a login shell exits.',doc(bash),'Bash executes this file with shell rights; it is not merely read as setting values.')
put(66,'MUST','S2.2-10','Executes commands when a login shell starts.',doc(bash),'Shell startup files are an explicit example of code requiring recording.')
put(67,'MUST','S2.2-10','Executes interactive shell startup commands.',doc(bash),'Bash executes the file with its own rights, matching the explicit shell-startup requirement.')
put(68,'MUST','S2.2-10','Executes commands when a login shell exits.',doc(bash),'The logout file is executable shell code running with shell rights.')
put(69,'MUST','S2.2-10','Executes login-shell startup commands.',doc(bash),'This startup file is code executed with the shell rights, explicitly requiring recording.')
put(70,'MUST','S2.2-10','Executes interactive-shell initialization commands.',doc(bash),'The shell executes this startup file; the text explicitly requires recording it.')
put(71,'HOLE','S2.2-1,S2.2-7,S2.2-13','Configures Readline editing and bindings across client programs.',doc('https://ftp.gnu.org/old-gnu/Manuals/bash-2.05a/html_mono/bashref.html'),'Each client applies settings internally, but multiple programs share the file; the text does not define whether file scope or individual application scope prevails.')
put(72,'NOT','S2.2-7,S2.2-13','Sets nano editing preferences and key bindings.',doc('https://www.nano-editor.org/dist/latest/nanorc.5.html'),'Nano reads the file as configuration values governing its own editing interface, meeting the one-program exemption.')
put(74,'HOLE','S2.2-1,S2.2-6','Records update completion and gates later update services.',doc(fd+'systemd-update-done.service.html'),'The timestamp records a past update but controls future service execution; the text does not say whether historical-record exemption or behavior requirement prevails.')
put(77,'MUST','S2.2-1','Provides the machine identifier at the D-Bus compatibility path.',doc(fd+'machine-id.html'),'The identity path supports system-wide interprocess communication, extending beyond an internal program setting.')
# Homogeneous rule L: explicit standalone historical log files are exempt by S2.2-6.
logs=[32,33,34,35,36,37,38,81,83,84,85]
for i in logs:put(i,'NOT','S2.2-6','Records past system events or login activity.','evidence','The row identifies a historical log file, explicitly exempt as a record of the past.')
# Homogeneous rule U: incomplete directory samples cannot establish all member functions.
unknown=[19,21,24,26,28,30,40,45,55,58,59,63,73,75,76,78,79,80,82]
for i in unknown:put(i,'UNKNOWN','S3-2','Contains a partially enumerated group of stored objects.','evidence','Only sample members are identified; absent raw inventory and unnamed members prevent establishing the behavior of the complete group.')
put(39,'UNKNOWN','S3-2','Retains unidentified directory structures.','evidence','The inventory gives only a directory-group count; paths, permissions, and consuming programs are unavailable.')
put(86,'UNKNOWN','S3-2','Retains unidentified directory structures.','evidence','The directory groups are not named; their effects on programs or access cannot be established.')
assert set(D)==set(range(len(rows))),set(range(len(rows)))-set(D)
p=Path('A1/c1/part-5.2.tsv'); existing=set()
if p.exists():existing={r['id'] for r in csv.DictReader(p.open(),delimiter='\t')}
with p.open('a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if p.stat().st_size==0:w.writerow(['id','decision','sentences','what_it_does','basis','reason'])
 for i,r in enumerate(rows):
  if r['id'] not in existing:
   assert len(D[i][2].split())<=15 and len(D[i][4].split())<=30,(i,D[i])
   w.writerow([r['id'],*D[i]]);f.flush()
print('appended',len(rows)-len(existing))

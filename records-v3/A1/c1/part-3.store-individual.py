import csv,json,re
rows=[r for r in csv.DictReader(open('A1/in/part-3.tsv'),delimiter='\t') if r['kind']=='system-closure-store-object'];p='A1/c1/part-3.store.tsv';done={r['id'] for r in csv.DictReader(open(p),delimiter='\t')};dec={};details={}
manual='https://nixos.org/manual/nixos/stable/'
config=json.load(open('A1/c1/part-3.store-configdocs.json'))
def put(i,d,s,what,basis,why):
 assert i not in dec;dec[i]=[rows[i]['id'],d,s,what,basis,why]
def code(i,what,basis,why='Executable code supplies this operation and runs with the executing program’s rights.'):
 put(i,'MUST','S2.2-9,S2.2-10',what,basis,why)
def must(i,what,basis,why,s='S2.2-1,S2.2-2'):
 put(i,'MUST',s,what,basis,why)
def not_(i,what,basis,why,s='S2.2-4'):
 put(i,'NOT',s,what,basis,why)
# Explicit individual decisions, indexed against the fixed input order.
for i,what in [(45,'Runs filesystem mount setup during activation.'),(282,'Updates accounts and groups during activation.'),(424,'Provides shell functions sourced during activation.'),(496,'Installs generated system configuration during activation.')]:
 code(i,what,'raw:A1/in/raw/nixos/activation-script.txt')
must(462,'Describes accounts and groups consumed by activation.','raw:A1/in/raw/nixos/activation-script.txt','Activation consumes this account description; accounts and account rights must be recorded.','S2.2-15')
must(217,'Supplies the installed static system configuration tree.','raw:A1/in/raw/nixos/activation-script.txt','Activation installs this tree as system configuration; removing it prevents the configured system setup.')
must(222,'Supplies device firmware through the kernel firmware search path.','raw:A1/in/raw/nixos/activation-script.txt','Activation explicitly selects these firmware files for device loading.','S2.2-1,S2.2-16')
must(411,'Provides the current system activation and boot configuration.','raw:A1/in/raw/nixos/activation-script.txt','This system directory is selected by the active system profile and supplies activation behavior.')
for i in [11,381]:code(i,'Launches a browser to display system help.','doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/misc/documentation.nix')
code(76,'Migrates the DHCP client database before service startup.','doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/services/networking/dhcpcd.nix')
for i,what in [(39,'Enters an installed system for administration.'),(93,'Reports the operating system version.'),(131,'Builds virtual machines from system configurations.'),(144,'Inspects system configuration options.'),(422,'Generates initial system configuration files.'),(587,'Installs a system from its configuration.')]:code(i,what,'doc:'+manual)
for i,what in [(65,'Runs shell initialization commands.'),(162,'Runs shell logout commands.'),(174,'Runs login shell initialization commands.')]:code(i,what,'doc:https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html')
not_(100,'Sets editor options and syntax presentation.','doc:'+config['nanorc']['url'],'These settings apply only inside the editor.','S2.2-7,S2.2-13')
for i,what in [(121,'Contains the system manual in HTML.'),(265,'Contains package manager documentation.'),(333,'Contains the system configuration reference manual.')]:not_(i,what,'doc:'+manual,'Removing this manual removes readable content without removing the documented programs.')
not_(478,'Displays informational text before a login prompt.','doc:'+config['issue']['url'],'Removing the message removes only displayed content; login functionality remains.')
not_(576,'Provides a bootloader wallpaper image.','evidence','Removing an image removes only that displayed content.')
not_(413,'Provides sound theme audio content.','doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/so/sound-theme-freedesktop/package.nix','Removing theme sounds removes their content, not the ability to play sound.')
not_(601,'Provides a fallback icon theme.','doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/hi/hicolor-icon-theme/package.nix','Theme assets supply presentation content; removal makes only those assets unavailable.')
# Exact generated inputs whose source definition establishes their control role.
must(205,'Controls whether a system configuration switch is permitted.','doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/system/activation/switchable-system.nix','Switch inhibitors are consumed before activation and control whether the system can switch.')
must(230,'Sets environment variables supplied to system generators.','doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/system/boot/systemd.nix','The generated environment influences executable generators and their system unit output.')
must(387,'Supplies bootloader installation parameters.','doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/system/boot/loader/grub/grub.nix','Bootloader generation consumes these settings; they determine boot entries and installation behavior.')
not_(610,'Supplies an empty comparison value for switch-inhibitor checks.','doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/system/activation/switchable-system.nix','This is a constant empty JSON object used as program input.',s='S2.2-4')
# Public database and association roles are known; recording boundary remains textual where applicable.
for i,key,what in [(113,'shared-mime-info','Provides shared MIME type recognition data.'),(384,'tzdata','Provides time-zone conversion rules.'),(396,'publicsuffix-list','Provides public domain suffix boundaries.'),(547,'iana-etc','Maps network protocol and service names to numbers.')]:
 url=json.load(open('A1/c1/part-3.store-research.json'))[key]['url']
 put(i,'HOLE','S2.2-1,S2.2-2,S2.2-4',what,'doc:'+url,'Runtime database values determine behavior, yet database contents are exempt; text does not define the boundary between functional data and content.')
for i in [19,404]:must(i,'Supplies certificate authority trust anchors.','doc:https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ca/cacert/package.nix','Removing trust anchors prevents certificate authentication; they are neither account passwords nor merely displayed content.')
must(603,'Supplies a public key authorized for account login.','evidence','Login keys are explicitly required to be recorded.','S2.2-15')
# For all other individually inspected objects, the inventory lacks operative contents.
unknown_indices=[0,2,7,13,14,16,18,23,38,46,49,60,61,63,64,77,80,86,87,112,114,116,125,128,134,135,139,149,150,153,155,158,164,180,195,204,207,208,214,215,216,241,244,248,262,263,275,281,283,293,304,306,316,325,329,335,338,341,343,354,356,369,371,382,386,405,412,423,429,436,440,441,455,458,476,491,494,498,501,506,507,510,511,512,516,518,519,521,523,527,530,536,539,540,543,544,548,549,550,551,562,577,582,588,590,591,594,606,611]
for i in unknown_indices:
 if rows[i]['id'] in done:continue
 put(i,'UNKNOWN','S3-2','Specific operative contents or execution role are not established.','evidence','Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role.')
with open(p,'a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 for i,row in sorted(dec.items()):
  if row[0] not in done:w.writerow(row);f.flush()
print('INDIVIDUAL',len(dec))
current={r['id'] for r in csv.DictReader(open(p),delimiter='\t')}
for i,r in enumerate(rows):
 if r['id'] not in current:print('MISSING',i,r['id'],r['name'].split('-',1)[1])

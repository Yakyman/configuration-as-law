import csv,json,pathlib
p=pathlib.Path('A1/c1/part-2.stored.tsv'); rr=list(csv.DictReader(p.open(),delimiter='\t')); source=[r for r in csv.DictReader(open('A1/in/part-2.tsv'),delimiter='\t') if r['kind'] in ('package-owned-paths','stored','stored-directory-skeleton')]; byid={r['id']:r for r in rr}; rule=json.load(open('A1/c1/part-2.stored.rule-ids.json'))
for r in rr:
 if r['id'] in rule['directories']:
  r.update(decision='UNKNOWN',sentences='S3-1,S3-2',what_it_does='Provides a directory; functional dependency and reconstruction behavior are unobserved.',reason='Directory metadata alone does not establish what functionality depends on its existence, beyond pathname availability.')
 else:
  why=r['reason'];why=why.replace('Directories: HOLE between namespace capability and content organization.','Directories: UNKNOWN without functional dependency evidence.').replace('Directory: HOLE between namespace capability and content organization.','Directory: UNKNOWN without functional dependency evidence.').replace('Directories: HOLE.','Directories: UNKNOWN.').replace('Directory: HOLE.','Directory: UNKNOWN.').replace('Directory: HOLE;','Directory: UNKNOWN;').replace('Directories: HOLE;','Directories: UNKNOWN;')
  if why!=r['reason']:
   r['reason']=why
   if 'S3-2' not in r['sentences']:r['sentences']+=',S3-2'
def fix(i,d,s,w,why,b=None):
 r=byid[source[i]['id']];r.update(decision=d,sentences=s,what_it_does=w,reason=why)
 if b:r['basis']=b
fix(9,'MIXED','S2.2-1,S2.2-4,S3-2','Supplies AppArmor access policy, abstractions, tunables, and directories.','Policy files: MUST because they constrain access. local/README: NOT as documentation. Directory dependencies: UNKNOWN.')
fix(30,'UNKNOWN','S2.2-10,S2.2-11,S3-2','Provides groff macro customization and directory.','Macro contents and execution safety mode are unobserved; cannot establish interface confinement or full-rights code execution.')
fix(36,'MIXED','S2.2-1,S2.2-4,S3-2','Supplies routing tool lookup tables, READMEs, and directories.','READMEs: NOT. Lookup tables: MUST for shared network name interpretation. Directory dependencies: UNKNOWN.')
fix(45,'UNKNOWN','S2.2-7,S2.2-10,S3-2','Supplies rotation configuration and directory.','Configuration can embed executed scripts; contents and directory dependencies were not collected.')
fix(77,'UNKNOWN','S2.2-7,S2.2-10,S2.2-13,S3-2','Provides screen session startup commands and settings.','Screen supports both internal settings and external command execution; inventory omits actual configuration needed to distinguish them.')
fix(86,'UNKNOWN','S2.2-7,S2.2-15,S3-2','Configures sudo log server transport and behavior.','Possible options include listening ports and internal preferences; actual values are absent, so their scope cannot be established.')
fix(96,'UNKNOWN','S2.2-1,S2.2-7,S3-2','Provides device manager settings and configuration directories.','Collected evidence omits settings values and directory dependencies; cannot establish their operative function.')
fix(101,'MUST','S2.2-1,S2.2-13','Defines shared extended-attribute preservation policy for file copying.','Library policy governs attribute preservation across multiple copying programs; the single-program exemption does not apply.')
fix(154,'MUST','S2.2-1,S2.2-10,S2.2-13','Sets GRUB generation defaults and system locale.','GRUB fragments are sourced shell code; locale values govern multiple programs. Both require recording.')
fix(185,'MIXED','S2.2-1,S2.2-13,S3-2','Controls Python module byte-compilation and provides its directory.','debian_config: MUST as shared package byte-compilation policy. Directory dependency: UNKNOWN.','doc:https://www.debian.org/doc/packaging-manuals/python-policy/')
fix(225,'MIXED','S2.2-1,S2.2-4,S2.2-6,S3-2','Stores debconf answers, templates, previous databases, and temporary directory.','config.dat/passwords.dat: MUST for package configuration. templates.dat: NOT as question content. Old databases: NOT as history. Directory dependency: UNKNOWN.')
fix(231,'MIXED','S2.2-1,S2.2-6,S2.2-10,S3-2','Stores package database, maintainer scripts, metadata, and directories.','Maintainer scripts, active package/trigger/alternative metadata: MUST. Backups: NOT. Locks and cmethopt: UNKNOWN without contents or use. Directory dependency: UNKNOWN.')
fix(232,'MUST','S2.2-1,S2.2-2','Enables automatic manual database regeneration during package installation.','Removing the marker makes the installation script skip rebuilding the manual database.','doc:https://sources.debian.org/src/man-db/2.11.2-2/debian/postinst/')
fix(233,'MUST','S2.2-1,S2.2-13,S2.2-15','Stores PAM policy generation state and prior selections.','Generation state controls authentication configuration across login clients; removal changes preservation of selected access policy.')
fix(238,'MIXED','S2.2-1,S2.2-6,S3-2','Stores configuration merge baselines, registration databases, and previous versions.','Numbered backups: NOT. Current baselines/hashfile/registry: MUST because they control merge decisions. Directory dependency: UNKNOWN.')
fix(239,'MUST','S2.2-1,S2.2-13','Stores registration databases for XML catalog generation.','Registrations govern generated entity resolution; removal changes document-processing behavior rather than merely making database content unavailable.')
fix(247,'MIXED','S2.2-6,S3-2','Stores system and user event journals in directories.','Journal files: NOT as logs. Directory dependencies: UNKNOWN without evidence of reconstruction behavior.')
fix(251,'UNKNOWN','S2.2-1,S2.2-4,S3-2','Aliases the mail spool directory.','Inventory does not establish a mail delivery consumer or whether this compatibility alias affects anything beyond access to messages.')
fix(50,'NOT','S2.2-7,S2.2-13','Sets default filesystem creation parameters inside mke2fs.','The formatter reads values for its own operation; resulting filesystems do not keep these defaults in force in other programs.','doc:https://manpages.debian.org/bookworm/e2fsprogs/mke2fs.conf.5.en.html')
fix(149,'MIXED','S2.2-1,S2.2-7,S3-2','Supplies repository locations, upgrade policy, and listchanges preferences.','Repository and shared APT policy: MUST. listchanges.conf: NOT as program preferences. mirrors directory dependency: UNKNOWN.')
fix(161,'MUST','S2.2-1,S2.2-2,S2.2-15','Stores group passwords, administrators, and membership.','Whole-file removal loses group administration and membership policy; exempt password fields do not exempt the functional policy object.')
fix(198,'MUST','S2.2-1,S2.2-2,S2.2-15','Stores password hashes, account lock markers, and expiry policy.','Whole-file removal loses account lock and expiry policy; exempt password fields do not exempt the functional access-policy object.')
fix(217,'NOT','S2.2-6','Records the first successful privileged invocation by an account.','The documented function records past sudo use; no collected evidence establishes an active consumer suppressing future advice.','doc:https://manpages.debian.org/bookworm/sudo/sudoers.5.en.html')
fix(46,'UNKNOWN','S2.2-1,S2.2-13,S3-2','Provides local file recognition rules to shared libmagic consumers.','Shared-library scope is documented, but inventory lacks contents establishing whether this file contains effective rules or only comments.','doc:https://deb.debian.org/debian/pool/main/f/file/file_5.44-3.debian.tar.xz')
fix(47,'UNKNOWN','S2.2-1,S2.2-13,S3-2','Provides legacy local MIME recognition rules to shared libmagic consumers.','Shared-library MIME compatibility loading is documented, but contents establishing effective rules rather than comments were not collected.','doc:https://deb.debian.org/debian/pool/main/f/file/file_5.44.orig.tar.gz')
for r in rr:
 assert len(r['what_it_does'].split())<=15
 assert len(r['reason'].split())<=30,(r['id'],r['reason'])
with p.open('w') as f:
 w=csv.DictWriter(f,fieldnames=rr[0].keys(),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rr)
print('refined',len(rr))

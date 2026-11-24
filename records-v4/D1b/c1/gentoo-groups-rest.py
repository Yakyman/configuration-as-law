# Continue append-only group classification after the first homogeneous batches.
exec(open('D1b/c1/gentoo-groups.py').read().split('rules=collections.defaultdict(list)')[0])
existing={r['id'] for r in read(OUT)}
individual={}
inputs={r['id']:r for r in read('D1b/in/part-gentoo.tsv')}
for fn in ['D1b/c1/part-gentoo.1.tsv','D1b/c1/part-gentoo.2.tsv']:
 for x in read(fn):
  if inputs[x['id']]['name'].startswith('/'):individual[inputs[x['id']]['name']]=x
S='S8.2-6,S8.2-7,S8.2-9,S8.2-13,S8.2-15,S8.2-16,S8.2-17'
# Explicitly inspected single-purpose generated files and collections.
record_paths={'/etc/.pwd.lock','/etc/ld.so.cache','/etc/env.d/rust/last-set','/etc/udev/hwdb.bin','/etc/xml/.lock/build-docbook-catalog.lock','/usr/lib/locale/locale-archive','/usr/lib64/gconv/gconv-modules.cache','/var/cache/ldconfig/aux-cache','/var/cache/rc/console/unicode','/var/lib/seedrng/seed.credit','/var/lib/misc/installkernel'}
record_prefixes=('/var/log/','/var/lib/gentoo/news/','/home/user/.mozilla/firefox/Crash Reports/','/home/user/.mozilla/firefox/Profile Groups/','/home/user/.mozilla/firefox/cal-check/datareporting/','/home/user/.mozilla/firefox/cal-check/saved-telemetry-pings/','/home/user/.mozilla/firefox/cal-check/crashes/')
unknown_purpose={
 '/':'Filesystem directories and swap storage.', '/boot':'Kernel, boot image, symbol map and build configuration.', '/boot/grub':'Boot menu, bootloader state and support directories.', '/boot/grub/fonts':'Bootloader font data.', '/boot/grub/i386-pc':'Bootloader modules, images and module lookup tables.', '/boot/grub/locale':'Bootloader message translations.', '/boot/grub/themes':'Bootloader theme directory.', '/boot/grub/themes/starfield':'Bootloader theme images, fonts and description.', '/etc':'System configuration, account databases, generated caches and backups.', '/etc/ssh':'SSH server host identity keys.', '/etc/xml':'XML catalogues and catalogue lock directory.', '/home':'Account home directory.', '/home/user':'Shell startup, user configuration, directories and script log.', '/home/user/.cache/AppImage-Cache/dconf':'User preference database.', '/home/user/.config':'User service and network configuration.', '/home/user/.local/bin':'User command script and browser launcher.', '/home/user/.local/opt':'Executable browser application image.', '/home/user/.ssh':'Authorized incoming SSH login keys.', '/home/user/Downloads':'Downloaded extension archive and acquisition metadata.', '/tmp':'Persistent temporary files, locks and directories.', '/usr/bin':'Command files and command selection links.', '/usr/lib':'Libraries, links and program support directories.', '/usr/lib64':'Shared libraries, loader links and support directories.', '/var/cache/distfiles':'Downloaded source archives and download cache metadata.', '/var/cache/edb':'Installer counters, metadata cache and serialized dependency state.', '/var/lib/dhcpcd':'DHCP leases, client identity and authentication state.', '/var/lib/nftables':'Saved packet filtering rules.', '/var/lib/portage':'Selected package list and package manager state.', '/var/spool/mail':'Local mailbox.', '/var/spool/nullmailer':'Persistent mail queue notification pipe.'}
def decide(m):
 p=m['path']; b=p.rsplit('/',1)[-1]; typ=m['type']
 if m['persistence']=='runtime':
  creator=('udev' if p.startswith('/run/udev') else 'OpenRC' if '/openrc' in p else 'dhcpcd' if p.startswith('/run/dhcpcd') else 'containerd' if p.startswith('/run/containerd') else 'Docker' if p.startswith('/run/docker') else 'user service' if p.startswith('/run/user') else 'boot and service programs')
  return 'RUNTIME',creator+' creates transient state; creator decision UNKNOWN where provenance or identity is unrecorded.','runtime-members'
 pp=pkg[norm(p)]
 if any(x['integrity']=='unchanged' for x in pp):return 'INSTALLED-PACKAGE','Unchanged package member after observed alias resolution.','package-member'
 if pp:return 'UNKNOWN','Original package member comparison is unknown; original versus modified object changes the deciding question.','comparison-unknown'
 if p in individual:
  x=individual[p];return x['decision'],x['reason'],'individual-overlap'
 if p.startswith('/var/db/pkg/'):
  if typ=='directory' or b in {'COUNTER','CONTENTS','metadata'}:return 'RECORD','Portage records installation inventory, counters and database structure.','vdb-generated'
  return 'UNKNOWN','Binary-package versus locally generated receipt origin and original-copy comparison are missing; executable receipts additionally lack derivation evidence.','vdb-receipts'
 if '/.cache/pip/' in p:
  if b.endswith('.body') or b.endswith('.whl'):return 'UNKNOWN','Cached payload content is unavailable; executable archive versus noncode response determines whether a program line is required.','pip-payload'
  return 'RECORD','Pip writes response metadata and cache directory structure while downloading.','pip-bookkeeping'
 if p in record_paths or p.startswith(record_prefixes) or b=='cal-user-script.log':return 'RECORD','Program-generated cache, log, working state or lock; not executable code or a chosen system value.','generated-state'
 if p.startswith('/home/user/.cache/'):
  if '/startupCache/' in p:
   if b=='urlCache-current.bin':return 'RECORD','Browser records URL cache state.','browser-url-cache'
   return 'UNKNOWN','Cached script or startup payload is opaque; originating executable code and its covering source line are unrecorded.','browser-script-cache'
  if p.endswith('/dconf/user'):return 'UNKNOWN','Preference database contents are unavailable; launch/access values versus personal preferences are not established.','opaque-preferences'
  if '/cache2/entries/' in p:return 'UNKNOWN','Response bytes and capabilities are unrecorded; cannot establish whether cached code satisfies the limited-browser-code clarification.','opaque-browser-cache'
  return 'RECORD','Browser or packaging tools create cache metadata and directory structure as working state.','cache-structure'
 if p.startswith('/home/user/.local/') and b=='__pycache__' and typ=='directory':return 'RECORD','Python creates a directory for compiled-module cache working state; this member is the directory, not its bytecode.','python-cache-directory'
 if p.startswith('/home/user/.mozilla/'):
  if '/extensions/' in p:return 'UNKNOWN','Extension installation reason and package provenance are not established for this stored archive.','extension-archive'
  if '/storage/' in p or '/extension-store/' in p:return 'UNKNOWN','Stored database payloads are unread; cannot distinguish ordinary application records from stored executable code or launch/access values.','opaque-browser-database'
  if b in {'prefs.js','user.js','handlers.json','permissions.sqlite','cert9.db','pkcs11.txt','extensions.json','addonStartup.json.lz4','extension-preferences.json','SiteSecurityServiceState.bin','security_state','data.safe.bin'}:return 'UNKNOWN','Unrecorded stored values may grant access or launch code; content and scope are needed for the ordered questions.','opaque-browser-preference'
  return 'RECORD','Firefox maintains profile bookkeeping, history, credentials or directory structure while running.','browser-profile-record'
 if p in {'/etc/group-','/etc/gshadow-','/etc/passwd-','/etc/shadow-','/etc/subuid-','/etc/subgid-'}:return 'RECORD','Account tools retain previous database contents as backup working state.','account-backup'
 if p.startswith('/var/cache/edb/'):
  if b=='vdb_blockers.pickle':return 'UNKNOWN','Pickle payload and deserialization behavior are not recorded; data-only cache versus executable reconstruction is unresolved.','opaque-pickle'
  return 'RECORD','Portage writes counters, metadata-cache directories and processing state.','portage-cache'
 if p.startswith('/var/cache/distfiles/'):
  if b in {'.layout.conf.distfiles.gentoo.org','.mirror-cache.json'}:return 'RECORD','Portage records mirror lookup cache data.','mirror-cache'
  return 'UNKNOWN','Archive contents and executable formats are unrecorded; a filename and prefix digest do not decide executable code versus cached data.','source-archive'
 if p.startswith('/usr/share/') and b=='dir':return 'RECORD','install-info maintains the generated Info document index.','info-index'
 if p in {'/var/lib/portage/preserved_libs_registry','/var/lib/portage/config'}:return 'RECORD','Portage records library preservation and configuration-file update bookkeeping.','portage-state'
 if p.startswith('/var/lib/dhcpcd/'):
  return 'UNKNOWN','Lease, identity or authentication contents and origin are unrecorded; person-chosen network values versus automatic working state are unresolved.','dhcp-state'
 if p.startswith('/etc/') or p.startswith('/home/user/.config/') or p.startswith('/home/user/.ssh/') or p.startswith('/var/lib/nftables/') or p.startswith('/var/lib/portage/'):
  return 'UNKNOWN','Historical creation and original package comparison are missing; personally chosen settings, installation defaults or generated state require different decisions.','configuration-origin'
 if typ=='directory':return 'UNKNOWN','Directory creator and original package metadata are unrecorded; package-supplied, program-created and personal directories have different decisions.','directory-origin'
 if typ=='symlink':return 'UNKNOWN','Link provenance and original target comparison are missing; package membership, generated selection and personal link creation remain unresolved.','link-origin'
 if p.startswith('/boot/'):
  return 'UNKNOWN','Boot-file installation or generation source and original-copy integrity are not recorded; package, derived program and noncode alternatives remain.','boot-origin'
 if p.startswith('/usr/'):
  return 'UNKNOWN','No original package-file comparison or generated-source record covers this member; package, program and noncode alternatives require those facts.','system-file-origin'
 if p.startswith('/tmp/'):
  return 'UNKNOWN','The file is persistent; contents and historical creator are unrecorded, so its name does not establish runtime or program-record status.','temporary-origin'
 if p=='/var/spool/nullmailer/trigger':return 'UNKNOWN','FIFO persists on disk; installation/default provenance and its creation history are not recorded.','persistent-fifo'
 if p=='/var/spool/mail/user':return 'UNKNOWN','Mailbox payload and creator history are not read; received material versus program-written mailbox state remains unresolved.','mailbox'
 if p.startswith('/home/user/Downloads/'):
  return 'UNKNOWN','Downloaded bytes and acquisition history are not established; archive execution and package installation cannot be determined from a filename.','download'
 if p.startswith('/home/user/'):
  return 'UNKNOWN','Stored user object contents and origin are missing; executable code, launch/access values and personal records require different decisions.','user-object'
 if p=='/swapfile':return 'UNKNOWN','Swap backing is persistent; creation/default provenance and active filesystem configuration are unrecorded.','swap-storage'
 raise ValueError(p)
# Supplemental member mapping makes every mixed partition explicit, including long groups.
ledger=pathlib.Path('D1b/c1/gentoo-member-decisions.tsv'); audits=[]; ruleids=collections.defaultdict(list)
f=OUT.open('a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
for r in rows:
 if r['id'] in existing:continue
 ms=members[r['id']];results=[decide(m) for m in ms];ds={a[0] for a in results}
 for m,(d,why,rule) in zip(ms,results):audits.append([r['id'],m['path'],d,rule,why]);ruleids[rule].append(r['id'])
 d=next(iter(ds)) if len(ds)==1 else 'MIXED'
 what=unknown_purpose.get(r['name'],'Stored '+('installation database members.' if r['name'].startswith('/var/db/pkg') else 'cache members.' if '/.cache/pip' in r['name'] else 'objects with individually inspected member roles.'))
 if d=='MIXED':
  if r['name'].startswith('/var/db/pkg'):why='COUNTER, CONTENTS, metadata: RECORD; remaining receipt files: UNKNOWN (original acquisition and integrity missing).'
  elif '/.cache/pip' in r['name']:why='*.body or *.whl: UNKNOWN (payload unread); all other members: RECORD (cache bookkeeping).'
  elif r['name'].endswith('/startupCache'):why='urlCache-current.bin: RECORD; other members: UNKNOWN (cached code/source identity unavailable).'
  else:why='Member decisions: '+', '.join(sorted(ds))+'. Exact per-member partition and missing facts: gentoo-member-decisions.tsv, keyed by this id.'
 elif d=='RUNTIME':
  creators=sorted({a[1].split(' creates ')[0] for a in results})
  what='Transient service state, endpoints or runtime directory entries.'
  why='Creators: '+', '.join(creators)+'. Parent decision UNKNOWN where identity/provenance is unrecorded; every member is transient.'
 elif d=='UNKNOWN':
  unique=list(dict.fromkeys(a[1] for a in results))
  why=unique[0] if len(unique)==1 else 'Member contents, package comparison or historical acquisition are missing; each unresolved fact and its alternatives are listed in gentoo-member-decisions.tsv under this id.'
 elif d=='RECORD':why='Every member is program-written bookkeeping, cache structure, history or working state; no installed package member, executable code or chosen system value is established.'
 else:why=results[0][1]
 assert len(what.split())<=15,(r['id'],what)
 assert len(why.split())<=30,(r['id'],why)
 w.writerow([r['id'],d,S,what,'raw:'+str(ROOT/decode(r['members'])['file']),why]);f.flush()
f.close()
with ledger.open('w') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['id','member','decision','rule','reason']);w.writerows(audits)
json.dump({k:list(dict.fromkeys(v)) for k,v in ruleids.items()},open('D1b/c1/gentoo-rest-rule-ids.json','w'),indent=2)
print('Rows appended',len({r[0] for r in audits}));print('Member rule counts',dict(collections.Counter(r[3] for r in audits)))

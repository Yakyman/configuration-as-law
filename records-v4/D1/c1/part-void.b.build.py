import csv,json,collections,re,pathlib
csv.field_size_limit(10000000)
root=pathlib.Path('D1/in/raw/void')
rs=[r for r in csv.DictReader(open('D1/in/part-void.tsv'),delimiter='\t') if r['kind']=='L2:stored-ownership-unresolved'][1015:2029]
pf={x['path']:x for x in csv.DictReader(open(root/'package-files.tsv'),delimiter='\t')}
headers=['id','decision','sentences','what_it_does','basis','reason']
out=pathlib.Path('D1/c1/part-void.b.tsv')
existing={r['id'] for r in csv.DictReader(open(out),delimiter='\t')} if out.exists() else set()
audit=[]
with out.open('a') as f:
 w=csv.DictWriter(f,headers,delimiter='\t',lineterminator='\n')
 if not existing:w.writeheader()
 for r in rs:
  p=r['name']; mf=json.loads(r['members']); ms=list(csv.DictReader(open(root/mf['file']),delimiter='\t'))
  assert len(ms)==mf['count'] and mf['complete']
  assert all(m['persistence']=='persistent' for m in ms)
  assert all(m['path'] not in pf for m in ms)
  d='UNKNOWN';s='S8.2-6,S8.2-7,S8.2-8,S8.2-15,S8.2-16'
  what='Stored directory entries organize files and subdirectories.'
  why='Missing member provenance and installation-integrity facts prevent deciding package coverage versus independently created objects.'
  rule='U'
  if p.startswith('/usr/lib/modules/'):
   what='Stored kernel-module tree entries provide drivers or organize module files.'
   why='Old-kernel member provenance and integrity are unrecorded; package coverage versus retained code or generated directories cannot be established.'
  elif p.startswith('/usr/lib/python'):
   what='Python library directories organize importable modules and compiled caches.'
  if p.endswith('/__pycache__'):
   assert all(m['path'].endswith('.pyc') and m['type']=='file' for m in ms)
   for m in ms:
    src=re.sub(r'\.cpython-314(?:\.opt-1)?\.pyc$','.py',m['path'].replace('/__pycache__/','/'))
    assert src in pf
   rule='P';d='PROGRAM-DERIVED';s='S8.2-6,S8.2-9,S8.2-10,S8.2-16'
   what='Compiled Python bytecode executes library modules through the interpreter.'
   why='Installation log records byte-compilation; these executable copies are covered by their source lines, before the cache-record question.'
  if p.startswith('/usr/share/mime/'):
   assert all(m['path'].endswith('.xml') and m['type']=='file' for m in ms)
   rule='M';d='RECORD';s='S8.2-6,S8.2-15,S8.2-23'
   what='Generated MIME descriptions supply file-type metadata to applications.'
   why='Recorded database regeneration creates noncode lookup output; no chosen setting is evidenced, so these are program records.'
  single={
   '/usr/share/applications':('UNKNOWN','Desktop MIME cache indexes application file-type handlers.','Whether this cache was delivered unchanged, generated, or manually edited is not established.'),
   '/usr/share/glib-2.0/schemas':('RECORD','Compiled schema database supplies application setting definitions.','The logged GSettings refresh generates a noncode schema database, not a chosen setting value; question four gives program record.'),
   '/usr/share/icons/Adwaita':('RECORD','Icon cache accelerates theme icon lookup.','The log records cache regeneration; the generated noncode lookup cache is a program record.'),
   '/usr/share/icons/hicolor':('RECORD','Icon cache accelerates theme icon lookup.','The log records cache regeneration; the generated noncode lookup cache is a program record.'),
   '/usr/share/man':('UNKNOWN','Manual-page database indexes documentation.','Database provenance is unrecorded: unchanged package content and generated program record give different decisions.'),
   '/usr/share/man/man1':('MIXED','Manual-page symlinks select command documentation.','ex.1, vi.1, view.1: UNKNOWN provenance; all other listed links: RECORD, their creation as documentation alternatives is logged.'),
   '/usr/share/man/man8':('MIXED','Manual-page symlinks select administration documentation.','ntpd.8, ping.8, ping6.8: RECORD, generated documentation links; traceroute.8: UNKNOWN creation provenance and installation integrity.'),
   '/usr/share/mime':('MIXED','MIME database files and directories organize type lookup.','Files: RECORD after logged regeneration; directories: UNKNOWN because creation provenance and unchanged package delivery are unestablished.'),
   '/var/cache/ldconfig':('UNKNOWN','Auxiliary linker cache accelerates shared-library inspection.','The logged main-cache update does not establish this auxiliary file was regenerated or whether it remains package-delivered.'),
   '/var/cache/xbps':('RECORD','Cached package archives and signatures support package installation.','Every archive and signature has a logged download; these stored installer cache copies are program records, distinct from installed package contents.'),
   '/var/db/dhcpcd':('UNKNOWN','DHCP leases, identity and secret support network configuration.','Creation provenance and whether identifiers or secret were chosen, generated, or package-delivered are unrecorded.'),
   '/var/db/sudo/lectured':('UNKNOWN','Sudo marker remembers whether an account received its lecture.','Marker provenance and unchanged package delivery are not established; a generated record and installed content differ.'),
   '/var/db/xbps':('UNKNOWN','Package database tracks installed packages and repository state.','Complete group includes metadata and directories; package delivery, generation provenance and installation integrity are not established for every member.'),
   '/var/db/xbps/keys':('UNKNOWN','Repository trust key authenticates package metadata.','Trust selection and key delivery provenance are unrecorded; package content, default setting and chosen setting require different lines.'),
   '/var/lib/NetworkManager':('UNKNOWN','Network state stores leases, timestamps, internal configuration and secret.','Member contents and creation origins do not establish unchanged package delivery, chosen settings, or generated state for every member.'),
   '/var/lib/chrony':('UNKNOWN','Clock drift file preserves frequency correction.','Whether the drift value was measured, manually supplied, or delivered unchanged is not established.'),
   '/var/lib/dbus':('UNKNOWN','Machine identifier identifies the computer to message-bus applications.','Whether this identifier was generated, explicitly chosen, or delivered unchanged is not established.'),
   '/var/lib/seedrng':('UNKNOWN','Persistent seed supplies randomness at later boots.','Seed creation provenance and package delivery are not established; persistent storage alone does not prove a generated record.'),
   '/var/log':('UNKNOWN','Login records, kernel log and chrony directory retain operational history.','File and directory creation provenance and installation integrity are unknown; filenames alone do not establish all members were generated.'),
   '/var/spool':('UNKNOWN','Mail symlink redirects spool storage.','Link delivery, creation provenance and unchanged installation state are unrecorded.'),
  }
  if p in single:
   rule='individual';d,what,why=single[p]
   if d=='RECORD':s='S8.2-6,S8.2-15,S8.2-23'
   if d=='MIXED':s='S8.2-6,S8.2-7,S8.2-15,S8.2-23'
  if p.startswith('/var/db/xbps/https_'):
   rule='individual';what='Repository index caches available package metadata.';why='Repository-index provenance is unrecorded; delivered package content, program download, and manually supplied material give different decisions.'
  row=dict(zip(headers,[r['id'],d,s,what,'raw:D1/in/raw/void/'+mf['file'],why]))
  assert len(what.split())<=15 and len(why.split())<=30
  if r['id'] not in existing:w.writerow(row);f.flush()
  audit.append((r,ms,rule,d))
print(collections.Counter(d for r,ms,rule,d in audit))

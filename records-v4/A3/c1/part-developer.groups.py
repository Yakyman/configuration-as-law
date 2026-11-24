import csv,json,collections,pathlib,re
ROOT=pathlib.Path('A3/in/raw/developer')
OUT=pathlib.Path('A3/c1/part-developer.tsv')
FIELDS=['id','decision','sentences','what_it_does','basis','reason']
rows=[r for r in csv.DictReader(open('A3/in/part-developer.tsv'),delimiter='\t') if r['kind'] in ['2:stored-ownership-unresolved','2:image-container-store']]
pf=collections.defaultdict(list)
for x in csv.DictReader(open(ROOT/'package-files.tsv'),delimiter='\t'):pf[x['path']].append(x)
def normal(s):
 p=s.strip('/').split('/')
 if p[0]=='home' and len(p)>1:return ('user-home' if p[1]=='user' else 'brew-home')+'/'+ '/'.join(p[2:])
 if p[0]=='root':return 'root-home/'+'/'.join(p[1:])
 return '/'.join(p)
def members(r):
 d=json.loads(r['members'])
 return list(csv.DictReader(open(ROOT/d['file']),delimiter='\t')) if 'file' in d else []
def append(r,decision,sentences,what,reason,basis=None):
 assert len(what.split())<=15 and len(reason.split())<=30,(r['id'],reason)
 val=dict(zip(FIELDS,[r['id'],decision,sentences,what,basis or 'raw:A3/in/raw/developer/'+json.loads(r['members'])['file'],reason]))
 assert all('\t' not in v and '\n' not in v for v in val.values())
 if r['id'] not in done:
  writer.writerow(val); stream.flush();done.add(r['id'])
def installation_tree(p):
 return (p.startswith('brew-home/.linuxbrew/') and '/.git' not in p and '/var/' not in p) or p.startswith('user-home/.julia/juliaup/julia-') or p.startswith('user-home/.bun/install/global/node_modules') or (p.startswith('user-home/.bun/install/cache/') and p!='user-home/.bun/install/cache') or p.startswith('user-home/Projects/scc/.cal-modcache/') or p.startswith('user-home/.local/share/gem/ruby/gems/') or p.startswith('user-home/.cache/uv/archive-v0/')
done=set()
if OUT.exists():done={r['id'] for r in csv.DictReader(open(OUT),delimiter='\t')}
stream=open(OUT,'a',newline='');writer=csv.DictWriter(stream,FIELDS,delimiter='\t',lineterminator='\n')
if OUT.stat().st_size==0:writer.writeheader();stream.flush()
for r in rows:
 p=normal(r['name']);ms=members(r)
 if installation_tree(p):
  assert ms and all(m['persistence']=='persistent' and m['path'] not in pf for m in ms)
  append(r,'UNKNOWN','S8.2-6,S8.2-7,S8.2-8,S8.2-16','Development tool files, directories, or links used for code, resources, and package management.','Member installation provenance and unchanged status are unestablished; package coverage versus later program, setting, record, or material decisions depends on these facts.')
stream.close()
print('Saved',len(done),'rows')
stream=open(OUT,'a',newline='');writer=csv.DictWriter(stream,FIELDS,delimiter='\t',lineterminator='\n')
for r in rows:
 if r['id'] in done:continue
 p=normal(r['name']);ms=members(r)
 if p.startswith('user-home/.cache/go-build'):
  assert all(m['persistence']=='persistent' and m['path'] not in pf for m in ms)
  assert all((m['type']=='file' and m['executable']=='False') or (p=='user-home/.cache/go-build' and m['type']=='directory') for m in ms)
  append(r,'RECORD','S8.2-6,S8.2-9,S8.2-15,S8.2-20','Go build cache indexes, non-executable intermediate artifacts, and cache directories.','Go creates these cache records; no executable cache-entry directories occur. Non-executable build intermediates and indexes satisfy the fourth question.')
 elif re.search(r'/\.git/(objects|logs|refs)(/|$)',p):
  assert all(m['type'] in ('directory','file') for m in ms)
  append(r,'RECORD','S8.2-9,S8.2-14,S8.2-15','Git object database, references, or reference-change logs.','Git stores repository history and working state here; these database objects and references are not executed or system settings.')
 elif p.startswith(('var/cache/libdnf5','var/cache/PackageKit','var/cache/man')):
  assert all(m['type'] in ('directory','file') for m in ms)
  append(r,'RECORD','S8.2-9,S8.2-15','Repository metadata cache or manual-page index cache.','Programs download or generate these non-executable indexes and metadata while running; they are caches, not installed package payloads or chosen settings.')
stream.close()
print('Saved',len(done),'rows')
stream=open(OUT,'a',newline='');writer=csv.DictWriter(stream,FIELDS,delimiter='\t',lineterminator='\n')
runtime_map={'NetworkManager':'NetworkManager','avahi-daemon':'avahi-daemon','chrony':'chronyd','cockpit':'cockpit-tls','containerd':'containerd','cups':'cupsd','dbus':'dbus-broker','docker':'dockerd','fsck':'fsck','irqbalance':'irqbalance','libvirt':'libvirtd','lvm':'lvmpolld','pcscd':'pcscd','ssh-unix-local':'sshd','stratisd':'stratisd','sudo':'sudo','tuned':'tuned','udev':'systemd-udevd','tmpfiles.d':'systemd-tmpfiles'}
def creator_decision(name):
 matches=[v for path,vs in pf.items() if path.endswith('/'+name) for v in vs]
 return 'INSTALLED-PACKAGE' if any(v['integrity']=='unchanged' for v in matches) else 'UNKNOWN'
for r in rows:
 if r['id'] in done:continue
 p=normal(r['name']);ms=members(r)
 if ms and all(m['persistence']=='runtime' for m in ms):
  creator='systemd'
  if p.startswith('run/'):
   creator=runtime_map.get(p.split('/')[1],'systemd')
  if p=='run':creator='systemd and boot services'
  elif p=='run/user/1000':creator='systemd and PipeWire'
  elif p=='run/user/1000/pulse':creator='pipewire-pulse'
  elif p.startswith('run/initramfs'):creator='dracut'
  elif p=='run/tpm2-tss':creator='TPM event-log service'
  dec=creator_decision(creator)
  append(r,'RUNTIME','S8.2-5','Volatile service sockets, state, generated files, or directories for this boot.',f'{creator} ({dec}) creates these boot-lifetime objects; member filesystem facts are runtime, so no separate declaration line applies.')
 elif p.startswith('user-home/Projects/scc/vendor'):
  assert all(m['persistence']=='persistent' and m['path'] not in pf for m in ms)
  append(r,'UNKNOWN','S8.2-7,S8.2-9,S8.2-15,S8.2-16','Vendored Go dependency sources, resources, and containing directories.','The inventory lacks member acquisition and generation lineage; package coverage, derivation from recorded sources, and independently brought source material cannot be distinguished.')
stream.close()
print('Saved',len(done),'rows')

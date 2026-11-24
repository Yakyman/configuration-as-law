import csv,json,collections,pathlib
base=pathlib.Path('D1b/handoff/gentoo'); out=pathlib.Path('D1b/c1/part-gentoo.2.tsv')
def rows(p):return list(csv.DictReader(open(p),delimiter='\t'))
rs=[r for r in rows('D1b/in/part-gentoo.tsv') if r['kind'] in ['L2:code-ownership-unresolved','L2:image','L2:image-container-store']]
pf=collections.defaultdict(list)
for r in rows(base/'package-files.tsv'):pf[r['path']].append(r)
aliases=[('/usr/bin/','/bin/'),('/usr/bin/','/sbin/'),('/usr/bin/','/usr/sbin/'),('/usr/lib/','/lib/'),('/usr/lib64/','/lib64/')]
seen={r['id'] for r in rows(out)} if out.exists() else set()
with open(out,'a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not seen:w.writerow(['id','decision','sentences','what_it_does','basis','reason'])
 for r in rs:
  if r['id'] in seen:continue
  p=r['name'];alts=[p]+[b+p[len(a):] for a,b in aliases if p.startswith(a)]; matches=[m for a in alts for m in pf[a]]
  d='UNKNOWN';s='S8.2-7,S8.2-9,S8.2-16';what='Stored executable code';basis='raw:D1b/handoff/gentoo/objects.tsv';reason='Acquisition and derivation history is unrecorded; package coverage, a generating source line, and a separate program line cannot be distinguished.'
  if matches:
   assert all(m['integrity']=='unchanged' for m in matches)
   d='INSTALLED-PACKAGE';s='S8.2-6,S8.2-7,S8.2-8,S8.2-16';what='Unchanged packaged boot code' if r['kind']=='L2:image' else 'Unchanged packaged executable or library';basis='raw:D1b/handoff/gentoo/package-files.tsv';reason='Unchanged package member; recorded filesystem aliases identify the same path. Its supplying package line covers it.'
  elif p.startswith('/var/db/repos/'):
   what='Repository script with a recorded interpreter marker';reason='Interpreter marker establishes code, but repository acquisition history and a recorded generating source are absent; own versus derived program coverage remains unknown.'
  elif p.endswith('/times.json'):
   d='RECORD';s='S8.2-14,S8.2-15,S8.2-23';what='Firefox profile creation timestamp';basis='doc:https://docs.telemetry.mozilla.org/concepts/profile/profile_creation';reason='Firefox writes profile age timestamps as program state; reading these values neither launches code nor grants access.'
  elif p=='/boot/grub/i386-pc/core.img':
   what='GRUB core boot code assembled from modules';basis='doc:https://www.gnu.org/software/grub/manual/grub/grub.html';reason='GRUB documents core image generation, but this copy has no recorded generating inputs or acquisition history; own versus derived coverage remains unknown.'
  elif p=='/boot/grub/i386-pc/boot.img':
   what='GRUB BIOS first-stage boot code';basis='doc:https://www.gnu.org/software/grub/manual/grub/grub.html';reason='Boot code is executable; no package reference or recorded installation-generation lineage establishes whether this stored copy has package, derived, or own coverage.'
  elif p=='/boot/initramfs-6.18.64-p1-gentoo-dist.img':
   what='Persistent initial RAM filesystem archive';reason='Archive contents and its generating inputs are unrecorded; package membership, executable members, and source-line coverage cannot be established.'
  elif p=='/etc/profile.env':
   what='Shell environment startup file';basis='raw:D1b/handoff/gentoo/configuration-origin.tsv';reason='Creation is explicitly unknown; no content or generating inputs establish whether this shell startup file is unchanged, generated, or independently supplied code.'
  elif p.endswith('/modinfo.sh'):what='GRUB module information shell script'
  elif p.endswith('/.bash_logout'):what='Bash logout commands'
  elif p.endswith('/.bash_profile'):what='Bash login startup commands'
  elif p.endswith('/.bashrc'):what='Bash interactive startup commands'
  elif p.endswith('/cal-user'):what='User service startup script'
  elif p.endswith('/cal-user-script'):what='User command script'
  elif p.endswith('/bin/firefox'):what='User browser launch script'
  elif p.endswith('.AppImage'):what='Self-contained browser executable image'
  elif '/bin/' in p:what='Python package command entry script'
  if r['kind']=='L2:image-container-store':
   d='MIXED';s='S8.2-7,S8.2-9,S8.2-13,S8.2-15,S8.2-16';basis='raw:D1b/handoff/gentoo/store-members.tsv';what='Persistent container storage and metadata'
   if p.endswith('containerd'):reason='.keep file: INSTALLED-PACKAGE; metadata databases and UUID: RECORD; snapshot and content members: UNKNOWN package integrity and acquisition lineage.'
   else:reason='Logs, caches, engine identifier: RECORD; hostconfig and configuration: SETTING-OWN; network database and remaining members: UNKNOWN contents or originating values.'
  assert len(what.split())<=15 and len(reason.split())<=30
  w.writerow([r['id'],d,s,what,basis,reason]);f.flush()
res=rows(out);assert len(res)==len(rs)==len({r['id'] for r in res});assert {r['id'] for r in res}=={r['id'] for r in rs}
assert all(r['decision'] in 'INSTALLED-OWN INSTALLED-PACKAGE INSTALLED-DERIVED PROGRAM-OWN PROGRAM-DERIVED SETTING-OWN SETTING-DEFAULT RECORD MATERIAL RUNTIME ACTION GAP-NONE GAP-TWO UNKNOWN MIXED'.split() for r in res)
print(collections.Counter(r['decision'] for r in res))

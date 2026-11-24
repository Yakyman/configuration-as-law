import csv,json,collections,pathlib
csv.field_size_limit(10000000)
root=pathlib.Path('D1/in/raw/microos')
rows=[r for r in csv.DictReader(open('D1/in/part-microos.tsv'),delimiter='\t') if r['kind'] in {'L2:executable-code-outside-packages','L2:image','L2:snapshot'}]
pf=collections.defaultdict(list)
for r in csv.DictReader(open(root/'package-files.tsv'),delimiter='\t'):pf[r['path']].append(r)
out=pathlib.Path('D1/c1/part-microos.code.tsv')
fields=['id','decision','sentences','what_it_does','basis','reason']
seen={r['id'] for r in csv.DictReader(open(out),delimiter='\t')} if out.exists() else set()
with out.open('a') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n')
 if not seen:w.writeheader()
 for r in rows:
  if r['id'] in seen:continue
  n=r['name']; m=json.loads(r['members']);m=m.get('metadata',m)
  assert m['persistence']=='persistent'
  d='UNKNOWN';s='S8.2-7,S8.2-9,S8.2-16';b='raw:D1/in/raw/microos/raw/0004-filesystem.out'
  if n.startswith('/.snapshots/1/snapshot/'):
   what='Persistent file retained in an earlier filesystem snapshot.'
   reason='Snapshot-specific package provenance and installation integrity are unrecorded; current-root ownership and prefix equality cannot establish the first question for this retained file.'
  elif r['kind']=='L2:snapshot':
   what='Persistent filesystem subvolume with unexpanded stored contents.'
   s='S8.2-7,S8.2-9,S8.2-11,S8.2-15'
   reason='The opaque directory has no complete member inventory or creation provenance; member classes and whether this stored subvolume is package content remain unknown.'
  elif any(p['integrity']=='unchanged' for p in pf[n]):
   d='INSTALLED-PACKAGE';s='S8.2-6,S8.2-7,S8.2-8,S8.2-16';b='raw:D1/in/raw/microos/package-files.tsv'
   what='Packaged GRUB boot image used to construct a bootloader.'
   reason='Exact path has unchanged package-file integrity; the first question decides before executability, and its package line covers it.'
  elif n.endswith('/.bashrc') or n.endswith('/.profile'):
   what='Persistent shell startup file executed to initialize a user shell.'
   reason='Startup code is a program; matching skeleton bytes do not establish whether the system generated it from a recorded source or a person copied it.'
  elif n.endswith('grub.cfg'):
   what='GRUB boot configuration interpreted as bootloader commands.'
   s='S8.2-9,S8.2-10,S8.2-16,S8.2-23'
   reason='GRUB executes this command file; inventory does not establish whether it was system-generated from a recorded source or independently written.'
  elif n.endswith('core.img'):
   what='GRUB core boot image containing bootloader code and modules.'
   reason='Bootloader code is present; inventory does not identify the source from which this installed core image was generated, needed to distinguish own and derived lines.'
  elif n.endswith('boot.img'):
   what='GRUB initial boot image for starting the core loader.'
   reason='Bootloader image matches packaged bytes, but actual installation provenance and a source line for system copying are absent; own versus derived coverage remains unknown.'
  elif n.endswith('MokManager.efi'):
   what='EFI program for managing machine owner Secure Boot keys.'
   reason='EFI executable provenance is unrecorded; inventory does not establish package delivery or system derivation from a source line versus independent copying.'
  elif n.endswith('.efi'):
   what='EFI boot executable used during firmware startup.'
   reason='EFI executable provenance is unrecorded; inventory does not establish package delivery or system derivation from a source line versus independent copying.'
  elif n.endswith('modinfo.sh'):
   what='Shell code describing GRUB module build parameters.'
   reason='A persistent shell script is present; inventory does not establish whether system copying from a recorded source or independent placement supplied this file.'
  elif n.endswith('activate-theme'):
   what='Shell script for activating the installed bootloader theme.'
   reason='Shebang identifies script code, but package ownership and the source of system generation are absent; own versus derived recording cannot be established.'
  else:raise ValueError(n)
  assert len(what.split())<=15 and len(reason.split())<=30
  w.writerow(dict(zip(fields,[r['id'],d,s,what,b,reason])));f.flush()
print(collections.Counter(r['decision'] for r in csv.DictReader(open(out),delimiter='\t')))

import csv,json,base64,pathlib,collections
csv.field_size_limit(10000000)
root=pathlib.Path('D1/in/raw/alma'); dst=pathlib.Path('D1/c1/part-alma.tsv')
rows=[r for r in csv.DictReader(open('D1/in/part-alma.tsv'),delimiter='\t') if r['kind'].startswith('L2:') and r['kind']!='L2:stored-ownership-unresolved']
def canon(p):
 for a,b in [('/lib/','/usr/lib/'),('/lib64/','/usr/lib64/'),('/bin/','/usr/bin/'),('/sbin/','/usr/sbin/')]:
  if p.startswith(a):return b+p[len(a):]
 return p
pf=collections.defaultdict(list)
for r in csv.DictReader((root/'package-files.tsv').open(),delimiter='\t'):pf[canon(r['path'])].append(r)
entries={}
for line in (root/'raw/0009-metadata-read-256.out').open():
 x=json.loads(line)
 if '/cal-marionette/' in x.get('path','') and x['path'].endswith('/RECORD') and x.get('status')=='ok':
  for p,h,size in csv.reader(base64.b64decode(x['data']).decode().splitlines()):
   if p.startswith('../../bin/'):
    tail=p.rsplit('/',1)[1]; hh=h[7:]; entries[tail]=(base64.urlsafe_b64decode(hh+'='*((4-len(hh)%4)%4)).hex(),int(size),x['path'].split('/')[-2])
# Explicit row-level judgments for nonhomogeneous files; no class inferred from inventory kind.
custom={
'ccee8b9ad93a05d741a4a687':('GRUB bootstrap image copied into the boot filesystem.','Its code is identifiable, but the retained facts do not establish whether the system obtained this copy from a recorded source.'),
'c83a82a3d1f5bc0ad561ed46':('GRUB core image combining boot code and modules.','The image is executable boot code; its actual build provenance and source line are not retained.'),
'6ab52ad29dde92c736eff4ca':('Shell metadata script for the GRUB module installation.','Shell code is present, but its package origin, installation integrity, and derivation from a recorded source are unretained.'),
'2c25c1a886c5db421b08087b':('Rescue initial filesystem image for early boot.','The opaque image has no retained member inventory or build provenance establishing its contents and covering source line.'),
'c4a7c6d6eb439eb9d680a65e':('Initial filesystem image used during kernel startup.','The package manifest marks this image changed; actual contents and generation provenance are not retained to determine its class and source line.'),
'9ba0bbb217552126cc411cf7':('Crash-dump initial filesystem image.','The opaque image has no retained member inventory or build provenance establishing its contents and covering source line.'),
'abd91d1c4f4b41c4ed6eb130':('Rescue Linux kernel image.','Executable kernel code is identifiable, but its actual copy provenance and covering source line are not retained.'),
'c5e3c35f51457c614d2f0db6':('Shell script contributing tuned parameters to generated GRUB configuration.','The script is executable code; whether it was separately supplied or generated from a recorded source is unretained.'),
'd8bd0ebf0971269fa664e177':('Shell commands executed when a login shell exits.','Package-copy origin and installation integrity are unretained; these determine installed-package coverage versus own or derived program coverage.'),
'd9c06dc1dfaaba01abd91aa8':('Shell commands executed when a login shell starts.','Package-copy origin and installation integrity are unretained; these determine installed-package coverage versus own or derived program coverage.'),
'fbc363e66275dcb22563f6ee':('Commands configuring an interactive Bash shell.','Package-copy origin and installation integrity are unretained; these determine installed-package coverage versus own or derived program coverage.'),
'cdd79753059a5ce23c29ee2e':('Executable local shell script.','The shebang establishes executable code, but the retained empty action log does not establish its contents, installation origin or generation source.'),
'930b9792c746a9bafad93f57':('Node.js command-line entry script for cowsay.','Package placement is known, but npm per-file provenance and installation integrity are unretained; unchanged installed content and separately modified code classify differently.'),
'79608afad4f605639b600ea2':('JavaScript library implementing terminal-aware text wrapping.','Package placement is known, but npm per-file provenance and installation integrity are unretained; unchanged installed content and separately modified code classify differently.'),
'0c99474b7568b9110f088ac0':('User Flatpak application and runtime storage directory.','Storage is persistent but unexpanded; its complete members and their deployment provenance are unavailable, so a homogeneous or mixed classification cannot be established.'),
'9fb5386f2fe6a4a2a188166a':('Persistent container image and writable-layer storage.','Storage is unexpanded; its complete members and their package, code, setting or record status are unavailable.'),
'3c6010fa39aa94b271b93734':('System Flatpak storage directory.','The directory is persistent and unexpanded; creation provenance and complete stored membership are not retained.'),
}
existing={r['id'] for r in csv.DictReader(dst.open(),delimiter='\t')}
checks=[]; decisions=[]
with dst.open('a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 for r in rows:
  rid=r['id']; p=r['name']; m=json.loads(r['members']); md=m.get('metadata',m)
  if any(q['integrity']=='unchanged' for q in pf[p]):
   d='INSTALLED-PACKAGE'; s='S8.2-6,S8.2-7,S8.2-8,S8.2-16';what='Unchanged packaged boot or library code.';basis='raw:D1/in/raw/alma/package-files.tsv';why='The native manifest verifies unchanged content; the first question decides before executable-code questions, and its package line covers it.'
   checks.append((rid,p,'native manifest unchanged'))
  elif '/cal-marionette/bin/' in p:
   digest,size,dist=entries[p.rsplit('/',1)[1]]
   assert md['size']==md['signature_bytes']==size and md['signature']=='sha256-prefix4096:'+digest
   d='INSTALLED-PACKAGE';s='S8.2-6,S8.2-7,S8.2-8,S8.2-16';what='Installed Python console entry script.';basis='raw:D1/in/raw/alma/raw/0009-metadata-read-256.out';why='The installed distribution RECORD digest and size exactly match the complete script bytes after pip target relocation; its package line covers unchanged installed content.'
   checks.append((rid,dist,'full RECORD digest and length match; target relocation'))
  elif rid=='alma-469368e2c39591fdcb2f7fa7':
   d='RECORD';s='S8.2-15,S8.2-23';what='Firefox profile creation timestamps stored as JSON values.';basis='doc:https://docs.telemetry.mozilla.org/concepts/profile/profile_creation';why='Firefox stores profile creation timestamps as values; executable permission does not make JSON code, and these timestamps neither launch programs nor grant access.'
  elif md.get('persistence')=='runtime':
   d='RUNTIME';s='S8.2-5,S8.2-7,S8.2-16';basis='raw:D1/in/raw/alma/raw/0004-filesystem.out'
   if '/seccomp/' in p:what='Temporary compiled seccomp filter cache created by crun.';why='Exists on a runtime filesystem; crun creates this cache. Its unchanged packaged executable is INSTALLED-PACKAGE.'
   else:what='Temporary file recording the container process identifier.';why='Exists on a runtime filesystem; crun writes the container PID file. Its unchanged packaged executable is INSTALLED-PACKAGE.'
  else:
   d='UNKNOWN';s='S8.2-7,S8.2-9,S8.2-15,S8.2-16';what,why=custom[rid[5:]];basis='raw:D1/in/raw/alma/raw/0004-filesystem.out'
  assert len(what.split())<=15,(rid,what)
  assert len(why.split())<=30,(rid,why)
  result=[rid,d,s,what,basis,why];decisions.append(result)
  if rid not in existing:w.writerow(result);f.flush()
with open('D1/c1/part-alma.notes.md','a') as f:
 f.write('## Individual stored files and images\n\nAll 41 non-group L2 rows were inspected individually. Thirteen native packaged files resolve exactly after the four filesystem symlinks /lib, /lib64, /bin and /sbin are followed, using their recorded target fields; the manifest says unchanged. S8.2-7 wins before code classification. Manual checks for this homogeneous unchanged-file rule (more than ten) are listed below.\n\n')
 for rid,p,why in checks:f.write(f'- {rid}: {p}; {why}.\n')
 f.write('\nEight Python entry scripts require a separate individual integrity calculation: each retained signature covers the whole file (size equals signature_bytes, under 4096), and its digest equals the installed RECORD SHA-256. These are not assumptions from prefix signatures: both the recorded installation digest and the complete-file length were checked. The apparent ../../bin path discrepancy is explained by pip target relocation, documented by the retained pip version source: https://github.com/pypa/pip/blob/23.3.2/src/pip/_internal/commands/install.py — `shutil.move(os.path.join(lib_dir, item), target_item_dir)`. Its _handle_target_dir moves library and data-directory items, including bin, into the target. All eight checks are listed above because the class contains fewer than ten objects. The original package-files.tsv is unchanged.\n\n')
 f.write('https://docs.telemetry.mozilla.org/concepts/profile/profile_creation — “a `times.json` containing a timestamp of the current time is stored inside that profile directory”. This resolves the individual Firefox file as RECORD despite its execute bits.\n\n')
 f.write('https://github.com/containers/crun/blob/main/src/libcrun/seccomp.c — `#define SECCOMP_CACHE_DIR ".cache/seccomp"`. https://github.com/containers/crun/blob/main/crun.1.md — “Path to the file that will contain the container process PID.” These identify the two volatile files; filesystem persistence is runtime and the native crun executable has unchanged integrity.\n\n')
 f.write('https://www.gnu.org/software/grub/manual/grub/grub.html — “The sole function of `boot.img` is to read the first sector of the core image from a local disk and jump to it.” Documentation identifies boot code, but does not establish the actual history of each local copy.\n\n')
 for rid,d,s,what,basis,why in decisions:
  if d not in ['INSTALLED-PACKAGE']:f.write(f'- {rid}: {d}. {what} {why}\n')
print('Individual files:',collections.Counter(x[1] for x in decisions))

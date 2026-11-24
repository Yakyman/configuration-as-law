#!/usr/bin/python3
import hashlib,json,shutil,sys
from pathlib import Path
root=Path.cwd();work=root/'libperl-guest-private';out=root/'records/libperl-guest-private'
assert not out.exists();out.mkdir()
retained=root/'interpreter-inputs/libperl-private/original'
retained.mkdir(exist_ok=True)
for p in (work/'disk.work/apt/archives').glob('libperl5.40_*.deb'):shutil.copyfile(p,retained/p.name)
library=work/'original/usr/lib/x86_64-linux-gnu/libperl.so.5.40.1'
if library.exists():shutil.copyfile(library,retained/library.name)
for pattern in ('*.json','*-dynamic.txt','*-symbols.txt','*-versions.txt'):
 for p in work.glob(pattern):shutil.copyfile(p,out/p.name)
for name in ('declaration.conf','probe.py'):
 p=work/'inputs'/name
 if p.exists():shutil.copyfile(p,out/name)
for name in ('libperl-guest-private.log','libperl-guest-private.serial'):
 p=root/'logs'/name
 if p.exists():(out/name).write_text(p.read_text(errors='replace').replace(str(root),'REMOTE_BUILD'))
(out/'result.json').write_text(json.dumps({'exit_status':int(sys.argv[1]),'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()}},indent=2)+'\n')
if work.exists():shutil.rmtree(work)
print('PRIVATE LIBPERL GUEST SCRATCH REMOVED')

#!/usr/bin/python3
"""Compose47 by adding exactly one tested override to sealed46 readers."""
import gzip,hashlib,json,os,subprocess as sp,tarfile,tempfile
from pathlib import Path
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert Path('VERSION').read_text()=='0.47\n'
metadata=Path('interpreter-inputs/libperl-private/metadata.json');meta=json.loads(metadata.read_text())
for group in ('source_inputs','recipes','retained','guest_evidence'):
 for item in meta[group]:assert digest(item['path'])==item['sha256'],item['path']
assert digest(meta['candidate_path'])==meta['sha256']=='9055c106dbe1ab867bb2832956a558c3e1d51f2918581c6e192f978a806df3c8'
baseline=Path('packages/confos-code-readers_0.46_amd64.deb');target=Path('packages/confos-code-readers_0.47_amd64.deb');assert not target.exists()
with tarfile.open('releases/confos-0.46-source.tar.gz') as tar:assert tar.extractfile(str(baseline)).read()==baseline.read_bytes()
def inventory(root):return {str(p.relative_to(root)):(p.lstat().st_mode,os.readlink(p) if p.is_symlink() else digest(p) if p.is_file() else None) for p in root.rglob('*')}
entry={k:meta[k] for k in ('package','source_version','target','mode','sha256','original_sha256')};entry['payload']='native47-libperl.gz'
with tempfile.TemporaryDirectory(dir='packages') as tmp:
 root=Path(tmp)/'root';sp.run(['dpkg-deb','-R',str(baseline),str(root)],check=True);before=inventory(root)
 control=root/'DEBIAN/control';old=control.read_text();assert old.count('Version: 0.46\n')==1;control.write_text(old.replace('Version: 0.46\n','Version: 0.47\n'))
 directory=root/'usr/lib/confos/reader-overrides';manifest=directory/'manifest.json';inherited=json.loads(manifest.read_text())
 assert not any(e['target']==entry['target'] for e in inherited)
 (directory/entry['payload']).write_bytes(gzip.compress(Path(meta['candidate_path']).read_bytes(),mtime=1795392000))
 manifest.write_text(json.dumps(inherited+[entry],sort_keys=True,indent=2)+'\n')
 after=inventory(root);changed={'DEBIAN/control','usr/lib/confos/reader-overrides/manifest.json'}
 assert all(after[k]==v for k,v in before.items() if k not in changed)
 assert set(after)-set(before)=={'usr/lib/confos/reader-overrides/'+entry['payload']}
 for p in [*root.rglob('*'),root]:os.utime(p,(1795392000,1795392000),follow_symlinks=False)
 sp.run(['dpkg-deb','--root-owner-group','-Zxz','-z6','--build',str(root),str(target)],check=True,env={**os.environ,'SOURCE_DATE_EPOCH':'1795392000'})
 check=Path(tmp)/'check';sp.run(['dpkg-deb','-R',str(target),str(check)],check=True);assert inventory(check)==after
target.with_suffix('.deb.sha256').write_text(digest(target)+'\n')
Path('records/reader-inheritance-0.47.json').write_text(json.dumps({'baseline_sha256':digest(baseline),'component_sha256':digest(target),'unchanged_entries':len(before)-2,'new_entry':entry,'metadata_sha256':digest(metadata)},indent=2)+'\n')
print('NATIVE47 INHERITED BYTES MODES LINKS AND EXACT LIBPERL EXTENSION PASS')

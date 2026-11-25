#!/usr/bin/python3
"""Repackage sealed54 readers with only the component version changed."""
import hashlib,json,os,subprocess as sp,tarfile,tempfile
from pathlib import Path
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
baseline=Path('packages/confos-code-readers_0.54_amd64.deb')
target=Path('packages/confos-code-readers_0.55_amd64.deb')
assert not target.exists()
with tarfile.open('releases/confos-0.54-source.tar.gz') as tar:assert tar.extractfile(str(baseline)).read()==baseline.read_bytes()
def inventory(root):
 return {str(p.relative_to(root)):(p.lstat().st_mode,os.readlink(p) if p.is_symlink() else digest(p) if p.is_file() else None) for p in root.rglob('*')}
with tempfile.TemporaryDirectory(dir='packages') as tmp:
 root=Path(tmp)/'root';sp.run(['dpkg-deb','-R',str(baseline),str(root)],check=True)
 before=inventory(root);control=root/'DEBIAN/control';old=control.read_text()
 assert old.count('Version: 0.54\n')==1;control.write_text(old.replace('Version: 0.54\n','Version: 0.55\n'))
 after=inventory(root);assert before.keys()==after.keys()
 assert all(before[k]==after[k] for k in before if k!='DEBIAN/control')
 for p in [*root.rglob('*'),root]:os.utime(p,(1795392000,1795392000),follow_symlinks=False)
 sp.run(['dpkg-deb','--root-owner-group','-Zxz','-z6','--build',str(root),str(target)],check=True,env={**os.environ,'SOURCE_DATE_EPOCH':'1795392000'})
 check=Path(tmp)/'check';sp.run(['dpkg-deb','-R',str(target),str(check)],check=True);assert inventory(check)==after
target.with_suffix('.deb.sha256').write_text(digest(target)+'\n')
Path('records/reader-inheritance-0.55.json').write_text(json.dumps({'baseline_sha256':digest(baseline),'component_sha256':digest(target),'unchanged_entries':len(before)-1},indent=2)+'\n')
print('NATIVE55 INHERITED BYTES MODES LINKS PASS')

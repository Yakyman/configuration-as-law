#!/usr/bin/python3
"""Reversion sealed39 byte-for-byte payload; rebuild runtime from edited source."""
from pathlib import Path
import hashlib, os, subprocess as sp, tarfile, tempfile
assert Path('VERSION').read_text()=='0.40\n'
baseline=Path('packages/confos-code-readers_0.39_amd64.deb')
with tarfile.open('releases/confos-0.39-source.tar.gz') as tar:
    assert tar.extractfile(str(baseline)).read()==baseline.read_bytes()
with tempfile.TemporaryDirectory(prefix='radio-reader-',dir='packages') as temporary:
    root=Path(temporary)/'root'
    sp.run(['dpkg-deb','-R',str(baseline),str(root)],check=True)
    control=root/'DEBIAN/control';text=control.read_text()
    assert text.count('Version: 0.39\n')==1
    control.write_text(text.replace('Version: 0.39\n','Version: 0.40\n'))
    for path in sorted(root.rglob('*'),reverse=True): os.utime(path,(1795392000,1795392000),follow_symlinks=False)
    os.utime(root,(1795392000,1795392000))
    target=Path('packages/confos-code-readers_0.40_amd64.deb')
    sp.run(['dpkg-deb','--root-owner-group','-Zxz','-z6','--build',str(root),str(target)],check=True,env={**os.environ,'SOURCE_DATE_EPOCH':'1795392000'})
    Path(str(target)+'.sha256').write_text(hashlib.sha256(target.read_bytes()).hexdigest()+'\n')
sp.run(['python3','package-base.py','packages/confos-runtime_0.40_all.deb'],check=True)
sp.run(['python3','check-runtime-source-package.py','0.40'],check=True)

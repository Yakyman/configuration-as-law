#!/usr/bin/python3
"""Compose original32 reader data with native BusyBox vi startup checks."""
from pathlib import Path
import hashlib
import os
import subprocess
import sys
import tempfile

version = sys.argv[1]
baseline = Path('packages/confos-code-readers_0.32_amd64.deb')
assert hashlib.sha256(baseline.read_bytes()).hexdigest() == '2eb0118ebd295c80407a287cdfeea660afbcf22c015f5b5a1811156c6d2f864e'
output = Path(f'packages/confos-code-readers_{version}_amd64.deb').resolve()
epoch = 1795392000
with tempfile.TemporaryDirectory(prefix='vi-readers-', dir=output.parent) as temporary:
    root = Path(temporary)/'root'
    subprocess.run(['dpkg-deb', '-R', baseline, root], check=True)
    (root/'usr/bin/busybox').write_bytes(Path('interpreter-inputs/busybox-vi/busybox').read_bytes())
    (root/'usr/bin/busybox').chmod(0o755)
    docs = root/'usr/share/doc/confos-code-readers'
    for name in ('patch-busybox-vi.py', 'build-busybox-vi.sh', 'package-busybox-vi-readers.py'):
        (docs/name).write_bytes(Path(name).read_bytes())
    control = root/'DEBIAN/control'
    text = control.read_text()
    assert 'Version: 0.32\n' in text
    control.write_text(text.replace('Version: 0.32\n', 'Version: '+version+'\n'))
    for path in [*root.rglob('*'), root]:
        if path.is_dir(): path.chmod(0o755)
        elif not path.is_symlink() and not path.stat().st_mode & 0o111: path.chmod(0o644)
        os.utime(path, (epoch, epoch), follow_symlinks=False)
    artifact = Path(temporary)/'payload.deb'
    subprocess.run(['dpkg-deb', '--root-owner-group', '--uniform-compression', '-Zgzip', '-z9', '--build', root, artifact],
                   check=True, env=dict(os.environ, SOURCE_DATE_EPOCH=str(epoch), TZ='UTC', LC_ALL='C'))
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    os.replace(artifact, output)
    output.with_suffix('.deb.sha256').write_text(digest+'\n')
    print(digest, output.name)

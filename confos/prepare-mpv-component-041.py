#!/usr/bin/python3
"""Promote only a verified private JS+Lua component; rebuild matching runtime."""
import hashlib
from pathlib import Path
import shutil
import subprocess

assert Path('VERSION').read_text() == '0.41\n'
draft = Path('interpreter-inputs/flatpak-mpv-js-integration41-draft')
package = draft/'confos-code-readers_0.41_amd64.deb'
if not package.exists():
    subprocess.run(['python3', str(draft/'prepare-component.py')], check=True)
subprocess.run(['python3', str(draft/'verify-component.py')], check=True)
assert (draft/'source/flatpak_readers.py').read_bytes() == Path('flatpak_readers.py').read_bytes()
digest = hashlib.sha256(package.read_bytes()).hexdigest()
assert package.with_suffix('.deb.sha256').read_text().strip() == digest
target = Path('packages')/package.name
assert not target.exists(), 'inspect previous promotion instead of overwriting'
shutil.copyfile(package, target)
Path(str(target)+'.sha256').write_text(digest+'\n')
subprocess.run(['python3', 'package-base.py', 'packages/confos-runtime_0.41_all.deb'], check=True)
subprocess.run(['python3', 'check-runtime-source-package.py', '0.41'], check=True)
print('VERIFIED PRIVATE MPV41 COMPONENT PROMOTED')

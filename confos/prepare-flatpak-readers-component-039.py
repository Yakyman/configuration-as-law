#!/usr/bin/python3
"""Compose from the actual sealed38 component, then rebuild the runtime."""
from pathlib import Path
import hashlib, subprocess, tarfile
assert Path('VERSION').read_text().strip()=='0.39'
baseline=Path('packages/confos-code-readers_0.38_amd64.deb')
with tarfile.open('releases/confos-0.38-source.tar.gz') as tar:
    expected=hashlib.sha256(tar.extractfile(str(baseline)).read()).hexdigest()
assert hashlib.sha256(baseline.read_bytes()).hexdigest()==expected
subprocess.run(['python3','package-flatpak-reader-overrides.py','0.39',str(baseline),expected,'flatpak-reader-candidate-manifest.json','packages/confos-code-readers_0.39_amd64.deb'],check=True)
subprocess.run(['python3','package-base.py','packages/confos-runtime_0.39_all.deb'],check=True)
subprocess.run(['python3','check-runtime-source-package.py','0.39'],check=True)
subprocess.run(['python3','check-flatpak-readers-inheritance.py'],check=True)

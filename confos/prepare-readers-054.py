#!/usr/bin/python3
"""Reader component of 0.54: the sealed component of 0.53 plus the guard of the office suite's
Basic interpreter (package-basic-guard.py checks that every other entry keeps bytes, mode and link)."""
import hashlib
import json
import subprocess
import tarfile
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


baseline = Path('packages/confos-code-readers_0.53_amd64.deb')
target = Path('packages/confos-code-readers_0.54_amd64.deb')
assert not target.exists()
with tarfile.open('releases/confos-0.53-source.tar.gz') as tar:
    assert tar.extractfile(str(baseline)).read() == baseline.read_bytes()
subprocess.run(['python3', 'package-basic-guard.py', '0.54', str(baseline), 'basic-library-inputs', str(target)], check=True)

Path('records/reader-inheritance-0.54.json').write_text(json.dumps(
    {'baseline_sha256': digest(baseline), 'component_sha256': digest(target),
     'added': ['usr/lib/confos/reader-overrides/libmergedlo.so.gz', 'one record of reader-overrides/manifest.json',
               'five files of usr/share/doc/confos-code-readers']}, indent=2)+'\n')
print('NATIVE54 INHERITED ENTRIES UNCHANGED, BASIC GUARD ADDED PASS')

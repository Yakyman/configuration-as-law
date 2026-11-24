#!/usr/bin/python3
"""Reject stale runtime packages before sealing a source release."""
import hashlib
from pathlib import Path
import runpy
import subprocess
import sys
import tarfile

here = Path(__file__).resolve().parent
version = (here / 'VERSION').read_text().strip()
if len(sys.argv) != 2 or sys.argv[1] != version:
    raise SystemExit('usage: check-runtime-source-package.py CURRENT_VERSION')
package = here / 'packages' / f'confos-runtime_{version}_all.deb'
expected = {
    'usr/lib/confos/' + name: (here / name).read_bytes()
    for name in runpy.run_path(str(here / 'package-base.py'))['RUNTIME']
}
for lock in sorted((here / 'components').glob('*Z.txt')):
    expected['usr/lib/confos/components/' + lock.name] = lock.read_bytes()
seen = set()
process = subprocess.Popen(['dpkg-deb', '--fsys-tarfile', str(package)], stdout=subprocess.PIPE)
try:
    with tarfile.open(fileobj=process.stdout, mode='r|') as archive:
        for member in archive:
            name = member.name.removeprefix('./')
            if name not in expected:
                continue
            if name in seen or not member.isfile():
                raise ValueError('duplicate or non-file runtime member: ' + name)
            actual = archive.extractfile(member).read()
            if actual != expected[name]:
                raise ValueError('stale runtime package member: ' + name)
            seen.add(name)
            print(hashlib.sha256(actual).hexdigest(), name)
    if process.wait() != 0:
        raise ValueError('dpkg-deb extraction failed')
    missing = expected.keys() - seen
    if missing:
        raise ValueError('missing runtime package members: ' + ', '.join(sorted(missing)))
finally:
    process.stdout.close()
    if process.poll() is None:
        process.terminate()
        process.wait()
print(f'RUNTIME SOURCE PACKAGE MATCH {version}: {len(seen)} files')

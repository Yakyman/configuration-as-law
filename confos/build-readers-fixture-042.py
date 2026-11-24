#!/usr/bin/python3
"""Future canonical42 fixture composed from exact private positive inputs."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess as sp
import tarfile

assert Path('VERSION').read_text() == '0.42\n'
work = Path('readers-042-fixture')
assert not work.exists()
shutil.copytree('examples', work)
rows = (work/'development.conf').read_text().splitlines()
with tarfile.open('pdb-gyp-evidence.tar.gz') as tar:
    declaration = tar.extractfile('pdb-gyp-evidence/inputs/declaration.conf').read().decode()
    for row in declaration.splitlines():
        if row.startswith('package '):
            rows.append(row)
        elif row.startswith('file '):
            parts = row.split()
            data = tar.extractfile('pdb-gyp-evidence/inputs/'+parts[-1]).read()
            assert hashlib.sha256(data).hexdigest() == parts[-2]
            name = 'pdb-'+parts[-1]
            (work/name).write_bytes(data)
            rows.append(' '.join(parts[:-1]+[name]))
curl = Path('curl-config-guest-draft-evidence/inputs')
for row in (curl/'declaration.conf').read_text().splitlines():
    if row.startswith('package '):
        rows.append(row)
    elif row.startswith('file '):
        parts = row.split()
        data = (curl/parts[-1]).read_bytes()
        assert hashlib.sha256(data).hexdigest() == parts[-2]
        name = 'curl-'+parts[-1]
        (work/name).write_bytes(data)
        rows.append(' '.join(parts[:-1]+[name]))
(work/'declaration.conf').write_text('\n'.join(rows)+'\n')
sp.run(['bash', 'build.sh', str(work/'declaration.conf'), 'images/readers-042.qcow2'], check=True)
root = Path('images/readers-042.work/root')
for source, target in (
    ('pdb-gyp-patched-draft/pdb.py', 'usr/lib/python3.13/pdb.py'),
    ('pdb-gyp-patched-draft/gyp-input.py', 'usr/lib/python3/dist-packages/gyp/input.py'),
    ('interpreter-inputs/curl-config-draft/candidate/curl', 'usr/bin/curl')):
    assert Path(source).read_bytes() == (root/target).read_bytes()
for relative, name in (('usr/lib/python3.13/__pycache__', 'pdb'),
                       ('usr/lib/python3/dist-packages/gyp/__pycache__', 'input')):
    assert not list((root/relative).glob(name+'.*.pyc')), 'stale original module cache'
for name, expected in json.loads((curl/'libraries.json').read_text()).items():
    assert hashlib.sha256((root/'usr/lib/x86_64-linux-gnu'/name).read_bytes()).hexdigest() == expected, name
print('NATIVE42 FIXTURE EXACT READERS LIBRARIES NO STALE BYTECODE PASS')

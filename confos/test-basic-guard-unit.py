#!/usr/bin/python3
"""Builder check without a machine: what optional_readers.apply does with the record of the
office suite's core library for each pinned release and for a release that is not listed.

Usage: test-basic-guard-unit.py READERS.deb INPUT_DIR
READERS.deb is the reader component with the record; INPUT_DIR the output of fetch-basic-library.py.
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import optional_readers  # noqa: E402

component, inputs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
located = json.loads((HERE/'basic-guard.json').read_text())
pinned = json.loads((HERE/'basic-guard-inputs.json').read_text())
target = pinned['target'].lstrip('/')
with tempfile.TemporaryDirectory(prefix='basic-guard-unit-', dir=inputs) as temp_name:
    temp = Path(temp_name)
    subprocess.run(['dpkg-deb', '-x', str(component), str(temp/'component')], check=True)
    for release in sorted(located)+['unlisted']:
        root = temp/'root'
        if root.exists():
            shutil.rmtree(root)
        shutil.copytree(temp/'component', root, symlinks=True)
        (root/target).parent.mkdir(parents=True)
        if release == 'unlisted':
            (root/target).write_bytes(b'another build of the library\n')
        else:
            shutil.copyfile(inputs/re.sub(r'[^A-Za-z0-9.+~-]', '_', release)/'libmergedlo.so', root/target)
        try:
            optional_readers.apply(root, {pinned['package']})
        except ValueError as error:
            assert release == 'unlisted', (release, error)
            print('unlisted release: refused:', error)
            continue
        assert release != 'unlisted'
        result = hashlib.sha256((root/target).read_bytes()).hexdigest()
        assert result == located[release]['sha256'], release
        data = (root/target).read_bytes()
        offset = located[release]['offset']
        assert data[offset-4:offset+3].hex() == 'f30f1efa31c0c3', release
        print(release, 'guarded file', result, 'payload' if release == pinned['payload_release'] else 'in place')
    # Without the suite's package the record changes nothing.
    root = temp/'root'
    shutil.rmtree(root)
    shutil.copytree(temp/'component', root, symlinks=True)
    optional_readers.apply(root, set())
    assert not (root/target).exists()
print('BASIC GUARD UNIT PASS')

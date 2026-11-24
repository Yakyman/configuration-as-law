#!/usr/bin/python3
"""Independently compare42 component against41, including modes and links."""
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess as sp
import tempfile

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
report = json.loads(Path('records/reader-inheritance-0.42.json').read_text())
with tempfile.TemporaryDirectory(prefix='confos-readers42-check-') as temp:
    roots = []
    for version, field in [('0.41', 'baseline_sha256'), ('0.42', 'component_sha256')]:
        package = Path('packages/confos-code-readers_'+version+'_amd64.deb')
        assert digest(package) == report[field]
        root = Path(temp)/version; roots.append(root)
        sp.run(['dpkg-deb', '-R', str(package), str(root)], check=True)
    old, new = roots
    manifest = 'usr/lib/confos/reader-overrides/manifest.json'
    inherited = json.loads((old/manifest).read_text())
    entries = json.loads((new/manifest).read_text())
    assert entries == inherited+report['new_entries']
    assert len(inherited) == report['unchanged_inherited_entries']
    old_names = set()
    for path in old.rglob('*'):
        name = path.relative_to(old); old_names.add(str(name)); other = new/name
        assert path.lstat().st_mode == other.lstat().st_mode, name
        if str(name) in ('DEBIAN/control', manifest):
            continue
        if path.is_symlink():
            assert os.readlink(path) == os.readlink(other), name
        elif path.is_file():
            assert path.read_bytes() == other.read_bytes(), name
    expected_new = set()
    for entry in report['new_entries']:
        name = 'usr/lib/confos/reader-overrides/'+entry['payload']
        expected_new.add(name)
        data = gzip.decompress((new/name).read_bytes())
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
        assert len(entry['original_sha256']) == 64
    assert {str(path.relative_to(new)) for path in new.rglob('*')} - old_names == expected_new
    assert (old/'DEBIAN/control').read_text().replace('Version: 0.41\n', 'Version: 0.42\n') == (new/'DEBIAN/control').read_text()
print('NATIVE42 INHERITED FILE BYTES MODES LINKS AND EXACT MANIFEST EXTENSION PASS')

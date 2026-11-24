#!/usr/bin/python3
"""Independently compare44 component against43, including modes and links."""
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess as sp
import tempfile

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
assert Path('VERSION').read_text() == '0.44\n'
report = json.loads(Path('records/reader-inheritance-0.44.json').read_text())
with tempfile.TemporaryDirectory(prefix='confos-readers44-check-') as temp:
    roots = []
    for version, field in [('0.43', 'baseline_sha256'), ('0.44', 'component_sha256')]:
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
    assert len(report['new_entries']) == 1
    ed = json.loads(Path('interpreter-inputs/ssh-reader-draft/metadata.json').read_text())
    entry = report['new_entries'][0]
    for key in ('package','source_version','target','mode','sha256','original_sha256'):
        assert entry[key] == ed[key], key
    assert digest(Path(ed['candidate_path'])) == entry['sha256']
    expected_new = set()
    for entry in report['new_entries']:
        name = 'usr/lib/confos/reader-overrides/'+entry['payload']
        expected_new.add(name)
        data = gzip.decompress((new/name).read_bytes())
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
        assert len(entry['original_sha256']) == 64
    assert {str(path.relative_to(new)) for path in new.rglob('*')} - old_names == expected_new
    assert (old/'DEBIAN/control').read_text().replace('Version: 0.43\n', 'Version: 0.44\n') == (new/'DEBIAN/control').read_text()
print('NATIVE44 INHERITED FILE BYTES MODES LINKS AND EXACT MANIFEST EXTENSION PASS')

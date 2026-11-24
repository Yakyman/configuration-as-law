#!/usr/bin/python3
"""Future42 only: extend sealed41 component with exact proven native candidates."""
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess as sp
import tarfile
import tempfile

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert Path('VERSION').read_text() == '0.42\n'
assert '\n73.' in Path('REQUESTS.md').read_text(), 'sealed41 handoff required'
archive = Path('releases/confos-0.41-source.tar.gz')
assert [digest(archive), str(archive)] in [line.split() for line in Path('releases/release-0.41.sha256').read_text().splitlines()]
baseline = Path('packages/confos-code-readers_0.41_amd64.deb')
with tarfile.open(archive) as tar:
    assert tar.extractfile(str(baseline)).read() == baseline.read_bytes()
assert digest(Path('pdb-gyp-evidence.tar.gz')) == '58eb67c7cea6ac2cad860994017e7619aca58f10f189e3b8ebd6a6d8c5e0d8a5'
sp.run(['python3', 'verify-curl-config-metadata-draft.py'], check=True)
curl = json.loads(Path('curl-config-metadata-draft.json').read_text())
items = [
    dict(package='libpython3.13-stdlib', source_version='3.13.5-2+deb13u5',
         target='/usr/lib/python3.13/pdb.py', source='pdb-gyp-patched-draft/pdb.py',
         original_sha256='8c200bf9066bb6baeac7bdb174db4d3a354ed0bff8c947b022e72566084cdb70', mode=0o644),
    dict(package='gyp', source_version='0.16.2-2',
         target='/usr/lib/python3/dist-packages/gyp/input.py', source='pdb-gyp-patched-draft/gyp-input.py',
         original_sha256='524dbc9400ef166fa74919c4872ba73d35f64ccebce13fae1b97f3b0576251da', mode=0o644),
    {key: curl[key] for key in ('package', 'source_version', 'target', 'original_sha256', 'mode')}
]
items[-1]['source'] = curl['candidate_path']
# Match actual private tested module bytes, not only their filenames.
with tarfile.open('pdb-gyp-evidence.tar.gz') as tar:
    for item in items[:2]:
        assert tar.extractfile('pdb-gyp-evidence/'+item['source']).read() == Path(item['source']).read_bytes()
target = Path('packages/confos-code-readers_0.42_amd64.deb')
assert not target.exists(), 'inspect prior promotion; never overwrite'
epoch = 1795392000
def inventory(folder):
    result = {}
    for path in folder.rglob('*'):
        key = str(path.relative_to(folder))
        st = path.lstat()
        result[key] = (st.st_mode, os.readlink(path) if path.is_symlink() else digest(path) if path.is_file() else None)
    return result

with tempfile.TemporaryDirectory(prefix='readers42-', dir='packages') as temp:
    stage = Path(temp)/'component'
    sp.run(['dpkg-deb', '-R', str(baseline), str(stage)], check=True)
    before = inventory(stage)
    control = stage/'DEBIAN/control'
    text = control.read_text()
    assert text.count('Version: 0.41\n') == 1
    control.write_text(text.replace('Version: 0.41\n', 'Version: 0.42\n'))
    directory = stage/'usr/lib/confos/reader-overrides'
    manifest = directory/'manifest.json'
    inherited = json.loads(manifest.read_text())
    additions = []
    for item in items:
        assert not any(old['target'] == item['target'] for old in inherited)
        data = Path(item['source']).read_bytes()
        entry = {key: value for key, value in item.items() if key != 'source'}
        entry.update(payload='native42-'+item['package']+'.gz', sha256=hashlib.sha256(data).hexdigest())
        destination = directory/entry['payload']
        assert not destination.exists()
        destination.write_bytes(gzip.compress(data, mtime=epoch))
        destination.chmod(0o644)
        additions.append(entry)
    manifest.write_text(json.dumps(inherited+additions, sort_keys=True, indent=2)+'\n')
    after = inventory(stage)
    allowed = {'DEBIAN/control', 'usr/lib/confos/reader-overrides/manifest.json'}
    assert all(after[name] == value for name, value in before.items() if name not in allowed)
    assert json.loads(manifest.read_text())[:len(inherited)] == inherited
    for path in [*stage.rglob('*'), stage]:
        os.utime(path, (epoch, epoch), follow_symlinks=False)
    temporary = Path(temp)/target.name
    sp.run(['dpkg-deb', '--root-owner-group', '-Zxz', '-z6', '--build', str(stage), str(temporary)],
           check=True, env={**os.environ, 'SOURCE_DATE_EPOCH': str(epoch)})
    os.link(temporary, target)
target.with_suffix('.deb.sha256').write_text(digest(target)+'\n')
Path('records/reader-inheritance-0.42.json').write_text(json.dumps({
    'baseline_sha256': digest(baseline), 'component_sha256': digest(target),
    'unchanged_inherited_entries': len(inherited), 'new_entries': additions,
    'inherited_bytes_modes_symlinks_preserved': True}, indent=2)+'\n')
sp.run(['python3', 'package-base.py', 'packages/confos-runtime_0.42_all.deb'], check=True)
sp.run(['python3', 'check-runtime-source-package.py', '0.42'], check=True)
print('NATIVE42 EXACT CANDIDATES AND INHERITANCE PASS; GUEST GATES STILL REQUIRED')

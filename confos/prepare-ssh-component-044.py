#!/usr/bin/python3
"""Canonical44 composition: extend exact sealed43 readers with tested SSH."""
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

assert Path('VERSION').read_text() == '0.44\n'
assert '\n75.' in Path('REQUESTS.md').read_text(), 'sealed43 handoff required'
archive = Path('releases/confos-0.43-source.tar.gz')
assert digest(archive) == '5299006ff74ecfa6fcd19b374589aeaf60482ccbe70d704759bdff2f2afcc669'
baseline = Path('packages/confos-code-readers_0.43_amd64.deb')
with tarfile.open(archive) as tar:
    assert tar.extractfile(str(baseline)).read() == baseline.read_bytes()
meta_path = Path('interpreter-inputs/ssh-reader-draft/metadata.json')
assert digest(meta_path) == '0fa9a006b9103f742c8245a1083914036cb89436142cd54bd306b6c39b651099'
ed = json.loads(meta_path.read_text())
for item in ed['inputs'] + ed['licences'] + ed['recipe'] + ed['build_dependencies'] + [ed['reader_policy'],ed['source_patch'],ed['native_comparison'],ed['build_provenance']]:
    assert digest(Path(item['path'])) == item['sha256'], item['path']
assert digest(Path(ed['candidate_path'])) == ed['sha256']
assert digest(Path('interpreter-inputs/ssh-reader-draft/original/usr/bin/ssh')) == ed['original_sha256']
items = [{key: ed[key] for key in ('package', 'source_version', 'target', 'original_sha256', 'mode')}]
items[0]['source'] = ed['candidate_path']
target = Path('packages/confos-code-readers_0.44_amd64.deb')
assert not target.exists(), 'inspect prior promotion; never overwrite'
assert not target.with_suffix('.deb.sha256').exists()
assert not Path('records/reader-inheritance-0.44.json').exists()
epoch = 1795392000
def inventory(folder):
    result = {}
    for path in folder.rglob('*'):
        key = str(path.relative_to(folder))
        st = path.lstat()
        result[key] = (st.st_mode, os.readlink(path) if path.is_symlink() else digest(path) if path.is_file() else None)
    return result

with tempfile.TemporaryDirectory(prefix='readers44-', dir='packages') as temp:
    stage = Path(temp)/'component'
    sp.run(['dpkg-deb', '-R', str(baseline), str(stage)], check=True)
    before = inventory(stage)
    control = stage/'DEBIAN/control'
    text = control.read_text()
    assert text.count('Version: 0.43\n') == 1
    control.write_text(text.replace('Version: 0.43\n', 'Version: 0.44\n'))
    directory = stage/'usr/lib/confos/reader-overrides'
    manifest = directory/'manifest.json'
    inherited = json.loads(manifest.read_text())
    additions = []
    for item in items:
        assert not any(old['target'] == item['target'] for old in inherited)
        data = Path(item['source']).read_bytes()
        entry = {key: value for key, value in item.items() if key != 'source'}
        entry.update(payload='native44-'+item['package']+'.gz', sha256=hashlib.sha256(data).hexdigest())
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
Path('records/reader-inheritance-0.44.json').write_text(json.dumps({
    'baseline_sha256': digest(baseline), 'component_sha256': digest(target),
    'unchanged_inherited_entries': len(inherited), 'new_entries': additions,
    'inherited_bytes_modes_symlinks_preserved': True}, indent=2)+'\n')
print('NATIVE44 EXACT SSH CANDIDATE AND INHERITANCE PASS; GUEST GATES STILL REQUIRED')

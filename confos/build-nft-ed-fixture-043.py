#!/usr/bin/python3
"""Canonical43 fixture with baseline development rows and proven ed inputs."""
import hashlib,json,shutil,subprocess as sp
from pathlib import Path
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
assert Path('VERSION').read_text()=='0.43\n'
sp.run(['python3','check-reader-inheritance-043.py'],check=True)
work=Path('nft-ed-043-fixture');image=Path('images/nft-ed-043.qcow2')
assert not work.exists() and not image.exists() and not Path('images/nft-ed-043.work').exists()
metadata=Path('ed-reader-metadata-draft.json')
assert digest(metadata)=='4b2f8944bc7bcfa3ac82212039ceca6b508f77909ca56ad50faf6158271350e1'
ed=json.loads(metadata.read_text())
inputs=Path('interpreter-inputs/ed-reader-draft/evidence/inputs')
assert digest(inputs/'declaration.conf')=='91401a4968cacd0a36e45a95c5d23490af0008f311bf52744c6ca6072600e37b'
shutil.copytree('examples',work)
rows=(work/'development.conf').read_text().splitlines()
assert rows[0]=='base 0.43'
assert any(row.startswith('file /home/user/bin/recorded.sh ') for row in rows)
for row in (inputs/'declaration.conf').read_text().splitlines():
    if row.startswith('package '):
        assert row=='package ed 1.21.1-1'
        rows.append(row)
    elif row.startswith('file '):
        parts=row.split();data=(inputs/parts[-1]).read_bytes()
        assert hashlib.sha256(data).hexdigest()==parts[-2]
        name='ed-'+parts[-1];assert not (work/name).exists()
        (work/name).write_bytes(data)
        rows.append(' '.join(parts[:-1]+[name]))
assert rows.count('package ed 1.21.1-1')==1
assert (work/'ed-probe.py').read_bytes()==Path('probe-ed-reader-guest-draft.py').read_bytes()
assert digest(work/'ed-original-ed')==ed['original_sha256']
assert json.loads((work/'ed-expected.json').read_text())=={
    'original_sha256':ed['original_sha256'],'sha256':ed['sha256'],'red_sha256':ed['red']['sha256']}
(work/'declaration.conf').write_text('\n'.join(rows)+'\n')
sp.run(['bash','build.sh',str(work/'declaration.conf'),str(image)],check=True)
root=Path('images/nft-ed-043.work/root')
assert digest(root/'usr/bin/ed')==ed['sha256']
assert digest(root/'usr/bin/red')==ed['red']['sha256']
assert not (root/'usr/bin/red').is_symlink()
assert (root/'usr/bin/ed').stat().st_mode&0o7777==ed['mode']
for relative,expected in ed['guest_libraries']['files'].items():
    assert digest(root/relative)==expected,relative
assert digest(Path('images/nft-ed-043.work/apt/archives/ed_1.21.1-1_amd64.deb'))==ed['inputs'][0]['sha256']
print('CANONICAL43 FIXTURE EXACT ED RED ORIGINAL CONTROL AND UNCHANGED LIBRARIES PASS')

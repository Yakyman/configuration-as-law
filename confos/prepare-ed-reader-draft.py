#!/usr/bin/python3
"""Exact cached-index ed inputs, private extraction only."""
import hashlib,json,subprocess,urllib.request
from pathlib import Path
root=Path.cwd();work=root/'interpreter-inputs/ed-reader-draft';work.mkdir(exist_ok=True)
pins={
'ed_1.21.1-1_amd64.deb':'b5498068d8ac54ad004bacbde2223a348fee781f9bb94328b01d8bfcbd179b48',
'ed_1.21.1-1.dsc':'c35f79215fc1039fb00379c9b63dafebf9f9c262b168a006ca657137dbfc41ca',
'ed_1.21.1.orig.tar.gz':'bb88a08496ffbaeca59bda93e5da195ef993522fb74f4fcfbf2619ff39f83b44',
'ed_1.21.1-1.debian.tar.xz':'ba8d3de70c1db8e50c978cf3b60beddf45b0c6c6931989865c20e550696d84ab'}
sources=(root/'interpreter-inputs/git/apt/lists/snapshot.debian.org_archive_debian_20261123T000000Z_dists_trixie_main_source_Sources').read_text()
packages=(root/'interpreter-inputs/git/dependencies/apt/lists/snapshot.debian.org_archive_debian_20261123T000000Z_dists_trixie_main_binary-amd64_Packages').read_text()
for label,index in [('source',sources),('binary',packages)]:
    stanza=next(x for x in index.split('\n\n') if x.startswith('Package: ed\n') and '\nVersion: 1.21.1-1\n' in x)
    (work/(label+'-index.txt')).write_text(stanza+'\n')
for name,expected in pins.items():
    assert expected in (packages if name.endswith('.deb') else sources)
    path=work/name
    if not path.exists():
        with urllib.request.urlopen('https://snapshot.debian.org/archive/debian/20261123T000000Z/pool/main/e/ed/'+name,timeout=60) as response:data=response.read()
        assert hashlib.sha256(data).hexdigest()==expected
        path.write_bytes(data)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==expected
(work/'input-pins.json').write_text(json.dumps(pins,indent=2)+'\n')
if not (work/'source').exists():subprocess.run(['dpkg-source','--no-check','-x','ed_1.21.1-1.dsc','source'],cwd=work,check=True)
if not (work/'original').exists():subprocess.run(['dpkg-deb','-x',str(work/'ed_1.21.1-1_amd64.deb'),str(work/'original')],check=True)
print('ED_READER_EXACT_INPUTS_VERIFIED')

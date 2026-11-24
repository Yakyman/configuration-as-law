#!/usr/bin/python3
"""Exact cached-index ed inputs, private extraction only."""
import hashlib,json,subprocess,urllib.request
from pathlib import Path
root=Path.cwd();work=root/'interpreter-inputs/ssh-reader-draft';work.mkdir(exist_ok=True)
pins={
'openssh-client_10.0p1-7+deb13u4_amd64.deb':'8fff343654f86c3b3266f94cd338c7b4da2e386da029327815118ea00bce03b9',
'openssh_10.0p1-7+deb13u4.dsc':'73fed3fd77d60925ed342bcb0afd3c037e4ea0d39333107bf617aa90f859910f',
'openssh_10.0p1.orig.tar.gz':'021a2e709a0edf4250b1256bd5a9e500411a90dddabea830ed59cef90eb9d85c',
'openssh_10.0p1.orig.tar.gz.asc':'f71cf3240516ce59c2240532143982fcd97e2e286e6eb1eb6c3080a1ec012a04',
'openssh_10.0p1-7+deb13u4.debian.tar.xz':'102e1065030c6002acabd7f896eeba1462bf54b4d7393bac34b0308312868ec6'}
sources=(root/'interpreter-inputs/git/apt/lists/snapshot.debian.org_archive_debian_20261123T000000Z_dists_trixie_main_source_Sources').read_text()
packages=(root/'interpreter-inputs/git/dependencies/apt/lists/snapshot.debian.org_archive_debian_20261123T000000Z_dists_trixie_main_binary-amd64_Packages').read_text()
for label,index in [('source',sources),('binary',packages)]:
    stanza=next(x for x in index.split('\n\n') if x.startswith('Package: '+('openssh' if label=='source' else 'openssh-client')+'\n') and '\nVersion: 1:10.0p1-7+deb13u4\n' in x)
    (work/(label+'-index.txt')).write_text(stanza+'\n')
for name,expected in pins.items():
    assert expected in (packages if name.endswith('.deb') else sources)
    path=work/name
    if not path.exists():
        with urllib.request.urlopen('https://snapshot.debian.org/archive/debian/20261123T000000Z/pool/main/o/openssh/'+name,timeout=60) as response:data=response.read()
        assert hashlib.sha256(data).hexdigest()==expected
        path.write_bytes(data)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==expected
(work/'input-pins.json').write_text(json.dumps(pins,indent=2)+'\n')
if not (work/'source').exists():subprocess.run(['dpkg-source','--no-check','-x','openssh_10.0p1-7+deb13u4.dsc','source'],cwd=work,check=True)
if not (work/'original').exists():subprocess.run(['dpkg-deb','-x',str(work/'openssh-client_10.0p1-7+deb13u4_amd64.deb'),str(work/'original')],check=True)
print('SSH_READER_EXACT_INPUTS_VERIFIED')

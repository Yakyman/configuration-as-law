#!/usr/bin/python3
"""Preserve portable private curl evidence and remove only its build tree."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

root=Path.cwd();work=root/'interpreter-inputs/curl-config-draft';publish=work/'publish'
assert 'CURL_CONFIG_NATIVE_COMPARISON_AND_CONTROLS_PASS' in (work/'controls.log').read_text()
assert hashlib.sha256((work/'candidate/curl').read_bytes()).hexdigest()=='cf221d19c07407cc275bd2653bbf8417283d383a46e0a9d5824cfeae3e792095'
publish.mkdir(exist_ok=True)
for path in (root/'interpreter-inputs/git/dependencies/apt/archives').glob('*.deb'):
    destination=work/'dependency-archives'/path.name
    if not destination.exists(): shutil.copyfile(path,destination)
for name in ['build.log','controls.log','input-provenance.json','reader-provenance.json','build-provenance.json',
             'comparison-controls.json','original-version.txt','candidate-version.txt','original-dynamic.txt',
             'candidate-dynamic.txt','curl-config-reader.patch']:
    (publish/name).write_text((work/name).read_text().replace(str(root),'<build>'))
tree=work/'build-tree'
for relative in ['config.log','config.status','lib/curl_config.h','src/Makefile']:
    path=tree/relative
    if path.exists():
        (publish/relative.replace('/','-')).write_text(path.read_text().replace(str(root),'<build>'))
toolchain=subprocess.check_output(['dpkg-query','-W','-f=${binary:Package}\t${Version}\n',
    'gcc','gcc-14','binutils','libc6-dev','libc6','autoconf','automake','libtool','make','dpkg-dev'],text=True)
(publish/'host-toolchain-packages.txt').write_text(toolchain)
inputs={}
paths=[*work.glob('*.dsc'),*work.glob('*.tar.*'),*work.glob('*.deb'),
       *work.joinpath('source').rglob('*'),*work.joinpath('dependencies').rglob('*'),
       *work.joinpath('dependency-archives').glob('*.deb'),*work.joinpath('patched').rglob('*'),
       *work.joinpath('candidate').glob('*'),*root.glob('*curl-config*draft.py')]
for path in sorted(set(paths)):
    key=str(path.relative_to(root))
    if path.is_symlink(): inputs[key]={'symlink':str(path.readlink())}
    elif path.is_file(): inputs[key]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
(publish/'complete-input-checksums.json').write_text(json.dumps(inputs,indent=2,sort_keys=True)+'\n')
(publish/'evidence-sha256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted(publish.iterdir()) if p.is_file() and p.name!='evidence-sha256.json'},indent=2)+'\n')
assert tree==root/'interpreter-inputs/curl-config-draft/build-tree'
if tree.exists(): shutil.rmtree(tree)
print('CURL_CONFIG_EVIDENCE_PRESERVED_AND_PRIVATE_BUILD_TREE_REMOVED',len(inputs))

#!/usr/bin/python3
"""Compare sealed38 payload against39; permit only exact new reader paths."""
import gzip,hashlib,json,subprocess,tarfile
from pathlib import Path

def contents(path):
    p=subprocess.Popen(['dpkg-deb','--fsys-tarfile',str(path)],stdout=subprocess.PIPE)
    entries={}; data={}
    with tarfile.open(fileobj=p.stdout,mode='r|') as tar:
        for item in tar:
            name=item.name.removeprefix('./').rstrip('/')
            raw=tar.extractfile(item).read() if item.isfile() else None
            entries[name]=(item.type,item.mode,item.uid,item.gid,item.linkname,hashlib.sha256(raw).hexdigest() if raw is not None else None)
            if raw is not None: data[name]=raw
    assert p.wait()==0
    return entries,data
old,_=contents('packages/confos-code-readers_0.38_amd64.deb')
new,data=contents('packages/confos-code-readers_0.39_amd64.deb')
for name,value in old.items(): assert new.get(name)==value,name
prefix='usr/lib/confos/flatpak-reader-overrides'
docs='usr/share/doc/confos-code-readers/flatpak'
files=['flatpak-reader-candidate-manifest.json','flatpak-reader-provenance-draft.md','flatpak-python-shared-draft.md','flatpak-bash-compatible-draft.md','patch-flatpak-python.py','patch-python-code.py','patch-flatpak-bash.py','code-file-policy.h','build-flatpak-python-shared.sh','build-flatpak-bash-compatible.sh','link-flatpak-bash-compatible.sh','flatpak_readers.py','package-flatpak-reader-overrides.py']
allowed={prefix,docs,prefix+'/manifest.json',*(prefix+f'/reader-{i}.gz' for i in range(3)),*(docs+'/'+f for f in files),*(docs+'/'+f for f in ['bash-COPYING','python-LICENSE','0001-bash-config.patch','python3-multiarch-include.patch'])}
assert new.keys()-old.keys()==allowed,(new.keys()-old.keys())^allowed
for name in files: assert data[docs+'/'+name]==Path(name).read_bytes(),name
for label,source in [('bash-COPYING','interpreter-inputs/flatpak-bash-compatible/COPYING'),('python-LICENSE','interpreter-inputs/flatpak-python-shared/LICENSE'),('0001-bash-config.patch','interpreter-inputs/flatpak-sdk-provenance/89e0d095f472b2620f985f509b263e2b4d853d5a/patches/bash/0001-bash-config.patch'),('python3-multiarch-include.patch','interpreter-inputs/flatpak-sdk-provenance/89e0d095f472b2620f985f509b263e2b4d853d5a/patches/python3/python3-multiarch-include.patch')]:
    assert data[docs+'/'+label]==Path(source).read_bytes(),label
candidate=json.loads(Path('flatpak-reader-candidate-manifest.json').read_text())
manifest=json.loads(data[prefix+'/manifest.json']); assert len(manifest)==3
for i,(row,original) in enumerate(zip(manifest,candidate['readers'])):
    assert row==dict(ref=candidate['runtime_ref'],commit=candidate['commit'],bundle_sha256=candidate['runtime_bundle_sha256'],target=original['target'].split('/files/',1)[1],original_sha256=original['sha256'],objects=original['object_paths'],payload=f'reader-{i}.gz',sha256=original['candidate_sha256'],mode=0o755)
    assert hashlib.sha256(gzip.decompress(data[prefix+'/'+row['payload']])).hexdigest()==row['sha256']
print('READER38 ALL PAYLOAD INHERITED; EXACT THREE FLATPAK OVERRIDES PASS')

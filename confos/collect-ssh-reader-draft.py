#!/usr/bin/python3
"""Collect exact portable SSH inputs after the private guest gates."""
import hashlib, json, shutil
from pathlib import Path
root=Path.cwd(); work=Path('interpreter-inputs/ssh-reader-draft')
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def item(p): return {'path':str(p),'sha256':digest(p)}
comparison=json.loads((work/'comparison.json').read_text())
for field in ('needed','versions','exports','version','queries'):
 assert comparison['original'][field]==comparison['candidate'][field],field
assert 'SSH_READER_PRIVATE42_PIPELINE_PASS' in (work/'guest-build-run.log').read_text()
assert 'SSH_READER_ROOT_PRIVATE_MATRIX_PASS' in (work/'root-controls.log').read_text()
for name in ('LICENCE','debian/copyright'):
 source=work/'source'/name
 target=work/'licences'/name
 target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
shutil.copyfile(work/'build-tree/confos-ssh-reader-policy.h',work/'confos-ssh-reader-policy.h')
pins=json.loads((work/'input-pins.json').read_text())
for name,sha in pins.items(): assert digest(work/name)==sha
recipes=['prepare-ssh-reader-draft.py','build-ssh-reader-draft.py','build-ssh-reader-guest-draft.py',
 'probe-ssh-reader-guest-draft.py','run-ssh-reader-guest-draft.sh','run-ssh-reader-root-draft.sh',
 'collect-ssh-reader-draft.py','cleanup-ssh-reader-draft.py']
metadata={'package':'openssh-client','source_version':'1:10.0p1-7+deb13u4','target':'/usr/bin/ssh','mode':0o755,
 'sha256':comparison['candidate']['sha256'],'original_sha256':comparison['original']['sha256'],
 'candidate_path':str(work/'candidate/ssh'),'inputs':[item(work/name) for name in pins],
 'build_dependencies':[item(p) for p in sorted((work/'apt/archives').glob('*.deb'))],
 'licences':[item(work/'licences'/name) for name in ('LICENCE','debian/copyright')],
 'recipe':[item(p) for p in recipes],'reader_policy':item(work/'confos-ssh-reader-policy.h'),
 'source_patch':item(work/'ssh-reader.patch'), 'native_comparison':item(work/'comparison.json'),
 'build_provenance':item(work/'build-provenance.json'),
 'observed_gates':['SSH_READER_PRIVATE42_GUEST_MATRIX_PASS 22','SSH_READER_ROOT_PRIVATE_MATRIX_PASS'],
 'limits':'Only observed config-reader routes; automatic user config creation refused by read-only mount; no universal reader closure.'}
assert digest(metadata['candidate_path'])==metadata['sha256']
assert digest(work/'original/usr/bin/ssh')==metadata['original_sha256']
(work/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
print('SSH_READER_PORTABLE_METADATA_PASS',digest(work/'metadata.json'))

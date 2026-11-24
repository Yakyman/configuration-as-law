#!/usr/bin/python3
"""Emit NUL-separated portable SSH inputs; exclude guest disks and keys."""
import hashlib,json,sys
from pathlib import Path
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert Path('VERSION').read_text().strip() in ('0.44','0.45','0.46','0.47','0.48','0.49')
work=Path('interpreter-inputs/ssh-reader-draft');metadata=work/'metadata.json'
assert digest(metadata)=='0fa9a006b9103f742c8245a1083914036cb89436142cd54bd306b6c39b651099'
ssh=json.loads(metadata.read_text())
assert not any((work/name).exists() for name in ('guest','source','build-tree','dependencies'))
assert not list(work.rglob('*.qcow2')) and not list(work.rglob('connection-key*'))
items=ssh['inputs']+ssh['licences']+ssh['recipe']+ssh['build_dependencies']+[ssh['reader_policy'],ssh['source_patch'],ssh['native_comparison'],ssh['build_provenance']]
for item in items: assert digest(item['path'])==item['sha256'],item['path']
assert digest(ssh['candidate_path'])==ssh['sha256']
names=[str(metadata),*[item['path'] for item in items],
 'prepare-ssh-component-044.py','check-reader-inheritance-044.py','ssh-archive-paths-044.py','build-tools-fixture-044.py',
 'SSH-READER-RESULTS.md','packages/confos-code-readers_0.43_amd64.deb','packages/confos-code-readers_0.43_amd64.deb.sha256',
 'records/reader-inheritance-0.44.json']
names += [str(work/name) for name in ('candidate','original','input-pins.json','source-index.txt','binary-index.txt','config.h',
 'original-dynamic.txt','candidate-dynamic.txt','original-symbols.txt','candidate-symbols.txt',
 'final-guest-composition.json','failed-guest-composition.json','fd-fixture-composition.json','auto-fixture-composition.json',
 'build.log','guest-build-run.log','guest-fd-fixture-failure.log','guest-auto-fixture-failure.log','root-controls.log','root-fixture-failure.log')]
for name in dict.fromkeys(names):
 assert Path(name).exists(),name
 sys.stdout.buffer.write(name.encode()+b'\0')

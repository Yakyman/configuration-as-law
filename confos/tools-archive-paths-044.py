#!/usr/bin/python3
import hashlib,json,sys
from pathlib import Path
assert Path('VERSION').read_text().strip() in ('0.44','0.45','0.46','0.47','0.48','0.49')
meta=json.loads(Path('visudo-recording-metadata.json').read_text())
for name,digest in meta['files'].items():
 assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
assert Path('visudo-command').read_bytes()==Path('visudo-recording-command-draft').read_bytes().replace(b'/usr/lib/confos/native/visudo',b'/usr/sbin/visudo')
names=list(meta['files'])+['visudo-command','visudo-recording-metadata.json',
 'collect-visudo-candidate.py','advance-tools-044.py','prepare-tools-probes-044.py',
 'probe-visudo-044.py','ssh-root-controls-044.sh','probe-tools-044.sh','prepare-tools-044.sh',
 'tools-archive-paths-044.py','archive-tools-044.sh','cleanup-tools-044.sh',
 'sync-tools-044.sh','fetch-tools-evidence-044.sh','handoff-tools-044.py',
 'document-tools-044.py','prepare-tools-release-scripts-044.py',
 'visudo-editor-controls-044.py','probe-visudo-editor-044.sh','visudo-editor-fixture-044.py',
 'records/visudo-editor-044-first-failure.log','records/visudo-editor-044-harness-retry.log',
 'records/visudo-editor-044-include-material.log',
 'packages/confos-code-readers_0.43_amd64.deb',
 'packages/confos-code-readers_0.43_amd64.deb.sha256']
for name in dict.fromkeys(names):
 assert Path(name).exists(),name
 sys.stdout.buffer.write(name.encode()+b'\0')

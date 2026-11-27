#!/usr/bin/env python3
"""Local freeze manifest only. Does not publish, upload, commit or run a system."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PUBLIC_TOP=['PROGRAMS.md','PORT.md','port.json','CASES.md','plans.json','FORMATS.md','ASSUMPTIONS.md',
            'QUESTIONS.md','README.md','STATEMENT-LABELS.json','adapter.py','core.py','engine.py','cli.py','casedefs.py',
            'run','derive','inventory','compare','local.env.example','READY.md','SELFTEST.md',
            'BINDING.md','CORRECTIONS.md','adapter_native.py','adapter_disk.py']
files=[ROOT/p for p in PUBLIC_TOP]
for folder in ('declarations','payloads','fixtures','selftest','tools','bindings'):
    files+=sorted(p for p in (ROOT/folder).rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts and p.name not in ('LAST.txt',))
files=sorted(set(files))
lines=[]
for p in files:
    if not p.is_file(): raise SystemExit('missing publication input: '+str(p.relative_to(ROOT)))
    lines.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(ROOT)))
(ROOT/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
(ROOT/'PUBLICATION.txt').write_text('\n'.join(str(p.relative_to(ROOT)) for p in files)+'\nSHA256SUMS\nPUBLICATION.txt\n')
print('Frozen '+str(len(files))+' files; nothing published')

#!/usr/bin/python3
"""Freeze the tested private recorder recipe and its limits for integration."""
import hashlib
import json
from pathlib import Path

log=Path('records/visudo-recording-explicit-removal-private.log').read_text()
assert 'VISUDO RECORDING PRIVATE MATRIX PASS' in log.splitlines()
for stage in ('add','remove'):
    assert 'VISUDO IMMEDIATE POST-APPLIED CUT '+stage in log.splitlines()
names=['visudo-recording-command-draft','visudo-recording-private-build.py',
       'visudo-recording-private-diagnostic.sh','visudo-recording-probe.py',
       'visudo-recording-include-probe.py','VISUDO-RECORDING-DRAFT.md',
       'records/visudo-recording-explicit-removal-private.log',
       'records/visudo-recording-private-final.log',
       'records/visudo-command-before-explicit-removal.txt',
       'records/visudo-probe-before-explicit-removal.py']
items={name:hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in names}
Path('visudo-recording-metadata.json').write_text(json.dumps({
    'sealed_source':'0.41',
    'sealed_source_sha256':'2c73f6a664a2754cc78a7244d31bb77c7ac3d5253f45653a3c12cdfb418e4ca9',
    'files':items,
    'result':'Private matrix passed; canonical release regression still required',
    'limits':['Only one supported sudoers snippet target per request',
              'Native empty edit remains unchanged; --remove explicitly deletes its row',
              'Individual native validation at recording; complete policy validated on apply',
              'Editor stays in confos-session confinement'],
},indent=2)+'\n')
print('VISUDO PRIVATE CANDIDATE INPUTS FROZEN; CANONICAL INTEGRATION PENDING')

#!/usr/bin/python3
"""Repair only the recorded test editor through the fixture declaration."""
import hashlib,shlex
from pathlib import Path
path=Path('/state/declaration.conf')
data=b'#!/bin/sh\ncat /proc/self/attr/current >&2\nfor target; do :; done\ncat > "$target"\n'
digest=hashlib.sha256(data).hexdigest()
source='visudo-editor-044-'+digest
(path.parent/source).write_bytes(data)
lines=path.read_text().splitlines();found=0
for index,line in enumerate(lines):
 row=shlex.split(line,comments=True)
 if row[:2]==['file','/usr/local/bin/visudo-test-editor']:
  lines[index]=shlex.join(['file',row[1],'0755','0:0',digest,source]);found+=1
assert found==1
path.write_text('\n'.join(lines)+'\n')
print('RECORDED TEST EDITOR FIXTURE',digest)

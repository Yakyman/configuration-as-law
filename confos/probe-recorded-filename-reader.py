#!/usr/bin/python3
"""Observe a recorded custom reader separately from native file-API controls."""
import subprocess as sp
from pathlib import Path
assert Path('/proc/self/attr/current').read_text().strip()=='confos-session (enforce)'
before=Path('/state/declaration.conf').read_bytes()
code=Path('/usr/local/share/embedded-recorded.py').read_bytes()
marker=Path('/tmp/embedded-python-marker');count=0
for root in (False,True):
 for route in ('home','tmp','stdin'):
  sp.run(['sudo','-n','rm','-f',str(marker)],check=True)
  saved=Path.home()/'relay-unrecorded.py' if route=='home' else Path('/tmp/relay-unrecorded.py')
  saved.write_bytes(code)
  command=(['sudo','-n'] if root else [])+['python3','/usr/local/share/recorded-filename-reader.py',str(saved) if route!='stdin' else '/proc/self/fd/0']
  with saved.open('rb') as stream:
   result=sp.run(command,stdin=stream if route=='stdin' else sp.DEVNULL,capture_output=True,timeout=20)
  print('RECORDED_FILENAME_READER',root,route,'COMMAND',command,'EXIT',result.returncode,'EXECUTED',marker.exists(),'OUT',repr(result.stdout),'ERR',repr(result.stderr),flush=True)
  assert result.returncode==0 and marker.exists()
  count+=1
sp.run(['sudo','-n','rm','-f',str(marker)],check=True)
assert Path('/state/declaration.conf').read_bytes()==before
print('RECORDED_FILENAME_READER_SAVED_EXECUTION_OBSERVED',count,flush=True)

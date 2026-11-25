#!/usr/bin/python3
import hashlib,os,subprocess as sp
from pathlib import Path
assert Path('/proc/self/attr/current').read_text().strip()=='confos-session (enforce)'
original=Path('/state/declaration.conf').read_bytes()
marker=Path('/tmp/embedded-python-marker')
source=Path('/usr/local/share/embedded-recorded.py')
lib=Path('/usr/lib/x86_64-linux-gnu/libpython3.13.so.1.0')
print('EMBEDDED_LIBRARY_SHA256',hashlib.sha256(lib.read_bytes()).hexdigest(),flush=True)
count=0
for root in (False,True):
 prefix=['sudo','-n'] if root else []
 def clear():sp.run(['sudo','-n','rm','-f',str(marker)],check=True)
 for name in ('recorded','saved-home','saved-tmp','regular-stdin','pipe','typed'):
  clear();code=source.read_bytes();input=None;stdin=None
  if name=='recorded':path=str(source)
  elif name in ('saved-home','saved-tmp'):
   path=str(Path.home()/'embedded-unrecorded.py') if name=='saved-home' else '/tmp/embedded-unrecorded.py'
   Path(path).write_bytes(code)
  else:path='/proc/self/fd/0'
  cmd=prefix+['/usr/local/bin/embedded-python','file',path]
  if name=='regular-stdin':
   Path('/tmp/embedded-unrecorded.py').write_bytes(code);stdin=open('/tmp/embedded-unrecorded.py','rb')
  if name=='pipe':input=code
  if name=='typed':cmd=prefix+['/usr/local/bin/embedded-python','typed',code.decode()]
  result=sp.run(cmd,input=input,stdin=stdin,capture_output=True,timeout=25)
  if stdin:stdin.close()
  print('EMBEDDED_PROBE',root,name,'EXIT',result.returncode,'EXECUTED',marker.exists(),'OUT',repr(result.stdout),'ERR',repr(result.stderr),flush=True)
  if name in ('saved-home','saved-tmp','regular-stdin'):
   assert result.returncode!=0 and not marker.exists(),(root,name)
   assert b'Permission denied' in result.stderr
  else:assert result.returncode==0 and marker.exists(),(root,name)
  if name in ('saved-home','saved-tmp','regular-stdin'):count+=1
 clear()
assert Path('/state/declaration.conf').read_bytes()==original
assert count==6
print('PRIVATE_LIBPYTHON_SAVED_CODE_REFUSED_CONTROLS_PASS',count,flush=True)

#!/usr/bin/python3
import hashlib,subprocess as sp
from pathlib import Path
assert Path('/proc/self/attr/current').read_text().strip()=='confos-session (enforce)'
before=Path('/state/declaration.conf').read_bytes();marker=Path('/tmp/embedded-perl-marker')
source=Path('/usr/local/share/embedded-recorded.pl');code=source.read_bytes()
library=Path('/usr/lib/x86_64-linux-gnu/libperl.so.5.40')
print('EMBEDDED_PERL_LIBRARY_SHA256',hashlib.sha256(library.read_bytes()).hexdigest(),flush=True)
count=0
for root in (False,True):
 for route in ('recorded','home','tmp','stdin','typed','pipe'):
  sp.run(['sudo','-n','rm','-f',str(marker)],check=True)
  saved=Path.home()/'embedded-unrecorded.pl' if route=='home' else Path('/tmp/embedded-unrecorded.pl')
  saved.write_bytes(code)
  args=[str(source)] if route=='recorded' else ['-e',code.decode()] if route=='typed' else ['/proc/self/fd/0'] if route in ('stdin','pipe') else [str(saved)]
  command=(['sudo','-n'] if root else [])+['/usr/local/bin/embedded-perl',*args]
  with saved.open('rb') as stream:
   result=sp.run(command,stdin=stream if route=='stdin' else None,input=code if route=='pipe' else None,capture_output=True,timeout=25)
  print('EMBEDDED_PERL',root,route,'COMMAND',command,'EXIT',result.returncode,'EXECUTED',marker.exists(),'OUT',repr(result.stdout),'ERR',repr(result.stderr),flush=True)
  if route in ('home','tmp','stdin'):
   assert result.returncode!=0 and not marker.exists(),(root,route)
   assert b'Permission denied' in result.stderr
  else:assert result.returncode==0 and marker.exists(),(root,route)
  if route in ('home','tmp','stdin'):count+=1
sp.run(['sudo','-n','rm','-f',str(marker)],check=True)
assert Path('/state/declaration.conf').read_bytes()==before
print('PRIVATE_LIBPERL_SAVED_REFUSALS_AND_CONTROLS_PASS',count,flush=True)

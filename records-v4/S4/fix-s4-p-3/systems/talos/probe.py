import pathlib,json,subprocess as sp,time,shlex,sys
from runner import R,L,D,O,N,run
queries=json.loads(sys.argv[1])
for label,cmd,seconds in queries:
 script='import subprocess as sp,sys,selectors,time,os\n'+f'cmd={cmd!r};limit={seconds};cap=67108864\n'+'''p=sp.Popen(cmd,stdout=sp.PIPE,stderr=sp.PIPE);s=selectors.DefaultSelector();s.register(p.stdout,selectors.EVENT_READ,1);s.register(p.stderr,selectors.EVENT_READ,2);n=0;t=time.monotonic();rc=None
while s.get_map():
 if time.monotonic()-t>limit:rc=124;break
 for k,e in s.select(.1):
  b=os.read(k.fileobj.fileno(),65536)
  if not b:s.unregister(k.fileobj);continue
  n+=len(b)
  if n>cap:rc=125;break
  os.write(k.data,b)
 if rc is not None:break
if rc is not None:p.kill()
x=p.wait();sys.exit(x if rc is None else rc)
'''
 run(label,[str(L/'lab.sh'),'run',N,'--timeout',str(seconds+20)],b'#!/usr/bin/env python3\n'+script.encode(),seconds+30)
 with (O/'commands.tsv').open('a') as f:f.write(label+'\t'+shlex.join(cmd)+'\t'+str(seconds)+'\n')

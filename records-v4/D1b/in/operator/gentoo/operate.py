import subprocess as sp,time,pathlib,os,json
root=pathlib.Path(__file__).resolve().parents[4]
os.chdir(root)
logs=pathlib.Path('D1b/in/operator/gentoo')
env=os.environ.copy();env['LAB_SEPARATE_STDERR']='1'
def call(tag,args,script=None):
 start=time.monotonic()
 with (logs/(tag+'.stdout')).open('wb') as out,(logs/(tag+'.stderr')).open('wb') as err:
  r=sp.run(args,input=script,stdout=out,stderr=err,env=env)
 with (logs/'operator-status.tsv').open('a') as f:f.write(f'{tag}\t{r.returncode}\t{time.monotonic()-start:.3f}\n')
 return r.returncode
try:
 rc=call('stage',['./lab.sh','run','d1b-gentoo','--timeout','120'],(logs/'guest-stage.sh').read_bytes())
 if rc:raise RuntimeError('Action stage failed; no retry')
 deadline=time.monotonic()+5400
 while True:
  r=sp.run(['./lab.sh','run','d1b-gentoo','--timeout','30'],input=b'test -f "$HOME/action-driver.status" && cat "$HOME/action-driver.status"\n',stdout=sp.PIPE,stderr=sp.PIPE,env=env)
  if r.returncode==0:
   (logs/'actions-overall.status').write_bytes(r.stdout);break
  if time.monotonic()>deadline:raise RuntimeError('Action session completion not certified within bound')
  time.sleep(20)
 script=b'#!/bin/bash\nset -e\ncd "$HOME"\ntar czf - actions-logs actions-status.tsv action-driver.sh action-driver.stdout action-driver.stderr action-driver.status action-driver.pid\n'
 if call('action-evidence',['./lab.sh','run','d1b-gentoo','--timeout','120'],script):raise RuntimeError('Action evidence transfer failed')
 script=b'rm -rf "$HOME/actions" "$HOME/actions-logs"; rm -f "$HOME/actions-status.tsv" "$HOME/action-driver.sh" "$HOME/action-driver.stdout" "$HOME/action-driver.stderr" "$HOME/action-driver.status" "$HOME/action-driver.pid"\n'
 if call('remove-control',['./lab.sh','run','d1b-gentoo','--timeout','60'],script):raise RuntimeError('Control cleanup failed')
 env['C1_INPUTS_COMMIT']='c62afbb5861fb038aa7da0aa00c0730ad140ec7c';env['LAB_ROOT']=str(root)
 call('collector',[str(root/'S4/fix-s4-p-3/collect.sh'),'--observe','d1b-gentoo','D1b/raw/gentoo'])
except Exception as e:
 (logs/'operator-error.txt').write_text(str(e)+'\n')
finally:
 rc=call('destroy',['./lab.sh','destroy','d1b-gentoo'])
 if rc:
  call('kill',['./lab.sh','kill','d1b-gentoo']);call('destroy-after-kill',['./lab.sh','destroy','d1b-gentoo'])
 (logs/'finished').write_text(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())+'\n')

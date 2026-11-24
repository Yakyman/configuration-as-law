import subprocess as sp,pathlib,time,json,base64,tarfile,io,os
R=pathlib.Path(__file__).resolve().parent
os.chdir(R)
O=R/'D1b/in/operator/void';O.mkdir(parents=True,exist_ok=True)
status=[]
def run(label,args,script=None):
 t=time.monotonic(); start=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
 with (O/(label+'.out')).open('wb') as out,(O/(label+'.err')).open('wb') as err:
  p=sp.run(args,input=script,stdout=out,stderr=err,env=dict(os.environ,LAB_SEPARATE_STDERR='1'))
 status.append(dict(operation=label,exit=p.returncode,seconds=round(time.monotonic()-t,3),utc=start))
 (O/'status.json').write_text(json.dumps(status,indent=2)+'\n')
 return p.returncode
def guest(label,script):return run(label,['./lab.sh','run','d1b-void','--timeout','90'],script.encode())
for label in ['base','bin']: (R/'C1'/label).symlink_to(pathlib.Path('../../C1')/label)
for label in ['keys','install','slots']:(R/label).symlink_to(pathlib.Path('..')/label)
(R/'C1/vms').mkdir()
run('preflight',['sh','-c','command -v python3; command -v dumpsolv; sha256sum lab.sh'])
# A shared lock is checked only for scheduling; the unchanged runner acquires and holds its own lock.
while True:
 free=sp.run(['sh','-c','for i in $(seq 1 12); do flock -n slots/slot-$i.lock true && exit 0; done; exit 1'],stdout=sp.DEVNULL,stderr=sp.DEVNULL).returncode==0
 if free:break
 time.sleep(20)
started=False
try:
 if run('new',['./lab.sh','new','d1b-void','void'])!=0:raise RuntimeError('Machine creation failed; no retry')
 started=True
 data=io.BytesIO()
 with tarfile.open(fileobj=data,mode='w') as tf:tf.add('C1/actions',arcname='actions')
 payload=base64.b64encode(data.getvalue()).decode()
 stage='#!/bin/bash\nset -e\nmkdir "$HOME/d1b-control"\nbase64 -d <<\'PAYLOAD\' | tar -xf - -C "$HOME/d1b-control"\n'+payload+'\nPAYLOAD\nnohup setsid sh -c \'cd "$HOME/d1b-control/actions"; bash void.sh > "$HOME/d1b-control/batch.out" 2> "$HOME/d1b-control/batch.err"; printf "%s\\n" "$?" > "$HOME/d1b-control/done"\' </dev/null >/dev/null 2>&1 &\n'
 if guest('stage-and-launch',stage)!=0:raise RuntimeError('Action launch transport failed; not repeated')
 t=time.monotonic()
 while True:
  n=sum(x['operation'].startswith('monitor-') for x in status)
  rc=guest('monitor-'+str(n),'#!/bin/sh\nif test -f "$HOME/d1b-control/done"; then cat "$HOME/d1b-control/done"; else exit 75; fi\n')
  if rc==0:break
  if time.monotonic()-t>13500:raise RuntimeError('Action monitoring limit reached')
  time.sleep(30)
 (O/'actions-duration.json').write_text(json.dumps({'seconds':round(time.monotonic()-t,3),'exit':int((O/('monitor-'+str(n)+'.out')).read_text().strip())})+'\n')
 for name,path in [('actions-logs','/home/user/actions-logs'),('actions-status','/home/user/actions-status.tsv'),('control','/home/user/d1b-control')]:
  if run('copy-'+name,['./lab.sh','copy-out','d1b-void',path,str(O/'actions')]):raise RuntimeError('Action copy failed')
 if guest('remove-scaffolding','#!/bin/sh\nrm -rf "$HOME/d1b-control" "$HOME/actions-logs" "$HOME/actions-status.tsv"\n'):raise RuntimeError('Scaffolding removal failed')
 run('collector',['sh','-c','INPUTS_COMMIT=c62afbb5861fb038aa7da0aa00c0730ad140ec7c; S4_INPUTS="$PWD/S4"; C1_INPUTS_COMMIT="$INPUTS_COMMIT" LAB_ROOT="$PWD" "$S4_INPUTS/fix-s4-p-3/collect.sh" --observe d1b-void D1b/raw/void'])
except Exception as e:
 (O/'orchestration-error.txt').write_text(str(e)+'\n')
finally:
 if (R/'C1/vms/d1b-void').exists():
  if run('destroy',['./lab.sh','destroy','d1b-void']):
   run('kill',['./lab.sh','kill','d1b-void']);run('destroy-after-kill',['./lab.sh','destroy','d1b-void'])
 (O/'FINISHED').write_text(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())+'\n')

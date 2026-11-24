import subprocess, pathlib, json, datetime, tarfile, io, base64, os, socket
lab=pathlib.Path.home()/'VMs/cal-1123'; work=lab/'A3/developer'; op=work/'operator'; state={}
def save(): (op/'status.json').write_text(json.dumps(state,indent=2)+'\n')
def run(label,args,data=None,timeout=None):
 state['current']=label;save()
 r=subprocess.run(args,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout,cwd=lab)
 for ext,b in [('out',r.stdout),('err',r.stderr)]:
  s=b.decode(errors='replace').replace(str(lab),'LAB_ROOT').replace(str(pathlib.Path.home()),'HOST_HOME').replace(socket.gethostname(),'the-host')
  (op/(label+'.'+ext)).write_text(s)
 state[label]={'exit':r.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};save();return r.returncode
L=str(lab/'lab.sh')
def guest(label,body,timeout=300): return run(label,[L,'run','a3-developer','--timeout',str(timeout)],body.encode(),timeout+60)
try:
 if run('new',[L,'new','a3-developer','fedora']): raise RuntimeError('new failed')
 guest('boot-before','cat /proc/sys/kernel/random/boot_id\n')
 b=io.BytesIO()
 with tarfile.open(fileobj=b,mode='w') as t:
  for n in ['lib.sh','lived-developer.sh']: t.add(work/'inputs/actions'/n,arcname=n)
 payload=base64.b64encode(b.getvalue()).decode()
 script='#!/bin/bash\nset -e\nmkdir -p /tmp/a3-developer-inputs\nprintf %s '+payload+' | base64 -d | tar -xf - -C /tmp/a3-developer-inputs\nexport XDG_RUNTIME_DIR=/run/user/$(id -u)\nexport DBUS_SESSION_BUS_ADDRESS=unix:path=$XDG_RUNTIME_DIR/bus\nbash /tmp/a3-developer-inputs/lived-developer.sh\n'
 guest('actions',script,12000)
 run('copy-actions-status',[L,'copy-out','a3-developer','/home/user/actions-status.tsv',str(op/'actions-status.tsv')])
 run('copy-actions-logs',[L,'copy-out','a3-developer','/home/user/actions-logs',str(op/'actions-logs')])
 guest('remove-input-staging','rm -rf /tmp/a3-developer-inputs\n')
 if run('restart-stop',[L,'stop','a3-developer']): raise RuntimeError('restart stop failed')
 if run('restart-start',[L,'start','a3-developer']): raise RuntimeError('restart start failed')
 guest('boot-after','cat /proc/sys/kernel/random/boot_id\n')
 env=os.environ.copy();env.update(LAB_ROOT=str(lab),C1_INPUTS_COMMIT='3e0207b104f9718793c5b2678810936c7c3c14d2')
 os.environ.update(env)
 run('collect',[str(work/'inputs/collect.sh'),'--observe','a3-developer',str(work/'raw/developer')])
finally:
 run('destroy',[L,'destroy','a3-developer'])
try:
 if run('base-new',[L,'new','a3-developer-base','fedora']): raise RuntimeError('base new failed')
 run('base-collect',[str(work/'inputs/collect.sh'),'--observe','a3-developer-base',str(work/'raw/developer-base')])
finally:
 run('base-destroy',[L,'destroy','a3-developer-base'])
state['current']='finished';save()

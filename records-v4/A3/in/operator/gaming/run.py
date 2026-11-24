import subprocess as sp,pathlib,os,json,datetime,tarfile,io,base64,socket,hashlib
lab=pathlib.Path.home()/'VMs/cal-1123'; work=lab/'A3/gaming'; os.chdir(lab)
logs=work/'operator'; logs.mkdir(exist_ok=False)
status={}; active=None

def run(tag,args,stdin=None,env=None):
 p=sp.run(args,input=stdin,stdout=sp.PIPE,stderr=sp.PIPE,env=env)
 for suffix,data in [('out',p.stdout),('err',p.stderr)]:
  data=data.replace(str(pathlib.Path.home()).encode(),b'<host-home>').replace(socket.gethostname().encode(),b'<host>')
  (logs/(tag+'.'+suffix)).write_bytes(data)
 status[tag]={'exit_status':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}; (logs/'lifecycle.json').write_text(json.dumps(status,indent=2))
 return p.returncode

def cmd(tag,*args,stdin=None): return run(tag,['./lab.sh',*args],stdin)
def collect(name,label):
 env=dict(os.environ,LAB_ROOT=str(lab),C1_INPUTS_COMMIT='3e0207b104f9718793c5b2678810936c7c3c14d2')
 run(label+'-collector',['sh',str(work/'inputs/collect.sh'),'--observe',name,str(work/label)],env=env)
try:
 active='a3-gaming'
 if cmd('lived-new','new',active,'mint')==0:
  cmd('boot-before','run',active,stdin=b'cat /proc/sys/kernel/random/boot_id\n')
  buf=io.BytesIO()
  with tarfile.open(fileobj=buf,mode='w:gz') as t:
   for n in ['lived-gaming.sh','lib.sh','gui_guard.py','apt_https_sources.py']: t.add(work/'inputs/actions'/n,arcname=n)
  script=b'#!/bin/bash\nset -e\nstage=/run/user/$(id -u)/a3-inputs\nmkdir -p "$stage"\nbase64 -d <<\'INPUTS\' | tar -xz -C "$stage"\n'+base64.b64encode(buf.getvalue())+b'\nINPUTS\nbash "$stage/lived-gaming.sh"\n'
  cmd('actions','run',active,'--timeout','11000',stdin=script)
  cmd('actions-status','copy-out',active,'/home/user/actions-status.tsv',str(logs/'actions-status.tsv'))
  cmd('actions-logs','copy-out',active,'/home/user/actions-logs',str(logs/'actions-logs'))
  if cmd('restart-stop','stop',active)==0 and cmd('restart-start','start',active)==0:
   cmd('boot-after','run',active,stdin=b'cat /proc/sys/kernel/random/boot_id\n')
   collect(active,'gaming')
  cmd('lived-destroy','destroy',active); active=None
 active='a3-gaming-base'
 if cmd('base-new','new',active,'mint')==0: collect(active,'gaming-base')
 cmd('base-destroy','destroy',active); active=None
finally:
 if active: cmd('final-destroy','destroy',active)
 (logs/'DONE').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')

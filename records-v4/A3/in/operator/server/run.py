import pathlib,subprocess,datetime,json,hashlib,os
root=pathlib.Path.home()/'VMs/cal-1123'; work=root/'A3/server'; op=work/'operator';op.mkdir(exist_ok=True)
lab=str(root/'lab.sh'); status=[]
def run(label,args,inp=None):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 r=subprocess.run(args,input=inp,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 for suffix,data in [('out',r.stdout),('err',r.stderr)]:
  data=data.replace(str(pathlib.Path.home()).encode(),b'<host-home>')
  (op/(label+'.'+suffix)).write_bytes(data)
 status.append(dict(step=label,exit_status=r.returncode,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 (op/'lifecycle.json').write_text(json.dumps(status,indent=2)+'\n')
 return r.returncode
try:
 for name in ['a3-server','a3-server-base']:
  short=name.removeprefix('a3-')
  if run(short+'-new',[lab,'new',name,'debian-server']):continue
  try:
   if name=='a3-server':
    run('actions',[lab,'run',name,'--timeout','7200'],(work/'guest-actions.sh').read_bytes())
    run('copy-action-status',[lab,'copy-out',name,'/home/user/actions-status.tsv',str(op)])
    run('copy-action-logs',[lab,'copy-out',name,'/home/user/actions-logs',str(op)])
    run('boot-before',[lab,'run',name],b'cat /proc/sys/kernel/random/boot_id\n')
    stopped=run('restart-stop',[lab,'stop',name])
    if stopped:raise RuntimeError('Restart stop failed; no alternative restart authorized')
    if run('restart-start',[lab,'start',name]):raise RuntimeError('Restart start failed')
    run('boot-after',[lab,'run',name],b'cat /proc/sys/kernel/random/boot_id\n')
   env=os.environ.copy();env['LAB_ROOT']=str(root);env['C1_INPUTS_COMMIT']='3e0207b104f9718793c5b2678810936c7c3c14d2'
   os.environ.update(env)
   run(short+'-collect',['sh',str(work/'inputs/collect.sh'),'--observe',name,str(work/'raw'/short)])
  finally:
   if run(short+'-destroy',[lab,'destroy',name]):
    run(short+'-kill',[lab,'kill',name]);run(short+'-destroy-after-kill',[lab,'destroy',name])
except Exception as e:
 (op/'exception.txt').write_text(str(e)+'\n')
finally:
 rows=[]
 for p in sorted((work/'raw').rglob('*')):
  if p.is_file():rows.append(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(work)}\n')
 (op/'raw-sha256.txt').write_text(''.join(rows))
 (op/'DONE').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')

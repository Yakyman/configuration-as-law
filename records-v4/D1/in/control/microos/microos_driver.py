import pathlib,subprocess,os,json,datetime
lab=pathlib.Path.home()/'VMs/cal-1123'
work=lab/'D1/microos';work.mkdir(parents=True,exist_ok=True)
name='d1-microos'
def call(label,args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (work/(label+'.out')).open('wb') as out,(work/(label+'.err')).open('wb') as err:
  p=subprocess.run(args,stdout=out,stderr=err,env={**os.environ,'LAB_ROOT':str(lab),'C1_INPUTS_COMMIT':'b3c3c141c612b8d287c8058733141cb56d1c2431','PYTHONDONTWRITEBYTECODE':'1'})
 with (work/'status.jsonl').open('a') as f:f.write(json.dumps({'operation':label,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_status':p.returncode})+'\n')
 return p.returncode
if (lab/'C1/vms'/name).exists() or (work/'status.jsonl').exists():raise SystemExit('Refuse existing case')
try:
 if call('new',[str(lab/'lab.sh'),'new',name,'microos'])==0:
  call('collector',[str(lab/'D1/inputs/collect.sh'),'--observe',name,str(work/'inventory')])
finally:
 if (lab/'C1/vms'/name).exists():
  if call('destroy',[str(lab/'lab.sh'),'destroy',name]):
   call('kill',[str(lab/'lab.sh'),'kill',name]);call('destroy-fallback',[str(lab/'lab.sh'),'destroy',name])
 (work/'done.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'vm_directory_absent':not (lab/'C1/vms'/name).exists()})+'\n')

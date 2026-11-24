import pathlib,subprocess as sp,os,time,csv,hashlib,json,shutil,re,datetime
from queries import queries,FACTS
R=pathlib.Path(__file__).resolve().parent; O=R/'evidence';O.mkdir(exist_ok=True); name='fx-s4-p-3-microos'
env={**os.environ,'LAB_SEPARATE_STDERR':'1'}
def clean(s):
 s=re.sub(r'/home/[^/\s]+','HOST_HOME',s)
 return s.replace(str(R),'TASK_ROOT')
def call(label,args,script=None):
 t=time.monotonic();p=sp.run(args,input=script,stdout=sp.PIPE,stderr=sp.PIPE,timeout=600,env=env)
 with (O/'status.tsv').open('a') as f:f.write(f'{label}\t{p.returncode}\t{time.monotonic()-t:.3f}\n')
 (O/(label+'.stderr')).write_text(clean(p.stderr.decode(errors='replace')))
 return p
(O/'status.tsv').write_text('operation\texit_status\tduration_seconds\n')
base=R/'C1/base/microos.qcow2'
def hashes():
 return {'base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'base_write_bits':base.stat().st_mode&0o222,**{x:hashlib.sha256((R/x).read_bytes()).hexdigest() for x in ['run.py','queries.py','lab.sh']}}
(O/'before.json').write_text(json.dumps(hashes(),indent=2)+'\n')
transient=R/'inventory';transient.mkdir()
try:
 p=call('boot',[str(R/'lab.sh'),'new',name,'microos'])
 if p.returncode:raise RuntimeError('boot failed')
 with (O/'diagnostics.tsv').open('w') as f:
  w=csv.writer(f,delimiter='\t');w.writerow(['fact','route','query_exit','output_bytes','output_lines','query_status_markers','fd_matches','maps_matches','note'])
  for fact,route,script in queries():
   (O/(fact+'-'+route+'.sh')).write_text('#!/bin/sh\n'+script+'\n')
   p=call(fact+'-'+route,[str(R/'lab.sh'),'run',name,'--root','--timeout','120'],script.encode())
   (transient/(fact+'-'+route+'.out')).write_bytes(p.stdout)
   out=p.stdout.decode(errors='replace'); fd=maps='not-requested'
   if fact=='M14' and route=='installation-current':
    fd=str(len(out.split('CURRENT_FD_BEGIN\n')[-1].split('CURRENT_FD_END')[0].strip().splitlines()))
    maps=str(len(out.split('CURRENT_MAPS_BEGIN\n')[-1].split('CURRENT_MAPS_END')[0].strip().splitlines()))
   w.writerow([fact,route,p.returncode,len(p.stdout),len(out.splitlines()),','.join(re.findall(r'query_exit=\d+',out)),fd,maps,'Current state and script text are not event records.']);f.flush()
   # Only numeric per-source counts retained; raw source data is never shown.
   counts={term:len(re.findall(re.escape(term),out,re.I)) for term in ['Created symlink','enable','disable','COMMAND=','grubenv','sudoers','ca-certificates','NetworkManager','mdcheck_continue','jeos-firstboot','query_exit=']}
   counts['historical_source_line_count']=sum(bool(re.match(r'/var/(log|lib)/[^:]+:\d+:',x)) for x in out.splitlines())
   (O/(fact+'-'+route+'.counts.json')).write_text(json.dumps(counts,indent=2)+'\n')
finally:
 shutil.rmtree(transient)
 p=call('destroy',[str(R/'lab.sh'),'destroy',name])
 if p.returncode:
  call('kill',[str(R/'lab.sh'),'kill',name]);call('destroy-fallback',[str(R/'lab.sh'),'destroy',name])
 (O/'after.json').write_text(json.dumps(hashes(),indent=2)+'\n')
 (O/'cleanup.json').write_text(json.dumps({'vm_directories':len(list((R/'C1/vms').iterdir())),'transient_inventories':int(transient.exists()),'source_and_base_hashes_unchanged':json.loads((O/'before.json').read_text())==hashes(),'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
 (O/'finished').touch()

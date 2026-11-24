import pathlib,subprocess as sp,time,os,json,tarfile,io,base64,shlex,shutil,re
R=pathlib.Path(__file__).resolve().parent; LAB=R; OUT=R/'raw4'; NAME='fx-s4p3-alma-full'
OUT.mkdir(parents=True,exist_ok=True)
def record(label,rc,duration):
 with (OUT/'status.tsv').open('a') as f:f.write(f'{label}\t{rc}\t{duration:.3f}\n')
def call(label,args,data=None,timeout=2400,capture=False):
 if label=='collector':
  group=pathlib.Path('/sys/fs/cgroup'+pathlib.Path('/proc/self/cgroup').read_text().strip().split(':',2)[2])
  for source in ('memory.events','memory.max','memory.current'):
   if (group/source).exists():(OUT/('collector-before-'+source)).write_text((group/source).read_text())
 t=time.monotonic();p=sp.run(args,input=data,stdout=sp.PIPE if capture else sp.DEVNULL,stderr=sp.PIPE,timeout=timeout,env={**os.environ,'LAB_SEPARATE_STDERR':'1','LAB_ROOT':str(LAB),'C1_INLINE_COUNTS':'1','LAB_REHEARSAL_COUNTS':str(OUT/'counts.tsv'),'LAB_REHEARSAL_ROUND':'3'})
 err=p.stderr.decode(errors='replace').replace(str(R),'S4');err=re.sub(r'/home/[^/\s]+','HOST_HOME',err)
 (OUT/(label+'.stderr')).write_text(err)
 if label=='collector':
  for source in ('memory.events','memory.max','memory.current','memory.peak'):
   if (group/source).exists():(OUT/('collector-after-'+source)).write_text((group/source).read_text())
 record(label,p.returncode,time.monotonic()-t);return p

def run(label,script,capture=False,timeout=300):return call(label,[str(LAB/'lab.sh'),'run',NAME,'--timeout',str(timeout)],script.encode(),timeout+15,capture)
(OUT/'status.tsv').write_text('operation\texit_status\tduration_seconds\n')
try:
 p=call('boot',[str(LAB/'lab.sh'),'new',NAME,'alma'],timeout=600)
 if p.returncode:raise RuntimeError('boot failed')
 buf=io.BytesIO()
 with tarfile.open(fileobj=buf,mode='w:gz') as tar:
  for path in sorted((R/'actions').glob('*')):
   if path.is_file():tar.add(path,arcname=path.name)
 stage='mkdir -p "$HOME/.s4-actions"\nprintf %s '+shlex.quote(base64.b64encode(buf.getvalue()).decode())+' | base64 -d | tar -xz -C "$HOME/.s4-actions"\n'
 if run('stage',stage).returncode:raise RuntimeError('stage failed')
 job='#!/bin/bash\nbash "$HOME/.s4-actions/alma.sh"\nprintf "%s\\n" "$?" > "$HOME/.s4-actions/done"\n'
 launch='printf %s '+shlex.quote(base64.b64encode(job.encode()).decode())+' | base64 -d > "$HOME/.s4-actions/job.sh"\nnohup setsid bash "$HOME/.s4-actions/job.sh" </dev/null >/dev/null 2>&1 &\n'
 t=time.monotonic()
 if run('launch-actions',launch).returncode:raise RuntimeError('launch failed')
 while time.monotonic()-t<5400:
  time.sleep(10)
  p=run('poll','test -f "$HOME/.s4-actions/done" && cat "$HOME/.s4-actions/done"\n',True)
  if p.returncode==0 and p.stdout.strip().isdigit():break
 else:raise RuntimeError('actions timed out')
 record('actions',int(p.stdout.strip()),time.monotonic()-t)
 p=run('action-status','cat "$HOME/actions-status.tsv"\n',True)
 (OUT/'actions.tsv').write_bytes(p.stdout)
 for name in ['package_program','application_package','language_program','browser_extension','personal_setting','user_service','network_connection','home_script','container_run']:
  p=run('action-'+name,'cat "$HOME/actions-logs/'+name+'.stderr"\n',True)
  text=p.stdout.decode(errors='replace');text=re.sub(r'/home/[^/\s]+','GUEST_HOME',text)
  (OUT/('action-'+name+'.stderr')).write_text(text)
 run('remove-action-logs','rm -rf "$HOME/actions-logs" "$HOME/actions-status.tsv" "$HOME/.s4-actions"\n')
 transient=OUT/'.inventory-unread'
 p=call('assembled-collector',['python3',str(R/'assembled-main.py'),'--rehearsal',NAME,str(transient)],timeout=2400)
 for name in ('fact-summary.json','s4-summary.json','coverage.tsv','status.json'):
  if (transient/name).exists():shutil.copyfile(transient/name,OUT/name)
 for path in (transient/'raw').glob('*.err'):
  text=path.read_text(errors='replace');text=re.sub(r'/home/[^/\s]+','GUEST_HOME',text)
  if text:(OUT/path.name).write_text(text)
 shutil.rmtree(transient,ignore_errors=True)
 if p.returncode:raise RuntimeError('assembled collector failed')
finally:
 shutil.rmtree(OUT/'.inventory-unread',ignore_errors=True)
 p=call('destroy',[str(LAB/'lab.sh'),'destroy',NAME],timeout=180)
 if p.returncode:
  call('kill',[str(LAB/'lab.sh'),'kill',NAME],timeout=60)
  call('destroy-fallback',[str(LAB/'lab.sh'),'destroy',NAME],timeout=180)
 (OUT/'cleanup.json').write_text(json.dumps({'clone_absent':not (LAB/'C1/vms'/NAME).exists(),'inventory_removed':not (OUT/'.inventory-unread').exists(),'event_payload_saved':False})+'\n')
 (OUT/'finished').touch()

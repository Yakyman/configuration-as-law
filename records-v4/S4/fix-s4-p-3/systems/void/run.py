import pathlib,subprocess as sp,time,os,json,tarfile,io,base64,shlex,shutil,re,hashlib
R=pathlib.Path(__file__).resolve().parent; O=R/'diagnostics';O.mkdir(exist_ok=True);N='fx-s4-p-3-void'
def clean(s):return re.sub(r'/home/[^/\s]+','GUEST_HOME',s.replace(str(R),'RUN_ROOT'))
def call(label,args,data=None,timeout=2400):
 t=time.monotonic();p=sp.run(args,input=data,stdout=sp.PIPE,stderr=sp.PIPE,timeout=timeout,env={**os.environ,'LAB_SEPARATE_STDERR':'1','LAB_ROOT':str(R)})
 (O/(label+'.stderr')).write_text(clean(p.stderr.decode(errors='replace')))
 with (O/'status.tsv').open('a') as f:f.write(f'{label}\t{p.returncode}\t{time.monotonic()-t:.3f}\n')
 return p
def run(label,script,timeout=300,root=False):return call(label,[str(R/'lab.sh'),'run',N]+(['--root'] if root else [])+['--timeout',str(timeout)],script.encode(),timeout+20)
(O/'status.tsv').write_text('operation\texit_status\tduration_seconds\n')
try:
 p=call('boot',[str(R/'lab.sh'),'new',N,'void'],timeout=600)
 if p.returncode:raise RuntimeError('boot failed')
 buf=io.BytesIO()
 with tarfile.open(fileobj=buf,mode='w:gz') as t:
  for path in (R/'actions').iterdir():
   if path.is_file():t.add(path,arcname=path.name)
 p=run('stage','mkdir -p "$HOME/.s4-actions"\nprintf %s '+shlex.quote(base64.b64encode(buf.getvalue()).decode())+' | base64 -d | tar -xz -C "$HOME/.s4-actions"\n')
 if p.returncode:raise RuntimeError('stage failed')
 p=run('actions','bash "$HOME/.s4-actions/void.sh" >/dev/null 2>&1\n',5400)
 (O/'actions.tsv').write_text(clean(run('action-status','cat "$HOME/actions-status.tsv"\n').stdout.decode()))
 # Only action diagnostics retained; no inventory.
 for name in ['package_program','application_package','language_program','browser_extension','personal_setting','user_service','network_connection','home_script','container_run']:
  p=run('action-'+name,'cat "$HOME/actions-logs/'+name+'.stderr"\n')
  (O/('action-'+name+'.stderr')).write_text(clean(p.stdout.decode(errors='replace')))
 run('remove-action-logs','rm -rf "$HOME/actions-logs" "$HOME/actions-status.tsv" "$HOME/.s4-actions"\n')
 (O/'actions-finished').touch()
 start=time.monotonic()
 while not (R/'probes-ready').exists():
  if time.monotonic()-start>2400:raise RuntimeError('probe staging timed out')
  time.sleep(5)
 for path in sorted((R/'probes').glob('*.py')):
  script="#!/bin/sh\npython3 - <<'S4_QUERY'\n"+path.read_text()+"\nS4_QUERY\n"
  p=run(path.stem,script,root=True)
  (O/(path.stem+'.json')).write_text(clean(p.stdout.decode(errors='replace')))
finally:
 p=call('destroy',[str(R/'lab.sh'),'destroy',N],timeout=180)
 if p.returncode:
  call('kill',[str(R/'lab.sh'),'kill',N],timeout=60);call('destroy-fallback',[str(R/'lab.sh'),'destroy',N],timeout=180)
 (O/'cleanup.json').write_text(json.dumps({'clone_absent':not (R/'C1/vms'/N).exists(),'inventory_written':False})+'\n')
 (O/'finished').touch()

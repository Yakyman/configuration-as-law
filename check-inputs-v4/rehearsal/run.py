#!/usr/bin/env python3
"""Run on the lab host. Never print rehearsal content; persist numeric reductions only."""
import base64,collections,csv,fcntl,io,json,os,pathlib,re,shlex,shutil,subprocess,sys,tarfile,time
csv.field_size_limit(536870912)
ROOT=pathlib.Path(__file__).resolve().parent.parent
LAB=ROOT.parent
system,round_no=sys.argv[1:3]
if system not in ('alma','void','gentoo','microos','talos','nixos','guix','fedora','mint','debian-server') or round_no not in ('1','2','3','4'):sys.exit(64)
name=f'reh-{system}-{round_no}'
out=ROOT/'rehearsal'/system;out.mkdir(parents=True,exist_ok=True)
status=out/'status.tsv';counts=out/'counts.tsv'
lock=open(out/'.run.lock','a')
try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
except BlockingIOError:sys.exit(73)
def append(path,header,row):
 new=not path.exists()
 with path.open('a') as f:
  w=csv.writer(f,delimiter='\t',lineterminator='\n')
  if new:w.writerow(header)
  w.writerow(row)
def record(label,rc,seconds,size=0):append(status,['round','operation','exit_status','duration_seconds','bytes'],[round_no,label,rc,round(seconds,3),size])
def count(kind,n):append(counts,['round','kind','rows'],[round_no,kind,n])
def call(label,argv,data=None,timeout=1800,capture=False):
 start=time.monotonic()
 # Bytes are counted without decoding; only explicitly numeric control results are parsed.
 p=subprocess.Popen(argv,stdin=subprocess.PIPE if data is not None else subprocess.DEVNULL,stdout=subprocess.PIPE if capture else subprocess.DEVNULL,stderr=subprocess.DEVNULL,env={**os.environ,'LAB_ROOT':str(LAB),'LAB_REHEARSAL_COUNTS':str(counts),'LAB_REHEARSAL_ROUND':round_no})
 try:b,_=p.communicate(data,timeout=timeout);rc=p.returncode
 except subprocess.TimeoutExpired:p.kill();b,_=p.communicate();rc=124
 record(label,rc,time.monotonic()-start,len(b or b''));return rc,b or b''
def run(label,script,timeout=300,capture=False):return call(label,[str(LAB/'lab.sh'),'run',name,'--timeout',str(timeout)],script.encode(),timeout+15,capture)
transient=out/f'.unread-{round_no}'
created=False
if transient.exists():sys.exit(73)
if status.exists():
 with status.open() as f:
  if any(r.get('round')==round_no for r in csv.DictReader(f,delimiter='\t')):sys.exit(73)
if (LAB/'C1/vms'/name).exists():
 record('refuse-existing-clone',73,0);sys.exit(73)
try:
 rc,_=call('create',[str(LAB/'lab.sh'),'new',name,system],timeout=600)
 if rc:
  created=(LAB/'C1/vms'/name/'meta.json').exists()
  sys.exit(rc)
 created=True
 for i in range(1,21):run(f'transport-{i:02d}','exit 0\n',60)
 entry={'alma':'alma.sh','void':'void.sh','gentoo':'gentoo.sh','fedora':'lived-developer.sh','mint':'lived-gaming.sh','debian-server':'lived-server.sh'}.get(system)
 if entry:
  buf=io.BytesIO()
  with tarfile.open(fileobj=buf,mode='w:gz') as t:
   for p in sorted((ROOT/'actions').glob('*')):
    if p.is_file() and p.suffix in ('.sh','.py'):t.add(p,arcname=p.name)
  encoded=base64.b64encode(buf.getvalue()).decode()
  rc,_=run('stage-actions','mkdir -p "$HOME/.cal-rehearsal-actions"\nprintf %s '+shlex.quote(encoded)+' | base64 -d | tar -xz -C "$HOME/.cal-rehearsal-actions"\n')
  if rc==0:
   job='#!/bin/bash\nbash "$HOME/.cal-rehearsal-actions/'+entry+'"\nrc=$?\nprintf "%s\\n" "$rc" > "$HOME/.cal-rehearsal-actions/done"\n'
   encoded_job=base64.b64encode(job.encode()).decode()
   launch='printf %s '+shlex.quote(encoded_job)+' | base64 -d > "$HOME/.cal-rehearsal-actions/job.sh"\nnohup setsid bash "$HOME/.cal-rehearsal-actions/job.sh" </dev/null >/dev/null 2>&1 &\n'
   start=time.monotonic()
   launched,_=run('launch-actions',launch,60)
   action_rc=launched
   if launched==0:
    action_rc=124
    while time.monotonic()-start<172800:
     time.sleep(15)
     poll=['%s'% (LAB/'lab.sh'),'run',name,'--timeout','30']
     try:
      done=subprocess.run(poll,input=b'test -f "$HOME/.cal-rehearsal-actions/done" && cat "$HOME/.cal-rehearsal-actions/done"\n',stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=40)
      if done.returncode==0 and done.stdout.strip().isdigit():action_rc=int(done.stdout.strip());break
     except subprocess.TimeoutExpired:pass
   record('actions',action_rc,time.monotonic()-start)
   _,b=run('action-status-reduction','cat "$HOME/actions-status.tsv"\n',60,True)
   expected={'alma':{'package_program','application_package','language_program','browser_extension','personal_setting','user_service','network_connection','home_script','container_run'},'void':{'package_program','application_package','language_program','browser_extension','personal_setting','user_service','network_connection','home_script','container_run','language_install_node','language_npm_install','language_cowsay'},'gentoo':{'package_program','application_package','language_program','browser_extension','personal_setting','user_service','network_connection','home_script','container_run'},'mint':{'gaming_prerequisites','gaming_store_runtime','gaming_anonymous_download','gaming_flatpak_game','gaming_launcher_tool','gaming_windows_program','gaming_overlay','gaming_user_settings','gaming_autostart'}}
   if system not in expected:
    import re
    expected[system]=set(re.findall(r'^((?:developer|server)_[a-z_]+) [0-9]+$',(ROOT/'actions'/entry).read_text(),re.M))
   allowed=set()
   # Labels originate in fixed input scripts; numeric fields are the only observations retained.
   for line in b.decode().splitlines():
    a=line.split('\t')
    if len(a)==3 and a[0] in expected[system] and a[1].isdigit() and a[2].isdigit():record('action-'+a[0],int(a[1]),int(a[2]));allowed.add(a[0])
   _,b=run('action-bytes-reduction','for f in "$HOME"/actions-logs/*.log; do test -f "$f" || continue; printf "%s\\t" "${f##*/}"; wc -c < "$f"; done\n',60,True)
   for line in b.decode().splitlines():
    a=line.split('\t')
    if len(a)==2 and a[0].removesuffix('.log') in allowed and a[1].strip().isdigit():record('action-output-'+a[0].removesuffix('.log'),0,0,int(a[1]))
   run('remove-action-output','rm -rf "$HOME/actions-logs" "$HOME/actions-status.tsv" "$HOME/.cal-rehearsal-actions"\n',60)
 if system not in ('nixos','guix'):
  collector_rc,_=call('collector',[str(ROOT/'collect.sh'),'--rehearsal',name,str(transient)],timeout=1800)
  count('collector:exit-success',int(collector_rc==0))
  if (transient/'coverage.tsv').exists():
   with (transient/'coverage.tsv').open() as f:
    for r in csv.DictReader(f,delimiter='\t'):record('query-'+re.sub(r'packages-flatpak-user-[0-9]+-', 'packages-flatpak-user-', r['query']),int(r['exit_status']),float(r['duration']),int(r['bytes']))
  schemas={'objects.tsv':['id','machine','level','kind','name','members','evidence'],'level-1.tsv':['id','machine','level','kind','name','members','evidence'],'level-2.tsv':['id','machine','level','kind','name','members','evidence'],'package-files.tsv':['package','path','integrity','evidence','rule'],'coverage.tsv':['query','exit_status','duration','rows','bytes','stdout','stderr','status','object_rows']}
  valid=collector_rc==0 and (transient/'metadata.json').exists()
  for artifact,columns in schemas.items():
   if not (transient/artifact).exists():valid=False;continue
   with (transient/artifact).open() as f:
    if next(csv.reader(f,delimiter='\t'),[])!=columns:valid=False
  scan_counts=collections.Counter()
  for scan in (transient/'raw').glob('*-filesystem.out'):
   with scan.open() as f:
    for line in f:
     try:row=json.loads(line)
     except ValueError:scan_counts['invalid-rows']+=1;continue
     if 'path' in row:scan_counts['entry-rows']+=1
     elif 'error' in row:scan_counts['error-rows']+=1
     elif 'alias' in row:scan_counts['alias-rows']+=1
  for kind,n in scan_counts.items():count('filesystem:'+kind,n)
  packages={};kinds=collections.Counter();levels=collections.Counter()
  if (transient/'objects.tsv').exists():
   with (transient/'objects.tsv').open() as f:
    for r in csv.DictReader(f,delimiter='\t'):
     kinds[r['kind']]+=1;levels[r['level']]+=1
     if r['kind']=='package':
      v=json.loads(r['members'])
      if isinstance(v,str):
       try:v=json.loads(v)
       except ValueError:v={}
      packages[r['id']]=v if isinstance(v,dict) else {}
  for k,v in sorted(kinds.items()):count('object:'+k,v)
  for k in ('1','2'):count('level:'+k,levels[k])
  count('packages:total',len(packages));count('packages:reason-known',sum(p.get('reason') in ('explicit','dependency') for p in packages.values()))
  integrity=collections.defaultdict(list)
  if (transient/'package-files.tsv').exists():
   with (transient/'package-files.tsv').open() as f:
    for r in csv.DictReader(f,delimiter='\t'):integrity[r['package']].append(r['integrity'] in ('unchanged','changed','missing'))
  count('packages:integrity-any-known',sum(any(integrity[p]) for p in packages));count('packages:integrity-all-known',sum(bool(integrity[p]) and all(integrity[p]) for p in packages))
  count('package-files:total',sum(map(len,integrity.values())));count('package-files:integrity-known',sum(sum(v) for v in integrity.values()))
  if (transient/'metadata.json').exists():
   m=json.loads((transient/'metadata.json').read_text());count('collector:gaps',len(m.get('gaps',[])));count('collector:filesystem-complete',int(m.get('filesystem_complete',False)))
  count('collector:reduction-complete',int(valid))
except Exception as exc:
 record('reduction-error-'+type(exc).__name__,65,0)
 raise SystemExit(65)
finally:
 shutil.rmtree(transient,ignore_errors=True)
 if created:
  rc,_=call('destroy',[str(LAB/'lab.sh'),'destroy',name],timeout=180)
  if rc:
   call('kill-fallback',[str(LAB/'lab.sh'),'kill',name],timeout=30)
   call('destroy-fallback',[str(LAB/'lab.sh'),'destroy',name],timeout=180)

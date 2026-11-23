#!/usr/bin/env python3
"""Run on the lab host. Never print rehearsal content; persist numeric reductions only."""
import traceback,signal,hashlib,base64,collections,csv,fcntl,io,json,os,pathlib,re,shlex,shutil,subprocess,sys,tarfile,time
csv.field_size_limit(536870912)
ROOT=pathlib.Path(__file__).resolve().parent.parent
LAB=ROOT.parent
system,round_no=sys.argv[1:3]
if system not in ('alma','void','gentoo','microos','talos','nixos','guix','fedora','mint','debian-server') or round_no not in ('1','2','3','4'):sys.exit(64)
round_no=str(int(round_no)+10)
name=f'reh-{system}-fx{int(round_no)-10}'
run_start=time.monotonic()
out=ROOT/'rehearsal'/system;out.mkdir(parents=True,exist_ok=True)
status=out/'status.tsv';counts=out/'counts.tsv'
diag=out/'diagnostics'/('fx'+str(int(round_no)-10));diag.mkdir(parents=True,exist_ok=True)
def save_diagnostic(name,data):
 text=data.decode(errors='replace').replace(str(LAB),'LAB_ROOT').replace(str(ROOT),'C1')
 text=re.sub(r'/home/(?!user(?:/|\b)|linuxbrew(?:/|\b)|calops(?:/|\b))[^/\s]+', 'HOST_HOME',text)
 (diag/name).write_text(text)

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
 p=subprocess.Popen(argv,stdin=subprocess.PIPE if data is not None else subprocess.DEVNULL,stdout=subprocess.PIPE if capture else subprocess.DEVNULL,stderr=subprocess.PIPE,start_new_session=True,env={**os.environ,'C1_INLINE_COUNTS':'1','LAB_SEPARATE_STDERR':'1','LAB_ROOT':str(LAB),'LAB_REHEARSAL_COUNTS':str(counts),'LAB_REHEARSAL_ROUND':round_no})
 try:b,err=p.communicate(data,timeout=timeout);rc=p.returncode
 except subprocess.TimeoutExpired:
  os.killpg(p.pid,signal.SIGKILL);b,err=p.communicate();rc=124
 save_diagnostic(label+'.stderr',err or b'')
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
 for i in range(1,21):
  transport_rc,_=run(f'transport-{i:02d}','exit 0\n',60)
  if transport_rc and system in ('nixos','guix'):
   # A failed consecutive sequence cannot pass; retain the failed call and
   # destroy this clone before repairing and trying the next fresh round.
   record('transport-sequence-aborted',transport_rc,0)
   break
 entry={'alma':'alma.sh','void':'void.sh','gentoo':'gentoo.sh','fedora':'lived-developer.sh','mint':'lived-gaming.sh','debian-server':'lived-server.sh'}.get(system)
 if entry:
  buf=io.BytesIO()
  with tarfile.open(fileobj=buf,mode='w:gz') as t:
   for p in sorted((ROOT/'actions').glob('*')):
    if p.is_file() and p.suffix in ('.sh','.py'):t.add(p,arcname=p.name)
  encoded=base64.b64encode(buf.getvalue()).decode()
  rc,_=run('stage-actions','mkdir -p "$HOME/.cal-rehearsal-actions"\nprintf %s '+shlex.quote(encoded)+' | base64 -d | tar -xz -C "$HOME/.cal-rehearsal-actions"\n')
  if rc==0:
   job='#!/bin/bash\nprintf \"%s\\n\" \"$$\" > \"$HOME/.cal-rehearsal-actions/job.sid\"\nbash "$HOME/.cal-rehearsal-actions/'+entry+'"\nrc=$?\nprintf "%s\\n" "$rc" > "$HOME/.cal-rehearsal-actions/done"\n'
   encoded_job=base64.b64encode(job.encode()).decode()
   launch='printf %s '+shlex.quote(encoded_job)+' | base64 -d > "$HOME/.cal-rehearsal-actions/job.sh"\nnohup setsid bash "$HOME/.cal-rehearsal-actions/job.sh" </dev/null >/dev/null 2>&1 &\nprintf "%s\\n" "$!" > "$HOME/.cal-rehearsal-actions/job.pid"\n'
   start=time.monotonic()
   launched,_=run('launch-actions',launch,60)
   action_rc=launched
   if launched==0:
    action_rc=124
    while time.monotonic()-start<int(os.getenv('C1_ACTION_BUDGET','1500')):
     time.sleep(5)
     poll=['%s'% (LAB/'lab.sh'),'run',name,'--timeout','30']
     try:
      done=subprocess.run(poll,input=b'test -f "$HOME/.cal-rehearsal-actions/done" && cat "$HOME/.cal-rehearsal-actions/done"\n',stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=40)
      if done.returncode==0 and done.stdout.strip().isdigit():action_rc=int(done.stdout.strip());break
     except subprocess.TimeoutExpired:pass
   record('actions',action_rc,time.monotonic()-start)
   if action_rc==124:
    stopped,_=run('stop-action-batch','job_session=$(cat "$HOME/.cal-rehearsal-actions/job.sid")\ncase "$job_session" in *[!0-9]*|"") exit 65;; esac\nsudo -n pkill -TERM -s "$job_session" || :\nsleep 3\nsudo -n pkill -KILL -s "$job_session" || :\nfor attempt in 1 2 3 4 5; do\n if sudo -n sh -c \'pgrep -s "$1" >/dev/null; result=$?; case "$result" in 0) exit 10;; 1) exit 11;; *) exit 70;; esac\' sh "$job_session"; then\n  check_status=0\n else\n  check_status=$?\n fi\n case "$check_status" in\n  11) exit 0;;\n  10) sleep 1;;\n  *) echo "action session check failed" >&2; exit 70;;\n esac\ndone\necho "action session remains after termination" >&2\nexit 70\n',30)
    if stopped:raise RuntimeError('Action session termination uncertified; collection refused')
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
   # A timed-out first action may not have written its final status row.
   # Retain stderr for every fixed action name, including incomplete actions.
   for label in sorted(expected[system]):
    _,err=run('fetch-action-stderr-'+label,'cat "$HOME/actions-logs/'+label+'.stderr"\n',60,True)
    save_diagnostic('action-'+label+'.stderr',err)
   run('remove-action-output','rm -rf "$HOME/actions-logs" "$HOME/actions-status.tsv" "$HOME/.cal-rehearsal-actions"\n',60)
 if system not in ('nixos','guix'):
  collector_rc,_=call('collector',[str(ROOT/'collect.sh'),'--rehearsal',name,str(transient)],timeout=1800)
  count('collector:exit-success',int(collector_rc==0))
  if (transient/'coverage.tsv').exists():shutil.copyfile(transient/'coverage.tsv',diag/'coverage.tsv')
  for diagnostic in (transient/'raw').glob('*.err'):save_diagnostic(diagnostic.name,diagnostic.read_bytes())
  if (transient/'coverage.tsv').exists():
   with (transient/'coverage.tsv').open() as f:
    for r in csv.DictReader(f,delimiter='\t'):record('query-'+re.sub(r'packages-flatpak-user-[0-9]+-', 'packages-flatpak-user-', r['query']),int(r['exit_status']),float(r['duration']),int(r['bytes']))
  # Numeric reductions are emitted from collector memory; raw artifacts stay unopened.

except Exception as exc:
 save_diagnostic('reducer.stderr',traceback.format_exc().encode())
 record('reduction-error-'+type(exc).__name__,65,0)
 raise SystemExit(65)
finally:
 shutil.rmtree(transient,ignore_errors=True)
 if created:
  rc,_=call('destroy',[str(LAB/'lab.sh'),'destroy',name],timeout=180)
  if rc:
   call('kill-fallback',[str(LAB/'lab.sh'),'kill',name],timeout=30)
   call('destroy-fallback',[str(LAB/'lab.sh'),'destroy',name],timeout=180)

record('whole-run',0,time.monotonic()-run_start)

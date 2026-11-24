#!/usr/bin/python3
"""BC3 guest transaction and removal assertions; external-root fixture setup."""
import base64,hashlib,json,os,pathlib,re,shutil,socket,subprocess,sys,time
P=pathlib.Path
sys.path.insert(0,'/usr/local/lib/stand')
import stand
OUT=P(sys.argv[1] if len(sys.argv)>1 else '/var/lib/stand/round3.jsonl');OUT.parent.mkdir(parents=True,exist_ok=True)
log=OUT.open('w',buffering=1);failures=[]
HOOK=P('/run/stand-test.json');WORK=P('/var/lib/stand/round3-fixtures');WORK.mkdir(exist_ok=True)
def record(**row):
 row['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());text=json.dumps(row,sort_keys=True);log.write(text+'\n');print(text,flush=True)
def expect(ident,expected,**kw):record(phase='expected',id=ident,expected=expected,source='S3-4; S2.4-4; B1/raw/mechanics-sources.md',**kw)
def result(ident,ok,**kw):
 record(phase='result',id=ident,passed=bool(ok),**kw)
 if not ok:failures.append(ident)
def cmd(args,timeout=180):
 p=subprocess.run(list(map(str,args)),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
 return p
def session(*fields):return cmd(['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-session','-c','\t'.join(map(str,fields))])
def candidate(name,rows):
 d=WORK/name;shutil.copytree(stand.current_dir(),d,dirs_exist_ok=True)
 (d/'machine.jsonl').write_text(''.join(json.dumps(r,sort_keys=True)+'\n' for r in rows));return d
def apply(ident,d):
 expect(ident,'SUCCESS and every-line verification')
 p=cmd(['/usr/local/bin/stand-apply',d]);record(phase='application-output',id=ident,rc=p.returncode,output=p.stdout);v=cmd(['/usr/local/bin/stand-verify'])
 result(ident,p.returncode==0 and p.stdout.startswith('SUCCESS ') and v.returncode==0,rc=p.returncode,output=p.stdout,verify=v.stdout)
 if p.returncode or not p.stdout.startswith('SUCCESS ') or v.returncode:
  record(phase='native-manager-diagnostic',id=ident,failed_units=cmd(['/usr/bin/systemctl','--failed','--no-pager']).stdout,journal=cmd(['/usr/bin/journalctl','-b','-n','100','--no-pager','-o','short-iso-precise']).stdout)
  raise RuntimeError(ident+' application or verification failed')
def values(ident=None):
 p=cmd(['/usr/local/bin/stand-compare','--snapshot','-'])
 try:rows=json.loads(p.stdout)
 except json.JSONDecodeError:
  record(phase='snapshot-diagnostic',id=ident or 'BASELINE',rc=p.returncode,error='snapshot is not JSON',output=p.stdout)
  if ident is None:raise RuntimeError('baseline snapshot is not JSON')
  return None
 if p.returncode:
  bad=[row for row in rows if not row.get('ok')]
  record(phase='snapshot-diagnostic',id=ident or 'BASELINE',rc=p.returncode,mismatches=bad)
  if ident is None:raise RuntimeError('baseline snapshot mismatches: '+','.join(row['id'] for row in bad))
 return rows
def alive(pid):
 try:return P('/proc',str(pid),'stat').read_text().split(') ',1)[1][0]!='Z'
 except FileNotFoundError:return False
def descendants(unit):
 deadline=time.monotonic()+10
 while time.monotonic()<deadline:
  p=cmd(['/usr/bin/systemctl','show',unit,'-p','MainPID','--value'])
  first=int(p.stdout.strip() or 0);seen=set();todo=[first] if first else []
  while todo:
   pid=todo.pop();seen.add(pid)
   try:children=map(int,P('/proc',str(pid),'task',str(pid),'children').read_text().split())
   except FileNotFoundError:children=[]
   todo.extend(x for x in children if x not in seen)
  if len(seen)>=3:return sorted(seen)
  time.sleep(.05)
 return sorted(seen)
def main():
 base=stand.load(stand.current_dir());dev=P('/usr/local/share/stand/dev')
 initial=base+[json.loads((dev/x).read_text()) for x in ('worker-1.json','service.json','rule.json','account.json')]
 apply('TRANSACTION-BASELINE',candidate('baseline',initial))
 modified=[r for r in initial if r['id'] not in ('dev-worker','dev-service','dev-rule','dev-account')]+[json.loads((dev/'worker-2.json').read_text())]
 # Add distinct contributions as well as changing/removing old ones, so the
 # inverse path must delete newly-created identities, files, jobs and rules.
 added_program=json.loads(json.dumps(json.loads((dev/'worker-1.json').read_text())))
 added_program['id']='round3-failure-program'
 for f0 in added_program['files']:f0['path']=f0['path'].replace('/dev-worker/','/round3-failure/')
 added_service=json.loads((dev/'service.json').read_text());added_service['id']='round3-failure-service';added_service['unit']='stand-round3-failure.service'
 added_service['unit_text']=added_service['unit_text'].replace('/dev-worker/','/round3-failure/')
 added_service['unit_sha256']=hashlib.sha256(added_service['unit_text'].encode()).hexdigest()
 added_account=json.loads((dev/'account.json').read_text());added_account.update(id='round3-failure-account',name='round3failure',uid=1888,gid=1888,groups=['round3failure'],home='/home/round3failure')
 added_rule=dict(json.loads((dev/'rule.json').read_text()),id='round3-failure-rule')
 modified += [added_program,added_service,added_account,added_rule]
 target=candidate('failure-candidate',modified)
 def additions_absent():
  import pwd
  try:pwd.getpwnam('round3failure');account_absent=False
  except KeyError:account_absent=True
  rule_text=cmd(['/usr/sbin/nft','list','table','inet','stand']).stdout
  job=cmd(['/usr/bin/systemctl','is-active',added_service['unit']])
  return account_absent and all(not P(f0['path']).exists() for f0 in added_program['files']) and not P('/etc/systemd/system',added_service['unit']).exists() and job.stdout.strip() not in ('active','activating') and 'round3-failure-rule' not in rule_text

 oldgen=stand.current_dir().name;oldreport=P('/var/lib/stand/last-success.json').read_bytes();oldvalues=values()
 def restoration_complete(output):
  ready=P('/run/stand-ready')
  return 'FAILED restored previous declaration:' in output and not P('/var/lib/stand/pending.json').exists() and ready.exists() and ready.read_text().strip()==oldgen and P('/var/lib/stand/last-success.json').read_bytes()==oldreport

 phases=['prepare','frozen','quiesce','files','accounts','rules','policy','jobs','readback','commit-ready']
 for phase in phases:
  ident='FAIL-'+phase.upper();expect(ident,'explicit injected failure; previous generation, report and every actual value restored',checkpoint=phase)
  HOOK.write_text(json.dumps({'fail_at':phase}));HOOK.chmod(0o600)
  try:p=cmd(['/usr/local/bin/stand-apply',target])
  finally:HOOK.unlink(missing_ok=True)
  record(phase='application-output',id=ident,rc=p.returncode,output=p.stdout)
  actual=values(ident);v=cmd(['/usr/local/bin/stand-verify'])
  ok=p.returncode!=0 and 'SUCCESS ' not in p.stdout and restoration_complete(p.stdout) and stand.current_dir().name==oldgen and P('/var/lib/stand/last-success.json').read_bytes()==oldreport and actual==oldvalues and v.returncode==0 and additions_absent()
  result(ident,ok,rc=p.returncode,output=p.stdout,generation=stand.current_dir().name,values_equal=actual==oldvalues,verify_rc=v.returncode,restoration_complete=restoration_complete(p.stdout))
  if not ok:raise RuntimeError(ident+' restoration assertion failed; see application-output and snapshot-diagnostic')
 for phase in ('prepare','files'):
  ident='STALL-'+phase.upper();expect(ident,'watchdog terminates stalled worker and restores exact prior state; test deadline 8 seconds, recovery bounded by 60 seconds',checkpoint=phase,test_timeout_seconds=8)
  HOOK.write_text(json.dumps({'stall_at':phase,'timeout_seconds':8,'deadline_seconds':60}));HOOK.chmod(0o600);start=time.monotonic()
  try:p=cmd(['/usr/local/bin/stand-apply',target],timeout=90)
  finally:HOOK.unlink(missing_ok=True)
  elapsed=time.monotonic()-start
  record(phase='application-output',id=ident,rc=p.returncode,output=p.stdout)
  actual=values(ident);v=cmd(['/usr/local/bin/stand-verify'])
  ok=p.returncode!=0 and 'SUCCESS ' not in p.stdout and restoration_complete(p.stdout) and stand.current_dir().name==oldgen and actual==oldvalues and v.returncode==0 and elapsed<60 and additions_absent()
  result(ident,ok,rc=p.returncode,output=p.stdout,elapsed_seconds=elapsed,values_equal=actual==oldvalues,verify_rc=v.returncode,restoration_complete=restoration_complete(p.stdout))
  if not ok:raise RuntimeError(ident+' restoration assertion failed; see application-output and snapshot-diagnostic')
 ident='WATCHDOG-SUPERVISOR-DEATH'
 expect(ident,'independent systemd timer kills orphaned stalled worker and restores old declaration/report/values within total 60-second test deadline',worker_timeout_seconds=8,total_deadline_seconds=60)
 HOOK.write_text(json.dumps({'stall_at':'files','timeout_seconds':8,'deadline_seconds':60}));HOOK.chmod(0o600)
 phasefile=P('/run/stand-phase');phasefile.unlink(missing_ok=True)
 pending=P('/var/lib/stand/pending.json');started=time.monotonic();worker=None;reached=False
 output=WORK/'watchdog-supervisor-output.log'
 with output.open('w') as stream:
  process=subprocess.Popen(['/usr/local/bin/stand-apply',str(target)],stdout=stream,stderr=subprocess.STDOUT,text=True)
  try:
   while time.monotonic()-started<25 and process.poll() is None:
    if phasefile.exists() and phasefile.read_text().strip()=='files' and pending.exists():
     journal=json.loads(pending.read_text());worker=journal.get('worker')
     if worker and journal.get('supervisor')==process.pid:reached=True;break
    time.sleep(.05)
   if reached:
    os.kill(process.pid,9);process.wait(timeout=5)
    while time.monotonic()-started<60:
     if not pending.exists() and not alive(worker):break
     time.sleep(.1)
   else:
    process.kill();process.wait(timeout=5)
  finally:HOOK.unlink(missing_ok=True)
 elapsed=time.monotonic()-started
 recovered=reached and not pending.exists() and worker is not None and not alive(worker)
 record(phase='application-output',id=ident,rc=process.returncode,output=output.read_text())
 actual=values(ident) if recovered else None
 v=cmd(['/usr/local/bin/stand-verify'])
 ok=recovered and elapsed<60 and stand.current_dir().name==oldgen and P('/var/lib/stand/last-success.json').read_bytes()==oldreport and actual==oldvalues and additions_absent() and v.returncode==0 and 'SUCCESS ' not in output.read_text()
 result(ident,ok,reached_files_checkpoint=reached,supervisor_pid=process.pid,worker_pid=worker,elapsed_seconds=elapsed,pending_exists=pending.exists(),values_equal=actual==oldvalues,verify_rc=v.returncode,output=output.read_text())
 apply('TRANSACTION-CLEANUP',candidate('clean',base))
 # Compiled fixture forks a descendant and leaves both alive until revocation.
 source='#include <unistd.h>\n#include <stdio.h>\nint main(void){fork();printf("HOLDER %ld\\n",(long)getpid());fflush(stdout);for(;;)pause();}\n'
 p=subprocess.run(['/usr/bin/cc','-x','c','-o',str(WORK/'holder'),'-'],input=source,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError('fixture compiler: '+p.stdout)
 data=(WORK/'holder').read_bytes();path='/opt/stand/pkgs/round3/holder'
 f=dict(path=path,kind='file',mode=493,uid=0,gid=0,sha256=hashlib.sha256(data).hexdigest(),content_b64=base64.b64encode(data).decode())
 program=dict(id='round3-program',type='program',version='1',source='selftest-fixture',managed=True,files=[f])
 service='stand-round3.service';timer='stand-round3.timer';sock='stand-round3.socket';sockpath='/run/stand-sockets/round3.sock'
 def unit(ident,typ,name,text):return dict(id=ident,type=typ,managed=True,unit=name,enabled='enabled',active=True,unit_text=text,unit_sha256=hashlib.sha256(text.encode()).hexdigest())
 service_row=unit('round3-service','service',service,'[Unit]\nDescription=Removal fixture\n[Service]\nType=simple\nUser=stand\nExecStart='+path+'\nRestart=no\nKillMode=control-group\nTimeoutStopSec=5\nMemoryDenyWriteExecute=yes\nNoNewPrivileges=yes\nProtectSystem=strict\nPrivateTmp=yes\n[Install]\nWantedBy=multi-user.target\n')
 timer_row=unit('round3-timer','timer',timer,'[Unit]\nDescription=Removal timer\n[Timer]\nOnUnitActiveSec=1s\nUnit='+service+'\nPersistent=false\n[Install]\nWantedBy=timers.target\n')
 socket_row=unit('round3-socket','socket',sock,'[Unit]\nDescription=Removal socket\n[Socket]\nListenStream='+sockpath+'\nService='+service+'\nAccept=no\nRemoveOnStop=yes\nSocketMode=0600\n[Install]\nWantedBy=sockets.target\n')
 rule=dict(json.loads((dev/'rule.json').read_text()),id='round3-rule')
 apply('REMOVAL-ADMIT',candidate('removal',base+[program,service_row,timer_row,socket_row,rule]))
 oldpids=descendants(service);copy=P('/home/stand/round3-retained');shutil.copy2(path,copy);os.chown(copy,1000,1000)
 retained_root=P('/var/lib/stand/code-root')/path.lstrip('/');cache=P('/home/stand/round3-cache');shutil.copy2(path,cache);os.chown(cache,1000,1000)
 expect('REMOVAL-PRECONDITIONS','running service parent/descendants, active timer/socket and effective rule',pids=oldpids)
 result('REMOVAL-PRECONDITIONS',len(oldpids)>=3 and P(sockpath).exists(),pids=oldpids,socket_exists=P(sockpath).exists())
 expect('SOCKET-ACTIVATION-POSITIVE','recorded socket starts stopped service before removal')
 cmd(['/usr/bin/systemctl','stop',timer]);cmd(['/usr/bin/systemctl','stop',service])
 connection=socket.socket(socket.AF_UNIX)
 try:connection.connect(sockpath)
 finally:connection.close()
 activated=descendants(service);cmd(['/usr/bin/systemctl','start',timer])
 result('SOCKET-ACTIVATION-POSITIVE',len(activated)>=3,pids=activated)
 oldpids=activated
 apply('REMOVAL-APPLY',candidate('removed',base))
 expect('REMOVAL-CONTRIBUTIONS','all holders dead; no original or snapshot file; no socket; all activators inactive/disabled; rule absent')
 states={u:{k:cmd(['/usr/bin/systemctl','is-'+k,u]).stdout.strip() for k in ('active','enabled')} for u in (service,timer,sock)}
 nft=cmd(['/usr/sbin/nft','list','table','inet','stand'])
 ok=bool(oldpids) and not any(alive(x) for x in oldpids) and not P(path).exists() and not retained_root.exists() and not P(sockpath).exists() and 'round3-rule' not in nft.stdout and all(x['active'] not in ('active','activating') and x['enabled'] not in ('enabled','enabled-runtime') for x in states.values())
 result('REMOVAL-CONTRIBUTIONS',ok,pids=oldpids,states=states,nft=nft.stdout)
 for label,entry in [('ORIGINAL',path),('COPY',copy),('SNAPSHOT',retained_root),('CACHE-COPY',cache)]:
  expect('REMOVED-'+label,'ordinary launcher refuses retained or removed contribution');p=session('run',entry);result('REMOVED-'+label,p.returncode!=0,rc=p.returncode,output=p.stdout)
 for frontend,args in [('systemctl',['start',service]),('systemctl',['start',timer]),('systemctl',['start',sock]),('podman',['start','round3-retained'])]:
  ident='REACTIVATE-'+args[-1];expect(ident,'removed activation request refuses');p=session('broker',frontend,*args);result(ident,p.returncode!=0,rc=p.returncode,output=p.stdout)
 expect('REMOVED-SOCKET-CONNECT','connection cannot reactivate removed service')
 connection=socket.socket(socket.AF_UNIX);denied=False
 try:connection.connect(sockpath)
 except OSError:denied=True
 finally:connection.close()
 result('REMOVED-SOCKET-CONNECT',denied)
 # Every overlapping line explicitly states the full required contribution.
 # Removing the original owners must preserve jobs, identity, code and rule;
 # only removing the last owners revokes all of those contributions.
 import pwd
 shared_account=dict(json.loads((dev/'account.json').read_text()),id='round3-shared-account')
 originals=[program,service_row,timer_row,socket_row,shared_account,rule]
 overlaps=[dict(row,id=row['id']+'-overlap') for row in originals]
 apply('SHARED-ADMIT',candidate('shared',base+originals+overlaps))
 apply('SHARED-REMOVE-ONE',candidate('shared-one',base+overlaps))
 expect('SHARED-RETAINED','remaining explicit lines preserve exact file/launch membership, active enabled service/timer/socket, account and effective rule')
 table=P('/etc/stand/launch.tsv').read_text();shared_pids=descendants(service)
 states={u:{k:cmd(['/usr/bin/systemctl','is-'+k,u]).stdout.strip() for k in ('active','enabled')} for u in (service,timer,sock)}
 nft=cmd(['/usr/sbin/nft','list','table','inet','stand'])
 try:account=pwd.getpwnam(shared_account['name']);account_matches=account.pw_uid==shared_account['uid'] and account.pw_gid==shared_account['gid']
 except KeyError:account_matches=False
 kept=P(path).exists() and P(path).read_bytes()==data and path in table and len(shared_pids)>=3 and P(sockpath).exists() and account_matches and all(x['active']=='active' and x['enabled']=='enabled' for x in states.values()) and 'round3-rule-overlap' in nft.stdout and rule['expression'] in nft.stdout
 result('SHARED-RETAINED',kept,pids=shared_pids,states=states,account_matches=account_matches,nft=nft.stdout)
 apply('SHARED-REMOVE-LAST',candidate('shared-none',base))
 expect('SHARED-LAST-REVOKED','last explicit coverage removal stops descendants, removes code/account/socket/rules/activators, and denies launch')
 p=session('run',path)
 states={u:{k:cmd(['/usr/bin/systemctl','is-'+k,u]).stdout.strip() for k in ('active','enabled')} for u in (service,timer,sock)}
 nft=cmd(['/usr/sbin/nft','list','table','inet','stand'])
 try:pwd.getpwnam(shared_account['name']);account_absent=False
 except KeyError:account_absent=True
 gone=p.returncode!=0 and not P(path).exists() and not retained_root.exists() and not P(sockpath).exists() and bool(shared_pids) and not any(alive(pid) for pid in shared_pids) and account_absent and 'round3-rule' not in nft.stdout and rule['expression'] not in nft.stdout and all(x['active'] not in ('active','activating') and x['enabled'] not in ('enabled','enabled-runtime') for x in states.values())
 result('SHARED-LAST-REVOKED',gone,rc=p.returncode,output=p.stdout,pids=shared_pids,states=states,account_absent=account_absent,nft=nft.stdout)
 # Remove readiness marker as an operator fixture; no ordinary session may pass.
 ready=P('/run/stand-ready');saved=ready.read_bytes() if ready.exists() else None
 expect('SESSION-REPLAY-GATE','ordinary launcher refuses when replay readiness is absent')
 ready.unlink(missing_ok=True)
 try:p=session('run','/usr/bin/cat','/etc/os-release')
 finally:
  if saved is not None:ready.write_bytes(saved)
 result('SESSION-REPLAY-GATE',p.returncode!=0,rc=p.returncode,output=p.stdout)
 record(phase='summary',passed=not failures,failures=failures)
 return bool(failures)
if __name__=='__main__':
 try:sys.exit(main())
 finally:HOOK.unlink(missing_ok=True)

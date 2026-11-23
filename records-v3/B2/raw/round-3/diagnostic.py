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
 p=cmd(['/usr/local/bin/stand-apply',d]);v=cmd(['/usr/local/bin/stand-verify'])
 result(ident,p.returncode==0 and p.stdout.startswith('SUCCESS ') and v.returncode==0,rc=p.returncode,output=p.stdout,verify=v.stdout)
 if p.returncode:raise RuntimeError(ident+' failed')
def values():
 p=cmd(['/usr/local/bin/stand-compare','--snapshot','-'])
 if p.returncode:raise RuntimeError('snapshot failed '+p.stdout)
 return json.loads(p.stdout)
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

 HOOK.write_text(json.dumps({'fail_at':'frozen'}));HOOK.chmod(0o600)
 try:
  p=cmd(['/usr/local/bin/stand-apply',target]);print('DIAGNOSTIC APPLY',p.returncode,p.stdout,flush=True)
 finally:HOOK.unlink(missing_ok=True)
 print(cmd(['/usr/bin/systemctl','status','stand-development.service','--no-pager']).stdout,flush=True)
 print(cmd(['/usr/bin/journalctl','-u','stand-development.service','-u','stand-watchdog.service','--no-pager','-n','100']).stdout,flush=True)
 print('PENDING',P('/var/lib/stand/pending.json').read_text() if P('/var/lib/stand/pending.json').exists() else 'absent',flush=True)
main()

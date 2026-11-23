#!/usr/bin/env python3
"""Single-use BC3 server evidence driver, including independent recipe peer."""
import argparse,base64,hashlib,importlib.util,json,os,pathlib,shlex,subprocess,sys,threading,time
P=pathlib.Path;ROOT=P(__file__).resolve().parent.parent
parser=argparse.ArgumentParser();parser.add_argument('phase');parser.add_argument('--peer-root',type=P);parser.add_argument('--skip-regressions',action='store_true');args=parser.parse_args()
if not args.phase.replace('-','').isalnum():parser.error('safe single-use phase required')
OUT=ROOT/'raw'/'round-3'/args.phase;OUT.mkdir(parents=True,exist_ok=False)
status=0;created=[]
def event(**row):
 row['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());print(json.dumps(row,sort_keys=True),flush=True)
def run(argv,log,script=None,root=ROOT,check=True):
 global status
 with (OUT/log).open('wb') as stream:
  p=subprocess.run(list(map(str,argv)),input=script.encode() if isinstance(script,str) else script,stdout=stream,stderr=subprocess.STDOUT,cwd=root,env={**os.environ,'STAND_ROOT':str(root),'PYTHONDONTWRITEBYTECODE':'1','STAND_EVIDENCE_DIR':'round-3/'+args.phase+'/original'})
 event(log=log,rc=p.returncode)
 if check and p.returncode:status=1
 return p.returncode
def lab(name,op,log,script=None,root=ROOT,extra=()):return run([sys.executable,root/'lab.py',op,name,*extra],log,script,root)
def new(name,root=ROOT):
 created.append((root,name))
 if lab(name,'new',name+'-new.log',root=root,extra=['stand']):raise RuntimeError('fresh VM failed')
def guest(name,script,log,root=ROOT):return lab(name,'run',log,script,root,extra=['--root'])
def deliver(name,filename):
 data=base64.b64encode((ROOT/'build'/filename).read_bytes()).decode()
 return guest(name,"python3 -I - <<'COPY'\nimport base64,pathlib\npathlib.Path('/tmp/"+filename+"').write_bytes(base64.b64decode('"+data+"'))\nCOPY\n",name+'-copy-'+filename+'.log')
def cleanup(root,name):
 if not (root/'vms'/name).exists():return
 if lab(name,'destroy',name+'-destroy.log',root=root):
  lab(name,'kill',name+'-kill.log',root=root);lab(name,'destroy',name+'-destroy-after-kill.log',root=root)
 created.remove((root,name))
def boot_gate(name):
 global status
 expect='delayed replay prevents all successful ordinary SSH commands until replay completion'
 event(phase='expected',id='BOOT-SESSION-GATE',expected=expect,source='S3-5; systemd unit ordering; B2/build/round3-driver.py')
 guest(name,"set -eu\nmkdir -p /etc/systemd/system/stand-replay.service.d\nprintf '[Service]\\nExecStartPre=/usr/bin/sleep 8\\n' > /etc/systemd/system/stand-replay.service.d/round3-test.conf\n/usr/bin/systemctl daemon-reload\n",'boot-delay-setup.log')
 lab(name,'stop','boot-gate-stop.log')
 spec=importlib.util.spec_from_file_location('round3_lab',ROOT/'lab.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 vm=ROOT/'vms'/name
 with (OUT/'boot-start.log').open('wb') as stream:
  starter=subprocess.Popen([sys.executable,str(ROOT/'lab.py'),'start',name],stdout=stream,stderr=subprocess.STDOUT)
  observations=[];deadline=time.monotonic()+240;premature=False;ready_seen=False;pre_ready_attempts=0;pre_ready_successes=0
  while starter.poll() is None and time.monotonic()<deadline:
   try:
    rootq=subprocess.run(module.ssh(vm,root=True)+['if test -f /run/stand-ready; then printf BOOT_READY; else printf PREMATURE_SESSION; exit 99; fi'],stdin=subprocess.DEVNULL,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=5)
    premature |= 'PREMATURE_SESSION' in rootq.stdout
    ready_seen |= rootq.returncode==0 and rootq.stdout=='BOOT_READY'
    observations.append({'monotonic':time.monotonic(),'kind':'operator-login','rc':rootq.returncode,'output':rootq.stdout})
   except subprocess.TimeoutExpired:observations.append({'monotonic':time.monotonic(),'kind':'operator-login','rc':'timeout'})
   before_ready=not ready_seen
   if before_ready:pre_ready_attempts+=1
   try:
    q=subprocess.run(module.ssh(vm),input='run\t/usr/bin/cat\t/etc/os-release\n',text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=5)
    if before_ready and q.returncode==0:pre_ready_successes+=1
    observations.append({'monotonic':time.monotonic(),'kind':'ordinary-login','before_observed_ready':before_ready,'rc':q.returncode,'output':q.stdout})
   except subprocess.TimeoutExpired:observations.append({'monotonic':time.monotonic(),'kind':'ordinary-login','before_observed_ready':before_ready,'rc':'timeout'})
   time.sleep(.2)
  if starter.poll() is None:starter.terminate();starter.wait();status=1
  elif starter.returncode:status=1
 passed=not premature and pre_ready_attempts>0 and pre_ready_successes==0
 event(phase='result',id='BOOT-SESSION-GATE',passed=passed,pre_ready_ordinary_attempts=pre_ready_attempts,pre_ready_ordinary_successes=pre_ready_successes,premature_operator_session=premature)
 if not passed:status=1
 (OUT/'boot-attempts.json').write_text(json.dumps(observations,indent=2)+'\n')
 # PAM account gating prevents every SSH login while port 22 remains available
 # to replay verification; the ordinary launcher independently checks readiness.
 check="""python3 -I - <<'CHECK'
import json,pathlib,subprocess
get=lambda u,p:int(subprocess.check_output(['/usr/bin/systemctl','show',u,'-p',p,'--value'],text=True).strip() or 0)
r=get('stand-replay.service','ActiveEnterTimestampMonotonic');s=get('ssh.service','ActiveEnterTimestampMonotonic')
pam=pathlib.Path('/etc/pam.d/common-account').read_text()
gate=any('account' in line and 'requisite' in line and 'pam_exec.so' in line and '/run/stand-ready' in line for line in pam.splitlines() if not line.lstrip().startswith('#'))
print(json.dumps({'id':'BOOT-ORDER','replay_ready_us':r,'ssh_active_us':s,'ready_marker':pathlib.Path('/run/stand-ready').exists(),'pam_account_gate':gate,'passed':r>0 and gate}))
assert r>0 and gate and pathlib.Path('/run/stand-ready').exists()
for u in ('getty@.service','systemd-logind.service','systemd-user-sessions.service'):
 p=subprocess.check_output(['/usr/bin/systemctl','show',u,'-p','After','-p','Requires'],text=True)
 print(u,p)
 assert 'stand-replay.service' in p
CHECK
"""
 guest(name,check,'boot-order.jsonl')
 guest(name,'rm /etc/systemd/system/stand-replay.service.d/round3-test.conf\n/usr/bin/systemctl daemon-reload\n','boot-delay-cleanup.log')
try:
 name='bc3-'+args.phase;new(name);deliver(name,'round3-selftest.py')
 if guest(name,'python3 -B /tmp/round3-selftest.py\n','round3.jsonl'):raise RuntimeError('transaction selftest failed; aborting dependent boot/power-cut branch')
 boot_gate(name)
 run([sys.executable,ROOT/'build/round3-cut.py',name],'powercuts.jsonl')
 cleanup(ROOT,name)
 name='bc3-inventory-'+args.phase;new(name);deliver(name,'round3-inventory-test.py');guest(name,'python3 -B /tmp/round3-inventory-test.py\n','inventory.jsonl');cleanup(ROOT,name)
 if not args.skip_regressions:
  run([sys.executable,ROOT/'build/development.py'],'original-console.log')
  for suite in (1,2):
   name='bc3-regression'+str(suite)+'-'+args.phase;new(name);deliver(name,'round'+str(suite)+'-selftest.py')
   if suite==2:deliver(name,'round2-probe.c')
   guest(name,'python3 -B /tmp/round'+str(suite)+'-selftest.py\n','round'+str(suite)+'.jsonl');cleanup(ROOT,name)
 if args.peer_root:
  peer=args.peer_root.resolve()
  if peer==ROOT:raise RuntimeError('independent build root must differ')
  event(phase='expected',id='INDEPENDENT-RECIPE-COMPARE',expected='byte-identical complete declaration and equal every-line values on separately rebuilt images')
  for root,name,label in [(ROOT,'bc3-peer-a','a'),(peer,'bc3-peer-b','b')]:
   new(name,root)
   guest(name,'python3 -B /usr/local/lib/stand/selftest.py add\n','peer-'+label+'-apply.log',root)
   lab(name,'copy-out','peer-'+label+'-snapshot-export.log',root=root,extra=['/var/lib/stand/evidence/added.json',root/'raw'/'round3-peer-export'])
   lab(name,'copy-out','peer-'+label+'-declaration-export.log',root=root,extra=['/var/lib/stand/dev-add',root/'raw'/'round3-peer-export'])
   import shutil
   dest=OUT/('peer-'+label);shutil.copytree(root/'raw'/'round3-peer-export',dest);shutil.rmtree(root/'raw'/'round3-peer-export')
   if label=='b':
    comparison_script="python3 -I - <<'SNAPSHOTS'\nimport base64,pathlib\n"
    for snapshot_label in ('a','b'):
     encoded=base64.b64encode((OUT/('peer-'+snapshot_label)/'added.json').read_bytes()).decode()
     comparison_script+="pathlib.Path('/tmp/round3-peer-"+snapshot_label+".json').write_bytes(base64.b64decode('"+encoded+"'))\n"
    comparison_script+="SNAPSHOTS\nstand-compare /tmp/round3-peer-a.json /tmp/round3-peer-b.json\n"
    guest(name,comparison_script,'independent-stand-compare.jsonl',root)
   cleanup(root,name)
  a=OUT/'peer-a/dev-add';b=OUT/'peer-b/dev-add';same={p.name:p.read_bytes() for p in a.iterdir()}=={p.name:p.read_bytes() for p in b.iterdir()}
  av=json.loads((OUT/'peer-a/added.json').read_text());bv=json.loads((OUT/'peer-b/added.json').read_text());equal=av==bv
  (OUT/'independent-compare.json').write_text(json.dumps({'declaration_bytes_equal':same,'values_equal':equal,'left':av,'right':bv},indent=2)+'\n')
  if not same or not equal:status=1
 else:
  event(id='INDEPENDENT-RECIPE-COMPARE',passed=False,reason='peer root not provided; not tested');status=1
except BaseException:
 status=1
 raise
finally:
 for root,name in list(created):cleanup(root,name)
 with (ROOT/'base/stand.qcow2').open('rb') as stream:sha=hashlib.file_digest(stream,'sha256').hexdigest()
 (OUT/'summary.json').write_text(json.dumps({'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'suite_exit':status,'image_sha256':sha,'regressions_run':not args.skip_regressions,'independent_peer_supplied':bool(args.peer_root),'vms_remaining':[p.name for p in (ROOT/'vms').glob('*')]},indent=2)+'\n')
sys.exit(status)

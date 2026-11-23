#!/usr/bin/env python3
"""Nine report-triggered hard cuts, with complete post-replay readback."""
import importlib.util,json,os,pathlib,signal,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('lab',ROOT/'lab.py');lab=importlib.util.module_from_spec(spec);spec.loader.exec_module(lab)
vm=lab.ROOT/'vms'/sys.argv[1]
def event(**kw):
 kw['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());print(json.dumps(kw,sort_keys=True),flush=True)
def guest(script):
 subprocess.run([sys.executable,str(ROOT/'lab.py'),'run',vm.name,'--root'],input=script.encode(),check=True)
for trial in range(1,4):
 for phase in ('add','change','remove'):
  ident='POWER-'+phase.upper()+'-'+str(trial)
  event(phase='expected',id=ident,expected='SIGKILL at first SUCCESS marker; selected generation and every required line survive boot',source='S3-5; B1/raw/mechanics-sources.md')
  guest('python3 -B /usr/local/lib/stand/selftest.py prepare-'+phase+'\n')
  command=([] if lab.meta(vm).get('operator_user') else ['sudo','-n'])+['/usr/local/bin/stand-apply','/var/lib/stand/cut-'+phase]
  import shlex
  proc=subprocess.Popen(lab.ssh(vm,root=True)+[shlex.join(command)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
  seen=False
  for line in proc.stdout:
   if line.startswith('SUCCESS '):
    received=time.monotonic_ns();reported=line.split()[1];pid=lab.live(vm)
    if not pid:raise RuntimeError('VM disappeared before cut')
    os.kill(pid,signal.SIGKILL);cut=time.monotonic_ns();seen=True
    event(phase='cut',id=ident,reported=reported,signal='SIGKILL',delay_ms=(cut-received)/1e6)
    break
   print(line,end='',flush=True)
  proc.wait(timeout=20)
  if not seen:raise RuntimeError('no success marker; no cut performed')
  limit=time.monotonic()+10
  while lab.live(vm) and time.monotonic()<limit:time.sleep(.05)
  subprocess.run([sys.executable,str(ROOT/'lab.py'),'start',vm.name],check=True)
  guest('set -eu\ntest "$(basename "$(readlink -f /var/lib/stand/current)")" = '+reported+'\nstand-verify\npython3 -I - <<\'VERIFY\'\nimport json,pathlib\nr=json.loads(pathlib.Path("/var/lib/stand/last-success.json").read_text())\nassert r["declaration"] == "'+reported+'"\nassert not pathlib.Path("/var/lib/stand/pending.json").exists()\nVERIFY\n')
  event(phase='result',id=ident,passed=True,reported=reported)

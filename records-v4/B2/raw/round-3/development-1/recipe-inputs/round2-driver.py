#!/usr/bin/env python3
"""Complete BC2 server evidence driver; each phase is single use."""
import hashlib,json,os,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
phase=sys.argv[1];out=ROOT/'raw'/phase
if not phase.replace('-','').isalnum():raise SystemExit('safe phase required')
out.mkdir(parents=True,exist_ok=False)
def run(args,log,script=None):
 with (out/log).open('wb') as stream:
  p=subprocess.run(list(map(str,args)),cwd=ROOT,input=script,stdout=stream,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','STAND_EVIDENCE_DIR':phase+'/original'})
 print(log+' EXIT '+str(p.returncode),flush=True);return p.returncode
status=0
name='bc2-'+phase
existing=phase.startswith('integration')
if existing:name='bc2-integration'
try:
 if not existing:status|=run([sys.executable,ROOT/'lab.py','new',name,'stand'],'new.log')
 m=json.loads((ROOT/'vms'/name/'meta.json').read_text())
 base=['-F','/dev/null','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','-i',str(ROOT/'keys/guest')]
 status|=run(['scp',*base,'-P',str(m['port']),ROOT/'build/round2-selftest.py',ROOT/'build/round2-probe.c','root@127.0.0.1:/tmp/'],'test-input-copy.log')
 status|=run([sys.executable,ROOT/'lab.py','run',name,'--root'],'round2.jsonl',b'python3 -B /tmp/round2-selftest.py /var/lib/stand/round2.jsonl\n')
 status|=run([sys.executable,ROOT/'lab.py','run',name],'ordinary-ssh.log',b'run\t/usr/bin/cat\t/etc/os-release\n')
 denied=run([sys.executable,ROOT/'lab.py','run',name],'ordinary-shell-refusal.log',b'python3 -c "print(12345)"\n')
 status|=int(denied==0)
 status|=run([sys.executable,ROOT/'lab.py','run',name,'--root'],'policy-state.log',b'''date -u +%FT%TZ
uname -r
cat /sys/kernel/security/lsm
cat /proc/sys/kernel/yama/ptrace_scope
cat /etc/stand/launch.tsv
cat /var/lib/stand/policy-status.json
/usr/sbin/sshd -T -C user=stand,host=localhost,addr=127.0.0.1 | /usr/bin/grep -E 'permituserrc|permituserenvironment|disableforwarding'
/usr/bin/readelf -l /usr/local/bin/stand-session
/usr/bin/systemctl is-active stand-replay.service
''')
finally:
 if not existing and (ROOT/'vms'/name).exists():
  if run([sys.executable,ROOT/'lab.py','destroy',name],'destroy.log'):
   run([sys.executable,ROOT/'lab.py','kill',name],'kill.log');run([sys.executable,ROOT/'lab.py','destroy',name],'destroy-after-kill.log')
if not existing:
 status|=run([sys.executable,ROOT/'build/development.py'],'original-console.log')
 name='bc1-'+phase
 try:
  status|=run([sys.executable,ROOT/'lab.py','new',name,'stand'],'round1-new.log')
  status|=run([sys.executable,ROOT/'lab.py','run',name,'--root'],'round1.jsonl',b'#!/usr/bin/python3 -I\n'+(ROOT/'build/round1-selftest.py').read_bytes())
 finally:
  if (ROOT/'vms'/name).exists():
   if run([sys.executable,ROOT/'lab.py','destroy',name],'round1-destroy.log'):
    run([sys.executable,ROOT/'lab.py','kill',name],'round1-kill.log');run([sys.executable,ROOT/'lab.py','destroy',name],'round1-destroy-after-kill.log')
with (ROOT/'base/stand.qcow2').open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
(out/'summary.json').write_text(json.dumps({'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'suite_exit':status,'image_sha256':sha,'vms_remaining':[p.name for p in (ROOT/'vms').glob('*')]},indent=2)+'\n')
raise SystemExit(status)

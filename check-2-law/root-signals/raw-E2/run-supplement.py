#!/usr/bin/python3
import datetime,json,os,pathlib,pty,select,shlex,subprocess,time,traceback
BASE=pathlib.Path('<WORKDIR>/E2');RAW=BASE/'raw-E2'
SSH=['ssh','-F','/dev/null','-i',str(BASE.parent/'B/id_ed25519'),'-o','BatchMode=yes','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(BASE/'known_hosts'),'-o','ConnectTimeout=5','-p','22292']
P='/usr/bin/python3 /usr/local/lib/e2/probe.py '
def record(d):
 d['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (RAW/'commands.jsonl').open('a') as f:f.write(json.dumps(d)+'\n')
def run(label,cmd,user='root',tty=False,timeout=45):
 a=SSH+(['-tt'] if tty else ['-T'])+[user+'@127.0.0.1',cmd]
 try:
  q=subprocess.run(a,capture_output=True,text=True,timeout=timeout);d={'label':label,'argv':a,'command':cmd,'rc':q.returncode,'stdout':q.stdout,'stderr':q.stderr}
 except subprocess.TimeoutExpired as e:d={'label':label,'argv':a,'command':cmd,'timeout':timeout,'stdout':str(e.stdout),'stderr':str(e.stderr)}
 (RAW/(label+'.txt')).write_text(d.get('stdout','')+'\nSTDERR\n'+d.get('stderr',''));record(d);print(label,d.get('rc','TIMEOUT'),flush=True);return d
class Interactive:
 def __init__(self,label,user='e2op'):
  self.label=label;self.master,slave=pty.openpty();self.data=bytearray();self.cursor=0
  self.argv=SSH+['-tt',user+'@127.0.0.1','env PS1=E2PROMPT\>\  bash --noprofile --norc -i']
  self.p=subprocess.Popen(self.argv,stdin=slave,stdout=slave,stderr=slave,start_new_session=True);os.close(slave)
 def wait(self,needle,seconds=30):
  end=time.monotonic()+seconds
  while time.monotonic()<end:
   found=self.data.find(needle,self.cursor)
   if found>=0:self.cursor=found+len(needle);return
   ready,_,_=select.select([self.master],[],[],min(1,max(0,end-time.monotonic())))
   if ready:
    try:b=os.read(self.master,65536)
    except OSError:break
    if not b:break
    self.data.extend(b)
  raise RuntimeError('missing prompt '+repr(needle)+' tail='+repr(self.data[-1000:]))
 def send(self,s):os.write(self.master,s.encode()+b'\n')
 def close(self):
  try:self.send('exit');self.p.wait(timeout=4)
  except Exception:self.p.terminate();self.p.wait(timeout=4)
  os.close(self.master);(RAW/(self.label+'.txt')).write_bytes(self.data);record({'label':self.label,'argv':self.argv,'controller':'server Python pty driver; no human input','rc':self.p.returncode,'transcript':self.label+'.txt'})
run('schedule-cron',"printf '%s\\n' '* * * * * root test -f /var/lib/e2/probes/cron-root.json || /usr/bin/python3 /usr/local/lib/e2/probe.py cron-root >/var/lib/e2/cron-root-output.txt 2>&1' '* * * * * e2op test -f /var/lib/e2/probes/cron-setuid.json || /usr/local/lib/e2/suid-helper cron-setuid >/tmp/e2-cron-setuid-output.txt 2>&1' >/etc/cron.d/e2-probe; chmod 644 /etc/cron.d/e2-probe")
run('expect-sudo-fixed','/usr/local/lib/e2/expect-auth.exp sudo expect-sudo-fixed',user='e2op')
run('expect-polkit-fixed','/usr/local/lib/e2/expect-auth.exp polkit expect-polkit-fixed',user='e2op',timeout=40)
# NOPASSWD is a separate, explicitly configured route; restore password policy.
run('enable-nopasswd',"printf '%s\\n' 'e2op ALL=(root) NOPASSWD: /usr/bin/python3 /usr/local/lib/e2/probe.py sudo-nopasswd' >/etc/sudoers.d/zz-e2-nopasswd; chmod 440 /etc/sudoers.d/zz-e2-nopasswd; visudo -c")
run('sudo-nopasswd','sudo -K; sudo -n '+P+'sudo-nopasswd',user='e2op')
run('disable-nopasswd','rm /etc/sudoers.d/zz-e2-nopasswd; visudo -c')
# A live automated login session is the destination for an explicit cgroup write.
anchor=subprocess.Popen(SSH+['-tt','e2op@127.0.0.1','echo $$ >/tmp/e2-anchor-pid; cat /proc/self/cgroup >/tmp/e2-anchor-cgroup; sleep 120'],stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
try:
 time.sleep(1)
 run('service-cgroup-move','cat /tmp/e2-anchor-cgroup; systemd-run --unit=e2-cgroup --wait --pipe /usr/bin/python3 /usr/local/lib/e2/cgroup-move.py service-cgroup-move')
finally:
 anchor.terminate()
 try:out,err=anchor.communicate(timeout=5)
 except subprocess.TimeoutExpired:anchor.kill();out,err=anchor.communicate()
 record({'label':'anchor-session','rc':anchor.returncode,'stdout':out.decode(errors='replace'),'stderr':err.decode(errors='replace')})
# Immutable audit loginuid: distinguish changing an existing value and first set.
run('enable-loginuid-immutable','auditctl --loginuid-immutable; auditctl -s')
run('immutable-rewrite','/usr/bin/python3 /usr/local/lib/e2/loginuid-write.py immutable-rewrite 1102')
run('immutable-service-first-set','systemd-run --unit=e2-immutable-first --wait --pipe /usr/bin/python3 /usr/local/lib/e2/loginuid-write.py immutable-service-first-set 1102')
run('immutable-inherited-setuid','/usr/local/lib/e2/suid-helper immutable-inherited-setuid',user='e2op',tty=True)
# Limit this wait to one cron boundary plus scheduling margin; progress printed.
for attempt in range(15):
 q=run('cron-readiness-'+str(attempt),'test -f /var/lib/e2/probes/cron-root.json && test -f /var/lib/e2/probes/cron-setuid.json')
 if q.get('rc')==0:break
 time.sleep(5)
run('stop-cron-probes','rm -f /etc/cron.d/e2-probe; cat /var/lib/e2/cron-root-output.txt /tmp/e2-cron-setuid-output.txt 2>/dev/null')
run('matrix-after','auditctl -s; auditctl -l; date -Is; find /var/lib/e2/probes -type f -printf "%f\\n" | sort; ps -eo pid,ppid,uid,euid,tty,args')
print('MATRIX_DONE',flush=True)

#!/usr/bin/python3
import datetime,json,os,pathlib,re,subprocess,sys,time
label=sys.argv[1]
if not re.fullmatch(r'[a-z0-9_-]+',label): raise SystemExit('bad label')
def read(p):
 try: return pathlib.Path(p).read_text().strip()
 except OSError as e: return {'error':str(e)}
def link(p):
 try: return os.readlink(p)
 except OSError as e: return {'error':str(e)}
def proc(pid):
 d={'pid':pid}
 try:
  s=pathlib.Path(f'/proc/{pid}/stat').read_text(); end=s.rfind(')'); f=s[end+2:].split()
  d.update(comm=s[s.find('(')+1:end],ppid=int(f[1]),pgrp=int(f[2]),posix_sid=int(f[3]),tty_nr=int(f[4]),starttime_ticks=int(f[19]))
  d['exe']=link(f'/proc/{pid}/exe'); d['cmdline']=pathlib.Path(f'/proc/{pid}/cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
  d['cgroup']=read(f'/proc/{pid}/cgroup');d['loginuid']=read(f'/proc/{pid}/loginuid');d['audit_sessionid']=read(f'/proc/{pid}/sessionid')
  d['status']={x.split(':',1)[0]:x.split(':',1)[1].strip() for x in pathlib.Path(f'/proc/{pid}/status').read_text().splitlines() if x.startswith(('Uid:','Gid:','Cap','NoNewPrivs:','Seccomp:'))}
 except OSError as e: d['error']=str(e)
 return d
p=proc(os.getpid()); chain=[]; seen=set(); parent=p.get('ppid',0)
while parent and parent not in seen and len(chain)<20:
 seen.add(parent); a=proc(parent); chain.append(a); parent=a.get('ppid',0)
fds={}
for fd in (0,1,2):
 fds[str(fd)]={'link':link(f'/proc/self/fd/{fd}'),'isatty':os.isatty(fd)}
 try: fds[str(fd)]['ttyname']=os.ttyname(fd)
 except OSError: pass
try:
 tty=os.open('/dev/tty',os.O_RDWR|os.O_NOCTTY); tty_info={'open':True,'ttyname':os.ttyname(tty),'foreground_pgrp':os.tcgetpgrp(tty)};os.close(tty)
except OSError as e: tty_info={'open':False,'error':str(e)}
marker=pathlib.Path('/var/lib/e2/markers')/(label+'.txt')
try: marker.write_text(f'{label} pid={os.getpid()} ruid={os.getuid()} euid={os.geteuid()}\n');mark={'ok':True,'path':str(marker)}
except OSError as e:mark={'ok':False,'error':str(e)}
r={'label':label,'controller':'automation','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'monotonic':time.monotonic(),'uids':os.getresuid(),'gids':os.getresgid(),'target':p,'ancestors':chain,'fds':fds,'controlling_tty':tty_info,'lsm':read('/proc/self/attr/current'),'marker':mark,'environment':{k:os.environ.get(k) for k in ('SUDO_USER','SUDO_UID','SUDO_COMMAND','PKEXEC_UID','XDG_SESSION_ID','SSH_TTY')}}
if os.environ.get('XDG_SESSION_ID'):
 q=subprocess.run(['loginctl','show-session',os.environ['XDG_SESSION_ID'],'--no-pager'],text=True,capture_output=True); r['logind']={'rc':q.returncode,'stdout':q.stdout,'stderr':q.stderr}
q=subprocess.run(['systemctl','status',str(os.getpid()),'--no-pager'],text=True,capture_output=True);r['systemd_status']={'rc':q.returncode,'stdout':q.stdout,'stderr':q.stderr}
s=json.dumps(r,sort_keys=True)
pathlib.Path('/var/lib/e2/probes',label+'.json').write_text(s+'\n')
print(s,flush=True)

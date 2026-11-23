#!/bin/sh
# All host state is relative to this script; no guest inventory is performed here.
exec 3<&0; exec python3 - "$0" "$@" <<'PY'
import os,sys,json,subprocess as sp,pathlib,fcntl,socket,time,signal,re,base64,uuid,shlex,shutil,io,tarfile,hashlib
R=pathlib.Path(sys.argv[1]).resolve().parent
A=sys.argv[2:]; B=R/'C1/base'; V=R/'C1/vms'; S=R/'slots'
for p in (B,V,S): p.mkdir(parents=True,exist_ok=True)
def metric(kind):
 path=os.environ.get('LAB_REHEARSAL_COUNTS');round_no=os.environ.get('LAB_REHEARSAL_ROUND')
 if path and round_no and round_no.isdigit():
  p=pathlib.Path(path);fresh=not p.exists()
  with p.open('a') as f:
   if fresh:f.write('round\tkind\trows\n')
   f.write(round_no+'\tlab:'+kind+'\t1\n')
def fail(s):
 labels={'Serial login timeout':'serial-login-timeout','Serial timeout; VM retained':'serial-frame-timeout','Serial disconnected':'serial-disconnected','Missing serial frame':'serial-missing-frame','Incomplete serial data frame; VM retained':'serial-incomplete-frame','Missing serial return status':'serial-missing-return'}
 if s in labels:metric(labels[s])
 raise RuntimeError(s)
def call(a,**kw): return sp.run([str(x) for x in a],check=True,**kw)
def valid(n):
 if not re.fullmatch('[a-z][a-z0-9-]{0,39}',n): fail('Invalid name')
 return n
def read(p): return json.loads(p.read_text())
def save(p,m):
 t=p.with_suffix('.tmp'); t.write_text(json.dumps(m,indent=2)+'\n'); t.replace(p)
def alive(d):
 try:
  pid=int((d/'qemu.pid').read_text()); cmd=pathlib.Path(f'/proc/{pid}/cmdline').read_bytes()
  return str(d/'disk.qcow2').encode() in cmd
 except (OSError,ValueError): return False
def qmp(d,command):
 s=socket.socket(socket.AF_UNIX);s.settimeout(5);s.connect(str(d/'qmp.sock'));f=s.makefile('rwb',buffering=0); f.readline()
 for cmd in ('qmp_capabilities',command):
  f.write((json.dumps({'execute':cmd})+'\n').encode())
  while True:
   obj=json.loads(f.readline())
   if 'return' in obj: break
   if 'error' in obj: fail(str(obj['error']))
 s.close()
def worker(n):
 d=V/n;m=read(d/'meta.json');locks=[];os.chdir(R)
 for i in range(1,13):
  f=open(S/f'slot-{i}.lock','a')
  try:
   if sp.run(['flock','-n',str(f.fileno())],pass_fds=(f.fileno(),)).returncode:raise BlockingIOError()
   locks.append(f)
  except BlockingIOError:f.close()
  if len(locks)==m.get('slots',1):break
 if len(locks)!=m.get('slots',1):fail('No free VM slot')
 # flock descriptors are inherited by QEMU; locks survive the wrapper.
 for f in locks:os.set_inheritable(f.fileno(),True)
 cmd=['qemu-system-x86_64','-enable-kvm','-m',str(4096*len(locks)),'-smp',str(2*len(locks)),'-cpu','host','-display','none','-no-reboot','-drive',f'file={d}/disk.qcow2,format=qcow2,if=virtio','-serial',f'unix:{d}/serial.sock,server=on,wait=off','-qmp',f'unix:{d}/qmp.sock,server=on,wait=off','-pidfile',str(d/'qemu.pid'),'-netdev',f'user,id=primary,hostfwd=tcp:127.0.0.1:{m["port"]}-:{50000 if m["transport"]=="talos" else 22}','-device','virtio-net-pci,netdev=primary,mac=52:54:00:ca:10:01','-netdev','user,id=secondary,net=10.0.3.0/24','-device','virtio-net-pci,netdev=secondary,mac=52:54:00:ca:10:02']
 if m.get('firmware_code'):
  cmd.extend(['-drive',f'if=pflash,format=raw,readonly=on,file={m["firmware_code"]}','-drive',f'if=pflash,format=raw,file={d}/firmware-vars.fd'])
 if m['system']=='mint':cmd.extend(['-audiodev','none,id=cal-audio','-device','intel-hda','-device','hda-duplex,audiodev=cal-audio'])
 for extra in m.get('qemu_args',[]):cmd.append(extra)
 os.execvp(cmd[0],cmd)
def interpreter(script):
 first=script.split(b'\n',1)[0]
 return shlex.split(first[2:].decode()) if first.startswith(b'#!') else ['sh']
def serial(d,m,script,root=False):
 if b'\0' in script:fail('Serial script must be text without NUL bytes')
 token='CAL'+uuid.uuid4().hex
 s=socket.socket(socket.AF_UNIX);s.settimeout(1);s.connect(str(d/'serial.sock'))
 def send(data):
  # Stay below serial line throughput and let the guest drain its UART FIFO.
  for i in range(len(data)):s.sendall(data[i:i+1]);time.sleep(.01)
 def receive_until(pattern,seconds,stage='frame'):
  data=b'';deadline=time.monotonic()+seconds
  while time.monotonic()<deadline:
   try:
    chunk=s.recv(65536)
    if not chunk:fail('Serial disconnected')
    data+=chunk
   except socket.timeout:continue
   if pattern(data):return data
  metric('serial-'+stage+'-timeout')
  fail('Serial '+stage+' timeout; VM retained')
 if os.getenv('LAB_PASSIVE_BOOT_LOGIN')!='1':send(b'\x03\r')
 data=b'';deadline=time.monotonic()+int(os.getenv('LAB_LOGIN_TIMEOUT','45'));last_receive=time.monotonic();nudged=False
 while time.monotonic()<deadline:
  if os.getenv('LAB_PASSIVE_BOOT_LOGIN')=='1' and not nudged and time.monotonic()-last_receive>10:
   send(b'\r');nudged=True
  try:
   chunk=s.recv(65536)
   if not chunk:fail('Serial disconnected')
   data+=chunk;last_receive=time.monotonic()
  except socket.timeout:continue
  clean=re.sub(rb'\x1b\].*?(?:\x07|\x1b\\)',b'',data,flags=re.S)
  clean=re.sub(rb'\x1b\[[0-9;?]*[a-zA-Z]',b'',clean)
  if re.search(rb'login:\s*$',clean):metric('serial-login-prompt');send((m.get('user','user')+'\n').encode());data=b'';continue
  if re.search(rb'[Pp]assword:\s*$',clean):metric('serial-password-prompt');send((m.get('password','cal-test')+'\n').encode());data=b'';continue
  if re.search(rb'(?:[#$]|CAL>)\s*$',clean):metric('serial-shell-prompt');break
 else:fail('Serial login timeout')
 # A prompt-shaped suffix is only a candidate; require an exact shell challenge.
 send(('printf \"\\n'+token+'SYNC\\n\"\n').encode())
 receive_until(lambda x:re.search(rb'(?:^|[\r\n])'+(token+'SYNC').encode()+rb'\r?\n',x) is not None,15,'shell-sync')
 runner=' '.join(shlex.quote(x) for x in interpreter(script))
 inner='printf %s "$cal_program" | '+runner
 if root and m.get('user','user')!='root':
  inner="printf '%s\\n' "+shlex.quote(m.get('password','cal-test'))+" | sudo -S -p '' sh -c "+shlex.quote('printf %s "$1" | '+runner)+' sh "$cal_program"'
 encoded=base64.b64encode(script)
 payload_digest=hashlib.sha256(encoded).hexdigest()
 checked_inner='cal_hash=$(printf %s "$payload" | sha256sum) && [ "${cal_hash%% *}" = "'+payload_digest+'" ] && cal_program=$(printf %s "$payload" | base64 -d; cal_decode=$?; printf X; exit "$cal_decode") && { cal_program=${cal_program%X}; '+inner+'; }'
 encoder='awk -v t='+shlex.quote(token)+' '+shlex.quote('{n+=length($0); printf "%sDATA%08d:%s:%s\\n",t,NR,$0,t} END {printf "%sCOUNT%d:%d\\n",t,NR,n}')
 receiver='printf "\\n'+token+'READY\\n"; payload=""; while IFS= read -r line; do [ "$line" = "'+token+'DATAEND" ] && break; payload="$payload$line"; done; printf "\\n'+token+'BEGIN\\n"; { '+checked_inner+'; cal_rc=$?; printf "\\n'+token+'RC=%s\\n" "$cal_rc"; } 2>&1 | base64 | '+encoder+'; printf "'+token+'END\\n"; IFS= read -r ack && [ "$ack" = "'+token+'ACK" ] && stty echo'
 # A noninteractive read loop consumes payload lines; interactive readline never
 # edits the base64 stream. Disable echo before sending the long wrapper,
 # preserve the login shell, and acknowledge its completed tty restoration.
 send(('stty -echo && cal_wrapper="" && printf "\\n'+token+'TTY\\n"\n').encode())
 receive_until(lambda x:re.search(rb'(?:^|[\r\n])'+(token+'TTY').encode()+rb'\r?\n',x) is not None,15,'tty')
 # Stage the wrapper through short acknowledged shell-variable assignments.
 # Coreutils sha256sum checks the complete staged bytes before decoding.
 wrapped=base64.b64encode(receiver.encode()).decode()
 for i in range(0,len(wrapped),128):
  ack=token+'PART'+str(i//128)
  send(('cal_wrapper="$cal_wrapper"'+shlex.quote(wrapped[i:i+128])+'; printf "\\n'+ack+'\\n"\n').encode())
  receive_until(lambda x:re.search(rb'(?:^|[\r\n])'+ack.encode()+rb'\r?\n',x) is not None,15,'wrapper-chunk')
 send(('cal_hash=$(printf %s "$cal_wrapper" | sha256sum) && [ "${cal_hash%% *}" = "'+hashlib.sha256(wrapped.encode()).hexdigest()+'" ] && printf "\\n'+token+'HASH\\n"\n').encode())
 receive_until(lambda x:re.search(rb'(?:^|[\r\n])'+(token+'HASH').encode()+rb'\r?\n',x) is not None,15,'wrapper-hash')
 send(('cal_code=$(printf %s "$cal_wrapper" | base64 -d) && printf "\\n'+token+'DECODE\\n"\n').encode())
 receive_until(lambda x:re.search(rb'(?:^|[\r\n])'+(token+'DECODE').encode()+rb'\r?\n',x) is not None,15,'wrapper-decode')
 setup='eval "$cal_code" && unset cal_wrapper cal_code && printf "\\n'+token+'CLOSED\\n"\n'
 send(setup.encode())
 receive_until(lambda x:re.search(rb'(?:^|[\r\n])'+(token+'READY').encode()+rb'\r?\n',x) is not None,15,'ready')
 for i in range(0,len(encoded),768):send(encoded[i:i+768]+b'\n')
 send((token+'DATAEND\n').encode())
 end=(token+'END').encode();start=(token+'BEGIN').encode()
 data=receive_until(lambda x:re.search(rb'(?:^|[\r\n])'+end+rb'\r?\n',x) is not None,int(os.getenv('LAB_RUN_TIMEOUT','300')))
 send((token+'ACK\n').encode())
 receive_until(lambda x:re.search(rb'(?:^|[\r\n])'+(token+'CLOSED').encode()+rb'\r?\n',x) is not None,15,'close')
 s.close()
 match=re.search(rb'(?:^|[\r\n])'+start+rb'\r?\n(.*?)'+end+rb'\r?\n',data,re.S)
 if not match:fail('Missing serial frame')
 frame=match.group(1)
 prefix=token.encode()
 chunks=re.findall(prefix+rb'DATA([0-9]{8}):([A-Za-z0-9+/=]*):'+prefix+rb'\r?\n',frame)
 count=re.search(prefix+rb'COUNT([0-9]+):([0-9]+)\r?\n',frame)
 if not count or [int(n) for n,b in chunks]!=list(range(1,int(count[1])+1)) or sum(len(b) for n,b in chunks)!=int(count[2]):
  fail('Incomplete serial data frame; VM retained')
 decoded=base64.b64decode(b''.join(b for n,b in chunks),validate=True)
 marker=('\n'+token+'RC=').encode()
 if marker not in decoded:
  fail('Missing serial return status')
 out,rc=decoded.rsplit(marker,1)
 metric('serial-frame-complete')
 return out,int(rc.strip())
def run(d,script,root=False,quiet=False,stream=False):
 m=read(d/'meta.json')
 if not alive(d):fail('VM is stopped')
 if m['transport']=='serial':return serial(d,m,script,root)
 if m['transport']=='talos':
  env=os.environ.copy();env['TALOSCONFIG']=str(R/m['talosconfig']);env['TALOS_ENDPOINTS']='127.0.0.1:'+str(m['port']);env['TALOS_NODES']=m.get('talos_node','10.0.2.15');env['PATH']=str(R/'C1/bin')+':'+env['PATH']
  env['TALOS_ENDPOINT']=env['TALOS_ENDPOINTS'];env['TALOS_NODE']=env['TALOS_NODES']
  bindir=d/'bin';bindir.mkdir(exist_ok=True)
  wrapper=bindir/'talosctl.tmp'
  wrapper.write_text('#!/bin/sh\nexec '+shlex.quote(str(R/'C1/bin/talosctl'))+' --talosconfig "$TALOSCONFIG" --endpoints "$TALOS_ENDPOINTS" --nodes "$TALOS_NODES" "$@"\n')
  wrapper.chmod(0o700);wrapper.replace(bindir/'talosctl')
  env['PATH']=str(bindir)+':'+env['PATH']
  p=sp.run(interpreter(script),input=script,stdout=sp.DEVNULL if quiet else (None if stream else sp.PIPE),stderr=sp.DEVNULL if quiet else (None if os.getenv("LAB_SEPARATE_STDERR")=="1" else sp.STDOUT),env=env,cwd=d,timeout=int(os.getenv('LAB_RUN_TIMEOUT','300')));return p.stdout or b'',p.returncode
 cmd=['ssh','-F','/dev/null','-o','BatchMode=yes','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','-o','ConnectTimeout=5','-i',str(R/m['key']),'-p',str(m['port']),m.get('ssh_user',m.get('user','user'))+'@127.0.0.1',('sudo -n ' if root else '')+' '.join(shlex.quote(x) for x in interpreter(script))]
 p=sp.run(cmd,input=script,stdout=sp.DEVNULL if quiet else (None if stream else sp.PIPE),stderr=sp.DEVNULL if quiet else (None if os.getenv("LAB_SEPARATE_STDERR")=="1" else sp.STDOUT),timeout=int(os.getenv('LAB_RUN_TIMEOUT','300')));return p.stdout or b'',p.returncode
def start(n):
 d=V/n;m=read(d/'meta.json')
 if alive(d):return
 for p in ('qemu.pid','serial.sock','qmp.sock'):(d/p).unlink(missing_ok=True)
 with socket.socket() as sock:sock.bind(('127.0.0.1',0));m['port']=sock.getsockname()[1]
 save(d/'meta.json',m)
 unit='cal-c1-'+n+'-'+uuid.uuid4().hex[:8];m['unit']=unit;save(d/'meta.json',m)
 call(['systemd-run','--user','--quiet','--collect','--unit',unit,'--property=MemoryMax='+str(4608*m.get('slots',1))+'M','--property=StandardOutput=null','--property=StandardError=null',str(R/'lab.sh'),'_worker',n])
 deadline=time.monotonic()+240
 while time.monotonic()<deadline:
  if alive(d):
   if m['transport']=='talos':
    try:
     old_timeout=os.environ.get('LAB_RUN_TIMEOUT');os.environ['LAB_RUN_TIMEOUT']='15'
     try:out,rc=run(d,b'talosctl version >/dev/null 2>&1\n',quiet=True)
     finally:
      if old_timeout is None:os.environ.pop('LAB_RUN_TIMEOUT',None)
      else:os.environ['LAB_RUN_TIMEOUT']=old_timeout
     if rc==0:return
    except (OSError,RuntimeError,sp.TimeoutExpired):pass
   else:
    try:
     probe_keys=('LAB_RUN_TIMEOUT','LAB_LOGIN_TIMEOUT','LAB_PASSIVE_BOOT_LOGIN')
     old_probe={key:os.environ.get(key) for key in probe_keys}
     os.environ['LAB_RUN_TIMEOUT']='15'
     if m['transport']=='serial' and m.get('passive_boot_login'):
      os.environ.update(LAB_LOGIN_TIMEOUT=str(max(1,int(deadline-time.monotonic()))),LAB_PASSIVE_BOOT_LOGIN='1')
     try:out,rc=run(d,b'exit 0\n',quiet=True)
     finally:
      for key,value in old_probe.items():
       if value is None:os.environ.pop(key,None)
       else:os.environ[key]=value
     if rc==0:return
    except (OSError,RuntimeError,sp.TimeoutExpired):pass
  p=sp.run(['systemctl','--user','is-active',unit],stdout=sp.PIPE)
  if p.returncode and p.stdout.strip() not in (b'activating',):fail('VM failed to start')
  time.sleep(2)
 fail('Boot/login timed out; VM retained')
def stop(n,cut=False):
 d=V/n
 if not alive(d):return
 if cut:
  os.kill(int((d/'qemu.pid').read_text()),signal.SIGKILL)
 else:
  if read(d/'meta.json')['transport']=='talos':
   out,rc=run(d,b'talosctl shutdown --wait=false >/dev/null 2>&1\n',quiet=True)
   if rc:fail('Talos shutdown failed')
  elif read(d/'meta.json')['system'] in ('guix','gentoo'):
   old_timeout=os.environ.get('LAB_RUN_TIMEOUT');os.environ['LAB_RUN_TIMEOUT']='15'
   shutdown=b'herd power-off shepherd >/dev/null 2>&1\n' if read(d/'meta.json')['system']=='guix' else b'poweroff >/dev/null 2>&1\n'
   try:
    try:out,rc=run(d,shutdown,True,quiet=True)
    except (RuntimeError,OSError,sp.TimeoutExpired):pass # Shutdown may close its transport before a return marker.
   finally:
    if old_timeout is None:os.environ.pop('LAB_RUN_TIMEOUT',None)
    else:os.environ['LAB_RUN_TIMEOUT']=old_timeout
  else:qmp(d,'system_powerdown')
 deadline=time.monotonic()+(20 if cut else 120)
 while alive(d) and time.monotonic()<deadline:time.sleep(.3)
 if alive(d):fail('Shutdown timeout; use kill for immediate power cut')
def main():
 if not A:fail('Usage: lab.sh new NAME SYSTEM | run NAME [--root] [--timeout N] | copy-out NAME PATH DIR | start/stop/kill/destroy NAME | list')
 op=A[0]
 if op=='_worker':worker(valid(A[1]));return
 if op=='list':
  print('name\tsystem\tstate')
  for d in sorted(V.iterdir()):
   if (d/'meta.json').exists():print(d.name,read(d/'meta.json')['system'],'running' if alive(d) else 'stopped',sep='\t')
  return
 n=valid(A[1]);d=V/n
 if op=='new':
  system=valid(A[2])
  if system not in ('alma','void','gentoo','microos','talos','nixos','guix','debian','fedora','mint','debian-server'):fail('Unsupported system')
  base=B/(system+'.qcow2');m=read(B/(system+'.json'))
  if base.stat().st_mode&0o222:fail('Backing image must be read-only')
  d.mkdir()
  if m.get('firmware_vars'):shutil.copyfile(R/m['firmware_vars'],d/'firmware-vars.fd')
  call(['qemu-img','create','-q','-f','qcow2','-F','qcow2','-b',base,d/'disk.qcow2']);m['system']=system;save(d/'meta.json',m);start(n)
 elif op=='start':start(n)
 elif op in ('stop','kill'):stop(n,op=='kill')
 elif op=='destroy':
  stop(n);shutil.rmtree(d)
 elif op=='run':
  # stdin was preserved by the shell wrapper on fd 3.
  seconds=int(A[A.index('--timeout')+1]) if '--timeout' in A else int(os.getenv('LAB_RUN_TIMEOUT','300'))
  if seconds<1:fail('Timeout must be positive')
  os.environ['LAB_RUN_TIMEOUT']=str(seconds)
  def expired(signum,frame):raise TimeoutError('Run time limit exceeded')
  signal.signal(signal.SIGALRM,expired);signal.alarm(seconds)
  script=os.fdopen(3,'rb').read()
  with open(d/'run.lock','a') as lock:
   fcntl.flock(lock,fcntl.LOCK_EX);out,rc=run(d,script,'--root' in A[2:],stream=True)
  signal.alarm(0)
  sys.stdout.buffer.write(out);sys.exit(rc if rc>=0 else 128-rc)
 elif op=='copy-out':
  path=A[2];dest=pathlib.Path(A[3]);dest.mkdir(parents=True,exist_ok=True)
  m=read(d/'meta.json')
  if m['transport']=='talos':
   command='talosctl read '+shlex.quote(path)+'\n'
   out,rc=run(d,command.encode(),True)
   if rc:fail('talosctl read failed')
   (dest/pathlib.PurePosixPath(path).name).write_bytes(out);return
  parent=str(pathlib.PurePosixPath(path).parent);leaf=pathlib.PurePosixPath(path).name
  command='set -e; test -e '+shlex.quote(path)+'; tar -C '+shlex.quote(parent)+' -cf - -- '+shlex.quote(leaf)+' | base64\n'
  out,rc=run(d,command.encode(),True)
  if rc:fail('Guest copy failed')
  with tarfile.open(fileobj=io.BytesIO(base64.b64decode(out))) as tf:tf.extractall(dest,filter='data')
 else:fail('Unknown operation')
try:
 if A and A[0] in ('new','start','stop','kill','destroy'):
  with open(R/('C1/'+valid(A[1])+'.lifecycle.lock'),'a') as lock:fcntl.flock(lock,fcntl.LOCK_EX);main()
 else:main()
except (TimeoutError,sp.TimeoutExpired):
 print('lab: time limit exceeded',file=sys.stderr);sys.exit(124)
except (RuntimeError,OSError,ValueError,sp.CalledProcessError,sp.TimeoutExpired,KeyError,IndexError) as e:
 print('lab: '+str(e),file=sys.stderr);sys.exit(1)
PY

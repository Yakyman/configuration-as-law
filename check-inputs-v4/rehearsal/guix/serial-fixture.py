#!/usr/bin/env python3
"""Synthetic PTY protocol test; no inventory or retained shell transcript."""
import ast,base64,hashlib,json,os,pathlib,pty,re,select,shlex,signal,socket,time,uuid
root=pathlib.Path(__file__).resolve().parents[2]
source=(root/'lab.sh').read_text().split("<<'PY'\n",1)[1].rsplit('\nPY',1)[0]
tree=ast.parse(source)
parts=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'interpreter','serial'}],type_ignores=[])
def fail(msg):raise RuntimeError(msg)
def scenario(kind):
 child,master=pty.fork()
 if child==0:os.execv('/bin/bash',['bash','--noprofile','--norc','-i'])
 altered=False;line=b'';wire_bytes=0
 class Connection:
  def settimeout(self,n):self.timeout=n
  def connect(self,path):pass
  def sendall(self,data):
   nonlocal altered,line,wire_bytes
   wire_bytes+=len(data)
   # Buffer only one outgoing line to allow deterministic fault injection.
   line+=data
   if b'\n' not in line and b'\r' not in line:return
   data=line;line=b''
   if not altered:
    if kind=='bad-sync' and data.startswith(b'printf ') and b'SYNC' in data:
     data=b'false\n';altered=True
    elif kind=='bad-wrapper' and data.startswith(b'cal_wrapper="$cal_wrapper"'):
     offset=len(b'cal_wrapper="$cal_wrapper"');data=data[:offset]+(b'A' if data[offset:offset+1]!=b'A' else b'B')+data[offset+1:];altered=True
    elif kind=='bad-payload' and data.startswith(b'ZXhpdCA'):
     data=b'A'+data[1:];altered=True
    elif kind=='bad-ack' and re.fullmatch(rb'CAL[0-9a-f]+ACK\n',data):data=data.replace(b'ACK\n',b'BAD\n');altered=True
    elif kind=='bad-stty' and data.startswith(b'stty -echo &&'):data=data.replace(b'stty -echo',b'false',1);altered=True
   while data:
    n=os.write(master,data);data=data[n:]
  def recv(self,n):
   if not select.select([master],[],[],self.timeout)[0]:raise socket.timeout()
   return os.read(master,n)
  def close(self):pass
 class Socket:
  AF_UNIX=socket.AF_UNIX;SOCK_STREAM=socket.SOCK_STREAM;timeout=socket.timeout
  def socket(self,*a):return Connection()
 namespace={**globals(),'socket':Socket(),'fail':fail,'metric':lambda *a:None}
 exec(compile(parts,'serial-under-test','exec'),namespace)
 os.environ['LAB_PASSIVE_BOOT_LOGIN']='1'
 results=[]
 try:
  for i in range(4 if kind=='normal' else 1):
   expected=0 if i%2==0 else 37
   wire_bytes=0
   out,rc=namespace['serial'](pathlib.Path('.'),{'user':'fixture'},f'exit {expected}\n\n'.encode())
   os.environ.pop('LAB_PASSIVE_BOOT_LOGIN',None)
   results.append({'call':i+1,'status':rc,'empty_output':out==b'','wire_bytes':wire_bytes})
   if kind=='normal':assert rc==expected and out==b''
   elif kind=='bad-payload':assert altered and rc!=0
   else:raise AssertionError('corrupt handshake was accepted')
  return {'scenario':kind,'passed':True,'results':results}
 except RuntimeError as exc:
  expected={'bad-sync':'shell-sync timeout','bad-wrapper':'wrapper-hash timeout','bad-ack':'close timeout','bad-stty':'tty timeout'}.get(kind)
  if expected and altered and expected in str(exc):return {'scenario':kind,'passed':True,'rejected':str(exc)}
  raise
 finally:
  os.environ.pop('LAB_PASSIVE_BOOT_LOGIN',None);os.close(master)
  try:os.kill(child,signal.SIGKILL)
  except ProcessLookupError:pass
  os.waitpid(child,0)
results=[]
for kind in ('normal','bad-wrapper','bad-payload','bad-ack','bad-stty'):
 results.append(scenario(kind))
 print(json.dumps(results[-1],sort_keys=True),flush=True)
print(json.dumps({'passed':True,'fixture':'synthetic PTY fixed commands and deterministic faults','scenarios':len(results)},sort_keys=True))

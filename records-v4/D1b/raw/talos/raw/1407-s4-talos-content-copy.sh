python3 -c '
import subprocess,json,sys,hashlib,selectors,time,os,concurrent.futures,tarfile,posixpath,re
paths=json.loads(sys.argv[1])
def sanitized(err,path):
 text=err.decode('"'"'utf-8'"'"','"'"'replace'"'"').replace(path,'"'"'<target>'"'"')
 text=re.sub(r'"'"'/home/[^/\s]+'"'"','"'"'<home>'"'"',text)
 return re.sub(r'"'"'\b(?:\d{1,3}\.){3}\d{1,3}\b'"'"','"'"'<node>'"'"',text)[:4096]
def category(status,detail):
 low=detail.lower()
 if '"'"'permission denied'"'"' in low:return '"'"'permission-denied'"'"'
 if '"'"'no such file'"'"' in low or '"'"'notfound'"'"' in low:return '"'"'not-found'"'"'
 if '"'"'regular file'"'"' in low:return '"'"'not-regular'"'"'
 return status
class BoundedPipe:
 def __init__(self,p):
  self.p=p;self.sel=selectors.DefaultSelector();self.sel.register(p.stdout,selectors.EVENT_READ,'"'"'out'"'"');self.sel.register(p.stderr,selectors.EVENT_READ,'"'"'err'"'"');self.err=b'"'"''"'"';self.total=0;self.stop=time.monotonic()+30;self.eof=False
 def read(self,size):
  if size<0:raise ValueError('"'"'unbounded archive read refused'"'"')
  if not size:return b'"'"''"'"'
  while not self.eof:
   if time.monotonic()>self.stop:raise TimeoutError('"'"'copy time bound'"'"')
   for key,_ in self.sel.select(.2):
    b=os.read(key.fileobj.fileno(),min(size,65536) if key.data=='"'"'out'"'"' else 4096)
    if not b:
     self.sel.unregister(key.fileobj)
     if key.data=='"'"'out'"'"':self.eof=True
     continue
    if key.data=='"'"'err'"'"':self.err=(self.err+b)[:4096];continue
    self.total+=len(b)
    if self.total>1074790400:raise OverflowError('"'"'compressed copy bound'"'"')
    return b
  return b'"'"''"'"'
def copy_one(request):
 path,size=request;p=subprocess.Popen(['"'"'talosctl'"'"','"'"'copy'"'"',path,'"'"'-'"'"'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);reader=BoundedPipe(p)
 status='"'"'ok'"'"';n=0;prefix=b'"'"''"'"';digest=hashlib.sha256();members=0;detail='"'"''"'"'
 try:
  with tarfile.open(fileobj=reader,mode='"'"'r|gz'"'"') as archive:
   for item in archive:
    members+=1
    if members!=1 or not item.isfile() or item.name!=posixpath.basename(path):raise ValueError('"'"'archive-member-mismatch'"'"')
    if item.size!=size:raise ValueError('"'"'archive-size-changed'"'"')
    if item.size>1073741824:raise OverflowError('"'"'copy payload bound'"'"')
    with archive.extractfile(item) as stream:
     while True:
      b=stream.read(65536)
      if not b:break
      n+=len(b)
      if n>1073741824:raise OverflowError('"'"'copy payload bound'"'"')
      digest.update(b);prefix=(prefix+b)[:16]
  while reader.read(65536):pass
  if members!=1 or n!=size:status='"'"'archive-incomplete'"'"'
 except TimeoutError:status='"'"'timeout'"'"'
 except OverflowError:status='"'"'size-cap'"'"'
 except (tarfile.TarError,ValueError,EOFError,OSError) as exc:status='"'"'archive-error'"'"';detail=str(exc)
 if status!='"'"'ok'"'"':p.kill()
 try:rc=p.wait(timeout=3)
 except subprocess.TimeoutExpired:p.kill();rc=p.wait(timeout=3);status='"'"'timeout'"'"'
 reader.err=(reader.err+p.stderr.read(4096))[:4096]
 reader.sel.close();p.stdout.close();p.stderr.close()
 if rc and status=='"'"'ok'"'"':status='"'"'copy-error'"'"'
 diagnostic=sanitized(reader.err,path)
 if detail:diagnostic=(diagnostic+'"'"'; '"'"'+detail).strip('"'"'; '"'"')
 return {'"'"'path'"'"':path,'"'"'status'"'"':status,'"'"'bytes'"'"':n,'"'"'sha256'"'"':digest.hexdigest() if status=='"'"'ok'"'"' else '"'"''"'"', '"'"'prefix_hex'"'"':prefix.hex() if status=='"'"'ok'"'"' else '"'"''"'"', '"'"'signature'"'"':('"'"'ELF'"'"' if prefix.startswith(b'"'"'\x7fELF'"'"') else '"'"'shebang'"'"' if prefix.startswith(b'"'"'#!'"'"') else '"'"'other'"'"') if status=='"'"'ok'"'"' else '"'"'unknown'"'"','"'"'query_exit'"'"':rc,'"'"'error_category'"'"':category(status,diagnostic) if status!='"'"'ok'"'"' else '"'"''"'"', '"'"'diagnostic'"'"':diagnostic}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for result in pool.map(copy_one,paths):
  print(json.dumps(result),flush=True)
  if result['"'"'status'"'"']!='"'"'ok'"'"':print('"'"'bounded copy query: '"'"'+result['"'"'error_category'"'"']+'"'"'; '"'"'+result['"'"'diagnostic'"'"'],file=sys.stderr,flush=True)
' '[["/var/lib/kubelet/pods/cc24b352660e443224e0f13dc185c8ac/containers/kube-scheduler/518e4e6c", 0], ["/var/lib/kubelet/pods/cc24b352660e443224e0f13dc185c8ac/containers/kube-scheduler/ecf92eb4", 0], ["/var/lib/kubelet/pods/cc24b352660e443224e0f13dc185c8ac/etc-hosts", 187], ["/var/lib/kubelet/pods/cc24b352660e443224e0f13dc185c8ac/plugins/kubernetes.io~empty-dir/run/ready", 0]]'

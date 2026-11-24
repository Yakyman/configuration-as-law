python3 -c '
import subprocess,json,sys,hashlib,selectors,time,os,concurrent.futures,re
paths=json.loads(sys.argv[1])
def read_one(request):
 path,size=request
 p=subprocess.Popen(['"'"'talosctl'"'"','"'"'read'"'"',path],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ,'"'"'out'"'"');sel.register(p.stderr,selectors.EVENT_READ,'"'"'err'"'"')
 digest=hashlib.sha256();prefix=b'"'"''"'"';n=0;err=b'"'"''"'"';stop=time.monotonic()+30;status='"'"'ok'"'"'
 try:
  while sel.get_map():
   if time.monotonic()>stop:status='"'"'timeout'"'"';break
   for key,_ in sel.select(.2):
    b=os.read(key.fileobj.fileno(),65536)
    if not b:sel.unregister(key.fileobj);continue
    if key.data=='"'"'err'"'"':err=(err+b)[:4096];continue
    n+=len(b)
    if n>1073741824:status='"'"'size-cap'"'"';break
    digest.update(b);prefix=(prefix+b)[:16]
   if status!='"'"'ok'"'"':break
  if status!='"'"'ok'"'"':p.kill()
  try:rc=p.wait(timeout=3)
  except subprocess.TimeoutExpired:
   p.kill();rc=p.wait(timeout=3);status='"'"'timeout'"'"'
 finally:
  sel.close();p.stdout.close();p.stderr.close()
 if rc and status=='"'"'ok'"'"':status='"'"'read-error'"'"'
 if status=='"'"'ok'"'"' and n!=size:status='"'"'size-changed'"'"'
 diagnostic=err.decode('"'"'utf-8'"'"','"'"'replace'"'"').replace(path,'"'"'<target>'"'"')
 diagnostic=re.sub(r'"'"'/home/[^/\s]+'"'"','"'"'<home>'"'"',diagnostic)
 diagnostic=re.sub(r'"'"'\b(?:\d{1,3}\.){3}\d{1,3}\b'"'"','"'"'<node>'"'"',diagnostic)
 low=diagnostic.lower();error_category='"'"'permission-denied'"'"' if '"'"'permission denied'"'"' in low else '"'"'not-found'"'"' if '"'"'no such file'"'"' in low or '"'"'notfound'"'"' in low else '"'"'not-regular'"'"' if '"'"'regular file'"'"' in low else status
 return {'"'"'path'"'"':path,'"'"'status'"'"':status,'"'"'bytes'"'"':n,'"'"'sha256'"'"':digest.hexdigest() if status=='"'"'ok'"'"' else '"'"''"'"', '"'"'prefix_hex'"'"':prefix.hex() if status=='"'"'ok'"'"' else '"'"''"'"', '"'"'signature'"'"':('"'"'ELF'"'"' if prefix.startswith(b'"'"'\x7fELF'"'"') else '"'"'shebang'"'"' if prefix.startswith(b'"'"'#!'"'"') else '"'"'other'"'"') if status=='"'"'ok'"'"' else '"'"'unknown'"'"', '"'"'query_exit'"'"':rc,'"'"'error_category'"'"':error_category if status!='"'"'ok'"'"' else '"'"''"'"', '"'"'diagnostic'"'"':diagnostic}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for result in pool.map(read_one,paths):
  print(json.dumps(result),flush=True)
  if result['"'"'status'"'"']!='"'"'ok'"'"':print('"'"'bounded content query: '"'"'+result['"'"'error_category'"'"']+'"'"'; '"'"'+result['"'"'diagnostic'"'"'],file=sys.stderr,flush=True)
' '[["/var/lib/kubelet/pods/440f86577bf52bc37b7de38238305fae/plugins/kubernetes.io~empty-dir/tmp/ready", 0], ["/var/lib/kubelet/pods/cc24b352660e443224e0f13dc185c8ac/containers/kube-scheduler/518e4e6c", 0], ["/var/lib/kubelet/pods/cc24b352660e443224e0f13dc185c8ac/containers/kube-scheduler/ecf92eb4", 0], ["/var/lib/kubelet/pods/cc24b352660e443224e0f13dc185c8ac/etc-hosts", 187], ["/var/lib/kubelet/pods/cc24b352660e443224e0f13dc185c8ac/plugins/kubernetes.io~empty-dir/run/ready", 0], ["/var/lib/kubelet/pods/cc24b352660e443224e0f13dc185c8ac/plugins/kubernetes.io~empty-dir/tmp/ready", 0], ["/var/lib/kubelet/pods/d42127b93b44dfb0a28ad83f726f3610/containers/kube-controller-manager/47f8eea9", 0], ["/var/lib/kubelet/pods/d42127b93b44dfb0a28ad83f726f3610/containers/kube-controller-manager/9bacce6a", 0], ["/var/lib/kubelet/pods/d42127b93b44dfb0a28ad83f726f3610/etc-hosts", 187], ["/var/lib/kubelet/pods/d42127b93b44dfb0a28ad83f726f3610/plugins/kubernetes.io~empty-dir/run/ready", 0], ["/var/lib/kubelet/pods/d42127b93b44dfb0a28ad83f726f3610/plugins/kubernetes.io~empty-dir/tmp/ready", 0]]'

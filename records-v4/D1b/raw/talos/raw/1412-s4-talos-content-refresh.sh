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

import posixpath

def safe_error(data,path):
 text=data.decode('"'"'utf-8'"'"','"'"'replace'"'"').replace(path,'"'"'<target>'"'"').replace(posixpath.dirname(path),'"'"'<parent>'"'"')
 text=re.sub(r'"'"'/home/[^/\s]+'"'"','"'"'<home>'"'"',text)
 return re.sub(r'"'"'\b(?:\d{1,3}\.){3}\d{1,3}\b'"'"','"'"'<node>'"'"',text)[:4096]

def metadata(path):
 parent=posixpath.dirname(path)
 p=subprocess.Popen(['"'"'talosctl'"'"','"'"'list'"'"','"'"'--depth'"'"','"'"'1'"'"','"'"'--long'"'"',parent],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ,'"'"'out'"'"');sel.register(p.stderr,selectors.EVENT_READ,'"'"'err'"'"')
 output=[];n=0;err=b'"'"''"'"';stop=time.monotonic()+15;status='"'"'ok'"'"'
 while sel.get_map():
  if time.monotonic()>stop:status='"'"'metadata-timeout'"'"';break
  for key,_ in sel.select(.2):
   b=os.read(key.fileobj.fileno(),65536)
   if not b:sel.unregister(key.fileobj);continue
   if key.data=='"'"'err'"'"':err=(err+b)[:4096];continue
   n+=len(b)
   if n>1048576:status='"'"'metadata-output-cap'"'"';break
   output.append(b)
  if status!='"'"'ok'"'"':break
 if status!='"'"'ok'"'"':p.kill()
 try:rc=p.wait(timeout=3)
 except subprocess.TimeoutExpired:p.kill();rc=p.wait(timeout=3);status='"'"'metadata-timeout'"'"'
 sel.close();p.stdout.close();p.stderr.close();diagnostic=safe_error(err,path)
 if rc or status!='"'"'ok'"'"':return {'"'"'status'"'"':'"'"'not-found'"'"' if '"'"'no such file'"'"' in diagnostic.lower() or '"'"'notfound'"'"' in diagnostic.lower() else status if status!='"'"'ok'"'"' else '"'"'metadata-query-failed'"'"','"'"'query_exit'"'"':rc,'"'"'diagnostic'"'"':diagnostic}
 try:
  lines=b'"'"''"'"'.join(output).decode('"'"'utf-8'"'"','"'"'strict'"'"').splitlines()
  headers=re.split(r'"'"'\s{2,}|\t+'"'"',lines[0].strip())
  if not {'"'"'NODE'"'"','"'"'MODE'"'"','"'"'UID'"'"','"'"'GID'"'"','"'"'SIZE(B)'"'"','"'"'LASTMOD'"'"','"'"'NAME'"'"'}<=set(headers):raise ValueError('"'"'metadata headers'"'"')
  starts=[];cursor=0
  for header in headers:
   start=lines[0].index(header,cursor);starts.append(start);cursor=start+len(header)
  matched=[]
  for line in lines[1:]:
   if not line.strip():continue
   if len(line)<starts[-1]:raise ValueError('"'"'metadata short row'"'"')
   row={key:line[start:starts[i+1] if i+1<len(starts) else None].strip() for i,(key,start) in enumerate(zip(headers,starts))}
   name=row['"'"'NAME'"'"'].split('"'"' -> '"'"',1)[0] if row['"'"'MODE'"'"'].startswith('"'"'L'"'"') else row['"'"'NAME'"'"']
   if posixpath.normpath(posixpath.join(parent,name))==path:matched.append(row)
  if not matched:return {'"'"'status'"'"':'"'"'not-found'"'"','"'"'query_exit'"'"':0,'"'"'diagnostic'"'"':'"'"'target absent from fresh immediate-parent listing'"'"'}
  if len(matched)!=1:raise ValueError('"'"'ambiguous metadata identity'"'"')
  row=matched[0]
  return {'"'"'status'"'"':'"'"'ok'"'"' if row['"'"'MODE'"'"'].startswith('"'"'-'"'"') else '"'"'nonregular-type'"'"','"'"'query_exit'"'"':0,'"'"'path'"'"':path,'"'"'mode'"'"':row['"'"'MODE'"'"'],'"'"'owner'"'"':row['"'"'UID'"'"']+'"'"':'"'"'+row['"'"'GID'"'"'],'"'"'size'"'"':int(row['"'"'SIZE(B)'"'"']),'"'"'mtime_display'"'"':row['"'"'LASTMOD'"'"'],'"'"'diagnostic'"'"':'"'"''"'"'}
 except (ValueError,KeyError,IndexError,UnicodeError) as exc:return {'"'"'status'"'"':'"'"'metadata-parser-failed'"'"','"'"'query_exit'"'"':0,'"'"'diagnostic'"'"':str(exc)}

def refresh_one(request):
 path,old_size=request;before=metadata(path)
 result={'"'"'path'"'"':path,'"'"'status'"'"':before['"'"'status'"'"'],'"'"'bytes'"'"':0,'"'"'sha256'"'"':'"'"''"'"','"'"'prefix_hex'"'"':'"'"''"'"','"'"'signature'"'"':'"'"'unknown'"'"','"'"'query_exit'"'"':before['"'"'query_exit'"'"'],'"'"'diagnostic'"'"':before.get('"'"'diagnostic'"'"','"'"''"'"'),'"'"'before'"'"':before,'"'"'after'"'"':None,'"'"'original_listing_size'"'"':old_size}
 if before['"'"'status'"'"']=='"'"'ok'"'"':
  if before['"'"'size'"'"']>1073741824:result['"'"'status'"'"']='"'"'size-cap'"'"'
  else:
   result.update(read_one([path,before['"'"'size'"'"']]))
   after=metadata(path);result['"'"'after'"'"']=after
   if result['"'"'status'"'"']=='"'"'ok'"'"':
    if after['"'"'status'"'"']!='"'"'ok'"'"':result['"'"'status'"'"']=after['"'"'status'"'"'];result['"'"'diagnostic'"'"']=after.get('"'"'diagnostic'"'"','"'"''"'"')
    elif any(before.get(k)!=after.get(k) for k in ('"'"'mode'"'"','"'"'owner'"'"','"'"'size'"'"','"'"'mtime_display'"'"')):result['"'"'status'"'"']='"'"'metadata-changed'"'"';result['"'"'diagnostic'"'"']='"'"'fresh pre/post metadata differ'"'"'
 if result['"'"'status'"'"']!='"'"'ok'"'"':result.update(sha256='"'"''"'"',prefix_hex='"'"''"'"',signature='"'"'unknown'"'"')
 result['"'"'error_category'"'"']=result['"'"'status'"'"'] if result['"'"'status'"'"']!='"'"'ok'"'"' else '"'"''"'"'
 return result

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for result in pool.map(refresh_one,paths):
  print(json.dumps(result),flush=True)
  if result['"'"'status'"'"']!='"'"'ok'"'"':print('"'"'bounded refresh query: '"'"'+result['"'"'error_category'"'"']+'"'"'; '"'"'+result['"'"'diagnostic'"'"'],file=sys.stderr,flush=True)
' '[["/var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/27/fs/etc/resolv.conf", 0], ["/var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/48/fs/etc/hostname", 0], ["/var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/48/fs/etc/hosts", 0], ["/var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/48/fs/etc/resolv.conf", 0]]'

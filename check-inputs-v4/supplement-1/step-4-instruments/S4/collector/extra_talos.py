"""Supplemental Talos evidence; no object decisions or ownership inference."""
import collections
import json
import posixpath
from main import write_tsv
import talos

ROOTS = ('/etc', '/opt', '/var/system', '/var/lib/containerd', '/var/lib/kubelet', '/var/log/containers')
MAX_DIRS = 8192
MAX_MEMBERS = 250000
MAX_DEPTH = 48
# Pseudo aliases remain explicit boundaries; workload metadata may be listed.
BOUNDARIES = {'proc', 'sys', 'dev'}
CONTENT_LIMIT = 1073741824
READ_SCRIPT = r'''
import subprocess,json,sys,hashlib,selectors,time,os,concurrent.futures,re
paths=json.loads(sys.argv[1])
def read_one(request):
 path,size=request
 p=subprocess.Popen(['talosctl','read',path],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ,'out');sel.register(p.stderr,selectors.EVENT_READ,'err')
 digest=hashlib.sha256();prefix=b'';n=0;err=b'';stop=time.monotonic()+30;status='ok'
 try:
  while sel.get_map():
   if time.monotonic()>stop:status='timeout';break
   for key,_ in sel.select(.2):
    b=os.read(key.fileobj.fileno(),65536)
    if not b:sel.unregister(key.fileobj);continue
    if key.data=='err':err=(err+b)[:4096];continue
    n+=len(b)
    if n>1073741824:status='size-cap';break
    digest.update(b);prefix=(prefix+b)[:16]
   if status!='ok':break
  if status!='ok':p.kill()
  try:rc=p.wait(timeout=3)
  except subprocess.TimeoutExpired:
   p.kill();rc=p.wait(timeout=3);status='timeout'
 finally:
  sel.close();p.stdout.close();p.stderr.close()
 if rc and status=='ok':status='read-error'
 if status=='ok' and n!=size:status='size-changed'
 diagnostic=err.decode('utf-8','replace').replace(path,'<target>')
 diagnostic=re.sub(r'/home/[^/\s]+','<home>',diagnostic)
 diagnostic=re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b','<node>',diagnostic)
 low=diagnostic.lower();error_category='permission-denied' if 'permission denied' in low else 'not-found' if 'no such file' in low or 'notfound' in low else 'not-regular' if 'regular file' in low else status
 return {'path':path,'status':status,'bytes':n,'sha256':digest.hexdigest() if status=='ok' else '', 'prefix_hex':prefix.hex() if status=='ok' else '', 'signature':('ELF' if prefix.startswith(b'\x7fELF') else 'shebang' if prefix.startswith(b'#!') else 'other') if status=='ok' else 'unknown', 'query_exit':rc,'error_category':error_category if status!='ok' else '', 'diagnostic':diagnostic}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for result in pool.map(read_one,paths):
  print(json.dumps(result),flush=True)
  if result['status']!='ok':print('bounded content query: '+result['error_category']+'; '+result['diagnostic'],file=sys.stderr,flush=True)
'''


COPY_SCRIPT = r'''
import subprocess,json,sys,hashlib,selectors,time,os,concurrent.futures,tarfile,posixpath,re
paths=json.loads(sys.argv[1])
def sanitized(err,path):
 text=err.decode('utf-8','replace').replace(path,'<target>')
 text=re.sub(r'/home/[^/\s]+','<home>',text)
 return re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b','<node>',text)[:4096]
def category(status,detail):
 low=detail.lower()
 if 'permission denied' in low:return 'permission-denied'
 if 'no such file' in low or 'notfound' in low:return 'not-found'
 if 'regular file' in low:return 'not-regular'
 return status
class BoundedPipe:
 def __init__(self,p):
  self.p=p;self.sel=selectors.DefaultSelector();self.sel.register(p.stdout,selectors.EVENT_READ,'out');self.sel.register(p.stderr,selectors.EVENT_READ,'err');self.err=b'';self.total=0;self.stop=time.monotonic()+30;self.eof=False
 def read(self,size):
  if size<0:raise ValueError('unbounded archive read refused')
  if not size:return b''
  while not self.eof:
   if time.monotonic()>self.stop:raise TimeoutError('copy time bound')
   for key,_ in self.sel.select(.2):
    b=os.read(key.fileobj.fileno(),min(size,65536) if key.data=='out' else 4096)
    if not b:
     self.sel.unregister(key.fileobj)
     if key.data=='out':self.eof=True
     continue
    if key.data=='err':self.err=(self.err+b)[:4096];continue
    self.total+=len(b)
    if self.total>1074790400:raise OverflowError('compressed copy bound')
    return b
  return b''
def copy_one(request):
 path,size=request;p=subprocess.Popen(['talosctl','copy',path,'-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);reader=BoundedPipe(p)
 status='ok';n=0;prefix=b'';digest=hashlib.sha256();members=0;detail=''
 try:
  with tarfile.open(fileobj=reader,mode='r|gz') as archive:
   for item in archive:
    members+=1
    if members!=1 or not item.isfile() or item.name!=posixpath.basename(path):raise ValueError('archive-member-mismatch')
    if item.size!=size:raise ValueError('archive-size-changed')
    if item.size>1073741824:raise OverflowError('copy payload bound')
    with archive.extractfile(item) as stream:
     while True:
      b=stream.read(65536)
      if not b:break
      n+=len(b)
      if n>1073741824:raise OverflowError('copy payload bound')
      digest.update(b);prefix=(prefix+b)[:16]
  while reader.read(65536):pass
  if members!=1 or n!=size:status='archive-incomplete'
 except TimeoutError:status='timeout'
 except OverflowError:status='size-cap'
 except (tarfile.TarError,ValueError,EOFError,OSError) as exc:status='archive-error';detail=str(exc)
 if status!='ok':p.kill()
 try:rc=p.wait(timeout=3)
 except subprocess.TimeoutExpired:p.kill();rc=p.wait(timeout=3);status='timeout'
 reader.err=(reader.err+p.stderr.read(4096))[:4096]
 reader.sel.close();p.stdout.close();p.stderr.close()
 if rc and status=='ok':status='copy-error'
 diagnostic=sanitized(reader.err,path)
 if detail:diagnostic=(diagnostic+'; '+detail).strip('; ')
 return {'path':path,'status':status,'bytes':n,'sha256':digest.hexdigest() if status=='ok' else '', 'prefix_hex':prefix.hex() if status=='ok' else '', 'signature':('ELF' if prefix.startswith(b'\x7fELF') else 'shebang' if prefix.startswith(b'#!') else 'other') if status=='ok' else 'unknown','query_exit':rc,'error_category':category(status,diagnostic) if status!='ok' else '', 'diagnostic':diagnostic}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for result in pool.map(copy_one,paths):
  print(json.dumps(result),flush=True)
  if result['status']!='ok':print('bounded copy query: '+result['error_category']+'; '+result['diagnostic'],file=sys.stderr,flush=True)
'''


REFRESH_SCRIPT = READ_SCRIPT.split('with concurrent.futures.ThreadPoolExecutor')[0] + r'''
import posixpath

def safe_error(data,path):
 text=data.decode('utf-8','replace').replace(path,'<target>').replace(posixpath.dirname(path),'<parent>')
 text=re.sub(r'/home/[^/\s]+','<home>',text)
 return re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b','<node>',text)[:4096]

def metadata(path):
 parent=posixpath.dirname(path)
 p=subprocess.Popen(['talosctl','list','--depth','1','--long',parent],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ,'out');sel.register(p.stderr,selectors.EVENT_READ,'err')
 output=[];n=0;err=b'';stop=time.monotonic()+15;status='ok'
 while sel.get_map():
  if time.monotonic()>stop:status='metadata-timeout';break
  for key,_ in sel.select(.2):
   b=os.read(key.fileobj.fileno(),65536)
   if not b:sel.unregister(key.fileobj);continue
   if key.data=='err':err=(err+b)[:4096];continue
   n+=len(b)
   if n>1048576:status='metadata-output-cap';break
   output.append(b)
  if status!='ok':break
 if status!='ok':p.kill()
 try:rc=p.wait(timeout=3)
 except subprocess.TimeoutExpired:p.kill();rc=p.wait(timeout=3);status='metadata-timeout'
 sel.close();p.stdout.close();p.stderr.close();diagnostic=safe_error(err,path)
 if rc or status!='ok':return {'status':'not-found' if 'no such file' in diagnostic.lower() or 'notfound' in diagnostic.lower() else status if status!='ok' else 'metadata-query-failed','query_exit':rc,'diagnostic':diagnostic}
 try:
  lines=b''.join(output).decode('utf-8','strict').splitlines()
  headers=re.split(r'\s{2,}|\t+',lines[0].strip())
  if not {'NODE','MODE','UID','GID','SIZE(B)','LASTMOD','NAME'}<=set(headers):raise ValueError('metadata headers')
  starts=[];cursor=0
  for header in headers:
   start=lines[0].index(header,cursor);starts.append(start);cursor=start+len(header)
  matched=[]
  for line in lines[1:]:
   if not line.strip():continue
   if len(line)<starts[-1]:raise ValueError('metadata short row')
   row={key:line[start:starts[i+1] if i+1<len(starts) else None].strip() for i,(key,start) in enumerate(zip(headers,starts))}
   name=row['NAME'].split(' -> ',1)[0] if row['MODE'].startswith('L') else row['NAME']
   if posixpath.normpath(posixpath.join(parent,name))==path:matched.append(row)
  if not matched:return {'status':'not-found','query_exit':0,'diagnostic':'target absent from fresh immediate-parent listing'}
  if len(matched)!=1:raise ValueError('ambiguous metadata identity')
  row=matched[0]
  return {'status':'ok' if row['MODE'].startswith('-') else 'nonregular-type','query_exit':0,'path':path,'mode':row['MODE'],'owner':row['UID']+':'+row['GID'],'size':int(row['SIZE(B)']),'mtime_display':row['LASTMOD'],'diagnostic':''}
 except (ValueError,KeyError,IndexError,UnicodeError) as exc:return {'status':'metadata-parser-failed','query_exit':0,'diagnostic':str(exc)}

def refresh_one(request):
 path,old_size=request;before=metadata(path)
 result={'path':path,'status':before['status'],'bytes':0,'sha256':'','prefix_hex':'','signature':'unknown','query_exit':before['query_exit'],'diagnostic':before.get('diagnostic',''),'before':before,'after':None,'original_listing_size':old_size}
 if before['status']=='ok':
  if before['size']>1073741824:result['status']='size-cap'
  else:
   result.update(read_one([path,before['size']]))
   after=metadata(path);result['after']=after
   if result['status']=='ok':
    if after['status']!='ok':result['status']=after['status'];result['diagnostic']=after.get('diagnostic','')
    elif any(before.get(k)!=after.get(k) for k in ('mode','owner','size','mtime_display')):result['status']='metadata-changed';result['diagnostic']='fresh pre/post metadata differ'
 if result['status']!='ok':result.update(sha256='',prefix_hex='',signature='unknown')
 result['error_category']=result['status'] if result['status']!='ok' else ''
 return result

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for result in pool.map(refresh_one,paths):
  print(json.dumps(result),flush=True)
  if result['status']!='ok':print('bounded refresh query: '+result['error_category']+'; '+result['diagnostic'],file=sys.stderr,flush=True)
'''


SOURCE_SCRIPT = r'''
import subprocess,json,sys
p=subprocess.run(['talosctl','get','StaticPods.kubernetes.talos.dev','-o','json'],capture_output=True,timeout=12)
if p.returncode:sys.stderr.buffer.write(p.stderr);sys.exit(p.returncode)
text=p.stdout.decode();decoder=json.JSONDecoder()
def images(value):
 if isinstance(value,dict):
  for key,item in value.items():
   if key=='image' and isinstance(item,str):yield item
   else:yield from images(item)
 elif isinstance(value,list):
  for item in value:yield from images(item)
while text.strip():
 text=text.lstrip();obj,end=decoder.raw_decode(text);text=text[end:]
 for image in sorted(set(images(obj.get('spec',{})))):print(json.dumps({'resource_id':obj.get('metadata',{}).get('id',''),'image':image}))
'''


def mount_map(ctx):
    data,rc,ev=ctx.query('s4-talos-mountinfo',['talosctl','read','/proc/self/mountinfo'],15,max_bytes=1048576)
    rows=[];status='ok' if rc==0 else 'query-failed'
    if rc==0:
        try:
            for line in data.decode('utf-8','strict').splitlines():
                left,right=line.split(' - ',1);a=left.split();b=right.split()
                if len(a)<6 or len(b)!=3 or not a[0].isdigit() or not a[1].isdigit():raise ValueError('mountinfo schema')
                rows.append(a[:6]+[' '.join(a[6:])]+b+[ev])
            if not rows:raise ValueError('empty mountinfo')
        except (ValueError,UnicodeError):rows=[];status='parser-failed'
    write_tsv(ctx.out/'talos-mountinfo.tsv',['mount_id','parent_id','device','root','mountpoint','mount_options','optional_fields','filesystem','source','super_options','evidence'],rows)
    write_tsv(ctx.out/'talos-mountinfo-coverage.tsv',['query_exit','status','mounts','namespace','evidence'],[[rc,status,len(rows),'API daemon process',ev]])
    return {'mountinfo_query_exit':rc,'mountinfo_status':status,'mountinfo_rows':len(rows)}


def collect(ctx):
    mount_summary=mount_map(ctx)
    source_data,source_rc,source_ev=ctx.query('s4-talos-source-images',['python3','-c',SOURCE_SCRIPT],15,max_lines=1000)
    sources=[]
    for line in source_data.splitlines():
        try:
            r=json.loads(line);sources.append([r['resource_id'],r['image'],source_ev])
        except (ValueError,KeyError):pass
    write_tsv(ctx.out/'talos-image-sources.tsv',['resource_id','image','evidence'],sources)
    queue=collections.deque((p,0) for p in ROOTS)
    entries={}; listings=[]; boundaries=[]; evidence={}
    while queue and len(listings)<MAX_DIRS and len(entries)<MAX_MEMBERS:
        directory,depth=queue.popleft()
        data,rc,ev=ctx.query('s4-talos-list',['talosctl','list','--depth','1','--long',directory],15,max_lines=MAX_MEMBERS-len(entries)+2)
        rows=[];status='ok' if rc==0 else 'query-failed'
        if rc==0:
            try:rows=talos.file_rows(data,directory)
            except (ValueError,UnicodeError):status='parser-failed'
        if len(rows)>MAX_MEMBERS-len(entries):rows=[];status='member-cap'
        listings.append([directory,rc,status,len(rows),ev])
        for row in rows:
            path=row['path'];entries[path]=row;evidence[path]=ev
            if row['type']=='directory':
                if posixpath.basename(path) in BOUNDARIES:boundaries.append([path,'workload-or-pseudo-boundary'])
                elif depth+1>=MAX_DEPTH:boundaries.append([path,'depth-cap'])
                else:queue.append((path,depth+1))
    boundaries.extend([path,'directory-or-member-cap'] for path,depth in queue)
    def ids(path):
        return [r[0] for r in ctx.objects if r[2]==2 and (r[4]==path or (r[3]=='stored-ownership-unknown' and posixpath.dirname(path)==r[4]))]
    write_tsv(ctx.out/'talos-expanded-members.tsv', ['object_ids','path','type','mode','owner','size','link_target','evidence'], [[json.dumps(ids(p)),p,r['type'],r['mode'],r['owner'],r['size'],r.get('link_target',''),evidence[p]] for p,r in sorted(entries.items())])
    write_tsv(ctx.out/'talos-listing-coverage.tsv',['directory','query_exit','status','members','evidence'],listings)
    write_tsv(ctx.out/'talos-listing-boundaries.tsv',['path','reason'],boundaries)
    eligible=[];content=[]
    for path,r in sorted(entries.items()):
        if r['type']!='file':continue
        size=int(r['size'])
        if size>CONTENT_LIMIT:content.append([json.dumps(ids(path)),path,'size-cap',0,'','','unknown', '', evidence[path],'metadata-cap','size-cap','listed size exceeds 1 GiB'])
        else:eligible.append([path,size])
    for start in range(0,len(eligible),64):
        batch=eligible[start:start+64]
        data,rc,ev=ctx.query('s4-talos-content',['python3','-c',READ_SCRIPT,json.dumps(batch)],min(570,35*((len(batch)+3)//4)+10),max_lines=len(batch)+1)
        got={}
        for line in data.splitlines():
            try:r=json.loads(line);got[r['path']]=r
            except (ValueError,KeyError):pass
        for path,size in batch:
            r=got.get(path,{})
            content.append([json.dumps(ids(path)),path,r.get('status','query-failed'),r.get('bytes',0),r.get('sha256',''),r.get('prefix_hex',''),r.get('signature','unknown'),r.get('query_exit',rc),ev,'read',r.get('error_category',''),r.get('diagnostic','')])
    attempts=list(content)
    read_status_counts=dict(collections.Counter(row[2] for row in content))
    fallback=[[row[1],int(entries[row[1]]['size'])] for row in content if row[2]!='ok' and int(entries[row[1]]['size'])<=CONTENT_LIMIT]
    locations={row[1]:index for index,row in enumerate(content)}
    copy_status_counts=collections.Counter()
    for start in range(0,len(fallback),4):
        batch=fallback[start:start+4]
        data,rc,ev=ctx.query('s4-talos-content-copy',['python3','-c',COPY_SCRIPT,json.dumps(batch)],80,max_lines=len(batch)+1)
        got={}
        for line in data.splitlines():
            try:r=json.loads(line);got[r['path']]=r
            except (ValueError,KeyError):pass
        for path,size in batch:
            r=got.get(path,{})
            row=[json.dumps(ids(path)),path,r.get('status','query-failed'),r.get('bytes',0),r.get('sha256',''),r.get('prefix_hex',''),r.get('signature','unknown'),r.get('query_exit',rc),ev,'copy',r.get('error_category','query-failed' if not r else ''),r.get('diagnostic','')]
            attempts.append(row);content[locations[path]]=row;copy_status_counts[row[2]]+=1
    refresh=[[row[1],int(entries[row[1]]['size'])] for row in content if row[2]!='ok' and int(entries[row[1]]['size'])<=CONTENT_LIMIT]
    refresh_status_counts=collections.Counter()
    for start in range(0,len(refresh),4):
        batch=refresh[start:start+4]
        data,rc,ev=ctx.query('s4-talos-content-refresh',['python3','-c',REFRESH_SCRIPT,json.dumps(batch)],160,max_lines=len(batch)+1)
        got={}
        for line in data.splitlines():
            try:r=json.loads(line);got[r['path']]=r
            except (ValueError,KeyError):pass
        for path,size in batch:
            r=got.get(path,{})
            row=[json.dumps(ids(path)),path,r.get('status','query-failed'),r.get('bytes',0),r.get('sha256',''),r.get('prefix_hex',''),r.get('signature','unknown'),r.get('query_exit',rc),ev,'refresh-read',r.get('error_category','query-failed' if not r else ''),r.get('diagnostic','')]
            attempts.append(row);content[locations[path]]=row;refresh_status_counts[row[2]]+=1
    content_header=['object_ids','path','status','bytes','sha256','prefix_hex','signature','query_exit','evidence','method','error_category','diagnostic']
    write_tsv(ctx.out/'talos-content.tsv',content_header,content)
    write_tsv(ctx.out/'talos-content-attempts.tsv',content_header,attempts)
    # Actual mount evidence is retained; no unverified deepest-prefix attribution.
    links=[]
    for obj in ctx.objects:
        if obj[2]==2:
            links.append([obj[0],obj[4],'talos-expanded-members.tsv','path or immediate parent','talos-content.tsv','path or immediate parent','talos-mountinfo.tsv:API-daemon-namespace' if mount_summary['mountinfo_status']=='ok' else 'unknown:mountinfo-unavailable','unknown:no-original-image-manifest'])
    write_tsv(ctx.out/'talos-fact-index.tsv',['object_id','name','members_file','members_join','content_file','content_join','backing','image_integrity'],links)
    if not hasattr(ctx,'s4_summary'):ctx.s4_summary={}
    ctx.s4_summary['talos']={'source_query_exit':source_rc,'current_image_source_rows':len(sources),'directories':len(listings),'listing_failures':sum(r[2]!='ok' for r in listings),'expanded_members':len(entries),'boundaries':len(boundaries),'boundary_reasons':dict(collections.Counter(row[1] for row in boundaries)),'content_requested':len(content),'content_ok':sum(r[2]=='ok' for r in content),'content_read_status_counts':read_status_counts,'content_copy_status_counts':dict(copy_status_counts),'content_refresh_status_counts':dict(refresh_status_counts),'content_error_categories':dict(collections.Counter(row[10] for row in content if row[2]!='ok')),'content_status_counts':dict(collections.Counter(r[2] for r in content)),'content_by_root':{root:dict(collections.Counter(r[2] for r in content if r[1].startswith(root+'/'))) for root in ROOTS},'opaque_targets_listed':sum(any(r[0]==p and r[2]=='ok' for r in listings) for p in ('/etc/containerd','/opt/containerd','/var/system','/var/lib/containerd','/var/lib/kubelet','/var/log/containers'))}

    ctx.s4_summary['talos'].update(mount_summary)

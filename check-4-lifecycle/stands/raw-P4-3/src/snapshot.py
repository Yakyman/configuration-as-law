import os,pathlib,json,hashlib,base64,stat,subprocess,time
P=pathlib.Path
def obj(path,content=True):
 p=P(path);o={'path':str(p)}
 try:
  s=p.lstat();o.update(exists=True,dev=s.st_dev,ino=s.st_ino,nlink=s.st_nlink,mode=s.st_mode,uid=s.st_uid,gid=s.st_gid,size=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
  if stat.S_ISREG(s.st_mode):
   b=p.read_bytes();o.update(sha256=hashlib.sha256(b).hexdigest())
   if content:o['base64']=base64.b64encode(b).decode()
  if stat.S_ISLNK(s.st_mode):o['target']=os.readlink(p)
 except FileNotFoundError:o['exists']=False
 except OSError as e:o['error']={'errno':e.errno,'message':str(e)}
 return o
def jsonobj(p):
 o=obj(p)
 if 'base64' in o:
  try:o['json']=json.loads(base64.b64decode(o['base64']))
  except Exception as e:o['json_error']=str(e)
 return o
def fs(path):
 s=os.statvfs(path)
 return {'path':str(path),**{k:getattr(s,k) for k in ('f_bsize','f_frsize','f_blocks','f_bfree','f_bavail','f_files','f_ffree','f_favail','f_flag')}}
def snapshot(control,daemon_pid,keys):
 c=P(control);paths=[]
 for name in ('active','archive'):
  root=P('/var/lib/cal')/name;paths.append(root)
  paths+=sorted(root.rglob('*'))
 for key in keys:
  for name in ('active','archive'):paths.append(P('/var/lib/cal')/name/key/'operational.bin')
 objects={str(p):obj(p) for p in paths}
 gens={p.stem:jsonobj(p) for p in sorted((c/'generations').glob('*.json'))}
 docs={str(p):jsonobj(p) for p in [P('/etc/cal/root.json'),P('/home/alice/declaration.json'),P('/home/bob/declaration.json'),c/'current.json',c/'pending.json']}
 payloads=set(['/home/alice/p43/cache','/usr/local/lib/cal/alpha','/usr/local/lib/cal/beta','/opt/p43-payloads/primary','/opt/p43-payloads/alpha','/opt/p43-payloads/beta'])
 for o in list(gens.values())+list(docs.values()):
  for item in o.get('json',{}).get('programs',{}).values():
   if 'executable' in item:payloads.add(item['executable'])
 for p in (c/'executables').glob('*/*'):payloads.add(str(p))
 payload={p:obj(p,False) for p in sorted(payloads)}
 targets={(o['dev'],o['ino']) for o in objects.values() if o.get('exists') and stat.S_ISREG(o['mode'])}
 processes=[];live=[]
 for proc in P('/proc').iterdir():
  if not proc.name.isdigit():continue
  try:
   exe=os.readlink(proc/'exe');cmd=(proc/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace');start=(proc/'stat').read_text().rsplit(')',1)[1].split()[19]
   rec={'pid':int(proc.name),'exe':exe,'cmdline':cmd,'start_ticks':start,'fds':[],'maps':[]}
   for fd in (proc/'fd').iterdir():
    try:
     s=fd.stat()
     if (s.st_dev,s.st_ino) in targets:rec['fds'].append({'fd':fd.name,'target':os.readlink(fd),'dev':s.st_dev,'ino':s.st_ino})
    except OSError:pass
   for line in (proc/'maps').read_text().splitlines():
    if '/var/lib/cal/' in line:rec['maps'].append(line)
   if exe in payload or rec['fds'] or rec['maps']:live.append(rec)
   if int(proc.name)==daemon_pid or exe in payload:processes.append(rec)
  except (OSError,ValueError,IndexError):pass
 filler=P('/var/lib/cal/.filler')
 names=sorted(p.name for p in filler.iterdir()) if filler.exists() else []
 instrument={p:obj(p,False) for p in ['/usr/local/sbin/cald','/usr/local/lib/cal/apply-policy','/usr/local/bin/calctl','/usr/local/bin/cal-login','/root/q-main/radio-apply.py']}
 return {'utc_ns':time.time_ns(),'control':str(c),'objects':objects,'generations':gens,'documents':docs,'payloads':payload,'instrument':instrument,'filesystems':[fs('/'),fs('/var/lib/cal'),fs(c)],'mountinfo':P('/proc/self/mountinfo').read_text(),'daemon_pid':daemon_pid,'processes':processes,'live_consumers_or_handles':live,'policy':obj('/etc/apparmor.d/cal-stand'),'profiles':P('/sys/kernel/security/apparmor/profiles').read_text(),'filler':{'entries':len(names),'names_sha256':hashlib.sha256('\n'.join(names).encode()).hexdigest()}}

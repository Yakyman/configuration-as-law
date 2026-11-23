#!/usr/bin/env python3
"""Host controller; never an inventory target itself."""
import argparse,base64,collections,csv,datetime,hashlib,json,os,pathlib,re,selectors,shlex,signal,subprocess,sys,time
HERE=pathlib.Path(__file__).resolve().parent
HEADER=['id','machine','level','kind','name','members','evidence']
MEMBER=['path','type','mode','owner','size','mtime','executable','signature','persistence']
PROBE='/tmp/c1-collector/probe'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write_tsv(path,header,rows):
 with path.open('w',newline='') as f:
  w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(header);w.writerows(rows)
class Context:
 def __init__(self,args,transport,meta):
  self.args=args;self.machine=args.machine;self.transport=transport;self.meta=meta;self.out=pathlib.Path(args.output);self.out.mkdir(parents=True,exist_ok=False)
  for x in ('raw','members'): (self.out/x).mkdir()
  self.start=time.monotonic();self.deadline=self.start+1740;self.coverage=[];self.objects=[];self.ids=set();self.byid={};self.gaps=[];self.entries={};self.users=[];self.owned={};self.package_files=[];self.package_ownership_complete=True;self.deployed=False;self.readcache={};self.filesystem_complete=False;self.scan_counts=collections.Counter()
 def query(self,label,script,timeout=60,max_lines=None,bootstrap=False,max_bytes=67108864):
  if self.args.mode=='rehearsal':
   label=re.sub(r'^packages-flatpak-user-[0-9]+-', 'packages-flatpak-user-',label)
   label=re.sub(r'^(package-reason-xbps|package-files-xbps)-.*',r'\1',label)
   label=re.sub(r'^user-.*-(service|timer|unit-file)$',r'user-\1',label)
   label=re.sub(r'^(sudo|user-containers|user-images)-.*',r'\1',label)
   label=re.sub(r'^(package-manager-discovery-user)-.*',r'\1',label)
  label=re.sub(r'[^a-zA-Z0-9_.-]','-',label)[:120];name=f'{len(self.coverage)+1:04d}-{label}';prefix=self.out/'raw'/name;ev=f'raw/{name}.out'
  if isinstance(script,list):script=shlex.join(script)
  (pathlib.Path(str(prefix)+'.sh')).write_text(script+'\n');remaining=self.deadline-time.monotonic();timeout=min(timeout,max(0,remaining));begin=time.monotonic();rc=125;reason='global-deadline';out=b'';err=b''
  if timeout>0:
   if self.deployed and not bootstrap:
    delim='C1_'+hashlib.sha256(script.encode()).hexdigest();payload=f'export LC_ALL=C TZ=UTC\nexec {PROBE} run {max(1,int(timeout))} sh -s <<\'{delim}\'\n{script}\n{delim}\n'
   else:payload='export LC_ALL=C TZ=UTC\n'+script+'\n'
   # File input avoids blocking while a stalled transport stops consuming stdin.
   inp=pathlib.Path(str(prefix)+'.input');inp.write_text(payload)
   with inp.open('rb') as source:
    p=subprocess.Popen(self.transport,stdin=source,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,env={**os.environ,'LAB_RUN_TIMEOUT':str(max(1,int(timeout))),'LAB_SEPARATE_STDERR':'1'})
    sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ,'out');sel.register(p.stderr,selectors.EVENT_READ,'err');chunks={'out':[],'err':[]};total=0;lines=0;reason='';stop=begin+timeout
    while sel.get_map():
     if time.monotonic()>=stop:reason='timeout';rc=124;break
     for key,_ in sel.select(min(.2,max(0,stop-time.monotonic()))):
      b=os.read(key.fileobj.fileno(),65536)
      if not b:sel.unregister(key.fileobj);continue
      total+=len(b);lines+=b.count(b'\n') if key.data=='out' else 0
      if total>max_bytes or max_lines is not None and lines>max_lines:reason='output-cap';rc=75;break
      chunks[key.data].append(b)
     if reason:break
    if reason:
     try:os.killpg(p.pid,signal.SIGKILL)
     except ProcessLookupError:pass
    try:code=p.wait(timeout=3)
    except subprocess.TimeoutExpired:
     try:os.killpg(p.pid,signal.SIGKILL)
     except ProcessLookupError:pass
     try:code=p.wait(timeout=5)
     except subprocess.TimeoutExpired:raise RuntimeError('Transport process could not be reaped after SIGKILL')
    if not reason:rc=code
    sel.close();p.stdout.close();p.stderr.close();out=b''.join(chunks['out']);err=b''.join(chunks['err'])
   inp.unlink()
  pathlib.Path(str(prefix)+'.out').write_bytes(out);pathlib.Path(str(prefix)+'.err').write_bytes(err)
  duration=time.monotonic()-begin;self.coverage.append([label,rc,round(duration,3),len(out.splitlines()),len(out),ev,f'raw/{name}.err',reason or ('ok' if rc==0 else 'not-collected'),0]);self.flush()
  if rc not in (0,127):self.gaps.append(f'{label}: not collected or incomplete (exit {rc}; {ev})')
  return out,rc,ev
 def count(self,ev,n):
  for c in self.coverage:
   if c[5]==ev:c[8]+=n;break
 def add(self,level,kind,name,members,evidence):
  ident=hashlib.sha256(json.dumps([self.machine,level,kind,name],ensure_ascii=True).encode()).hexdigest()[:24]
  if ident in self.ids:ident=hashlib.sha256((ident+str(len(self.objects))).encode()).hexdigest()[:24]
  self.ids.add(ident);self.objects.append([ident,self.machine,level,kind,name,json.dumps(members,ensure_ascii=True,sort_keys=True),evidence]);self.byid[ident]=self.objects[-1];self.count(evidence.split(':')[0],1);return ident
 def write_members(self,ident,rows):
  rows=list(rows);write_tsv(self.out/'members'/f'{ident}.tsv',MEMBER,[[r.get(k,'unknown') if k!='owner' else r.get('owner',f"{r.get('uid','?')}:{r.get('gid','?')}") for k in MEMBER] for r in rows])
  if ident in self.byid:self.byid[ident][5]=json.dumps({'file':f'members/{ident}.tsv','count':len(rows),'detail':json.loads(self.byid[ident][5])})
  return f'members/{ident}.tsv'
 def safe_reads(self,paths,limit=16777216):
  pending=[p for p in paths if (p,limit) not in self.readcache]
  # Limit one batch's base64 amplification; an oversized individual record is refused.
  for i in range(0,len(pending),64):
   batch=pending[i:i+64];request='\n'.join(json.dumps({'path':p,'limit':limit}) for p in batch)+'\n';data,rc,ev=self.query('metadata-read-'+str(i),'printf %s '+shlex.quote(base64.b64encode(request.encode()).decode())+' | base64 -d | '+PROBE+' reads',120)
   got={}
   for line in data.splitlines():
    try:r=json.loads(line);got[r['path']]=(base64.b64decode(r.get('data','')),0 if r.get('status')=='ok' else 75,ev)
    except (ValueError,KeyError):continue
   for p in batch:self.readcache[p,limit]=got.get(p,(b'',rc or 75,ev))
  return {p:self.readcache[p,limit] for p in paths}
 def safe_read(self,path,limit=1048576):return self.safe_reads([path],limit)[path]
 def digests(self,requests,max_bytes=16777216):
  result={}
  for i in range(0,len(requests),2000):
   batch=requests[i:i+2000]; reverse=collections.defaultdict(list)
   for p,a in batch: reverse[(canonical(self,p),a)].append(p)
   req='\n'.join(json.dumps({'path':p,'algorithm':a,'limit':max_bytes}) for p,a in reverse)+'\n';data,rc,ev=self.query('package-digests-'+str(i),'printf %s '+shlex.quote(base64.b64encode(req.encode()).decode())+' | base64 -d | '+PROBE+' digests',120)
   for line in data.splitlines():
    try:
     r=json.loads(line);r['evidence']=ev
     for original in reverse.get((r['path'],r['algorithm']),[]):result[(original,r['algorithm'])]=r
    except (ValueError,KeyError):pass
  return result
 def digest(self,path,algorithm,max_bytes=16777216):
  r=self.digests([(path,algorithm)],max_bytes).get((path,algorithm),{});return r.get('digest',''),0 if r.get('status')=='ok' else 75,r.get('evidence','')
 def as_user(self,user,script):
  if isinstance(user,str):user=next(u for u in self.users if u['name']==user)
  if str(user['uid'])=='0':return script
  return 'command -v runuser >/dev/null 2>&1 || exit 127; runuser -u '+shlex.quote(user['name'])+' -- env HOME='+shlex.quote(user['home'])+' XDG_RUNTIME_DIR=/run/user/'+str(user['uid'])+' sh -c '+shlex.quote(script)
 def flush(self):
  write_tsv(self.out/'coverage.tsv',['query','exit_status','duration','rows','bytes','stdout','stderr','status','object_rows'],self.coverage)
  write_tsv(self.out/'objects.tsv',HEADER,self.objects)
 def finish(self):
  self.flush()
  for level in (1,2):write_tsv(self.out/f'level-{level}.tsv',HEADER,[r for r in self.objects if r[2]==level])
  # Directory entries establish ownership but are not packaged files.
  self.package_files=[r for r in self.package_files if r.get('recorded_type', self.entries.get(r.get('path',''),{}).get('type')) != 'directory']
  cols=['package','path','integrity','evidence','rule'];write_tsv(self.out/'package-files.tsv',cols,[[r.get(k,'unknown') for k in cols] for r in self.package_files])
  (self.out/'metadata.json').write_text(json.dumps({'utc':utc(),'machine':self.machine,'system':self.meta['system'],'duration':round(time.monotonic()-self.start,3),'filesystem_complete':self.filesystem_complete,'package_ownership_complete':self.package_ownership_complete,'gaps':list(dict.fromkeys(self.gaps)),'ready_for_observation':False},indent=2)+'\n')
  self.rehearsal_counts()
 def rehearsal_counts(self):
  target=os.environ.get('LAB_REHEARSAL_COUNTS');round_no=os.environ.get('LAB_REHEARSAL_ROUND')
  if self.args.mode!='rehearsal' or not target or not round_no:return
  counts=collections.Counter({'filesystem:'+k:v for k,v in self.scan_counts.items()})
  packages={};integrity=collections.defaultdict(list)
  for row in self.objects:
   counts['object:'+row[3]]+=1;counts['level:'+str(row[2])]+=1
   if row[3]=='package':
    try:facts=json.loads(row[5])
    except (TypeError,ValueError):facts={}
    if isinstance(facts,str):
     try:facts=json.loads(facts)
     except ValueError:facts={}
    packages[row[0]]=facts if isinstance(facts,dict) else {}
  for facts in packages.values():
   counts['reason:'+str(facts.get('manager','unknown'))+':'+str(facts.get('reason','unknown'))]+=1
   if facts.get('manager')=='rpm':counts['rpm-reason:'+str(facts.get('native_reason','unknown'))]+=1
  language_managers={'python','npm','cargo','gem'}
  known=lambda p:p.get('reason') in ('explicit','dependency')
  native_linked=lambda p:bool(p.get('native_package_ids'))
  for record in self.package_files:
   integrity[record['package']].append(record['integrity'] in ('unchanged','changed','missing'))
   kind=str(record.get('recorded_type',self.entries.get(record.get('path',''),{}).get('type','unresolved')))
   counts['package-files:type:'+kind]+=1
   if record['integrity']=='unknown':counts['package-files:unknown-type:'+kind]+=1
  counts.update({'packages:total':len(packages),'packages:reason-known':sum(p.get('reason') in ('explicit','dependency') for p in packages.values()),
   'packages:reason-known-nonlanguage':sum(known(p) and p.get('manager') not in language_managers for p in packages.values()),
   'packages:language-reason-known-own-manager':sum(known(p) and p.get('manager') in language_managers and p.get('reason_source') not in (None,'unknown','native-owner') for p in packages.values()),
   'packages:language-reason-known-native-derived':sum(known(p) and p.get('manager') in language_managers and p.get('reason_source')=='native-owner' for p in packages.values()),
   'packages:language-native-linked-total':sum(p.get('manager') in language_managers and native_linked(p) for p in packages.values()),
   'packages:language-native-linked-reason-known':sum(p.get('manager') in language_managers and native_linked(p) and known(p) for p in packages.values()),
   'packages:integrity-any-known':sum(any(integrity[p]) for p in packages),'packages:integrity-all-known':sum(bool(integrity[p]) and all(integrity[p]) for p in packages),
   'package-files:total':len(self.package_files),'package-files:integrity-known':sum(sum(v) for v in integrity.values()),
   'collector:gaps':len(self.gaps),
   'collector:unsupported-brew-adapter':sum(g.startswith('brew manager present but complete installed package manifest adapter unavailable.') for g in self.gaps),
   'collector:filesystem-complete':int(self.filesystem_complete),'collector:reduction-complete':1})
  for level in ('1','2'):counts.setdefault('level:'+level,0)
  path=pathlib.Path(target);fresh=not path.exists()
  with path.open('a') as f:
   writer=csv.writer(f,delimiter='\t',lineterminator='\n')
   if fresh:writer.writerow(['round','kind','rows'])
   writer.writerows([round_no,k,v] for k,v in sorted(counts.items()))


def lines(ctx,kind,label,script,user=None):
 data,rc,ev=ctx.query(label,ctx.as_user(user,script) if user else script)
 if rc:return
 if kind in ('firewall-nft','container','container-image','docker-container','docker-image'):
  try:
   decoded=data.decode();items=[]
   if kind.startswith('docker-'):items=[json.loads(x) for x in decoded.splitlines() if x.strip()]
   else:
    result=json.loads(decoded)
    items=result.get('nftables',[]) if kind=='firewall-nft' else result if isinstance(result,list) else [result]
   for item in items:
    if kind=='firewall-nft':
     for typ,rule in item.items():
      if typ=='metainfo':continue
      name='/'.join(str(rule.get(k,'')) for k in ('family','table','chain','name','handle'))
      ctx.add(1,'firewall-'+typ,name,rule,ev)
    else:
     name=str(item.get('Id',item.get('ID',item.get('id',item.get('Repository','unknown')))))
     ctx.add(1,kind,(user['name']+':' if user else '')+name,item,ev)
  except (ValueError,TypeError,AttributeError):ctx.gaps.append(label+': failed normalization; not collected')
  return
 for line in data.decode(errors='replace').splitlines():
  if line.strip():ctx.add(1,kind,(user['name']+':' if user else '')+line.split()[0],{'record':line},ev)

def general(ctx):
 # Capture accounts before querying user managers, but never password hashes.
 for path,kind in [('/etc/passwd','account'),('/etc/group','group')]:
  b,rc,ev=ctx.safe_read(path)
  if rc:continue
  for s in b.decode(errors='replace').splitlines():
   a=s.split(':');ctx.add(1,kind,a[0],{'record':s},ev)
   if kind=='account' and len(a)==7 and a[2].isdigit():ctx.users.append({'name':a[0],'uid':int(a[2]),'home':a[5],'shell':a[6]})
 data,rc,ev=ctx.query('filesystem',PROBE+' scan',620,max_bytes=536870912)
 summaries=[]
 for row in data.splitlines():
  try:r=json.loads(row)
  except ValueError:ctx.gaps.append('filesystem: invalid record');continue
  if 'path' in r:ctx.entries[r['path']]=r;ctx.scan_counts['entry-rows']+=1
  elif r.get('summary'):summaries.append(r)
  elif 'alias' in r:ctx.scan_counts['alias-rows']+=1
  elif 'error' in r:
   ctx.scan_counts['error-rows']+=1
   ctx.gaps.append('filesystem error: '+r['error'])
   print('filesystem traversal error: '+str(r.get('detail','unknown error')),file=sys.stderr)
 ctx.filesystem_complete=rc==0 and bool(summaries) and summaries[-1]['complete'];ctx.filesystem_evidence=ev;ctx.count(ev,len(ctx.entries))
 if not ctx.filesystem_complete:ctx.gaps.append('stored objects: traversal incomplete; emitted groups are partial')
 import packages
 packages.collect(ctx)
 if hasattr(packages,'collect_metadata'):packages.collect_metadata(ctx)
 for kind,cmd in [('service','systemctl --no-pager --no-legend list-units --all --type=service'),('timer','systemctl --no-pager --no-legend list-timers --all'),('unit-file','systemctl --no-pager --no-legend list-unit-files --type=service,timer'),('runit-service',"for p in /var/service/* /run/runit/service/* /etc/service/*; do test -e \"$p\" || continue; printf '%s\\t' \"$p\"; readlink \"$p\" || :; done"),('openrc-service','rc-status --all'),('openrc-runlevel','rc-update show -v'),('port','ss -H -lntu'),('firewall-nft','nft -j list ruleset'),('firewall-ipv4','iptables-save'),('firewall-ipv6','ip6tables-save'),('saved-network','nmcli -t -f NAME,UUID,TYPE,DEVICE connection show'),('polkit-action','pkaction'),('container','podman ps -a --no-trunc --format json'),('container-image','podman images --no-trunc --format json'),('docker-container','docker ps -a --no-trunc --format "{{json .}}"'),('docker-image','docker images --no-trunc --format "{{json .}}"')]:
  lines(ctx,kind,kind,cmd)
 # Only pseudo-filesystem names and symlink targets; no cat, ps or lsmod.
 lines(ctx,'process','process-executables',"for p in /proc/[0-9]*; do test -d \"$p\" || continue; printf '%s\\t' \"${p##*/}\"; readlink \"$p/exe\" || printf 'unknown\\n'; done")
 lines(ctx,'module-name','module-names',"for p in /sys/module/*; do test -d \"$p\" && printf '%s\\n' \"${p##*/}\"; done")
 lines(ctx,'driver','driver-names',"for p in /sys/bus/*/drivers/*; do test -d \"$p\" && printf '%s\\n' \"$p\"; done")
 for u in ctx.users:
  if u['uid']!=0 and (u['uid']<1000 or u['shell'].endswith(('nologin','false'))):continue
  for kind,cmd in [('service','list-units --all --type=service'),('timer','list-timers --all'),('unit-file','list-unit-files --type=service,timer')]:lines(ctx,'user-'+kind,'user-'+u['name']+'-'+kind,'systemctl --user --no-pager --no-legend '+cmd,u)
  lines(ctx,'sudo-access','sudo-'+u['name'],'sudo -n -l -U '+shlex.quote(u['name']))
  lines(ctx,'container','user-containers-'+u['name'],'podman ps -a --no-trunc --format json',u)
  lines(ctx,'container-image','user-images-'+u['name'],'podman images --no-trunc --format json',u)
 # Rule files are captured bounded, as data. Never execute discovered code.
 rules=[];net=[]
 for p,r in ctx.entries.items():
  if r['type']!='file':continue
  if p in ('/etc/sudoers','/etc/doas.conf','/etc/security/access.conf') or p.startswith(('/etc/sudoers.d/','/etc/polkit-1/','/usr/share/polkit-1/','/etc/pam.d/','/etc/security/access.d/')):rules.append(p)
  if p.startswith(('/etc/NetworkManager/system-connections/','/etc/systemd/network/','/var/lib/iwd/','/etc/wpa_supplicant/')) or p in ('/etc/network/interfaces','/etc/wpa_supplicant.conf'):net.append(p)
 for p,(b,rc,e) in ctx.safe_reads(rules,1048576).items():
  if rc==0:ctx.add(1,'access-rule',p,{'content':b.decode(errors='replace')},e)
 for p in net:ctx.add(1,'saved-network-file',p,{'metadata':ctx.entries[p],'content':'not read: may contain credentials'},ev)
 stored(ctx)

def canonical(ctx,p):
 for _ in range(32):
  bits=p.split('/');changed=False
  for i in range(1,len(bits)):
   prefix='/'.join(bits[:i+1]);r=ctx.entries.get(prefix,{})
   if r.get('type')=='symlink':
    target=r.get('target','');p=os.path.normpath((target if target.startswith('/') else os.path.dirname(prefix)+'/'+target)+'/'+'/'.join(bits[i+1:]));changed=True;break
  if not changed:return p
 return p

def stored(ctx):
 for p,owners in list(ctx.owned.items()):ctx.owned.setdefault(canonical(ctx,p),set()).update(owners)
 groups=collections.defaultdict(list);configuration=[];ev=ctx.filesystem_evidence
 install_paths=[p for p in ctx.entries if p.startswith('/var/log/installer/') or p in ('/var/log/dpkg.log','/var/log/apt/history.log')]
 scripts=[p for p in ctx.entries if p.endswith(('.postinst','.preinst','.postrm','.prerm')) and '/var/lib/dpkg/info/' in p]
 script_data=ctx.safe_reads(scripts,1048576)
 for p,r in sorted(ctx.entries.items()):
  if r.get('atomic'):ctx.add(2,r['atomic'],p,{'metadata':r,'expanded':False},ev)
  if p in ctx.owned:continue
  groups[os.path.dirname(p)].append(r)
  if r['type']=='file' and (r.get('executable') or r.get('shebang') or r.get('startup')):
   kind='executable-code-outside-packages' if ctx.package_ownership_complete else 'code-ownership-unresolved';ctx.add(2,kind,p,r,ev)
  home=any(p.startswith(u['home'].rstrip('/')+'/') for u in ctx.users if u['home'] not in ('/','/nonexistent','/dev/null'))
  if r['type']=='file' and (p.startswith(('/etc/','/home/','/root/')) or home):
   refs=[f'{q} ({e})' for q,(b,rc,e) in script_data.items() if rc==0 and p.encode() in b]
   configuration.append([p,'unknown','mtime is last modification, not creation; a script path mention does not prove execution',r['mtime'],r.get('ctime','unknown'),json.dumps(refs),json.dumps(install_paths),ev])
 for directory,rows in sorted(groups.items()):
  kind='stored-outside-packages' if ctx.package_ownership_complete else 'stored-ownership-unresolved'
  ident=ctx.add(2,kind,directory,{},ev);member=ctx.write_members(ident,rows);ctx.objects[-1][5]=json.dumps({'file':member,'count':len(rows),'complete':ctx.filesystem_complete})
 write_tsv(ctx.out/'configuration-origin.tsv',['path','created','rule_uncertainty','mtime','ctime','package_script_mentions','installation_time_evidence','evidence'],configuration)

def main():
 global PROBE
 ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['instrument-test','rehearsal','observe']);ap.add_argument('machine');ap.add_argument('output');ap.add_argument('--container');ap.add_argument('--family',choices=['rpm','apk','pacman','xbps','portage']);args=ap.parse_args([x if x not in ('--instrument-test','--rehearsal','--observe') else x[2:] for x in sys.argv[1:]])
 # Observation remains a separate authorization/rehearsal step.
 if args.mode=='observe' and not os.environ.get('C1_INPUTS_COMMIT'):sys.exit('Set C1_INPUTS_COMMIT to the committed inputs before observation.')
 if not re.fullmatch(r'[a-z][a-z0-9-]{0,39}',args.machine):sys.exit('A synthetic machine ID is required')
 lab=pathlib.Path(os.environ.get('LAB_ROOT','.')).resolve()
 if args.container:
  if not args.family:sys.exit('--container requires --family')
  # Only explicitly created task containers with a family declaration.
  manifest=json.loads((lab/'containers'/f'{args.container}.json').read_text())
  if manifest.get('throwaway') is not True or manifest.get('family')!=args.family or manifest.get('check_system',True):sys.exit('Refusing a non-throwaway/check container')
  meta={'system':manifest['distribution']};transport=['podman','--root',str(lab/'podman-root'),'--runroot',str(lab/'podman-run'),'--storage-driver','vfs','exec','-i',args.container,'sh']
 else:
  meta=json.loads((lab/'C1/vms'/args.machine/'meta.json').read_text())
  if args.mode=='instrument-test' and meta['system']!='debian':sys.exit('Instrument testing restricted to throwaway Debian; no target command was run.')
  if args.mode=='rehearsal' and not args.machine.startswith('reh-'):sys.exit('Rehearsal requires a named throwaway reh- clone.')
  if args.mode=='rehearsal':
   disk=lab/'C1/vms'/args.machine/'disk.qcow2'
   check=subprocess.run(['qemu-img','info','-U','--output=json',str(disk)],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
   info=json.loads(check.stdout) if check.returncode==0 else {}
   backing=pathlib.Path(info.get('full-backing-filename',info.get('backing-filename','')))
   expected=(lab/'C1/base'/(meta['system']+'.qcow2')).resolve()
   if not disk.is_file() or not backing.is_absolute() or backing.resolve()!=expected or expected.stat().st_mode & 0o222:sys.exit('Rehearsal requires a disposable overlay on a read-only registered base.')
  transport=[str(lab/'lab.sh'),'run',args.machine,'--root']
 ctx=Context(args,transport,meta)
 def deadline_alarm(signum,frame): raise TimeoutError('Total run deadline')
 signal.signal(signal.SIGALRM,deadline_alarm);signal.alarm(1760)
 try:
  if meta['system']=='talos':
   import talos
   talos.collect(ctx)
   return 0
  packed=HERE/'probe-linux-amd64.gz'
  binary=packed.read_bytes() if packed.exists() else b''.join(p.read_bytes() for p in sorted(HERE.glob('probe-linux-amd64.gz.part-*')))
  encoded=base64.b64encode(binary).decode()
  script='case "$(uname -m)" in x86_64) ;; *) exit 69;; esac\nfor d in /tmp/c1-collector /var/tmp/c1-collector /run/c1-collector; do\n mkdir -m 700 "$d" 2>/dev/null || continue\n printf %s '+shlex.quote(encoded)+' | base64 -d | gzip -d > "$d/probe"\n chmod 700 "$d/probe"\n if "$d/probe" run 1 true 2>/dev/null; then printf "%s\\n" "$d/probe"; exit 0; fi\n rm -f "$d/probe"; rmdir "$d"\ndone\nexit 69'
  data,rc,ev=ctx.query('bootstrap',script,120,bootstrap=True)
  if rc:ctx.gaps.append('probe deployment failed; requires writable executable staging directory');return 2
  PROBE=data.decode().strip()
  if PROBE not in ('/tmp/c1-collector/probe','/var/tmp/c1-collector/probe','/run/c1-collector/probe'):raise ValueError('Invalid bootstrap path')
  ctx.deployed=True;general(ctx)
 except Exception as exc:
  ctx.gaps.append('controller exception: '+type(exc).__name__+': '+str(exc));raise
 finally:
  signal.alarm(0)
  if ctx.deployed:
   ctx.deadline=max(ctx.deadline,time.monotonic()+10)
   _,rc,ev=ctx.query('cleanup','rm -f '+PROBE+'; rmdir '+shlex.quote(os.path.dirname(PROBE)),10,bootstrap=True)
   if rc:ctx.gaps.append('probe cleanup failed')
  ctx.finish()
 return 0 if ctx.filesystem_complete else 2
if __name__=='__main__':sys.exit(main())

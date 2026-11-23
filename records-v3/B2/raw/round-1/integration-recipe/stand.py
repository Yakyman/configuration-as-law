#!/usr/bin/python3 -I
"""Finite declaration prototype. Development instrument, not a complete P4 system."""
import argparse, base64, contextlib, fcntl, grp, hashlib, json, os, pathlib, pwd
import re, shutil, signal, stat, subprocess as sp, sys, tempfile, time

sys.dont_write_bytecode=True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import guard
ROOT=pathlib.Path('/var/lib/stand')
CURRENT=ROOT/'current'
POLICY=None

def run(*args, check=True, input=None):
    backend={'systemctl':'/usr/bin/systemctl','nft':'/usr/sbin/nft','nmcli':'/usr/bin/nmcli',
             'useradd':'/usr/sbin/useradd','userdel':'/usr/sbin/userdel','usermod':'/usr/sbin/usermod',
             'groupadd':'/usr/sbin/groupadd','groupdel':'/usr/sbin/groupdel'}
    args=(backend.get(str(args[0]),args[0]),)+args[1:]
    p=sp.run([str(a) for a in args],input=input,text=True,stdout=sp.PIPE,stderr=sp.PIPE,timeout=90, env={'PATH':'/usr/sbin:/usr/bin:/sbin:/bin','HOME':'/root','LANG':'C.UTF-8','LC_ALL':'C.UTF-8'})
    if check and p.returncode: raise RuntimeError('command failed: '+str(args[0])+': '+p.stderr.strip())
    return p

def digest(data): return hashlib.sha256(data).hexdigest()
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'))
def syncdir(p):
    fd=os.open(str(p),os.O_RDONLY|os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)
def atomic(p,data,mode=0o644,uid=0,gid=0):
    p=pathlib.Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.stand-',dir=p.parent)
    try:
        with os.fdopen(fd,'wb') as f:
            f.write(data.encode() if isinstance(data,str) else data)
            os.fchmod(f.fileno(),mode);os.fchown(f.fileno(),uid,gid);f.flush();os.fsync(f.fileno())
        os.replace(name,p);syncdir(p.parent)
    finally:
        if os.path.exists(name): os.unlink(name)
def filevalue(path):
    p=pathlib.Path(path)
    try:
        s=p.lstat();v={'path':str(p),'mode':stat.S_IMODE(s.st_mode),'uid':s.st_uid,'gid':s.st_gid}
        if p.is_symlink():v.update(kind='symlink',target=os.readlink(p))
        elif p.is_file():v.update(kind='file',sha256=sha(p))
        else:v.update(kind='other')
        return v
    except FileNotFoundError:return {'path':str(p),'missing':True}
def manifest(row,d):
    if 'files_manifest' in row:
        name=row['files_manifest']
        if pathlib.PurePosixPath(name).name!=name:raise ValueError('manifest must be in declaration directory')
        data=(d/name).read_bytes()
        if digest(data)!=row['manifest_sha256']:raise ValueError('manifest digest mismatch')
        return json.loads(data)
    return row.get('files',[])
def load(d, guarded=True):
    d=pathlib.Path(d).resolve()
    rows=[]
    for line in (d/'machine.jsonl').read_text().splitlines():
        if line.strip():rows.append(json.loads(line))
    ids=[r['id'] for r in rows]
    if len(set(ids))!=len(ids):raise ValueError('duplicate line id')
    for r in rows:
        if not re.fullmatch('[a-zA-Z0-9_.:@+-]+',r['id']):raise ValueError('invalid id '+r['id'])
        if r['type'] not in ('base','program','code','account','service','timer','privilege','login-key','password-login','rule','port','wifi','bluetooth','boot'):
            raise ValueError('unsupported line type '+r['type'])
        if r['type'] in ('base','program','code'):
            if not r.get('version') or not r.get('source'):raise ValueError('source/version required')
            for f in manifest(r,d):
                p=f['path']
                if not p.startswith('/') or '..' in pathlib.PurePosixPath(p).parts:raise ValueError('invalid file path')
                if f.get('kind') not in ('file','symlink'):raise ValueError('unsupported file kind')
                if r.get('managed'):
                    if not p.startswith('/opt/stand/pkgs/'+r['id']+'/'):raise ValueError('managed artifact path outside its package')
                    if f['kind']=='symlink':raise ValueError('managed symlinks unsupported')
                    b=base64.b64decode(f['content_b64'],validate=True)
                    if digest(b)!=f['sha256']:raise ValueError('payload hash mismatch')
                    if f['mode'] & 0o7000:raise ValueError('special permission bits refused')
        if r['type'] in ('service','timer') and r.get('managed'):
            if not re.fullmatch(r'stand-[a-zA-Z0-9_-]+\.(service|timer)',r['unit']):raise ValueError('managed unit name required')
            if sha_text(r['unit_text'])!=r['unit_sha256']:raise ValueError('unit hash mismatch')
        if r['type']=='account' and r.get('managed') and not (1100<=r['uid']<=60000):raise ValueError('managed uid range 1100..60000')
        if r['type']=='rule' and r.get('managed'):
            if not re.fullmatch('(tcp|udp) dport [1-9][0-9]{0,4} (accept|drop)',r['expression']):raise ValueError('unsupported nft expression')
        if r['type']=='password-login' and r['allowed']:raise ValueError('password login enabling unsupported')
        if r['type']=='boot' and r['order']!=['disk']:raise ValueError('this VM fixes boot order to disk')
    owners={}
    for r in rows:
        for f in manifest(r,d) if r['type'] in ('base','program','code') else []:
            val={k:v for k,v in f.items() if k!='content_b64'}
            if f['path'] in owners and owners[f['path']]!=val:raise ValueError('conflicting file contributions')
            owners[f['path']]=val
    if guarded:guard.validate(rows,d)
    return rows
def sha_text(s):return digest(s.encode())
def current_dir():return CURRENT.resolve(strict=True)
def desired_file(f):return {k:v for k,v in f.items() if k not in ('content_b64','size')}
def account_value(name):
    try:
        p=pwd.getpwnam(name)
        groups=sorted(grp.getgrgid(x).gr_name for x in os.getgrouplist(name,p.pw_gid))
        return {'name':p.pw_name,'uid':p.pw_uid,'gid':p.pw_gid,'groups':groups,'shell':p.pw_shell,'home':p.pw_dir,'gecos':p.pw_gecos}
    except KeyError:return {'missing':True}
def expected_account(r):return {k:r[k] for k in ('name','uid','gid','groups','shell','home','gecos')}
def service_value(r):
    unit=r['unit']
    if r.get('scope')=='user-global':
        return {'unit':unit,'enabled':run('systemctl','--global','is-enabled',unit,check=False).stdout.strip(),
                'unit_sha256':sha(r['unit_path'])}
    p=run('systemctl','show',unit,'-p','LoadState','-p','UnitFileState','-p','ActiveState','-p','FragmentPath',check=False)
    v=dict(line.split('=',1) for line in p.stdout.splitlines() if '=' in line)
    path=v.get('FragmentPath','')
    enabled=run('systemctl','is-enabled',unit,check=False).stdout.strip()
    out={'unit':unit,'enabled':enabled,'unit_sha256':sha(path) if path and pathlib.Path(path).is_file() else None}
    if 'active' in r:out['active']=v.get('ActiveState')=='active'
    return out
def rule_value(r):
    if r.get('backend')=='mount':
        opts=run('/usr/bin/findmnt','-n','-o','OPTIONS','--target',r['path']).stdout.strip()
        return {'effective':','.join(sorted(opts.split(','))),'path':r['path']}
    if r.get('backend')=='nft-chain':
        p=run('nft','-j','list','table','inet','stand',check=False)
        if p.returncode:return {'missing':True}
        chains=[x['chain'] for x in json.loads(p.stdout)['nftables'] if 'chain' in x and x['chain']['name']=='input']
        return {'effective':[{k:v for k,v in x.items() if k!='handle'} for x in chains]}
    p=run('nft','-j','list','table','inet','stand',check=False)
    if p.returncode:return {'missing':True}
    doc=json.loads(p.stdout)
    rules=[i['rule'] for i in doc.get('nftables',[]) if 'rule' in i and i['rule'].get('comment')==r['id']]
    out=[]
    for rule in rules:
        out.append({k:v for k,v in rule.items() if k not in ('handle','index')})
    # Also read the effective textual form, stripping only the handle annotation.
    txt=run('nft','list','table','inet','stand').stdout
    textrows=[re.sub(r'\s+# handle \d+','',s.strip()) for s in txt.splitlines() if 'comment "'+r['id']+'"' in s]
    return {'effective':textrows,'rules':out}
def profile_path(r):return pathlib.Path('/etc/NetworkManager/system-connections')/('stand-'+r['id']+'.nmconnection')
def wifi_text(r):
    return ('[connection]\nid='+r['name']+'\nuuid='+r['uuid']+'\ntype=wifi\nautoconnect='+str(r['autoconnect']).lower()+
            '\n[wifi]\nmode=infrastructure\nssid='+r['ssid']+'\n[ipv4]\nmethod=auto\n[ipv6]\nmethod=disabled\n')
def bt_path(r):return pathlib.Path('/var/lib/bluetooth')/r['adapter']/r['address']/'info'
def bt_text(r):return '[General]\nName='+r['name']+'\nTrusted='+str(r['trusted']).lower()+'\nBlocked=false\n'
def port_values(protocol='tcp'):
    p=run('ss','-H','-ln'+('t' if protocol=='tcp' else 'u'),check=False)
    return sorted(set(line.split()[3] for line in p.stdout.splitlines()))
def observe(r,d):
    typ=r['type']
    if typ in ('base','program','code'):
        expected=[desired_file(f) for f in manifest(r,d)]
        value=[filevalue(f['path']) for f in expected]
        return value==expected,{'version':r['version'],'source':r['source'],'files':value}
    if typ=='account':
        v=account_value(r['name']);return v==expected_account(r),v
    if typ in ('service','timer'):
        v=service_value(r);want={k:r[k] for k in ('unit','enabled','unit_sha256')}
        if 'active' in r:want['active']=r['active']
        return v==want,v
    if typ=='privilege':
        p=pathlib.Path(r['path']);v=p.read_text() if p.exists() else None
        actual={'effective':v,'mode':stat.S_IMODE(p.stat().st_mode) if p.exists() else None,'uid':p.stat().st_uid if p.exists() else None,'gid':p.stat().st_gid if p.exists() else None}
        return actual=={'effective':r['text'],'mode':r['mode'],'uid':r['uid'],'gid':r['gid']},actual
    if typ=='login-key':
        p=pathlib.Path(r['path']);v=p.read_text() if p.exists() else None
        actual={'keys':v,'mode':stat.S_IMODE(p.stat().st_mode) if p.exists() else None,'uid':p.stat().st_uid if p.exists() else None,'gid':p.stat().st_gid if p.exists() else None}
        return actual=={'keys':r['text'],'mode':r['mode'],'uid':r['uid'],'gid':r['gid']},actual
    if typ=='password-login':
        p=run('/usr/sbin/sshd','-T');v={x.split()[0]:x.split()[1] for x in p.stdout.splitlines()}
        val={'passwordauthentication':v['passwordauthentication'],'kbdinteractiveauthentication':v['kbdinteractiveauthentication']}
        return val=={'passwordauthentication':'no','kbdinteractiveauthentication':'no'},val
    if typ=='rule':
        if r.get('backend')=='mount':
            v=rule_value(r);return set(r['required_options']).issubset(set(v['effective'].split(','))),v
        if r.get('backend')=='nft-chain':
            v=rule_value(r);return v=={'effective':[r['chain']]},v
        v=rule_value(r);expected=r['expression']+' comment "'+r['id']+'"'
        return v.get('effective')==[expected],v
    if typ=='port':
        ports=port_values(r['protocol']);v={'protocol':r['protocol'],'port':r['port'],'local':r['local'],'listening':r['local'] in ports}
        return v['listening']==r['listening'],v
    if typ=='wifi':
        p=profile_path(r);content=p.read_text() if p.exists() else None
        q=run('nmcli','-g','connection.uuid','connection','show',r['uuid'],check=False)
        v={'profile':content,'backend_uuid':q.stdout.strip() if q.returncode==0 else None,'hardware':'not tested on hardware'}
        if r['state']=='connected':
            active=run('nmcli','-g','UUID','connection','show','--active',check=False).stdout.splitlines()
            v['connected']=r['uuid'] in active
        return content==wifi_text(r) and v['backend_uuid']==r['uuid'] and v.get('connected',True),v
    if typ=='bluetooth':
        p=bt_path(r)
        if r['state']=='prepared':
            v={'local_profile':p.read_text() if p.exists() else None,'paired':False,'hardware':'not tested on hardware'}
            return v['local_profile']==bt_text(r),v
        q=run('/usr/bin/bluetoothctl','info',r['address'],check=False)
        v={'paired':'Paired: yes' in q.stdout,'trusted':('Trusted: yes' in q.stdout)}
        return q.returncode==0 and v['paired'] and v['trusted']==r['trusted'],v
    if typ=='boot':
        v={'order':['disk'],'firmware':'external fixed firmware','guest_can_change':False}
        return r['order']==v['order'] and r['guest_can_change']==False,v
    raise ValueError(typ)
def verify(d=None,emit=True):
    d=pathlib.Path(d) if d else current_dir();rows=load(d);out=[]
    for r in rows:
        try:ok,v=observe(r,d)
        except Exception as e:ok=False;v={'error':str(e)}
        item={'id':r['id'],'type':r['type'],'ok':ok,'observed':v};out.append(item)
        if emit:print(r['id']+'\t'+r['type']+'\t'+('OK' if ok else 'FAIL')+'\t'+digest(canonical(v).encode()),flush=True)
    return out
def managed_files(rows,d):
    return {f['path']:f for r in rows if r['type'] in ('program','code','base') for f in manifest(r,d) if f['path'].startswith('/opt/stand/pkgs/')}
def terminate_files(paths):
    victims=[]
    for proc in pathlib.Path('/proc').iterdir():
        if not proc.name.isdigit() or int(proc.name)==os.getpid():continue
        try:
            exe=os.readlink(proc/'exe').removesuffix(' (deleted)')
            cmd=(proc/'cmdline').read_bytes().split(b'\0')
            maps=(proc/'maps').read_text()
            if exe in paths or any(os.fsencode(p) in cmd or p in maps for p in paths):victims.append(int(proc.name))
        except (OSError,PermissionError):pass
    for pid in victims:
        try:os.kill(pid,signal.SIGKILL)
        except ProcessLookupError:pass
    deadline=time.monotonic()+10
    for pid in victims:
        while pathlib.Path('/proc',str(pid)).exists() and time.monotonic()<deadline:
            try:
                if (pathlib.Path('/proc',str(pid))/'stat').read_text().split()[2]=='Z':break
            except FileNotFoundError:break
            time.sleep(.02)
    return victims
def activate(rows,d,old,olddir):
    oldfiles=managed_files(old,olddir) if olddir else {};newfiles=managed_files(rows,d)
    coverage={f['path']:f for r in rows if r['type'] in ('base','program','code') for f in manifest(r,d)}
    changed={p for p,f in oldfiles.items() if p not in coverage or desired_file(coverage[p])!=desired_file(f)}
    new_by_id={r['id']:r for r in rows}
    for r in old:
        if r['type'] in ('service','timer') and r.get('managed') and new_by_id.get(r['id'])!=r:
            run('systemctl','stop',r['unit'])
            run('systemctl','disable',r['unit'],check=False)
            pathlib.Path('/etc/systemd/system',r['unit']).unlink(missing_ok=True)
    killed=terminate_files(changed)
    for p in set(oldfiles)-set(coverage):
        pathlib.Path(p).unlink(missing_ok=True);syncdir(pathlib.Path(p).parent)
    for p,f in newfiles.items():
        if filevalue(p)!=desired_file(f):atomic(p,base64.b64decode(f['content_b64']),f['mode'],f['uid'],f['gid'])
    for r in old:
        if r['id'] in new_by_id or not r.get('managed'):continue
        t=r['type']
        if t=='account':run('userdel',r['name']);run('groupdel',r['name'],check=False)
        elif t in ('privilege','login-key'):pathlib.Path(r['path']).unlink(missing_ok=True)
        elif t=='wifi':run('nmcli','connection','delete',r['uuid'],check=False);profile_path(r).unlink(missing_ok=True)
        elif t=='bluetooth':shutil.rmtree(bt_path(r).parent,ignore_errors=True)
    for r in rows:
        t=r['type']
        if t=='account' and r.get('managed'):
            v=account_value(r['name'])
            if v.get('missing'):
                run('groupadd','-g',r['gid'],r['name'])
                run('useradd','-u',r['uid'],'-g',r['gid'],'-d',r['home'],'-s',r['shell'],'-c',r['gecos'],'-m',r['name'])
            else:
                if (v['uid'],v['gid'])!=(r['uid'],r['gid']):raise ValueError('changing numeric account identifiers unsupported')
                run('usermod','-d',r['home'],'-s',r['shell'],'-c',r['gecos'],r['name'])
            primary=grp.getgrgid(r['gid']).gr_name
            run('usermod','-G',','.join(g for g in r['groups'] if g!=primary),r['name'])
        elif t in ('privilege','login-key') and r.get('managed'):
            atomic(r['path'],r['text'],r['mode'],r['uid'],r['gid'])
        elif t=='password-login':
            atomic('/etc/ssh/sshd_config.d/00-stand.conf','PasswordAuthentication no\nKbdInteractiveAuthentication no\nPermitRootLogin prohibit-password\n')
        elif t=='wifi':
            atomic(profile_path(r),wifi_text(r),0o600);run('nmcli','connection','load',profile_path(r))
            if r['state']=='connected':run('nmcli','--wait','30','connection','up','uuid',r['uuid'])
        elif t=='bluetooth':
            if r['state']=='prepared':atomic(bt_path(r),bt_text(r),0o600)
            else:
                run('/usr/bin/bluetoothctl','--timeout','30','pair',r['address'])
                run('/usr/bin/bluetoothctl','trust' if r['trusted'] else 'untrust',r['address'])
        elif t in ('service','timer') and r.get('managed'):
            atomic('/etc/systemd/system/'+r['unit'],r['unit_text'])
    # A single netlink batch replaces this prototype's owned table; other tables are not overwritten.
    rules=[r for r in rows if r['type']=='rule' and r.get('backend','nft')=='nft']
    exists=run('nft','list','table','inet','stand',check=False).returncode==0
    nft=('delete table inet stand\n' if exists else '')+'add table inet stand\nadd chain inet stand input { type filter hook input priority 0; policy accept; }\n'
    nft+=''.join('add rule inet stand input '+r['expression']+' comment "'+r['id']+'"\n' for r in rules)
    run('nft','-f','-',input=nft)
    run('systemctl','daemon-reload')
    if POLICY:
        result=POLICY.refresh_trust(rows,d)
        atomic(ROOT/'policy-status.json',canonical(result)+'\n')
    for r in rows:
        if r['type'] in ('service','timer') and r.get('managed'):
            run('systemctl','enable' if r['enabled']=='enabled' else 'disable',r['unit'])
            if r.get('active'):run('systemctl','start',r['unit'])
            else:run('systemctl','stop',r['unit'])
    if run('systemctl','is-active','--quiet','ssh',check=False).returncode==0:
        run('systemctl','reload','ssh')
    return killed
def fsync_tree(d):
    for p in sorted(d.rglob('*')):
        if p.is_file():
            with p.open('rb') as f:os.fsync(f.fileno())
    for p in sorted([d]+[p for p in d.rglob('*') if p.is_dir()],reverse=True):syncdir(p)
def freeze(source):
    rows=load(source)
    names=['machine.jsonl']+[r['files_manifest'] for r in rows if 'files_manifest' in r]
    content={n:(pathlib.Path(source)/n).read_bytes() for n in sorted(set(names))}
    ident=digest(b''.join(n.encode()+b'\0'+v for n,v in content.items()))
    target=ROOT/'generations'/ident
    if not target.exists():
        tmp=ROOT/'generations'/('.stage-'+str(os.getpid()));tmp.mkdir(mode=0o700)
        for n,b in content.items():atomic(tmp/n,b,0o444)
        fsync_tree(tmp);os.chmod(tmp,0o755);os.replace(tmp,target);syncdir(target.parent)
    return target,load(target),ident
def select(target):
    tmp=ROOT/'current.new';tmp.unlink(missing_ok=True);tmp.symlink_to('generations/'+target.name)
    os.replace(tmp,CURRENT);syncdir(ROOT)
def apply(source):
    ROOT.mkdir(exist_ok=True);(ROOT/'generations').mkdir(exist_ok=True)
    with transaction():
        olddir=current_dir() if CURRENT.exists() else None;old=load(olddir) if olddir else []
        try:
            target,rows,ident=freeze(source)
            factory={r['id']:r for r in load('/etc/stand/factory')}
            new={r['id']:r for r in rows}
            for ident0,r in factory.items():
                if new.get(ident0)!=r:raise ValueError('factory line change/removal unsupported: '+ident0)
            for r in rows:
                if r['type']=='port' and r['id'] not in factory:raise ValueError('standalone listener creation unsupported')
        except Exception as e:
            print('FAILED preparation: '+str(e),flush=True);return 1
        atomic(ROOT/'pending.json',canonical({'previous':olddir.name if olddir else None,'candidate':ident})+'\n')
        try:
            killed=activate(rows,target,old,olddir)
            result=verify(target,False)
            failures=[r['id'] for r in result if not r['ok']]
            if failures:raise RuntimeError('readback mismatch: '+','.join(failures))
            # The durable local report is the completion report. stdout forwards this exact record.
            report={'status':'SUCCESS','declaration':ident,'time_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'terminated':killed}
            select(target)
            atomic(ROOT/'last-success.json',canonical(report)+'\n')
            (ROOT/'pending.json').unlink();syncdir(ROOT);os.sync()
            print('SUCCESS '+ident,flush=True);return 0
        except Exception as e:
            if olddir:
                try:
                    activate(old,olddir,rows,target)
                    bad=[r['id'] for r in verify(olddir,False) if not r['ok']]
                    if bad:raise RuntimeError('rollback mismatches '+','.join(bad))
                    select(olddir);(ROOT/'pending.json').unlink(missing_ok=True);syncdir(ROOT)
                    print('FAILED restored previous declaration: '+str(e),flush=True)
                except Exception as rollback:
                    print('FAILED rollback incomplete: '+str(e)+'; '+str(rollback),flush=True)
            else:print('FAILED initial application: '+str(e),flush=True)
            return 1
def replay_unlocked():
    d=current_dir();rows=load(d)
    pending=ROOT/'pending.json'
    if pending.exists():
        item=json.loads(pending.read_text())
        if item['previous']:
            d=ROOT/'generations'/item['previous'];rows=load(d);select(d)
        # An incomplete live activation is explicitly not proven fully recoverable.
    activate(rows,d,rows,d)
    result=verify(d,False);bad=[r['id'] for r in result if not r['ok']]
    if bad:raise RuntimeError('boot readback mismatch: '+','.join(bad))
    pending.unlink(missing_ok=True);syncdir(ROOT)
    print('REPLAY '+d.name,flush=True)
def snapshot(path):
    value=verify(emit=False)
    if path=='-':print(canonical(value))
    else:atomic(path,canonical(value)+'\n')
    return 0 if all(x['ok'] for x in value) else 1
def compare(a,b):
    left={r['id']:r for r in json.loads(pathlib.Path(a).read_text())};right={r['id']:r for r in json.loads(pathlib.Path(b).read_text())};bad=False
    for ident in sorted(set(left)|set(right)):
        same=left.get(ident)==right.get(ident);bad|=not same
        print(canonical({'id':ident,'equal':same,'left':left.get(ident),'right':right.get(ident)}))
    return int(bad)
def candidate_edit_unlocked(add=None,remove=None):
    d=current_dir();rows=load(d)
    if add:
        rows=[r for r in rows if r['id']!=add['id']]+[add]
    if remove:rows=[r for r in rows if r['id']!=remove]
    with tempfile.TemporaryDirectory(prefix='edit-',dir=ROOT) as td:
        for p in d.iterdir():shutil.copyfile(p,pathlib.Path(td)/p.name)
        atomic(pathlib.Path(td)/'machine.jsonl',''.join(canonical(r)+'\n' for r in rows))
        return apply(td)
LOCK_DEPTH=0
@contextlib.contextmanager
def transaction():
    global LOCK_DEPTH
    if LOCK_DEPTH:
        yield
        return
    with (ROOT/'apply.lock').open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise RuntimeError('REFUSED application in progress')
        LOCK_DEPTH=1
        try:yield
        finally:LOCK_DEPTH=0

def candidate_edit(add=None,remove=None):
    with transaction():return candidate_edit_unlocked(add,remove)
def replay():
    with transaction():return replay_unlocked()

def frontend(name,args):
    # Only these finite operations are supported. Every other option refuses identically under sudo.
    if name in ('stand-pkg','apt','apt-get','pip','pip3','npm','flatpak','podman'):
        if len(args)==2 and args[0] in ('install','update') and name in ('stand-pkg','apt','apt-get'):
            r=json.loads(pathlib.Path(args[1]).read_text())
            if r['type'] not in ('program','code'):raise ValueError('artifact program/code line required')
            return candidate_edit(add=r)
        if len(args)==2 and args[0]=='remove':return candidate_edit(remove=args[1])
    if name=='stand-line' and len(args)==2:
        if args[0]=='add':return candidate_edit(add=json.loads(pathlib.Path(args[1]).read_text()))
        if args[0]=='remove':return candidate_edit(remove=args[1])
    print('REFUSED '+name+': use stand-line add LINE.json or a supported pinned artifact operation',flush=True);return 64
def main():
    global POLICY
    import noexec as POLICY
    name=pathlib.Path(sys.argv[0]).name;args=sys.argv[1:]
    if name=='stand-compare' and len(args)==2 and args[0]!='--snapshot':return compare(*args)
    if os.geteuid()!=0:
        # Explicit privileged dispatch; authorization is the declared sudo line.
        os.execv('/usr/bin/sudo',['sudo','-n','/usr/local/bin/'+name]+args)
    # All privileged entry points acquire one nonblocking lock, including reads.
    with transaction():return dispatch(name,args)
def dispatch(name,args):
    if name=='stand-verify':return int(any(not r['ok'] for r in verify()))
    if name=='stand-compare' and args[:1]==['--snapshot']:
        if len(args)!=2:raise ValueError('snapshot path required')
        if os.environ.get('SUDO_USER') and args[1]!='-':raise ValueError('privileged snapshot writes refused; use --snapshot -')
        return snapshot(args[1])
    if name=='stand-apply' and len(args)==1:return apply(args[0])
    if name=='stand-replay':replay();return 0
    return frontend(name,args)
if __name__=='__main__':
    try:sys.exit(main())
    except Exception as e:print('FAILED '+str(e),file=sys.stderr);sys.exit(1)

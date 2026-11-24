#!/usr/bin/python3 -I
"""Conservative P1 census. Unknown semantics never imply declaration coverage."""
import collections, grp, hashlib, itertools, json, os, pathlib, pwd, shutil, stat, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import stand

# Kernel interfaces are inspected separately, not read recursively as ordinary files.
VIRTUAL = ('/proc', '/sys', '/dev')

def inventory(d=None, emit=True):
    d = pathlib.Path(d) if d else stand.current_dir()
    rows = stand.load(d, guarded=False)
    result = []
    def add(kind, identity, state, lines=(), status=None, **extra):
        item = dict(kind=kind, object=identity, status=status or ('covered' if lines else 'unrecorded'), lines=sorted(set(lines)), observed=state, **extra)
        result.append(item)
        if emit: print(json.dumps(item, sort_keys=True), flush=True)
    def command(argv, kind):
        try:
            p = subprocess.run(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30,
                               env={'PATH':'/usr/sbin:/usr/bin:/sbin:/bin','LC_ALL':'C','LANG':'C'})
            if p.returncode: add('scan-error', kind, {'returncode':p.returncode,'stderr_sha256':stand.sha_text(p.stderr)}, status='unknown'); return ''
            return p.stdout
        except (OSError, subprocess.TimeoutExpired) as e:
            add('scan-error', kind, str(e), status='unknown'); return ''
    fileclaims = collections.defaultdict(list)
    for r in rows:
        if r['type'] in ('base','program','code'):
            for f in stand.manifest(r,d): fileclaims[f['path']].append((r['id'],stand.desired_file(f)))
        if r['type'] in ('privilege','login-key'):
            fileclaims[r['path']].append((r['id'],dict(path=r['path'], kind='file',sha256=stand.sha_text(r['text']),mode=r['mode'],uid=r['uid'],gid=r['gid'])))
    def classify(path, mode):
        p=path.lower()
        if '/systemd/' in p and p.endswith(('.service','.timer','.socket','.path')): return 'unit-file'
        if '/cron' in p or '/atjobs/' in p: return 'scheduled-job'
        if 'authorized_keys' in p or 'authorized_principals' in p: return 'login-key'
        if '/sudoers' in p or '/polkit-1/' in p: return 'privilege'
        if '/system-connections/' in p or '/wpa_supplicant/' in p or '/iwd/' in p: return 'saved-network'
        if '/bluetooth/' in p and p.endswith('/info'): return 'device-profile'
        if p.startswith('/boot/') or p.startswith('/etc/default/grub') or '/loader/entries/' in p: return 'boot-file'
        if '/nftables' in p or '/iptables' in p or '/apparmor' in p or '/selinux/' in p: return 'rule-file'
        if mode & 0o6000: return 'privilege-file'
        # Positive signatures identify candidates only, never exempt other bytes.
        return 'file'
    def scan_error(e): add('scan-error', getattr(e,'filename','filesystem'),str(e),status='unknown')
    trees=itertools.chain(os.walk('/',followlinks=False,onerror=scan_error),
                          os.walk('/dev/shm',followlinks=False,onerror=scan_error))
    for root, dirs, names in trees:
        dirs[:] = sorted(x for x in dirs if os.path.join(root,x) not in VIRTUAL)
        try:
            ds=os.stat(root,follow_symlinks=False)
            directory_value=dict(path=root,kind='directory',mode=stat.S_IMODE(ds.st_mode),uid=ds.st_uid,gid=ds.st_gid)
            ids=[r['id'] for r in rows if r['type']=='rule' and r.get('backend')=='dac' and directory_value in r.get('paths',[])]
            add('directory-rights',root,directory_value,ids,status='covered' if ids else 'unknown')
            for attr in os.listxattr(root,follow_symlinks=False):
                if attr in ('system.posix_acl_access','system.posix_acl_default'):
                    add('rights-xattr',root+':'+attr,os.getxattr(root,attr,follow_symlinks=False).hex())
        except OSError as e:scan_error(e)
        for name in sorted(names + [x for x in dirs if os.path.islink(os.path.join(root,x))]):
            path=os.path.join(root,name)
            try:
                s=os.lstat(path)
                if stat.S_ISSOCK(s.st_mode):
                    add('unix-socket',path,dict(uid=s.st_uid,gid=s.st_gid,mode=stat.S_IMODE(s.st_mode)),status='unknown',reason='May provide an agent or other authority; socket name does not classify contents.')
                if not (stat.S_ISREG(s.st_mode) or stat.S_ISLNK(s.st_mode)):continue
                kind=classify(path,s.st_mode)
                claims=fileclaims.get(path,[])
                if claims:
                    value=stand.filevalue(path)
                    ids=[i for i,want in claims if want==value]
                    add(kind,path,value,ids,status='covered' if ids else 'mismatch')
                else:
                    value=dict(mode=stat.S_IMODE(s.st_mode),uid=s.st_uid,gid=s.st_gid,size=s.st_size)
                    if stat.S_ISLNK(s.st_mode):value['target']=os.readlink(path)
                    elif s.st_size:
                        with open(path,'rb') as f: head=f.read(128)
                        if head.startswith(b'\x7fELF'): kind='program'
                        elif head.startswith(b'#!'):kind='code'
                    add(kind,path,value,status='unknown' if kind in ('file','program','code') else 'unrecorded',in_force='not established from file signature')
                try:
                    attrs=os.listxattr(path,follow_symlinks=False)
                    for attr in attrs:
                        if attr in ('security.capability','system.posix_acl_access','system.posix_acl_default'):
                            add('rights-xattr',path+':'+attr,os.getxattr(path,attr,follow_symlinks=False).hex())
                except OSError as e: add('scan-error',path+':xattr',str(e),status='unknown')
            except (OSError,ValueError) as e:scan_error(e)
    for p in pwd.getpwall():
        val=stand.account_value(p.pw_name)
        claims=[r for r in rows if r['type']=='account' and r['name']==p.pw_name]
        add('account',p.pw_name,val,[r['id'] for r in claims if stand.expected_account(r)==val],status=None if not claims or any(stand.expected_account(r)==val for r in claims) else 'mismatch')
    for g in grp.getgrall():
        # Account supplementary memberships do not declare existence of an independent group.
        add('group',g.gr_name,dict(gid=g.gr_gid,members=sorted(g.gr_mem)),status='unknown')
    # Read effective policy without running any granted command or exposing key blobs.
    sudo=shutil.which('sudo',path='/usr/bin:/usr/sbin')
    sshd=shutil.which('sshd',path='/usr/sbin:/usr/bin')
    for account in pwd.getpwall():
        groups=stand.account_value(account.pw_name).get('groups',[])
        if sudo:
            policy=command([sudo,'-n','-ll','-U',account.pw_name],'sudo:'+account.pw_name)
            add('effective-privilege',account.pw_name,{'groups':groups,'sudo_listing_sha256':stand.sha_text(policy),'sudo_listing_bytes':len(policy),'sudo_policy_lines':policy.splitlines()},status='unknown',reason='Effective sudo policy read; finite schema does not independently declare its normalized per-account result.')
        if sshd:
            config=command([sshd,'-T','-C','user='+account.pw_name+',addr=127.0.0.1,host=localhost,laddr=127.0.0.1,lport=22'],'sshd:'+account.pw_name)
            cfg=dict(line.split(None,1) for line in config.splitlines() if len(line.split(None,1))==2)
            for key in ('authorizedkeysfile','authorizedprincipalsfile','trustedusercakeys'):
                for value in cfg.get(key,'').split():
                    if value=='none':continue
                    path=value.replace('%%','\x00').replace('%h',account.pw_dir).replace('%u',account.pw_name).replace('%U',str(account.pw_uid)).replace('\x00','%')
                    if not path.startswith('/'):path=str(pathlib.Path(account.pw_dir)/path)
                    try:
                        state=stand.filevalue(path)
                        ids=[i for i,want in fileclaims.get(path,[]) if want==state]
                        add('configured-login-key',account.pw_name+':'+path,state,ids,status='covered' if ids else 'unknown' if state.get('missing') else 'unrecorded',configuration=key)
                    except OSError as e:scan_error(e)
            add('ssh-login-policy',account.pw_name,{key:cfg.get(key) for key in ('passwordauthentication','kbdinteractiveauthentication','pubkeyauthentication','permitrootlogin')},status='unknown',reason='Loopback Match context only; other addresses, alternate daemon arguments and key commands remain unresolved.')
            for key in ('authorizedkeyscommand','authorizedprincipalscommand'):
                if cfg.get(key,'none')!='none':add('login-key-command',account.pw_name+':'+key,{'command_sha256':stand.sha_text(cfg[key])},status='unknown')
    for directory in ('/etc/polkit-1','/usr/share/polkit-1','/etc/cron.d','/etc/cron.daily','/etc/cron.hourly','/etc/cron.weekly','/etc/cron.monthly','/var/spool/cron','/var/spool/at','/etc/sv','/etc/runit','/etc/s6','/etc/init.d'):
        p=pathlib.Path(directory)
        add('manager-configuration',directory,{'exists':p.exists()},status='unknown',reason='Configuration entries are enumerated in the file census; effective alternate-manager semantics are not inferred.')
    if shutil.which('atq',path='/usr/bin:/usr/sbin'):
        queue=command(['/usr/bin/atq'],'at-queue')
        add('scheduled-queue','at',{'listing_sha256':stand.sha_text(queue),'entries':len(queue.splitlines())},status='unknown')
    try:
        for line in pathlib.Path('/proc/keys').read_text().splitlines():
            parts=line.split()
            if len(parts)>=8:add('kernel-key',parts[0],{'flags':parts[1],'permissions':parts[4],'uid':parts[5],'gid':parts[6],'type':parts[7]},status='unknown')
        add('kernel-key-visibility','current-credentials',{},status='unknown',reason='Only keys visible to current credentials; key descriptions and payloads are not printed.')
    except OSError as e:scan_error(e)
    try:
        for line in pathlib.Path('/proc/self/mountinfo').read_text().splitlines():
            parts=line.split();separator=parts.index('-')
            add('mount',parts[0],{'parent':parts[1],'root':parts[3],'mountpoint':parts[4],'fstype':parts[separator+1],'options_sha256':stand.sha_text(parts[5]+' '+parts[-1])},status='unknown')
    except (OSError,ValueError) as e:scan_error(e)
    managers=[([], 'system'),(['--global'],'user-global')]
    for p in pathlib.Path('/run/user').glob('*'):
        if p.name.isdigit() and (p/'bus').exists():
            try: account=pwd.getpwuid(int(p.name)).pw_name
            except KeyError:account=p.name
            managers.append((['--user','--machine='+account+'@.host'],'user:'+p.name))
    for args,scope in managers:
        for operation in ('list-unit-files','list-units'):
            argv=['/usr/bin/systemctl']+args+[operation,'--type=service,timer,socket,path','--no-legend','--no-pager','--plain']
            if operation=='list-units': argv+=['--all']
            if scope=='user-global' and operation=='list-units':continue
            for line in command(argv,scope+':'+operation).splitlines():
                bits=line.split()
                if not bits:continue
                unit=bits[0]
                claims=[r for r in rows if r['type'] in ('service','timer','socket') and r['unit']==unit and r.get('scope','system')==scope]
                matching=[]
                for r in claims:
                    try:
                        if stand.observe(r,d)[0]:matching.append(r['id'])
                    except Exception:pass
                add('manager-unit',scope+':'+unit,{'listing':line,'operation':operation},matching,status='covered' if matching else 'mismatch' if claims else 'unrecorded')
    for protocol in ('tcp','udp'):
        for local in stand.port_values(protocol):
            ids=[r['id'] for r in rows if r['type']=='port' and r['protocol']==protocol and r['local']==local and r.get('listening') is True]
            add('port',protocol+':'+local,{'listening':True},ids)
    nft=command(['/usr/sbin/nft','-j','list','ruleset'],'nft')
    if nft:
        for item in json.loads(nft).get('nftables',[]):
            for kind,value in item.items():
                if kind=='metainfo':continue
                normalized={k:v for k,v in value.items() if k not in ('handle','index')}
                ids=[]
                for r in rows:
                    if r['type']!='rule':continue
                    if kind=='chain' and r.get('backend')=='nft-chain' and r.get('chain')==normalized:ids.append(r['id'])
                    if kind=='rule' and value.get('comment')==r['id']:
                        try:
                            if stand.observe(r,d)[0]:ids.append(r['id'])
                        except Exception:pass
                add('firewall-'+kind,':'.join(str(value.get(k,'')) for k in ('family','table','name','handle')),normalized,ids)
    for line in command(['/usr/bin/nmcli','-t','-f','UUID,TYPE','connection','show'],'networks').splitlines():
        uuid,_,kind=line.partition(':')
        ids=[]
        for r in rows:
            if r['type']=='wifi' and r.get('uuid')==uuid:
                try:
                    if stand.observe(r,d)[0]:ids.append(r['id'])
                except Exception:pass
        add('saved-network',uuid,{'type':kind},ids)
    namespaces=set()
    for proc in pathlib.Path('/proc').iterdir():
        if not proc.name.isdigit():continue
        try:
            exe=os.readlink(proc/'exe'); ns=tuple(os.readlink(proc/'ns'/n) for n in ('mnt','net','pid'))
            namespaces.add(ns)
            path=exe.removesuffix(' (deleted)'); ids=[]
            # /proc/PID/exe is a magic link: hash its target content, never its pathname alone.
            if fileclaims.get(path):
                actual=stand.sha(proc/'exe')
                ids=[i for i,w in fileclaims[path] if w.get('sha256')==actual]
            add('process',proc.name,{'exe':exe,'namespaces':ns},ids,in_force='running executable readback')
            credentials={}
            for entry in (proc/'status').read_text().splitlines():
                key,_,value=entry.partition(':')
                if key in ('Uid','Gid','Groups','CapInh','CapPrm','CapEff','CapBnd','CapAmb','NoNewPrivs'):
                    credentials[key]=value.strip()
            add('effective-process-rights',proc.name,credentials,status='unknown')
            try:
                for entry in (proc/'environ').read_bytes().split(b'\0'):
                    if entry.startswith(b'SSH_AUTH_SOCK='):
                        add('ssh-agent-socket',proc.name,{'path':os.fsdecode(entry.split(b'=',1)[1])},status='unknown',reason='Agent location observed; no key payload requested.')
            except OSError:pass
            for line in (proc/'maps').read_text().splitlines():
                parts=line.split(None,5)
                if len(parts)<2 or 'x' not in parts[1]:continue
                identity=proc.name+':'+parts[0]
                if len(parts)<6 or not parts[5].startswith('/'):
                    add('executable-memory',identity,{'mapping':parts[-1]},status='unknown')
                    continue
                mapped_path=parts[5]
                state={'mapping':mapped_path,'permissions':parts[1],'offset':parts[2],'device':parts[3],'inode':parts[4]}
                backing_lines=[]
                if mapped_path.endswith(' (deleted)'):
                    state['readback']='deleted backing object; pathname cannot establish declaration coverage'
                else:
                    try:
                        # map_files refers to the mapped backing object, not a replacement at its former path.
                        with open(proc/'map_files'/parts[0],'rb') as stream:
                            fs=os.fstat(stream.fileno())
                            content_hash=hashlib.sha256()
                            for block in iter(lambda:stream.read(1024*1024),b''):content_hash.update(block)
                        value={'path':mapped_path,'kind':'file','mode':stat.S_IMODE(fs.st_mode),'uid':fs.st_uid,'gid':fs.st_gid,'sha256':content_hash.hexdigest()}
                        backing_lines=[i for i,want in fileclaims.get(mapped_path,[]) if want==value]
                        state['backing_object']=value
                    except OSError as e:
                        state['readback']='mapped backing object unreadable'
                        state['errno']=e.errno
                add('executable-file-mapping',identity,state,status='unknown',backing_lines=backing_lines,reason='Exact mapped backing-file comparison when readable; private or modified resident pages are not authenticated by a backing-file hash.')
        except (OSError,ProcessLookupError):continue
    add('namespace-census','runtime',{'namespaces':sorted(namespaces)},status='unknown',reason='Separate namespace managers, detached mounts and network listeners require namespace-specific readback.')
    efivars=pathlib.Path('/sys/firmware/efi/efivars')
    if efivars.exists():
        for p in sorted(efivars.glob('Boot*')):
            try:add('boot-variable',p.name,{'sha256':stand.sha(p)})
            except OSError as e:scan_error(e)
    else:add('boot-order','external-firmware',{},status='unknown',reason='Guest cannot read the hypervisor boot selector; a declaration claim is not device readback.')
    add('semantic-coverage','unclassified',{},status='unknown',reason='File bytes and installed managers do not decide all own-rights code, custom managers, in-memory rules, firmware or semantic effects. Unknown is not an exemption or proof of coverage.')
    counts=dict(collections.Counter(x['status'] for x in result))
    summary=dict(kind='summary',complete=False,counts=counts,p1='?',scope='Observed census; unclassified objects require Section 3 evidence.')
    if emit:print(json.dumps(summary,sort_keys=True),flush=True)
    return result,summary

if __name__=='__main__':
    objects,summary=inventory(sys.argv[1] if len(sys.argv)>1 else None)
    sys.exit(1 if summary['counts'].get('unrecorded') or summary['counts'].get('mismatch') else 2)

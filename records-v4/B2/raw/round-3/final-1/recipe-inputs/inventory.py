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

def independent_census():
    """Snapshot actual objects before reading any declaration or enumerating claims."""
    import object_rules
    objects=[]
    memberships=collections.defaultdict(list)
    # Native installer metadata includes no-code and dependency-only packages.
    try:
        query=subprocess.run(['/usr/bin/dpkg-query','-W','-f=${binary:Package}\t${Version}\t${Architecture}\t${db:Status-Status}\n'],
                             text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
        if query.returncode:raise RuntimeError('dpkg-query failed')
        for line in query.stdout.splitlines():
            name,version,architecture,status=line.split('\t')
            if status!='installed':continue
            observed=dict(backend='dpkg',name=name,version=version,architecture=architecture,status=status)
            objects.append(dict(kind='package',object='dpkg:'+name,observed=observed,
                                facts=dict(package_installed=True)))
            # Reading native package membership does not use declaration file lists.
            filelist=pathlib.Path('/var/lib/dpkg/info')/(name+'.list')
            if not filelist.exists():filelist=pathlib.Path('/var/lib/dpkg/info')/(name.split(':')[0]+'.list')
            try:
                for path in filelist.read_text().splitlines(): memberships[path].append(name)
            except OSError:pass
    except (OSError,ValueError,RuntimeError,subprocess.TimeoutExpired) as exc:
        objects.append(dict(kind='scan-error',object='dpkg',observed={'error':type(exc).__name__},facts={}))
    def scan_error(exc):
        objects.append(dict(kind='scan-error',object=str(getattr(exc,'filename','filesystem')),
                            observed={'error':type(exc).__name__},facts={}))
    trees=itertools.chain(os.walk('/',followlinks=False,onerror=scan_error),
                         os.walk('/dev/shm',followlinks=False,onerror=scan_error))
    for root,dirs,names in trees:
        dirs[:]=sorted(x for x in dirs if os.path.join(root,x) not in VIRTUAL)
        for name in sorted(names+[x for x in dirs if os.path.islink(os.path.join(root,x))]):
            path=os.path.join(root,name)
            try:
                st=os.lstat(path)
                if not (stat.S_ISREG(st.st_mode) or stat.S_ISLNK(st.st_mode)):continue
                observed=stand.filevalue(path)
                facts=dict(package_installed=False,package_member=bool(memberships.get(path)))
                # dpkg lists prove membership, but do not preserve all received modes,
                # ownership and symlink targets. Checksums alone cannot prove Q1.
                objects.append(dict(kind='file',object=path,observed=observed,facts=facts,
                                    packages=memberships.get(path,[])))
            except (OSError,ValueError) as exc:scan_error(exc)
    setting_facts=dict(package_installed=False,package_member=False,executable=False,setting=True)
    for account in pwd.getpwall():
        objects.append(dict(kind='account',object='account:'+account.pw_name,
                            observed=stand.account_value(account.pw_name),facts=dict(setting_facts)))
    for group in grp.getgrall():
        objects.append(dict(kind='group',object='group:'+group.gr_name,
                            observed=dict(name=group.gr_name,gid=group.gr_gid,members=sorted(group.gr_mem)),
                            facts=dict(setting_facts)))
    # Native manager enumeration, not the list of declared units.
    try:
        listing=stand.run('systemctl','list-unit-files','--type=service,timer,socket,path',
                         '--no-legend','--no-pager','--plain',check=False)
        if listing.returncode:raise RuntimeError('service enumeration failed')
        for line in listing.stdout.splitlines():
            fields=line.split()
            if len(fields)<2 or fields[1] not in ('enabled','enabled-runtime','linked','linked-runtime'):continue
            unit=fields[0]
            state=stand.service_value({'unit':unit,'active':True})
            active=state.pop('active')
            objects.append(dict(kind='service',object='service:system:'+unit,
                                observed=state,active=active,facts=dict(setting_facts)))
    except (OSError,RuntimeError,subprocess.TimeoutExpired) as exc:
        objects.append(dict(kind='scan-error',object='system-service-manager',
                            observed={'error':type(exc).__name__},facts={}))
    # One implemented native chosen-value reader, even if its ledger is absent.
    try:
        objects.append(dict(kind='setting',object='sysctl:kernel.printk',
                            observed={'name':'kernel.printk','value':' '.join(pathlib.Path('/proc/sys/kernel/printk').read_text().split())},
                            facts={}))
    except OSError as exc:scan_error(exc)
    file_index={item['object']:item for item in objects if item['kind']=='file'}
    # Relationships are diagnostics; they do not create mandatory separate rows.
    for proc in pathlib.Path('/proc').iterdir():
        if not proc.name.isdigit():continue
        try:
            exe=os.readlink(proc/'exe')
            observed=dict(exe=exe,exe_sha256=stand.sha(proc/'exe'))
            backing=file_index.get(exe)
            if backing and backing['observed'].get('sha256')==observed['exe_sha256']:
                backing['facts'].update(executable=True,own_process=True)
            objects.append(dict(kind='process',object='process:'+proc.name,observed=observed,
                                facts=dict(runtime_only=True,creator={'path':exe,'sha256':observed['exe_sha256']})))
        except OSError:pass
    for protocol in ('tcp','udp'):
        for local in stand.port_values(protocol):
            objects.append(dict(kind='port',object=protocol+':'+local,observed={'listening':True},
                                facts={'runtime_only':True}))
    try:
        for line in pathlib.Path('/proc/self/mountinfo').read_text().splitlines():
            fields=line.split(); separator=fields.index('-')
            objects.append(dict(kind='mount',object='mount:'+fields[0],
                                observed={'mountpoint':fields[4],'fstype':fields[separator+1]},
                                facts={'runtime_only':True}))
    except (OSError,ValueError) as exc:scan_error(exc)
    return objects


def v4_inventory(d=None,emit=True):
    import object_rules
    # Snapshot phase finishes before the current declaration is even loaded.
    objects=independent_census()
    try:
        import recorded_objects
        supplements=recorded_objects.census()
    except (ImportError,AttributeError) as exc:
        recorded_objects=None
        supplements=[dict(kind='scan-error',object='provenance-reader',
                          observed={'error':type(exc).__name__},facts={})]
    index={obj['object']:obj for obj in objects}
    for extra in supplements:
        old=index.get(extra['object'])
        if old and old['observed']!=extra['observed']:
            old['fact_error']='Independent census and provenance reader disagree'
            continue
        if old:
            old['facts'].update(extra.get('facts',{}))
            old['origins']=extra.get('origins',[])
        else:
            objects.append(extra); index[extra['object']]=extra
    d=pathlib.Path(d) if d else stand.current_dir()
    rows=stand.load(d,guarded=False)
    claims=collections.defaultdict(list)
    if recorded_objects is not None:
        for key,values in recorded_objects.claims(rows,d,objects).items():claims[key].extend(values)
    # Explicit own file records match whole state, never pathname alone. These
    # claims do not manufacture missing classification/provenance facts.
    for row in rows:
        if row['type'] in ('base','program','code'):
            for value in stand.manifest(row,d):
                claims[value['path']].append(dict(line=row['id'],relation='own',
                    required=stand.desired_file(value),provenance_verified=True))
    for row in rows:
        key=None;required=None
        if row['type']=='account':
            key='account:'+row['name'];required=stand.expected_account(row)
        elif row['type']=='group':
            key='group:'+row['name'];required={k:row[k] for k in ('name','gid','members')}
        elif row['type'] in ('service','timer','socket'):
            key='service:'+row.get('scope','system')+':'+row['unit']
            required={k:row[k] for k in ('unit','enabled','unit_sha256')}
            if 'active' in row and index.get(key,{}).get('active')!=row['active']:continue
        if key is not None:
            claims[key].append(dict(line=row['id'],relation='own',required=required,provenance_verified=True))
    result=[]
    for obj in objects:
        classification=object_rules.classify(obj['facts'])
        if obj.get('fact_error'):
            classification=dict(category='FACT_UNKNOWN',required=None,question=None,missing=[obj['fact_error']])
        decision=object_rules.coverage(classification,obj['observed'],claims.get(obj['object'],[]))
        item=dict(obj,classification=classification,**decision)
        if classification['category']=='runtime':
            creator=obj['facts'].get('creator')
            item['creator_coverage']='FACT_UNKNOWN'
            if creator and creator.get('path') in index:
                parent=index[creator['path']]
                if parent['observed'].get('sha256')==creator.get('sha256'):
                    parent_class=object_rules.classify(parent['facts'])
                    item['creator_coverage']=object_rules.coverage(parent_class,parent['observed'],claims.get(parent['object'],[]))
        result.append(item)
        if emit:print(json.dumps(item,sort_keys=True),flush=True)
    counts=dict(collections.Counter(item['status'] for item in result))
    summary=dict(kind='summary',version=4,complete=not counts.get('FACT_UNKNOWN'),counts=counts,
                 hypothesis_outcome='?',
                 observed_coverage='failed' if counts.get('unrecorded') or counts.get('mismatch') else 'unknown' if counts.get('FACT_UNKNOWN') else 'matched',
                 scope='Independent census and finite provenance readers; runtime rows are diagnostics')
    if emit:print(json.dumps(summary,sort_keys=True),flush=True)
    return result,summary


if __name__=='__main__':
    args=sys.argv[1:]
    v4='--v4' in args
    args=[arg for arg in args if arg!='--v4']
    objects,summary=(v4_inventory if v4 else inventory)(args[0] if args else None)
    sys.exit(1 if summary['counts'].get('unrecorded') or summary['counts'].get('mismatch') else 2 if not summary.get('complete') else 0)

"""Declaration-derived ordinary launch, executable mapping and read-closure policy."""
import hashlib,json,os,pathlib,re,shlex,signal,stat,subprocess,time,shutil
P=pathlib.Path
DATA={'/usr/bin/dd':'document','/usr/bin/red':'editor','/usr/bin/w3m':'w3m','/usr/bin/cat':'-','/usr/bin/cp':'-','/usr/bin/mkdir':'-','/usr/bin/curl':'-'}
CHANNEL_PROFILES=('stand-format-parser','stand-build')

def key(path):return 'stand-run-'+hashlib.sha256(path.encode()).hexdigest()[:20]
def safe(path):
    if not re.fullmatch(r'/[a-zA-Z0-9_./:+,@=-]+',path):raise ValueError('unsupported policy path '+path)
    return path

def immutable(path):
    p=P(path)
    try:
        for q in [p,*p.parents]:
            s=q.stat()
            if s.st_uid!=0 or s.st_mode&0o022:return False
            if (q==p and not s.st_mode&0o004) or (q!=p and not s.st_mode&0o001):return False
        return True
    except OSError:return False

def inputs(rows,d):
    from stand import manifest
    return {f['path']:f for r in rows if r['type'] in ('base','program','code') for f in manifest(r,d) if f['kind']=='file'}

def generate(rows,d):
    files=inputs(rows,d);read=[];mapped=[];launch=[];profiles=[]
    for path,f in sorted(files.items()):
        if not immutable(path):continue
        # AppArmor paths must be quoted. Literal names containing policy syntax are refused for launch;
        # non-code documentation with such names is not part of the interpreter's closure.
        if not re.fullmatch(r'/[a-zA-Z0-9_./:+,@=-]+',path):continue
        read.append(path)
        with open(path,'rb') as s:magic=s.read(4)
        if magic==b'\x7fELF':mapped.append(path)
    admitted={}
    def add(name,binary,script=None,mode='sealed',extra='-'):
        spec=(binary,script,mode,extra)
        if name in admitted:
            if admitted[name]!=spec:raise ValueError('conflicting launch contributions')
            return
        admitted[name]=spec
        
        if name.startswith('service:'):
            if not re.fullmatch(r'service:[a-zA-Z0-9_.@-]+',name):raise ValueError('invalid service key')
        else:safe(name)
        if script:safe(script)
        if any(c in extra for c in '\t\r\n'):raise ValueError('invalid launch arguments')
        binary=str(P(binary).resolve());safe(binary)
        if binary not in files or not immutable(binary):raise ValueError('interpreter/executable outside recorded immutable closure')
        if script and (script not in files or not immutable(script)):raise ValueError('script outside recorded immutable closure')
        profile=key(name)
        launch.append('\t'.join([name,mode,profile,binary,files[binary]['sha256'],script or '-',files[script]['sha256'] if script else '-',extra]))
        common=['  #include <abstractions/stand-map>',f'  "{binary}" ix,','  /dev/null rw,','  /dev/urandom r,','  /dev/random r,','  /proc/*/attr/current r,','  signal (receive) peer=unconfined,','  signal (send,receive) peer='+profile+',','  signal (send) peer=stand-session,']
        if mode in ('container','application'):
            common+=[f'  "{binary.removeprefix(extra)}" rixm,']
        if mode!='data':common+=['  /** r,','  capability sys_chroot,','  capability setuid,','  capability setgid,','  network unix stream,']
        else:common+=['  /** r,','  /home/stand/ rw,','  /home/stand/** rwk,','  /tmp/ rw,','  /tmp/** rwk,','  network inet stream,','  network inet6 stream,','  network inet dgram,','  network inet6 dgram,','  network unix stream,']
        if name.startswith('service:'):common+=['  /usr/local/lib/stand/service-launch ix,']
        # No shell/helper exec, ptrace, capabilities, mount or child profile changes.
        profiles.append('profile '+profile+' flags=(attach_disconnected,chroot_relative) {\n'+'\n'.join(common)+'\n}\n')
    for path,extra in DATA.items():
        binary=str(P('/usr/bin/ed' if extra=='editor' else path).resolve())
        if binary in files:add(path,binary,mode='data',extra=extra)
    for r in rows:
        if r['type'] not in ('program','code') or not r.get('managed'):continue
        from stand import manifest
        if r.get('channel') in ('oci','flatpak','appimage'):
            add(r['application_entry'],r['application_entry'],mode='container' if r['channel']=='oci' else 'application',extra='/opt/stand/pkgs/'+r['id'])
            continue
        for f in manifest(r,d):
            if f['mode']&0o111 and f['path'] in mapped:add(f['path'],f['path'],extra='|'.join(r.get('native_arguments',{}).get(f['path'],[])) or '-')
        for ep in r.get('entrypoints',[]):add(ep['path'],ep['interpreter'],ep['path'])
    for r in rows:
        if r['type']=='service' and r.get('managed'):
            import configparser
            c=configparser.ConfigParser(interpolation=None);c.read_string(r['unit_text']);args=shlex.split(c['Service']['ExecStart'])
            # Services use the same boundary; arguments originate in their declaration line.
            add('service:'+r['unit'],args[0],extra='|'.join(args[1:]) or '-')
    dirs={str(p) for x in read for p in P(x).parents if str(p).startswith(('/usr/','/opt/stand/pkgs/')) and immutable(p)}
    closure='\n'.join(sorted(set(read)|dirs|{'/dev/null'}))+'\n'
    mapping='\n'.join('"'+p+'" m,' for p in mapped)+'\n'
    launcher='''profile stand-session /usr/local/bin/stand-session flags=(attach_disconnected) {
  #include <abstractions/stand-map>
  /** r,
  /var/lib/stand/apply.lock rk,
  network unix stream,
  /dev/tty rw,
  /dev/null rw,
  /proc/*/attr/current w,
  /usr/bin/sudo Ux,
  /usr/local/bin/stand-session ix,
  capability sys_chroot,
  capability setuid,
  capability setgid,
  signal (receive) peer=unconfined,
  signal (send,receive) peer=stand-session,
  signal (receive) peer=stand-run-*,
  change_profile -> stand-run-*,
}
'''
    return {'read-closure':closure,'launch.tsv':'\n'.join(launch)+'\n','stand-map.rules':mapping,'stand-profiles':launcher+'\n'.join(profiles)}

def snapshot_spec(rows,d,generated):
    from stand import manifest
    files=inputs(rows,d)
    entries={p:{'kind':'file','sha256':files[p]['sha256'],'mode':files[p]['mode'],'gid':files[p]['gid']} for p in generated['read-closure'].splitlines() if p in files}
    for row in rows:
        if row['type'] not in ('base','program','code'):continue
        for f in manifest(row,d):
            p=f['path']
            if f['kind']=='symlink' and re.fullmatch(r'/[a-zA-Z0-9_./:+,@=-]+',p):
                entries[p]={'kind':'symlink','target':f['target']}
    entries['/etc/stand/read-closure']={'kind':'generated','text':generated['read-closure'],'mode':0o644}
    entries['/dev/null']={'kind':'null','mode':0o666}
    # Assembly never traverses a symlink. Canonical file names are represented;
    # directory aliases are created last and resolve only within the new root.
    for p in list(entries):
        if any(str(q) in entries and entries[str(q)]['kind']=='symlink' for q in P(p).parents):del entries[p]
    dirs={str(q) for p in entries for q in P(p).parents}
    for p in dirs:entries[p]={'kind':'directory','mode':0o755}
    return entries

def input_root(rows,d,generated):
    """Atomically replace the entire immutable filesystem view; retain no removed names."""
    from stand import atomic
    import tempfile
    spec=snapshot_spec(rows,d,generated)
    root=P('/var/lib/stand/code-root');state=P('/var/lib/stand/code-root.json')
    if state.exists() and root.exists() and json.loads(state.read_text())==spec:return
    stage=P(tempfile.mkdtemp(prefix='code-root-',dir='/var/lib/stand'));os.chmod(stage,0o755)
    try:
        for p,v in sorted(spec.items(),key=lambda x:len(P(x[0]).parts)):
            if v['kind']=='directory':(stage/p.lstrip('/')).mkdir(mode=0o755,exist_ok=True)
        for p,v in spec.items():
            target=stage/p.lstrip('/');kind=v['kind']
            if kind=='file':
                try:os.link(p,target)
                except OSError:shutil.copy2(p,target)
            elif kind=='generated':atomic(target,v['text'])
            elif kind=='null':os.mknod(target,stat.S_IFCHR|0o666,os.makedev(1,3));os.chmod(target,0o666)
        for p,v in spec.items():
            if v['kind']=='symlink':(stage/p.lstrip('/')).symlink_to(v['target'])
        previous=P('/var/lib/stand/code-root-previous')
        if root.exists():os.replace(root,previous)
        os.replace(stage,root)
        if previous.exists():shutil.rmtree(previous)
        atomic(state,json.dumps(spec,sort_keys=True))
    finally:
        if stage.exists():shutil.rmtree(stage)

def verify_root(rows,d,generated):
    spec=snapshot_spec(rows,d,generated);root=P('/var/lib/stand/code-root');bad=[];seen={'/'}
    for directory,dirs,files in os.walk(root,followlinks=False):
        for name in dirs+files:seen.add('/'+str((P(directory)/name).relative_to(root)))
    if seen!=set(spec):bad.append('exact input-root membership')
    for path,v in spec.items():
        p=root/path.lstrip('/')
        try:
            st=p.lstat();kind=v['kind']
            if st.st_uid!=0 or st.st_gid!=v.get('gid',0):raise ValueError('ownership')
            if kind=='symlink':
                if not p.is_symlink() or os.readlink(p)!=v['target']:raise ValueError('symlink')
            else:
                if stat.S_IMODE(st.st_mode)!=v['mode']:raise ValueError('mode')
                if kind=='directory' and not stat.S_ISDIR(st.st_mode):raise ValueError('directory')
                if kind in ('file','generated'):
                    if not stat.S_ISREG(st.st_mode):raise ValueError('file type')
                    # Linked immutable inodes were already checked by file observers;
                    # copy fallback and generated files require content comparison.
                    if kind=='file':
                        source=P(path).stat()
                        if (st.st_ino,st.st_dev)!=(source.st_ino,source.st_dev) and hashlib.sha256(p.read_bytes()).hexdigest()!=v['sha256']:raise ValueError('hash')
                    elif p.read_text()!=v['text']:raise ValueError('generated content')
                if kind=='null' and (not stat.S_ISCHR(st.st_mode) or st.st_rdev!=os.makedev(1,3)):raise ValueError('null device')
        except (OSError,ValueError) as error:bad.append('input-root '+path+': '+str(error))
    return bad

def refresh_trust(rows,d):
    from stand import atomic
    import noexec
    state=noexec.refresh_trust(rows,d)
    generated=generate(rows,d)
    input_root(rows,d,generated)
    for name,text in generated.items():
        p=P('/etc/apparmor.d/abstractions')/name.removesuffix('.rules') if name in ('stand-map.rules','stand-read.rules') else P('/etc/stand')/name
        atomic(p,text)
    parsed=subprocess.run(['/usr/sbin/apparmor_parser','-r','-T','/etc/stand/stand-profiles'],capture_output=True,text=True)
    if parsed.returncode:raise RuntimeError('policy load: '+parsed.stderr.strip())
    for name in CHANNEL_PROFILES:
        parsed=subprocess.run(['/usr/sbin/apparmor_parser','-r','-T','/etc/apparmor.d/'+name],capture_output=True,text=True)
        if parsed.returncode:raise RuntimeError('channel policy load: '+parsed.stderr.strip())
    wanted={x.split('\t')[2] for x in generated['launch.tsv'].splitlines()}
    for line in P('/sys/kernel/security/apparmor/profiles').read_text().splitlines():
        old=line.split(' ')[0]
        if old.startswith('stand-run-') and old not in wanted:
            with open('/sys/kernel/security/apparmor/.remove','wb') as f:f.write(old.encode()+b'\0')
    for r in rows:
        if r['type']=='service' and r.get('managed'):
            atomic(P('/etc/systemd/system')/(r['unit']+'.d')/'50-code-boundary.conf',service_dropin(r))
    state.update(mechanism='AppArmor exec/map + sealed Landlock read closure + inherited seccomp',profiles=len(generated['launch.tsv'].splitlines()))
    return state

def service_dropin(row):return '[Service]\nUser=root\nNoNewPrivileges=no\nExecStart=\nExecStart=/usr/local/lib/stand/service-launch --service '+row['unit']+'\nAppArmorProfile='+key('service:'+row['unit'])+'\n'

def verify_policy(rows,d):
    expected=generate(rows,d);bad=verify_root(rows,d,expected)
    from codeverify import verify_kernel_policy
    bad+=verify_kernel_policy('/etc/stand/stand-profiles',{'stand-session'}|{x.split('\t')[2] for x in expected['launch.tsv'].splitlines()})
    for name in CHANNEL_PROFILES:
        bad+=verify_kernel_policy('/etc/apparmor.d/'+name,{name})
    for name,text in expected.items():
        p=P('/etc/apparmor.d/abstractions')/name.removesuffix('.rules') if name in ('stand-map.rules','stand-read.rules') else P('/etc/stand')/name
        if not p.exists() or p.read_text()!=text:bad.append(name)
    active=P('/sys/kernel/security/apparmor/profiles').read_text()
    wanted={x.split('\t')[2]+' (enforce)' for x in expected['launch.tsv'].splitlines()}
    actual={x for x in active.splitlines() if x.startswith('stand-run-')}
    if actual!=wanted:bad.append('exact active workload profile set')
    if 'stand-session (enforce)' not in active:bad.append('launcher enforcement')
    for line in expected['launch.tsv'].splitlines():
        if line.split('\t')[2]+' (enforce)' not in active:bad.append(line.split('\t')[2])
    return {'ok':not bad,'mismatches':bad,'launches':len(expected['launch.tsv'].splitlines())}

def revoke():
    """All ordinary workload descendants remain in these profiles; kill before file mutation."""
    victims=set();deadline=time.monotonic()+10
    while time.monotonic()<deadline:
        live=[]
        for p in P('/proc').iterdir():
            if not p.name.isdigit():continue
            try:
                if (p/'attr/current').read_text().startswith('stand-run-') and (p/'stat').read_text().split(') ',1)[1][0]!='Z':
                    live.append(int(p.name));os.kill(int(p.name),signal.SIGKILL)
            except (OSError,ProcessLookupError):pass
        victims.update(live)
        if not live:return sorted(victims)
        time.sleep(.02)
    raise RuntimeError('ordinary code holders did not exit')

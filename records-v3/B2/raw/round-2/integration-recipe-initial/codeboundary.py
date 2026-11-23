"""Declaration-derived ordinary launch, executable mapping and read-closure policy."""
import hashlib,json,os,pathlib,re,shlex,signal,stat,subprocess,time
P=pathlib.Path
DATA={'/usr/bin/ed':'ed','/usr/bin/w3m':'w3m','/usr/bin/cat':'-','/usr/bin/cp':'-','/usr/bin/mkdir':'-','/usr/bin/curl':'-'}

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
    def add(name,binary,script=None,mode='sealed',extra='-'):
        binary=str(P(binary).resolve());safe(binary)
        if binary not in files or not immutable(binary):raise ValueError('interpreter/executable outside recorded immutable closure')
        if script and (script not in files or not immutable(script)):raise ValueError('script outside recorded immutable closure')
        profile=key(name)
        launch.append('\t'.join([name,mode,profile,binary,files[binary]['sha256'],script or '-',files[script]['sha256'] if script else '-',extra]))
        common=['  #include <stand-map.rules>',f'  "{binary}" ix,','  /dev/null rw,','  /dev/urandom r,','  /dev/random r,','  /proc/*/attr/current r,','  signal (receive) peer=unconfined,','  signal (send,receive) peer='+profile+',','  signal (send) peer=stand-session,']
        if mode=='sealed':common+=['  /** r,'] # Landlock further narrows reads to exact immutable closure.
        else:common+=['  /** r,','  /home/stand/ rw,','  /home/stand/** rwk,','  /tmp/ rw,','  /tmp/** rwk,','  network inet stream,','  network inet6 stream,','  network inet dgram,','  network inet6 dgram,','  network unix stream,']
        # No shell/helper exec, ptrace, capabilities, mount or child profile changes.
        profiles.append('profile '+profile+' flags=(attach_disconnected) {\n'+'\n'.join(common)+'\n}\n')
    for path,extra in DATA.items():
        if path in files:add(path,path,mode='data',extra=extra)
    for r in rows:
        if r['type'] not in ('program','code') or not r.get('managed'):continue
        from stand import manifest
        for f in manifest(r,d):
            if f['mode']&0o111 and f['path'] in mapped:add(f['path'],f['path'])
        for ep in r.get('entrypoints',[]):add(ep['path'],ep['interpreter'],ep['path'])
    for r in rows:
        if r['type']=='service' and r.get('managed'):
            import configparser
            c=configparser.ConfigParser(interpolation=None);c.read_string(r['unit_text']);args=shlex.split(c['Service']['ExecStart'])
            # Services use the same boundary; arguments originate in their declaration line.
            add('service:'+r['unit'],args[0],extra='|'.join(args[1:]) or '-')
    dirs={str(p) for x in read for p in P(x).parents}
    closure='\n'.join(sorted(set(read)|dirs|{'/dev/null'}))+'\n'
    mapping='\n'.join('"'+p+'" m,' for p in mapped)+'\n'
    launcher='''profile stand-session /usr/local/bin/stand-session flags=(attach_disconnected) {
  #include <stand-map.rules>
  /** r,
  /var/lib/stand/apply.lock rk,
  /dev/tty rw,
  /dev/null rw,
  /proc/*/attr/current w,
  /usr/bin/sudo Ux,
  /usr/local/bin/stand-session ix,
  signal (receive) peer=unconfined,
  signal (send,receive) peer=stand-session,
  signal (receive) peer=stand-run-*,
  change_profile -> stand-run-*,
}
'''
    return {'read-closure':closure,'launch.tsv':'\n'.join(launch)+'\n','stand-map.rules':mapping,'stand-profiles':launcher+'\n'.join(profiles)}

def refresh_trust(rows,d):
    from stand import atomic
    import noexec
    state=noexec.refresh_trust(rows,d)
    generated=generate(rows,d)
    for name,text in generated.items():
        p=P('/etc/apparmor.d/stand-map.rules') if name=='stand-map.rules' else P('/etc/stand')/name
        atomic(p,text)
    subprocess.run(['/usr/sbin/apparmor_parser','-r','-T','/etc/stand/stand-profiles'],check=True,capture_output=True)
    for r in rows:
        if r['type']=='service' and r.get('managed'):
            atomic(P('/etc/systemd/system')/(r['unit']+'.d')/'50-code-boundary.conf',service_dropin(r))
    state.update(mechanism='AppArmor exec/map + sealed Landlock read closure + inherited seccomp',profiles=len(generated['launch.tsv'].splitlines()))
    return state

def service_dropin(row):return '[Service]\nExecStart=\nExecStart=/usr/local/bin/stand-session --service '+row['unit']+'\n'

def verify_policy(rows,d):
    expected=generate(rows,d);bad=[]
    for name,text in expected.items():
        p=P('/etc/apparmor.d/stand-map.rules') if name=='stand-map.rules' else P('/etc/stand')/name
        if not p.exists() or p.read_text()!=text:bad.append(name)
    active=P('/sys/kernel/security/apparmor/profiles').read_text()
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

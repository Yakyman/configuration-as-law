"""Admission of inert files and fixed C compilation of recorded source bytes."""
import base64, ctypes, hashlib, json, os, pathlib, re, resource, subprocess, tempfile
P=pathlib.Path
LIMIT=16*1024*1024

def read(path):
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        import stat
        if not stat.S_ISREG(os.fstat(fd).st_mode):raise ValueError('regular input required')
        with os.fdopen(fd,'rb',closefd=False) as f:b=f.read(LIMIT+1)
        if len(b)>LIMIT:raise ValueError('input size limit')
        return b
    finally:os.close(fd)

def prepare(operation,filename):
    spec=json.loads(read(filename))
    if set(spec)-{'id','version','source','sha256','path','interpreter'}:raise ValueError('unsupported import field')
    ident=spec['id']
    if not re.fullmatch('[a-zA-Z0-9_-]+',ident):raise ValueError('invalid import id')
    b=read(spec['path'])
    if hashlib.sha256(b).hexdigest()!=spec['sha256']:raise ValueError('import checksum mismatch')
    if operation not in ('install','source'):raise ValueError('use install or source with exact import specification')
    interpreter=spec.get('interpreter')
    if operation=='source' and interpreter:raise ValueError('build source is not an executable entry')
    if operation=='install' and not interpreter and b[:4]!=b'\x7fELF':raise ValueError('native file or explicit fixed interpreter required')
    path='/opt/stand/pkgs/'+ident+('/src/input.c' if operation=='source' else '/bin/program')
    row={'id':('source:' if operation=='source' else 'import:')+ident,'type':'code' if operation=='source' or interpreter else 'program','managed':True,
         'version':spec['version'],'source':spec['source'],'channel':'build-source' if operation=='source' else 'direct-import',
         'files':[{'path':path,'kind':'file','mode':0o444 if operation=='source' or interpreter else 0o555,'uid':0,'gid':0,
                   'sha256':spec['sha256'],'content_b64':base64.b64encode(b).decode()}]}
    if interpreter:row['entrypoints']=[{'path':path,'interpreter':interpreter}]
    return row

def build(ident):
    import stand
    rows=stand.load(stand.current_dir());byid={r['id']:r for r in rows}
    row=byid.get(ident,{})
    if row.get('channel')!='build-source' or len(row.get('files',[]))!=1 or row.get('entrypoints'):raise ValueError('one recorded C source line required')
    f=row['files'][0];source=P(f['path'])
    if stand.filevalue(source)!=stand.desired_file(f):raise ValueError('recorded source readback failed')
    compiler=P('/usr/bin/gcc').resolve()
    closure={f['path']:f for r in rows if r['type'] in ('base','program','code') for f in stand.manifest(r,stand.current_dir())}
    if str(compiler) not in closure or stand.filevalue(compiler)!=stand.desired_file(closure[str(compiler)]):raise ValueError('compiler is not exact recorded code')
    outname=ident.removeprefix('source:')
    if not re.fullmatch('[a-zA-Z0-9_-]+',outname):raise ValueError('invalid build identifier')
    apparmor=ctypes.CDLL('libapparmor.so.1',use_errno=True)
    apparmor.aa_change_onexec.argtypes=[ctypes.c_char_p]
    apparmor.aa_change_onexec.restype=ctypes.c_int
    def restrict():
        if apparmor.aa_change_onexec(b'stand-build'):
            error=ctypes.get_errno();raise OSError(error,os.strerror(error))
        os.setgroups([]);os.setgid(1000);os.setuid(1000)
        resource.setrlimit(resource.RLIMIT_CPU,(30,30));resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_FSIZE,(LIMIT,LIMIT))
    with tempfile.TemporaryDirectory(prefix='stand-build-',dir='/var/lib/stand') as td:
        os.chown(td,1000,1000);os.chmod(td,0o700)
        output=P(td)/'result'
        result=subprocess.run([str(compiler),'-x','c','-O2','-fno-lto','-static',str(source),'-o',str(output)],
                 env={'PATH':'/usr/bin:/bin','HOME':td,'TMPDIR':td,'LANG':'C'},preexec_fn=restrict,capture_output=True,text=True,timeout=60)
        if result.returncode:raise ValueError('fixed recorded compiler refused: '+result.stderr[-3000:])
        payload=read(output)
    # Output remains inert. Publishing uses the ordinary identity and refuses
    # links; the separate import application is the only launch admission.
    target=P('/home/stand')/(outname+'.built')
    spec={'id':outname+'-built','version':row['version'],'source':'recorded-build:'+f['sha256']+':'+closure[str(compiler)]['sha256'],
          'sha256':hashlib.sha256(payload).hexdigest(),'path':str(target)}
    old=os.geteuid();os.seteuid(1000)
    try:
        for p,b in ((target,payload),(P(str(target)+'.json'),(json.dumps(spec,sort_keys=True)+'\n').encode())):
            fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_TRUNC|os.O_NOFOLLOW,0o600)
            with os.fdopen(fd,'wb') as stream:stream.write(b)
    finally:os.seteuid(old)
    print('BUILT INERT '+str(target)+' sha256:'+spec['sha256'],flush=True)
    print('IMPORT_SPEC '+str(target)+'.json',flush=True)
    return 0

"""Offline exact-content language project admission; never invokes package code.

The complete lock is declaration content. Archives remain data until the broker
applies the returned row. No pip backend, npm lifecycle, or package evaluator is
used during admission. Runtime execution uses the existing sealed launcher.
"""
import base64,email,hashlib,io,json,os,pathlib,re,stat,tarfile,tempfile,zipfile
MAX_BYTES=32*1024*1024

def digest(b):return hashlib.sha256(b).hexdigest()
def name(s):
    if not isinstance(s,str) or not re.fullmatch(r'[a-zA-Z0-9_.-]+',s):raise ValueError('unsupported package/project name')
    return re.sub(r'[-_.]+','-',s).lower()
def path(s):
    p=pathlib.PurePosixPath(s)
    if not s or p.is_absolute() or '..' in p.parts or not re.fullmatch(r'[a-zA-Z0-9_./+@,=-]+',s):raise ValueError('unsafe archive path')
    return str(p)
def payload(p,b):return dict(path=p,kind='file',mode=0o444,uid=0,gid=0,sha256=digest(b),content_b64=base64.b64encode(b).decode())
def read(p):
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb') as f:
        if not stat.S_ISREG(os.fstat(f.fileno()).st_mode):raise ValueError('regular artifact required')
        b=f.read(MAX_BYTES+1)
    if len(b)>MAX_BYTES:raise ValueError('artifact exceeds admission size limit')
    return b

def archive(data,channel):
    out={};total=0
    def add(n,b):
        nonlocal total
        n=path(n);total+=len(b)
        if total>MAX_BYTES or n in out:raise ValueError('archive size/duplicate refused')
        out[n]=b
    if channel=='pip':
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for f in z.infolist():
                if f.is_dir():continue
                mode=f.external_attr>>16
                if stat.S_ISLNK(mode) or f.file_size>MAX_BYTES:raise ValueError('wheel link/size refused')
                add(f.filename,z.read(f))
        if any(n.endswith('.pth') or '.data/' in n for n in out):raise ValueError('wheel .pth and relocation require explicit separate code import')
        metas=[b for n,b in out.items() if n.endswith('.dist-info/METADATA')]
        wheels=[b for n,b in out.items() if n.endswith('.dist-info/WHEEL')]
        if len(metas)!=1 or len(wheels)!=1:raise ValueError('one wheel metadata set required; build backends refused')
        m=email.message_from_bytes(metas[0]);deps=m.get_all('Requires-Dist',[])
        return out,m['Name'],m['Version'],deps
    with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as t:
        for f in t:
            if f.isdir():continue
            if not f.isfile() or f.size>MAX_BYTES or not f.name.startswith('package/'):raise ValueError('npm archive links/devices/layout refused')
            add(f.name[len('package/'):],t.extractfile(f).read())
    m=json.loads(out['package.json']);deps=m.get('dependencies',{})
    if m.get('optionalDependencies') or m.get('peerDependencies') or m.get('bundleDependencies') or m.get('bundledDependencies'):raise ValueError('optional/peer/bundled dependencies require explicit supported resolution')
    return out,m['name'],m['version'],[k+' '+v for k,v in deps.items()]

def version(v):
    if not re.fullmatch(r'\d+(?:\.\d+)*',v):raise ValueError('unsupported dependency version syntax')
    return tuple(int(x) for x in v.split('.'))+(0,)*max(0,3-len(v.split('.')))
def dependency(req,channel,versions):
    # Deliberately finite constraints, never silently omit a conditional dependency.
    if channel=='pip':m=re.fullmatch(r'([A-Za-z0-9_.-]+)\s*\(?\s*(==|>=)?\s*([0-9.]+)?\s*\)?',req)
    else:m=re.fullmatch(r'([A-Za-z0-9_.-]+)\s+(\^|~|>=|=)?([0-9.]+)',req)
    if not m:raise ValueError('unsupported dependency constraint: '+req)
    n=name(m[1]);op=m[2] or '=';want=m[3]
    if n not in versions:raise ValueError('missing locked dependency '+n)
    if want:
        actual=version(versions[n]);v=version(want)
        ok= actual>=v if op=='>=' else actual>=v and actual<(v[0]+1,0,0) if op=='^' and v[0]>0 else actual>=v and actual<(v[0],v[1]+1,0) if op=='~' else actual==v
        if not ok:raise ValueError('locked version violates dependency '+req)
    return n

def prepare(tool,args):
    channel='pip' if tool in ('pip','pip3') else 'npm'
    if tool not in ('pip','pip3','npm') or len(args)!=3 or args[:2]!=['install','--stand-lock']:
        raise ValueError('use install --stand-lock FILE; mutable installs, links, source builds, lifecycle commands and configuration overrides refused')
    lock_bytes=read(args[2]);lock=json.loads(lock_bytes)
    if set(lock)!={'schema','channel','project','packages','entry_code','entry_sha256'} or lock['schema']!=1 or lock['channel']!=channel:raise ValueError('invalid language lock')
    project=name(lock['project']);root='/opt/stand/pkgs/'+channel+'-'+project
    packages=lock['packages']
    if not isinstance(packages,list) or not packages or len(packages)>128:raise ValueError('finite locked package list required')
    versions={name(p['name']):p['version'] for p in packages}
    if len(versions)!=len(packages):raise ValueError('duplicate package')
    files={};resolved=[]
    for p in packages:
        if set(p)!={'name','version','sha256','source','archive','dependencies'}:raise ValueError('invalid package lock fields')
        n=name(p['name'])
        if pathlib.PurePosixPath(p['archive']).name!=p['archive']:raise ValueError('artifact must be alongside lock')
        data=read(pathlib.Path(args[2]).parent/p['archive'])
        if digest(data)!=p['sha256']:raise ValueError('artifact checksum mismatch')
        if not isinstance(p['source'],str) or not p['source'] or not isinstance(p['version'],str) or not p['version']:raise ValueError('source and exact version required')
        artifact_path=root+'/artifacts/'+p['archive']
        if artifact_path in files:raise ValueError('duplicate archive filename')
        files[artifact_path]=payload(artifact_path,data)
        entries,actual_name,actual_version,deps=archive(data,channel)
        if name(actual_name)!=n or actual_version!=p['version']:raise ValueError('archive name/version mismatch')
        required=sorted(set(dependency(x,channel,versions) for x in deps))
        if required!=sorted(p['dependencies']):raise ValueError('dependency edges differ from archive metadata')
        target=root+('/site/' if channel=='pip' else '/node_modules/'+n+'/')
        for f,b in entries.items():
            key=target+f
            if key in files:raise ValueError('overlapping package paths')
            files[key]=payload(key,b)
        resolved.append({k:v for k,v in p.items() if k!='archive'})
    code=lock['entry_code'].encode()
    if digest(code)!=lock['entry_sha256']:raise ValueError('entry checksum mismatch')
    if channel=='pip':
        code=('import sys\nsys.path.insert(0,'+repr(root+'/site')+')\n').encode()+code
        ep=root+'/main.py';interpreter='/usr/bin/python3.13'
    else:ep=root+'/main.js';interpreter='/usr/bin/node'
    files[ep]=payload(ep,code)
    # Keep the submitted lock itself: install state identifies every source byte,
    # dependency edge and chosen project entry, rather than just a digest label.
    files[root+'/project.lock.json']=payload(root+'/project.lock.json',lock_bytes)
    return dict(id='language:'+channel+':'+project,type='program',managed=True,version=digest(lock_bytes),source='locked-'+channel+'-project',channel=channel,packages=resolved,lock_sha256=digest(lock_bytes),files=list(files.values()),entrypoints=[dict(path=ep,interpreter=interpreter)])


def validate(row):
    """Re-derive exactly the installed state and metadata from declared archives."""
    if row.get('channel') not in ('pip','npm'):raise ValueError('unsupported language channel')
    files={f['path']:f for f in row['files']}
    if len(files)!=len(row['files']):raise ValueError('duplicate language file')
    locks=[f for p,f in files.items() if p.endswith('/project.lock.json')]
    if len(locks)!=1:raise ValueError('one language project lock required')
    raw=base64.b64decode(locks[0]['content_b64'],validate=True)
    if len(raw)>MAX_BYTES:raise ValueError('lock size refused')
    lock=json.loads(raw);root='/opt/stand/pkgs/'+row['channel']+'-'+name(lock['project'])
    with tempfile.TemporaryDirectory(prefix='language-validate-') as directory:
        target=pathlib.Path(directory);(target/'project.lock.json').write_bytes(raw)
        for p in lock['packages']:
            filename=p['archive']
            if pathlib.PurePosixPath(filename).name!=filename or filename=='project.lock.json':raise ValueError('unsafe artifact filename')
            f=files[root+'/artifacts/'+filename];data=base64.b64decode(f['content_b64'],validate=True)
            if len(data)>MAX_BYTES:raise ValueError('artifact size refused')
            (target/filename).write_bytes(data)
        expected=prepare(row['channel'],['install','--stand-lock',str(target/'project.lock.json')])
    if row!=expected:raise ValueError('language declaration differs from its exact lock/artifact state')

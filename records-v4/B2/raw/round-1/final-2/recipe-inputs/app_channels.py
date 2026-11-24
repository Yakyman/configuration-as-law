"""Pinned application-format import. No artifact runtime or build hook is executed."""
import base64, configparser, hashlib, io, json, os, pathlib, re, stat, struct, subprocess, tarfile, tempfile
P=pathlib.Path
LIMIT=64*1024*1024
PERMISSIONS={'network':False,'devices':False,'host_files':False,'writable_root':False,'extra_arguments':False}
_CACHE={}
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def checked_name(s):
    if not isinstance(s,str) or not re.fullmatch(r'[A-Za-z0-9_.+-]+',s):raise ValueError('invalid artifact identifier')
    return s
def safe_name(s):
    p=pathlib.PurePosixPath(s)
    if p.is_absolute() or '..' in p.parts or not re.fullmatch(r'[A-Za-z0-9_./+@=-]+',s):raise ValueError('unsafe archive name')
    return str(p)
def untar(data):
    out={};total=0
    with tarfile.open(fileobj=io.BytesIO(data),mode='r:*') as t:
        for m in t:
            name=safe_name(m.name)
            if m.isdir():continue
            if not m.isfile() or m.mode&0o7000 or name in out:raise ValueError('archive links/devices/special bits/duplicates refused')
            total+=m.size
            if total>LIMIT:raise ValueError('archive too large')
            out[name]=(t.extractfile(m).read(),0o555 if m.mode&0o111 else 0o444)
    return out
def native(data):
    if len(data)<64 or data[:6]!=b'\x7fELF\x02\x01' or struct.unpack_from('<H',data,18)[0]!=62:raise ValueError('fixed native ELF64 entrypoint required')
    off=struct.unpack_from('<Q',data,32)[0];size,count=struct.unpack_from('<HH',data,54)
    if size<56 or off+size*count>len(data):raise ValueError('invalid ELF')
    for n in range(count):
        typ,flags=struct.unpack_from('<II',data,off+n*size)
        if typ==3:raise ValueError('this application profile requires static native code')
        if typ==1 and flags&3==3 or typ==0x6474e551 and flags&1:raise ValueError('writable executable ELF refused')
def command(*args):
    p=subprocess.run(list(map(str,args)),capture_output=True,timeout=60,env={'PATH':'/usr/bin:/bin','HOME':'/nonexistent','LANG':'C'})
    if p.returncode:raise ValueError('artifact parser refused: '+p.stderr.decode(errors='replace')[:500])
    return p.stdout

def tree(root):
    out={}
    for p in root.rglob('*'):
        if p.is_symlink():raise ValueError('artifact symlinks refused')
        if p.is_dir():continue
        if not p.is_file() or p.stat().st_size>LIMIT:raise ValueError('artifact device or size refused')
        out[safe_name(str(p.relative_to(root)))]=(p.read_bytes(),0o555 if p.stat().st_mode&0o111 else 0o444)
    if sum(len(v[0]) for v in out.values())>LIMIT:raise ValueError('artifact too large')
    return out

def unpack(channel,spec,blob):
    if spec['permissions']!=PERMISSIONS:raise ValueError('unsupported application permissions')
    entry=safe_name(spec['entrypoint'])
    if channel=='oci':
        files=untar(blob)
        def get(name):return files[name][0]
        def desc(d):
            dg=d['digest']
            if not re.fullmatch('sha256:[0-9a-f]{64}',dg):raise ValueError('sha256 descriptor required')
            b=get('blobs/sha256/'+dg[7:])
            if len(b)!=d['size'] or sha(b)!=dg[7:]:raise ValueError('OCI descriptor mismatch')
            return b
        if json.loads(get('oci-layout'))!={'imageLayoutVersion':'1.0.0'}:raise ValueError('unsupported OCI layout')
        index=json.loads(get('index.json'))
        matches=[d for d in index['manifests'] if d['digest']==spec['digest']]
        if len(matches)!=1:raise ValueError('exact image digest required')
        manifest=json.loads(desc(matches[0]))
        if manifest['schemaVersion']!=2 or len(manifest['layers'])!=1:raise ValueError('single-layer OCI image required')
        config=json.loads(desc(manifest['config']))
        layer=desc(manifest['layers'][0])
        if manifest['layers'][0]['mediaType']!='application/vnd.oci.image.layer.v1.tar':raise ValueError('uncompressed OCI layer required')
        expected={'Entrypoint':['/'+entry],'Cmd':[],'Env':[],'User':'1000:1000','WorkingDir':'/'}
        if config.get('architecture')!='amd64' or config.get('os')!='linux' or config.get('config')!=expected:raise ValueError('unsupported OCI process config')
        if config.get('rootfs')!={'type':'layers','diff_ids':['sha256:'+sha(layer)]}:raise ValueError('OCI diff_id mismatch')
        if spec['configuration']!={'image':spec['digest'],'entrypoint':'/'+entry,'uid':1000,'gid':1000,'read_only':True,'network':'none','mounts':[],'capabilities':[],'hooks':[]}:raise ValueError('unsupported container configuration')
        out=untar(layer)
    elif channel=='flatpak':
        with tempfile.TemporaryDirectory(prefix='stand-flatpak-') as td:
            td=P(td);repo=td/'repo';repo.mkdir()
            for name,(data,mode) in untar(blob).items():
                p=repo/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
            # Canonical file-only transport omits empty repository directories.
            for directory in ('objects','tmp','state','extensions','refs/heads','refs/remotes','refs/mirrors'):
                (repo/directory).mkdir(parents=True,exist_ok=True)
            # Repository config is supplied by the importer, never by artifact input.
            (repo/'config').write_text('[core]\nrepo_version=1\nmode=archive-z2\n')
            for field in ('commit','runtime_commit'):
                if not re.fullmatch('[0-9a-f]{64}',spec[field]):raise ValueError('exact OSTree commit required')
            command('/usr/local/lib/stand/format-tools/ostree','--repo='+str(repo),'fsck','--quiet')
            for kind,commit in [('app',spec['commit']),('runtime',spec['runtime_commit'])]:
                command('/usr/local/lib/stand/format-tools/ostree','--repo='+str(repo),'checkout','--user-mode','--force-copy',commit,td/kind)
            app=tree(td/'app');runtime=tree(td/'runtime')
            c=configparser.ConfigParser(interpolation=None);c.read_string(app['metadata'][0].decode())
            if set(c.sections())!={'Application'} or dict(c['Application'])!={'name':spec['application'],'runtime':spec['runtime'],'command':entry.removeprefix('files/bin/')}:raise ValueError('unsupported Flatpak metadata/permissions')
            rc=configparser.ConfigParser(interpolation=None);rc.read_string(runtime['metadata'][0].decode())
            if set(rc.sections())!={'Runtime'} or rc['Runtime'].get('name')!=spec['runtime'].split('/')[0]:raise ValueError('runtime metadata mismatch')
            out={'app/'+k:v for k,v in app.items()};out.update({'runtime/'+k:v for k,v in runtime.items()});entry='app/'+entry
    elif channel=='appimage':
        if blob[:4]!=b'\x7fELF' or blob[8:11]!=b'AI\x02':raise ValueError('type-2 AppImage required')
        offset=spec['squashfs_offset']
        if type(offset)!=int or offset<64 or blob[offset:offset+4]!=b'hsqs':raise ValueError('invalid AppImage filesystem offset')
        if spec['runtime_sha256']!=sha(blob[:offset]):raise ValueError('AppImage runtime digest mismatch')
        with tempfile.TemporaryDirectory(prefix='stand-appimage-') as td:
            td=P(td);p=td/'image';p.write_bytes(blob)
            command('/usr/local/lib/stand/format-tools/unsquashfs','-no-progress','-no-xattrs','-o',offset,'-d',td/'root',p)
            out=tree(td/'root')
    else:raise ValueError('unsupported application channel')
    if entry not in out:raise ValueError('entrypoint absent')
    native(out[entry][0])
    # Only the one declared process entry may be launched. Other contents remain recorded readable data.
    return {k:(v[0],0o555 if k==entry else 0o444) for k,v in out.items()},entry

def file_row(path,data,mode):return {'path':path,'kind':'file','sha256':sha(data),'mode':mode,'uid':0,'gid':0,'content_b64':base64.b64encode(data).decode()}
def build_rows(channel,spec,blob):
    ident=checked_name(spec['id'])
    if len(blob)>LIMIT or sha(blob)!=spec['sha256']:raise ValueError('artifact checksum mismatch')
    payload,entry=unpack(channel,spec,blob);prefix='/opt/stand/pkgs/'+ident
    common={'type':'program','managed':True,'source':channel+':sha256:'+sha(blob),'version':spec.get('commit',spec.get('digest',sha(blob)))}
    row={**common,'id':ident,'channel':channel,'application_spec':spec,'artifact_b64':base64.b64encode(blob).decode(),'files':[file_row(prefix+'/'+k,b,m) for k,(b,m) in sorted(payload.items())],'application_entry':prefix+'/'+entry}
    if channel!='oci':return [row]
    image={**common,'id':ident+'-image','channel':'oci-image','image_digest':spec['digest'],'files':[file_row(prefix+'-image/image.oci.tar',blob,0o444)]}
    row['image_line']=image['id']
    return [image,row]
def import_rows(channel,spec):
    spec=dict(spec);artifact=P(spec.pop('artifact'))
    fd=os.open(artifact,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb') as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):raise ValueError('regular artifact file required')
        blob=stream.read(LIMIT+1)
    return build_rows(channel,spec,blob)
def validate(rows,directory):
    known={r['id']:r for r in rows}
    for row in rows:
        channel=row.get('channel')
        if channel not in ('oci','flatpak','appimage'):continue
        cache_key=sha(canonical(row).encode())
        if cache_key not in _CACHE:
            blob=base64.b64decode(row['artifact_b64'],validate=True)
            expected=build_rows(channel,row['application_spec'],blob)
            if row!=expected[-1]:raise ValueError('application line differs from pinned artifact')
            _CACHE[cache_key]=expected
        expected=_CACHE[cache_key]
        if channel=='oci' and known.get(row['image_line'])!=expected[0]:raise ValueError('container requires exact declared image line')

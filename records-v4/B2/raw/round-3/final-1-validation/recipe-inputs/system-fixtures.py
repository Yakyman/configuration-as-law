#!/usr/bin/python3
"""Fixed Debian inputs and trusted catalog generation inside the image build."""
import base64,hashlib,io,json,os,pathlib,re,shutil,stat,subprocess,sys,tarfile,tempfile,urllib.request
P=pathlib.Path
ITEMS={
 'ed-old':('e/ed/ed_1.19-1_amd64.deb','eb009104f25267f6bddbf936afbfa2cb23b6c1685b2d4c60027c4513feb17745'),
 'ed-new':('e/ed/ed_1.21.1-1_amd64.deb','b5498068d8ac54ad004bacbde2223a348fee781f9bb94328b01d8bfcbd179b48'),
 'hello':('h/hello/hello_2.10-5_amd64.deb','4536aabbb75ec21ffe161099ee4b97274945770bdb0682e25ec322421211ca5e')}
def sha(b):return hashlib.sha256(b).hexdigest()
def run(*args):return subprocess.check_output(args,text=True)
def item(root,key):
    rel,wanted=ITEMS[key];p=root/rel.split('/')[-1]
    if sha(p.read_bytes())!=wanted:raise ValueError('distribution artifact checksum mismatch')
    return p
def meta(p):
    text=run('/usr/bin/dpkg-deb','-f',str(p));out={}
    for line in text.splitlines():
        if line.startswith(' ') or ':' not in line:continue
        k,v=line.split(':',1);out[k]=v.strip()
    return out
def files(p):
    data=subprocess.check_output(['/usr/bin/dpkg-deb','--fsys-tarfile',str(p)])
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        return sorted(set(str(P('/'+x.name.removeprefix('./')).parent.resolve()/P(x.name).name) for x in t if x.isfile() or x.issym()))
def value(p):
    p=P(p)
    if not p.exists() and not p.is_symlink():return None
    s=p.lstat();v=dict(path=str(p),mode=stat.S_IMODE(s.st_mode),uid=s.st_uid,gid=s.st_gid)
    if p.is_symlink():return dict(v,kind='symlink',target=os.readlink(p))
    if not p.is_file():raise ValueError('unsupported transaction path '+str(p))
    b=p.read_bytes();return dict(v,kind='file',sha256=sha(b),content_b64=base64.b64encode(b).decode())
def snapshot(paths):return {p:v for p in sorted(paths) if (v:=value(p)) is not None}
def dbpaths():return {str(p) for p in P('/var/lib/dpkg').rglob('*') if p.is_file() and p.name not in ('lock','lock-frontend','Lock','status-old','available-old') and not p.name.endswith('-old')}
def packages():return dict(line.split('\t') for line in run('/usr/bin/dpkg-query','-W','-f=${binary:Package}\t${Version}\n').splitlines())
def restore(old,paths):
    for p in paths:
        target=P(p)
        if p not in old and (target.is_file() or target.is_symlink()):target.unlink()
    for p,v in old.items():
        target=P(p);target.parent.mkdir(parents=True,exist_ok=True)
        if target.is_symlink():target.unlink()
        if v['kind']=='symlink':target.unlink(missing_ok=True);target.symlink_to(v['target'])
        else:target.write_bytes(base64.b64decode(v['content_b64']));target.chmod(v['mode']);os.chown(target,v['uid'],v['gid'])
def fetch(root):
    root.mkdir(parents=True,exist_ok=True)
    for rel,wanted in ITEMS.values():
        target=root/rel.split('/')[-1]
        if not target.exists():
            with urllib.request.urlopen('https://deb.debian.org/debian/pool/main/'+rel,timeout=60) as r:target.write_bytes(r.read())
        if sha(target.read_bytes())!=wanted:raise ValueError('download hash mismatch')
    print('SYSTEM_FIXTURES_READY')
def dependency_states(expression):
    db={}
    for line in run('/usr/bin/dpkg-query','-W','-f=${binary:Package}\t${Version}\t${Depends}\t${Pre-Depends}\n').splitlines():
        n,v,deps,pre=line.split('\t');db[n]=(v,','.join(x for x in (deps,pre) if x))
    found={};pending=[expression]
    while pending:
        expr=pending.pop()
        for required in filter(None,(x.strip() for x in expr.split(','))):
            chosen=None
            for alternate in required.split('|'):
                m=re.fullmatch(r'\s*([a-zA-Z0-9+.-]+)(?::(?:any|native|amd64))?\s*(?:\((<<|<=|=|>=|>>)\s*([^() ]+)\))?\s*',alternate)
                if not m:raise ValueError('unsupported distribution dependency '+required)
                candidates=[n for n in db if n==m[1] or n.split(':')[0]==m[1]]
                for n in candidates:
                    if not m[2] or subprocess.run(['/usr/bin/dpkg','--compare-versions',db[n][0],m[2],m[3]]).returncode==0:chosen=n;break
                if chosen:break
            if chosen is None:raise ValueError('unresolved repository dependency '+required)
            if chosen in found:continue
            entries=[]
            for path in run('/usr/bin/dpkg-query','-L',chosen).splitlines():
                p=P(path)
                if not p.is_absolute() or (not p.is_file() and not p.is_symlink()):continue
                p=p.parent.resolve()/p.name;f=value(p)
                if f:entries.append({k:v for k,v in f.items() if k!='content_b64'})
            found[chosen]=dict(version=db[chosen][0],declaration_line='package:'+chosen,files=sorted(entries,key=lambda x:x['path']))
            pending.append(db[chosen][1])
    return found

def repository(package,key):
    m=meta(package);prefix='/opt/stand/pkgs/repository-'+m['Package'];installed=[]
    with tempfile.TemporaryDirectory(prefix='system-extract-') as td:
        subprocess.run(['/usr/bin/dpkg-deb','-x',str(package),td],check=True)
        for p in sorted(P(td).rglob('*')):
            if p.is_dir():continue
            f=value(p)
            if f['kind']!='file':raise ValueError('repository relocation currently requires regular files')
            f['path']=prefix+'/'+str(p.relative_to(td));f['mode'] &= 0o555;installed.append(f)
    archive=value(package);archive.update(path=prefix+'/artifact.deb',mode=0o444,uid=0,gid=0);installed.append(archive)
    rel,h=ITEMS[key];deps=','.join(x for x in (m.get('Depends',''),m.get('Pre-Depends','')) if x)
    return dict(id='repository:'+m['Package'],type='program',managed=True,channel='repository',package=m['Package'],version=m['Version'],source='https://deb.debian.org/debian/pool/main/'+rel,source_sha256=h,dependencies=deps,dependency_states=dependency_states(deps),files=installed)

def build(root):
    out=P('/usr/local/share/stand/system');out.mkdir(parents=True,exist_ok=True)
    old=item(root,'ed-old');new=item(root,'ed-new');hello=item(root,'hello')
    subprocess.run(['/usr/bin/dpkg','-i',str(old)],check=True)
    paths=set(files(old))|set(files(new))|dbpaths()|{'/usr/share/info/dir'}
    before=snapshot(paths);base_before=packages()
    subprocess.run(['/usr/bin/dpkg','-i',str(new)],check=True)
    paths|=dbpaths();after=snapshot(paths);base_after=packages()
    members=run('/usr/bin/dpkg-query','-L','ed').splitlines()
    changed=sorted(p for p in paths if before.get(p)!=after.get(p))
    before={p:before[p] for p in changed if p in before};after={p:after[p] for p in changed if p in after}
    # A real transaction produces the new bytes. Restore the exact captured old
    # bytes after a real downgrade so the factory starts from the old base.
    subprocess.run(['/usr/bin/dpkg','-i',str(old)],check=True);restore(before,changed)
    if packages()!=base_before:raise RuntimeError('base downgrade metadata mismatch')
    for p in changed:
        if value(p)!=before.get(p):raise RuntimeError('base restoration mismatch '+p)
    newrel,newhash=ITEMS['ed-new'];oldrel,oldhash=ITEMS['ed-old']
    row=dict(id='system:base-state',type='program',managed=True,channel='system-update',catalog_key='ed',source='https://deb.debian.org/debian/pool/main/'+newrel,source_sha256=newhash,version=sha(json.dumps(base_after,sort_keys=True).encode()),base_packages=base_after,previous_base_packages=base_before,native_arguments={'/usr/bin/ed':['--version']},files=list(after.values()),absent=sorted(set(changed)-set(after)),package_members={'ed':members},artifacts=[dict(source='https://deb.debian.org/debian/pool/main/'+newrel,sha256=newhash,package='ed',version=meta(new)['Version']),dict(source='https://deb.debian.org/debian/pool/main/'+oldrel,sha256=oldhash,package='ed',version=meta(old)['Version'])])
    installs={}
    for key in ('hello',):
        package=item(root,key);installed_row=repository(package,key)
        installs[installed_row['package']]=installed_row
    result=dict(schema=1,installs=installs,updates={'ed':dict(row=row,before=list(before.values()),after=list(after.values()),paths=changed)})
    (out/'catalog.json').write_text(json.dumps(result,sort_keys=True)+'\n');(out/'catalog.json').chmod(0o444)
    for key in ITEMS:
        src=item(root,key);shutil.copyfile(src,out/src.name);(out/src.name).chmod(0o444)
    print('SYSTEM_CATALOG_READY changed='+str(len(changed))+' base_packages='+str(len(base_after)),flush=True)
if __name__=='__main__':
    mode=sys.argv[1];root=P(sys.argv[2]);fetch(root) if mode=='fetch' else build(root) if mode=='catalog' else sys.exit('use fetch or catalog')

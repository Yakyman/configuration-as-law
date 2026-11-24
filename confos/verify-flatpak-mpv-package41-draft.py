#!/usr/bin/python3
"""Check additive inheritance and real app-object replacement in a disposable tree."""
import gzip,hashlib,json,os,shutil,subprocess,tarfile,tempfile
from pathlib import Path
draft=Path('interpreter-inputs/flatpak-mpv-integration41-draft')
old=Path('packages/confos-code-readers_0.40_amd64.deb')
new=draft/'confos-code-readers_0.41_amd64.deb'
manifest_name='usr/lib/confos/flatpak-reader-overrides/manifest.json'
def contents(path):
    process=subprocess.Popen(['dpkg-deb','--fsys-tarfile',str(path)],stdout=subprocess.PIPE)
    entries={};data={}
    with tarfile.open(fileobj=process.stdout,mode='r|') as tar:
        for item in tar:
            name=item.name.removeprefix('./').rstrip('/')
            assert name not in entries
            raw=tar.extractfile(item).read() if item.isfile() else None
            entries[name]=(item.type,item.mode,item.uid,item.gid,item.linkname,hashlib.sha256(raw).hexdigest() if raw is not None else None)
            if raw is not None: data[name]=raw
    assert process.wait()==0
    return entries,data
before,bdata=contents(old);after,adata=contents(new)
for name,value in before.items():
    assert name in after,name
    assert after[name]==value if name!=manifest_name else after[name][:5]==value[:5],name
original=json.loads(bdata[manifest_name]);items=json.loads(adata[manifest_name])
assert items[:len(original)]==original and len(items)==len(original)+3
rows=json.loads((draft/'mpv-app-overrides.json').read_text())
keys=('ref','commit','bundle_sha256','target','original_sha256','sha256','objects','mode','payload')
assert items[len(original):]==[{k:row[k] for k in keys} for row in rows]
docs='usr/share/doc/confos-code-readers/mpv41'
docnames=['mpv-app-overrides.json','flatpak-mpv-continuation-draft.md','flatpak-mpv-integration41-draft.md','patch-flatpak-app-ref41-draft.py','patch-mpv-lua-stream-draft.py','patch-luajit-code.py','code-file-policy.h']
allowed={docs,*(docs+'/'+name for name in docnames),*(str(Path(manifest_name).parent/row['payload']) for row in rows)}
assert after.keys()-before.keys()==allowed,(after.keys()-before.keys())^allowed
for row in rows:
    raw=gzip.decompress(adata[str(Path(manifest_name).parent/row['payload'])])
    assert hashlib.sha256(raw).hexdigest()==row['sha256']
namespace={}
exec(compile((draft/'source/flatpak_readers.py').read_text(),'private-flatpak-readers','exec'),namespace)
native=Path('interpreter-inputs/flatpak-analysis/root/usr/lib/confos/flatpak')
with tempfile.TemporaryDirectory(prefix='verify-',dir=draft) as temp:
    root=Path(temp)/'root';subprocess.run(['dpkg-deb','-x',str(new),str(root)],check=True)
    store=root/'usr/lib/confos/flatpak'
    for row in rows:
        rel=Path(row['ref'])/row['commit']/'files'/row['target']
        target=store/rel;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(native/rel,target);target.chmod(row['mode'])
        for obj in row['objects']:
            path=store/obj;path.parent.mkdir(parents=True,exist_ok=True);os.link(target,path)
        for name,destination in row['preserve_symlinks'].items():
            alias=store/row['ref']/row['commit']/'files'/name
            alias.parent.mkdir(parents=True,exist_ok=True);alias.symlink_to(destination)
    row=rows[0]
    try: namespace['apply'](root,store,row['ref'],row['commit'],'f'*64)
    except ValueError: pass
    else: raise AssertionError('wrong bundle accepted')
    paths=namespace['apply'](root,store,row['ref'],row['commit'],row['bundle_sha256'])
    for row in rows:
        target=store/row['ref']/row['commit']/'files'/row['target']
        assert hashlib.sha256(target.read_bytes()).hexdigest()==row['sha256']
        for obj in row['objects']:
            assert hashlib.sha256((store/obj).read_bytes()).hexdigest()==row['original_sha256']
            assert not os.path.samefile(target,store/obj)
            assert '/usr/lib/confos/flatpak/'+obj in paths and '/run/host/usr/lib/confos/flatpak/'+obj in paths
        for name,destination in row['preserve_symlinks'].items():
            alias=store/row['ref']/row['commit']/'files'/name
            assert os.readlink(alias)==destination and alias.resolve()==target.resolve()
print('SEALED40_PAYLOAD_INHERITED_EXCEPT_ADDITIVE_MANIFEST; THREE_EXACT_APP_REPLACEMENTS; ORIGINAL_OBJECTS_SYMLINKS_PRESERVED')
print('PRIVATE_STAGING_ONLY; NO_GUEST_RESULT')

#!/usr/bin/python3
"""Read exact native app targets and OSTree identities; write only private draft metadata."""
import hashlib,json,os,stat
from pathlib import Path
root=Path.cwd()
out=root/'interpreter-inputs/flatpak-mpv-integration41-draft'
out.mkdir(exist_ok=True)
store=root/'interpreter-inputs/flatpak-analysis/root/usr/lib/confos/flatpak'
ref='app/io.mpv.Mpv/x86_64/stable'
commit='13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc'
files=store/ref/commit/'files'
work=root/'interpreter-inputs/flatpak-mpv-lua-candidate'
bundle=root/'flatpak-inputs/mpv.flatpak'
def digest(path):
    with path.open('rb') as stream: return hashlib.file_digest(stream,'sha256').hexdigest()
bundle_hash=digest(bundle)
assert bundle_hash=='66d65390ff1b7a526b25a448f12d137f72df5859460c1d05e17508ed6a88bed9'
expected={
 'bin/mpv':('a6de4a9af6d84e78d7451bc0b68150de958c9c369ce010e8c2b9575b6e954cbb','42c25feff2de540289d7ec4245bd2d77785c042c994ce9978bab8c11437e6656'),
 'lib/libmpv.so.2.6.0':('1fcd8306d860def640c68c2fec47f20e38fc9c5f3bc4176d04fe2c6ca39902e4','a3fb816802e6fff0598e5326af29788155ee13b7275002dbb1f49095ddc52c68'),
 'lib/libluajit-5.1.so.2.1.1781966178':('565e9aa1f51c3880a66e9189d3fe505dd536b0ff4e8c34ad100c7ab76ceee523','3f3d40eb32dbd6303717c3c1fccb0ff819775a053f2653147fac2eee835236cf')}
identities={}
for name in expected:
    path=files/name
    assert path.is_file() and not path.is_symlink()
    identities[(path.stat().st_dev,path.stat().st_ino)]=name
objects={name:[] for name in expected}
for path in (store/'repo/objects').glob('*/*.file'):
    info=path.lstat()
    if not stat.S_ISREG(info.st_mode): continue
    name=identities.get((info.st_dev,info.st_ino))
    if name: objects[name].append(str(path.relative_to(store)))
rows=[]
for index,(name,(old,new)) in enumerate(expected.items()):
    path=files/name; candidate=work/'candidate'/path.name
    assert digest(path)==old and digest(candidate)==new
    assert stat.S_IMODE(path.stat().st_mode)==0o755
    assert objects[name]
    aliases={str(p.relative_to(files)):os.readlink(p) for p in (files/'lib').iterdir() if p.is_symlink() and p.resolve()==path.resolve()}
    rows.append({'ref':ref,'commit':commit,'bundle_sha256':bundle_hash,'target':name,
                 'original_sha256':old,'sha256':new,'objects':sorted(objects[name]),
                 'mode':0o755,'payload':'mpv41-'+str(index)+'.gz',
                 'candidate_worker_path':str(candidate.relative_to(root)),
                 'preserve_symlinks':aliases,'original_nlink':path.stat().st_nlink})
(out/'mpv-app-overrides.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n')
print(json.dumps(rows,indent=2,sort_keys=True))
print('EXACT_APP_BUNDLE_TARGET_OBJECT_MODE_SYMLINK_DISCOVERY_PASS')

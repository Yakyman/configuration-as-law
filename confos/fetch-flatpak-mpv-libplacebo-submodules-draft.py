#!/usr/bin/python3
"""Retain exact generator/development submodules from the pinned upstream Git tree."""
import hashlib,json,urllib.request,tarfile
from pathlib import Path
out=Path('interpreter-inputs/flatpak-mpv-lua-candidate/dev-sources')
url='https://api.github.com/repos/haasn/libplacebo/git/trees/451d8ea5661c868562725e6500deda7fdd4e9a1e?recursive=1'
data=urllib.request.urlopen(url).read()
(out/'libplacebo-git-tree.json').write_bytes(data)
tree=json.loads(data)
assert not tree.get('truncated')
commits={v['path']:v['sha'] for v in tree['tree'] if v['mode']=='160000'}
repos={'glad':'Dav1dde/glad','jinja':'pallets/jinja','markupsafe':'pallets/markupsafe','fast_float':'fastfloat/fast_float','Vulkan-Headers':'KhronosGroup/Vulkan-Headers'}
result=[]
for name,repo in repos.items():
    commit=commits['3rdparty/'+name]
    source=f'https://codeload.github.com/{repo}/tar.gz/{commit}'
    archive=out/('libplacebo-'+name+'.archive')
    payload=urllib.request.urlopen(source).read()
    archive.write_bytes(payload)
    with tarfile.open(archive) as t: assert t.getmembers()
    entry={'name':name,'commit':commit,'url':source,'sha256':hashlib.sha256(payload).hexdigest(),'bytes':len(payload)}
    result.append(entry)
    print(json.dumps(entry),flush=True)
(out/'libplacebo-submodules.json').write_text(json.dumps({'tree_url':url,'tree_sha256':hashlib.sha256(data).hexdigest(),'sources':result},indent=2)+'\n')

#!/usr/bin/python3
"""Fresh JS extension of retained Lua source in the same pinned SDK and headers."""
import hashlib,json,shutil,subprocess
from pathlib import Path
recipe=Path('prepare-flatpak-mpv-dependency-headers-draft.py').read_text()
exec(recipe[recipe.index('root = Path.cwd()'):recipe.index('import sys')])
overlay=work/'development-overlay'
exec(recipe[recipe.index('base = '):recipe.index('module=entry')])
jswork=root/'interpreter-inputs/flatpak-mpv-js-candidate'
assert not jswork.exists(), 'fresh independent candidate tree required'
old={'mpv':'42c25feff2de540289d7ec4245bd2d77785c042c994ce9978bab8c11437e6656','libmpv.so.2.6.0':'a3fb816802e6fff0598e5326af29788155ee13b7275002dbb1f49095ddc52c68','libluajit-5.1.so.2.1.1781966178':'3f3d40eb32dbd6303717c3c1fccb0ff819775a053f2653147fac2eee835236cf'}
for name,value in old.items(): assert hashlib.sha256((work/'candidate'/name).read_bytes()).hexdigest()==value
jswork.mkdir();shutil.copytree(work/'mpv',jswork/'mpv')
subprocess.run(['python3','patch-flatpak-mpv-js-stream-draft.py',str(jswork/'mpv')],check=True)
base += ['--bind',str(jswork),'/jswork']
options=['--prefix=/app','--libdir=lib','--wrap-mode=nofallback','-Dbackend_max_links=1',*find(manifest,'mpv')['config-opts'],'-Dsixel=enabled']
print('SAME_SDK_ORIGINAL_FEATURES',json.dumps(options),flush=True)
subprocess.run(base+['meson','setup','/jswork/build','/jswork/mpv',*options],check=True)
subprocess.run(base+['ninja','-C','/jswork/build','-j1','mpv','libmpv.so.2.6.0'],check=True)
candidate=jswork/'candidate';candidate.mkdir()
for name in ('mpv','libmpv.so.2.6.0'): shutil.copy2(jswork/'build'/name,candidate/name)
shutil.copy2(work/'candidate/libluajit-5.1.so.2.1.1781966178',candidate/'libluajit-5.1.so.2.1.1781966178')
for name,value in old.items(): assert hashlib.sha256((work/'candidate'/name).read_bytes()).hexdigest()==value
hashes={str(p.relative_to(jswork)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ('mpv','candidate') for p in (jswork/folder).rglob('*') if p.is_file()}
(jswork/'candidate-provenance.json').write_text(json.dumps({'prior_candidate_hashes_unchanged':old,'files':hashes,'js_patch_sha256':hashlib.sha256(Path('patch-flatpak-mpv-js-stream-draft.py').read_bytes()).hexdigest(),'sdk_commit':'a1b744b072d9f55d061e35382547ae80dad8d92abecc1da7dc1818de2daabfd3','build_options':options},indent=2)+'\n')
print('SEPARATE_JS_CANDIDATE_BUILT; ABI_FEATURE_NATIVE_CONTROLS_PENDING',flush=True)

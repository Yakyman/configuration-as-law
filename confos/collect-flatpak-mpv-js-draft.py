#!/usr/bin/python3
"""Preserve portable separate-JS evidence and verify the earlier candidate stayed intact."""
import hashlib,json,shutil
from pathlib import Path
root=Path.cwd();old=root/'interpreter-inputs/flatpak-mpv-lua-candidate'
work=root/'interpreter-inputs/flatpak-mpv-js-candidate'
out=work/'publish';out.mkdir(exist_ok=True)
assert (work/'native-controls-passed.json').is_file()
provenance=json.loads((work/'candidate-provenance.json').read_text())
for name,value in provenance['prior_candidate_hashes_unchanged'].items():
    assert hashlib.sha256((old/'candidate'/name).read_bytes()).hexdigest()==value
def hashes(folder):
    return {str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.rglob('*') if p.is_file()}
before,after=hashes(old/'mpv'),hashes(work/'mpv')
assert before.keys()==after.keys()
changed=sorted(name for name in before if before[name]!=after[name])
assert changed==['player/javascript.c','player/javascript/defaults.js'],changed
overlay_hashes=json.loads((old/'continuation-publish/continuation-file-hashes.json').read_text())
for name,value in overlay_hashes.items():
    if name.startswith('development-overlay/'):
        assert hashlib.sha256((old/name).read_bytes()).hexdigest()==value
files=list(work.glob('*.json'))+list(work.glob('*-abi.txt'))
files += [root/'logs'/name for name in ('flatpak-mpv-js-candidate-build.log','flatpak-mpv-js-native-controls.log','flatpak-mpv-js-native-controls2.log')]
for path in files:
    (out/path.name).write_text(path.read_text().replace(str(root),'<build>'))
for name in ('intro-buildoptions.json','intro-compilers.json'):
    (out/name).write_text((work/'build/meson-info'/name).read_text().replace(str(root),'<build>'))
(out/'config.h').write_bytes((work/'build/config.h').read_bytes())
(out/'meson-log.txt').write_text((work/'build/meson-logs/meson-log.txt').read_text().replace(str(root),'<build>'))
shutil.copytree(root/'interpreter-inputs/flatpak-mpv-js-integration41-draft',out/'alternate-recipe',dirs_exist_ok=True)
sources=['patch-flatpak-mpv-js-stream-draft.py','build-flatpak-mpv-js-candidate-draft.py','probe-flatpak-mpv-js-candidate-draft.py','prepare-flatpak-mpv-js-integration41-draft.py','compile-flatpak-mpv-candidate-draft.py','probe-flatpak-mpv-complete-runtime-draft.py','prepare-flatpak-mpv-dependency-headers-draft.py']
(out/'js-extension-inputs.json').write_text(json.dumps({'only_changed_source_files':changed,'original_candidate_unchanged':provenance['prior_candidate_hashes_unchanged'],'original_overlay_unchanged':True,'scripts_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in sources},'sdk_checksums_manifest_sha256':hashlib.sha256((old/'continuation-publish/sdk-input-checksums.json').read_bytes()).hexdigest(),'inherited_inputs_manifest_sha256':hashlib.sha256((old/'continuation-publish/complete-input-checksums.json').read_bytes()).hexdigest()},indent=2)+'\n')
print('SEPARATE_JS_EVIDENCE_PRESERVED; ONLY_TWO_SOURCE_FILES_CHANGED; OLD_CANDIDATES_AND_HEADERS_UNCHANGED')

#!/usr/bin/python3
"""After native success, derive an alternate sealed40-gated recipe; preserve old draft."""
import ast,hashlib,json
from pathlib import Path
root=Path.cwd()
work=root/'interpreter-inputs/flatpak-mpv-js-candidate'
old_dir='interpreter-inputs/flatpak-mpv-integration41-draft'
new_dir='interpreter-inputs/flatpak-mpv-js-integration41-draft'
out=root/new_dir
assert not out.exists(), 'alternate recipe already exists; inspect rather than overwrite'
assert (work/'native-controls-passed.json').is_file()
comparison=json.loads((work/'mpv-candidate-comparison.json').read_text())
assert not comparison['missing_features'] and not comparison['added_features']
assert all(not row['missing_exports'] for row in comparison['abi'].values())
old=(root/old_dir/'mpv-app-overrides.json').read_bytes()
assert hashlib.sha256(old).hexdigest()=='4ada6b113190b3cbf44ddaec16be03967fc05224c66ab89566cca94b5d8da0bf'
rows=json.loads(old)
expected={'mpv':'5c006b40eff5524ff10c24e9cb7392d776880f8acf7760f4a69accee139adf85','libmpv.so.2.6.0':'90a5f3cc9b7c141b93f26a1e951571a02fca1cf5d66996d43648ce4d55df6c66','libluajit-5.1.so.2.1.1781966178':'3f3d40eb32dbd6303717c3c1fccb0ff819775a053f2653147fac2eee835236cf'}
for index,row in enumerate(rows):
    name=Path(row['target']).name;path=work/'candidate'/name
    assert hashlib.sha256(path.read_bytes()).hexdigest()==expected[name]
    row['sha256']=expected[name];row['candidate_worker_path']=str(path.relative_to(root))
    row['payload']='mpv41js-'+str(index)+'.gz'
out.mkdir()
metadata=json.dumps(rows,indent=2,sort_keys=True)+'\n'
(out/'mpv-app-overrides.json').write_text(metadata)
metadata_hash=hashlib.sha256(metadata.encode()).hexdigest()
def replace(text,old,new):
    assert text.count(old)==1,old
    return text.replace(old,new)
inputs={}
for original,generated in [('patch-flatpak-app-ref41-draft.py','patch-app-ref.py'),('prepare-flatpak-mpv-package41-draft.py','prepare-component.py'),('verify-flatpak-mpv-package41-draft.py','verify-component.py')]:
    raw=(root/original).read_bytes();inputs[original]=hashlib.sha256(raw).hexdigest()
    text=replace(raw.decode(),old_dir,new_dir)
    if generated=='prepare-component.py':
        text=replace(text,"'patch-flatpak-app-ref41-draft.py',str(draft/","'"+new_dir+"/patch-app-ref.py',str(draft/")
        text=replace(text,"'verify-flatpak-mpv-package41-draft.py'","'"+new_dir+"/verify-component.py'")
        text=replace(text,'4ada6b113190b3cbf44ddaec16be03967fc05224c66ab89566cca94b5d8da0bf',metadata_hash)
        text=replace(text,"root/'code-file-policy.h']:","root/'code-file-policy.h',root/'flatpak-mpv-js-candidate-draft.md',root/'patch-flatpak-mpv-js-stream-draft.py']:")
    if generated=='verify-component.py':
        text=replace(text,"'code-file-policy.h']","'code-file-policy.h','flatpak-mpv-js-candidate-draft.md','patch-flatpak-mpv-js-stream-draft.py']")
    if generated!='patch-app-ref.py':
        text=replace(text,'usr/share/doc/confos-code-readers/mpv41','usr/share/doc/confos-code-readers/mpv41-js')
    ast.parse(text)
    (out/generated).write_text(text)
(out/'alternate-recipe-provenance.json').write_text(json.dumps({'original_recipe_inputs_sha256':inputs,'original_metadata_sha256':hashlib.sha256(old).hexdigest(),'alternate_metadata_sha256':metadata_hash,'candidate_sha256':expected,'generated_scripts_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.py')},'composition_executed':False},indent=2)+'\n')
print('ALTERNATE_JS_METADATA_AND_SEALED40_GATED_RECIPE_PREPARED',metadata_hash)
print('OLD_CANDIDATES_AND_DRAFT_UNCHANGED; NO_PACKAGE_COMPOSITION_OR_GUEST_RUN')

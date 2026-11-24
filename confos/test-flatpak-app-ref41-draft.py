#!/usr/bin/python3
"""Exercise app-ref widening without changing the live implementation."""
import ast,importlib.util,json,tempfile
from pathlib import Path
loader=importlib.util.spec_from_file_location('draft_patch','patch-flatpak-app-ref41-draft.py')
module=importlib.util.module_from_spec(loader);loader.loader.exec_module(module)
source=Path('flatpak_readers.py').read_text();patched=module.patched(source)
assert len([line for line in patched.splitlines() if '(?:runtime|app)' in line])==1
namespace={};exec(compile(patched,'private-flatpak-readers','exec'),namespace)
with tempfile.TemporaryDirectory(prefix='mpv41-validation-',dir='.') as temp:
    root=Path(temp);manifest=root/namespace['MANIFEST'];manifest.parent.mkdir(parents=True)
    item=dict(ref='app/io.mpv.Mpv/x86_64/stable',commit='a'*64,bundle_sha256='b'*64,
              original_sha256='c'*64,sha256='d'*64,target='bin/mpv',payload='mpv41-0.gz',mode=0o755,
              objects=['repo/objects/ab/'+'e'*62+'.file'])
    for ref in ('app/io.mpv.Mpv/x86_64/stable','runtime/org.freedesktop.Platform/x86_64/26.08'):
        manifest.write_text(json.dumps([dict(item,ref=ref)]));assert len(namespace['_items'](root))==1
    invalid={'ref':['app/../x86_64/stable','runtime/../x86_64/stable','app/io.mpv.Mpv/x86_64/..','app/io.mpv.Mpv/aarch64/stable','app/io.mpv.Mpv/x86_64/../stable','app/io.mpv.Mpv/x86_64/stable/extra','extension/io.mpv.Mpv/x86_64/stable'],
             'commit':['a'*63], 'bundle_sha256':['B'*64], 'target':['../bin/mpv','/bin/mpv'],
             'payload':['../x.gz'],'mode':[0o644], 'objects':[[],['repo/objects/../../x.file']]}
    for key,values in invalid.items():
        for value in values:
            manifest.write_text(json.dumps([dict(item,**{key:value})]))
            try: namespace['_items'](root)
            except ValueError: pass
            else: raise AssertionError((key,value))
for name in ('inspect-flatpak-mpv-integration41-draft.py','patch-flatpak-app-ref41-draft.py','prepare-flatpak-mpv-package41-draft.py','verify-flatpak-mpv-package41-draft.py'):
    ast.parse(Path(name).read_text())
print('PRIVATE_APP_AND_RUNTIME_REF_ALLOWLIST_AND_EXISTING_STRICT_VALIDATION_PASS')

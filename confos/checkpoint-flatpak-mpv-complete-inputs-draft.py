#!/usr/bin/python3
"""Checksum retained exact inputs before any disposable compiler output cleanup."""
import hashlib
import json
from pathlib import Path
root=Path.cwd()
work=root/'interpreter-inputs/flatpak-mpv-lua-candidate'
out=work/'continuation-publish'
sdk=work/'sdk-store/runtime/org.freedesktop.Sdk/x86_64/26.08/a1b744b072d9f55d061e35382547ae80dad8d92abecc1da7dc1818de2daabfd3'
def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        while chunk:=stream.read(1024*1024): h.update(chunk)
    return h.hexdigest()
def record(path):
    if path.is_symlink(): return {'symlink':str(path.readlink())}
    if path.is_file(): return {'sha256':digest(path)}
sdk_hashes={str(p.relative_to(sdk)):entry for p in sorted(sdk.rglob('*')) if (entry:=record(p)) is not None}
(out/'sdk-input-checksums.json').write_text(json.dumps(sdk_hashes,indent=2)+'\n')
paths=list((work/'dev-sources').glob('*'))
paths += [root/'interpreter-inputs/flatpak-readers'/name for name in ('mpv.tar.gz','luajit.tar.gz','mujs.tar.gz')]
paths += list((work/'mpv').rglob('*'))
paths += list((work/'development-overlay').rglob('*'))
paths += list(root.glob('*flatpak-mpv*draft*py'))
paths += [root/'code-file-policy.h',root/'patch-luajit-code.py',work/'luajit/.relver']
inputs={str(p.relative_to(root)):entry for p in sorted(set(paths)) if (entry:=record(p)) is not None}
(out/'complete-input-checksums.json').write_text(json.dumps(inputs,indent=2)+'\n')
print('ALL_SDK_SOURCE_HEADER_INPUTS_CHECKSUMMED',len(sdk_hashes),len(inputs),flush=True)
print('SDK_CHECKSUM_MANIFEST_SHA256',digest(out/'sdk-input-checksums.json'),flush=True)
print('SOURCE_HEADER_CHECKSUM_MANIFEST_SHA256',digest(out/'complete-input-checksums.json'),flush=True)

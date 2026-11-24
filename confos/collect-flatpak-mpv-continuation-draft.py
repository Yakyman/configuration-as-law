#!/usr/bin/python3
"""Preserve portable candidate/header/build evidence; no shared package mutation."""
import hashlib
import json
from pathlib import Path
root=Path.cwd()
work=root/'interpreter-inputs/flatpak-mpv-lua-candidate'
out=work/'continuation-publish'
out.mkdir(exist_ok=True)
files=list((root/'logs').glob('flatpak-mpv-*-cont*.log'))
files += [root/'logs/flatpak-mpv-candidate-compile.log',root/'logs/flatpak-mpv-candidate-compile2.log',root/'logs/flatpak-mpv-complete-runtime.log']
files += list(work.glob('*-development-provenance.json')) + list(work.glob('*-abi.txt'))
files += [work/'mpv-candidate-comparison.json',work/'mpv-dynamic-abi-comparison.json']
for path in files:
    if path.exists(): (out/path.name).write_text(path.read_text().replace(str(root),'<build>'))
build=work/'mpv-zimg-configure'
for name,relative in [('mpv-final-config.h','config.h'),('mpv-build-options.json','meson-info/intro-buildoptions.json'),('mpv-build-compilers.json','meson-info/intro-compilers.json'),('mpv-final-meson.log','meson-logs/meson-log.txt')]:
    path=build/relative
    if path.exists(): (out/name).write_text(path.read_text().replace(str(root),'<build>'))
paths=list((work/'development-overlay').rglob('*'))+list((work/'candidate').glob('*'))
paths += [work/'mpv'/p for p in ('player/lua.c','stream/stream.c','stream/stream.h','stream/stream_file.c','stream/confos-code-policy.h')]
hashes={str(p.relative_to(work)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}
(out/'continuation-file-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
print('PORTABLE_CONTINUATION_EVIDENCE_READY',len(files),len(hashes),flush=True)

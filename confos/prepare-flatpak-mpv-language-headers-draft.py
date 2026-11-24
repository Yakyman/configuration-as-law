#!/usr/bin/python3
"""Restore exact retained language headers, without building either interpreter."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

recipe=Path('prepare-flatpak-mpv-dependency-headers-draft.py').read_text()
exec(recipe[recipe.index('root = Path.cwd()'):recipe.index('import sys')])
overlay=work/'development-overlay'
exec(recipe[recipe.index('base = '):recipe.index('module=entry')])
archive=root/'interpreter-inputs/flatpak-readers/mujs.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='c7abfce241eb5f0b45bddf4b99e112a0661e2119e432931de5dc8fddab1a9c4a'
source=work/'mujs-development-source'
source.mkdir(exist_ok=True)
subprocess.run(['tar','-xf',str(archive),'--strip-components=1','-C',str(source)],check=True)
header=(source/'mujs.h').read_text()
version='.'.join(re.search(r'#define JS_VERSION_'+x+r' (\d+)',header)[1] for x in ('MAJOR','MINOR','PATCH'))
print('MUJS_ORIGINAL_MODULE',json.dumps(find(manifest,'mujs')),flush=True)
print('MUJS_HEADER_VERSION',version,flush=True)
run(['make','-j1','build/release/mujs.pc','prefix=/app','VERSION='+version])
shutil.copyfile(source/'mujs.h',overlay/'include/mujs.h')
shutil.copyfile(source/'build/release/mujs.pc',overlay/'lib/pkgconfig/mujs.pc')
luajit=work/'luajit'
shutil.copyfile(luajit/'.relver',luajit/'src/luajit_relver.txt')
subprocess.run(base+['--chdir','/work/luajit/src','/work/candidate/luajit','host/genversion.lua'],check=True)
destination=overlay/'include/luajit-2.1'
destination.mkdir(exist_ok=True)
for name in ('lua.h','lualib.h','lauxlib.h','luaconf.h','lua.hpp','luajit.h'):
    shutil.copyfile(luajit/'src'/name,destination/name)
# Same substitutions as the exact upstream Makefile's SED_PC installation rule.
pc=(luajit/'etc/luajit.pc').read_text().replace('prefix=/usr/local','prefix=/app').replace('relver=ROLLING','relver=1781966178')
(overlay/'lib/pkgconfig/luajit.pc').write_text(pc)
command=['meson','setup','/work/mpv-language-configure','/work/mpv','--prefix=/app','--libdir=lib','--wrap-mode=nofallback','-Dbackend_max_links=1',*find(manifest,'mpv')['config-opts']]
print('ORIGINAL_FEATURE_MPV_CONFIGURE',json.dumps(command),flush=True)
result=subprocess.run(base+command)
print('MPV_CONFIGURE_STATUS',result.returncode,flush=True)

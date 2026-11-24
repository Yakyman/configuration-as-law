#!/usr/bin/python3
"""Exact public headers and dynamic-only metadata; no private/static closure claimed."""
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
source=work/'libbluray-development-source'
assert hashlib.sha256((work/'dev-sources/libbluray.archive').read_bytes()).hexdigest()=='f676408e91a5d321abf8b8d4dfdae36205c297dab5c54c3ec519639025f474a2'
definition=(source/'src/libbluray/meson.build').read_text()
paths=re.findall(r"'([^']+\.h)'",definition.split('# Copy headers')[0])
destination=overlay/'include/libbluray'
destination.mkdir(exist_ok=True)
for name in paths: shutil.copyfile(source/'src/libbluray'/name,destination/Path(name).name)
project=(source/'meson.build').read_text()
version=re.search(r"version:\s*'([0-9.]+)'",project)[1]
header=(source/'src/libbluray/bluray-version.h.in').read_text()
for key,value in zip(('MAJOR','MINOR','MICRO'),version.split('.')):
    header=header.replace('@BLURAY_VERSION_'+key+'@',value)
assert '@BLURAY_VERSION_' not in header
(destination/'bluray-version.h').write_text(header)
(overlay/'lib/pkgconfig/libbluray.pc').write_text('prefix=/app\nlibdir=${prefix}/lib\nincludedir=${prefix}/include\nName: libbluray\nDescription: library supporting Blu-ray playback\nVersion: '+version+'\nLibs: -L${libdir} -lbluray\nCflags: -I${includedir}\n')
print('PUBLIC_HEADERS_FROM_EXACT_UPSTREAM_INSTALL_DEFINITION',paths,version,flush=True)
print('DYNAMIC_ONLY_METADATA; private/static dependencies intentionally unspecified; original library unchanged',flush=True)
command=['meson','setup','/work/mpv-bluray-public-configure','/work/mpv','--prefix=/app','--libdir=lib','--wrap-mode=nofallback','-Dbackend_max_links=1',*find(manifest,'mpv')['config-opts']]
print('ORIGINAL_FEATURE_MPV_CONFIGURE',json.dumps(command),flush=True)
result=subprocess.run(base+command)
print('MPV_CONFIGURE_STATUS',result.returncode,flush=True)

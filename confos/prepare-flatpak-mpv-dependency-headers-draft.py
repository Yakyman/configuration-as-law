#!/usr/bin/python3
"""Bounded pinned libplacebo development generation; original shared library retained."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

root = Path.cwd()
work = root/'interpreter-inputs/flatpak-mpv-lua-candidate'
sdk = work/'sdk-store/runtime/org.freedesktop.Sdk/x86_64/26.08/a1b744b072d9f55d061e35382547ae80dad8d92abecc1da7dc1818de2daabfd3/files'
app = root/'interpreter-inputs/flatpak-analysis/root/usr/lib/confos/flatpak/app/io.mpv.Mpv/x86_64/stable/13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc/files'
import sys
name = sys.argv[1]
entry = next(x for x in json.loads((work/'dev-sources/manifest.json').read_text()) if x['name']==name)
source=work/(name+'-development-source')
assert not source.exists()
archive=work/'dev-sources'/(name+'.archive')
assert hashlib.sha256(archive.read_bytes()).hexdigest()==entry['sha256']
source.mkdir()
subprocess.run(['tar','-xf',str(archive),'--strip-components=1','-C',str(source)],check=True)
overlay=work/'development-overlay'
base = ['bwrap', '--unshare-all', '--die-with-parent', '--clearenv', '--ro-bind', str(sdk), '/usr',
        '--ro-bind', str(app), '/app', '--bind', str(work), '/work',
        '--bind', str(overlay/'include'), '/app/include',
        '--bind', str(overlay/'lib/pkgconfig'), '/app/lib/pkgconfig',
        '--bind', str(overlay/'share/pkgconfig'), '/app/share/pkgconfig',
        '--symlink', 'usr/bin', '/bin', '--symlink', 'usr/lib', '/lib', '--symlink', 'usr/lib64', '/lib64',
        '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp',
        '--setenv', 'PATH', '/usr/bin:/app/bin', '--setenv', 'HOME', '/tmp', '--setenv', 'LC_ALL', 'C',
        '--setenv', 'SOURCE_DATE_EPOCH', '1795392000',
        '--setenv', 'PKG_CONFIG_PATH', '/app/lib/pkgconfig:/app/share/pkgconfig',
        '--setenv', 'LD_LIBRARY_PATH', '/app/lib:/usr/lib/x86_64-linux-gnu']
manifest = json.loads((app/'manifest.json').read_text())
def find(value, name):
    if isinstance(value, dict):
        if value.get('name') == name:
            return value
        for child in value.values():
            if found := find(child, name):
                return found
    elif isinstance(value, list):
        for child in value:
            if found := find(child, name):
                return found


def run(command):
    print('NATIVE_DEVELOPMENT_COMMAND',json.dumps(command),flush=True)
    subprocess.run(base+['--chdir','/work/'+source.name,*command],check=True)
module=entry['module']
if module.get('buildsystem','autotools')=='autotools':
    if not (source/'configure').exists(): run(['autoreconf','-vif'])
    run(['./configure','--prefix=/app','--libdir=/app/lib',*module.get('config-opts',[])])
    run(['make','-j2','install-data','DESTDIR=/work/'+name+'-development-install'])
else:
    raise ValueError('unsupported native metadata stage')
installed=work/(name+'-development-install/app')
for directory in ('include','lib/pkgconfig','share/pkgconfig'):
    if (installed/directory).exists(): shutil.copytree(installed/directory,overlay/directory,dirs_exist_ok=True)
provenance={'source':entry,'installed':{str(p.relative_to(installed)):hashlib.sha256(p.read_bytes()).hexdigest() for p in installed.rglob('*') if p.is_file()}}
(work/(name+'-development-provenance.json')).write_text(json.dumps(provenance,indent=2)+'\n')
command=['meson','setup','/work/mpv-'+name+'-configure','/work/mpv','--prefix=/app','--libdir=lib','--wrap-mode=nofallback','-Dbackend_max_links=2',*find(manifest,'mpv')['config-opts']]
print('ORIGINAL_FEATURE_MPV_CONFIGURE',json.dumps(command),flush=True)
result=subprocess.run(base+command)
print('MPV_CONFIGURE_STATUS',result.returncode,flush=True)

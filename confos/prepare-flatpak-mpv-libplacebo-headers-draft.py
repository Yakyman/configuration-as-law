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
source = work/'libplacebo-source'
archive = work/'dev-sources/libplacebo.archive'
expected = '63251b5af660e264abcf70b2d4dbadc5817443e3d10a6e03f03d4f0647b48ac6'
assert hashlib.sha256(archive.read_bytes()).hexdigest() == expected
assert not source.exists(), 'fresh source required'
source.mkdir()
subprocess.run(['tar', '-xf', str(archive), '--strip-components=1', '-C', str(source)], check=True)
submodules = json.loads((work/'dev-sources/libplacebo-submodules.json').read_text())
for entry in submodules['sources']:
    archive_path = work/'dev-sources'/('libplacebo-'+entry['name']+'.archive')
    assert hashlib.sha256(archive_path.read_bytes()).hexdigest() == entry['sha256']
    destination = source/'3rdparty'/entry['name']
    destination.mkdir(parents=True, exist_ok=True)
    subprocess.run(['tar', '-xf', str(archive_path), '--strip-components=1', '-C', str(destination)], check=True)
overlay = work/'development-overlay'
original = {str(p.relative_to(app)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (app/'lib').glob('libplacebo.so*') if p.is_file()}
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

options = find(manifest, 'libplacebo')['config-opts']
command = ['meson', 'setup', '/work/libplacebo-header-build', '/work/libplacebo-source',
           '--prefix=/app', '--libdir=lib', '--wrap-mode=nofallback', '-Dbackend_max_links=2', *options]
print('ORIGINAL_LIBPLACEBO_CONFIGURE', json.dumps(command), flush=True)
result = subprocess.run(base+command)
print('LIBPLACEBO_CONFIGURE_STATUS', result.returncode, flush=True)
evidence = work/'libplacebo-header-evidence'
evidence.mkdir(exist_ok=True)
for relative in ('.gitmodules', 'src/opengl/include/glad/meson.build',
                 'src/include/libplacebo/config.h.in', 'src/include/libplacebo/meson.build'):
    destination = evidence/relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source/relative, destination)
shutil.copytree(work/'libplacebo-header-build/meson-logs', evidence/'meson-logs', dirs_exist_ok=True)
if result.returncode == 0:
    plan = subprocess.check_output(base+['meson', 'introspect', '--install-plan', '/work/libplacebo-header-build'], text=True)
    (work/'libplacebo-install-plan.json').write_text(plan)
    subprocess.run(base+['meson', 'install', '-C', '/work/libplacebo-header-build', '--no-rebuild',
                         '--tags', 'devel', '--destdir', '/work/libplacebo-header-install'], check=True)
    installed = work/'libplacebo-header-install/app'
    config = work/'libplacebo-header-build/src/include/libplacebo/config.h'
    assert config.is_file()
    destination = installed/'include/libplacebo/config.h'
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(config, destination)
    print('GENERATED_PUBLIC_CONFIG', config.read_text(), flush=True)
    for directory in ('include', 'lib/pkgconfig'):
        shutil.copytree(installed/directory, overlay/directory, dirs_exist_ok=True)
    options = find(manifest, 'mpv')['config-opts']
    command = ['meson', 'setup', '/work/mpv-libplacebo-configure', '/work/mpv', '--prefix=/app',
               '--wrap-mode=nofallback', '-Dbackend_max_links=2', *options]
    print('ORIGINAL_FEATURE_MPV_CONFIGURE', json.dumps(command), flush=True)
    result = subprocess.run(base+command)
    print('MPV_CONFIGURE_STATUS', result.returncode, flush=True)
for relative, digest in original.items():
    assert hashlib.sha256((app/relative).read_bytes()).hexdigest() == digest
provenance = {'archive_sha256': expected, 'original_options': find(manifest, 'libplacebo')['config-opts'],
              'original_library_sha256': original, 'last_configure_status': result.returncode, 'submodules': submodules}
(work/'libplacebo-headers-provenance.json').write_text(json.dumps(provenance, indent=2)+'\n')
print('ORIGINAL_LIBPLACEBO_OBJECTS_UNCHANGED', len(original), flush=True)
print('BOUNDED_LIBPLACEBO_STAGE_COMPLETE; no library or mpv executable compiled', flush=True)

# Failed configure trees contain disposable compiler checks only.
if not (work/'libplacebo-header-install').exists():
    shutil.rmtree(work/'libplacebo-header-build')
    shutil.rmtree(source)

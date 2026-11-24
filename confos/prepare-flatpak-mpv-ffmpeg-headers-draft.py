#!/usr/bin/python3
"""Bounded development metadata recovery; never rebuild or replace FFmpeg libs."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

root = Path.cwd()
work = root/'interpreter-inputs/flatpak-mpv-lua-candidate'
sdk = work/'sdk-store/runtime/org.freedesktop.Sdk/x86_64/26.08/a1b744b072d9f55d061e35382547ae80dad8d92abecc1da7dc1818de2daabfd3/files'
app = root/'interpreter-inputs/flatpak-analysis/root/usr/lib/confos/flatpak/app/io.mpv.Mpv/x86_64/stable/13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc/files'
source = work/'ffmpeg-headers-source'
archive = work/'dev-sources/ffmpeg.archive'
expected = '979e06585856b823e07a94bb9560106e4eb73ac7d061000556e2484270afc09c'
assert hashlib.sha256(archive.read_bytes()).hexdigest() == expected
if source.exists():
    raise ValueError('fresh bounded header generation required; source path already exists')
source.mkdir()
subprocess.run(['tar', '-xf', str(archive), '--strip-components=1', '-C', str(source)], check=True)
configure = (source/'configure').read_text()
assert 'HAVE_LIST_PUB="\n    bigendian\n    fast_unaligned\n"' in configure
print('PUBLIC_GENERATED_CONFIG: bigendian and fast_unaligned only', flush=True)
overlay = work/'development-overlay'
for directory in ('include', 'lib/pkgconfig', 'share/pkgconfig'):
    (overlay/directory).mkdir(parents=True, exist_ok=True)
    if (app/directory).exists():
        shutil.copytree(app/directory, overlay/directory, dirs_exist_ok=True, symlinks=True)
original_libraries = {str(p.relative_to(app)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for pattern in ('lib/libav*.so.*', 'lib/libsw*.so.*') for p in app.glob(pattern) if p.is_file()}
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
# These options control ONLY generation of installed development metadata.
# Public avconfig macros are verified below. No library/program is built.
arguments = ['./configure', '--prefix=/app', '--disable-everything', '--disable-autodetect',
             '--disable-programs', '--disable-doc', '--enable-shared', '--disable-static']
print('HEADER_GENERATION_ONLY_CONFIG', json.dumps(arguments), flush=True)
subprocess.run(base+['--chdir', '/work/ffmpeg-headers-source', *arguments], check=True)
subprocess.run(base+['--chdir', '/work/ffmpeg-headers-source', 'make', '-j2',
                    'install-headers', 'DESTDIR=/work/ffmpeg-header-install'], check=True)
installed = work/'ffmpeg-header-install/app'
avconfig = (installed/'include/libavutil/avconfig.h').read_text()
print('GENERATED_AVCONFIG', avconfig, flush=True)
assert '#define AV_HAVE_BIGENDIAN 0' in avconfig
assert '#define AV_HAVE_FAST_UNALIGNED 1' in avconfig
# Verify the original objects are little-endian x86-64, the public-header target.
for relative, digest in original_libraries.items():
    payload = (app/relative).read_bytes()
    assert payload[:6] == b'\x7fELF\x02\x01' and int.from_bytes(payload[18:20], 'little') == 62
    assert hashlib.sha256(payload).hexdigest() == digest
for directory in ('include', 'lib/pkgconfig'):
    shutil.copytree(installed/directory, overlay/directory, dirs_exist_ok=True)
provenance = {'ffmpeg_archive_sha256': expected, 'metadata_only_configure': arguments,
              'original_library_sha256': original_libraries,
              'generated': {str(p.relative_to(installed)): hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in installed.rglob('*') if p.is_file()}}
(work/'ffmpeg-headers-provenance.json').write_text(json.dumps(provenance, indent=2)+'\n')
print('ORIGINAL_FFMPEG_OBJECTS_UNCHANGED', len(original_libraries), flush=True)
subprocess.run(base+['pkg-config', '--modversion', 'libavcodec', 'libavfilter', 'libavformat',
                    'libavutil', 'libavdevice', 'libswresample', 'libswscale'], check=True)
manifest = json.loads((app/'manifest.json').read_text())
def find(value):
    if isinstance(value, dict):
        if value.get('name') == 'mpv':
            return value
        for child in value.values():
            if found := find(child):
                return found
    elif isinstance(value, list):
        for child in value:
            if found := find(child):
                return found
options = find(manifest)['config-opts']
command = ['meson', 'setup', '/work/mpv-sdk-configure', '/work/mpv', '--prefix=/app',
           '--wrap-mode=nofallback', '-Dbackend_max_links=2', *options]
print('ORIGINAL_FEATURE_MPV_CONFIGURE', json.dumps(command), flush=True)
result = subprocess.run(base+command)
print('MPV_CONFIGURE_STATUS', result.returncode, flush=True)
for relative, digest in original_libraries.items():
    assert hashlib.sha256((app/relative).read_bytes()).hexdigest() == digest
print('BOUNDED_FFMPEG_HEADER_STAGE_COMPLETE; no FFmpeg library or mpv executable compiled', flush=True)

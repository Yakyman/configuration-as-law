#!/usr/bin/python3
"""Fetch exact manifest sources needed to recover missing app development inputs."""
import hashlib
import json
from pathlib import Path
import urllib.request
import urllib.error
import io
import tarfile

base = Path('interpreter-inputs/flatpak-mpv-lua-candidate/dev-sources')
base.mkdir(exist_ok=True)
manifest = Path('interpreter-inputs/flatpak-analysis/root/usr/lib/confos/flatpak/app/io.mpv.Mpv/x86_64/stable/13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc/files/manifest.json')
names = {'ffmpeg', 'libplacebo', 'libass', 'libbluray', 'libdvdnav', 'libdvdread',
         'libcdio', 'libcdio-paranoia', 'rubberband', 'uchardet', 'zimg'}
modules = {}
def visit(value):
    if isinstance(value, dict):
        if value.get('name') in names:
            modules[value['name']] = value
        for child in value.values():
            visit(child)
    elif isinstance(value, list):
        for child in value:
            visit(child)
visit(json.loads(manifest.read_text()))
records = []
for name, module in modules.items():
    sources = module.get('sources', [])
    if len(sources) != 1:
        print('BLOCKED_COMPLEX_SOURCE', name, flush=True)
        continue
    source = sources[0]
    url = source['url']
    if source['type'] == 'git':
        pin = source['commit']
        if url.startswith('https://github.com/'):
            url = 'https://codeload.github.com/'+url.split('github.com/', 1)[1].removesuffix('.git')+'/tar.gz/'+pin
        elif url == 'https://git.ffmpeg.org/ffmpeg.git':
            # The gitweb snapshot endpoint returned an HTML anti-bot page.
            # Use the project's source mirror at the same exact commit.
            url = 'https://codeload.github.com/FFmpeg/FFmpeg/tar.gz/'+pin
        elif url.startswith('https://code.videolan.org/'):
            repo = url.removesuffix('.git')
            url = repo+'/-/archive/'+pin+'/'+repo.rsplit('/', 1)[-1]+'-'+pin+'.tar.gz'
        else:
            print('BLOCKED_GIT_ARCHIVE_MAPPING', name, url, flush=True)
            continue
    elif source['type'] != 'archive':
        print('BLOCKED_SOURCE_TYPE', name, source['type'], flush=True)
        continue
    target = base/(name+'.archive')
    try:
        if target.exists() and not tarfile.is_tarfile(target):
            print('REJECTED_NON_ARCHIVE', name, hashlib.sha256(target.read_bytes()).hexdigest(), flush=True)
            target.unlink()
        if not target.exists():
            with urllib.request.urlopen(url, timeout=30) as response:
                payload = response.read(100000001)
            if len(payload) > 100000000:
                raise ValueError('archive exceeds source-fetch limit')
            digest = hashlib.sha256(payload).hexdigest()
            if source.get('sha256', digest) != digest:
                raise ValueError('manifest source archive hash mismatch')
            try:
                with tarfile.open(fileobj=io.BytesIO(payload)) as archive:
                    archive.getmembers()
            except tarfile.TarError as error:
                raise ValueError('download is not a source archive') from error
            target.write_bytes(payload)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if source.get('sha256', digest) != digest:
            raise ValueError('retained source archive hash mismatch')
        records.append({'name': name, 'archive_url': url, 'sha256': digest, 'module': module})
        print('SOURCE_RETAINED', name, digest, url, flush=True)
    except (urllib.error.URLError, ValueError) as error:
        print('BLOCKED_SOURCE', name, url, str(error), flush=True)
(base/'manifest.json').write_text(json.dumps(records, indent=2)+'\n')
print('SOURCE_FETCH_COUNT', len(records), 'OF', len(modules), flush=True)

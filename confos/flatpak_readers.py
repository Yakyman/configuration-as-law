"""Exact-component Flatpak reader overrides; preserve immutable input objects."""
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

MANIFEST = 'usr/lib/confos/flatpak-reader-overrides/manifest.json'
def digest(data):
    return hashlib.sha256(data).hexdigest()

def _items(root):
    p = Path(root)/MANIFEST
    if not p.exists():
        return []
    items = json.loads(p.read_text())
    if not isinstance(items, list):
        raise ValueError('invalid Flatpak reader manifest')
    for item in items:
        if not re.fullmatch(r'(?:runtime|app)/(?![.]{1,2}/)[A-Za-z0-9_.-]+/x86_64/(?![.]{1,2}$)[A-Za-z0-9_.-]+', item['ref']):
            raise ValueError('invalid reader app/runtime ref')
        for key in ('commit', 'bundle_sha256', 'original_sha256', 'sha256'):
            if not re.fullmatch('[0-9a-f]{64}', item[key]):
                raise ValueError('invalid reader digest')
        target = Path(item['target'])
        if target.is_absolute() or '..' in target.parts or not target.parts:
            raise ValueError('invalid reader target')
        if not re.fullmatch('[A-Za-z0-9_.-]+[.]gz', item['payload']) or item['mode'] != 0o755:
            raise ValueError('invalid reader payload or mode')
        if not item['objects'] or any(not re.fullmatch(r'repo/objects/[0-9a-f]{2}/[0-9a-f]{62}[.]file', x) for x in item['objects']):
            raise ValueError('invalid reader original object')
    return items

def _regular(base, relative):
    p = base/relative
    if not p.is_file() or p.is_symlink() or not p.resolve().is_relative_to(base.resolve()):
        raise ValueError('reader override requires contained regular file')
    return p

def apply(root, store, ref, commit, bundle_sha256):
    """Called after native bundle deployment validation, before store relocation."""
    root, store = Path(root), Path(store)
    if not store.resolve().is_relative_to(root.resolve()):
        raise ValueError('Flatpak store outside assembled root')
    prepared = []
    targets = set()
    for item in _items(root):
        if (item['ref'], item['commit']) != (ref, commit):
            continue
        # The ref and the OSTree commit identify the deployed content; two exports of one
        # commit differ as bundle files (up to 0.48 only the export named in the manifest
        # was accepted, and a declaration naming another export could not be built).
        # The bytes replaced are still checked object by object below.
        relative = str(Path(ref)/commit/'files'/item['target'])
        if relative in targets:
            raise ValueError('duplicate Flatpak reader target')
        targets.add(relative)
        target = _regular(store, relative)
        if digest(target.read_bytes()) != item['original_sha256']:
            raise ValueError('Flatpak reader original checksum mismatch')
        for obj in item['objects']:
            original = _regular(store, obj)
            if digest(original.read_bytes()) != item['original_sha256'] or not os.path.samefile(target, original):
                raise ValueError('Flatpak reader original object identity mismatch')
        payload = _regular(root/Path(MANIFEST).parent, item['payload'])
        data = gzip.decompress(payload.read_bytes())
        if digest(data) != item['sha256']:
            raise ValueError('Flatpak reader payload checksum mismatch')
        prepared.append((target, data, item['mode']))
    # All inputs checked before any mutation. Failure discards the staged root.
    for target, data, mode in prepared:
        fd, name = tempfile.mkstemp(prefix='.confos-reader-', dir=target.parent)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
                os.fchmod(stream.fileno(), mode)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, target)
            directory = os.open(target.parent, os.O_RDONLY | os.O_DIRECTORY)
            try: os.fsync(directory)
            finally: os.close(directory)
        finally:
            if os.path.exists(name): os.unlink(name)
    return denial_paths(root, store)

def denial_paths(root, store=None):
    """Derive exact original-object restrictions from installed component inputs."""
    root = Path(root)
    store = Path(store) if store is not None else root/'usr/lib/confos/flatpak'
    paths = set()
    if not store.exists():
        return []
    for item in _items(root):
        target = store/item['ref']/item['commit']/'files'/item['target']
        if not target.exists():
            continue
        target = _regular(store, target.relative_to(store))
        if digest(target.read_bytes()) != item['sha256']:
            raise ValueError('Flatpak reader replacement checksum mismatch')
        for obj in item['objects']:
            original = _regular(store, obj)
            if digest(original.read_bytes()) != item['original_sha256'] or os.path.samefile(target, original):
                raise ValueError('Flatpak reader original object changed or still linked')
            for prefix in ('/usr/lib/confos/flatpak/', '/run/host/usr/lib/confos/flatpak/'):
                paths.add(prefix+obj)
    return sorted(paths)

def policy(root):
    # Paths are generated solely from strict hex object names above.
    return ''.join('  deny "'+p+'" mx,\n' for p in denial_paths(root))


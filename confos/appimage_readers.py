"""Apply original-component byte overrides for an exact declared AppImage digest."""
import gzip
import hashlib
import json
from pathlib import Path

def apply(root, appdir, archive_digest):
    root, appdir = Path(root), Path(appdir)
    directory = root/'usr/lib/confos/appimage-reader-overrides'
    manifest = directory/'manifest.json'
    if not manifest.is_file():
        return
    for item in json.loads(manifest.read_text()):
        if item['archive_sha256'] != archive_digest:
            continue
        target, payload = Path(item['target']), Path(item['payload'])
        if (target.is_absolute() or '..' in target.parts or not target.parts
                or payload.is_absolute() or len(payload.parts) != 1 or payload.name in ('.', '..')):
            raise ValueError('invalid AppImage reader override path')
        path = appdir/target
        if (not path.is_file() or path.is_symlink()
                or not path.resolve().is_relative_to(appdir.resolve())):
            raise ValueError('AppImage override requires an original regular file')
        if hashlib.sha256(path.read_bytes()).hexdigest() != item['original_sha256']:
            raise ValueError('AppImage override original checksum mismatch')
        data = gzip.decompress((directory/payload).read_bytes())
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError('AppImage override payload checksum mismatch')
        path.write_bytes(data)
        path.chmod(item['mode'])

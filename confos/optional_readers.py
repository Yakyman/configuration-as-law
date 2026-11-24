"""Apply declared component's byte-exact reader overrides to installed packages.

The original component carries compressed payloads and a declarative manifest.
An override is active only when its Debian package is selected. A removed package
does not leave its executable behind merely because enforcement is available.
"""
import gzip
import hashlib
import json
from pathlib import Path

def apply(root, package_names):
    root = Path(root)
    directory = root/'usr/lib/confos/reader-overrides'
    manifest = directory/'manifest.json'
    if not manifest.exists():
        return
    for item in json.loads(manifest.read_text()):
        if item['package'] not in package_names:
            continue
        target = Path(item['target'])
        payload = Path(item['payload'])
        if (not target.is_absolute() or '..' in target.parts or payload.is_absolute()
                or len(payload.parts) != 1 or payload.name in ('.', '..')):
            raise ValueError('invalid reader override pathname')
        data = gzip.decompress((directory/payload).read_bytes())
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError('reader override checksum mismatch')
        path = root/str(target).lstrip('/')
        if not path.is_file() or path.is_symlink():
            raise ValueError('reader override requires the original package file: '+str(target))
        original = item.get('original_sha256')
        if original is not None and hashlib.sha256(path.read_bytes()).hexdigest() != original:
            raise ValueError('reader override original checksum mismatch: '+str(target))
        path.write_bytes(data)
        path.chmod(item['mode'])

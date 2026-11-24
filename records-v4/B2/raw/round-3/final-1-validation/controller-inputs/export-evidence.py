#!/usr/bin/env python3
"""Publish completed saved evidence; never starts a guest or changes a test."""
import hashlib
import io
import json
from pathlib import Path
import tarfile
import time

root = Path(__file__).resolve().parent.parent
raw = root / 'raw/round-0'
assert (raw / 'summary.json').is_file(), 'baseline must have finished'
archive = root / 'evidence-publication.tar.gz'
assert not archive.exists(), 'single-use publication export'
changes = []
inventory = []
replacements = [(str(root), '[stand-root]'), (str(Path.home()), '[host-home]')]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def add(bundle, name, data, mode=0o644):
    entry = tarfile.TarInfo(name)
    entry.size = len(data)
    entry.mode = mode
    entry.mtime = int(time.time())
    bundle.addfile(entry, io.BytesIO(data))

with tarfile.open(archive, 'w:gz', compresslevel=1) as bundle:
    for source, target, redact in ((raw, 'raw/round-0', True),
                                   (root/'channel-example', 'example', False)):
        if not source.exists():
            continue
        for path in sorted(source.rglob('*')):
            if not path.is_file():
                continue
            assert not path.is_symlink(), 'publication must contain ordinary files'
            name = str(Path(target)/path.relative_to(source))
            data = path.read_bytes()
            original = digest(data)
            try:
                text = data.decode('utf-8')
            except UnicodeDecodeError:
                text = None
            if text is not None:
                for old, new in replacements:
                    if old in text:
                        assert redact, 'complete declarations must remain byte-identical'
                        text = text.replace(old, new)
                data = text.encode('utf-8')
            published = digest(data)
            if original != published:
                changes.append({'file': name, 'original_sha256': original,
                                'published_sha256': published})
            inventory.append({'file': name, 'sha256': published, 'bytes': len(data)})
            add(bundle, name, data, path.stat().st_mode & 0o777)
    note = {
        'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'source': 'Completed new round-0 evidence; no previous-night raw logs copied',
        'normalization': 'Actual server task-root and account-home prefixes in text logs become [stand-root] and [host-home]; original server logs retained',
        'declaration_bytes_changed': False,
        'changed_files': changes,
        'published_files': inventory,
    }
    add(bundle, 'raw/round-0/publication.json', (json.dumps(note, indent=2, sort_keys=True)+'\n').encode())
print(json.dumps({'archive': archive.name, 'files': len(inventory),
                  'normalized_files': len(changes), 'bytes': archive.stat().st_size}))

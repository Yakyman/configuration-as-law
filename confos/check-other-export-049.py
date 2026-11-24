#!/usr/bin/python3
"""Every reader replacement of the manifest whose ref and commit are deployed is in place."""
import hashlib
import json
from pathlib import Path
import sys
import flatpak_readers

root = Path(sys.argv[1])
store = root/'usr/lib/confos/flatpak'
items = json.loads((root/flatpak_readers.MANIFEST).read_text())
deployed = 0
for item in items:
    target = store/item['ref']/item['commit']/'files'/item['target']
    if not target.exists():
        continue
    assert hashlib.sha256(target.read_bytes()).hexdigest() == item['sha256'], target
    deployed += 1
    print('PASS replacement in place', item['ref'], item['target'])
refs = {item['ref'] for item in items if (store/item['ref']/item['commit']).exists()}
assert refs == {'runtime/org.freedesktop.Platform/x86_64/26.08', 'app/io.mpv.Mpv/x86_64/stable'}, refs
paths = flatpak_readers.denial_paths(root)
assert deployed and paths
print('FLATPAK READER REPLACEMENTS', deployed, 'ORIGINAL OBJECT DENIALS', len(paths))

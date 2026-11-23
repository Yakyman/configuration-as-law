#!/usr/bin/env python3
"""Package completed server evidence; normalize only host identifiers in logs."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import tarfile
import time

p = argparse.ArgumentParser()
p.add_argument('root', type=Path)
p.add_argument('archive', type=Path)
p.add_argument('--transport-name', required=True)
a = p.parse_args()
root = a.root.resolve()
for relative in ('raw/round-4/rebuilt/summary.json',
                 'raw/round-4/rebuilt/regressions/summary.json',
                 'raw/round-4/combined/summary.json'):
    if json.loads((root/relative).read_text())['suite_exit'] != 0:
        raise SystemExit('refusing incomplete or failed final evidence')
sources = {
    'raw/round-4/rebuild-attempt-1': 'rebuild-attempt-1',
    'raw/round-4/rebuild-attempt-2': 'rebuild-attempt-2',
    'raw/round-4/rebuilt': 'rebuilt',
    'raw/round-4/combined': 'combined',
    'channel-example': 'example-export',
    'raw/final-suite-console.jsonl': 'final-suite-console.jsonl',
    'raw/combined-final-console.jsonl': 'combined-final-console.jsonl',
    'raw/assembly-final.json': 'assembly-final.json',
    'raw/final-build-provenance.json': 'final-build-provenance.json',
    'raw/build-factory-comparison.json': 'build-factory-comparison.json',
    'raw/final-validation-console.jsonl': 'final-validation-console.jsonl',
    'raw/rebuild-final.log': 'rebuild-final.log',
    'raw/recipe.log': 'recipe-final.log',
    '../round-4-peer/raw/rebuild-final.log': 'peer/rebuild-final.log',
    '../round-4-peer/raw/recipe.log': 'peer/recipe-final.log',
}
replacements = [(str(root.parent).encode(), b'stand'),
                (a.transport_name.encode(), b'the-host')]
manifest = {}
normalized = []
stamp = int(time.time())
with tarfile.open(a.archive, 'w:gz', compresslevel=1) as archive:
    def add(name, data):
        info = tarfile.TarInfo(name)
        info.size = len(data)
        info.mode = 0o644
        info.mtime = stamp
        archive.addfile(info, io.BytesIO(data))
    for source, destination in sources.items():
        path = root/source
        files = sorted(path.rglob('*')) if path.is_dir() else [path]
        for file in files:
            if not file.is_file():
                continue
            if file.is_symlink() or '__pycache__' in file.parts:
                raise SystemExit('unexpected non-source export member')
            name = str(Path(destination)/file.relative_to(path)) if path.is_dir() else destination
            original = file.read_bytes()
            if b'PRIVATE KEY-----' in original:
                raise SystemExit('private material must not be published')
            data = original
            for before, after in replacements:
                data = data.replace(before, after)
            if data != original:
                if file.name in ('machine.jsonl', 'base-files.json') or name.startswith('example-export/'):
                    raise SystemExit('declaration payload would require rewriting')
                normalized.append(name)
            manifest[name] = hashlib.sha256(data).hexdigest()
            add(name, data)
    add('publication-manifest.json', (json.dumps({
        'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(stamp)),
        'files_sha256': manifest,
        'host_identifier_normalization': normalized,
        'declaration_payloads_unchanged': True,
    }, indent=2, sort_keys=True)+'\n').encode())
print(json.dumps({'files': len(manifest), 'normalized_logs': normalized,
                  'archive_bytes': a.archive.stat().st_size}, sort_keys=True))

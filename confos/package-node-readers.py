#!/usr/bin/python3
"""Extend original component29 with source-built native Node/library payloads."""
from pathlib import Path
import gzip
import hashlib
import json
import os
import subprocess
import sys
import tempfile

version, baseline_name, tree_name, output_name = sys.argv[1:]
baseline, tree, output = map(Path, (baseline_name, tree_name, output_name))
if hashlib.sha256(baseline.read_bytes()).hexdigest() != '076ab98d393a2e1e08c3952f958c64716dd44a1e1d3d0df6872212a361dd264a':
    raise ValueError('baseline29 component checksum mismatch')
output = output.resolve()
output.parent.mkdir(parents=True, exist_ok=True)
epoch = 1795392000
with tempfile.TemporaryDirectory(prefix='node-readers-', dir=output.parent) as temp_name:
    temp = Path(temp_name)
    root = temp/'root'
    subprocess.run(['dpkg-deb', '-R', baseline, root], check=True)
    directory = root/'usr/lib/confos/reader-overrides'
    manifest = json.loads((directory/'manifest.json').read_text())
    for package, name, target, mode in [
        ('nodejs', 'node', '/usr/bin/node', 0o755),
        ('libnode115', 'libnode.so.115', '/usr/lib/x86_64-linux-gnu/libnode.so.115', 0o644)]:
        artifact = temp/name
        artifact.write_bytes((tree/'out/Release'/name).read_bytes())
        subprocess.run(['strip', '--strip-unneeded', artifact], check=True)
        data = artifact.read_bytes()
        payload = name+'.gz'
        (directory/payload).write_bytes(gzip.compress(data, compresslevel=9, mtime=epoch))
        manifest.append(dict(package=package, source_version='20.19.2+dfsg-1+deb13u3',
            target=target, payload=payload, mode=mode, sha256=hashlib.sha256(data).hexdigest()))
    (directory/'manifest.json').write_text(json.dumps(manifest, sort_keys=True, indent=2)+'\n')
    docs = root/'usr/share/doc/confos-code-readers'
    for name in ('patch-node-code.py', 'patch-node-metadata.py', 'patch-node-startup.py', 'harden-node-bindings.py',
                 'node-source.sha256', 'package-node-readers.py'):
        (docs/name).write_bytes(Path(name).read_bytes())
    (docs/'node-license').write_bytes((tree/'LICENSE').read_bytes())
    control = root/'DEBIAN/control'
    text = control.read_text()
    if 'Version: 0.29\n' not in text: raise ValueError('unexpected baseline version')
    control.write_text(text.replace('Version: 0.29\n', 'Version: '+version+'\n'))
    for path in [*root.rglob('*'), root]:
        if path.is_dir(): path.chmod(0o755)
        elif not path.is_symlink() and not path.stat().st_mode & 0o111: path.chmod(0o644)
        os.utime(path, (epoch, epoch), follow_symlinks=False)
    artifact = temp/'payload.deb'
    subprocess.run(['dpkg-deb', '--root-owner-group', '--uniform-compression', '-Zgzip', '-z9',
                    '--build', root, artifact], check=True,
                    env=dict(os.environ, SOURCE_DATE_EPOCH=str(epoch), TZ='UTC', LC_ALL='C'))
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    os.replace(artifact, output)
    output.with_suffix('.deb.sha256').write_text(digest+'\n')
    print(digest, output.name)

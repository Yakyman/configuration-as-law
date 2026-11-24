#!/usr/bin/python3
"""Compose original component30 and native Git reader/helper payloads."""
from pathlib import Path
import gzip
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile

version, baseline_name, tree_name, original_name, output_name = sys.argv[1:]
baseline, tree, original, output = map(Path, (baseline_name, tree_name, original_name, output_name))
assert hashlib.sha256(baseline.read_bytes()).hexdigest() == '2b68a0d6688c175eb3a94ac15f139c62707fdb0493a1a73e0a90531d65cfbc79'
assert hashlib.sha256(original.read_bytes()).hexdigest() == '3e35662fd5c46add561703e54031a1d8ad9df45811927689f0a51122b13be722'
targets = ['/usr/bin/'+n for n in ('git', 'git-shell', 'scalar')]
targets += ['/usr/lib/git-core/'+n for n in ('git', 'git-daemon', 'git-http-backend',
    'git-http-fetch', 'git-http-push', 'git-imap-send', 'git-remote-http',
    'git-sh-i18n--envsubst', 'git-shell', 'scalar')]
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['dpkg-deb', '--fsys-tarfile', original]))) as tar:
    elves = ['/'+m.name.removeprefix('./') for m in tar if m.isfile() and tar.extractfile(m).read(4) == b'\x7fELF']
    assert sorted(elves) == sorted(targets), elves
output = output.resolve()
output.parent.mkdir(parents=True, exist_ok=True)
epoch = 1795392000
with tempfile.TemporaryDirectory(prefix='git-readers-', dir=output.parent) as name:
    temp = Path(name)
    root = temp/'root'
    subprocess.run(['dpkg-deb', '-R', baseline, root], check=True)
    directory = root/'usr/lib/confos/reader-overrides'
    manifest = json.loads((directory/'manifest.json').read_text())
    payloads = {}
    for target in targets:
        command = Path(target).name
        if command not in payloads:
            artifact = temp/command
            artifact.write_bytes((tree/command).read_bytes())
            subprocess.run(['strip', '--strip-unneeded', artifact], check=True)
            data = artifact.read_bytes()
            payload = 'git-'+command+'.gz'
            (directory/payload).write_bytes(gzip.compress(data, compresslevel=9, mtime=epoch))
            payloads[command] = (payload, hashlib.sha256(data).hexdigest())
        payload, digest = payloads[command]
        manifest.append(dict(package='git', source_version='1:2.47.3-0+deb13u1',
                             target=target, payload=payload, mode=0o755, sha256=digest))
    (directory/'manifest.json').write_text(json.dumps(manifest, sort_keys=True, indent=2)+'\n')
    docs = root/'usr/share/doc/confos-code-readers'
    for name in ('patch-git-code.py', 'git-code-policy.h', 'git-source.sha256', 'package-git-readers.py'):
        (docs/name).write_bytes(Path(name).read_bytes())
    (docs/'git-license').write_bytes((tree/'COPYING').read_bytes())
    control = root/'DEBIAN/control'
    text = control.read_text()
    assert 'Version: 0.30\n' in text
    control.write_text(text.replace('Version: 0.30\n', 'Version: '+version+'\n'))
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

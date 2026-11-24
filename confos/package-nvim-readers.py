#!/usr/bin/python3
"""Compose original component31 and static exact-AppImage Neovim overrides."""
from pathlib import Path
import gzip
import hashlib
import json
import os
import struct
import subprocess
import sys
import tempfile

version, baseline_name, tree_name, image_name, output_name = sys.argv[1:]
baseline, tree, image, output = map(Path, (baseline_name, tree_name, image_name, output_name))
assert hashlib.sha256(baseline.read_bytes()).hexdigest() == '118d46f992ea680f057de39c9d1500567d640cf1a6a17c4deee5d1a79a91e049'
image_data = image.read_bytes()
image_digest = hashlib.sha256(image_data).hexdigest()
assert image_digest == 'd1b1488ef6a970dc3a2826b788d31d81b2f308ad42ef70ed62d35d0bf6189336'
offset = struct.unpack_from('<Q', image_data, 40)[0]
size, count = struct.unpack_from('<HH', image_data, 58)
offset += size*count
assert image_data[offset:offset+4] == b'hsqs'
output = output.resolve()
output.parent.mkdir(parents=True, exist_ok=True)
epoch = 1795392000
with tempfile.TemporaryDirectory(prefix='nvim-readers-', dir=output.parent) as name:
    temp = Path(name)
    root = temp/'root'
    subprocess.run(['dpkg-deb', '-R', baseline, root], check=True)
    directory = root/'usr/lib/confos/appimage-reader-overrides'
    directory.mkdir()
    binary = temp/'nvim'
    binary.write_bytes((tree/'build/bin/nvim').read_bytes())
    subprocess.run(['strip', '--strip-unneeded', binary], check=True)
    # Build-directory debug records must not survive stripping into a release.
    assert str(Path.cwd()).encode() not in binary.read_bytes()
    manifest = []
    for target, source, mode in [
        ('usr/bin/nvim', binary, 0o755),
        ('usr/share/nvim/runtime/lua/vim/loader.lua', tree/'runtime/lua/vim/loader.lua', 0o644),
        ('AppRun', Path('nvim-appimage-entry'), 0o755)]:
        original = subprocess.check_output(['unsquashfs', '-offset', str(offset), '-cat', image, target])
        data = source.read_bytes()
        payload = Path(target).name+'.gz'
        (directory/payload).write_bytes(gzip.compress(data, compresslevel=9, mtime=epoch))
        manifest.append(dict(archive_sha256=image_digest, target=target,
            original_sha256=hashlib.sha256(original).hexdigest(), payload=payload,
            mode=mode, sha256=hashlib.sha256(data).hexdigest()))
    (directory/'manifest.json').write_text(json.dumps(manifest, sort_keys=True, indent=2)+'\n')
    docs = root/'usr/share/doc/confos-code-readers'
    for name in ('patch-nvim-code.py', 'patch-luajit-code.py', 'nvim-source.sha256',
                 'package-nvim-readers.py', 'nvim-appimage-entry'):
        (docs/name).write_bytes(Path(name).read_bytes())
    (docs/'nvim-license').write_bytes((tree/'LICENSE.txt').read_bytes())
    dependencies = tree/'.deps/build/src'
    for source in sorted(dependencies.rglob('*')):
        if source.is_file() and source.name.startswith(('COPYING', 'COPYRIGHT', 'LICENSE')):
            target = docs/'nvim-dependency-licenses'/source.relative_to(dependencies)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
    control = root/'DEBIAN/control'
    text = control.read_text()
    assert 'Version: 0.31\n' in text
    control.write_text(text.replace('Version: 0.31\n', 'Version: '+version+'\n'))
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

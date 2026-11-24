#!/usr/bin/python3
"""Compose original reader package and source-built optional reader payloads.

No installed-system snapshot is an input. Original baseline package28 is fixed;
new payloads are from authenticated, patched Debian source trees.
"""
from pathlib import Path
import gzip
import hashlib
import json
import os
import subprocess
import sys
import tempfile

version, baseline_name, tools_name, output_name = sys.argv[1:]
baseline, work, output = map(Path, (baseline_name, tools_name, output_name))
baseline_hash = 'eb1c1ba68da7ce23a9420a42dd83522f1776f755dac450717edbcd26ce959edc'
if hashlib.sha256(baseline.read_bytes()).hexdigest() != baseline_hash:
    raise ValueError('baseline reader component checksum mismatch')
output = output.resolve()
output.parent.mkdir(parents=True, exist_ok=True)
epoch = 1795392000
with tempfile.TemporaryDirectory(prefix='optional-readers-', dir=output.parent) as temp_name:
    temp = Path(temp_name)
    root = temp/'root'
    subprocess.run(['dpkg-deb', '-R', baseline, root], check=True)
    directory = root/'usr/lib/confos/reader-overrides'
    directory.mkdir(parents=True)
    manifest = []
    inputs = [('dash', '0.5.12-12', 'dash/src/dash', 'dash'),
              ('mawk', '1.3.4.20250131-1', 'mawk/mawk', 'mawk'),
              ('gawk', '1:5.2.1-2', 'gawk/gawk', 'gawk'),
              ('sed', '4.9-2+deb13u1', 'sed/sed/sed', 'sed'),
              ('make', '4.4.1-2', 'make/make', 'make')]
    for package, source_version, relative, command in inputs:
        artifact = temp/command
        artifact.write_bytes((work/relative).read_bytes())
        subprocess.run(['strip', '--strip-unneeded', artifact], check=True)
        data = artifact.read_bytes()
        name = command+'.gz'
        (directory/name).write_bytes(gzip.compress(data, compresslevel=9, mtime=epoch))
        manifest.append(dict(package=package, source_version=source_version,
            target='/usr/bin/'+command, payload=name, mode=0o755,
            sha256=hashlib.sha256(data).hexdigest()))
    (directory/'manifest.json').write_text(json.dumps(manifest, sort_keys=True, indent=2)+'\n')
    docs = root/'usr/share/doc/confos-code-readers'
    for name in ('patch-tools-code.py', 'patch-make-code.py', 'make-code-policy.h',
                 'tools-source.sha256', 'package-optional-readers.py'):
        (docs/name).write_bytes(Path(name).read_bytes())
    for name in ('dash', 'mawk', 'gawk', 'sed', 'make'):
        license_file = work/name/'COPYING'
        if not license_file.exists(): license_file = work/name/'COPYING.LIB'
        (docs/(name+'-license')).write_bytes(license_file.read_bytes())
    control = root/'DEBIAN/control'
    text = control.read_text().replace('Version: 0.28\n', 'Version: '+version+'\n')
    text = text.replace('Description: ConfOS Bash, Python, Perl and BusyBox code-input enforcement',
                        'Description: ConfOS native code-input enforcement with optional readers')
    control.write_text(text)
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

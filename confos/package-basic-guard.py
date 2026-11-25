#!/usr/bin/python3
"""Add the guard of the office suite's Basic interpreter to the reader component.

Usage: package-basic-guard.py VERSION BASELINE.deb INPUT_DIR OUTPUT.deb
BASELINE.deb is the reader component of the previous release. INPUT_DIR is the output of
fetch-basic-library.py (the merged core library of every pinned release of libreoffice-core,
taken from the pinned archive). basic-guard.json, written by locate-basic-step.py, gives for
every release the file offset of SbiRuntime::Step(), the three bytes found there and the
three that replace them (`xor %eax,%eax; ret`: the function reports "do not go on" and
executes no instruction of Basic), and the checksum of the result.

The component receives one record of the reader-override manifest (INTERFACE.md, revision 29)
with the complete guarded library of the release `payload_release` of basic-guard-inputs.json
as its payload, so that this file follows from the component by checksum. For the other
releases the record lists the replacement itself (`other_releases`); optional_readers.py makes
it in the file of that release at assembly. A release that the record does not list is
refused (`unlisted_release`).
"""
import gzip
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
version, baseline_name, inputs_name, output_name = sys.argv[1:]
baseline, inputs, output = Path(baseline_name), Path(inputs_name), Path(output_name).resolve()
pinned = json.loads((HERE/'basic-guard-inputs.json').read_text())
located = json.loads((HERE/'basic-guard.json').read_text())
epoch = 1795392000
assert not output.exists()


def inventory(root):
    return {str(p.relative_to(root)): (p.lstat().st_mode, os.readlink(p) if p.is_symlink()
                                       else hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None)
            for p in root.rglob('*')}


def guarded(release):
    record = located[release]
    assert record['archive_sha256'] == pinned['releases'][release]['archive_sha256']
    data = bytearray((inputs/re.sub(r'[^A-Za-z0-9.+~-]', '_', release)/'libmergedlo.so').read_bytes())
    assert hashlib.sha256(data).hexdigest() == record['original_sha256'] == pinned['releases'][release]['original_sha256']
    assert record['call_sites'] == 2 and record['symbol'] == '_ZN10SbiRuntime4StepEv'
    before, after = bytes.fromhex(record['original']), bytes.fromhex(record['replacement'])
    assert after == bytes.fromhex('31c0c3') and bytes(data[record['offset']:record['offset']+3]) == before
    data[record['offset']:record['offset']+3] = after
    assert hashlib.sha256(data).hexdigest() == record['sha256']
    return bytes(data)


with tempfile.TemporaryDirectory(prefix='basic-guard-', dir=output.parent) as temp_name:
    temp = Path(temp_name)
    root = temp/'root'
    subprocess.run(['dpkg-deb', '-R', str(baseline), str(root)], check=True)
    before_inventory = inventory(root)
    directory = root/'usr/lib/confos/reader-overrides'
    manifest_path = directory/'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    assert not any(item['package'] == pinned['package'] for item in manifest)
    payload_release = pinned['payload_release']
    data = guarded(payload_release)
    name = 'libmergedlo.so.gz'
    assert not (directory/name).exists()
    (directory/name).write_bytes(gzip.compress(data, compresslevel=9, mtime=epoch))
    others = []
    for release in sorted(located):
        if release == payload_release:
            continue
        guarded(release)
        record = located[release]
        others.append(dict(version=release, original_sha256=record['original_sha256'], offset=record['offset'],
                           original=record['original'], replacement=record['replacement'], sha256=record['sha256']))
    manifest.append(dict(package=pinned['package'], source_version=payload_release, target=pinned['target'],
                         payload=name, mode=0o644, sha256=hashlib.sha256(data).hexdigest(),
                         original_sha256=located[payload_release]['original_sha256'],
                         other_releases=others, unlisted_release='refuse'))
    manifest_path.write_text(json.dumps(manifest, sort_keys=True, indent=2)+'\n')
    docs = root/'usr/share/doc/confos-code-readers'
    for document in ('package-basic-guard.py', 'locate-basic-step.py', 'fetch-basic-library.py',
                     'basic-guard-inputs.json', 'basic-guard.json'):
        (docs/document).write_bytes((HERE/document).read_bytes())
    control = root/'DEBIAN/control'
    text = control.read_text()
    old = re.search(r'^Version: (\S+)$', text, re.M).group(1)
    control.write_text(text.replace('Version: '+old+'\n', 'Version: '+version+'\n'))
    # Every entry of the baseline keeps its bytes, mode and link; only the new files, the
    # manifest and the control file differ.
    new = {'usr/lib/confos/reader-overrides/'+name, *('usr/share/doc/confos-code-readers/'+d for d in (
        'package-basic-guard.py', 'locate-basic-step.py', 'fetch-basic-library.py', 'basic-guard-inputs.json',
        'basic-guard.json'))}
    for relative in new:
        (root/relative).chmod(0o644)
    after_inventory = inventory(root)
    changed = {key for key in set(before_inventory) | set(after_inventory)
               if before_inventory.get(key) != after_inventory.get(key)}
    assert changed == new | {'DEBIAN/control', 'usr/lib/confos/reader-overrides/manifest.json'}, sorted(changed)
    for path in [*root.rglob('*'), root]:
        os.utime(path, (epoch, epoch), follow_symlinks=False)
    artifact = temp/'payload.deb'
    subprocess.run(['dpkg-deb', '--root-owner-group', '-Zxz', '-z6', '--build', str(root), str(artifact)], check=True,
                   env=dict(os.environ, SOURCE_DATE_EPOCH=str(epoch), TZ='UTC', LC_ALL='C'))
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    os.replace(artifact, output)
    output.with_suffix('.deb.sha256').write_text(digest+'\n')
    print(digest, output.name, 'payload release', payload_release, 'guarded sha256', manifest[-1]['sha256'],
          'in place:', ', '.join(entry['version'] for entry in others))

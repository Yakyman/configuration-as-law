#!/usr/bin/env python3
"""Remove the completed round's temporary peer after exporting its evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('root', type=Path)
p.add_argument('--remove-peer', action='store_true', required=True)
a = p.parse_args()
root = a.root.resolve()
assert root.name == 'round-4' and root.parent.name == 'stand'
peer = root.parent/'round-4-peer'
assert peer.is_dir() and not peer.is_symlink()

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

service = dict(line.split('=', 1) for line in subprocess.check_output([
    'systemctl', '--user', 'show', 'bc4-final3-validation.service',
    '--property=Result', '--property=ActiveState', '--property=SubState'],
    text=True).splitlines())
assert service['Result'] == 'success' and service['ActiveState'] == 'inactive'
for relative in ('raw/round-4/rebuilt/summary.json',
                 'raw/round-4/rebuilt/regressions/summary.json',
                 'raw/round-4/combined/summary.json'):
    assert json.loads((root/relative).read_text())['suite_exit'] == 0
for directory in (root, peer):
    assert not list((directory/'vms').iterdir()), 'owned VM remains'
    assert not (directory/'base/stand.qcow2').is_symlink()

owned_qemu = []
for process in Path('/proc').iterdir():
    if not process.name.isdigit():
        continue
    try:
        command = (process/'cmdline').read_bytes().split(b'\0')
    except (OSError, PermissionError):
        continue
    if command and b'qemu-system' in command[0] and any(
            str(directory).encode() in argument
            for directory in (root, peer) for argument in command):
        owned_qemu.append(int(process.name))
assert not owned_qemu, 'owned QEMU process remains'

primary_sha = digest(root/'base/stand.qcow2')
peer_sha = digest(peer/'base/stand.qcow2')
provenance = json.loads((root/'raw/final-build-provenance.json').read_text())['builds']
assert primary_sha == provenance[root.name]['image_sha256']
assert peer_sha == provenance[peer.name]['image_sha256']
generated = sorted((root/'build').rglob('__pycache__'), reverse=True)
for directory in generated:
    shutil.rmtree(directory)
shutil.rmtree(peer)
archive = root/'raw/final-evidence.tar.gz'
if archive.exists():
    archive.unlink()

result = {
    'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    'validation_service': service,
    'image': 'round-4/base/stand.qcow2',
    'image_sha256': primary_sha,
    'image_mode': oct((root/'base/stand.qcow2').stat().st_mode & 0o777),
    'peer_image_sha256_before_removal': peer_sha,
    'peer_root_removed': not peer.exists(),
    'owned_vms_remaining': [],
    'owned_qemu_processes': owned_qemu,
    'generated_recipe_cache_directories_removed': len(generated),
    'temporary_export_archive_removed': not archive.exists(),
    'scope': 'Only the two round-4 build roots; other testbed instances were untouched.',
}
(root/'raw/cleanup-final.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
print(json.dumps(result, indent=2, sort_keys=True))

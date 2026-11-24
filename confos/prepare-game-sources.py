#!/usr/bin/python3
"""Fetch immutable upstream inputs; this does not inspect installed game files."""
import hashlib
from pathlib import Path
import subprocess

destination = Path('game-inputs')
destination.mkdir(exist_ok=True)
sources = [
    ('linuxgsm-26.5.0.tar.gz', 'https://codeload.github.com/GameServerManagers/LinuxGSM/tar.gz/50dc4e551b661b9d1fa39c291068a16a66056aff', None),
    ('linuxgsm-26.6.0.tar.gz', 'https://codeload.github.com/GameServerManagers/LinuxGSM/tar.gz/9ca2e951c6e15d4db7184a60e1fd8a831b2cdb0f', None),
    ('wet-2.60b.tar.xz', 'https://linuxgsm.download/WolfensteinEnemyTerritory/wet-2.60b-linux-i386-linuxgsm-20261101.tar.xz', 'ac359aebe0bf8fd568341876e3a8992d7c562ee6fdc4a8906bdbab47eae66cf3'),
]
for name, url, expected in sources:
    target = destination/name
    if not target.exists():
        temporary = target.with_suffix(target.suffix+'.part')
        subprocess.run(['curl', '-fL', '--retry', '2', '--max-time', '180', url, '-o', str(temporary)], check=True)
        temporary.rename(target)
    with target.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    if expected is not None and digest != expected:
        raise ValueError('upstream input checksum mismatch: '+name)
    print(digest, name, flush=True)

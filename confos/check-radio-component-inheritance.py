#!/usr/bin/python3
"""Compare40 reader payload with the exact sealed39 component."""
import hashlib
from pathlib import Path
import subprocess
import tarfile

assert Path('VERSION').read_text().strip() == '0.40'
baseline = Path('packages/confos-code-readers_0.39_amd64.deb')
with tarfile.open('releases/confos-0.39-source.tar.gz') as archive:
    assert archive.extractfile(str(baseline)).read() == baseline.read_bytes()

def entries(path):
    process = subprocess.Popen(['dpkg-deb', '--fsys-tarfile', str(path)], stdout=subprocess.PIPE)
    result = {}
    with tarfile.open(fileobj=process.stdout, mode='r|') as archive:
        for member in archive:
            assert member.name not in result
            digest = hashlib.sha256(archive.extractfile(member).read()).hexdigest() if member.isfile() else None
            result[member.name] = (member.type, member.mode, member.uid, member.gid, member.linkname, digest)
    assert process.wait() == 0
    return result

assert entries(baseline) == entries('packages/confos-code-readers_0.40_amd64.deb')
print('READER39 ALL PAYLOAD INHERITED BYTE MODE OWNER LINK EQUALITY PASS')

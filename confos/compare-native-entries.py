#!/usr/bin/python3
"""Verify that the installer and configuration commands of the assembled root are the
package objects themselves: same path, bytes, mode or link target as in the downloaded
data archives. From 0.49 nothing is moved or relinked; the recording entries are
runtime-package files reached through /usr/local/bin."""
import hashlib
from pathlib import Path
import stat
import subprocess
import sys
import tarfile

work = Path(sys.argv[1])
paths = {'usr/sbin/nft', 'usr/bin/systemctl', 'usr/bin/flatpak', 'usr/bin/podman',
         'usr/bin/pip', 'usr/bin/pip3', 'usr/bin/npm', 'usr/bin/npx',
         'usr/bin/hostnamectl', 'usr/bin/timedatectl', 'usr/sbin/sysctl',
         'usr/sbin/useradd', 'usr/sbin/usermod', 'usr/sbin/userdel',
         'usr/sbin/groupadd', 'usr/sbin/groupdel',
         'usr/bin/apt', 'usr/bin/apt-get', 'usr/sbin/visudo'}
owners = {'nftables', 'systemd', 'flatpak', 'podman', 'python3-pip', 'npm', 'passwd', 'procps', 'apt', 'sudo'}
expected = {}
for archive in sorted((work/'apt/archives').glob('*.deb')):
    if archive.name.split('_')[0] not in owners:
        continue
    process = subprocess.Popen(['dpkg-deb', '--fsys-tarfile', str(archive)], stdout=subprocess.PIPE)
    with tarfile.open(fileobj=process.stdout, mode='r|') as stream:
        for member in stream:
            name = member.name.removeprefix('./')
            if name not in paths:
                continue
            if member.issym():
                expected[name] = ('link', member.linkname, None)
            elif member.isfile():
                expected[name] = ('file', hashlib.file_digest(stream.extractfile(member), 'sha256').hexdigest(), member.mode)
    if process.wait():
        raise RuntimeError('data archive extraction failed')
for required in ('usr/bin/apt', 'usr/bin/apt-get'):
    assert required in expected, 'no package object found for /'+required
assert not (work/'root/usr/lib/confos/native').exists(), 'relocated package executables present'
for name, wanted in sorted(expected.items()):
    path = work/'root'/name
    if path.is_symlink():
        value = ('link', str(path.readlink()), None)
    else:
        value = ('file', hashlib.sha256(path.read_bytes()).hexdigest(), stat.S_IMODE(path.stat().st_mode))
    assert value == wanted, (name, wanted, value)
    entry = work/'root/usr/local/bin'/Path(name).name
    assert entry.is_symlink() and str(entry.readlink()) == '/usr/lib/confos/commands/'+Path(name).name, entry
    print('PASS package object in place /'+name, 'recording or query entry', '/usr/local/bin/'+Path(name).name)
print('NATIVE PACKAGE ENTRY EQUALITY PASS', len(expected))

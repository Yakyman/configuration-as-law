#!/usr/bin/python3
"""Canonical40 radio/recorded39 Flatpak composition; worker only, explicit build."""
from pathlib import Path
import hashlib, shutil, subprocess as sp, tarfile

root=Path.cwd();assert (root/'VERSION').read_text()=='0.40\n'
fixture=root/'radio-040-flatpak-fixture';fixture.mkdir(exist_ok=True)
base=root/'radio-040-fixture'
assert (base/'normal.conf').is_file(),'first run build-radio-fixture-040.py'
for path in base.iterdir():
    if path.is_file():shutil.copyfile(path,fixture/path.name)
rows=(base/'normal.conf').read_text().splitlines()
with tarfile.open(root/'releases/confos-0.39-source.tar.gz') as archive:
    sealed=archive.extractfile('build-flatpak-readers-fixture-039.py').read().decode()
    for name,ref,commit in (
        ('runtime','runtime/org.freedesktop.Platform/x86_64/26.08','df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c'),
        ('mpv','app/io.mpv.Mpv/x86_64/stable','13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc')):
        assert ref in sealed and commit in sealed,'fixture differs from sealed39'
        source=root/'flatpak-inputs'/(name+'.flatpak');assert source.is_file()
        target=fixture/source.name;shutil.copyfile(source,target)
        rows.append('flatpak '+ref+' '+commit+' '+hashlib.sha256(target.read_bytes()).hexdigest()+' '+target.name)
# App deployment checks the OSTree ref/commit against each declared bundle; the
# immutable39 reader component matches these exact runtime/application commits.
for name,version in (('flatpak','1.16.6-1~deb13u3'),('util-linux','2.41.5-0+deb13u1'),('gpg','2.4.7-21+deb13u1+b5'),('gpg-agent','2.4.7-21+deb13u1+b5')):
    row='package '+name+' '+version
    previous=[r for r in rows if r.startswith('package '+name+' ')]
    assert not previous or previous==[row],previous
    if not previous:rows.append(row)
payloads={
    'radio-flatpak-control-probe.py':(root/'radio-flatpak-control-probe.py').read_bytes(),
    'radio-flatpak-positive.py':b'print("RECORDED-RADIO-FLATPAK-PYTHON-PASS")\n',
    'radio-flatpak-entry.sh':b'set -eu\necho RECORDED-RADIO-FLATPAK-BASH-PASS\nexec /usr/bin/python3 /home/user/bin/radio-flatpak-control-probe.py\n',
}
for name,data in payloads.items():
    (fixture/name).write_bytes(data)
    rows.append('file /home/user/bin/'+name+' 0644 0:0 '+hashlib.sha256(data).hexdigest()+' '+name)
declaration=fixture/'declaration.conf';declaration.write_text('\n'.join(rows)+'\n')
sp.run(['bash','build.sh',str(declaration),'images/radio-040-flatpak.qcow2'],check=True)
print('CANONICAL40 FLATPAK RADIO FIXTURE BUILT',flush=True)

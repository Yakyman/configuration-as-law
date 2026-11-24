#!/usr/bin/python3
"""Minimal private sealed42 ssh derivative; shared release remains untouched."""
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess as sp
import tarfile

root=Path.cwd();work=root/'interpreter-inputs/ssh-reader-draft';guest=work/'guest';source=guest/'source'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
used=int(sp.check_output(['du','-sx','-B1',str(root)]).split()[0])
assert used+6*1024**3<60*1024**3,used
assert not guest.exists();source.mkdir(parents=True)
archive=root/'releases/confos-0.42-source.tar.gz'
assert digest(archive)=='38a9ff3f01eaf5fec7b818a9ab305988321fa1a39890012d41170e7aa35f3137'
with tarfile.open(archive) as tar:
    members=[m for m in tar.getmembers() if len(Path(m.name).parts)==1 or Path(m.name).parts[0] in ('components','examples','packages')]
    assert sum(m.size for m in members)<2*1024**3
    tar.extractall(source,members=members,filter='data')
assert (source/'VERSION').read_text()=='0.42\n'
inputs=guest/'inputs';inputs.mkdir()
comparison=json.loads((work/'comparison.json').read_text())
expected={'original_sha256':comparison['original']['sha256'],'sha256':comparison['candidate']['sha256']}
payloads={'match.conf':b'Match exec "touch /tmp/ssh-reader-marker"\n',
 'proxy.conf':b'Host ssh-reader-test\n ProxyCommand touch /tmp/ssh-reader-marker\n',
 'include-positive.conf':b'Include /usr/local/share/ssh-reader-draft/include-inner.conf\n',
 'include-inner.conf':b'Include /usr/local/share/ssh-reader-draft/match.conf\n',
 'include-negative.conf':b'Include /home/user/ssh-reader-material/match.conf\n',
 'expected.json':(json.dumps(expected,indent=2)+'\n').encode()}
rows=[r for r in (source/'examples/development.conf').read_text().splitlines() if r.startswith(('base ','snapshot ','account ','authorized-key '))]
rows+=['package openssh-client 1:10.0p1-7+deb13u4','account sshcheck 1001 1001 - /bin/bash /home/sshcheck']
sp.run(['ssh-keygen','-q','-t','ed25519','-N','','-C','disposable-private-fixture-only','-f',str(inputs/'connection-key')],check=True)
public=(inputs/'connection-key.pub').read_text().split()
rows.append('authorized-key sshcheck '+' '.join(public[:2]))
rows.append(f'file /usr/local/share/ssh-reader-draft/connection-key 0600 1000:1000 {digest(inputs/"connection-key")} connection-key')
for name,data in payloads.items():
    (inputs/name).write_bytes(data)
    rows.append(f'file /usr/local/share/ssh-reader-draft/{name} 0644 0:0 {digest(inputs/name)} {name}')
for name,path,target,mode in [
    ('probe.py',root/'probe-ssh-reader-guest-draft.py','/usr/local/bin/probe-ssh-reader-guest-draft.py','0644'),
    ('original-ssh',work/'original/usr/bin/ssh','/usr/local/libexec/ssh-reader-original','0755')]:
    shutil.copyfile(path,inputs/name)
    rows.append(f'file {target} {mode} 0:0 {digest(inputs/name)} {name}')
(inputs/'declaration.conf').write_text('\n'.join(rows)+'\n')
component=source/'packages/confos-code-readers_0.42_amd64.deb'
baseline=digest(component);stage=guest/'component'
sp.run(['dpkg-deb','-R',str(component),str(stage)],check=True)
def files(folder):return {str(p.relative_to(folder)):digest(p) for p in folder.rglob('*') if p.is_file() and not p.is_symlink()}
before=files(stage);directory=stage/'usr/lib/confos/reader-overrides';manifest=directory/'manifest.json'
items=json.loads(manifest.read_text());assert not any(x['package']=='openssh-client' for x in items)
data=(work/'candidate/ssh').read_bytes();assert hashlib.sha256(data).hexdigest()==expected['sha256']
(directory/'ssh-reader-private.gz').write_bytes(gzip.compress(data,mtime=1795392000))
items.append({'package':'openssh-client','source_version':'1:10.0p1-7+deb13u4','target':'/usr/bin/ssh',
              'payload':'ssh-reader-private.gz','sha256':hashlib.sha256(data).hexdigest(),'mode':0o755,'original_sha256':expected['original_sha256']})
manifest.write_text(json.dumps(items,indent=2,sort_keys=True)+'\n')
after=files(stage)
assert all(after[k]==v for k,v in before.items() if k!='usr/lib/confos/reader-overrides/manifest.json')
for p in [*stage.rglob('*'),stage]:os.utime(p,(1795392000,1795392000),follow_symlinks=False)
sp.run(['dpkg-deb','--root-owner-group','-Zxz','-z6','--build',str(stage),str(component)],check=True,env={**os.environ,'SOURCE_DATE_EPOCH':'1795392000'})
component.with_suffix('.deb.sha256').write_text(digest(component)+'\n')
(guest/'composition.json').write_text(json.dumps({'baseline42_component_sha256':baseline,'private_component_sha256':digest(component),
    'sealed42_source_sha256':digest(archive),'candidate_sha256':hashlib.sha256(data).hexdigest(),'inherited_file_bytes_preserved':True},indent=2)+'\n')
sp.run(['bash','build.sh',str(inputs/'declaration.conf'),str(guest/'disk.qcow2')],cwd=source,check=True)
guestroot=guest/'disk.work/root'
assert digest(guestroot/'usr/bin/ssh')==hashlib.sha256(data).hexdigest()
print('SSH_READER_PRIVATE42_IMAGE_PASS',flush=True)

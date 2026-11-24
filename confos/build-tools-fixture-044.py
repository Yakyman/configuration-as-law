#!/usr/bin/python3
"""Canonical44 combined SSH-reader and configuration-tool fixture."""
import hashlib,json,shutil,subprocess as sp
from pathlib import Path
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert Path('VERSION').read_text()=='0.44\n'
sp.run(['python3','check-reader-inheritance-044.py'],check=True)
work=Path('tools-044-fixture');inputs=work/'inputs';image=Path('images/tools-044.qcow2')
assert not work.exists() and not image.exists() and not Path('images/tools-044.work').exists()
shutil.copytree('examples',inputs)
rows=(inputs/'development.conf').read_text().splitlines()
assert rows[0]=='base 0.44'
assert any(r.startswith('file /home/user/bin/recorded.sh ') for r in rows)
metadata=Path('interpreter-inputs/ssh-reader-draft/metadata.json')
assert digest(metadata)=='0fa9a006b9103f742c8245a1083914036cb89436142cd54bd306b6c39b651099'
ssh=json.loads(metadata.read_text())
expected={'original_sha256':ssh['original_sha256'],'sha256':ssh['sha256']}
payloads={'match.conf':b'Match exec "touch /tmp/ssh-reader-marker"\n',
 'proxy.conf':b'Host ssh-reader-test\n ProxyCommand touch /tmp/ssh-reader-marker\n',
 'include-positive.conf':b'Include /usr/local/share/ssh-reader-draft/include-inner.conf\n',
 'include-inner.conf':b'Include /usr/local/share/ssh-reader-draft/match.conf\n',
 'include-negative.conf':b'Include /home/user/ssh-reader-material/match.conf\n',
 'expected.json':(json.dumps(expected,indent=2)+'\n').encode()}
rows+=['package openssh-client 1:10.0p1-7+deb13u4','account sshcheck 1001 1001 - /bin/bash /home/sshcheck']
sp.run(['ssh-keygen','-q','-t','ed25519','-N','','-C','disposable-private-fixture-only','-f',str(inputs/'connection-key')],check=True)
public=(inputs/'connection-key.pub').read_text().split()
rows.append('authorized-key sshcheck '+' '.join(public[:2]))
rows.append(f'file /usr/local/share/ssh-reader-draft/connection-key 0600 1000:1000 {digest(inputs/"connection-key")} connection-key')
for name,data in payloads.items():
 (inputs/name).write_bytes(data)
 rows.append(f'file /usr/local/share/ssh-reader-draft/{name} 0644 0:0 {digest(inputs/name)} {name}')
for name,path,target,mode in [
 ('ssh-probe.py',Path('probe-ssh-reader-guest-draft.py'),'/usr/local/bin/probe-ssh-reader-guest-draft.py','0644'),
 ('original-ssh',Path('interpreter-inputs/ssh-reader-draft/original/usr/bin/ssh'),'/usr/local/libexec/ssh-reader-original','0755')]:
 shutil.copyfile(path,inputs/name)
 rows.append(f'file {target} {mode} 0:0 {digest(inputs/name)} {name}')
editor=b'#!/bin/sh\ncat /proc/self/attr/current >&2\nfor target; do :; done\ncat > "$target"\n'
(inputs/'test-editor').write_bytes(editor)
rows.append('file /usr/local/bin/visudo-test-editor 0755 0:0 '+digest(inputs/'test-editor')+' test-editor')
(inputs/'declaration.conf').write_text('\n'.join(rows)+'\n')
assert digest(inputs/'original-ssh')==ssh['original_sha256']
sp.run(['bash','build.sh',str(inputs/'declaration.conf'),str(image)],check=True)
guest=Path('images/tools-044.work/root')
assert digest(guest/'usr/bin/ssh')==ssh['sha256']
assert (guest/'usr/bin/ssh').stat().st_mode&0o7777==ssh['mode']
print('CANONICAL44 FIXTURE EXACT SSH CANDIDATE ORIGINAL AND VISUDO EDITOR PASS')

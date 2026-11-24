#!/usr/bin/python3
"""Exercise a real recorded native editor, without shell-quote interpretation."""
import hashlib,subprocess
from pathlib import Path
declaration=Path('/state/declaration.conf')
before=declaration.read_bytes()
assert b'file /etc/sudoers.d/' not in before
identity=subprocess.check_output(['confos','status'],text=True)
assert identity.strip()=='APPLIED '+hashlib.sha256(before).hexdigest()
policy={str(p):p.read_bytes() for p in [Path('/etc/sudoers'),*Path('/etc/sudoers.d').iterdir()] if p.is_file()}
target=Path('/tmp/visudo-include-target');target.write_text('# ORIGINAL\n');target.chmod(0o600)
editor='/usr/local/bin/visudo-test-editor'
def edit(data,ok):
 result=subprocess.run(['env','EDITOR='+editor,'visudo'],input=data,text=True,capture_output=True)
 print('EDITOR REQUEST',repr(data),'EXIT',result.returncode,'STDOUT',result.stdout,'STDERR',result.stderr,flush=True)
 assert (result.returncode==0)==ok
 assert 'confos-session (enforce)' in result.stderr.splitlines()
 return result.stdout+result.stderr
out=edit('@include /tmp/visudo-include-target\n',False)
assert 'snippet includes are unsupported' in out
print('NATIVE INCLUDE MATERIAL AFTER REFUSAL',repr(target.read_bytes()),flush=True)
assert declaration.read_bytes()==before
assert policy=={str(p):p.read_bytes() for p in [Path('/etc/sudoers'),*Path('/etc/sudoers.d').iterdir()] if p.is_file()}
# This /tmp file is editor material, never applied policy. Native visudo may
# offer to edit it before the recorder rejects the captured include directive.
target.unlink()
assert not Path('/etc/sudoers.d/confos-local').exists()
text='user ALL=(ALL) NOPASSWD: /usr/bin/id\n'
edit(text,True)
recorded=declaration.read_bytes();assert recorded!=before
assert b'file /etc/sudoers.d/confos-local 0440 0:0 ' in recorded
assert not Path('/etc/sudoers.d/confos-local').exists()
edit(text,True);assert declaration.read_bytes()==recorded
result=subprocess.run(['visudo','--remove'],text=True,capture_output=True)
print('REMOVE RECORDED EDITOR REQUEST EXIT',result.returncode,result.stdout,result.stderr,flush=True)
assert result.returncode==0 and declaration.read_bytes()==before
assert subprocess.check_output(['confos','status'],text=True)==identity
assert not Path('/etc/sudoers.d/confos-local').exists()
print('VISUDO44 RECORDED EDITOR CONFINEMENT INCLUDE REFUSAL RECORD REPEAT REMOVE PASS',flush=True)

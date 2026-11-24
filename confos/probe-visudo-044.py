import subprocess as s,sys,hashlib
from pathlib import Path
mode=sys.argv[1] if len(sys.argv)>1 else 'before'
def run(command,data=None,ok=True):
 p=s.run(command,input=data,text=True,capture_output=True);print('COMMAND',command,'EXIT',p.returncode,'STDOUT',p.stdout,'STDERR',p.stderr,flush=True);assert (p.returncode==0)==ok;return p.stdout+p.stderr
def declaration():return Path('/state/declaration.conf').read_bytes()
program=sys.argv[2] if len(sys.argv)>2 else 'id'
assert program in ('id','true')
text='user ALL=(ALL) NOPASSWD: /usr/bin/'+program+'\n'
print('MODE',mode,flush=True);run(['confos','status'])
if mode=='before':
 before=declaration()
 Path('/tmp/visudo-native-check').write_text(text)
 run(['visudo','-cf','/tmp/visudo-native-check']);assert declaration()==before
 run(['sudo','-n','chown','0:0','/tmp/visudo-native-check']);run(['sudo','-n','chmod','0600','/tmp/visudo-native-check'])
 run(['env','EDITOR=tee','visudo'],text,False);assert declaration()==before
 run(['sudo','-n','env','EDITOR=tee','visudo','-f','/etc/sudoers'],text,False);assert declaration()==before
 out=run(['sudo','-n','env','EDITOR=tee','visudo'],'INVALID SUDOERS\n');assert 'syntax error' in out and declaration()==before
 out=run(['sudo','-n','env','EDITOR=tee','visudo'],'@include /tmp/visudo-native-check\n',False);assert 'snippet includes are unsupported' in out and declaration()==before
 Path('/home/user/visudo-editor.sh').write_text('echo SAVED-EDITOR-RAN >&2\ncat > "$1"\n')
 out=run(['sudo','-n','env','EDITOR=sh /home/user/visudo-editor.sh','visudo'],text);assert 'Permission denied for saved code input' in out and 'SAVED-EDITOR-RAN' not in out and declaration()==before
 out=run(['sudo','-n','env','EDITOR=tee','visudo'],text)
 after=declaration();assert after!=before and b'file /etc/sudoers.d/confos-local 0440 0:0 ' in after
 assert not Path('/etc/sudoers.d/confos-local').exists()
 run(['sudo','-n','env','VISUAL=tee','visudo'],text);assert declaration()==after
 # Preserve native append-editor mode from P4-BT-5, on an explicitly named snippet.
 run(['sudo','-n','env','EDITOR=tee -a','visudo','-f','/etc/sudoers.d/append-test'],text)
 assert not Path('/etc/sudoers.d/append-test').exists()
elif mode=='change':
 before=declaration()
 for name in ('confos-local','append-test'):
  assert run(['sudo','-n','cat','/etc/sudoers.d/'+name])=='user ALL=(ALL) NOPASSWD: /usr/bin/id\n'
  run(['sudo','-n','env','EDITOR=tee','visudo','-f','/etc/sudoers.d/'+name],text)
  assert run(['sudo','-n','cat','/etc/sudoers.d/'+name])=='user ALL=(ALL) NOPASSWD: /usr/bin/id\n'
 assert declaration()!=before
 after=declaration()
 for name in ('confos-local','append-test'):
  run(['sudo','-n','env','EDITOR=tee','visudo','-f','/etc/sudoers.d/'+name],text)
 assert declaration()==after
elif mode=='applied':
 for name in ('confos-local','append-test'):
  p=Path('/etc/sudoers.d')/name;assert run(['sudo','-n','cat',str(p)])==text and (p.stat().st_mode&0o777)==0o440 and p.stat().st_uid==0
 run(['sudo','-n','visudo','-c']);run(['sudo','-n','sudo','-l','-U','user'])
 before=declaration();run(['sudo','-n','env','SUDO_EDITOR=tee','visudo'],text);assert declaration()==before
elif mode=='remove':
 before=declaration()
 # Native visudo treats a zero-length edit as unchanged; preserve that behavior.
 run(['sudo','-n','env','EDITOR=tee','visudo'],'');assert declaration()==before
 for name in ('confos-local','append-test'):
  run(['sudo','-n','visudo','--remove','-f','/etc/sudoers.d/'+name])
  assert Path('/etc/sudoers.d',name).exists()
 after=declaration();run(['sudo','-n','visudo','--remove']);assert declaration()==after
 assert b'file /etc/sudoers.d/' not in after
elif mode=='removed':
 assert not Path('/etc/sudoers.d/confos-local').exists() and not Path('/etc/sudoers.d/append-test').exists()
 run(['sudo','-n','visudo','-c'])
print('VISUDO',mode,'PASS DECLARATION',hashlib.sha256(declaration()).hexdigest(),flush=True)

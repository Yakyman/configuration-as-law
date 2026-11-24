#!/usr/bin/python3
"""Prepare canonical change and root controls from the private probe recipes."""
from pathlib import Path
source=Path('visudo-recording-probe.py').read_text()
old="text='user ALL=(ALL) NOPASSWD: /usr/bin/id\\n'"
assert source.count(old)==1
source=source.replace(old,"program=sys.argv[2] if len(sys.argv)>2 else 'id'\nassert program in ('id','true')\ntext='user ALL=(ALL) NOPASSWD: /usr/bin/'+program+'\\n'")
anchor="elif mode=='applied':"
assert source.count(anchor)==1
source=source.replace(anchor,"""elif mode=='change':
 before=declaration()
 for name in ('confos-local','append-test'):
  assert run(['sudo','-n','cat','/etc/sudoers.d/'+name])=='user ALL=(ALL) NOPASSWD: /usr/bin/id\\n'
  run(['sudo','-n','env','EDITOR=tee','visudo','-f','/etc/sudoers.d/'+name],text)
  assert run(['sudo','-n','cat','/etc/sudoers.d/'+name])=='user ALL=(ALL) NOPASSWD: /usr/bin/id\\n'
 assert declaration()!=before
 after=declaration()
 for name in ('confos-local','append-test'):
  run(['sudo','-n','env','EDITOR=tee','visudo','-f','/etc/sudoers.d/'+name],text)
 assert declaration()==after
"""+anchor)
compile(source,'probe-visudo-044.py','exec')
Path('probe-visudo-044.py').write_text(source)
root=Path('run-ssh-reader-root-draft.sh').read_text().split("<<'ROOT_CONTROLS'\n",1)[1].rsplit('\nROOT_CONTROLS',1)[0]
Path('ssh-root-controls-044.sh').write_text(root+'\n')
print('CANONICAL44 PROBES PREPARED; NO GUEST CLAIM')

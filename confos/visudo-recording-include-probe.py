import subprocess,shlex
from pathlib import Path
p=Path('/tmp/visudo-include-target');p.write_text('# ORIGINAL\n');p.chmod(0o600)
code="from pathlib import Path;import sys;p=Path(sys.argv[-1]);print('EDITOR TARGET',str(p),'CONTEXT',Path('/proc/self/attr/current').read_text().strip(),flush=True);p.write_text('@include /tmp/visudo-include-target\\n' if 'snippet.tmp' in str(p) else '# CHANGED BY NATIVE INCLUDE EDIT\\n')"
editor=shlex.join(['/usr/bin/python3','-c',code])
before=Path('/state/declaration.conf').read_bytes()
r=subprocess.run(['env','EDITOR='+editor,'visudo'],input='\n',text=True,capture_output=True,timeout=30)
print('EDITOR',editor,'EXIT',r.returncode,'STDOUT',r.stdout,'STDERR',r.stderr,'TARGET',p.read_text(),'DECLARATION_UNCHANGED',Path('/state/declaration.conf').read_bytes()==before,flush=True)

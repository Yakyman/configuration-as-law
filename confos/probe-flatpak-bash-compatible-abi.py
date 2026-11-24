#!/usr/bin/python3
import subprocess
from pathlib import Path
root=Path.cwd()
runtime=next((root/'interpreter-inputs/flatpak-analysis/root/usr/lib/confos/flatpak/runtime/org.freedesktop.Platform/x86_64/26.08').glob('df26*/files'))
candidate=root/'interpreter-inputs/flatpak-bash-compatible/bash'
base=['bwrap','--unshare-all','--die-with-parent','--clearenv','--ro-bind',str(runtime),'/usr','--symlink','usr/bin','/bin','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--setenv','PATH','/usr/bin','--setenv','LD_LIBRARY_PATH','/usr/lib/x86_64-linux-gnu']
outputs=[]
for patched in (False,True):
    cmd=base+(['--ro-bind',str(candidate),'/usr/bin/bash'] if patched else [])
    p=subprocess.run(cmd+['/usr/bin/bash','-c','printf "%s\\n" "$BASH_VERSION"; enable -a; shopt; set -o; true'],capture_output=True,text=True)
    print('PATCHED',patched,'RC',p.returncode)
    print(p.stdout); print(p.stderr)
    assert p.returncode==0
    outputs.append(p.stdout)
assert outputs[0]==outputs[1], 'runtime feature/default option list differs'
print('ORIGINAL/PATCHED BUILTINS AND DEFAULT SHELL OPTIONS MATCH')


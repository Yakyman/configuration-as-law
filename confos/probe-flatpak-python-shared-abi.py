#!/usr/bin/python3
"""ABI/import checks against unchanged runtime; unconfined worker is not P4 proof."""
import glob, hashlib, json, os, subprocess
from pathlib import Path
base=Path.cwd()
runtime=next((base/'interpreter-inputs/flatpak-analysis/root/usr/lib/confos/flatpak/runtime/org.freedesktop.Platform/x86_64/26.08').glob('df26*/files'))
work=base/'interpreter-inputs/flatpak-python-shared'
modules=sorted(p.name.split('.')[0] for p in (runtime/'lib/python3.14/lib-dynload').glob('*.so'))
def command(patched):
    args=['bwrap','--unshare-all','--die-with-parent','--clearenv','--ro-bind',str(runtime),'/usr','--symlink','usr/bin','/bin','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--dir','/home','--setenv','HOME','/home','--setenv','PATH','/usr/bin','--setenv','LD_LIBRARY_PATH','/usr/lib/x86_64-linux-gnu','--chdir','/tmp']
    if patched:
        args += ['--ro-bind',str(work/'python'),'/usr/bin/python3.14','--ro-bind',str(work/'libpython3.14.so.1.0'),'/usr/lib/x86_64-linux-gnu/libpython3.14.so.1.0']
    return args+['/usr/bin/python3.14']
code="""import importlib,json,sys,sysconfig
out={}
for name in MODULES:
 try:
  importlib.import_module(name)
  out[name]='OK'
 except Exception as e: out[name]=type(e).__name__+': '+str(e)
print(json.dumps(out,sort_keys=True))
print(sys.version)
print(sysconfig.get_config_var('SOABI'))
""".replace('MODULES',repr(modules))
results=[]
for patched in (False,True):
    p=subprocess.run(command(patched)+['-c',code],capture_output=True,text=True)
    print('PATCHED',patched,'RC',p.returncode,flush=True)
    print(p.stdout,flush=True); print(p.stderr,flush=True)
    if p.returncode: raise SystemExit('runtime import process failed')
    results.append(json.loads(p.stdout.splitlines()[0]))
assert results[0]==results[1], 'native extension import result mismatch'
for path in (work/'python',work/'libpython3.14.so.1.0'):
    print('SHA256',path.name,hashlib.sha256(path.read_bytes()).hexdigest())
    subprocess.run(['readelf','-d',str(path)],check=True)
    subprocess.run(['readelf','-V',str(path)],check=True)
# Original native extension symbol imports must remain exported by shared core.
def exports(path):
    text=subprocess.check_output(['nm','-D','--defined-only',str(path)],text=True)
    return {line.split()[-1] for line in text.splitlines() if line.split()}
old=exports(runtime/'lib/x86_64-linux-gnu/libpython3.14.so.1.0')
new=exports(work/'libpython3.14.so.1.0')
missing=sorted(old-new)
print('ORIGINAL EXPORTED SYMBOLS MISSING',json.dumps(missing),flush=True)
assert not missing
print('SHARED CORE ORIGINAL RUNTIME IMPORT/EXPORT ABI CHECK PASS',len(modules),flush=True)
print('SAVED-CODE POLICY UNTESTED HERE: worker unconfined; guest required',flush=True)


#!/usr/bin/python3
"""Unconfined native ABI and Lua controls for both original and complete candidate."""
from pathlib import Path
import subprocess
import json
import re
compile_text=Path('compile-flatpak-mpv-candidate-draft.py').read_text()
exec(compile_text[compile_text.index('import hashlib'):compile_text.index("build=work/")])
exec(compile_text[compile_text.index("runtime=root/"):compile_text.index('features={}')])
candidate=work/'candidate'
probe=work/'libmpv-runtime-probe.py'
probe.write_text('''import ctypes
m=ctypes.CDLL('/app/lib/libmpv.so.2')
m.mpv_client_api_version.restype=ctypes.c_ulong
m.mpv_create.restype=ctypes.c_void_p
m.mpv_initialize.argtypes=[ctypes.c_void_p]
m.mpv_set_option_string.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
m.mpv_terminate_destroy.argtypes=[ctypes.c_void_p]
h=m.mpv_create()
assert h
for name,value in [(b'config',b'no'),(b'vo',b'null'),(b'ao',b'null')]:
    assert m.mpv_set_option_string(h,name,value)==0
assert m.mpv_initialize(h)==0
print('LIBMPV_API_INITIALIZE_DESTROY',m.mpv_client_api_version())
m.mpv_terminate_destroy(h)
''')
versions=[]
for changed in (False,True):
    prefix=runbase.copy()
    if changed:
        for name,target in (('mpv','bin/mpv'),('libmpv.so.2.6.0','lib/libmpv.so.2.6.0'),('libluajit-5.1.so.2.1.1781966178','lib/libluajit-5.1.so.2.1.1781966178')):
            prefix+=['--ro-bind',str(candidate/name),'/app/'+target]
    result=subprocess.run(prefix+['--ro-bind',str(probe),'/tmp/probe.py','/usr/bin/python3','/tmp/probe.py'],text=True,capture_output=True,timeout=30)
    print('LIBMPV_PATCHED',changed,'RC',result.returncode,result.stdout,result.stderr,flush=True)
    assert result.returncode==0
    versions.append(result.stdout)
    data='print("INITIAL_LUA_CONTROL",jit.version); local f=assert(io.open("/tmp/n.lua","w")); f:write("return 47"); f:close(); assert(assert(loadfile("/tmp/n.lua"))()==47); assert(dofile("/tmp/n.lua")==47); package.path="/tmp/?.lua"; assert(require("n")==47); print("NESTED_LUA_DATA_CONTROL"); mp.commandv("quit")\n'
    result=subprocess.run(prefix+['--symlink','/proc/self/fd/0','/tmp/typed.lua','/app/bin/mpv','--no-config','--load-scripts=no','--vo=null','--ao=null','--idle=yes','--script=/tmp/typed.lua'],input=data,text=True,capture_output=True,timeout=30)
    print('LUA_PATCHED',changed,'RC',result.returncode,result.stdout,result.stderr,flush=True)
    assert result.returncode==0 and 'NESTED_LUA_DATA_CONTROL' in result.stdout+result.stderr
assert versions[0]==versions[1]
abi={}
for name,target in (('mpv','bin/mpv'),('libmpv.so.2.6.0','lib/libmpv.so.2.6.0')):
    rows={}
    for label,path in (('original',app/target),('candidate',candidate/name)):
        output=subprocess.check_output(['readelf','-d','-V',str(path)],text=True)
        rows[label]={'needed':sorted(re.findall(r'\(NEEDED\).*?\[(.*?)\]',output)),
                     'soname':re.findall(r'\(SONAME\).*?\[(.*?)\]',output),
                     'version_names':sorted(set(re.findall(r'Name: (\S+)',output)))}
    rows['needed_added']=sorted(set(rows['candidate']['needed'])-set(rows['original']['needed']))
    rows['needed_removed']=sorted(set(rows['original']['needed'])-set(rows['candidate']['needed']))
    rows['versions_added']=sorted(set(rows['candidate']['version_names'])-set(rows['original']['version_names']))
    assert rows['original']['soname']==rows['candidate']['soname']
    abi[name]=rows
print('DYNAMIC_ABI_COMPARISON',json.dumps(abi),flush=True)
(work/'mpv-dynamic-abi-comparison.json').write_text(json.dumps(abi,indent=2)+'\n')
print('COMPLETE_CANDIDATE_ORIGINAL_RUNTIME_NATIVE_CONTROLS_PASS; no confinement claim',flush=True)

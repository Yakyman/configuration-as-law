#!/usr/bin/python3
"""Original-runtime feature/ABI and native JS/Lua/libmpv controls, no confinement."""
import hashlib,json,re,subprocess
from pathlib import Path
compile_text=Path('compile-flatpak-mpv-candidate-draft.py').read_text()
exec(compile_text[compile_text.index('import hashlib'):compile_text.index('build=work/')])
exec(compile_text[compile_text.index('runtime=root/'):compile_text.index('features={}')])
work=root/'interpreter-inputs/flatpak-mpv-js-candidate'
candidate=work/'candidate'
# Same original feature/export comparison; reports are written only to NEW work.
exec(compile_text[compile_text.index('features={}'):])
native=Path('probe-flatpak-mpv-complete-runtime-draft.py').read_text()
exec(native[native.index("probe=work/'libmpv-runtime-probe.py'"):])
controls=work/'native-js-controls';controls.mkdir(exist_ok=True)
(controls/'module.js').write_text('exports.answer = 47;\n')
(controls/'data.js').write_text('print("JS_EXPLICIT_DATA_EVAL_CONTROL");\n')
program='''var m = require('/controls/module');
if (m.answer !== 47) throw Error('module result mismatch');
var text = mp.utils.read_file('/controls/data.js');
if (text.indexOf('JS_EXPLICIT_DATA_EVAL_CONTROL') < 0) throw Error('data read mismatch');
mp.utils.compile_js('explicit-data', text)();
print('JS_INITIAL_REQUIRE_DATA_CONTROL');
mp.commandv('quit');
'''
(controls/'main.js').write_text(program)
(controls/'libmpv-js.py').write_text('''import ctypes,time
m=ctypes.CDLL('/app/lib/libmpv.so.2')
m.mpv_create.restype=ctypes.c_void_p
m.mpv_initialize.argtypes=[ctypes.c_void_p]
m.mpv_set_option_string.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
m.mpv_terminate_destroy.argtypes=[ctypes.c_void_p]
class Event(ctypes.Structure):
    _fields_=[('event_id',ctypes.c_int),('error',ctypes.c_int),('reply_userdata',ctypes.c_ulonglong),('data',ctypes.c_void_p)]
m.mpv_wait_event.argtypes=[ctypes.c_void_p,ctypes.c_double]
m.mpv_wait_event.restype=ctypes.POINTER(Event)
h=m.mpv_create(); assert h
for k,v in [(b'config',b'no'),(b'terminal',b'yes'),(b'vo',b'null'),(b'ao',b'null'),(b'scripts',b'/controls/main.js')]:
    result=m.mpv_set_option_string(h,k,v)
    assert result==0,(k,result)
assert m.mpv_initialize(h)==0
deadline=time.monotonic()+15
while time.monotonic()<deadline:
    if m.mpv_wait_event(h,1).contents.event_id==1:
        break
else: raise AssertionError('script shutdown event missing')
m.mpv_terminate_destroy(h)
print('LIBMPV_JS_SCRIPT_SHUTDOWN_CONTROL')
''')
for changed in (False,True):
    prefix=runbase+['--ro-bind',str(controls),'/controls']
    if changed:
        for name,target in (('mpv','bin/mpv'),('libmpv.so.2.6.0','lib/libmpv.so.2.6.0'),('libluajit-5.1.so.2.1.1781966178','lib/libluajit-5.1.so.2.1.1781966178')):
            prefix+=['--ro-bind',str(candidate/name),'/app/'+target]
    for kind in ('saved-initial-js','typed-pipe-js','libmpv-js'):
        command=prefix.copy();data=None
        if kind=='libmpv-js':
            command+=['/usr/bin/python3','/controls/libmpv-js.py']
        else:
            if kind=='typed-pipe-js':
                command+=['--symlink','/proc/self/fd/0','/tmp/typed.js'];data=program
            script='/tmp/typed.js' if data else '/controls/main.js'
            command+=['/app/bin/mpv','--no-config','--load-scripts=no','--vo=null','--ao=null','--idle=yes','--script='+script]
        result=subprocess.run(command,input=data,text=True,capture_output=True,timeout=25)
        output=result.stdout+result.stderr
        print('JS_NATIVE_CONTROL',kind,'PATCHED',changed,'RC',result.returncode,output,flush=True)
        assert result.returncode==0
        assert 'JS_INITIAL_REQUIRE_DATA_CONTROL' in output
        assert 'JS_EXPLICIT_DATA_EVAL_CONTROL' in output
        if kind=='libmpv-js': assert 'LIBMPV_JS_SCRIPT_SHUTDOWN_CONTROL' in output
(work/'native-controls-passed.json').write_text(json.dumps({'original_and_candidate':'feature/export/SONAME; Lua initial+nested; libmpv initialize/destroy; JS saved initial, typed pipe, require, explicit data read/eval, libmpv JS shutdown','confined':False},indent=2)+'\n')
print('SEPARATE_JS_CANDIDATE_ALL_NATIVE_CONTROLS_PASS; no guest confinement claim',flush=True)

#!/usr/bin/python3
"""Deterministic development wheel from the image's exact CPython native module.
Run only inside the build VM, before factory capture; no native compilation.
"""
import base64,csv,hashlib,io,json,pathlib,sys,zipfile
P=pathlib.Path
root=P(sys.argv[1]);root.mkdir(parents=True,exist_ok=True)
modules=list(P('/usr/lib/python3.13/lib-dynload').glob('_bz2*.so'))
if len(modules)!=1:raise RuntimeError('one CPython 3.13 native _bz2 module required')
module=modules[0];data=module.read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest()
metadata='stand_native-1.0.dist-info/'
entries={module.name:data,metadata+'METADATA':b'Metadata-Version: 2.1\nName: stand-native\nVersion: 1.0\n',metadata+'WHEEL':b'Wheel-Version: 1.0\nGenerator: deterministic-development-fixture\nRoot-Is-Purelib: false\nTag: cp313-cp313-linux_x86_64\n'}
record=io.StringIO(newline='');writer=csv.writer(record,lineterminator='\n')
for name,body in sorted(entries.items()):writer.writerow((name,'sha256='+base64.urlsafe_b64encode(hashlib.sha256(body).digest()).rstrip(b'=').decode(),len(body)))
writer.writerow((metadata+'RECORD','',''));entries[metadata+'RECORD']=record.getvalue().encode()
archive=root/'stand_native-1.0-cp313-cp313-linux_x86_64.whl'
buffer=io.BytesIO()
with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_STORED) as wheel:
    for name,body in sorted(entries.items()):
        info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.create_system=3;info.external_attr=0o100444<<16;wheel.writestr(info,body)
raw=buffer.getvalue()
if archive.exists() and archive.read_bytes()!=raw:raise ValueError('native wheel cache differs from pinned base input')
archive.write_bytes(raw)
code="import _bz2\nassert _bz2.__file__.startswith('/opt/stand/pkgs/pip-native-development/site/')\ncompressor=_bz2.BZ2Compressor()\ncompressed=compressor.compress(b'abc')+compressor.flush()\nprint('NATIVE_POSITIVE '+_bz2.BZ2Decompressor().decompress(compressed).decode())\n"
lock=dict(schema=1,channel='pip',project='native-development',packages=[dict(name='stand-native',version='1.0',source='factory-cpython-extension:'+str(module)+'#sha256='+sha(data),sha256=sha(raw),archive=archive.name,dependencies=[])],entry_code=code,entry_sha256=sha(code.encode()))
content=json.dumps(lock,sort_keys=True)+'\n';target=root/'pip-native.lock.json'
if target.exists() and target.read_text()!=content:raise ValueError('native lock cache differs from pinned base input')
target.write_text(content)
print('NATIVE_WHEEL_READY sha256='+sha(raw)+' module_sha256='+sha(data))

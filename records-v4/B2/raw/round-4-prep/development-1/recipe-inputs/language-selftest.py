#!/usr/bin/python3
"""Fresh-VM BC4 tests: fixture root argument, optional raw JSONL output."""
import hashlib,io,json,os,pathlib,shutil,subprocess,sys,time,tarfile,zipfile
P=pathlib.Path;fixtures=P(sys.argv[1]);out=P(sys.argv[2] if len(sys.argv)>2 else '/var/lib/stand/language-selftest.jsonl');failed=[]
log=out.open('w',buffering=1)
def record(x):
    x['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());s=json.dumps(x,sort_keys=True);log.write(s+'\n');print(s,flush=True)
def run(ident,variant,args,positive=False,contains=None):
    record(dict(phase='expected',id=ident,variants=variant,command=args,expected='success' if positive else 'refusal',source='B2/raw/round-4/language-notes.md'))
    try:
        p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
        ok=(p.returncode==0 if positive else p.returncode!=0) and (contains is None or contains in p.stdout) and 'UNRECORDED_NATIVE' not in p.stdout
        record(dict(phase='result',id=ident,passed=ok,rc=p.returncode,output=p.stdout))
    except subprocess.TimeoutExpired:
        ok=False;record(dict(phase='result',id=ident,passed=False,error='timeout'))
    if not ok:failed.append(ident)
def session(ident,variant,fields,**kw):run(ident,variant,['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-session','-c','\t'.join(fields)],**kw)
for tool in ('pip','npm'):
    lock=str(fixtures/(tool+'.lock.json'));variant=['C2.1' if tool=='pip' else 'C2.2','C2.3']
    session('LANG-'+tool+'-INSTALL',variant,['broker',tool,'install','--stand-lock',lock],positive=True)
    entry='/opt/stand/pkgs/'+tool+'-development/main.'+('py' if tool=='pip' else 'js')
    session('LANG-'+tool+'-RUN',variant,['run',entry],positive=True,contains='PIP_POSITIVE 2026' if tool=='pip' else 'NPM_POSITIVE true')
    run('LANG-'+tool+'-ROOT-INSTALL',variant,['/usr/bin/sudo','-n','/usr/local/bin/'+tool,'install','--stand-lock',lock],positive=True)
    examples=P('/var/lib/stand/channel-examples');examples.mkdir(exist_ok=True)
    rows=[json.loads(line) for line in (P('/var/lib/stand/current')/'machine.jsonl').read_text().splitlines() if line.strip()]
    exported=[r for r in rows if r['id']=='language:'+tool+':development']
    if len(exported)!=1:raise RuntimeError('successful language example row missing')
    (examples/(tool+'.jsonl')).write_text(json.dumps(exported[0],sort_keys=True)+'\n')
    cases=([['install','--user','six'],['install','--target','/tmp/pkg','six'],['install','--prefix','/tmp/pkg','six'],['install','-e','/tmp/source'],['install','git+https://invalid.example/repo'],['install','--index-url','https://invalid.example','six'],['install','--config-settings','x=y','/tmp/source']] if tool=='pip' else [['install','--global','is-odd'],['install','--prefix','/tmp/pkg','is-odd'],['install','--workspace','x','is-odd'],['link','/tmp/source'],['run','preinstall'],['start'],['test'],['install','--ignore-scripts','is-odd'],['install','--registry','https://invalid.example','is-odd'],['install','git+https://invalid.example/repo'],['install','/home/stand/unrecorded.tgz']])
    for i,args in enumerate(cases):
        session('LANG-'+tool+'-BYPASS-'+str(i),['C2.1','C2.2','C2.3','C2.4','C2.5'],['broker',tool,*args])
        run('LANG-'+tool+'-SUDO-BYPASS-'+str(i),['C2.1','C2.2','C2.3','C2.4','C2.5'],['/usr/bin/sudo','-n','/usr/local/bin/'+tool,*args])
    session('LANG-'+tool+'-EXTRA-ARGV',['C2.5','C2.6'],['run',entry,'/tmp/unrecorded'])
    session('LANG-'+tool+'-RAW-INTERPRETER',['C2.4','C2.6'],['run','/usr/bin/python3.13' if tool=='pip' else '/usr/bin/node','/tmp/unrecorded'])
    if tool=='pip':session('LANG-pip-VIRTUALENV',['C2.1'],['run','/usr/bin/python3.13','-m','venv','/home/stand/unrecorded-venv'])
    obj=json.loads(P(lock).read_text());obj['packages'][0]['sha256']='0'*64;bad=fixtures/(tool+'.bad.lock.json');bad.write_text(json.dumps(obj))
    session('LANG-'+tool+'-BAD-HASH',['C2.3'],['broker',tool,'install','--stand-lock',str(bad)])
    obj=json.loads(P(lock).read_text());obj['packages']=obj['packages'][:1];bad.write_text(json.dumps(obj))
    session('LANG-'+tool+'-MISSING-DEPENDENCY',['C2.1','C2.2'],['broker',tool,'install','--stand-lock',str(bad)])
    bad.unlink()
    obj=json.loads(P(lock).read_text());original=fixtures/obj['packages'][0]['archive']
    mutated=fixtures/(tool+'.hook-artifact');marker=P('/tmp/language-unrecorded-hook')
    marker.unlink(missing_ok=True)
    if tool=='pip':
        with zipfile.ZipFile(original) as src,zipfile.ZipFile(mutated,'w') as dst:
            for item in src.infolist():dst.writestr(item,src.read(item))
            dst.writestr('unrecorded.pth',"import pathlib; pathlib.Path('/tmp/language-unrecorded-hook').touch()\n")
    else:
        with tarfile.open(original,'r:gz') as src,tarfile.open(mutated,'w:gz') as dst:
            for item in src:
                if not item.isfile():dst.addfile(item);continue
                data=src.extractfile(item).read()
                if item.name=='package/package.json':
                    meta=json.loads(data);meta.setdefault('scripts',{})['preinstall']='touch /tmp/language-unrecorded-hook'
                    data=json.dumps(meta).encode();item.size=len(data)
                dst.addfile(item,io.BytesIO(data))
    obj['packages'][0]['archive']=mutated.name;obj['packages'][0]['sha256']=hashlib.sha256(mutated.read_bytes()).hexdigest();bad.write_text(json.dumps(obj))
    session('LANG-'+tool+'-HOOK-ARTIFACT',['C2.5','C2.6'],['broker',tool,'install','--stand-lock',str(bad)],positive=(tool=='npm'))
    ok=not marker.exists();record(dict(phase='result',id='LANG-'+tool+'-HOOK-NOT-EXECUTED',passed=ok,marker_exists=not ok))
    if not ok:failed.append('LANG-'+tool+'-HOOK-NOT-EXECUTED')
    session('LANG-'+tool+'-RESTORE',['C2.1','C2.2'],['broker',tool,'install','--stand-lock',lock],positive=True)
    bad.unlink();mutated.unlink();marker.unlink(missing_ok=True)
    if tool=='pip':
        source=fixtures/'source-backend.tar.gz'
        with tarfile.open(source,'w:gz') as archive:
            for filename,data in [('pyproject.toml',b'[build-system]\nrequires=[]\nbuild-backend="backend"\nbackend-path=["."]\n'),('backend.py',b"open('/tmp/language-unrecorded-hook','w').write('bad')\n")]:
                item=tarfile.TarInfo(filename);item.size=len(data);archive.addfile(item,io.BytesIO(data))
        obj=json.loads(P(lock).read_text());obj['packages'][0]['archive']=source.name;obj['packages'][0]['sha256']=hashlib.sha256(source.read_bytes()).hexdigest();bad.write_text(json.dumps(obj))
        session('LANG-pip-SOURCE-BACKEND',['C2.5'],['broker','pip','install','--stand-lock',str(bad)])
        ok=not marker.exists();record(dict(phase='result',id='LANG-pip-SOURCE-NOT-EXECUTED',passed=ok))
        if not ok:failed.append('LANG-pip-SOURCE-NOT-EXECUTED')
        source.unlink();bad.unlink();marker.unlink(missing_ok=True)
        lib=P('/home/stand/language-mutable.so');shutil.copyfile('/usr/lib/x86_64-linux-gnu/libm.so.6',lib);lib.chmod(0o644)
        obj=json.loads(P(lock).read_text());obj['entry_code']="import ctypes\nctypes.CDLL('/home/stand/language-mutable.so')\nprint('UNRECORDED_NATIVE')\n";obj['entry_sha256']=hashlib.sha256(obj['entry_code'].encode()).hexdigest();bad.write_text(json.dumps(obj))
        session('LANG-pip-DECLARE-NATIVE-ATTEMPT',['C2.6'],['broker','pip','install','--stand-lock',str(bad)],positive=True)
        session('LANG-pip-MUTABLE-NATIVE-REFUSED',['C2.6'],['run',entry])
        session('LANG-pip-AFTER-NATIVE-RESTORE',['C2.6'],['broker','pip','install','--stand-lock',lock],positive=True)
        lib.unlink();bad.unlink()

    session('LANG-'+tool+'-IMMUTABLE-WRITE',['C2.1','C2.2','C2.4'],['run','/usr/bin/cp',lock,entry])
    oldcopy='/home/stand/language-old-'+tool+('.py' if tool=='pip' else '.js')
    session('LANG-'+tool+'-COPY-OLD',['C2.4'],['run','/usr/bin/cp',entry,oldcopy],positive=True)
    session('LANG-'+tool+'-REMOVE',['C2.4'],['broker',tool,'remove','language:'+tool+':development'],positive=True)
    session('LANG-'+tool+'-REMOVED-LAUNCH',['C2.4'],['run',entry])
    session('LANG-'+tool+'-COPIED-LAUNCH',['C2.4'],['run',oldcopy])
    P(oldcopy).unlink(missing_ok=True)
    session('LANG-'+tool+'-REINSTALL',['C2.1','C2.2'],['broker',tool,'install','--stand-lock',lock],positive=True)
native_lock=fixtures/'pip-native.lock.json'
native_entry='/opt/stand/pkgs/pip-native-development/main.py'
session('LANG-NATIVE-WHEEL-INSTALL',['C2.6'],['broker','pip','install','--stand-lock',str(native_lock)],positive=True)
session('LANG-NATIVE-WHEEL-IMPORT',['C2.6'],['run',native_entry],positive=True,contains='NATIVE_POSITIVE abc')
rows=[json.loads(line) for line in (P('/var/lib/stand/current')/'machine.jsonl').read_text().splitlines() if line.strip()]
exported=[r for r in rows if r['id']=='language:pip:native-development']
if len(exported)!=1:raise RuntimeError('successful native wheel example row missing')
(examples/'pip-native.jsonl').write_text(json.dumps(exported[0],sort_keys=True)+'\n')
session('LANG-NATIVE-WHEEL-REMOVE',['C2.6'],['broker','pip','remove','language:pip:native-development'],positive=True)
session('LANG-NATIVE-WHEEL-REMOVED-LAUNCH',['C2.6'],['run',native_entry])
run('LANG-VERIFY', ['C2.1','C2.2'],['/usr/local/bin/stand-verify'],positive=True)
record(dict(summary=True,failed=failed));sys.exit(bool(failed))

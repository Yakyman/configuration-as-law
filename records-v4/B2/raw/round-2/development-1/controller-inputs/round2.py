#!/usr/bin/env python3
"""One-shot round 2 build and validation, run by a server user service."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
phase=sys.argv[1]
if phase not in ('development-1','development-2','final-1','final-2','final-3'):
    raise SystemExit('unused named phase required')
OUT=ROOT/'raw/round-2'/phase
OUT.mkdir(parents=True,exist_ok=False)
ENV={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','STAND_V4_CHANNELS':'1','LAB_RUN_TIMEOUT':'7200'}
steps=[];owned=[];peer=ROOT/'round2-peer'
def utc():return time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
def save(name,value):(OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def run(argv,log,script=None,root=ROOT,legacy=False,required=True):
    rec={'argv':[str(a).replace(str(ROOT),'[stand-root]') for a in argv],
         'started_utc':utc(),'log':log,'expected_exit':0,'legacy_protocol':legacy}
    print(json.dumps({'phase':'expected',**rec}),flush=True)
    with (OUT/log).open('wb') as stream:
        result=subprocess.run(argv,cwd=root,input=script.encode() if script else None,
            stdout=stream,stderr=subprocess.STDOUT,
            env={**ENV,'STAND_ROOT':str(root),'STAND_LEGACY':'1' if legacy else '0'})
    rec.update(exit=result.returncode,ended_utc=utc());steps.append(rec);save('steps.json',steps)
    print(json.dumps({'phase':'result',**rec}),flush=True)
    if required and result.returncode:raise RuntimeError('stage failed: '+log)
    return result.returncode
def lab(op,name,log,script=None,extra=()):
    return run(['python3','lab.py',op,name,*extra],log,script)
def destroy(name):
    if (ROOT/'vms'/name).exists():
        if run(['python3','lab.py','destroy',name],name+'-destroy.log',required=False):
            lab('kill',name,name+'-kill.log');lab('destroy',name,name+'-destroy-after-kill.log')
status=1
try:
    shutil.copytree(ROOT/'build',OUT/'recipe-inputs')
    shutil.copytree(ROOT/'tools',OUT/'controller-inputs')
    save('input-sha256.json',{str(p.relative_to(ROOT)):sha(p) for folder in ('build','tools')
        for p in sorted((ROOT/folder).iterdir()) if p.is_file()})
    run(['python3','build/build.py','--server','--replace'],'build.log')
    shutil.copyfile(ROOT/'raw/recipe.log',OUT/'recipe.log')
    save('image.json',{'sha256':sha(ROOT/'base/stand.qcow2'),'mode':oct((ROOT/'base/stand.qcow2').stat().st_mode&0o777)})
    suites=('objects',) if phase.startswith('development') else ('objects','shell','gate','tools','supplement')
    for suite in suites:
        name='bc2-'+phase+'-'+suite;owned.append(name)
        lab('new',name,suite+'-new.log',extra=['stand'])
        if suite=='supplement':
            for part in ('direct','extra'):
                run(['python3','lab.py','run',name,'--root'],'supplement-'+part+'.jsonl',
                    (ROOT/'tools'/('v4-'+part+'-selftest.py')).read_text(),required=False)
        else:
            run(['python3','lab.py','run',name,'--root'],suite+'.jsonl',
                'python3 -B /usr/local/lib/stand/v4-'+suite+'-selftest.py\n',required=False)
        if suite in ('objects','shell','supplement'):
            lab('run',name,suite+'-before-verify.log','stand-verify\n',extra=['--root'])
            lab('stop',name,suite+'-stop.log');lab('start',name,suite+'-start.log')
            if suite in ('objects','shell'):
                run(['python3','lab.py','run',name,'--root'],suite+'-reboot.jsonl',
                    'python3 -B /usr/local/lib/stand/v4-'+suite+'-selftest.py --after\n',required=False)
        run(['python3','lab.py','run',name,'--root'],suite+'-verify.log','stand-verify\n',required=False)
        if suite=='objects':
            lab('copy-out',name,'objects-export.log',extra=['/var/lib/stand/round2-evidence',str(OUT/'objects-evidence')])
            lab('copy-out',name,'factory-export.log',extra=['/etc/stand/factory',str(OUT/'factory-export')])
        destroy(name)
    if phase.startswith('final'):
        if peer.exists():raise RuntimeError('peer collision')
        peer.mkdir()
        for folder in ('build','downloads','keys'):shutil.copytree(ROOT/folder,peer/folder)
        run(['python3','build/build.py','--server'],'peer-build.log',root=peer)
        ident='bc2-'+phase
        run(['python3','build/round4-driver.py',ident,'--regressions','--peer-root','round2-peer'],
            'regressions-console.jsonl',legacy=True,required=False)
        carried=ROOT/'raw/round-4'/ident
        if carried.exists():shutil.move(carried,OUT/'carried-suite')
        run(['python3','build/assemble-channel-examples.py',str(OUT/'carried-suite'),'round2-example'],'assemble.log',legacy=True)
        run(['python3','build/combined-selftest.py',ident+'-combined','round2-example/combined',
             '--peer-root','round2-peer','--reboot'],'combined-console.jsonl',legacy=True,required=False)
        combined=ROOT/'raw/round-4'/(ident+'-combined')
        if combined.exists():shutil.move(combined,OUT/'combined')
        save('peer-image.json',{'sha256':sha(peer/'base/stand.qcow2')})
    status=int(any(step['exit'] for step in steps))
except Exception as error:
    save('failure.json',{'utc':utc(),'error':str(error).replace(str(ROOT),'[stand-root]')})
finally:
    for name in owned:
        try:destroy(name)
        except Exception:status=1
    if peer.exists() and not any((peer/'vms').glob('*')):shutil.rmtree(peer)
    save('summary.json',{'utc':utc(),'controller_exit':status,'steps':steps,
        'remaining_vms':[p.name for p in (ROOT/'vms').glob('*')],
        'peer_remaining':peer.exists(),'hypothesis_outcome':'?'})
sys.exit(status)

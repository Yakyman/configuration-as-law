#!/usr/bin/env python3
"""Single-use BC1 build/validation controller, supervised by a user service."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
phase=sys.argv[1]
if phase not in ('development-1','final-1','final-2','final-3'):raise SystemExit('fresh named phase required')
OUT=ROOT/'raw/round-1'/phase
OUT.mkdir(parents=True,exist_ok=False)
ENV={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','STAND_V4_CHANNELS':'1','LAB_RUN_TIMEOUT':'7200'}
steps=[];owned=[]
def utc():return time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
def save(name,obj):(OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def run(argv,log,script=None,legacy=False,root=ROOT,required=True):
    record={'argv':[str(a).replace(str(ROOT),'[stand-root]') for a in argv],'started_utc':utc(),'log':log,'expected_exit':0,'legacy_protocol':legacy}
    print(json.dumps({'phase':'expected',**record}),flush=True)
    env={**ENV,'STAND_ROOT':str(root),'STAND_LEGACY':'1' if legacy else '0'}
    with (OUT/log).open('wb') as f:
        p=subprocess.run(argv,cwd=root,input=script.encode() if script else None,stdout=f,stderr=subprocess.STDOUT,env=env)
    record.update(exit=p.returncode,ended_utc=utc());steps.append(record);save('steps.json',steps)
    print(json.dumps(record),flush=True)
    if required and p.returncode:raise RuntimeError('stage failed: '+log)
    return p.returncode
def lab(op,name,log,script=None,extra=None):return run(['python3','lab.py',op,name,*(extra or [])],log,script)
def destroy(name):
    if (ROOT/'vms'/name).exists():
        try:lab('destroy',name,name+'-destroy.log')
        except Exception:
            lab('kill',name,name+'-kill.log');lab('destroy',name,name+'-destroy-again.log')
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
status=1
try:
    shutil.copytree(ROOT/'build',OUT/'recipe-inputs')
    save('input-sha256.json',{p.name:sha(p) for p in sorted((ROOT/'build').iterdir()) if p.is_file()})
    run(['python3','build/build.py','--server','--replace'],'build.log')
    shutil.copyfile(ROOT/'raw/recipe.log',OUT/'recipe.log')
    save('image.json',{'sha256':sha(ROOT/'base/stand.qcow2'),'mode':oct((ROOT/'base/stand.qcow2').stat().st_mode&0o777)})
    for suite in ('shell','gate','tools'):
        name='v4-'+phase+'-'+suite;owned.append(name)
        lab('new',name,suite+'-new.log',extra=['stand'])
        if suite=='shell':
            lab('run',name,'login.log',script="printf '%s\\n' 'LOGIN SHELL' | tr A-Z a-z > login.txt; cat login.txt\n")
        rc=run(['python3','lab.py','run',name,'--root'],suite+'.jsonl','python3 -B /usr/local/lib/stand/v4-'+suite+'-selftest.py\n',required=False)
        if suite=='shell':
            lab('stop',name,'shell-stop.log');lab('start',name,'shell-start.log')
            run(['python3','lab.py','run',name,'--root'],'shell-reboot.jsonl','python3 -B /usr/local/lib/stand/v4-shell-selftest.py --after\n',required=False)
        run(['python3','lab.py','run',name,'--root'],suite+'-verify.log','stand-verify\n',required=False)
        if suite=='tools':
            run(['python3','lab.py','copy-out',name,'/etc/stand/factory',str(OUT/'factory')], 'factory-export.log')
        destroy(name)
    if phase.startswith('final'):
        # Whole carried suite and complete-example replay, explicitly through
        # the retained compatibility interface. New shell assertions are above.
        peer=ROOT/'round1-peer'
        if peer.exists():raise RuntimeError('peer collision')
        peer.mkdir()
        for name in ('build','downloads','keys'):shutil.copytree(ROOT/name,peer/name)
        run(['python3','build/build.py','--server'],'peer-build.log',root=peer)
        run(['python3','build/round4-driver.py',phase,'--regressions','--peer-root','round1-peer'],'regressions-console.jsonl',legacy=True,required=False)
        evidence=ROOT/'raw/round-4'/phase
        if evidence.exists():shutil.move(evidence,OUT/'carried-suite')
        run(['python3','build/assemble-channel-examples.py',str(OUT/'carried-suite'),'round1-example'],'assemble.log',legacy=True)
        run(['python3','build/combined-selftest.py','v4-'+phase,'round1-example/combined','--peer-root','round1-peer','--reboot'],'combined-console.jsonl',legacy=True,required=False)
        combined=ROOT/'raw/round-4'/('v4-'+phase)
        if combined.exists():shutil.move(combined,OUT/'combined')
        save('peer-image.json',{'sha256':sha(peer/'base/stand.qcow2')})
    status=int(any(s['exit'] for s in steps))
except Exception as error:
    save('failure.json',{'utc':utc(),'error':str(error).replace(str(ROOT),'[stand-root]')})
finally:
    for name in owned:
        try:destroy(name)
        except Exception:status=1
    peer=ROOT/'round1-peer'
    if peer.exists() and not any((peer/'vms').glob('*')):shutil.rmtree(peer)
    remaining=[p.name for p in (ROOT/'vms').glob('*')]
    save('summary.json',{'utc':utc(),'controller_exit':status,'steps':steps,'remaining_vms':remaining,'peer_remaining':peer.exists(),'hypothesis_outcome':'?'})
sys.exit(status)

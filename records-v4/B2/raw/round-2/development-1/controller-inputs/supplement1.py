#!/usr/bin/env python3
"""One-shot Round 1 supplemental observation driver for the frozen final image."""
import hashlib,json,os,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
phase=sys.argv[1] if len(sys.argv)>1 else 'final-2'
if phase not in ('final-1','final-2','final-3'):raise SystemExit('fresh named phase required')
OUT=ROOT/'raw/round-1'/phase/'supplement'
OUT.mkdir(parents=True,exist_ok=False)
name='v4-'+phase+'-supplement';steps=[]
ENV={**os.environ,'STAND_ROOT':str(ROOT),'STAND_LEGACY':'0','PYTHONDONTWRITEBYTECODE':'1','LAB_RUN_TIMEOUT':'7200'}
def utc():return time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
def save(name,value):(OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def run(args,log,script=None,required=True):
    row={'argv':args,'utc':utc(),'log':log,'expected_exit':0,
         'stdin_sha256':hashlib.sha256(script.encode()).hexdigest() if script else None}
    print(json.dumps({'phase':'expected',**row}),flush=True)
    with (OUT/log).open('wb') as f:
        result=subprocess.run(args,input=script.encode() if script else None,stdout=f,stderr=subprocess.STDOUT,cwd=ROOT,env=ENV)
    row.update(exit=result.returncode,ended_utc=utc());steps.append(row);save('steps.json',steps)
    print(json.dumps(row),flush=True)
    if required and result.returncode:raise RuntimeError('failed '+log)
    return result.returncode
status=1
try:
    sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'tools').glob('v4-*-selftest.py')}
    save('input-sha256.json',sources)
    save('image.json',json.loads((ROOT/'raw/round-1'/phase/'image.json').read_text()))
    run(['python3','lab.py','new',name,'stand'],'new.log')
    for suite in ('direct','extra'):
        payload=(ROOT/'tools'/('v4-'+suite+'-selftest.py')).read_text()
        run(['python3','lab.py','run',name,'--root'],suite+'.jsonl',"python3 -B - <<'V4_SUPPLEMENT_PAYLOAD'\n"+payload+"\nV4_SUPPLEMENT_PAYLOAD\n",required=False)
    run(['python3','lab.py','run',name,'--root'],'before-reboot-verify.jsonl','stand-verify\n')
    run(['python3','lab.py','run',name,'--root'],'before-report.json','cat /var/lib/stand/last-success.json\n')
    run(['python3','lab.py','stop',name],'stop.log')
    run(['python3','lab.py','start',name],'start.log')
    run(['python3','lab.py','run',name,'--root'],'after-reboot-verify.jsonl','stand-verify\n')
    run(['python3','lab.py','run',name,'--root'],'after-report.json','cat /var/lib/stand/last-success.json\n')
    equal=(OUT/'before-report.json').read_bytes()==(OUT/'after-report.json').read_bytes()
    save('reboot.json',{'last_success_bytes_equal':equal,'utc':utc()})
    status=int(not equal or any(s['exit'] for s in steps))
except Exception as error:save('failure.json',{'error':str(error).replace(str(ROOT),'[stand-root]'),'utc':utc()})
finally:
    if (ROOT/'vms'/name).exists():
        try:run(['python3','lab.py','destroy',name],'destroy.log')
        except Exception:status=1
    save('summary.json',{'controller_exit':status,'utc':utc(),'steps':steps,
                        'remaining_owned_vm':(ROOT/'vms'/name).exists(),
                        'exit_semantics':'Completion only; property and ordinary-work failures stay in result rows',
                        'hypothesis_outcome':'?'})
raise SystemExit(status)

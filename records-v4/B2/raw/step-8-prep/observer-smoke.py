#!/usr/bin/env python3
"""One preparatory collector integration check; performs no history action."""
import hashlib,json,pathlib,subprocess,sys,time
ROOT=pathlib.Path.cwd()
OUT=ROOT/'raw/step-8-prep/observer-smoke'
OUT.mkdir(parents=True,exist_ok=False)
VM='prep-s8-observer'
records=[]
def save(name,value):
    (OUT/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
def run(name,args,data=None,timeout=900):
    row={'command':name,'argv':[str(x).replace(str(ROOT),'<stand-root>') for x in args],
         'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
    try:
        with (OUT/(name+'.stdout')).open('wb') as out,(OUT/(name+'.stderr')).open('wb') as err:
            p=subprocess.run(args,input=data,stdout=out,stderr=err,timeout=timeout)
        row['exit']=p.returncode
    except subprocess.TimeoutExpired:row.update(exit=None,error='TimeoutExpired')
    row['ended_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    records.append(row);save('commands.json',records)
    return row['exit']
lab=[sys.executable,str(ROOT/'lab.py')]
if (ROOT/'vms'/VM).exists():raise RuntimeError('owned name already exists')
save('expected.json',{
 'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
 'kind':'preparation collector integration, not a history or property attempt',
 'source_review':['cases-8/observe.py','build/bc4-compare.py','build/lab.py','build/bc3_filesystem.py:read'],
 'unanswered':'New combined collector has not been run with the final image Python/native readers.',
 'expected':'Root stdin collection produces one parseable JSON with independent census, all required rows and explicit errors/limits; no guest helper is installed, no history action is executed.',
 'repeat_policy':'One run only; preserve failure and do not change the image.'})
try:
    if run('create',lab+['new',VM,'stand'],timeout=240)!=0:raise RuntimeError('creation failed')
    source=(ROOT/'cases-8/observe.py').read_bytes()
    save('source.json',{'sha256':hashlib.sha256(source).hexdigest()})
    rc=run('collector',lab+['run',VM,'--root'],data=source)
    result=json.loads((OUT/'collector.stdout').read_text())
    save('summary.json',{
      'transport_exit':rc,'format':result.get('format'),'collection_error':result.get('collection_error'),
      'files':len(result.get('independent_census',{}).get('files',{})),
      'machine_rows':len(result.get('p2_rows',{})),
      'filesystems':list(result.get('p2_filesystems',{})),
      'declaration_stable':result.get('declaration_stable'),
      'success_reports_stable':result.get('success_reports_stable'),
      'hypothesis_outcome':'not assigned; integration check only'})
except Exception as e:
    save('failure.json',{'error':type(e).__name__,'message':str(e).replace(str(ROOT),'<stand-root>')})
finally:
    if (ROOT/'vms'/VM).exists():
        if run('stop',lab+['stop',VM],timeout=140)!=0:run('kill',lab+['kill',VM],timeout=30)
        run('destroy',lab+['destroy',VM],timeout=150)
    save('cleanup.json',{'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'owned_guest_exists':(ROOT/'vms'/VM).exists()})

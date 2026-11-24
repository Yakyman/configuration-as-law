#!/usr/bin/env python3
"""Construct fixed declarations on separate disposable copies; never run cases.

Only fixture installation and desired-state export occur here. There is no pair
comparison, opposite-order trial, removal sequence, or hypothesis outcome.
"""
import hashlib,json,os,pathlib,shutil,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/'raw/round-4-prep/inputs';OUT.mkdir(parents=True,exist_ok=False)
DEST=ROOT/'cases-6';DEST.mkdir(exist_ok=False)
def save(n,v):(OUT/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
def run(label,args,script=None):
    (OUT/(label+'.command.json')).write_text(json.dumps({'argv':args,'stdin':script},indent=2)+'\n')
    with (OUT/(label+'.log')).open('wb') as f:
        result=subprocess.run([sys.executable,'lab.py',*args],input=script.encode() if script else None,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
    (OUT/(label+'.exit')).write_text(str(result.returncode)+'\n')
    if result.returncode:raise RuntimeError('preparation command failed: '+label)

scenarios={
 'accounts':'stand-pkg install /usr/local/share/stand/bc4/package-alpha.json\nstand-pkg install /usr/local/share/stand/bc4/package-beta.json\n',
 'removal':'stand-pkg install /usr/local/share/stand/dev/worker-1.json\nstand-line add /usr/local/share/stand/dev/service.json\nstand-line add /usr/local/share/stand/dev/rule.json\n',
 'both-owners':'stand-pkg install /usr/local/share/stand/bc4/removal/bc4-owner-a.json\nstand-pkg install /usr/local/share/stand/bc4/removal/bc4-owner-b.json\n',
}
def remove_input(ids,destination):
    return '''set -eu
python3 -B - <<'PY'
import pathlib,json,shutil
source=pathlib.Path('/var/lib/stand/current')
target=pathlib.Path('/var/lib/stand/bc4-construction-candidate')
target.mkdir(exist_ok=True)
for p in source.iterdir():shutil.copyfile(p,target/p.name)
removed='''+repr(ids)+'''
lines=(source/'machine.jsonl').read_text().splitlines(keepends=True)
assert {json.loads(s)['id'] for s in lines}.issuperset(removed)
(target/'machine.jsonl').write_text(''.join(s for s in lines if json.loads(s)['id'] not in removed))
PY
stand-apply /var/lib/stand/bc4-construction-candidate
python3 -B /usr/local/lib/stand/bc4_bundle.py export /var/lib/stand/'''+destination+'\n'
save('expected.json',{'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'expected':'Each fixture configuration installs and exports exact existing-format complete desired input; no case outcome observed','scenarios':scenarios})
for name,setup in scenarios.items():
    vm='bc4-prepare-'+name
    try:
        run(name+'-new',['new',vm,'stand'])
        script='set -eu\n'+setup+'stand-verify\npython3 -B /usr/local/lib/stand/bc4_bundle.py export /var/lib/stand/bc4-export\n'
        run(name+'-construct',['run',vm,'--root'],script)
        run(name+'-export',['copy-out',vm,'/var/lib/stand/bc4-export',str(OUT/name)])
        if name=='removal':
            run(name+'-construct-after',['run',vm,'--root'],remove_input(['dev-worker','dev-service','dev-rule'],'bc4-after'))
            run(name+'-export-after',['copy-out',vm,'/var/lib/stand/bc4-after',str(OUT/name)])
        if name=='both-owners':
            for label,ids in [('one',['bc4:owner-a']),('none',['bc4:owner-b'])]:
                run(name+'-construct-'+label,['run',vm,'--root'],remove_input(ids,'bc4-'+label))
                run(name+'-export-'+label,['copy-out',vm,'/var/lib/stand/bc4-'+label,str(OUT/name)])
    finally:
        if (ROOT/'vms'/vm).exists():run(name+'-destroy',['destroy',vm])
mapping={'case-1':'removal/bc4-export','case-2a':'accounts/bc4-export','case-3-before':'removal/bc4-export','case-3-after':'removal/bc4-after',
         'case-4-both':'both-owners/bc4-export','case-4-one':'both-owners/bc4-one','case-4-none':'both-owners/bc4-none'}
for name,source in mapping.items():shutil.copytree(OUT/source,DEST/name)
save('mapping.json',mapping)
print('Prepared seven complete declaration inputs; no second-party case performed')

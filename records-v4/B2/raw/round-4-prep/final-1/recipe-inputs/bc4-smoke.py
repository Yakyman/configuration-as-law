#!/usr/bin/env python3
"""Single-package replay integration trial, not a step-6 case."""
import json,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/'raw/round-4-prep/smoke-1';OUT.mkdir(parents=True,exist_ok=False)
script='''set -eu
stand-pkg install /usr/local/share/stand/bc4/package-alpha.json
getent passwd bc4alpha
python3 -B /usr/local/lib/stand/bc4_bundle.py export /var/lib/stand/bc4-smoke-input
python3 -B /usr/local/lib/stand/bc4_bundle.py apply /var/lib/stand/bc4-smoke-input
'''
(OUT/'expected.json').write_text(json.dumps({'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'expected':'one package creates its exact account; complete exported description reapplies with exact bytes and successful machine/filesystem readback','scope':'fixture integration only; no step-6 case','stdin':script},indent=2)+'\n')
def run(label,args,data=None):
    with (OUT/(label+'.log')).open('wb') as f:r=subprocess.run([sys.executable,'lab.py',*args],cwd=ROOT,input=data.encode() if data else None,stdout=f,stderr=subprocess.STDOUT)
    (OUT/(label+'.exit')).write_text(str(r.returncode)+'\n')
    return r.returncode
status=1
try:
    if run('new',['new','bc4-smoke','stand'])==0:status=run('trial',['run','bc4-smoke','--root'],script)
finally:
    if (ROOT/'vms/bc4-smoke').exists():run('destroy',['destroy','bc4-smoke'])
(OUT/'result.json').write_text(json.dumps({'exit':status,'case_outcome':'not attempted'})+'\n')
raise SystemExit(status)

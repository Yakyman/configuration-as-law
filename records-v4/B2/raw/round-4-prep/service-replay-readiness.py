#!/usr/bin/env python3
"""Single complete-input fixture replay readiness; no paired case or removal observation."""
import importlib.util,json,pathlib,subprocess,sys,tarfile,tempfile,time
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'raw/round-4-prep/service-readiness';OUT.mkdir(parents=True,exist_ok=False)
(OUT/'expected.json').write_text(json.dumps({'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'source':'bc3_filesystem.py apply_description and fixed case-3-before filesystem path maps','question':'Can the active-service fixture complete replay with a fresh PrivateTmp namespace and exact target filesystem descriptions?','expected':'complete replay succeeds or explicitly refuses an incompatible open handle; no refusal can be called readiness','scope':'one fixture application only; no pair comparison, removed process observation, opposite order or case outcome'},indent=2)+'\n')
spec=importlib.util.spec_from_file_location('lab',ROOT/'lab.py');lab=importlib.util.module_from_spec(spec);spec.loader.exec_module(lab)
def run(label,args,data=None):
 with (OUT/(label+'.log')).open('wb') as f:r=subprocess.run([sys.executable,'lab.py',*args],cwd=ROOT,input=data.encode() if data else None,stdout=f,stderr=subprocess.STDOUT)
 (OUT/(label+'.exit')).write_text(str(r.returncode)+'\n')
 if r.returncode:raise RuntimeError('fixture readiness command failed: '+label)
vm='bc4-service-readiness'
if (ROOT/'vms'/vm).exists():raise RuntimeError('existing guest')
try:
 run('new',['new',vm,'stand'])
 run('stage-directory',['run',vm,'--root'],'mkdir -p /var/lib/stand/bc4-inputs\n')
 with tempfile.TemporaryFile() as archive:
  with tarfile.open(fileobj=archive,mode='w') as t:t.add(ROOT/'cases-6/case-3-before',arcname='case-3-before')
  archive.seek(0)
  with (OUT/'stage.log').open('wb') as f:subprocess.run(lab.ssh(ROOT/'vms'/vm,root=True)+['tar -xf - -C /var/lib/stand/bc4-inputs'],stdin=archive,stdout=f,stderr=subprocess.STDOUT,check=True)
 run('replay',['run',vm,'--root'],'python3 -B /usr/local/lib/stand/bc4_bundle.py apply /var/lib/stand/bc4-inputs/case-3-before\n')
finally:
 if (ROOT/'vms'/vm).exists():run('destroy',['destroy',vm])
print('Single service fixture replay readiness completed; no case outcome assigned')

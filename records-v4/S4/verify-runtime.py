#!/usr/bin/env python3
"""Verify final-run executable inputs against the assembled instrument."""
import csv,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent

def hashes(path):
 text=path.read_text();out={}
 if text.startswith(('file\t','path\t')):
  for row in csv.DictReader(text.splitlines(),delimiter='\t'):out[row.get('file',row.get('path'))]=row['sha256']
 else:
  for line in text.splitlines():
   digest,name=line.split(None,1);out[name.strip()]=digest
 return {k.removeprefix('S4/'):v for k,v in out.items()}

specs={
'alma':('rehearsal/alma/round3','source-before.sha256','source-after.sha256',['main.py','extended.py','packages.py','extra_alma.py','extra_void.py','probe.go','probe-linux-amd64.gz']),
'void':('rehearsal/void/round3','input-sha256.tsv','input-sha256-after.tsv',['main.py','extended.py','packages.py','extra_void.py','probe.go','probe-linux-amd64.gz']),
'microos':('rehearsal/microos/round-3','before.sha256.tsv','after.sha256.tsv',['main.py','extended.py','packages.py','extra_microos.py','probe.go','probe-linux-amd64.gz']),
'gentoo':('rehearsal/gentoo/round2','source-before.sha256','source-after.sha256',['main.py','extended.py','packages.py','probe.go','probe-linux-amd64.gz'])}
results={}
for system,(directory,before,after,names) in specs.items():
 a=hashes(R/directory/before);b=hashes(R/directory/after);checked=[]
 for name in names:
  key='collector/'+name;actual=hashlib.sha256((R/key).read_bytes()).hexdigest()
  assert a[key]==b[key]==actual,(system,key)
  checked.append(key)
 results[system]={'before_after_local_equal':True,'files':checked,'evidence':directory}
talos=hashes(R/'rehearsal/talos/content-final/source-hashes.tsv')
checked=[]
for name in ('main.py','extended.py','talos.py','extra_talos.py'):
 key='collector/'+name
 assert talos[key]==hashlib.sha256((R/key).read_bytes()).hexdigest(),key
 checked.append(key)
results['talos']={'final_source_local_equal':True,'files':checked,'evidence':'rehearsal/talos/content-final','irrelevant_test_difference':'collector/parser-tests.py fixture mode/tempdir update is not runtime-loaded'}
assert (R/'collect.sh').read_bytes()==(R.parent/'C1/collect.sh').read_bytes()
(R/'raw/runtime-hash-check.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
print('PASS: selected final runtime source/binary hashes for all five systems; wrapper unchanged')

#!/usr/bin/env python3
"""One named preparation scratch build; never run the step-6 cases."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
phase=sys.argv[1]
if phase not in ('development-1','development-2','final-1','final-2'):raise SystemExit('unused named phase required')
OUT=ROOT/'raw/round-4-prep'/phase;OUT.mkdir(parents=True,exist_ok=False)
def sha(p):
    with p.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def save(name,value):(OUT/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
shutil.copytree(ROOT/'build',OUT/'recipe-inputs')
save('input-sha256.json',{p.name:sha(p) for p in sorted((ROOT/'build').iterdir()) if p.is_file()})
save('expected.json',{'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'expected':'scratch recipe completes with fixture sources and complete declaration application support; no case performed','command':'python3 build/build.py --server --replace'})
with (OUT/'build.log').open('wb') as output:
    result=subprocess.run([sys.executable,'build/build.py','--server','--replace'],cwd=ROOT,stdout=output,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
save('result.json',{'exit':result.returncode,'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})
if result.returncode==0:save('image.json',{'sha256':sha(ROOT/'base/stand.qcow2'),'mode':oct((ROOT/'base/stand.qcow2').stat().st_mode&0o777)})
raise SystemExit(result.returncode)

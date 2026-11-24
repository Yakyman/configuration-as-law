#!/usr/bin/env python3
"""Single-use scratch build; snapshots every source and preserves failed output."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
phase=sys.argv[1]
if not phase.startswith(('development-','final-')) or '/' in phase:raise SystemExit('named phase required')
OUT=ROOT/'raw/round-3'/phase
OUT.mkdir(parents=True,exist_ok=False)
def sha(p):
    with p.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def save(n,v):(OUT/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
shutil.copytree(ROOT/'build',OUT/'recipe-inputs')
save('input-sha256.json',{p.name:sha(p) for p in sorted((ROOT/'build').iterdir()) if p.is_file()})
save('expected.json',{'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'expected':'scratch recipe completes; same frozen source used by new guests','command':'python3 build/build.py --server --replace'})
with (OUT/'build.log').open('wb') as log:
    r=subprocess.run([sys.executable,'build/build.py','--server','--replace'],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
save('build-result.json',{'exit':r.returncode,'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})
if r.returncode==0:
    save('image.json',{'sha256':sha(ROOT/'base/stand.qcow2'),'mode':oct((ROOT/'base/stand.qcow2').stat().st_mode&0o777)})
raise SystemExit(r.returncode)

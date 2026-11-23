#!/usr/bin/env python3
"""Run the predeclared builder-only observations on disposable clean overlays."""
import importlib.util,json,os,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
RAW=ROOT/'raw'/os.environ.get('STAND_EVIDENCE_DIR','legacy');RAW.mkdir(parents=True,exist_ok=True)
if not RAW.resolve().is_relative_to((ROOT/'raw').resolve()):raise ValueError('evidence must remain under raw')
created=[]
def run(name,args,data=None):
    print(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())+' '+name,flush=True)
    with (RAW/(name+'.log')).open('wb') as out:
        p=subprocess.run(list(map(str,args)),input=data,stdout=out,stderr=subprocess.STDOUT,cwd=ROOT)
    print(name+' EXIT '+str(p.returncode),flush=True)
    if p.returncode:raise RuntimeError(name+' failed; preserve this observation')
def lab(name,*args,script=None):
    run(name,[sys.executable,ROOT/'lab.py',*args],script.encode() if script else None)
def new(name):
    created.append(name);lab('create-'+name,'new',name,'stand')
def operation(vm,op,label):
    lab(label,'run',vm,'--root',script='python3 -B /usr/local/lib/stand/selftest.py '+op+'\n')
def main():
    try:
        new('dev')
        for label,op in [('D01','factory'),('D02','add'),('D03','invalid'),('D04','admission'),('D05','frontends'),('D08','work'),('D09','radio'),('D06','remove')]:operation('dev',op,label)
        lab('export-dev','copy-out','dev','/var/lib/stand/evidence',RAW/'dev')
        lab('export-example','copy-out','dev','/etc/stand/factory',RAW/'example')
        lab('destroy-dev','destroy','dev');created.remove('dev')
        for vm in ('peer-a','peer-b'):
            new(vm);operation(vm,'add','D10-'+vm)
            lab('export-'+vm,'copy-out',vm,'/var/lib/stand/evidence/added.json',RAW/vm)
            lab('export-declaration-'+vm,'copy-out',vm,'/var/lib/stand/dev-add',RAW/vm)
            lab('destroy-'+vm,'destroy',vm);created.remove(vm)
        sys.path.insert(0,str(ROOT/'build'));import stand
        with (RAW/'D10-compare.jsonl').open('w') as out:
            old=sys.stdout
            try:
                sys.stdout=out;status=stand.compare(RAW/'peer-a/added.json',RAW/'peer-b/added.json')
            finally:sys.stdout=old
        a=RAW/'peer-a/dev-add';b=RAW/'peer-b/dev-add'
        identical=all((a/p.name).read_bytes()==p.read_bytes() for p in b.iterdir())
        (RAW/'D10-summary.log').write_text('DECLARATION_BYTES_EQUAL '+str(identical)+'\nCOMPARE_EXIT '+str(status)+'\n')
        if status or not identical:raise RuntimeError('D10 comparison differs')
        new('cut')
        run('D07',[sys.executable,ROOT/'build/powercut.py','cut'])
        lab('export-cut','copy-out','cut','/var/lib/stand/last-success.json',RAW/'cut')
        print('DEVELOPMENT OBSERVATIONS COMPLETE',flush=True)
    finally:
        for vm in list(created):
            if not (ROOT/'vms'/vm).is_dir():continue
            try:lab('cleanup-'+vm,'destroy',vm)
            except Exception:
                lab('kill-cleanup-'+vm,'kill',vm);lab('destroy-cleanup-'+vm,'destroy',vm)
        print('DISPOSABLE VM CLEANUP COMPLETE',flush=True)
if __name__=='__main__':main()

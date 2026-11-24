import pathlib,subprocess as sp,time,json,os,shutil,hashlib
R=pathlib.Path(__file__).resolve().parent;L=R/'lab';D=R/'transient';O=R/'raw';N='fx-s4-p-3-talos'; O.mkdir(exist_ok=True);D.mkdir(exist_ok=True)
def run(label,args,stdin=None,limit=600):
 t=time.monotonic();p=sp.run(args,input=stdin,stdout=sp.PIPE,stderr=sp.PIPE,timeout=limit)
 (D/(label+'.out')).write_bytes(p.stdout);(D/(label+'.err')).write_bytes(p.stderr)
 with (O/'status.tsv').open('a') as f:f.write(f'{label}\t{p.returncode}\t{time.monotonic()-t:.3f}\t{len(p.stdout)}\t{len(p.stderr)}\n')
 return p.returncode
if __name__=='__main__':
 (O/'status.tsv').write_text('operation\texit_status\tduration_seconds\tstdout_bytes\tstderr_bytes\n')
 run('boot',[str(L/'lab.sh'),'new',N,'talos'])
 (O/'boot-complete').touch()

import pathlib,subprocess as sp,time,os,json,tarfile,io,base64,shlex,shutil,re
R=pathlib.Path(__file__).resolve().parents[2]; LAB=R/'lab-microos'; OUT=R/'rehearsal/microos/round-2'; NAME='reh-s4-microos-2'
OUT.mkdir(parents=True,exist_ok=True)
def record(label,rc,duration):
 with (OUT/'status.tsv').open('a') as f:f.write(f'{label}\t{rc}\t{duration:.3f}\n')
def call(label,args,data=None,timeout=2400,capture=False):
 t=time.monotonic();p=sp.run(args,input=data,stdout=sp.PIPE if capture else sp.DEVNULL,stderr=sp.PIPE,timeout=timeout,env={**os.environ,'LAB_SEPARATE_STDERR':'1','LAB_ROOT':str(LAB),'C1_INLINE_COUNTS':'1','LAB_REHEARSAL_COUNTS':str(OUT/'counts.tsv'),'LAB_REHEARSAL_ROUND':'2'})
 err=p.stderr.decode(errors='replace').replace(str(R),'S4');err=re.sub(r'/home/[^/\s]+','HOST_HOME',err)
 (OUT/(label+'.stderr')).write_text(err);record(label,p.returncode,time.monotonic()-t);return p

def run(label,script,capture=False,timeout=300):return call(label,[str(LAB/'lab.sh'),'run',NAME,'--timeout',str(timeout)],script.encode(),timeout+15,capture)
(OUT/'status.tsv').write_text('operation\texit_status\tduration_seconds\n')
try:
 p=call('boot',[str(LAB/'lab.sh'),'new',NAME,'microos'],timeout=600)
 if p.returncode:raise RuntimeError('boot failed')
 transient=OUT/'.inventory-unread'
 p=call('collector',[str(R/'collect.sh'),'--rehearsal',NAME,str(transient)],timeout=2400)
 if (transient/'coverage.tsv').exists():shutil.copyfile(transient/'coverage.tsv',OUT/'coverage.tsv')
 for path in (transient/'raw').glob('*.err'):
  text=path.read_text(errors='replace').replace(str(R),'S4');text=re.sub(r'/home/[^/\s]+','GUEST_HOME',text)
  (OUT/path.name).write_text(text)
finally:
 shutil.rmtree(OUT/'.inventory-unread',ignore_errors=True)
 p=call('destroy',[str(LAB/'lab.sh'),'destroy',NAME],timeout=180)
 if p.returncode:
  call('kill',[str(LAB/'lab.sh'),'kill',NAME],timeout=60)
  call('destroy-fallback',[str(LAB/'lab.sh'),'destroy',NAME],timeout=180)
 (OUT/'finished').touch()

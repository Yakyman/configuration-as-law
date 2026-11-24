import pathlib,subprocess as sp,time,os,json,shutil,re,hashlib
R=pathlib.Path(__file__).resolve().parents[2];LAB=R/'lab-talos';OUT=R/'rehearsal/talos/content-final';NAME='reh-s4-talos-content-final'
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'status.tsv').write_text('operation\texit_status\tduration_seconds\n')
def call(label,args,timeout=2400):
 t=time.monotonic();p=sp.run(args,stdout=sp.DEVNULL,stderr=sp.PIPE,timeout=timeout,env={**os.environ,'LAB_ROOT':str(LAB),'LAB_SEPARATE_STDERR':'1','C1_INLINE_COUNTS':'1'})
 err=re.sub(r'/home/[^/\s]+','HOST_HOME',p.stderr.decode(errors='replace').replace(str(R),'S4'));(OUT/(label+'.stderr')).write_text(err)
 with (OUT/'status.tsv').open('a') as f:f.write(f'{label}\t{p.returncode}\t{time.monotonic()-t:.3f}\n')
 return p
try:
 (OUT/'source-hashes.tsv').write_text('file\tsha256\n'+''.join(str(p.relative_to(R))+'\t'+hashlib.sha256(p.read_bytes()).hexdigest()+'\n' for p in sorted((R/'collector').glob('*.py'))))
 if call('boot',[str(LAB/'lab.sh'),'new',NAME,'talos'],600).returncode:raise RuntimeError('boot failed')
 transient=OUT/'.inventory-unread'
 p=call('collector',[str(R/'collect.sh'),'--rehearsal',NAME,str(transient)])
 if (transient/'coverage.tsv').exists():shutil.copyfile(transient/'coverage.tsv',OUT/'coverage.tsv')
 for path in (transient/'raw').glob('*.err'):
  err=re.sub(r'/home/[^/\s]+','HOST_HOME',path.read_text(errors='replace').replace(str(R),'S4'));(OUT/path.name).write_text(err)
finally:
 shutil.rmtree(OUT/'.inventory-unread',ignore_errors=True)
 if call('destroy',[str(LAB/'lab.sh'),'destroy',NAME],180).returncode:
  call('kill',[str(LAB/'lab.sh'),'kill',NAME],60);call('destroy-fallback',[str(LAB/'lab.sh'),'destroy',NAME],180)
 (OUT/'finished').touch()

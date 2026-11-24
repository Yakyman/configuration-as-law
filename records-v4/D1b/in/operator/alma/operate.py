import pathlib,subprocess as sp,time,json,tarfile,io,base64,os,fcntl
start=time.time(); R=pathlib.Path.cwd(); O=R/'D1b/in/operator/alma'; O.mkdir(parents=True,exist_ok=True)
os.environ['LAB_SEPARATE_STDERR']='1'
def call(label,args,data=None):
 t=time.time()
 with (O/(label+'.stdout')).open('wb') as a,(O/(label+'.stderr')).open('wb') as b:
  p=sp.run(args,input=data,stdout=a,stderr=b)
 with (O/'status.tsv').open('a') as f:f.write(f'{label}\t{p.returncode}\t{time.time()-t:.3f}\t{time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())}\n')
 return p.returncode
def run(label,script,limit=90):return call(label,['./lab.sh','run','d1b-alma','--timeout',str(limit)],script.encode())
free=0
for n in range(1,13):
 with (R/'slots'/f'slot-{n}.lock').open('a') as f:
  try:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);free+=1
  except BlockingIOError:pass
(O/'slots.txt').write_text(str(free)+' free shared slots before creation\n')
if free<1:raise SystemExit('No slot available: no creation attempted')
try:
 rc=call('new',['./lab.sh','new','d1b-alma','alma'])
 if rc:raise SystemExit(rc)
 data=io.BytesIO()
 with tarfile.open(fileobj=data,mode='w:gz') as tf:tf.add('C1/actions',arcname='actions')
 encoded=base64.b64encode(data.getvalue()).decode()
 script='''#!/bin/bash
set -e
mkdir "$HOME/d1b-actions"
base64 -d <<'PAYLOAD' | tar -xz -C "$HOME/d1b-actions"
'''+encoded+'''\nPAYLOAD
cat > "$HOME/d1b-actions/start.sh" <<'START'
#!/bin/bash
cd "$HOME/d1b-actions/actions"
bash alma.sh > "$HOME/d1b-actions/stdout" 2> "$HOME/d1b-actions/stderr"
printf '%s\\n' "$?" > "$HOME/d1b-actions/exit"
START
chmod +x "$HOME/d1b-actions/start.sh"
nohup setsid bash "$HOME/d1b-actions/start.sh" </dev/null >/dev/null 2>&1 &
printf '%s\\n' "$!" > "$HOME/d1b-actions/pid"
'''
 if run('actions-start',script):raise SystemExit('Action staging failed; no retry')
 i=0
 while True:
  time.sleep(30);i+=1
  rc=run('monitor-'+str(i),'test -f "$HOME/d1b-actions/exit"\n')
  if rc==0:break
  if time.time()-start>13500:raise SystemExit('Operator deadline; no observation')
 script='''#!/bin/bash
set -e
tar -C "$HOME" -czf - actions-status.tsv actions-logs d1b-actions/exit d1b-actions/stdout d1b-actions/stderr | base64
'''
 if run('actions-copy',script):raise SystemExit('Action copy failed; no retry')
 with tarfile.open(fileobj=io.BytesIO(base64.b64decode((O/'actions-copy.stdout').read_bytes()))) as tf:tf.extractall(O/'action-evidence',filter='data')
 if run('actions-remove','rm -rf -- "$HOME/actions-status.tsv" "$HOME/actions-logs" "$HOME/d1b-actions"\n'):raise SystemExit('Action scaffolding cleanup failed')
 envcmd='C1_INPUTS_COMMIT="c62afbb5861fb038aa7da0aa00c0730ad140ec7c" LAB_ROOT="$PWD" "$PWD/S4/fix-s4-p-3/collect.sh" --observe d1b-alma D1b/raw/alma'
 call('collector',['bash','-c',envcmd])
finally:
 if (R/'C1/vms/d1b-alma').exists():
  if call('destroy',['./lab.sh','destroy','d1b-alma']):
   call('kill',['./lab.sh','kill','d1b-alma']);call('destroy-after-kill',['./lab.sh','destroy','d1b-alma'])
 (O/'finished').write_text(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())+'\n')

import pathlib,subprocess,os,json,time,datetime,hashlib,shlex,traceback,sys
D=pathlib.Path(__file__).resolve().parent;os.chdir(D)
OUT=D/'results';OUT.mkdir(exist_ok=True)
DEADLINE=datetime.datetime.fromisoformat('2026-11-19T12:16:13+00:00').timestamp()
SSH=['ssh','-F','/dev/null','-i',str(D/'key-root'),'-o','BatchMode=yes','-o','ConnectTimeout=3','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(D/'known_hosts'),'-p','23442','root@127.0.0.1']
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def control(a):
 r=subprocess.run(['python3',str(D/'control.py'),a],capture_output=True,text=True,timeout=95)
 if r.returncode:raise RuntimeError((a,r.stdout,r.stderr))
 return json.loads(r.stdout)
def command(folder,label,cmd,timeout=140):
 start=time.monotonic_ns();p=subprocess.Popen(SSH+[cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 try:stdout,stderr=p.communicate(timeout=timeout)
 except subprocess.TimeoutExpired:
  p.kill();stdout,stderr=p.communicate();rc='timeout'
 else:rc=p.returncode
 received=time.monotonic_ns()
 (folder/(label+'.stdout')).write_bytes(stdout);(folder/(label+'.stderr')).write_bytes(stderr)
 meta={'command':SSH+[cmd],'start_monotonic_ns':start,'complete_response_and_exit_monotonic_ns':received,'rc':rc,'utc':now(),'stdout_sha256':hashlib.sha256(stdout).hexdigest(),'stderr_sha256':hashlib.sha256(stderr).hexdigest()}
 save(folder/(label+'.command.json'),meta)
 return meta,stdout
def ack(folder,label,args):
 m,b=command(folder,label,'/usr/local/bin/calctl '+shlex.join(args))
 try:
  o=json.loads(b);good=m['rc']==0 and b.endswith(b'\n') and isinstance(o,dict) and o.get('ok') is True
  if args[0] in ('apply','rollback'):good=good and isinstance(o.get('generation'),str) and o.get('effective',{}).get('generation')==o['generation']
  else:good=good and isinstance(o.get('generations'),list) and isinstance(o.get('current'),dict)
 except Exception:o=None;good=False
 m.update(ack_valid=bool(good),response=o,args=args);save(folder/(label+'.ack.json'),m)
 if not good:raise RuntimeError('No genuine successful ACK: '+label)
 return m
def snap(folder,label):
 m,b=command(folder,label,'python3 /root/p42/snapshot.py')
 assert m['rc']==0,(label,m)
 o=json.loads(b);assert o['uuid']=='e9d11119-0042-4042-8042-000000000042',o['uuid']
 save(folder/(label+'.json'),o);return o
def ready(folder,label,oldboot=None):
 start=time.monotonic();last=None
 for i in range(60):
  m,b=command(folder,label+f'-{i:02}','cat /proc/sys/kernel/random/boot_id; /usr/local/bin/calctl status',10)
  if m['rc']==0:
   try:
    boot,body=b.decode().split('\n',1);j=json.loads(body)
    if j.get('ok') is True and (oldboot is None or boot!=oldboot):return
   except Exception:pass
  if time.monotonic()-start>120:break
  time.sleep(.5)
 raise RuntimeError('guest readiness failed')
def declaration(mode,owners):return {'archive':mode,'programs':{x:{'version':'1','scope':'system','owners':[]} for x in owners},'policies':{},'allow_channels':{},'shared':{'lookup':['alpha','beta']}}
def publish(folder,label,doc):
 b=(json.dumps(doc,sort_keys=True,indent=2)+'\n').encode();(folder/(label+'.input.json')).write_bytes(b)
 import base64
 script="import pathlib,base64; pathlib.Path('/etc/cal/root.json').write_bytes(base64.b64decode('"+base64.b64encode(b).decode()+"'))"
 m,_=command(folder,label,'python3 -c '+shlex.quote(script));assert m['rc']==0
def native(folder,label,owner,verb,path='',key='',confined=True):
 args=['/usr/local/lib/cal/'+owner,verb]+([path,key] if path else [])
 cmd=shlex.join(args)
 if confined:cmd='runuser -u alice -- /usr/local/bin/cal-login -c '+shlex.quote(cmd)
 return command(folder,label,cmd)
def observe_access(folder,label,snapshot,key):
 results={}
 # Actual payload execution for both retained fixture versions, independent of launch policy.
 for owner in ('alpha','beta'):
  m,b=native(folder,label+'-'+owner+'-payload',owner,'identity',confined=False);results[owner+'-payload']={'rc':m['rc'],'stdout':b.decode()}
 current=snapshot['files'].get('/var/lib/cal/current.json',{}).get('json',{})
 for owner in current.get('programs',{}):
  if owner not in ('alpha','beta'):continue
  m,b=native(folder,label+'-'+owner+'-lookup',owner,'lookup','/var/lib/cal/active/shared-lookup/lookup',key)
  results[owner+'-lookup']={'rc':m['rc'],'stdout':b.decode()}
 save(folder/(label+'.access.json'),results)
 return results
def run_row(op,mode,cut,ident=None):
 if time.time()>=DEADLINE:raise RuntimeError('probe cutoff reached')
 ident=ident or f'{op}-{mode}-{cut}';folder=OUT/ident;folder.mkdir()
 meta={'id':ident,'op':op,'policy':mode,'cut':cut,'start_utc':now(),'primary':cut in ('immediate','sync') and not ident.startswith('replay-')}
 save(folder/'meta.json',meta);print(now(),'BEGIN',ident,flush=True)
 try:
  meta['reset']=control('reset');ready(folder,'boot-ready')
  import base64
  script="import pathlib,base64;pathlib.Path('/root/p42/snapshot.py').write_bytes(base64.b64decode('"+base64.b64encode((D/'snapshot.py').read_bytes()).decode()+"'))"
  m,_=command(folder,'install-observer','python3 -c '+shlex.quote(script));assert m['rc']==0
  initial=snap(folder,'baseline')
  # Every row starts with the same sealed empty baseline and its own cache key.
  key=ident
  publish(folder,'G1-publish',declaration(mode,['alpha','beta']))
  g1=ack(folder,'G1-apply',['apply'])['response']['generation']
  m,_=native(folder,'create','alpha','create','/var/lib/cal/active/shared-lookup/lookup',key,False);assert m['rc']==0
  for owner in ('alpha','beta'):
   m,_=native(folder,'initial-read-'+owner,owner,'lookup','/var/lib/cal/active/shared-lookup/lookup',key);assert m['rc']==0
  # Negative dependence: same program/key fails with the actual cache temporarily absent.
  m,_=command(folder,'hide-cache','mv /var/lib/cal/active/shared-lookup/lookup /var/lib/cal/active/shared-lookup/lookup.hidden');assert m['rc']==0
  m,_=native(folder,'missing-read','beta','lookup','/var/lib/cal/active/shared-lookup/lookup',key);assert m['rc']==3
  m,_=command(folder,'restore-cache','mv /var/lib/cal/active/shared-lookup/lookup.hidden /var/lib/cal/active/shared-lookup/lookup');assert m['rc']==0
  publish(folder,'G2-publish',declaration(mode,['beta']))
  g2=ack(folder,'G2-apply',['apply'])['response']['generation']
  s2=snap(folder,'G2');m,_=native(folder,'remaining-owner-read','beta','lookup','/var/lib/cal/active/shared-lookup/lookup',key);assert m['rc']==0
  if op in ('G','B'):
   publish(folder,'G3-publish',declaration(mode,[]));g3=ack(folder,'G3-apply',['apply'])['response']['generation']
  else:
   publish(folder,'requested-publish',declaration(mode,[]));g3=None
  # Durably establish preparation AND intended input file. Never sync inside measured operation.
  m,_=command(folder,'prepare-sync','sync');assert m['rc']==0
  before=snap(folder,'before');assert not before['live_consumers'],before['live_consumers']
  owning=[p.rsplit('/',1)[1][:-5] for p,r in before['files'].items() if '/generations/' in p and set(r.get('json',{}).get('programs',{}))&{'alpha','beta'}]
  assert set(owning)=={g1,g2},owning
  args={'R':['apply'],'G':['gc',*sorted(owning)],'B':['rollback',g2]}[op]
  meta.update(g1=g1,g2=g2,g3=g3,owning_before=owning,key=key,measured_args=args)
  if time.time()>=DEADLINE:raise RuntimeError('probe cutoff before measured command')
  measured=ack(folder,'measured',args);meta['ack']=measured
  # Mandatory external snapshot, no native reads/writes, sync or intentional delay.
  precut=snap(folder,'precut');assert not precut['live_consumers'],precut['live_consumers']
  if cut=='sync':
   m,_=command(folder,'postack-sync','sync');assert m['rc']==0;meta['sync']=m
  if cut in ('immediate','sync'):
   c=control('cut');meta['cut_receipt']=c;meta['ack_to_cut_ms']=(c['signal_monotonic_ns']-measured['complete_response_and_exit_monotonic_ns'])/1e6
   meta['restart']=control('boot');ready(folder,'restart-ready',precut['boot_id'])
  elif cut=='reboot':
   command(folder,'normal-poweroff','poweroff');meta['stop']=control('wait-stopped');meta['restart']=control('boot');ready(folder,'restart-ready',precut['boot_id'])
  elif cut!='nocut':raise ValueError(cut)
  after=snap(folder,'after-boot' if cut!='nocut' else 'after-no-cut')
  meta['after_label']='after-boot' if cut!='nocut' else 'after-no-cut'
  observe_access(folder,'after',after,key)
  command(folder,'boot-journal','journalctl -b --no-pager -u cald; journalctl -b --no-pager -k; systemctl cat cald')
  # Exactly one separate recovery diagnostic. It must not determine first-boot score.
  if time.time()>=DEADLINE:raise RuntimeError('probe cutoff before recovery diagnostic')
  recovery_args=['rollback',g2] if op=='B' else ['apply']
  try:meta['recovery']=ack(folder,'recovery',recovery_args)
  except Exception as e:meta['recovery_error']=str(e)
  recovered=snap(folder,'recovered');observe_access(folder,'recovered',recovered,key)
  meta['status']='complete';meta['end_utc']=now()
 except Exception as e:
  meta.update(status='unsupported-or-instrument-error',error=str(e),traceback=traceback.format_exc(),end_utc=now())
  print(traceback.format_exc(),flush=True)
 finally:
  save(folder/'meta.json',meta)
  try:command(folder,'final-poweroff','poweroff',20);control('wait-stopped')
  except Exception as e:meta['shutdown_error']=str(e);save(folder/'meta.json',meta)
 print(now(),'END',ident,meta['status'],flush=True)
 return meta
if __name__=='__main__':
 if len(sys.argv)>1:
  run_row(*sys.argv[1:])
 else:
  # Controls first, then fixed primary order. Every cell remains in planned-matrix.json.
  for cut in ('nocut','reboot','immediate','sync'):
   for op in ('R','G','B'):
    for mode in ('keep','delete'):
     r=run_row(op,mode,cut)
     if r['status']!='complete':raise SystemExit('STOP: investigate failed row, preserve original; no silent retry')

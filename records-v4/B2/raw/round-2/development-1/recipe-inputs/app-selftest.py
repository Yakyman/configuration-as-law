#!/usr/bin/python3
"""Fresh-guest application-channel self-tests; each expectation precedes its action."""
import argparse,copy,hashlib,json,os,pathlib,selectors,signal,subprocess,sys,time
sys.path.insert(0,'/usr/local/lib/stand')
import app_channels as a
P=pathlib.Path
p=P('/usr/local/share/stand/channels')
parser=argparse.ArgumentParser();parser.add_argument('--parser',action='store_true');parser.add_argument('--output',default='/var/lib/stand/app-selftest.jsonl');opts=parser.parse_args()
log=P(opts.output);log.parent.mkdir(parents=True,exist_ok=True);stream=log.open('w',buffering=1);failures=[]
def record(**row):
 row['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());s=json.dumps(row,sort_keys=True);stream.write(s+'\n');print(s,flush=True)
def expect(ident,variants,expected,**kw):record(phase='expected',id=ident,variants=variants,expected=expected,source='B1/CHANNELS.md; B1/raw/install-sources.md E8,E13,E19,E20; B2/raw/round-4/app-notes.md',**kw)
def result(ident,ok,**kw):
 record(phase='result',id=ident,passed=bool(ok),**kw)
 if not ok:failures.append(ident)
def cmd(args):
 try:return subprocess.run(list(map(str,args)),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
 except FileNotFoundError:return subprocess.CompletedProcess(args,127,'UNAVAILABLE: '+str(args[0]))
def ordinary(*fields):return ['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-session','-c','\t'.join(map(str,fields))]
def attempt(ident,variants,args,success=False,contains=None):
 expect(ident,variants,'success through declaration' if success else 'refusal with current declaration unchanged',command=list(map(str,args)))
 before=P('/var/lib/stand/current').resolve()
 q=cmd(args);same=P('/var/lib/stand/current').resolve()==before
 result(ident,(q.returncode==0 if success else q.returncode!=0 and same) and (contains is None or contains in q.stdout),rc=q.returncode,output=q.stdout,generation_unchanged=same)
 return q
channels={'flatpak':('flatpak',['C3.1','C3.2','C3.3']),'appimage':('stand-appimage',['C3.4','C3.5']),'oci':('podman',['C9.1','C9.2','C9.3','C9.4','C9.5','C9.6'])}
for channel,(frontend,variants) in channels.items():
 spec=json.loads((p/(channel+'.json')).read_text())
 expect(channel+'-SOURCE',variants,'artifact source matches predeclared SHA-256',sha256=spec['sha256'])
 result(channel+'-SOURCE',a.sha(P(spec['artifact']).read_bytes())==spec['sha256'])
 expect(channel+'-PARSE',variants,'pinned import and exact reconstructed declaration validate')
 rows=a.import_rows(channel,spec);a.validate(rows,p);result(channel+'-PARSE',True,entry=rows[-1]['application_entry'])
 for case,mutate in [('checksum',lambda s:s.update(sha256='0'*64)),('permissions',lambda s:s['permissions'].update(network=True)),('entrypoint',lambda s:s.update(entrypoint='../../escape'))]:
  ident=channel+'-'+case;expect(ident,variants,'parser refuses invalid pinned import')
  bad=copy.deepcopy(spec);mutate(bad)
  try:a.import_rows(channel,bad)
  except (ValueError,KeyError) as error:result(ident,True,refusal=str(error))
  else:result(ident,False)
 bad=copy.deepcopy(rows);bad[-1]['files'][0]['mode']=0o777
 expect(channel+'-TAMPER',variants,'payload tampering refused')
 try:a.validate(bad,p)
 except ValueError as error:result(channel+'-TAMPER',True,refusal=str(error))
 else:result(channel+'-TAMPER',False)
 if channel=='oci':
  expect('OCI-MISSING-IMAGE',variants,'container without separate exact image line refused')
  try:a.validate(rows[-1:],p)
  except ValueError as error:result('OCI-MISSING-IMAGE',True,refusal=str(error))
  else:result('OCI-MISSING-IMAGE',False)
 if opts.parser:continue
 for authority in ('ordinary','root'):
  args=ordinary('broker',frontend,'install',p/(channel+'.json')) if authority=='ordinary' else ['/usr/local/bin/'+frontend,'install',p/(channel+'.json')]
  attempt(channel+'-INSTALL-'+authority,variants,args,True,'SUCCESS ')
  attempt(channel+'-VERIFY-'+authority,variants,['/usr/local/bin/stand-verify'],True)
 exported=P('/var/lib/stand/channel-examples');exported.mkdir(exist_ok=True)
 ids={r['id'] for r in rows}
 installed=[line for line in (P('/var/lib/stand/current')/'machine.jsonl').read_text().splitlines() if json.loads(line)['id'] in ids]
 expect(channel+'-EXPORT',variants,'exact original installed declaration lines retained for the check-2 input')
 result(channel+'-EXPORT',{json.loads(line)['id'] for line in installed}==ids)
 (exported/(channel+'.jsonl')).write_text('\n'.join(installed)+'\n')
 entry=rows[-1]['application_entry']
 for authority in ('ordinary','root'):
  args=ordinary('broker',frontend,'run',rows[-1]['id']) if authority=='ordinary' else ['/usr/local/bin/'+frontend,'run',rows[-1]['id']]
  attempt(channel+'-TOOL-RUN-'+authority,variants,args,True,'RECORDED_APPLICATION_OK WRITE_REFUSED EXEC_REFUSED')
 expect(channel+'-NATIVE-BOUNDARY',variants,'uid/gid 1000, socket creation refused, filesystem writes refused, unrecorded execution refused; OCI cannot read host Python path')
 positive=attempt(channel+'-POSITIVE',variants,ordinary('run',entry),True,'RECORDED_APPLICATION_OK WRITE_REFUSED EXEC_REFUSED')
 if channel=='oci':result('OCI-ROOT-CONTENT',positive.returncode==0 and 'IMAGE_ROOT_ONLY' in positive.stdout and 'EXISTING_NONENTRY_EXEC_REFUSED' in positive.stdout,output=positive.stdout)
 if channel=='oci':
  expect('OCI-OWN-ROOT',variants,'container executable path is configured under its own immutable image root')
  table=P('/etc/stand/launch.tsv').read_text();line=[x for x in table.splitlines() if x.split('\t')[0]==entry]
  result('OCI-OWN-ROOT',len(line)==1 and line[0].split('\t')[1]=='container',launch=line)
 cases=[]
 if channel=='flatpak':
  cases=[('SYSTEM',['install','flathub','org.unrecorded.App']),('UPDATE',['update','org.stand.Probe']),('USER',['--user','install','flathub','org.unrecorded.App']),('ROOT',['--installation=other','install','unrecorded.flatpak']),('REMOTE',['remote-add','unrecorded','https://invalid.example/repo']),('BUNDLE',['install','--bundle','unrecorded.flatpak']),('RUNTIME',['install','flathub','org.unrecorded.Runtime']),('OVERRIDE',['override','--filesystem=host','org.stand.Probe']),('ALT-COMMAND',['run','--command=sh','org.stand.Probe']),('DEVEL',['run','--devel','org.stand.Probe'])]
 elif channel=='appimage':
  attempt('APPIMAGE-DOWNLOADED',variants,ordinary('run',spec['artifact']))
  attempt('APPIMAGE-FUSE',variants,ordinary('run',spec['artifact'],'--appimage-mount'))
  attempt('APPIMAGE-SELF-UPDATE',variants,ordinary('run',entry,'--appimage-update'))
  extracted=P('/home/stand/round4-AppRun');extracted.write_bytes(__import__('base64').b64decode(next(f['content_b64'] for f in rows[-1]['files'] if f['path']==entry)));extracted.chmod(0o755)
  try:attempt('APPIMAGE-EXTRACTED',variants,ordinary('run',extracted))
  finally:extracted.unlink()
  cases=[('UNPINNED',['install',spec['artifact']]),('SELF-UPDATE',['update','--unrecorded'])]
 else:
  cases=[('PULL-TAG',['pull','example.invalid/unrecorded:latest']),('RUN-TAG',['run','example.invalid/unrecorded:latest']),('ROOTLESS',['--root','/home/stand/oci','run','unrecorded']),('BIND',['run','-v','/home/stand:/code','unrecorded']),('OVERLAY',['run','--read-only=false','unrecorded']),('EXEC',['exec','round4-oci','/bin/sh']),('PACKAGE-INSTALL',['exec','round4-oci','apt-get','install','hello']),('BUILD-RUN',['build','/home/stand']),('LOAD',['load','-i',spec['artifact']]),('IMPORT',['import',spec['artifact']]),('COMMIT',['commit','round4-oci','unrecorded']),('PRIVILEGED',['run','--privileged','unrecorded']),('HOST-NS',['run','--pid=host','unrecorded']),('DEVICE',['run','--device=/dev/kvm','unrecorded']),('HOOK',['--hooks-dir=/home/stand','run','unrecorded']),('API',['system','service','unix:/tmp/unrecorded.sock'])]
 for name,args in cases:
  for authority in ('ordinary','root'):
   command=ordinary('broker',frontend,*args) if authority=='ordinary' else ['/usr/local/bin/'+frontend,*args]
   attempt(channel+'-'+name+'-'+authority,variants,command)
 if channel=='flatpak':
  attempt('FLATPAK-ABSOLUTE-ROOT',variants,['/usr/bin/flatpak','--user','install','unrecorded.flatpak'])
  attempt('FLATPAK-DBUS-HELPER',variants,['/usr/bin/busctl','--system','call','org.freedesktop.DBus','/org/freedesktop/DBus','org.freedesktop.DBus','StartServiceByName','su','org.freedesktop.Flatpak.SystemHelper','0'])
 if channel=='oci':
  for runtime in ('/usr/bin/runc','/usr/bin/crun','/usr/bin/bwrap'):
   executable=P(runtime);launches={line.split('\t')[0] for line in P('/etc/stand/launch.tsv').read_text().splitlines()}
   record(phase='availability',id='OCI-ALTERNATIVE-'+executable.name,variants=variants,path=runtime,exists=executable.exists(),ordinary_entry=runtime in launches,mode=oct(executable.stat().st_mode & 0o7777) if executable.exists() else None,sha256=a.sha(executable.read_bytes()) if executable.is_file() else None)
   attempt('OCI-ALTERNATIVE-'+P(runtime).name,variants,ordinary('run',runtime,'run','unrecorded'))
 attempt(channel+'-REMOVE',variants,ordinary('broker',frontend,'remove',rows[-1]['id']),True,'SUCCESS ')
 attempt(channel+'-REMOVED-ENTRY',variants,ordinary('run',entry))
 if channel=='oci':
  attempt('OCI-RETAINED-IMAGE',variants,ordinary('broker','podman','start','round4-oci'))
  attempt('OCI-REMOVE-IMAGE',variants,ordinary('broker','podman','remove',rows[0]['id']),True,'SUCCESS ')
 attempt(channel+'-FINAL-VERIFY',variants,['/usr/local/bin/stand-verify'],True)
if not opts.parser:
 variants=['C9.3','C9.6'];hold_spec=json.loads((p/'oci-hold.json').read_text())
 expect('OCI-HOLDER-SOURCE',variants,'holder artifact matches predeclared source hash; marker activates a recorded long-lived process',sha256=hold_spec['sha256'])
 result('OCI-HOLDER-SOURCE',a.sha(P(hold_spec['artifact']).read_bytes())==hold_spec['sha256'])
 holder_rows=a.import_rows('oci',hold_spec);holder=holder_rows[-1]['application_entry']
 attempt('OCI-HOLDER-INSTALL',variants,ordinary('broker','podman','install',p/'oci-hold.json'),True,'SUCCESS ')
 import codeboundary
 profile=codeboundary.key(holder)
 def profile_pids():
  found=[]
  for proc in P('/proc').iterdir():
   if not proc.name.isdigit():continue
   try:
    if (proc/'attr/current').read_text().split(' ')[0]==profile and (proc/'stat').read_text().split(') ',1)[1][0]!='Z':found.append(int(proc.name))
   except OSError:pass
  return found
 expect('OCI-HOLDER-START',variants,'recorded container and fork descendant reach ready markers, real non-entry execution fails and at least two profile processes stay alive')
 running=subprocess.Popen(ordinary('run',holder),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 output=b'';sel=selectors.DefaultSelector();sel.register(running.stdout,selectors.EVENT_READ)
 deadline=time.monotonic()+15
 try:
  while time.monotonic()<deadline and not (b'CONTAINER_HOLDER_READY' in output and b'CONTAINER_CHILD_READY' in output):
   if sel.select(.2):
    data=os.read(running.stdout.fileno(),4096)
    if not data:break
    output+=data
  victims=profile_pids()
  result('OCI-HOLDER-START',b'CONTAINER_HOLDER_READY' in output and b'CONTAINER_CHILD_READY' in output and b'EXISTING_NONENTRY_EXEC_REFUSED' in output and len(victims)>=2,output=output.decode(errors='replace'),pids=victims)
  expect('OCI-HOLDER-LIVE-REMOVAL',variants,'removing the container line kills all recorded holder profile processes before SUCCESS; retained image stays inert')
  attempt('OCI-HOLDER-REMOVE',variants,ordinary('broker','podman','remove',holder_rows[-1]['id']),True,'SUCCESS ')
  after=profile_pids()
  result('OCI-HOLDER-LIVE-REMOVAL',len(victims)>=2 and not after,pids_before=victims,pids_after=after)
  attempt('OCI-HOLDER-REMOVED-PATH',variants,ordinary('run',holder))
  attempt('OCI-HOLDER-RETAINED-ARCHIVE',variants,ordinary('run',holder_rows[0]['files'][0]['path']))
  attempt('OCI-HOLDER-RESTART',variants,ordinary('broker','podman','start',holder_rows[-1]['id']))
  attempt('OCI-HOLDER-REMOVE-IMAGE',variants,ordinary('broker','podman','remove',holder_rows[0]['id']),True,'SUCCESS ')
 finally:
  sel.close()
  for pid in profile_pids():
   try:os.kill(pid,signal.SIGKILL)
   except ProcessLookupError:pass
  try:running.communicate(timeout=5)
  except subprocess.TimeoutExpired:running.kill();running.communicate()
 attempt('OCI-HOLDER-FINAL-VERIFY',variants,['/usr/local/bin/stand-verify'],True)
record(phase='summary',passed=not failures,failures=failures)
sys.exit(bool(failures))

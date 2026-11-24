#!/usr/bin/python3 -B
"""The seventeen fixed BC3 cases; builder observations, not independent acceptance.

Run as guest root. --case ID performs one case; default performs all seventeen.
Every ordinary command uses the recorded stand-shell. Fixtures are written through
that ordinary interface, never injected into a backing store. No failure is turned
into a closure by exit status alone. The controller emits exact snapshots to JSONL.
"""
import argparse,base64,hashlib,json,os,pathlib,pwd,grp,shlex,subprocess,time
P=pathlib.Path
HERE=P(__file__).resolve().parent
FIXTURES=HERE/'bc3-fixtures.json'
FSROOT=P('/var/lib/stand-fs')
def digest(b):return hashlib.sha256(b).hexdigest()
def emit(**r):
 # Full evidence is retained once per content digest; JSONL keeps references.
 for key,value in list(r.items()):
  if isinstance(value,dict) and 'primary' in value and 'filesystem' in value:
   encoded=(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()
   sha=digest(encoded);directory=P('/var/lib/stand/bc3-evidence/snapshots')
   directory.mkdir(parents=True,exist_ok=True);path=directory/(sha+'.json')
   if not path.exists():path.write_bytes(encoded)
   r[key]=dict(snapshot_path=str(path),snapshot_sha256=sha,
      primary_sha256=value['primary']['sha256'],
      filesystem={k:dict(sha256=v['sha256'],generation=v['declaration']['generation'],success=v['success']) for k,v in value['filesystem'].items()})
 r['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());print(json.dumps(r,sort_keys=True),flush=True)
def primary():
 p=P('/var/lib/stand/current/machine.jsonl');b=p.read_bytes()
 return dict(sha256=digest(b),rows=[json.loads(x) for x in b.splitlines()],report=json.loads(P('/var/lib/stand/last-success.json').read_text()))
def fs_snapshot():
 result={}
 for key in ('home','tmp','vartmp','shm','etc'):
  p=FSROOT/key/'current'/'declaration.json'
  if p.exists():
   directory=p.parent.resolve();b=(directory/'declaration.json').read_bytes();audit=FSROOT/key/'audit.jsonl'
   result[key]=dict(path=str(directory/'declaration.json'),sha256=digest(b),declaration=json.loads(b),success=json.loads((directory/'success.json').read_text()),audit_bytes=audit.stat().st_size if audit.exists() else 0)
 return result
def snapshot():return dict(primary=primary(),filesystem=fs_snapshot())
def audit_since(before):
 result={}
 for key in ('home','tmp','vartmp','shm','etc'):
  path=FSROOT/key/'audit.jsonl'
  if path.exists():
   with path.open('rb') as stream:
    stream.seek(before['filesystem'].get(key,{}).get('audit_bytes',0))
    result[key]=[json.loads(line) for line in stream if line.strip()]
 return result

def ordinary(command,cwd='/home/stand',timeout=300):
 # Direct supplemental input had an outer cwd prefix in its original controller.
 full=('cd '+shlex.quote(cwd)+'; '+command) if cwd!='/home/stand' else command
 return subprocess.run(['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-shell','-c',full],capture_output=True,text=True,timeout=timeout,cwd=cwd)
def result_process(p):return dict(rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
def setup_file(f):
 data=f['content_b64'];path=f['path'];parent=str(P(path).parent)
 command='mkdir -p '+shlex.quote(parent)+' && printf %s '+shlex.quote(data)+' | base64 -d > '+shlex.quote(path)+' && chmod '+oct(f['mode'])[2:]+' '+shlex.quote(path)
 emit(phase='fixture_expected',path=path,sha256=f['sha256'],command=command)
 p=ordinary(command)
 good=p.returncode==0 and P(path).is_file() and digest(P(path).read_bytes())==f['sha256']
 emit(phase='fixture_result',path=path,passed=good,**result_process(p))
 if not good:raise RuntimeError('fixture creation failed: '+path)
def covering_files(snapshot_value):
 """Return exact file requirements; finalized with FS schema during integration."""
 found=[]
 for row in snapshot_value['primary']['rows']:
  for f in row.get('files',[]):found.append(dict(f,covering_line=row['id'],declaration='primary'))
 for key,entry in snapshot_value['filesystem'].items():
  declaration=entry['declaration']
  mounts={'home':'/home/stand','tmp':'/tmp','vartmp':'/var/tmp','shm':'/dev/shm','etc':'/etc'}
  report=entry['success']
  if report.get('declaration_sha256')!=entry['sha256'] or report.get('generation')!=declaration.get('generation'):
   continue
  for relative,inode in declaration.get('paths',{}).items():
   obj=declaration['objects'][str(inode)]
   if 'sha256' in obj:
    found.append(dict(path=mounts[key]+relative,sha256=obj['sha256'],size=obj['st_size'],declaration=key,generation=declaration['generation'],inode=inode,report=report))
 return found
def coverage(paths,snap,fixtures):
 rows=covering_files(snap);out=[]
 for path in paths:
  expected=fixtures[path];actual=digest(P(path).read_bytes()) if P(path).is_file() else None
  matches=[r for r in rows if r.get('path')==path and r.get('sha256')==expected['sha256']]
  out.append(dict(path=path,expected_sha256=expected['sha256'],actual_sha256=actual,covering_rows=matches,covered=actual==expected['sha256'] and bool(matches)))
 return out
def way(case,all_fixtures,data):
 ident=case['id']
 if ident=='DISPATCHER-SAVED':
  path='/tmp/v4-extra-7z89hz2f/dispatcher.json';payload=(json.dumps(data['dispatcher_row'])+'\n').encode()
  setup_file(dict(path=path,content_b64=base64.b64encode(payload).decode(),sha256=digest(payload),mode=0o600))
  p=ordinary('stand-pkg install '+path)
  emit(phase='dispatcher_install',id=ident,**result_process(p))
  if p.returncode:raise RuntimeError('dispatcher install failed')
 # Inline-writing cases retain their original write+evaluate command. Other cases
 # require saved source from an ordinary write immediately before the attempt.
 if not case['inline_writes']:
  for path in case['files']:setup_file(all_fixtures[path])
 before=snapshot();emit(phase='expected',id=ident,role='attempt',command=case['command'],cwd=case['cwd'],expected='refused or exact saved source recorded before use',before=before)
 p=ordinary(case['command'],case['cwd']);after=snapshot();covered=coverage(case['files'],after,all_fixtures)
 marker=any(x.strip()==case['marker'] for x in p.stdout.splitlines())
 refusal=p.returncode!=0 and not marker and any(x in p.stderr.lower() for x in ('permission denied','operation not permitted','refused'))
 # Post-state coverage alone is not temporal proof; retain before/after for the
 # filesystem transaction audit. The supplied filesystem records before exposure.
 recorded=p.returncode==0 and marker and all(x['covered'] for x in covered)
 emit(phase='attempt_result',id=ident,marker_observed=marker,refused=refusal,recorded=recorded,coverage=covered,after=after,audit=audit_since(before),**result_process(p))
 if not all(x['covered'] for x in covered):
  # The positive fixture is an explicit ordinary prospective write through the
  # declaration filesystem; failure here is not hidden by attempting a wrapper.
  for path in case['files']:setup_file(all_fixtures[path])
 pre=snapshot();precoverage=coverage(case['files'],pre,all_fixtures)
 emit(phase='expected',id=ident,role='permitted',command=case['command'],cwd=case['cwd'],expected='same bytes already declared, same command succeeds',coverage=precoverage,before=pre)
 q=ordinary(case['command'],case['cwd']);post=snapshot();postcoverage=coverage(case['files'],post,all_fixtures)
 positive=q.returncode==0 and any(x.strip()==case['marker'] for x in q.stdout.splitlines()) and all(x['covered'] for x in precoverage+postcoverage)
 passed=(refusal or recorded) and positive
 emit(phase='case_result',id=ident,passed=passed,attempt_closed=refusal or recorded,permitted=positive,coverage=postcoverage,after=post,audit=audit_since(pre),**result_process(q))
 return passed
def account(data):
 case=data['account'];before=snapshot()
 emit(phase='expected',id=case['id'],command=case['command'],expected='native root tool records exact account and applies change',before=before)
 p=subprocess.run(case['command'],capture_output=True,text=True,timeout=300)
 after=snapshot();actual=None
 try:
  a=pwd.getpwnam('v4raw');groups=sorted(g.gr_name for g in grp.getgrall() if 'v4raw' in g.gr_mem or g.gr_gid==a.pw_gid)
  actual=dict(name=a.pw_name,uid=a.pw_uid,gid=a.pw_gid,gecos=a.pw_gecos,home=a.pw_dir,shell=a.pw_shell,groups=groups)
 except KeyError:pass
 candidates=[]
 etc=after['filesystem'].get('etc',{})
 if etc.get('success',{}).get('declaration_sha256')==etc.get('sha256'):
  candidates=etc.get('declaration',{}).get('account_rows',[])
 rows=[r for r in candidates if r.get('type')=='account' and r.get('name')=='v4raw']
 covered=actual is not None and any(all(r.get(k)==v for k,v in actual.items()) for r in rows)
 good=p.returncode==0 and covered and actual['uid']==1998 and actual['shell']=='/usr/sbin/nologin' and before['filesystem'].get('etc',{}).get('sha256')!=after['filesystem'].get('etc',{}).get('sha256')
 emit(phase='case_result',id=case['id'],passed=good,account=actual,covering_rows=rows,after=after,audit=audit_since(before),**result_process(p));return good

def ordinary_work():
 # One stand-shell process executes every listed action in order.
 payload=b'#!/usr/bin/bash\nprintf "PERSONAL_SCRIPT_OK:%s\\n" "$1"\n'
 path='/opt/stand/pkgs/bc3-personal/bin/personal'
 row=dict(id='bc3-personal',type='code',managed=True,version='1',source='builder:personal-script',entrypoints=[dict(path=path,interpreter='/usr/bin/bash')],files=[dict(path=path,kind='file',mode=493,uid=0,gid=0,sha256=digest(payload),content_b64=base64.b64encode(payload).decode())])
 data=(json.dumps(row)+'\n').encode();setup_file(dict(path='/tmp/bc3-personal.json',content_b64=base64.b64encode(data).decode(),sha256=digest(data),mode=0o644))
 command='''set -e
message='two words'; f() { printf '%s\\n' "$1"; }; f "$message" | tr a-z A-Z > document.txt; cat < document.txt
stand-pkg install /tmp/bc3-personal.json
/opt/stand/pkgs/bc3-personal/bin/personal 'ordinary argument'
apt install hello=2.10-5
/opt/stand/pkgs/repository-hello/usr/bin/hello
curl -fsS http://10.0.2.2:18753/index.html > page.html
w3m -dump -config /etc/stand/w3m.conf http://10.0.2.2:18753/index.html
printf '1c\\nEdited document\\n.\\nw\\nq\\n' | ed -s document.txt
cat document.txt
printf 'BC3_ORDINARY_COMPLETE\\n'
'''
 before=snapshot();emit(phase='expected',id='ordinary-work',command=command,expected='all six ordinary actions in one shell session',before=before)
 p=ordinary(command,timeout=900)
 after=snapshot();markers=['TWO WORDS','PERSONAL_SCRIPT_OK:ordinary argument','Hello, world!','BC3 NETWORK PAGE','Edited document','BC3_ORDINARY_COMPLETE']
 good=p.returncode==0 and all(m in p.stdout for m in markers) and P('/home/stand/document.txt').read_bytes()==b'Edited document\n'
 emit(phase='case_result',id='ordinary-work',passed=good,required_markers=markers,after=after,audit=audit_since(before),**result_process(p));return good

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--case');parser.add_argument('--fixtures',default=str(FIXTURES));args=parser.parse_args()
 if os.geteuid()!=0:raise RuntimeError('guest root controller required')
 data=json.loads(P(args.fixtures).read_text());files={f['path']:f for f in data['files']}
 known=[c['id'] for c in data['cases']]+[data['account']['id'],'ordinary-work']
 if args.case and args.case not in known:parser.error('unknown case')
 selected=[args.case] if args.case else known;results={}
 for ident in selected:
  try:
   if ident==data['account']['id']:good=account(data)
   elif ident=='ordinary-work':good=ordinary_work()
   else:good=way(next(c for c in data['cases'] if c['id']==ident),files,data)
  except Exception as e:
   good=False;emit(phase='case_error',id=ident,error=repr(e))
  results[ident]=good
 emit(phase='summary',results=results,passed=all(results.values()),count=len(results),hypothesis_outcome='?',acceptance='builder self-test only')
 return 0 if all(results.values()) else 1
if __name__=='__main__':raise SystemExit(main())

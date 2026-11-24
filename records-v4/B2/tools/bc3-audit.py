#!/usr/bin/python3 -B
"""Offline BC3 evidence consistency audit; never executes guest commands.

Usage: bc3-audit.py EXPORTED_DIRECTORY [--output REPORT.json]
Missing observations remain limitations. This is not independent acceptance or
proof of ordering from post-state snapshots. Exit 1 means inconsistent evidence;
exit 2 means required evidence is missing; exit 0 means checked evidence agrees,
subject to the explicitly reported observational limitations.
"""
import argparse,base64,hashlib,json,pathlib,re,collections,datetime
P=pathlib.Path
MOUNTS={'home':'/home/stand','tmp':'/tmp','vartmp':'/var/tmp','shm':'/dev/shm','etc':'/etc'}
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return (json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()

class Audit:
 def __init__(self,root):
  self.root=root;self.errors=[];self.missing=[];self.limitations=[];self.checks=0;self.snapshots={};self.references=0
 def check(self,test,label):
  self.checks+=1
  if test is not True:self.errors.append(label)
 def need(self,obj,key,label):
  if key not in obj:self.missing.append(label+': missing '+key);return None
  return obj[key]
 def single(self,rows,label):
  self.check(len(rows)==1,label+': exactly one record')
  return rows[0] if len(rows)==1 else {}
 def snap(self,ref,label):
  if not isinstance(ref,dict) or 'snapshot_sha256' not in ref:
   self.missing.append(label+': snapshot reference absent');return {}
  self.references+=1;digest=ref['snapshot_sha256']
  matches=list(self.root.rglob(digest+'.json'))
  matches=[p for p in matches if p.parent.name=='snapshots']
  if not matches:self.missing.append(label+': exported snapshot absent');return {}
  self.check(len(matches)==1,label+': unique snapshot export')
  if digest not in self.snapshots:
   raw=matches[0].read_bytes();self.check(sha(raw)==digest,label+': snapshot SHA-256')
   data=json.loads(raw);self.snapshots[digest]=data
   primary=data.get('primary',{});rows=primary.get('rows')
   if rows is None:self.missing.append(label+': primary rows absent')
   else:self.check(sha(b''.join(canon(r) for r in rows))==primary.get('sha256'),label+': reconstructed primary file SHA-256')
   self.check(primary.get('report',{}).get('status')=='SUCCESS',label+': primary successful report')
   fs=data.get('filesystem',{});self.check(set(fs)==set(MOUNTS),label+': five filesystem declarations')
   for key,entry in fs.items():
    d=entry.get('declaration',{});report=entry.get('success',{})
    self.check(sha(canon(d))==entry.get('sha256'),label+': '+key+' declaration SHA-256')
    self.check(report.get('status')=='success' and report.get('declaration_sha256')==entry.get('sha256') and report.get('generation')==d.get('generation'),label+': '+key+' successful report binding')
    self.check(all(str(i) in d.get('objects',{}) for i in d.get('paths',{}).values()),label+': '+key+' namespace references exist')
  data=self.snapshots[digest]
  self.check(ref.get('primary_sha256')==data.get('primary',{}).get('sha256'),label+': primary summary identity')
  for key,entry in data.get('filesystem',{}).items():
   short=ref.get('filesystem',{}).get(key,{})
   self.check(short.get('sha256')==entry['sha256'] and short.get('generation')==entry['declaration']['generation'] and short.get('success')==entry['success'],label+': '+key+' summary identity')
  return data
 def files(self,snap):
  found=[]
  for r in snap.get('primary',{}).get('rows',[]):found.extend(r.get('files',[]))
  for key,entry in snap.get('filesystem',{}).items():
   d=entry['declaration']
   for path,ino in d.get('paths',{}).items():
    obj=d['objects'].get(str(ino),{})
    if 'sha256' in obj:found.append(dict(path=MOUNTS[key]+path,sha256=obj['sha256'],size=obj['st_size']))
  return found
 def coverage(self,rows,paths,snap,fixtures,label):
  if not isinstance(rows,list):self.missing.append(label+': coverage absent');return
  self.check(len(rows)==len(paths) and {r.get('path') for r in rows}==set(paths),label+': exact coverage paths')
  declared=self.files(snap)
  for r in rows:
   path=r.get('path');wanted=fixtures.get(path,{}).get('sha256')
   self.check(r.get('covered') is True,label+': explicit Boolean coverage')
   self.check(r.get('actual_sha256')==wanted and r.get('expected_sha256')==wanted,label+': exact observed bytes')
   self.check(any(f.get('path')==path and f.get('sha256')==wanted for f in declared),label+': independent snapshot coverage')
 def writes(self,result,case,fixtures,label):
  self.check(result.get('inline_write_verified') is True,label+': inline-write Boolean')
  if not case['inline_writes']:return
  self.check(not any(t in result.get('stderr','').lower() for t in ('permission denied','operation not permitted','read-only file system','write error','traceback')),label+': no failed inline write diagnostic')
  events=result.get('audit',{}).get('home')
  if events is None:self.missing.append(label+': inline write audit absent');return
  for path in case['files']:
   self.check(any(e.get('operation')=='write' and e.get('status')=='success' and any(c.get('path')==path[len(MOUNTS['home']):] and c.get('sha256')==fixtures[path]['sha256'] for c in e.get('changes',[])) for e in events),label+': successful exact inline-write event')
 def run(self):
  fp=self.root/'recipe-inputs/bc3-fixtures.json'
  if not fp.exists():self.missing.append('frozen fixture file absent');return
  spec=json.loads(fp.read_bytes());fixtures={r['path']:r for r in spec['files']}
  for r in fixtures.values():
   data=base64.b64decode(r['content_b64'],validate=True);self.check(len(data)==r['bytes'] and sha(data)==r['sha256'],'fixture bytes/hash identity')
  lp=self.root/'cases.jsonl'
  if not lp.exists():self.missing.append('cases.jsonl absent');return
  records=[json.loads(line) for line in lp.read_text().splitlines() if line.strip()]
  expected_ids=[c['id'] for c in spec['cases']]+[spec['account']['id'],'ordinary-work']
  results=[r for r in records if r.get('phase')=='case_result']
  self.check(len(results)==17 and collections.Counter(r.get('id') for r in results)==collections.Counter(expected_ids),'seventeen unique expected case results')
  self.check(not any(r.get('phase')=='case_error' for r in records),'no case errors')
  for r in results:self.check(r.get('passed') is True,r.get('id','unknown')+': explicit true result Boolean')
  for r in records:
   for key in ('before','after'):
    if key in r:self.snap(r[key],r.get('id',r['phase'])+' '+key)
   if r.get('phase')=='fixture_result':self.check(r.get('passed') is True and r.get('rc')==0,'fixture actual success')
  for case in spec['cases']:
   ident=case['id'];rows=[r for r in records if r.get('id')==ident]
   attempt=self.single([r for r in rows if r.get('phase')=='attempt_result'],ident+' attempt')
   positive=self.single([r for r in rows if r.get('phase')=='case_result'],ident+' permitted')
   pre={}
   for role in ('attempt','permitted'):
    e=self.single([r for r in rows if r.get('phase')=='expected' and r.get('role')==role],ident+' '+role+' command')
    self.check(e.get('command')==case['command'] and e.get('cwd')==case['cwd'],ident+' '+role+' exact command/cwd')
    if role=='permitted':pre=e
   for role,r in [('attempt',attempt),('permitted',positive)]:
    self.check(r.get('rc')==0 and case['marker'] in [line.strip() for line in r.get('stdout','').splitlines()],ident+' '+role+' actual successful marker')
    self.writes(r,case,fixtures,ident+' '+role)
    snap=self.snap(r.get('after'),ident+' '+role)
    self.coverage(r.get('coverage'),case['files'],snap,fixtures,ident+' '+role)
   for key in ('marker_observed','recorded'):self.check(attempt.get(key) is True,ident+': '+key+' true Boolean')
   self.check(type(attempt.get('refused')) is bool,ident+': refusal actual Boolean')
   for key in ('permitted','attempt_closed'):self.check(positive.get(key) is True,ident+': '+key+' true Boolean')
   self.coverage(pre.get('coverage'),case['files'],self.snap(pre.get('before'),ident+' permitted before'),fixtures,ident+' permitted precoverage')
  aid=spec['account']['id'];ar=self.single([r for r in results if r.get('id')==aid],'account result')
  ae=self.single([r for r in records if r.get('id')==aid and r.get('phase')=='expected'],'account command')
  self.check(ae.get('command')==spec['account']['command'],'account exact native argv')
  wanted=dict(name='v4raw',uid=1998,gid=1998,groups=['v4raw'],home='/home/v4raw',gecos='',shell='/usr/sbin/nologin')
  self.check(ar.get('rc')==0 and ar.get('account')==wanted,'account full actual tuple')
  after=self.snap(ar.get('after'),'account after');before=self.snap(ae.get('before'),'account before')
  rows=after.get('filesystem',{}).get('etc',{}).get('declaration',{}).get('account_rows',[])
  self.check(any(r.get('type')=='account' and all(r.get(k)==v for k,v in wanted.items()) for r in rows),'account independent exact declaration tuple')
  self.check(before.get('filesystem',{}).get('etc',{}).get('sha256')!=after.get('filesystem',{}).get('etc',{}).get('sha256'),'account changed declaration')
  ordinary=self.single([r for r in results if r.get('id')=='ordinary-work'],'ordinary result')
  command=self.single([r for r in records if r.get('id')=='ordinary-work' and r.get('phase')=='expected'],'ordinary command')
  markers=['TWO WORDS','PERSONAL_SCRIPT_OK:ordinary argument','Hello, world!','BC3 NETWORK PAGE','Edited document','BC3_ORDINARY_COMPLETE']
  self.check(ordinary.get('rc')==0 and all(m in ordinary.get('stdout','').splitlines() for m in markers),'ordinary actual complete output lines')
  self.check(ordinary.get('required_markers')==markers,'ordinary fixed markers')
  c=command.get('command','')
  self.check(c.startswith('set -e\n') and all(s in c for s in ('| tr a-z A-Z > document.txt','cat < document.txt','stand-pkg install /tmp/bc3-personal.json','apt install hello=2.10-5','curl -fsS','w3m -dump','| ed -s document.txt','BC3_ORDINARY_COMPLETE')),'ordinary one-session command includes all actions')
  s=self.snap(ordinary.get('after'),'ordinary after');rows=s.get('primary',{}).get('rows',[])
  personal=[r for r in rows if r.get('id')=='bc3-personal'];package=[r for r in rows if r.get('id')=='repository:hello']
  payload=b'#!/usr/bin/bash\nprintf "PERSONAL_SCRIPT_OK:%s\\n" "$1"\n'
  self.check(len(personal)==1 and any(f.get('path')=='/opt/stand/pkgs/bc3-personal/bin/personal' and f.get('sha256')==sha(payload) for f in personal[0].get('files',[])),'ordinary own script exact declaration')
  self.check(len(package)==1 and package[0].get('version')=='2.10-5' and bool(package[0].get('files')),'ordinary package exact version recorded')
  self.check(any(f.get('path')=='/home/stand/document.txt' and f.get('sha256')==sha(b'Edited document\n') for f in self.files(s)),'ordinary final document declaration content')
  summary=self.single([r for r in records if r.get('phase')=='summary'],'summary')
  self.check(summary.get('count')==17 and summary.get('passed') is True and summary.get('results')==dict.fromkeys(expected_ids,True),'summary exact successful Boolean results')
  self.limitations.extend([
   'Filesystem prepublication ordering depends on source review and mounted implementation evidence; post-state hashes alone do not prove timing.',
   'Shell records contain exact command strings and working directories, not kernel-observed argv; the fixed controller source establishes the runuser/stand-shell invocation.',
   'Primary success declaration digest covers the combined declaration inputs; snapshots provide machine rows only, so its combined digest cannot be recomputed here.',
   'Ordinary final document exact bytes are represented by the declaration hash and output; no separate actual final byte hash or exported document bytes are present in this controller schema.',
   'Filesystem blob bytes and ordinary installed package readbacks are not exported in snapshots; exact live bytes beyond fixture coverage require the separate complete verification record.',
   'This is a builder-record consistency audit, not independent acceptance or a hypothesis outcome.'
  ])
 def report(self):
  return dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='inconsistent' if self.errors else 'incomplete' if self.missing else 'consistent_with_stated_limitations',checks=self.checks,snapshots=len(self.snapshots),snapshot_references=self.references,errors=self.errors,missing_evidence=self.missing,limitations=self.limitations)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=P);p.add_argument('--output',type=P);a=p.parse_args();audit=Audit(a.directory)
 try:audit.run()
 except (OSError,ValueError,KeyError,TypeError) as error:audit.missing.append('Audit could not finish: '+str(error))
 report=audit.report();text=json.dumps(report,sort_keys=True,indent=2)+'\n'
 if a.output:a.output.write_text(text)
 else:print(text,end='')
 return 1 if audit.errors else 2 if audit.missing else 0
if __name__=='__main__':raise SystemExit(main())

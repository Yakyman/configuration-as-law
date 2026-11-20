#!/usr/bin/env python3
"""Evidence integrity/accounting only; not independent acceptance."""
from pathlib import Path
import json,hashlib,datetime,re
R=Path(__file__).resolve().parent
E=R/'evidence'
events=[json.loads(s) for s in (E/'events.jsonl').read_text().splitlines()]
by={x['label']:x for x in events}
summary=json.loads((E/'summary.json').read_text())
digest=summary['digest']; payload='/var/lib/cal/executables/alice/'+digest
checks=[]
def check(name,value,detail=None):
 checks.append(dict(name=name,ok=bool(value),detail=detail))
def state(label):return json.loads((E/(label+'.json')).read_text())
def file(s,p):return s['files'].get(p,{'exists':False})
def equal_artifacts(a,b,paths):return all(file(a,p)==file(b,p) for p in paths)
def generation(s):return json.loads(file(s,'/var/lib/cal/current.json')['text'])['generation']
def generations(s):return {p:v['sha256'] for p,v in s['files'].items() if '/generations/' in p}
def response(e):return json.loads(e['stdout'].split('IDENTITY_END\n',1)[1])
def utc(x):return datetime.datetime.fromisoformat(x.replace('Z','+00:00'))
for line in (R/'PREPROBE.sha256').read_text().splitlines():
 h,p=line.split('  ',1);check('preprobe hash '+p,hashlib.sha256((R/p).read_bytes()).hexdigest()==h)
check('freeze before first probe',utc((R/'frozen-at.txt').read_text().strip())<utc(events[0]['started']))
check('summary event count',summary['events']==len(events))
check('unique event labels',len(by)==len(events))
for e in events:
 pre=e['stdout'].split('IDENTITY_END\n',1)[0]
 expected={'root':0,'alice':24101,'bob':24102,'negative':24103}[e['user']]
 check(e['label']+' credential UID',f'uid={expected}(' in pre)
 if e['user']!='root':check(e['label']+' zero effective capabilities','CapEff:\t0000000000000000' in pre)
 profile='cal-'+e['user']+' (enforce)' if e['confined'] else 'unconfined'
 check(e['label']+' profile',profile in pre)
 if e['user']=='alice':check(e['label']+' fresh grant group','24104(p24grant)' in pre)
matrix=[]
for item in summary['results']:
 tag=item['tag']
 a=state(tag+'-baseline'); b=state(tag+'-after-apply')
 reply=response(by[tag+'-personal-apply'])
 paths=['/var/lib/cal/current.json','/etc/apparmor.d/cal-stand',payload,'/var/lib/cal/executables/alice']
 if item['apply_rc']:
  check(tag+' rejected: accepted artifacts unchanged',equal_artifacts(a,b,paths))
  check(tag+' rejected: generations unchanged',generations(a)==generations(b))
 else:
  check(tag+' ACK/new generation',reply['ok'] and generation(a)!=generation(b))
  p=file(b,payload)
  check(tag+' snapshot bytes/ownership/mode',p.get('sha256')==digest and p.get('uid')==0 and p.get('gid')==24101 and p.get('mode')=='0o550')
  check(tag+' snapshot parent ownership/mode',file(b,'/var/lib/cal/executables/alice').get('uid')==0 and file(b,'/var/lib/cal/executables/alice').get('gid')==24101 and file(b,'/var/lib/cal/executables/alice').get('mode')=='0o750')
 row=dict(tag=tag,source=item.get('source'),source_negative=item.get('source_negative'),apply_rc=item['apply_rc'],reply=reply,generation_before=generation(a),generation_after=generation(b),snapshot_before=file(a,payload),snapshot_after=file(b,payload),payload_alice=item['payload_alice'],payload_negative=item.get('payload_negative'),payload_bob=item.get('payload_bob'),fixed_limb=None)
 if 'case' in item:
  root=json.loads(file(a,'/etc/cal/root.json')['text'])
  check(tag+' no lists and no bypass',root['policies']=={} and root['allow_channels']=={})
  c=state(tag+'-after-access')
  check(tag+' payload immutable under attempted write',file(b,payload)==file(c,payload) and by[tag+'-payload-alice-write-denied']['rc']!=0)
  if item['source']['exec_rc']==0 and item['source']['exec_marker'] and (item['apply_rc']!=0 or not item['payload_alice']['exec_marker']):row['fixed_limb']='9.6 third limb; stand defect => hypothesis ?'
  check(tag+' negative private payload denied',item['payload_negative']['read_rc']!=0 and item['payload_negative']['exec_rc']!=0 and not item['payload_negative']['exec_marker'])
  check(tag+' Bob private payload denied',item['payload_bob']['read_rc']!=0 and item['payload_bob']['exec_rc']!=0 and not item['payload_bob']['exec_marker'])
  if item['apply_rc']==0:
   t1=state(tag+'-temporal-before'); t2=state(tag+'-temporal-after-reapply')
   check(tag+' temporal declaration/current/policy/snapshot unchanged',equal_artifacts(t1,t2,paths+['/home/alice/declaration.json']))
   check(tag+' temporal generations unchanged',generations(t1)==generations(t2))
   check(tag+' temporal source denied/snapshot survives',by[tag+'-revoked-source-alice-read']['rc']!=0 and by[tag+'-revoked-source-alice-exec']['rc']!=0 and by[tag+'-old-payload-alice-exec']['rc']==0 and by[tag+'-reapply-UNCHANGED']['rc']!=0)
  # Make compact per-case records containing exact raw commands, identities and replies.
  (E/(tag+'-events.json')).write_text(json.dumps([e for e in events if e['label'].startswith(tag+'-')],indent=2,sort_keys=True)+'\n')
 else:
  expect=tag in ('allow-match','deny-unrelated')
  check(tag+' list outcome',bool(item['apply_rc']==0)==expect and bool(item['payload_alice']['exec_rc']==0)==expect)
  (E/(tag+'-events.json')).write_text(json.dumps([e for e in events if e['label'].startswith(tag+'-')],indent=2,sort_keys=True)+'\n')
 matrix.append(row)
for c in ['owned','foreign','group','acl','mask','parent','xonly','noexec']:
 r1=next(x for x in summary['results'] if x['tag']=='r1-'+c);r2=next(x for x in summary['results'] if x['tag']=='r2-'+c)
 check(c+' replay agrees',all(r1[k]==r2[k] for k in ['source','source_negative','apply_rc','payload_alice','payload_negative','payload_bob']))
initial=state('initial');final=state('final-state')
for p in initial['files']:
 if '/p24-shared/' in p or p=='/home/alice/p24-private-parent/parent':check(p+' final source unchanged',file(initial,p)==file(final,p))
fails=[x for x in checks if not x['ok']]
out=dict(kind='Executor evidence integrity/accounting, NOT acceptance',events=len(events),matrix_trials=16,distinct_source_cases=8,list_controls=4,temporal_extensions=2,checks=len(checks),failed_checks=fails,stand_failure_cases=[x['tag'] for x in matrix if x['fixed_limb']],matrix=matrix)
(R/'audit.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
(R/'audit-checks.json').write_text(json.dumps(checks,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='matrix'},indent=2))
if fails:raise SystemExit(1)

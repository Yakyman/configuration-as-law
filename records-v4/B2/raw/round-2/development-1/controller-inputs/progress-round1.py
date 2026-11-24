#!/usr/bin/env python3
"""Read existing Round 1 logs only; never starts a probe or changes a guest."""
import json,pathlib,sys,time
root=pathlib.Path(__file__).resolve().parent.parent
phase=sys.argv[1] if len(sys.argv)>1 else 'final-2'
base=root/'raw/round-1'/phase
print(json.dumps({'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'phase':phase}))
steps=base/'steps.json'
if steps.exists():
 values=json.loads(steps.read_text())
 print(json.dumps({'completed_stages':len(values),'last_stages':[{k:v.get(k) for k in ('log','exit','ended_utc')} for v in values[-2:]]}))
for name in ('gate.jsonl','tools.jsonl','regressions-console.jsonl','combined-console.jsonl'):
 path=base/name
 if not path.exists():continue
 rows=[];current=None;summary=None
 with path.open() as stream:
  for line in stream:
   try:row=json.loads(line)
   except ValueError:continue
   if not isinstance(row,dict):continue
   if row.get('phase')=='expected':current=row.get('id',row.get('log'))
   if row.get('id') and isinstance(row.get('passed'),bool):rows.append(row)
   if row.get('phase')=='summary':summary=row
 print(json.dumps({'log':name,'completed_assertions':len(rows),'failed':[r['id'] for r in rows if not r['passed']],
                   'last_results':[{k:r.get(k) for k in ('id','passed','utc')} for r in rows[-2:]],'last_expected':current,
                   'summary':summary}))
if (base/'summary.json').exists():
 value=json.loads((base/'summary.json').read_text());print(json.dumps({k:value[k] for k in ('controller_exit','utc','remaining_vms','peer_remaining')}))
active=[]
for folder in (root/'raw/round-4'/phase,root/'raw/round-3'/('bc4-'+phase)):
 for name in ('language.jsonl','applications.jsonl','system.jsonl','ordinary.jsonl','round3.jsonl','powercuts.jsonl','round1.jsonl','round2.jsonl'):
  p=folder/name
  if p.exists():active.append(p)
if active:
 path=max(active,key=lambda p:p.stat().st_mtime)
 tests=[];last=None
 for line in path.read_text().splitlines():
  try:r=json.loads(line)
  except ValueError:continue
  if not isinstance(r,dict):continue
  if r.get('id') and isinstance(r.get('passed'),bool):tests.append(r)
  if r.get('phase')=='expected':last=r.get('id')
 print(json.dumps({'active_suite':str(path.relative_to(root/'raw')),'assertions':len(tests),'failed':[r['id'] for r in tests if not r['passed']],'last_expected':last,'last_results':[{k:r.get(k) for k in ('id','passed','utc')} for r in tests[-2:]]}))

#!/usr/bin/env python3
"""Compact read-only status of existing BC3 logs; no guest operations."""
import json,pathlib,time
r=pathlib.Path(__file__).resolve().parent.parent
folders=['raw/round-3/final-1-validation','raw/round-3/bc3-final-final-1-regressions','raw/round-4/bc3-final-final-1','raw/round-3/final-1-continuation']
print(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
for folder in folders:
 p=r/folder
 candidates=sorted(p.glob('*.jsonl'),key=lambda q:q.stat().st_mtime,reverse=True)[:2]
 for path in candidates:
  values=[]
  for line in path.read_text(errors='replace').splitlines():
   try:v=json.loads(line)
   except ValueError:continue
   if isinstance(v,dict):values.append(v)
  if values:
   v=values[-1];print(json.dumps({'log':str(path.relative_to(r)),'last':{k:v[k] for k in ('phase','id','utc','passed','rc','count') if k in v},'true_assertions':sum(x.get('passed') is True for x in values),'false_assertions':sum(x.get('passed') is False for x in values)}))
p=r/folders[0]/'summary.json'
if p.exists():
 x=json.loads(p.read_text());print(json.dumps({k:x[k] for k in ('controller_exit','lanes','remaining_vms','peer_remaining') if k in x}))

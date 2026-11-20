import pathlib,json,sys,collections,datetime
r=pathlib.Path(sys.argv[1]);groups=collections.defaultdict(list);stand_windows={};snapshots=[];absence_checks=0;shutdown_timeouts=[];shared={}
for stand in ['BQ','X3']:
 base=r/'guest'/stand
 if not base.exists():continue
 for p in sorted((base/'evidence/primary').glob('*/summary.json')):
  j=json.loads(p.read_text());kind='control' if j['control'] else 'primary';groups[kind].append(j)
  absence_checks+=len(j.get('absence_checks',{}))
  for stage in ['workload','rollback_workload']:
   if j.get(stage,{}).get('shutdown_timeout'):shutdown_timeouts.append(dict(case=j['id'],stage=stage))
 for p in (base/'evidence/primary').glob('*/*-inventory-status.json'):snapshots.append(json.loads(p.read_text()))
 if (base/'primary-end.txt').exists():
  start=(base/'primary-start.txt').read_text().strip();end=(base/'primary-end.txt').read_text().strip();stand_windows[stand]=dict(start=start,end=end,minutes=(datetime.datetime.fromisoformat(end.replace('Z','+00:00'))-datetime.datetime.fromisoformat(start.replace('Z','+00:00'))).total_seconds()/60)
 p=base/'evidence/shared-control.jsonl'
 if p.exists():
  parsed=[];unparsed=[]
  for n,line in enumerate(p.read_text().splitlines(),1):
   try:parsed.append(json.loads(line))
   except json.JSONDecodeError:unparsed.append(dict(line=n,text=line))
  shared[stand]=dict(assertions=sum(x.get('event')=='assertion' for x in parsed),failed_assertions=[x for x in parsed if x.get('event')=='assertion' and not x.get('passed')],case_results=[x for x in parsed if x.get('event')=='case-result'],unparsed=unparsed)
out={}
for kind,rows in groups.items():
 initial=[j.get('workload',{}).get('active_seconds',0) for j in rows];rollback=[j.get('rollback_workload',{}).get('active_seconds',0) for j in rows]
 out[kind]=dict(cases=len(rows),completed=sum(j['completed'] for j in rows),usable=sum(j.get('usable',False) for j in rows),initial_active_seconds=sum(initial),initial_range=[min(initial),max(initial)],rollback_active_seconds=sum(rollback),rollback_range=[min(rollback),max(rollback)],trajectory_wall_seconds=sum((j['end_ns']-j['start_ns'])/1e9 for j in rows))
print(json.dumps(dict(groups=out,stand_windows=stand_windows,absence_checkpoints=absence_checks,shutdown_timeouts=shutdown_timeouts,inventory_snapshots=len(snapshots),inventory_entry_observations=sum(j['entries'] for j in snapshots),inventory_entry_range=[min(j['entries'] for j in snapshots),max(j['entries'] for j in snapshots)] if snapshots else [],shared=shared),indent=2))

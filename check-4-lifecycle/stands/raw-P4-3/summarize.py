#!/usr/bin/python3
"""Post-run report aggregation of the frozen oracle and predeclared parity checks."""
import pathlib,json,re,datetime,hashlib,csv,sys
P=pathlib.Path;D=P(__file__).resolve().parent;R=D/'guest/results'
def read(p):return json.loads(p.read_text())
rows=read(D/'analysis-reproduced/analysis.json');by={r['name']:r for r in rows}
primary=[('a2-' if f=='blocks' else '')+f+'-'+l+'-'+p for f in ['blocks','inodes','ro'] for l in ['current','saved'] for p in ['keep','delete']]
shared=['a2-shared-'+f+'-'+p for f in ['healthy','blocks','inodes','ro'] for p in ['keep','delete']]
controls=['control-'+l+'-'+p for l in ['current','saved'] for p in ['keep','delete']]
selected=primary+shared+controls
def normalized(d):
 snapshots={p.stem:read(p) for p in d.glob('*.json') if p.stem in ['baseline','prepared','before-attempt','after-transition','before-recovery','after-retry','after-rollback']}
 ids=sorted({g for s in snapshots.values() for g in s['generations']});mapping={g:'G'+str(i+1) for i,g in enumerate(ids)}
 def n(o):
  if isinstance(o,dict):return {mapping.get(k,k):n(v) for k,v in o.items()}
  if isinstance(o,list):return [n(v) for v in o]
  if isinstance(o,str):return mapping.get(o,o).replace('/var/lib/p43-control/executables/','/var/lib/cal/executables/')
  return o
 out={}
 for phase,s in snapshots.items():
  doc={k:v.get('json') for k,v in s['documents'].items() if k in ['/etc/cal/root.json','/home/alice/declaration.json','/home/bob/declaration.json',s['control']+'/current.json']}
  doc['current']=doc.pop(s['control']+'/current.json')
  import base64
  policy=base64.b64decode(s['policy']['base64']).decode().replace('/var/lib/p43-control/executables/','/var/lib/cal/executables/')
  out[phase]={'documents':n(doc),'generations':n({g:v['json'] for g,v in s['generations'].items()}),'policy':policy}
 return out
parity=[]
for limb in ['current','saved']:
 for policy in ['keep','delete']:
  a=normalized(R/('original-'+limb+'-'+policy));b=normalized(R/('control-'+limb+'-'+policy))
  for phase in a:parity.append({'pair':limb+'-'+policy,'phase':phase,'equal':a[phase]==b.get(phase)})
native=[]
for name in selected:
 d=R/name;created=read(d/'create-native.json');c=json.loads(created['stdout']);expected=c['lookup']
 for label in ['initial-read','prepare-rollback-read','rollback-read','rollback-second-read']+(['after-transition-read','after-retry-read'] if 'shared' in name else []):
  p=d/(label+'.json')
  if p.exists():
   r=read(p);v=json.loads(r['stdout']) if r['rc']==0 else {};native.append({'row':name,'read':label,'rc':r['rc'],'same_lookup':v.get('lookup')==expected,'size':v.get('size')})
replays=[]
for p in read(D/'replays/selection.json'):
 a=by[p['parent']];b=by[p['name']]
 def normalized_error(r):return re.sub(r'\.cal-[a-z0-9_]+','.cal-TMP',r['transition']['error'] or '')
 keys=['current_programs','current_needer','active','archive','native_read_rc','L1_protected_deletion','L2_current_reading_ownerless_active_unarchived','L2_designated_reading_ownerless_active_unarchived','L3_shared_loss','L4_policy_mismatch_after_all_owners_absent']
 replays.append({'parent':p['parent'],'replay':p['name'],'both_reject':a['transition']['response_ok'] is False and b['transition']['response_ok'] is False,'same_normalized_error':normalized_error(a)==normalized_error(b),'same_endpoint':all(a['after-transition'][k]==b['after-transition'][k] for k in keys),'initial_errors':a['syscall_errors'],'replay_errors':b['syscall_errors']})
metas=[read(R/r['name']/'meta.json') for r in rows]
summary={'total_rows':len(rows),'complete':sum(bool(r['complete']) for r in rows),'initial_planned_rows':28,'amended_rows':12,'replay_rows':17,'primary_denominator':12,'initial_primary_fault_verified':sum(by[f+'-'+l+'-'+p]['condition_verified'] for f in ['blocks','inodes','ro'] for l in ['current','saved'] for p in ['keep','delete']),'primary_observation_selection':primary,'primary_selected_fault_verified':sum(by[n]['condition_verified'] for n in primary),'corrected_shared':shared,'selected':selected,'transition_ack_true':sum(r['transition']['response_ok'] is True for r in rows),'retry_ack_true':sum(r['retry']['response_ok'] is True for r in rows),'same_daemon_identity':sum(r['controller_alive_same_identity'] for r in rows),'quiescent':sum(r['quiescent'] for r in rows),'all_source_payload_joins':all(r['after-transition']['premises_complete'] and r['after-retry']['premises_complete'] for r in rows),'source_healthy_parity':parity,'native_reads':native,'replays':replays,'selected_retry_all_ack':all(by[n]['retry']['response_ok'] is True for n in selected),'first_row_utc':datetime.datetime.fromtimestamp(min(m['start_ns'] for m in metas)/1e9,datetime.timezone.utc).isoformat(),'last_row_utc':datetime.datetime.fromtimestamp(max(m['end_ns'] for m in metas)/1e9,datetime.timezone.utc).isoformat()}
for phase in ['after-transition','after-retry']:
 summary[phase]={k:[r['name'] for r in rows if r[phase][k] is True] for k in ['L1_protected_deletion','L2_current_reading_ownerless_active_unarchived','L2_designated_reading_ownerless_active_unarchived','L3_shared_loss','L4_policy_mismatch_after_all_owners_absent']}
dest=P(sys.argv[1]);dest.mkdir(exist_ok=False);(dest/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
fields=['row','fault','limb','policy','condition_verified','transition_ack','transition_error','current_needers','saved_needing_generations','active','archive','retry_ack','rollback_read','pre_gc_rollback_read','archive_error_count']
with (dest/'selected-matrix.csv').open('w') as f:
 w=csv.DictWriter(f,fields);w.writeheader()
 for n in selected:
  r=by[n];e=r['after-transition'];w.writerow({'row':n,'fault':r['fault'],'limb':r['limb'],'policy':r['policy'],'condition_verified':r['condition_verified'],'transition_ack':r['transition']['response_ok'],'transition_error':r['transition']['error'],'current_needers':e['current_needer'],'saved_needing_generations':len(e['saved_needing_generations']),'active':e['active'],'archive':e['archive'],'retry_ack':r['retry']['response_ok'],'rollback_read':r['rollback_read_rc'],'pre_gc_rollback_read':r['pre_gc_rollback_read_rc'],'archive_error_count':len(r['archive_faults'])})
print(json.dumps({'rows':len(rows),'selected_primary':len(primary),'parity_checks':len(parity),'parity_all':all(x['equal'] for x in parity),'native_read_checks':len(native),'native_all':all(x['rc']==0 and x['same_lookup'] for x in native),'replays':len(replays),'same_normalized_error':sum(x['same_normalized_error'] for x in replays),'same_endpoint':sum(x['same_endpoint'] for x in replays),'selected_retry_all_ack':summary['selected_retry_all_ack'],'first':summary['first_row_utc'],'last':summary['last_row_utc']}))

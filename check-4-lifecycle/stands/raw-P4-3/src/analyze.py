#!/usr/bin/python3
"""Read-only independent finite oracle; no controller/harness module import."""
import pathlib,json,sys,re,hashlib,csv,datetime,os
P=pathlib.Path
def read(p):return json.loads(p.read_text())
def current(s):return s['documents'][s['control']+'/current.json'].get('json',{})
def needs(doc,key):
 programs=set(doc.get('programs',{}))
 if key.startswith('shared-'):return bool(programs.intersection(doc.get('shared',{}).get(key[7:],[])))
 return key in programs
def present(s,key,place):return s['objects'].get('/var/lib/cal/'+place+'/'+key+'/operational.bin',{'error':'missing observation'})
def response(d,label):
 p=d/(label+'.json')
 return read(p) if p.exists() else {}
def joins(s,original,expected):
 instruments={k:v.get('sha256') for k,v in s['instrument'].items()}
 expected_instruments=expected['original' if original else 'layout']
 source_ok=all(instruments.get(k)==v for k,v in expected_instruments.items())
 docs=[current(s)]+[v.get('json',{}) for v in s['generations'].values()];payload_joins=[]
 for doc in docs:
  for name,item in doc.get('programs',{}).items():
   path=item.get('executable','/usr/local/lib/cal/'+name)
   wanted=item.get('sha256',expected['catalog'].get(name))
   found=s['payloads'].get(path,{})
   payload_joins.append({'generation':doc.get('generation'),'program':name,'path':path,'expected':wanted,'actual':found.get('sha256'),'ok':bool(wanted and found.get('exists') and found.get('sha256')==wanted)})
 return {'source_ok':source_ok,'payloads_ok':all(x['ok'] for x in payload_joins),'payloads':payload_joins}
def endpoint(d,s,key,baseline,policy,limb,readlabel):
 cur=current(s);gens={k:v.get('json',{}) for k,v in s['generations'].items()};a=present(s,key,'active');r=present(s,key,'archive');old=present(baseline,key,'active')
 owners=needs(cur,key);saved=[k for k,v in gens.items() if needs(v,key)];copies=[o for o in (a,r) if o.get('exists')]
 evidence_ok=all('error' not in o and 'exists' in o and (not o['exists'] or all(k in o for k in ['dev','ino','sha256'])) for o in [a,r,old]) and bool(old.get('exists'))
 continuity=all((o.get('dev'),o.get('ino'),o.get('sha256'))==(old.get('dev'),old.get('ino'),old.get('sha256')) for o in copies) if evidence_ok else None
 old_incarnation_present=any((o.get('dev'),o.get('ino'))==(old.get('dev'),old.get('ino')) for o in copies) if evidence_ok else None
 declared=s['documents']['/etc/cal/root.json'].get('json',{});personal=s['documents']['/home/alice/declaration.json'].get('json',{})
 designated={**declared,'programs':{**declared.get('programs',{}),**personal.get('programs',{})}}
 designated_needer=needs(designated,key)
 readresult=response(d,readlabel);shared_read_ok=readresult.get('rc')==0
 archived_now=r.get('exists',False);active_now=a.get('exists',False)
 return {'object_evidence_ok':evidence_ok,'current_generation':cur.get('generation'),'current_programs':sorted(cur.get('programs',{})),'saved_generations':sorted(gens),'saved_needing_generations':saved,'current_needer':owners,'designated_needer':designated_needer,'designated_equals_current':declared==cur.get('root') and personal==cur.get('personal',{}).get('alice'),'active':active_now,'archive':archived_now,'continuity':continuity,'old_incarnation_present':old_incarnation_present,'replacement_candidate':bool(copies and old_incarnation_present is False),'native_read_rc':readresult.get('rc'),
 'L1_protected_deletion':bool((owners or saved) and not old_incarnation_present) if evidence_ok else None,
 'L2_current_reading_ownerless_active_unarchived':bool(active_now and not owners and not archived_now) if evidence_ok else None,
 'L2_designated_reading_ownerless_active_unarchived':bool(active_now and not designated_needer and not archived_now) if evidence_ok else None,
 'L3_shared_loss':bool(limb=='shared' and owners and (archived_now or not active_now or not shared_read_ok)) if evidence_ok and (limb!='shared' or readresult.get('rc') is not None) else None,
 'L4_policy_mismatch_after_all_owners_absent':bool(not owners and not saved and ((policy=='keep' and not copies) or (policy=='delete' and archived_now))) if evidence_ok else None,
 'policy_constant':declared.get('archive')==policy and cur.get('archive')==policy,
 'active_identity':{k:a.get(k) for k in ('dev','ino','nlink','sha256')},'archive_identity':{k:r.get(k) for k in ('dev','ino','nlink','sha256')}}
def analyze(d,expected=None):
 if expected is None:expected=read(P(__file__).resolve().parent/'expected-hashes.json')
 m=read(d/'meta.json');o={k:m.get(k) for k in ['name','fault','limb','policy','original','complete','error','gown','gc_ids','rollback_target_retained']}
 if not m.get('complete'):return o
 base=read(d/'baseline.json');key=m['key'];o['baseline_joins']=joins(base,m['original'],expected)
 for phase,label in [('after-transition','after-transition-read'),('after-retry','after-retry-read')]:
  s=read(d/(phase+'.json'));e=endpoint(d,s,key,base,m['policy'],m['limb'],label);j=joins(s,m['original'],expected);e['joins']=j
  e['premises_complete']=e['object_evidence_ok'] and j['source_ok'] and j['payloads_ok'] and o['baseline_joins']['source_ok'] and o['baseline_joins']['payloads_ok'] and all('json' in v for v in s['generations'].values()) and all('json' in s['documents'].get(p,{}) for p in ['/etc/cal/root.json','/home/alice/declaration.json',s['control']+'/current.json']) and bool(current(s))
  if not e['premises_complete']:
   for k in list(e):
    if k.startswith('L'):e[k]=None
  o[phase]=e
 for label in ['transition','retry','rollback','prepare-rollback']:
  r=response(d,label)
  if r:o[label]={'rc':r.get('rc'),'response_ok':(r.get('response') or {}).get('ok'),'error':(r.get('response') or {}).get('error'),'start_ns':r.get('start_ns'),'end_ns':r.get('end_ns')}
 cond=read(d/'condition.json');o['condition']={k:cond[k] for k in ['class','after','verification'] if k in cond};f=cond['after'];err=cond.get('verification',{}).get('errno')
 o['condition_verified']={'healthy':True,'blocks':err==28 and f['f_bavail']==0 and f['f_ffree']>0,'inodes':err==28 and f['f_ffree']==0 and f['f_bavail']>0,'ro':err==30 and bool(f['f_flag']&os.ST_RDONLY)}[m['fault']]
 tr=(d/'transition.trace').read_text(errors='replace');pid=m['daemon_pid'];errors=[];mutations=[]
 for line in tr.splitlines():
  if re.search(r'\b(?:rename|renameat|renameat2|unlink|unlinkat|rmdir|mkdir|mkdirat|openat)\(',line) and ('/var/lib/cal/' in line or '= -1 ENOSPC' in line or '= -1 EROFS' in line):mutations.append(line)
  if re.search(r'= -1 (?:ENOSPC|EROFS|EXDEV|EACCES)\b',line):errors.append(line)
 o['syscall_errors']=errors;o['filesystem_mutations']=mutations
 o['archive_faults']=[x for x in errors if '/var/lib/cal/archive/' in x and re.match(r'^'+str(pid)+r'\s',x) and re.search(r'\b(rename|renameat|renameat2|unlink|unlinkat|rmdir)\(',x)]
 o['controller_errors']=[x for x in errors if re.match(r'^'+str(pid)+r'\s',x)]
 identities=[]
 for phase in ['before-attempt','after-transition','before-recovery','after-retry']:
  identities.append([(p['pid'],p['start_ticks']) for p in read(d/(phase+'.json'))['processes'] if p['pid']==pid])
 o['controller_alive_same_identity']=bool(identities[0]) and all(x==identities[0] for x in identities)
 o['quiescent']=all(not read(p)['live_consumers_or_handles'] for p in d.glob('*.json') if p.name in ['baseline.json','prepared.json','before-attempt.json','after-transition.json','before-recovery.json','after-retry.json','after-rollback.json'])
 o['rollback_read_rc']=response(d,'rollback-read').get('rc');o['pre_gc_rollback_read_rc']=response(d,'prepare-rollback-read').get('rc')
 o['runtime_source_hashes']=read(d/'before-attempt.json')['instrument']
 return o
if __name__=='__main__':
 root=P(sys.argv[1]);dest=P(sys.argv[2]);dest.mkdir(exist_ok=False)
 expected=read(P(__file__).resolve().parent/'expected-hashes.json');plan=read(P(__file__).resolve().parent/'matrix-plan.json')
 found={p.name:p for p in root.iterdir() if (p/'meta.json').exists()};rows=[]
 for name,fault,limb,policy,original in plan:
  if name in found:rows.append(analyze(found.pop(name),expected))
  else:rows.append({'name':name,'fault':fault,'limb':limb,'policy':policy,'original':original,'complete':False,'error':'planned row missing; coverage ?'})
 rows += [analyze(p,expected) for p in sorted(found.values())]
 (dest/'analysis.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n')
 fields=['name','fault','limb','policy','complete','ack','retry_ack','archive_faults','active','archive','current_needer','saved_needing','L1','L2_current','L2_designated','L3','L4','rollback_read']
 with (dest/'matrix.csv').open('w') as f:
  w=csv.DictWriter(f,fields);w.writeheader()
  for r in rows:
   e=r.get('after-transition',{});w.writerow({'name':r['name'],'fault':r['fault'],'limb':r['limb'],'policy':r['policy'],'complete':r['complete'],'ack':r.get('transition',{}).get('response_ok'),'retry_ack':r.get('retry',{}).get('response_ok'),'archive_faults':len(r.get('archive_faults',[])),'active':e.get('active'),'archive':e.get('archive'),'current_needer':e.get('current_needer'),'saved_needing':len(e.get('saved_needing_generations',[])),'L1':e.get('L1_protected_deletion'),'L2_current':e.get('L2_current_reading_ownerless_active_unarchived'),'L2_designated':e.get('L2_designated_reading_ownerless_active_unarchived'),'L3':e.get('L3_shared_loss'),'L4':e.get('L4_policy_mismatch_after_all_owners_absent'),'rollback_read':r.get('rollback_read_rc',r.get('pre_gc_rollback_read_rc'))})
 print(json.dumps({'rows':len(rows),'complete':sum(bool(r['complete']) for r in rows),'out':str(dest)}))

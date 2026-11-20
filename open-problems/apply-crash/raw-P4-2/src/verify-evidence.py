"""Recompute raw identities and literal absence separately from frozen analyzer alarms."""
import pathlib,json,hashlib,base64,sys,datetime
R=pathlib.Path(sys.argv[1]); S=R/'server'; failures=[]; rows=[]; checked_files=0
expected={
 '/usr/local/sbin/cald':hashlib.sha256((R/'source/cald.py').read_bytes()).hexdigest(),
 '/usr/local/lib/cal/apply-policy':hashlib.sha256((R/'source/apply-policy.py').read_bytes()).hexdigest(),
 '/root/q-main/radio-apply.py':hashlib.sha256((R/'source/radio-apply.py').read_bytes()).hexdigest()}
fixture=json.loads((R/'fixture/boot-snapshot.json').read_text())
for n in ('alpha','beta','worker'):expected['/usr/local/lib/cal/'+n]=fixture['files']['/usr/local/lib/cal/'+n]['sha256']
for n in ('calctl','cal-login'):expected['/usr/local/bin/'+n]=fixture['files']['/usr/local/bin/'+n]['sha256']
for mp in sorted((S/'results').glob('*/meta.json')):
 m=json.loads(mp.read_text());d=mp.parent;rf=[];snaps={}
 if m.get('status')!='complete':failures.append([m['id'],'incomplete']);continue
 for label in ('baseline','G2','before','precut',m['after_label'],'recovered'):
  snap=json.loads((d/(label+'.json')).read_text());snaps[label]=snap
  if snap['uuid']!='e9d11119-0042-4042-8042-000000000042':rf.append(label+':uuid')
  if snap['machine_id']!=fixture['machine_id']:rf.append(label+':machine_id')
  for path,rec in snap['files'].items():
   if 'bytes_b64' in rec:
    b=base64.b64decode(rec['bytes_b64']);checked_files+=1
    if len(b)!=rec['size'] or hashlib.sha256(b).hexdigest()!=rec['sha256']:rf.append(label+':raw hash '+path)
  for path,h in expected.items():
   if snap['files'].get(path,{}).get('sha256')!=h:rf.append(label+':source '+path)
  if label in ('before','precut') and snap.get('live_consumers'):rf.append(label+':live_consumer')
 for cp in d.glob('*.command.json'):
  c=json.loads(cp.read_text());stem=cp.name[:-13]
  for kind in ('stdout','stderr'):
   f=d/(stem+'.'+kind)
   if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=c[kind+'_sha256']:rf.append('command hash '+str(f))
 for ap in d.glob('*.ack.json'):
  a=json.loads(ap.read_text());stem=ap.name[:-9];raw=(d/(stem+'.stdout')).read_bytes()
  if not raw.endswith(b'\n') or json.loads(raw)!=a['response'] or a['rc']!=0 or not a['ack_valid']:rf.append('ACK '+str(ap))
 a=snaps[m['after_label']];cur=a['files'].get('/var/lib/cal/current.json',{}).get('json');root=a['files'].get('/etc/cal/root.json',{}).get('json')
 saved={p:r.get('json') for p,r in a['files'].items() if '/generations/' in p and p.endswith('.json')}
 views={'designated':root,'current':cur,'ack':m['ack']['response'].get('effective',m['ack']['response'].get('current'))}
 literal={}
 ledger=json.loads((R/'fixture/payload-ledger.json').read_text())
 for view,doc in views.items():
  if not isinstance(doc,dict):literal[view]={'evidence':'missing document','absent_recorded_payload_paths':None};continue
  names=set(doc.get('programs',{}))&set(ledger)
  literal[view]={'recorded_catalog_names':sorted(names),'absent_recorded_payload_paths':[ledger[n]['path'] for n in sorted(names) if not a['files'].get(ledger[n]['path'],{}).get('exists',False)]}
 lookup_paths=[p for p in a['files'] if p.endswith('/shared-lookup/lookup')]
 precut=snaps['precut'];current_pre=precut['files']['/var/lib/cal/current.json']['json']
 expected_beta_access=('beta' in current_pre['programs'])
 actual_access=json.loads((d/'after.access.json').read_text())
 recovery=snaps['recovered'];rc=recovery['files'].get('/var/lib/cal/current.json',{}).get('json',{})
 expected_owner_set={'beta'} if m['op']=='B' else set()
 recovered_owners_match=set(rc.get('programs',{}))==expected_owner_set
 r={'id':m['id'],'integrity_failures':rf,'literal_payload_existence_by_view':literal,
    'designated_equals_current':root==cur.get('root') if cur else None,'lookup_paths_after':lookup_paths,
    'saved_generations_after':len(saved),'saved_owning_after':sum(bool(set((x or {}).get('programs',{}))&{'alpha','beta'}) for x in saved.values()),
    'ack_expected_beta_lookup_attempted':not expected_beta_access or 'beta-lookup' in actual_access,
    'recovery_current_owners_match_request':recovered_owners_match,
    'recovery_lookup_paths':[p for p in recovery['files'] if p.endswith('/shared-lookup/lookup')]}
 rows.append(r);failures.extend([m['id'],f] for f in rf)
# Validate the exact extracted text is contained in the preregistered document.
import re,html
paper=(R/'inputs/PAPER.html').read_text();protocol=(R/'PROTOCOL.md').read_text()
for title in ['9.1. General rules','9.2. Check 1: census','9.5. Check 4: lifecycle of a derivative']:
 start=paper.index('<h3>'+title+'</h3>');end=paper.find('<h3>',start+4)
 quote=html.unescape(re.sub('<[^>]+>','',paper[start:end])).strip()
 if quote not in protocol:failures.append(['protocol','quotation '+title])
result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'recorded_file_bytes_rehashed':checked_files,'rows':rows,'failures':failures,'note':'Frozen analyzer literal_p2_object_absence/payload_absences are composite payload-validation alarms. This verifier reports actual exists=false separately per view and does not adopt an authority selector.'}
(R/'integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'rows':len(rows),'recorded_file_bytes_rehashed':checked_files,'failures':failures},indent=2))

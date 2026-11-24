import csv,json,pathlib,collections,re
base=pathlib.Path('A3/c1');target=base/'part-developer.tsv'
fields=['id','decision','sentences','what_it_does','basis','reason']
inputrows=list(csv.DictReader(open('A3/in/part-developer.tsv'),delimiter='\t'))
byid={r['id']:r for r in inputrows}
existing=list(csv.DictReader(open(target),delimiter='\t'));done={r['id'] for r in existing}
with open(target,'a',newline='') as f:
 w=csv.DictWriter(f,fields,delimiter='\t',lineterminator='\n')
 for part in ['code','runtime']:
  for r in csv.DictReader(open(base/f'part-developer.{part}.tsv'),delimiter='\t'):
   if r['id'] not in done:w.writerow(r);f.flush();done.add(r['id'])
rows=list(csv.DictReader(open(target),delimiter='\t'));changes=[]
for r in rows:
 original=dict(r);source=byid[r['id']]
 if source['kind']=='2:stored-ownership-unresolved' and '/.cache/go-build/' in source['name']:
  ms=list(csv.DictReader(open(pathlib.Path('A3/in/raw/developer')/json.loads(source['members'])['file']),delimiter='\t'))
  if any(m['path'].endswith('-d') for m in ms):
   r.update(decision='UNKNOWN',sentences='S8.2-9,S8.2-15,S8.2-16,S8.2-20',what_it_does='Go cache action indexes and saved build-output payloads.',reason='Cached output contents and possible execution through another program are unrecorded; non-executable permission alone cannot distinguish records from code requiring source-line coverage.')
 if r['id']=='developer-df39a529b53c474304339913':
  r['reason']='systemd and modular libvirt daemons (INSTALLED-PACKAGE) create these sockets and runtime directories; members name the daemon families, rather than solely libvirtd.'
 if r['id']=='developer-bc2eff9fbcd1c8ce543692ad':
  r['reason']='virtqemud (INSTALLED-PACKAGE) creates QEMU daemon runtime state; member filesystem facts are runtime, so no separate declaration line applies.'
 if r['id'] in ['developer-5eb44d0def12c43daae1fbb3','developer-525ed7742d9bd835216a4b96','developer-da97ea3d424d9e95f97e9301']:
  r.update(decision='UNKNOWN',sentences='S8.2-13,S8.2-14,S8.2-17',reason='The launch setting is established, but creation provenance is unknown; custom naming and user location do not distinguish own settings from installation-created defaults.')
 if r['id']=='developer-d1fbc4bd76f69c08a8b6ecf7':
  r.update(decision='UNKNOWN',sentences='S8.2-7,S8.2-9,S8.2-15,S8.2-16',what_it_does='Python distribution represented by metadata and adjacent payload in the uv cache.',reason='The represented distribution includes code, not only metadata; installation reason and payload integrity are unknown, so package, program, or cache coverage cannot be settled.')
 if r!=original:changes.append({'id':r['id'],'previous':original['decision'],'decision':r['decision'],'reason':r['reason']})
if changes:
 tmp=base/'part-developer.revised.tmp'
 with open(tmp,'w',newline='') as f:
  w=csv.DictWriter(f,fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
 tmp.replace(target)
 cp=base/'part-developer.revisions.tsv'
 with open(cp,'a',newline='') as f:
  w=csv.DictWriter(f,['id','previous','decision','reason'],delimiter='\t',lineterminator='\n')
  if cp.stat().st_size==0:w.writeheader()
  w.writerows(changes)
# Exact structural validation, including all fifteen labels and field budgets.
allowed='INSTALLED-OWN INSTALLED-PACKAGE INSTALLED-DERIVED PROGRAM-OWN PROGRAM-DERIVED SETTING-OWN SETTING-DEFAULT RECORD MATERIAL RUNTIME ACTION GAP-NONE GAP-TWO UNKNOWN MIXED'.split()
a=collections.Counter(r['id'] for r in inputrows);b=collections.Counter(r['id'] for r in rows)
assert a==b and len(rows)==len(inputrows)==len(b)==6409
assert all(n==1 for n in b.values())
sentences=set(re.findall(r'\*\*(S8\.[123]-\d+)\*\*',open('SENTENCES.md').read()))
for r in rows:
 assert list(r)==fields and r['decision'] in allowed,r
 assert len(r['what_it_does'].split())<=15 and len(r['reason'].split())<=30,r
 assert all('\t' not in v and '\n' not in v and '\r' not in v for v in r.values()),r
 assert all(s in sentences for s in r['sentences'].split(',')),r
 assert r['basis'] in ('evidence','none') or r['basis'].startswith(('raw:','doc:')),r
counts=collections.Counter(r['decision'] for r in rows)
with open(base/'part-developer.done','w') as f:
 for d in allowed:f.write(f'{d}\t{counts[d]}\n')
print('Validated',len(rows),'unique matching rows')
print(json.dumps({d:counts[d] for d in allowed}))

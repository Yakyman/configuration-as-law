import csv,json,collections,pathlib,re,os
csv.field_size_limit(10000000)
base=pathlib.Path('D1/in/raw/void')
rows=list(csv.DictReader(open('D1/in/part-void.tsv'),delimiter='\t'))
pfs=collections.defaultdict(list)
for x in csv.DictReader(open(base/'package-files.tsv'),delimiter='\t'):pfs[x['path']].append(x)
header=['id','decision','sentences','what_it_does','basis','reason']
out=pathlib.Path('D1/c1/part-void.tsv')
existing={x['id'] for x in csv.DictReader(open(out),delimiter='\t')} if out.exists() else set()
f=out.open('a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
if not existing:w.writerow(header);f.flush()
rules=collections.defaultdict(list)
def emit(x,d,s,what,b,why,rule):
 rules[rule].append(x['id'])
 if x['id'] in existing:return
 assert len(what.split())<=15,(x['id'],what)
 assert len(why.split())<=30,(x['id'],why)
 assert not any('\t' in z or '\n' in z for z in [what,b,why])
 w.writerow([x['id'],d,s,what,b,why]);f.flush();existing.add(x['id'])
for x in rows:
 k=x['kind'];m=json.loads(x['members']);name=x['name'];ev='raw:D1/in/raw/void/'+x['evidence']
 if k=='L1:package':
  reason=m['reason']
  if reason=='unknown' and m['manager']=='python' and '/cal-marionette/' in m['location']:
   emit(x,'INSTALLED-DERIVED','S8.1-6,S8.2-7,S8.2-8,S8.2-16','Python dependency installed for marionette_driver.','raw:D1/in/control/void/actions-logs/actions-logs/browser_extension.log','Installation log explicitly collects this distribution through marionette_driver dependencies; its line covers the dependency.','python-dependencies');continue
  d={'explicit':'INSTALLED-OWN','dependency':'INSTALLED-DERIVED','unknown':'UNKNOWN'}[reason]
  why={'explicit':'The installed package was explicitly selected; no containing package or derivation is established. It needs its own line.','dependency':'The installed package was obtained as a dependency; the recorded requesting package line covers it.','unknown':'Package existence is established, but explicit selection versus dependency or containing-package provenance is unknown; the required recording line cannot be selected.'}[reason]
  emit(x,d,'S8.1-6,S8.2-7,S8.2-8,S8.2-16','Installed package managed as one unit.',ev,why,'package-'+reason)
 elif k in ['L1:access-rule','L1:saved-network-file','L2:image'] and any(p['integrity']=='unchanged' for p in pfs[name]):
  emit(x,'INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16','Unchanged package file supplying policy, defaults, or boot components.','raw:D1/in/raw/void/package-files.tsv','Manifest ownership and unchanged integrity answer the first question affirmatively; the supplying package line covers the file.','unchanged-files')
 elif k=='L1:polkit-action':
  candidates=[]
  for z in rows:
   if z['kind']=='L1:access-rule' and name in json.loads(z['members']).get('content','') and z['name'].endswith('.policy'):
    candidates.extend(pfs[z['name']])
  if any(p['integrity']=='unchanged' for p in candidates):
   emit(x,'INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16','Registered authorization action defined in packaged XML policy.','raw:D1/in/raw/void/package-files.tsv','The action definition occurs in an unchanged packaged policy file. The first question prevails over its access-policy function.','polkit-packaged')
f.close()
pathlib.Path('D1/c1/part-void.main-rules.json').write_text(json.dumps(rules,indent=2))
print('Appended/preserved',len(existing),'rows')

import csv,json,collections,pathlib
ROOT=pathlib.Path('D1b/handoff/gentoo')
OUT=pathlib.Path('D1b/c1/part-gentoo.tsv')
HEADER=['id','decision','sentences','what_it_does','basis','reason']
def read(p):
 with open(p) as f:return list(csv.DictReader(f,delimiter='\t'))
def decode(s):
 while isinstance(s,str):s=json.loads(s)
 return s
rows=[r for r in read('D1b/in/part-gentoo.tsv') if r['kind']=='L2:stored-ownership-unresolved']
aliases={'/lib64/':'/usr/lib64/','/lib/':'/usr/lib/','/bin/':'/usr/bin/','/sbin/':'/usr/bin/','/usr/sbin/':'/usr/bin/'}
def norm(p):
 for a,b in aliases.items():
  if p.startswith(a):return b+p[len(a):]
 return p
pkg=collections.defaultdict(list)
for p in read(ROOT/'package-files.tsv'):pkg[norm(p['path'])].append(p)
# Read every complete table, including members not selected by a rule.
members={}
for r in rows:
 meta=decode(r['members']); ms=read(ROOT/meta['file']); assert meta['complete'] and len(ms)==meta['count']; members[r['id']]=ms
rules=collections.defaultdict(list)
existing={r['id'] for r in read(OUT)} if OUT.exists() else set()
f=OUT.open('a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
if not existing:w.writerow(HEADER)
def put(r,rule,d,s,what,why,basis=None):
 if r['id'] in existing:return
 assert len(what.split())<=15 and len(why.split())<=30,(what,why)
 w.writerow([r['id'],d,s,what,basis or 'raw:'+str(ROOT/decode(r['members'])['file']),why]); f.flush();existing.add(r['id']);rules[rule].append(r['id'])
for r in rows:
 ms=members[r['id']];name=r['name']
 if name.startswith('/var/db/repos'):
  assert all(m['persistence']=='persistent' and not pkg[norm(m['path'])] for m in ms)
  put(r,'repository-provenance','UNKNOWN','S8.2-7,S8.2-9,S8.2-15,S8.2-16','Repository recipes, support files, metadata or directory entries.','Missing acquisition history: system-obtained from a recorded source versus personally supplied repository entries; code requires own/derived lines, noncode requires record/material provenance.')
 elif name.startswith('/usr/lib/modules') or all(any(p['integrity']=='unchanged' for p in pkg[norm(m['path'])]) for m in ms):
  known=[m for m in ms if any(p['integrity']=='unchanged' for p in pkg[norm(m['path'])])]
  other=[m for m in ms if m not in known]
  if not other:
   put(r,'unchanged-package-members','INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16','Unchanged package files, resolved through observed filesystem aliases.','Every member matches an unchanged package-file entry through observed aliases; the supplying package line covers it.','raw:D1b/handoff/gentoo/package-files.tsv')
  elif all(m['type']=='directory' for m in other):
   if known:put(r,'package-files-and-unverified-directories','MIXED','S8.2-7,S8.2-8,S8.2-15,S8.2-16','Kernel package files and persistent directory entries.','Files: INSTALLED-PACKAGE (unchanged package matches); directories: UNKNOWN (no supplied-directory integrity or creator history).')
   else:put(r,'unverified-module-directories','UNKNOWN','S8.2-7,S8.2-15','Persistent kernel module directory entries.','Directory provenance and original metadata comparison are unrecorded; installed package directories, program-created records and personally created material remain distinguishable possibilities.')
  else:raise ValueError(r)
f.close()
with open('D1b/c1/gentoo-group-rule-ids.json','w') as f:json.dump(rules,f,indent=2)
print('Appended rules', {k:len(v) for k,v in rules.items()})
print('Remaining',len([r for r in rows if r['id'] not in existing]))

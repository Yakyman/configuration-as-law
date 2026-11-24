import csv,json,collections,posixpath,pathlib
base=pathlib.Path('D1/c1'); details=json.loads((base/'part-alma.1.details.json').read_text()); replacements={}
for x in details:
 cats=collections.defaultdict(list)
 for m in x['members']:cats[m['decision']].append(m)
 if len(cats)<2:continue
 types=collections.defaultdict(set)
 for m in x['members']:types[m['type']].add(m['decision'])
 if all(len(v)==1 for v in types.values()):
  text='; '.join(f'{next(iter(d))}: all {t} members' for t,d in sorted(types.items()))+'.'
 else:
  assert len(cats)==2
  a,b=sorted(cats,key=lambda d:len(cats[d])); names=', '.join(posixpath.basename(m['member']) for m in cats[a])
  text=f'{a}: {names}; {b}: all other members.'
 assert len(text.split())<=30,(x['id'],text)
 replacements[x['id']]=text
for name in ['part-alma.tsv','part-alma.1.tsv']:
 p=base/name
 with p.open() as f:r=csv.DictReader(f,delimiter='\t');h=r.fieldnames;rows=list(r)
 for r in rows:
  if r['id'] in replacements:r['reason']=replacements[r['id']]
 with p.open('w') as f:w=csv.DictWriter(f,fieldnames=h,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
print('Compacted mixed descriptions',len(replacements))

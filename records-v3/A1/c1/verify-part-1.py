import csv,collections,pathlib,re
base=pathlib.Path('A1/c1')
header=['id','decision','sentences','what_it_does','basis','reason']
source=list(csv.DictReader(open('A1/in/part-1.tsv'),delimiter='\t'))
out=base/'part-1.tsv'
rows=list(csv.DictReader(out.open(),delimiter='\t')); seen={x['id'] for x in rows}
# Append finalized independently completed subsets; preserve all earlier rows.
with out.open('a') as f:
 w=csv.DictWriter(f,header,delimiter='\t',lineterminator='\n')
 for name in ['part-1.packages.tsv','part-1.units.tsv','part-1.owned.tsv']:
  for x in csv.DictReader((base/name).open(),delimiter='\t'):
   if x['id'] not in seen:w.writerow(x);f.flush();seen.add(x['id'])
with out.open() as f:
 reader=csv.DictReader(f,delimiter='\t');assert reader.fieldnames==header;rows=list(reader)
expected=collections.Counter(x['id'] for x in source);actual=collections.Counter(x['id'] for x in rows)
assert expected==actual,(expected-actual,actual-expected)
assert len(rows)==len(source)==len(actual)
assert all(n==1 for n in actual.values())
valid=['MUST','NOT','HOLE','UNKNOWN','MIXED']
for x in rows:
 assert set(x)==set(header),x['id']
 assert x['decision'] in valid,x
 assert 0<len(x['what_it_does'].split())<=15,x
 assert 0<len(x['reason'].split())<=30,x
 assert all(re.fullmatch(r'S2\.2-(?:[1-9]|1[0-6])|S3-[12]',s) for s in x['sentences'].split(',')),x
 assert x['basis'] in ['none','evidence'] or x['basis'].startswith(('raw:','doc:')),x
 assert all('\t' not in v and '\n' not in v for v in x.values()),x
# Each completed subset must agree with the corresponding merged rows.
byid={x['id']:x for x in rows}
for name in ['part-1.packages.tsv','part-1.units.tsv','part-1.owned.tsv','stored-decisions.tsv']:
 for x in csv.DictReader((base/name).open(),delimiter='\t'):assert x==byid[x['id']],(name,x['id'])
counts=collections.Counter(x['decision'] for x in rows)
(base/'part-1.done').write_text(''.join(d+'\t'+str(counts[d])+'\n' for d in valid))
print('Verified',len(rows),'unique input/output IDs, exact header, decisions, field word limits, sentence scope, merged subset consistency.')
for d in valid:print(d,counts[d])

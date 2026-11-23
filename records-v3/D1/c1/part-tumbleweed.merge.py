import csv,collections,pathlib,json,re,sys
p=pathlib.Path('D1/c1')
head=['id','decision','sentences','what_it_does','basis','reason']
source=list(csv.DictReader(open('D1/in/part-tumbleweed.tsv'),delimiter='\t'))
expected={x['id'] for x in source}
out=p/'part-tumbleweed.tsv'
existing=list(csv.DictReader(out.open(),delimiter='\t'))
seen={x['id'] for x in existing}
assert len(seen)==len(existing)
for shard in sys.argv[1:]:
 s=p/('part-tumbleweed.'+shard+'.tsv')
 with s.open() as f:
  reader=csv.DictReader(f,delimiter='\t');assert reader.fieldnames==head
  data=list(reader)
 assert len(data)==len({x['id'] for x in data})
 with out.open('a',newline='') as f:
  w=csv.DictWriter(f,fieldnames=head,delimiter='\t',lineterminator='\n')
  for r in data:
   assert r['id'] in expected
   if r['id'] in seen:
    assert next(x for x in existing if x['id']==r['id'])==r
   else:
    w.writerow(r);f.flush();seen.add(r['id']);existing.append(r)
rows=list(csv.DictReader(out.open(),delimiter='\t'))
allowed=['MUST','NOT','HOLE','UNKNOWN','MIXED']
known_sentences=set(re.findall(r'\*\*(S[0-9.]+-\d+)\*\*',pathlib.Path('SENTENCES.md').read_text()))
for r in rows:
 assert set(r)==set(head)
 assert r['decision'] in allowed
 assert all(t in known_sentences for t in r['sentences'].split(','))
 assert len(r['what_it_does'].split())<=15,(r['id'],'description')
 assert len(r['reason'].split())<=30,(r['id'],'reason')
 assert all('\t' not in v and '\n' not in v and '\r' not in v for v in r.values())
 assert r['basis'] in ['evidence','none'] or r['basis'].startswith(('doc:http','raw:'))
 assert '/home/' not in str(r)
ids=[x['id'] for x in rows]
assert len(ids)==len(set(ids))
assert set(ids)<=expected
counts=collections.Counter(x['decision'] for x in rows)
if len(rows)==len(source):
 assert set(ids)==expected
 assert len(source)==len(expected)
 with (p/'part-tumbleweed.done').open('w') as f:
  for d in allowed:f.write(f'{d}\t{counts[d]}\n')
 print('Complete: exact input/output ID sets and counts, uniqueness, decisions, sentence IDs and field limits verified.')
else:print('Partial:',len(rows),'of',len(source))
print(dict(counts))

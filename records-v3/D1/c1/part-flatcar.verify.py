import csv,collections,pathlib,re,json
base=pathlib.Path('D1/c1')
source=list(csv.DictReader(open('D1/in/part-flatcar.tsv'),delimiter='\t'))
with (base/'part-flatcar.tsv').open(encoding='utf-8',newline='') as f:
 reader=csv.DictReader(f,delimiter='\t')
 assert reader.fieldnames==['id','decision','sentences','what_it_does','basis','reason']
 rows=list(reader)
assert len(rows)==len(source)
assert collections.Counter(r['id'] for r in rows)==collections.Counter(r['id'] for r in source)
assert all(n==1 for n in collections.Counter(r['id'] for r in rows).values())
allowed=['MUST','NOT','HOLE','UNKNOWN','MIXED']
valid=set(re.findall(r'\*\*(S[23][\d.]*-\d+)\*\*',open('SENTENCES.md').read()))
for row in rows:
 assert set(row)=={'id','decision','sentences','what_it_does','basis','reason'} and None not in row.values()
 assert row['decision'] in allowed
 assert len(row['what_it_does'].split())<=15,(row['id'],'description word limit')
 assert len(row['reason'].split())<=30,(row['id'],'reason word limit')
 assert all('\t' not in v and '\n' not in v and '\r' not in v for v in row.values())
 assert set(row['sentences'].split(','))<=valid,(row['id'],'sentence identifier')
 assert all(s.startswith('S2.2-') or s in ['S3-1','S3-2'] for s in row['sentences'].split(','))
 b=row['basis']
 assert b in ['evidence','none'] or b.startswith(('raw:','doc:'))
 if b.startswith('raw:'):
  s=re.sub(r':\d+$','',b[4:])
  f=pathlib.Path(s) if s.startswith('D1/') else pathlib.Path('D1/in')/s if s.startswith('raw/') else pathlib.Path('D1/in/raw')/s
  assert f.is_file(),(row['id'],'raw file missing',str(f))
counts=collections.Counter(r['decision'] for r in rows)
with (base/'part-flatcar.done').open('w',encoding='utf-8') as f:
 for k in allowed:f.write(f'{k}\t{counts[k]}\n')
print(json.dumps({'rows':len(rows),'unique_ids':len({r['id'] for r in rows}),'same_ids_same_count_each_once':True,'valid_decisions':True,'counts':{k:counts[k] for k in allowed}}))

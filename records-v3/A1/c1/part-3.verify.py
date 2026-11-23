"""Merge completed subset rows without replacing prior work; validate final deliverables."""
import csv
from collections import Counter
from pathlib import Path

folder=Path('A1/c1')
header=['id','decision','sentences','what_it_does','basis','reason']
allowed=['MUST','NOT','HOLE','UNKNOWN','MIXED']
source=list(csv.DictReader(Path('A1/in/part-3.tsv').open(),delimiter='\t'))
source_ids=[r['id'] for r in source]
assert len(set(source_ids))==len(source_ids)
sentence_ids={line.split('**')[1] for line in Path('SENTENCES.md').read_text().splitlines() if line.startswith('- **')}

def read(path):
 with path.open() as f:
  reader=csv.DictReader(f,delimiter='\t')
  assert reader.fieldnames==header,(path,reader.fieldnames)
  rows=list(reader)
 for r in rows:
  assert set(r)==set(header) and all(v is not None for v in r.values()),(path,r)
  assert r['id'] in source_ids and r['decision'] in allowed,(path,r)
  assert all(s in sentence_ids for s in r['sentences'].split(',')),(path,r)
  assert len(r['what_it_does'].split())<=15,(path,r)
  assert len(r['reason'].split())<=30,(path,r)
  assert r['basis'] in ['evidence','none'] or r['basis'].startswith(('raw:','doc:')),(path,r)
  assert not any('\t' in v or '\n' in v or '\r' in v for v in r.values()),(path,r)
 assert len({r['id'] for r in rows})==len(rows),path
 return rows

out=folder/'part-3.tsv'
existing=read(out)
by_id={r['id']:r for r in existing}
for suffix in ['store','stored','units']:
 path=folder/f'part-3.{suffix}.tsv'
 if not path.exists(): continue
 rows=read(path)
 with out.open('a') as f:
  writer=csv.DictWriter(f,fieldnames=header,delimiter='\t',lineterminator='\n')
  for row in rows:
   if row['id'] in by_id:
    assert row==by_id[row['id']],('Conflicting existing row',row['id'])
    continue
   writer.writerow(row); f.flush(); by_id[row['id']]=row
rows=read(out)
counts=Counter(r['decision'] for r in rows)
print('Saved rows:',len(rows),'of',len(source))
print(dict(counts))
if len(rows)!=len(source):
 print('Incomplete: no done marker written.')
 raise SystemExit(0)
assert Counter(r['id'] for r in rows)==Counter(source_ids)
for suffix in ['core','store','stored','units']:
 if not (folder/f'part-3.{suffix}.notes.md').exists():
  print('Awaiting notes:', suffix)
  raise SystemExit(0)
with (folder/'part-3.notes.md').open('w') as f:
 f.write('# Part 3 classification notes\n\n')
 for suffix in ['core','store','stored','units']:
  f.write((folder/f'part-3.{suffix}.notes.md').read_text()+'\n\n')
 f.write('## Mechanical verification\n\nInput and output ids have the same set and count, with each id occurring once. All decisions, sentence references, field counts, and word limits were checked by `part-3.verify.py`.\n')
(folder/'part-3.done').write_text(''.join(f'{decision}\t{counts[decision]}\n' for decision in allowed))
print('Verified; notes and done marker written.')

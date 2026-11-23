"""Append completed c1 fragments; validate the requested TSV contract and write counts."""
import argparse
import collections
import csv
import re
from pathlib import Path

root=Path(__file__).resolve().parents[2]
folder=root/'A1/c1'
header=['id','decision','sentences','what_it_does','basis','reason']
allowed=['MUST','NOT','HOLE','UNKNOWN','MIXED']
p=argparse.ArgumentParser()
p.add_argument('--merge',nargs='*',default=[])
p.add_argument('--complete',action='store_true')
a=p.parse_args()

def read(path):
 with path.open(encoding='utf-8',newline='') as f:
  reader=csv.DictReader(f,delimiter='\t')
  assert reader.fieldnames==header,(str(path),'header')
  data=list(reader)
 for row in data:
  assert set(row)==set(header) and all(v is not None for v in row.values()),row
  assert all('\t' not in v and '\n' not in v and '\r' not in v for v in row.values()),row
 return data

inputs=list(csv.DictReader((root/'A1/in/part-2.tsv').open(),delimiter='\t'))
inids=[r['id'] for r in inputs]
assert len(inids)==len(set(inids))
valid_sentences=set(re.findall(r'\*\*(S[0-9.]+-\d+)\*\*',(root/'SENTENCES.md').read_text()))
out=folder/'part-2.tsv'
rows=read(out)
seen={r['id']:r for r in rows}
assert len(seen)==len(rows)
for name in a.merge:
 fragment=folder/name
 incoming=read(fragment)
 with out.open('a',encoding='utf-8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=header,delimiter='\t',lineterminator='\n')
  for row in incoming:
   if row['id'] in seen:
    assert seen[row['id']]==row,('conflicting duplicate',row['id'])
    continue
   assert row['id'] in inids,('unexpected id',row['id'])
   writer.writerow(row)
   f.flush()
   seen[row['id']]=row
rows=read(out)
for r in rows:
 assert r['decision'] in allowed,r
 assert len(r['what_it_does'].split())<=15,r
 assert len(r['reason'].split())<=30,r
 assert r['basis'] in ('evidence','none') or r['basis'].startswith(('raw:','doc:')),r
 if r['basis'].startswith('raw:'):
  assert (root/'A1/in/raw'/r['basis'][4:]).is_file(),r
 ids=r['sentences'].split(',')
 assert all(i in valid_sentences and (i.startswith('S2.2-') or i in ('S3-1','S3-2')) for i in ids),r
 assert not re.search(r'/home/[^/\s]+|/root(?:/|\b)', '\n'.join(r.values())),r
outids=[r['id'] for r in rows]
assert len(outids)==len(set(outids))
assert set(outids)<=set(inids)
counts=collections.Counter(r['decision'] for r in rows)
if a.complete:
 assert len(outids)==len(inids) and set(outids)==set(inids),(len(outids),len(inids),set(inids)-set(outids))
 (folder/'part-2.done').write_text(''.join(f'{d}\t{counts[d]}\n' for d in allowed),encoding='utf-8')
print('rows',len(rows),'of',len(inputs))
for d in allowed: print(d,counts[d])

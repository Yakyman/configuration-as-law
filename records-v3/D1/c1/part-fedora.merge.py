import csv,collections,re
from pathlib import Path
root=Path('D1/c1')
header=['id','decision','sentences','what_it_does','basis','reason']
source=list(csv.DictReader(open('D1/in/part-fedora.tsv'),delimiter='\t'))
allowed={'MUST','NOT','HOLE','UNKNOWN','MIXED'}
p=root/'part-fedora.tsv'
current=list(csv.DictReader(p.open(),delimiter='\t')) if p.exists() else []
assert len({r['id'] for r in current})==len(current)
seen={r['id'] for r in current}
valid_ids={r['id'] for r in source}
with p.open('a',newline='') as f:
 w=csv.DictWriter(f,header,delimiter='\t',lineterminator='\n')
 if not current:w.writeheader()
 for suffix in ['units','policy','rpm']:
  shard=root/f'part-fedora.{suffix}.tsv'
  if not shard.exists():continue
  with shard.open() as sf:
   rd=csv.DictReader(sf,delimiter='\t')
   assert rd.fieldnames==header,(shard,rd.fieldnames)
   for r in rd:
    assert r['id'] in valid_ids,r
    if r['id'] in seen:
     old=next(x for x in current if x['id']==r['id'])
     assert r==old,('conflicting existing row',r['id'])
     continue
    assert set(r)==set(header),r
    assert r['decision'] in allowed,r
    assert len(r['what_it_does'].split())<=15,r
    assert len(r['reason'].split())<=30,r
    assert all('\t' not in v and '\n' not in v for v in r.values()),r
    w.writerow(r);f.flush();seen.add(r['id']);current.append(r)
with (root/'part-fedora.notes.md').open('w') as f:
 f.write('# Fedora c1 classification notes\n\nThese sections document the current independent c1 classification, its rules, sources and manual checks. The append-only result is `part-fedora.tsv`. The merger retains existing rows and rejects conflicting duplicates. Each shard is restricted to disjoint input kinds.\n\n')
 for suffix in ['main','units','policy','rpm']:
  note=root/f'part-fedora.{suffix}.notes.md'
  if note.exists():f.write(note.read_text()+'\n\n')
counts=collections.Counter(r['decision'] for r in current)
for r in current:
 assert set(r)==set(header),r
 assert r['decision'] in allowed,r
 assert len(r['what_it_does'].split())<=15,r
 assert len(r['reason'].split())<=30,r
 assert re.fullmatch(r'(?:S2\.2-\d+|S3-[12])(?:,(?:S2\.2-\d+|S3-[12]))*',r['sentences']),r
 assert r['basis'] in ('evidence','none') or r['basis'].startswith(('raw:','doc:')),r
 assert all('\t' not in v and '\n' not in v for v in r.values()),r
assert len({r['id'] for r in current})==len(current)
assert seen<=valid_ids
if seen==valid_ids:
 assert len(source)==len(current)==len(valid_ids)
 with (root/'part-fedora.done').open('w') as f:
  for d in ['MUST','NOT','HOLE','UNKNOWN','MIXED']:f.write(f'{d}\t{counts[d]}\n')
print('Rows',len(current),'/',len(source),dict(counts))

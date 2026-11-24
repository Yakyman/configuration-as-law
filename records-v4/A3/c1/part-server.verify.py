import csv,collections,pathlib,re,sys
D=pathlib.Path('A3/c1')
header=['id','decision','sentences','what_it_does','basis','reason']
allowed='INSTALLED-OWN INSTALLED-PACKAGE INSTALLED-DERIVED PROGRAM-OWN PROGRAM-DERIVED SETTING-OWN SETTING-DEFAULT RECORD MATERIAL RUNTIME ACTION GAP-NONE GAP-TWO UNKNOWN MIXED'.split()
def read(path):
 with path.open(newline='',encoding='utf-8') as f:
  reader=csv.DictReader(f,delimiter='\t');assert reader.fieldnames==header,(path,reader.fieldnames)
  return list(reader)
source=list(csv.DictReader(open('A3/in/part-server.tsv'),delimiter='\t'))
source_ids=[r['id'] for r in source];assert len(set(source_ids))==len(source_ids)
valid_sentences=set(re.findall(r'\*\*(S8\.[123]-\d+)\*\*',pathlib.Path('SENTENCES.md').read_text()))
out=D/'part-server.tsv'
existing=read(out) if out.exists() else []
byid={r['id']:r for r in existing};assert len(byid)==len(existing)
with out.open('a',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=header,delimiter='\t',lineterminator='\n')
 if not existing:w.writeheader()
 for name in ['main','code','stored']:
  part=D/f'part-server.{name}.tsv'
  if not part.exists():continue
  for r in read(part):
   if r['id'] in byid:
    assert r==byid[r['id']],('conflicting existing row',r['id'])
    continue
   assert r['id'] in source_ids,(part,r['id'])
   assert r['decision'] in allowed,r
   assert len(r['what_it_does'].split())<=15,r
   assert len(r['reason'].split())<=30,r
   assert set(r['sentences'].split(','))<=valid_sentences,r
   assert r['basis'] in ('evidence','none') or r['basis'].startswith(('raw:','doc:')),r
   assert all('\t' not in v and '\n' not in v and '\r' not in v for v in r.values()),r
   w.writerow(r);f.flush();byid[r['id']]=r
if '--finish' in sys.argv:
 final=read(out);counts=collections.Counter(r['id'] for r in final)
 assert len(final)==len(source_ids),(len(final),len(source_ids))
 assert set(counts)==set(source_ids)
 assert all(n==1 for n in counts.values())
 assert all(r['decision'] in allowed for r in final)
 totals=collections.Counter(r['decision'] for r in final)
 (D/'part-server.done').write_text(''.join(f'{d}\t{totals[d]}\n' for d in allowed),encoding='utf-8')
 notes=['# Server classification c1\n\nThe following sections contain the rules, manual checks and evidence for all three disjoint parts. Structural validation checks exact input/output ID equality, counts, uniqueness, permitted decisions, sentence IDs, fields and word limits. No independent acceptance is claimed.\n']
 for name in ['main','code','stored']:notes.append((D/f'part-server.{name}.notes.md').read_text())
 (D/'part-server.notes.md').write_text('\n\n'.join(notes),encoding='utf-8')
 print(dict(totals))
else:print(f'Appended/retained {len(byid)} of {len(source_ids)} rows; no completion marker written.')

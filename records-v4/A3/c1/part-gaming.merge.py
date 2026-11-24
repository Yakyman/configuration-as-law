"""Append completed parts and verify the exact input/output contract."""
import csv,collections,pathlib,re
D=pathlib.Path('A3/c1');I=pathlib.Path('A3/in/part-gaming.tsv')
H=['id','decision','sentences','what_it_does','basis','reason']
DECISIONS=['INSTALLED-OWN','INSTALLED-PACKAGE','INSTALLED-DERIVED','PROGRAM-OWN','PROGRAM-DERIVED','SETTING-OWN','SETTING-DEFAULT','RECORD','MATERIAL','RUNTIME','ACTION','GAP-NONE','GAP-TWO','UNKNOWN','MIXED']
expected=list(csv.DictReader(I.open(),delimiter='\t'));expected_ids=[r['id'] for r in expected]
assert len(expected_ids)==len(set(expected_ids))
valid_sentences=set(re.findall(r'\*\*(S8\.[123]-\d+)\*\*',pathlib.Path('SENTENCES.md').read_text()))
parts={}
for name in ['code','special','groups']:
 with (D/f'part-gaming.{name}.tsv').open() as f:
  reader=csv.DictReader(f,delimiter='\t');assert reader.fieldnames==H
  for r in reader:
   assert r['id'] not in parts,('duplicate part id',r['id'])
   parts[r['id']]=r
assert set(parts)==set(expected_ids)
out=D/'part-gaming.tsv'
existing={}
if out.exists():
 with out.open() as f:
  reader=csv.DictReader(f,delimiter='\t');assert reader.fieldnames==H
  for r in reader:
   assert r['id'] not in existing
   existing[r['id']]=r
with out.open('a') as f:
 w=csv.DictWriter(f,fieldnames=H,delimiter='\t',lineterminator='\n')
 if not f.tell():w.writeheader()
 for id in expected_ids:
  if id not in existing:w.writerow(parts[id]);f.flush()
with out.open() as f:
 reader=csv.DictReader(f,delimiter='\t');assert reader.fieldnames==H
 actual=list(reader)
ids=[r['id'] for r in actual]
assert len(ids)==len(expected_ids)==len(set(ids)) and set(ids)==set(expected_ids)
for r in actual:
 assert set(r)==set(H) and None not in r
 assert r['decision'] in DECISIONS
 assert len(r['what_it_does'].split())<=15 and len(r['reason'].split())<=30
 assert r['sentences'] and set(r['sentences'].split(','))<=valid_sentences
 assert all('\t' not in v and '\n' not in v and '\r' not in v for v in r.values())
 assert r['basis']=='evidence' or r['basis']=='none' or r['basis'].startswith(('raw:','doc:'))
counts=collections.Counter(r['decision'] for r in actual)
notes='''# Gaming classification c1\n\nThis file consolidates the independently partitioned work within c1. The parts are disjoint input rows, not comparisons with another classification. The input contained 16,515 rows; every row was retained exactly once. Rules below are conditional on the supplied inventory facts, with manual checks for scripted rules. Detailed member decisions for grouped rows are in `part-gaming.groups.members.tsv`.\n\n`part-gaming.merge.py` verifies exact header, identical input/output ID sets and counts, unique IDs, the fifteen permitted decisions, sentence IDs, field lengths, and absence of embedded delimiters. The final counts are in `part-gaming.done`. No hypothesis outcome is inferred by this classification.\n'''
for name in ['code','special','groups']:
 notes+='\n\n---\n\n'+(D/f'part-gaming.{name}.notes.md').read_text()
(D/'part-gaming.notes.md').write_text(notes)
with (D/'part-gaming.done').open('w') as f:
 for d in DECISIONS:f.write(f'{d}\t{counts[d]}\n')
print('VERIFIED',len(actual))
for d in DECISIONS:
 if counts[d]:print(d,counts[d])

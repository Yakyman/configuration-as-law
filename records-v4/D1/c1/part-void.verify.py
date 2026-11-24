import csv,collections,pathlib,re
csv.field_size_limit(10000000)
folder=pathlib.Path('D1/c1')
header=['id','decision','sentences','what_it_does','basis','reason']
allowed=['INSTALLED-OWN','INSTALLED-PACKAGE','INSTALLED-DERIVED','PROGRAM-OWN','PROGRAM-DERIVED','SETTING-OWN','SETTING-DEFAULT','RECORD','MATERIAL','RUNTIME','ACTION','GAP-NONE','GAP-TWO','UNKNOWN','MIXED']
def read(path):
 with path.open(newline='') as f:
  reader=csv.DictReader(f,delimiter='\t');assert reader.fieldnames==header,(path,reader.fieldnames)
  return list(reader)
out=folder/'part-void.tsv'; current=read(out); ids={r['id'] for r in current}
with out.open('a',newline='') as f:
 w=csv.DictWriter(f,fieldnames=header,delimiter='\t',lineterminator='\n')
 for part in ['a','b']:
  for row in read(folder/f'part-void.{part}.tsv'):
   if row['id'] in ids:
    assert [r for r in current if r['id']==row['id']]==[row]
    continue
   w.writerow(row);f.flush();ids.add(row['id']);current.append(row)
source=list(csv.DictReader(open('D1/in/part-void.tsv'),delimiter='\t'))
current=read(out); expected=[r['id'] for r in source]; actual=[r['id'] for r in current]
assert len(actual)==len(expected)==len(set(expected))==len(set(actual))
assert set(actual)==set(expected)
valid_sentences=set(re.findall(r'\*\*(S8\.[123]-\d+)\*\*',pathlib.Path('SENTENCES.md').read_text()))
for row in current:
 assert set(row)==set(header) and all(row[k] is not None for k in header),row
 assert row['decision'] in allowed,row
 assert 0<len(row['what_it_does'].split())<=15,row
 assert 0<len(row['reason'].split())<=30,row
 assert all(s in valid_sentences for s in row['sentences'].split(',')),row
 assert all('\t' not in v and '\n' not in v and '\r' not in v for v in row.values()),row
 assert row['basis'] in ['evidence','none'] or row['basis'].startswith(('raw:','doc:')),row
 if row['basis'].startswith('raw:'):
  assert pathlib.Path(row['basis'][4:]).exists(),row
counts=collections.Counter(r['decision'] for r in current)
(folder/'part-void.done').write_text(''.join(f'{d}\t{counts[d]}\n' for d in allowed))
print('Verified',len(current),'rows, each ID exactly once, 15-value vocabulary, sentence IDs, field limits, raw basis paths.')
print((folder/'part-void.done').read_text())

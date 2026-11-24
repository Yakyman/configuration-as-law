import csv,collections,re,pathlib
csv.field_size_limit(10000000)
root=pathlib.Path('D1/c1')
fields=['id','decision','sentences','what_it_does','basis','reason']
allowed='INSTALLED-OWN INSTALLED-PACKAGE INSTALLED-DERIVED PROGRAM-OWN PROGRAM-DERIVED SETTING-OWN SETTING-DEFAULT RECORD MATERIAL RUNTIME ACTION GAP-NONE GAP-TWO UNKNOWN MIXED'.split()
with open('D1/in/part-microos.tsv',encoding='utf-8',newline='') as f:source=list(csv.DictReader(f,delimiter='\t'))
with open(root/'part-microos.tsv',encoding='utf-8',newline='') as f:
 reader=csv.DictReader(f,delimiter='\t');assert reader.fieldnames==fields;out=list(reader)
expected=collections.Counter(x['id'] for x in source);actual=collections.Counter(x['id'] for x in out)
assert actual==expected
assert len(out)==len(source)==len(actual)
assert all(count==1 for count in actual.values())
sentences=set(re.findall(r'\*\*(S8\.[123]-\d+)\*\*',pathlib.Path('SENTENCES.md').read_text()))
for x in out:
 assert set(x)==set(fields)
 assert x['decision'] in allowed
 assert len(x['what_it_does'].split())<=15,(x['id'],'what_it_does')
 assert len(x['reason'].split())<=30,(x['id'],'reason')
 assert all(s in sentences for s in x['sentences'].split(',')),x['id']
 assert all(not any(c in value for c in '\t\r\n') for value in x.values())
 assert x['basis'] in ['evidence','none'] or x['basis'].startswith(('raw:','doc:'))
counts=collections.Counter(x['decision'] for x in out)
with open(root/'part-microos.done','w',encoding='utf-8') as f:
 f.write('decision\tcount\n')
 for decision in allowed:f.write(f'{decision}\t{counts[decision]}\n')
print(f'Validated {len(out)} rows: equal ID sets/counts, unique IDs, fifteen-word vocabulary, field limits and sentence IDs.')
for decision in allowed:
 if counts[decision]:print(f'{decision}: {counts[decision]}')

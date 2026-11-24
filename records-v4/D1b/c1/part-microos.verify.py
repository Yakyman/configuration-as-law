import csv,collections,re
from pathlib import Path
root=Path('D1b/c1')
valid='INSTALLED-OWN INSTALLED-PACKAGE INSTALLED-DERIVED PROGRAM-OWN PROGRAM-DERIVED SETTING-OWN SETTING-DEFAULT RECORD MATERIAL RUNTIME ACTION GAP-NONE GAP-TWO UNKNOWN MIXED'.split()
def read(p):
 with open(p,newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
a=read('D1b/in/part-microos.tsv');b=read(root/'part-microos.tsv')
assert list(b[0])==['id','decision','sentences','what_it_does','basis','reason']
assert len(a)==len(b)==len({r['id'] for r in b})
assert collections.Counter(r['id'] for r in a)==collections.Counter(r['id'] for r in b)
sentences=set(re.findall(r'\*\*(S8\.[123]-\d+)\*\*',Path('SENTENCES.md').read_text()))
for r in b:
 assert r['decision'] in valid,r
 assert len(r['what_it_does'].split())<=15,r
 assert len(r['reason'].split())<=30,r
 assert set(r['sentences'].split(','))<=sentences,r
 assert all(v is not None and '\t' not in v and '\n' not in v and '\r' not in v for v in r.values()),r
c=collections.Counter(r['decision'] for r in b)
(root/'part-microos.done').write_text(''.join(f'{d}\t{c[d]}\n' for d in valid),encoding='utf-8')
print(dict(c));print('Verified',len(b),'unique rows')

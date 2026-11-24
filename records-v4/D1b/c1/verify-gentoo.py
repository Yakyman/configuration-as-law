import csv,collections,pathlib,re,hashlib
base=pathlib.Path('D1b/c1')
def read(p):
 with open(p,newline='',encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
header=['id','decision','sentences','what_it_does','basis','reason']
allowed=['INSTALLED-OWN','INSTALLED-PACKAGE','INSTALLED-DERIVED','PROGRAM-OWN','PROGRAM-DERIVED','SETTING-OWN','SETTING-DEFAULT','RECORD','MATERIAL','RUNTIME','ACTION','GAP-NONE','GAP-TWO','UNKNOWN','MIXED']
source=read('D1b/in/part-gentoo.tsv');out=read(base/'part-gentoo.tsv')
with open(base/'part-gentoo.tsv',newline='') as f:assert next(csv.reader(f,delimiter='\t'))==header
assert len(source)==len(out)==32775
assert collections.Counter(r['id'] for r in source)==collections.Counter(r['id'] for r in out)
assert all(n==1 for n in collections.Counter(r['id'] for r in out).values())
sids=set(re.findall(r'\*\*(S8\.[123]-\d+)\*\*',pathlib.Path('SENTENCES.md').read_text()))
for r in out:
 assert list(r)==header and all(r.values())
 assert r['decision'] in allowed
 assert len(r['what_it_does'].split())<=15
 assert len(r['reason'].split())<=30
 assert all(s in sids for s in r['sentences'].split(','))
 assert r['basis'] in {'evidence','none'} or r['basis'].startswith(('raw:','doc:'))
 assert all(not any(c in v for c in '\t\r\n') for v in r.values())
counts=collections.Counter(r['decision'] for r in out)
digest=hashlib.sha256((base/'part-gentoo.tsv').read_bytes()).hexdigest()
with (base/'part-gentoo.done').open('w') as f:
 for d in allowed:f.write(f'{d}\t{counts[d]}\n')
print('VERIFIED',len(out),'unique exact-input IDs; valid fields and sentence references.')
print('SHA256',digest)
print('\n'.join(f'{d}\t{counts[d]}' for d in allowed))

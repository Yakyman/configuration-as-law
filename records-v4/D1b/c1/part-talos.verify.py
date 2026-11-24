import csv,collections,pathlib,re,hashlib
p=pathlib.Path('D1b/c1')
allowed='INSTALLED-OWN INSTALLED-PACKAGE INSTALLED-DERIVED PROGRAM-OWN PROGRAM-DERIVED SETTING-OWN SETTING-DEFAULT RECORD MATERIAL RUNTIME ACTION GAP-NONE GAP-TWO UNKNOWN MIXED'.split()
def read(path):
 with open(path,encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
a=read('D1b/in/part-talos.tsv');b=read(p/'part-talos.tsv')
assert (p/'part-talos.tsv').read_text().splitlines()[0]=='id\tdecision\tsentences\twhat_it_does\tbasis\treason'
x=collections.Counter(r['id'] for r in a);y=collections.Counter(r['id'] for r in b)
assert x==y and len(a)==len(b)==len(x)==len(y)==43
assert all(n==1 for n in y.values())
sids=set(re.findall(r'\*\*(S8\.[123]-\d+)\*\*',pathlib.Path('SENTENCES.md').read_text()))
for r in b:
 assert len(r)==6 and None not in r
 assert r['decision'] in allowed
 assert set(r['sentences'].split(','))<=sids
 assert len(r['what_it_does'].split())<=15
 assert len(r['reason'].split())<=30
 assert r['basis'] in ('evidence','none') or r['basis'].startswith(('raw:','doc:'))
 assert all('\t' not in v and '\n' not in v and '\r' not in v for v in r.values())
 if r['basis'].startswith('raw:'):assert pathlib.Path(r['basis'][4:]).is_file()
counts=collections.Counter(r['decision'] for r in b)
with (p/'part-talos.done').open('w') as f:
 for key in allowed:f.write(f'{key}\t{counts[key]}\n')
print('Verified: 43 input IDs, 43 output IDs, each once; valid decisions, sentence IDs, fields and local evidence references.')
print(dict(counts))
print('Frozen table SHA256:',hashlib.sha256((p/'part-talos.tsv').read_bytes()).hexdigest())

import csv,json
from pathlib import Path
rows=[r for r in csv.DictReader(open('D1/in/part-mint.tsv'),delimiter='\t') if r['kind']=='L1:package:dpkg-query'][:635]
s=json.load(open('D1/c1/part-mint.1.sources.json'))
p=Path('D1/c1/part-mint.1.tsv');header=['id','decision','sentences','what_it_does','basis','reason']
existing={r['id'] for r in csv.DictReader(p.open(),delimiter='\t')} if p.exists() else set()
skip={5,6,7,8,10,13,19,21,22,24,25,32,33,35,41,44,49,55,57,61,62,69,71,72,73,74,75,78,80,83,87,98,102,107,115,121,122,123,132,141,147,148,150,162,164,167,176,178,179,180,181,183,185,198,201,214,216,224,225,299,300,303,305,308,318,319,322,324,327,328,339,343,362,369,371,374,376,377,378,379,380,383,389,392,395,412,413,414,419,425,426,427,428,429,430,440,449,465,469,507,513,514,531,546,547,549,550,557,561,571,577,582,583,598,605,613}
skip.update(range(186,198));skip.update(range(229,299))
with p.open('a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not existing:w.writerow(header)
 for i,r in enumerate(rows):
  if i in skip or r['id'] in existing:continue
  n=r['name'].split(':')[1];d=s.get(n)
  if not d:continue
  what=' '.join(d['description'].split()[:15])
  # Explicitly selected runtime libraries and executable programs, not a name-prefix classification.
  lib=i>=433 or i in [39,81,127,146,302,312,323,344,345,346,347,348,349,350,352,354,356,357,360,361,365,368,381,384,385,386,390,402]
  ids='S2.2-10,S2.2-13' if lib else 'S2.2-9'
  reason='Executable library or module supplies functionality under the calling program’s rights; it is code, not values.' if lib else 'This package supplies a runnable program; installation method does not exempt programs from recording.'
  w.writerow([r['id'],'MUST',ids,what,'doc:'+d['url'],reason]);f.flush()
print('Rows appended; total',sum(1 for _ in p.open())-1)

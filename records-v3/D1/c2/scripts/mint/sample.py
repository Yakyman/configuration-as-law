import json, random, csv, gzip, re
from collections import defaultdict
random.seed(20261122)
ids = json.load(open('work/mint/rule-ids.json'))
out = {r['id']: r for r in csv.DictReader(open('part-mint.tsv'), delimiter='\t')}
inp = {r['id']: r for r in csv.DictReader(open('../in/part-mint.tsv'), delimiter='\t')}
files = defaultdict(list)
for l in gzip.open('raw/mint/pkgfiles.tsv.gz', 'rt'):
    n, p = l.rstrip('\n').split('\t', 1); files[n].append(p)
sel = {}
for k, v in ids.items():
    sel[k] = random.sample(v, 10)
    print('==', k)
    for i in sel[k]:
        name = inp[i]['name']; print(i, name, '|', out[i]['decision'], '|', out[i]['what_it_does'], '|', inp[i]['members'][:70])
        if ':' in name:
            pkg = name.split(':')[1]
            fs = [p for p in files[pkg] if not p.startswith('usr/share/doc')]
            print('    files:', len(fs), ' '.join(fs[:6])[:260])
json.dump(sel, open('work/mint/handcheck-ids.json', 'w'), indent=0)

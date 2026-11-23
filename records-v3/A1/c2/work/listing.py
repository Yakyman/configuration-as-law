import csv,json
R='raw/coreos/'
pk=set(l.rstrip('\n') for l in open(R+'package-files.txt'))
files=[l.rstrip('\n').split('\t') for l in open(R+'files.tsv')]
rows=[r for r in csv.reader(open('part-1.tsv'),delimiter='\t')][1:]
own=[r for r in rows if r[3]=='package-owned-paths']
names=[r[4] for r in own]
groups={n:[] for n in names}
for f in files:
    p=f[1]
    if p not in pk: continue
    best=None
    for n in names:
        if p==n or p.startswith(n.rstrip('/')+'/'):
            if best is None or len(n)>len(best): best=n
    if best: groups[best].append(f)
ug=json.load(open(R+'unowned-groups.json'))
for r in rows:
    if r[3]=='package-owned-paths':
        m=groups[r[4]]
        print(f"## {r[0]} OWNED {r[4]} n={len(m)}")
        for f in m[:30]: print('   ',f[0],f[1],('->'+f[2]) if f[2] else '',f[3])
        if len(m)>30: print('    ...',len(m)-30,'more')
    elif r[3]=='stored':
        m=ug.get(r[4],[])
        print(f"## {r[0]} STORED {r[4]} n={len(m)}")
        for f in m[:30]: print('   ',f['type'],f['path'],('->'+f['target']) if f['target'] else '',f['size'])
        if len(m)>30: print('    ...',len(m)-30,'more')

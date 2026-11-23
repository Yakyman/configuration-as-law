import sys,csv
R='raw/coreos/'
pk=set(l.rstrip('\n') for l in open(R+'package-files.txt'))
files=[l.rstrip('\n').split('\t') for l in open(R+'files.tsv')]
names=[r[4] for r in csv.reader(open('part-1.tsv'),delimiter='\t') if len(r)>3 and r[3]=='package-owned-paths']
nameset=set(names)
groups={n:[] for n in names}
for f in files:
    p=f[1]
    if p not in pk: continue
    # most specific group that is prefix
    best=None
    for n in names:
        if p==n or p.startswith(n.rstrip('/')+'/'):
            if best is None or len(n)>len(best): best=n
    if best: groups[best].append((f[0],p,f[2] if len(f)>2 else ''))
for n in names:
    print(n,len(groups[n]))
    for g in groups[n][:int(sys.argv[1])]: print('   ',*g)

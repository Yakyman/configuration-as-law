import sys,csv
R='in/raw/debian/'
pk=set(l.rstrip('\n') for l in open(R+'package-files.txt'))
files=[l.rstrip('\n').split('\t') for l in open(R+'files.tsv')]
rows=[r for r in csv.reader(open('in/part-2.tsv'),delimiter='\t') if r[3]=='package-owned-paths']
names=[r[4] for r in rows]
for r in rows:
    g=r[4]; n=int(r[5])
    mem=[f for f in files if (f[1]==g or f[1].startswith(g+'/')) and f[1] in pk]
    # exclude members belonging to deeper groups
    deeper=[x for x in names if x!=g and x.startswith(g+'/')]
    mem=[f for f in mem if not any(f[1]==d or f[1].startswith(d+'/') for d in deeper)]
    flag='' if len(mem)==n else ' MISMATCH(%d)'%len(mem)
    print('##',r[0],g,n,flag)
    for f in mem: print('   ',f[0],f[1],('-> '+f[2]) if f[2] else '')

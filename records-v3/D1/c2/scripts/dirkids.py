import sys
fs=open(sys.argv[1],'rb').read().split(b'\0')
paths=[fs[i].decode('utf-8','replace') for i in range(0,len(fs)-5,6)]
pset=set(paths)
kids={}
for p in paths:
    par=p.rsplit('/',1)[0] or '/'
    kids[par]=kids.get(par,0)+1
for line in open(sys.argv[2]):
    a=line.rstrip('\n').split('\t')
    if a[2]=='d': print(a[1], kids.get(a[1],0))

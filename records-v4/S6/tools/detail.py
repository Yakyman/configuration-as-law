import json,sys
d={x['path']:x for x in json.load(open(sys.argv[1]))['all_differences']}
c=d.get('/evidence/commands')
if c:
    L,R=c['left'],c['right']; print('commands', len(L), len(R))
    for i,(a,b) in enumerate(zip(L,R)):
        if a!=b:
            print(' index',i,'argv',a.get('argv'))
            for k in set(a)|set(b):
                if a.get(k)!=b.get(k): print('   ',k,'L:',json.dumps(a.get(k))[:400]); print('   ',k,'R:',json.dumps(b.get(k))[:400])
k=d.get('/rows/code-boundary/observed/kernel_profiles')
if k:
    l=k['left'].splitlines(); r=k['right'].splitlines()
    print('kernel_profiles lines',len(l),len(r),'same multiset:',sorted(l)==sorted(r))
for p,x in d.items():
    if p not in ('/evidence/commands','/rows/code-boundary/observed/kernel_profiles'):
        print(p)

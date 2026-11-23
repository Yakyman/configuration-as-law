import sys, os, gzip, lzma
wd=sys.argv[1]; want=set(sys.argv[2:]); found={}
for fn in sorted(os.listdir(wd)):
    op = lzma.open if fn.endswith('.xz') else gzip.open if fn.endswith('Packages.gz') else None
    if not op or 'Packages' not in fn: continue
    for rec in op(os.path.join(wd,fn),'rt',errors='replace').read().split('\n\n'):
        d={}
        for l in rec.split('\n'):
            if ':' in l and not l.startswith(' '): k,v=l.split(':',1); d[k]=v.strip()
        n=d.get('Package')
        if n in want: found[n]=(d.get('Depends','-'), d.get('Recommends','-'))
for n in sorted(want): print(n, '| D:', found.get(n,('?','?'))[0][:150], '| R:', found.get(n,('?','?'))[1][:80])

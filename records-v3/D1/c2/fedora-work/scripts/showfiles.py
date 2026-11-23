import json,gzip,sys
want=set(l.split('\t')[0] for l in open(sys.argv[2]) if l.split('\t')[1]!='CODE')
n=int(sys.argv[3]) if len(sys.argv)>3 else 6
for l in gzip.open(sys.argv[1],'rt'):
    d=json.loads(l)
    if d['name'] not in want: continue
    fs=[p for p,t in d.get('files',[]) if t!='d']
    fs=[p for p in fs if not p.startswith(('/usr/share/licenses/','/usr/share/doc/'))] or fs
    print(d['name'],'::',' '.join(fs[:n]), ('...+%d'%(len(fs)-n) if len(fs)>n else ''))

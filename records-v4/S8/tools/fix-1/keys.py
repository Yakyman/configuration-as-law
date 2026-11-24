import json, sys, os
base = sys.argv[1]
for p in ['h1-after-restart-1','h1-after-restart-2','h1-end','h2-end','h3-end','h4-install-disconnected']:
    d=json.load(open(os.path.join(base,p+'.summary.json')))
    print('==',p)
    for k,v in d.items():
        if isinstance(v,(int,float,str,bool)) or v is None: print('  ',k,v)
        elif isinstance(v,dict):
            print('  ',k,'dict:',{kk:(vv if isinstance(vv,(int,float,str,bool)) else type(vv).__name__+str(len(vv) if hasattr(vv,'__len__') else '')) for kk,vv in list(v.items())[:25]})
        elif isinstance(v,list): print('  ',k,'list len',len(v))

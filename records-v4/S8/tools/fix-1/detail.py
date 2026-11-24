import json, sys, os
base = sys.argv[1]
for p in ['h1-after-restart-1','h1-after-restart-2','h1-end','h2-end','h3-end','h4-install-disconnected']:
    d=json.load(open(os.path.join(base,p+'.summary.json')))
    print('==',p)
    for k in sys.argv[2:]:
        print(' --',k, json.dumps(d.get(k), indent=None)[:3000])

import json,sys
d={x['path']:x for x in json.load(open(sys.argv[1]))['all_differences']}
for p,x in d.items():
    if p.endswith('success_report') or p=='/evidence/last_success':
        L=json.loads(x['left']); R=json.loads(x['right'])
        print(p,'differing keys:',sorted(k for k in set(L)|set(R) if L.get(k)!=R.get(k)))
s=json.load(open(sys.argv[2]))
for k,v in s['rows'].items():
    if 'bc4' in k: print(k, json.dumps(v['observed'])[:300])

import json,collections,sys
d=json.load(open(sys.argv[1]))['files']
rows=[json.loads(l) for l in d['/var/lib/stand/current/machine.jsonl'].splitlines() if l.strip()]
print('machine rows',len(rows), collections.Counter(r['type'] for r in rows))
bf=json.loads(d['/var/lib/stand/current/base-files.json']); print('base-files', type(bf).__name__, len(bf)); print(bf[0] if isinstance(bf,list) else list(bf)[:3])
fs=[k for k in d if k.startswith('/var/lib/stand-fs/')]
for k in fs:
    x=json.loads(d[k]); print(k, {a:(len(b) if isinstance(b,(list,dict)) else b) for a,b in x.items()})
x=json.loads(d[[k for k in fs if '/home/' in k][0]]); print(json.dumps(x)[:1200])
print([d[k] for k in d if k.endswith('bc3-primary.json')][0])

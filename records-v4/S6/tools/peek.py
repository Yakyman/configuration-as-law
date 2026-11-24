import json,sys,collections
d=json.load(open(sys.argv[1])); print(list(d.keys())); print(list(d['files'].keys()))
fsname=[k for k in d['files'] if 'stand-fs' in k and k.endswith('declaration.json')]
fs=json.loads(d['files'][fsname[0]]); print(fsname[0], list(fs.keys()))
k=list(fs['paths'].items())[:2]; print(k); print([fs['objects'][v] for _,v in k])
print(len(fs['paths']), json.dumps(fs.get('account_rows',[])[:1])[:600])
r=[json.loads(l) for l in d['files']['/var/lib/stand/current/machine.jsonl'].splitlines() if l.strip()]
print(collections.Counter(tuple(sorted(x.get('package_identity',{}).keys())) for x in r if x['type']=='program'))
print([x.get('package_identity') for x in r if x['type']=='program'][:2])
for x in r:
    if x.get('managed'): print(x['id'], sorted(x.keys()))

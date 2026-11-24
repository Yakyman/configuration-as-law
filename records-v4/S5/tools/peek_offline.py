import json, sys
d = json.load(open(sys.argv[1]))
files = d['files']
for k in files: print(k, len(files[k]))
desig = [k for k in files if k.endswith('bc3-primary.json')][0]
print(files[desig])
h = json.loads(files['/var/lib/stand-fs/home/current/declaration.json'])
print(list(h)); print(json.dumps(h['paths'])[:600]); print(json.dumps(list(h['objects'].items())[:3])[:800])

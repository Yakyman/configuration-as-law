import json
g=json.load(open('in/raw/coreos/directory-only-groups.json'))
for k,v in g.items(): print(k, len(v), [x['path'] for x in v][:8])

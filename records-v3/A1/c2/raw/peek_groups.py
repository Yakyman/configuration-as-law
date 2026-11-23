import json, sys, collections
raw = sys.argv[1]
d = json.load(open(raw + '/unowned-groups.json'))
for g in sys.argv[2:]:
    m = d.get(g, [])
    if len(m) > 40:
        print(g, len(m), collections.Counter('/'.join(x['path'].split('/')[:4]) for x in m).most_common(12))
        continue
    print(g, [(x['type'], x['path'][len(g):], x['target'][-40:]) for x in m])
dd = json.load(open(raw + '/directory-only-groups.json'))
print(len(dd), list(dd))

import json
g = json.load(open('in/raw/debian/unowned-groups.json'))
for k, v in g.items():
    print('##', k, len(v))
    for m in v:
        print('   ', m['type'], m['path'], ('-> ' + m['target']) if m['target'] else '')

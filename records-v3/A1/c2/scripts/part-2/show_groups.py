"""Print members (type path [target] size) of stored groups named on the command line, from the inventory JSON."""
import json, sys
g = json.load(open('in/raw/debian/unowned-groups.json'))
lim = 80
for name in sys.argv[1:]:
    v = g.get(name, [])
    print('##', name, len(v))
    for m in v[:lim]:
        print('  ', m['type'], m['path'], ('-> ' + m['target']) if m['target'] else '', m['size'])

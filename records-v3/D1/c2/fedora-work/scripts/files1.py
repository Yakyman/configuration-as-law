import json,gzip,sys
want=set(sys.argv[2:])
for l in gzip.open(sys.argv[1],'rt'):
    d=json.loads(l)
    if d['name'] in want:
        print('##',d['name'],d.get('matched'),d.get('url'))
        for p,t in d['files']:
            if t!='d' and not p.startswith(('/usr/share/man/','/usr/share/licenses/','/usr/share/locale/')): print('  ',p,t)

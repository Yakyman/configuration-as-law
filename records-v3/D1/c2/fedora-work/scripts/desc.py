import json,gzip,sys,re
want=set(l.split('\t')[0] for l in open(sys.argv[2]) if l.split('\t')[1]!='CODE')
for l in gzip.open(sys.argv[1],'rt'):
    d=json.loads(l)
    if d['name'] in want and re.search(sys.argv[3],(d.get('summary') or '')+' '+(d.get('description') or ''),re.I):
        print(d['name'],'::',re.sub(r'\s+',' ',(d.get('description') or ''))[:260])

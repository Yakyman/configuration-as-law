import json, sys, lzma, re
raw = lzma.open(sys.argv[1]).read().decode()
i = raw.find('"/var/lib/stand/objects.json": "[')
j = raw.find('"]', i)
s = json.loads(raw[i+len('"/var/lib/stand/objects.json": '): raw.find('"', raw.find(']', raw.rfind('}]', i, i+2000000))) +1]) if False else None
# simpler: decode the JSON string literal starting at the value
k = i + len('"/var/lib/stand/objects.json": ')
dec = json.JSONDecoder()
val, end = dec.raw_decode(raw, k)
objs = json.loads(val)
print('ledger objects', len(objs), 'dev-worker in ledger:', 'dev-worker' in val)
print('kinds', sorted(set(o.get('kind') for o in objs)))
print('all dev-worker positions', [m.start() for m in re.finditer('dev-worker', raw)][:30])
for m in re.finditer('dev-worker', raw):
    print('  ', raw[max(0,m.start()-60):m.start()+30].replace('\n',' '))

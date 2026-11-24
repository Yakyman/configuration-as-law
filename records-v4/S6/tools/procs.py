import json,sys
for f in sys.argv[1:]:
    d=json.load(open(f)); print(f, 'file:', json.dumps(d['file'])[:200])
    for h in d['holders']: print('  ', {k:h.get(k) for k in ('pid','starttime','state','exe','argv','scan_error')})

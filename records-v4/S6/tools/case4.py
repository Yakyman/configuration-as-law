import json
for st in ('both','one','none'):
    s=json.load(open(f'raw/case-4/{st}-snapshot.stdout'))
    led=json.loads(s['evidence']['objects_ledger'])
    hits=[(e.get('object'),[o.get('line') for o in e.get('origins',[])]) for e in led if 'bc4-' in json.dumps(e) or 'bc4:' in json.dumps(e)]
    print(st,'ledger entries mentioning bc4:',hits)
    print(st,'rows with bc4:',[k for k in s['rows'] if 'bc4-' in k or 'bc4:' in k], 'machine identical:',s['current_machine_byte_identical'])
    b=s['rows'].get('bc4:owner-b')
    if b: print(st,'owner-b required deps:',b['required'].get('package_dependencies'),'observed deps:',json.dumps(b['observed'].get('dependency_registrations'))[:300])

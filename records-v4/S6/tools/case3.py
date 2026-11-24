import json,sys
a=json.load(open('raw/case-3/after-snapshot.stdout')); b=json.load(open('raw/case-3/before-snapshot.stdout'))
for name,s in (('before',b),('after',a)):
    cb=s['rows']['code-boundary']['observed']
    lt=cb['launch_table'] if isinstance(cb['launch_table'],str) else ''
    print(name,'launch.tsv lines with dev-worker:',[l for l in lt.splitlines() if 'dev-worker' in l][:3])
    print(name,'policy sources mentioning dev-worker:',[k for k,v in cb['policy_sources'].items() if isinstance(v,str) and 'dev-worker' in v])
    print(name,'rows present:',[k for k in ('dev-worker','dev-service','dev-rule') if k in s['rows']])
    print(name,'ledger mentions dev-worker:', isinstance(s['evidence']['objects_ledger'],str) and 'dev-worker' in s['evidence']['objects_ledger'])
    hits=[(k,p) for k,fs in s['filesystems'].items() for p in fs['paths'] if 'stand-development' in p or 'dev-worker' in p]
    print(name,'filesystem declared paths with removed names:',hits[:5])
    print(name,'current_machine_byte_identical',s['current_machine_byte_identical'],'requested',s['requested_machine_sha256'][:12])

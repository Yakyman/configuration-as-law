import json
for n in ('before','after'):
    s=json.load(open(f'raw/case-3/{n}-snapshot.stdout'))
    cb=s['rows']['code-boundary']['observed']
    kp=cb['kernel_profiles'] if isinstance(cb['kernel_profiles'],str) else ''
    print(n,[l for l in kp.splitlines() if '458181eb3efbccd6aaa7' in l or '281b3a23a0238221a716' in l],
          'exported:',[k for k in cb['kernel_exported_policy'] if '458181eb3efbccd6aaa7' in k or '281b3a23a0238221a716' in k])
    rl=s['rows'].get('firewall:input',{}).get('observed',{}).get('effective_text','')
    print(n,'17777 in firewall chain effective text:', '17777' in (rl or ''))

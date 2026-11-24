import json, sys, os
base = sys.argv[1]
SKIP = ('/run/', '/var/lib/stand-fs/', '/var/lib/stand/generations')
pts = ['h1-after-restart-1','h1-after-restart-2','h1-end','h2-end','h3-end','h4-install-disconnected']
R = {}
for p in pts:
    d = json.load(open(os.path.join(base, p+'.summary.json')))
    R[p] = {e['path']: e for e in d['unclaimed_changed_outside_code_root_copies'] if not e['path'].startswith(SKIP)}
    print(p, len(R[p]))
def show(a, b):
    print('\n== in', a, 'not in', b)
    for k in sorted(set(R[a]) - set(R[b])):
        e = R[a][k]
        print(' ', k, e['kind'], 'exec' if e.get('executable_bit') else '', 'dpkg:'+','.join(e['dpkg_member_of']) if e.get('dpkg_member_of') else '', e.get('mtime_utc') or e.get('st_mtime') or '')
for a,b in [('h1-after-restart-1','h2-end'),('h1-after-restart-1','h4-install-disconnected'),('h1-end','h2-end'),('h1-end','h4-install-disconnected'),('h4-install-disconnected','h2-end'),('h4-install-disconnected','h1-after-restart-1'),('h2-end','h4-install-disconnected')]:
    show(a,b)
print('\nsample entry keys:', list(next(iter(R['h1-end'].values())).keys()))

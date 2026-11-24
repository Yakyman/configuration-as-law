import json, sys, os, collections
base = sys.argv[1]
for p in ['h1-after-restart-1','h1-after-restart-2','h1-end','h2-end','h3-end','h4-install-disconnected']:
    d = json.load(open(os.path.join(base, p+'.summary.json')))
    nd = d['unclaimed_unchanged_non_directories']
    cr = sum(1 for x in nd if x[0].startswith('/var/lib/stand/code-root/'))
    dpkg = sum(1 for x in nd if x[2])
    print(p, 'dirs', d['unclaimed_unchanged_by_kind'].get('directory'), 'nondirs', len(nd), 'of which code-root', cr, 'dpkg-member', dpkg, 'boundary-changed', d['unclaimed_changed_since_boundary_count'], 'unclaimed_total', d['unclaimed_total'], 'code_root_copies', d['code_root_copies'])

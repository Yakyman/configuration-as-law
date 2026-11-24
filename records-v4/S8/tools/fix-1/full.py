import json, sys, os, datetime
base = sys.argv[1]
SKIP = ('/run/', '/var/lib/stand-fs/', '/var/lib/stand/generations')
def t(x):
    return datetime.datetime.fromtimestamp(x, datetime.timezone.utc).strftime('%H:%M:%S') if isinstance(x,(int,float)) else x
for p in sys.argv[2:]:
    d = json.load(open(os.path.join(base, p+'.summary.json')))
    print('==', p)
    for e in d['unclaimed_changed_outside_code_root_copies']:
        if e['path'].startswith(SKIP): continue
        dm = e.get('dpkg_member_of') or []
        print(' ', e['path'], e['kind'], oct(e['mode']) if isinstance(e.get('mode'),int) else e.get('mode'), 'mtime', t(e.get('mtime')), 'ctime', t(e.get('ctime')), 'dpkg:%d%s' % (len(dm), '(ed)' if 'ed' in dm else ''), (e.get('sha256') or '')[:12])

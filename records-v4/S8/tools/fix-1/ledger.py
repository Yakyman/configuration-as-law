"""For each changed unclaimed entry of a summary (outside /run and the declaration machinery), report whether the
installer ledger (the objects.json saved in the raw observation) registers that path."""
import json, sys, lzma
summary, rawobs = sys.argv[1], sys.argv[2]
SKIP = ('/run/', '/var/' + 'lib/stand-fs/', '/var/' + 'lib/stand/generations')
LEDGER = '"/var/' + 'lib/stand/objects.json": '
op = lzma.open if rawobs.endswith('.xz') else open
raw = op(rawobs, 'rt').read()
import re
m = re.search(re.escape(LEDGER.rstrip()) + r"\s*\"\[", raw)
i = m.start()
LEDGER = raw[m.start():m.end() - 2]
val, _ = json.JSONDecoder().raw_decode(raw, i + len(LEDGER))
objs = json.loads(val)
reg = {}
for o in objs:
    for p in [o.get('object', ''), (o.get('identity') or {}).get('path', '')]:
        if p:
            reg.setdefault(p.split(':', 1)[-1], o.get('object'))
print('ledger objects', len(objs))
print('sample file object', json.dumps([o for o in objs if o.get('kind') == 'file'][:1])[:400])
s = json.load(open(summary))
for e in s['unclaimed_changed_outside_code_root_copies']:
    p = e['path']
    if p.startswith(SKIP):
        continue
    print(p, 'ledger:' + (reg.get(p) or '-'), 'dpkg:' + str(len(e.get('dpkg_member_of') or [])))

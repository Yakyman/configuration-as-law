"""Compare the commands of B2/CASES-5.md and the fixture manifest with round-1 records."""
import base64, hashlib, json, re, sys
from pathlib import Path
B2 = Path(sys.argv[1])
r1 = B2 / 'raw/round-1/final-2'
logs = {'shell': r1/'shell.jsonl', 'tools': r1/'tools.jsonl',
        'direct': r1/'supplement/direct.jsonl', 'extra': r1/'supplement/extra.jsonl'}
rows = {k: [json.loads(l) for l in open(p)] for k, p in logs.items()}
fx = json.loads((B2/'build/bc3-fixtures.json').read_text())
cases_md = (B2/'CASES-5.md').read_text()
# blocks per case section
sections = re.split(r'\n## (\d\d)\. ', cases_md)
md = {}
for i in range(1, len(sections), 2):
    body = sections[i+1]
    cid = body.split('\n', 1)[0].strip()
    blocks = re.findall(r'```sh\n(.*?)```', body, re.S)
    md[cid] = blocks
out = []
for c in fx['cases']:
    cid = c['id']
    r1cmds = [(k, i, r['command']) for k, rs in rows.items() for i, r in enumerate(rs)
              if r.get('id') == cid and 'command' in r]
    r1fix = [(k, i, r) for k, rs in rows.items() for i, r in enumerate(rs)
             if 'path' in r and 'sha256' in r and r.get('phase', '').startswith('fixture') and r['path'] in c['files']]
    blocks = md.get(cid, [])
    rec = {'id': cid, 'fixture_command': c['command'], 'cwd': c['cwd'],
           'round1': [{'log': k, 'line': i + 1, 'command': cmd, 'equal_to_fixture': cmd == c['command']} for k, i, cmd in r1cmds],
           'cases_md_attempt_equal': len(blocks) >= 1 and blocks[0].rstrip('\n') == c['command'].rstrip('\n'),
           'cases_md_permitted_equal': len(blocks) >= 2 and blocks[1].rstrip('\n') == c['command'].rstrip('\n'),
           'cases_md_attempt_exact_bytes': len(blocks) >= 1 and blocks[0] == c['command'] + '\n',
           'round1_fixtures': [{'log': k, 'line': i + 1, 'path': r['path'], 'sha256': r['sha256'], 'bytes': r['bytes'], 'mode': r.get('mode')} for k, i, r in r1fix]}
    fl = fx['files']
    rec['manifest_files'] = []
    for p in c['files']:
        f = fl[p] if isinstance(fl, dict) else next(x for x in fl if x['path'] == p)
        data = base64.b64decode(f.get('content_b64') or f.get('base64') or f.get('b64'))
        rec['manifest_files'].append({'path': p, 'sha256_declared': f.get('sha256'), 'sha256_of_bytes': hashlib.sha256(data).hexdigest(), 'bytes': len(data), 'mode': f.get('mode')})
    out.append(rec)
acc = fx['account']
r1acc = [(k, i, r['command']) for k, rs in rows.items() for i, r in enumerate(rs) if r.get('id') == acc['id'] and 'command' in r]
out.append({'id': acc['id'], 'fixture_command': acc['command'], 'round1': [{'log': k, 'line': i + 1, 'command': cmd, 'equal_to_fixture': cmd == acc['command']} for k, i, cmd in r1acc],
            'cases_md_block': md.get('root-native-account-bypass')})
print(json.dumps(out, indent=1))

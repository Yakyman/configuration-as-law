"""Read the declarations before and after each step of one second-party case.

Usage: analyse_case.py CASEDIR NN  -> JSON on stdout.
Verifies every referenced snapshot digest, diffs the primary machine declaration
and the five filesystem declarations, checks success-report consistency and the
coverage of the case's saved sources, and lists the audit events.
"""
import hashlib, json, sys
from pathlib import Path
base = Path(sys.argv[1]); nn = sys.argv[2]
rows = [json.loads(l) for l in open(base / f'{nn}.jsonl')]
snapdir = base / f'{nn}-evidence' / 'bc3-evidence' / 'snapshots'
MOUNTS = {'home': '/home/stand', 'tmp': '/tmp', 'vartmp': '/var/tmp', 'shm': '/dev/shm', 'etc': '/etc'}
problems = []
def load(ref):
    p = snapdir / Path(ref['snapshot_path']).name
    if not p.exists():
        problems.append('missing snapshot ' + p.name); return None
    b = p.read_bytes(); h = hashlib.sha256(b).hexdigest()
    if h != ref['snapshot_sha256']:
        problems.append('snapshot digest mismatch ' + p.name)
    snap = json.loads(b)
    # recompute the declaration digest from the parsed declaration as encoded by the service
    for key, fs in snap['filesystem'].items():
        enc = (json.dumps(fs['declaration'], sort_keys=True, separators=(',', ':')) + '\n').encode()
        if hashlib.sha256(enc).hexdigest() != fs['sha256']:
            problems.append(f'{key}: declaration bytes digest != recorded sha256 ({p.name})')
        s = fs['success']
        if s.get('declaration_sha256') != fs['sha256'] or s.get('generation') != fs['declaration'].get('generation') or s.get('status') != 'success':
            problems.append(f'{key}: success report does not match declaration ({p.name})')
    return dict(file=str(p.relative_to(base.parent.parent.parent)) if False else p.name, sha=h, snap=snap)
def fs_diff(a, b):
    out = {}
    for key in sorted(set(a['filesystem']) | set(b['filesystem'])):
        da = a['filesystem'].get(key, {}).get('declaration', {'paths': {}, 'objects': {}})
        db = b['filesystem'].get(key, {}).get('declaration', {'paths': {}, 'objects': {}})
        added, removed, changed = [], [], []
        for path in sorted(set(da['paths']) | set(db['paths'])):
            ia, ib = da['paths'].get(path), db['paths'].get(path)
            oa = da['objects'].get(ia) if ia else None; ob = db['objects'].get(ib) if ib else None
            full = MOUNTS[key] + ('' if path == '/' else path)
            if ia is None: added.append(dict(path=full, inode=ib, sha256=ob.get('sha256'), mode=oct(ob['st_mode']), uid=ob['st_uid'], size=ob['st_size']))
            elif ib is None: removed.append(dict(path=full))
            elif ia != ib or {k: v for k, v in oa.items() if k not in ('st_atime', 'st_mtime', 'st_ctime')} != {k: v for k, v in ob.items() if k not in ('st_atime', 'st_mtime', 'st_ctime')}:
                changed.append(dict(path=full, inode=ib, sha256_before=oa.get('sha256'), sha256_after=ob.get('sha256'), mode=oct(ob['st_mode'])))
        # objects reachable only through open handles (not via paths)
        unlinked = sorted(set(db['objects']) - set(db['paths'].values()))
        if added or removed or changed or da.get('generation') != db.get('generation') or unlinked:
            out[key] = dict(generation=[da.get('generation'), db.get('generation')], added=added, removed=removed, changed=changed, unlinked_objects_after=unlinked)
    pa, pb = a['primary'], b['primary']
    ra = {json.dumps(r, sort_keys=True) for r in pa['rows']}; rb = {json.dumps(r, sort_keys=True) for r in pb['rows']}
    out['primary'] = dict(sha256=[pa['sha256'], pb['sha256']], unchanged=pa['sha256'] == pb['sha256'],
                          rows_added=[json.loads(x).get('id') for x in rb - ra], rows_removed=[json.loads(x).get('id') for x in ra - rb],
                          report=[pa['report'], pb['report']])
    return out
def coverage(snap, path, sha):
    for key, m in MOUNTS.items():
        if path.startswith(m + '/') and key in snap['filesystem']:
            d = snap['filesystem'][key]['declaration']; rel = path[len(m):]
            ino = d['paths'].get(rel)
            if ino is None: return dict(declaration=key, covered=False, reason='no path row')
            o = d['objects'][ino]
            return dict(declaration=key, generation=d['generation'], inode=ino, sha256=o.get('sha256'), mode=oct(o['st_mode']), uid=o['st_uid'], covered=o.get('sha256') == sha)
    return dict(covered=False, reason='outside mediated roots')
def audit_summary(a):
    out = []
    for key, events in (a or {}).items():
        for e in events:
            out.append(dict(fs=key, generation=e.get('generation'), operation=e.get('operation'), status=e.get('status'),
                            changes=[(MOUNTS[key] + c['path'] if c['path'] != '/' else MOUNTS[key], (c.get('sha256') or '')[:12], c.get('present')) for c in e.get('changes', [])]))
    return out
result = dict(case=nn, steps=[], problems=problems)
fixtures = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else None
files = {f['path']: f for f in fixtures['files']} if fixtures else {}
pending = None
for r in rows:
    if r.get('phase') == 'expected':
        pending = r
    elif r.get('phase') in ('attempt_result', 'case_result') and pending is not None:
        a = load(pending['before']); b = load(r['after'])
        step = dict(role=pending.get('role', r['id']), command=pending['command'], rc=r.get('rc'), stdout=r.get('stdout'), stderr=r.get('stderr'),
                    before_snapshot=a and a['file'], after_snapshot=b and b['file'],
                    controller_flags={k: r.get(k) for k in ('marker_observed', 'refused', 'recorded', 'inline_write_verified', 'passed', 'permitted', 'attempt_closed')},
                    diff=fs_diff(a['snap'], b['snap']) if a and b else None, audit=audit_summary(r.get('audit')))
        case_files = [c for c in fixtures['cases'] if c['id'] == r['id']] if fixtures else []
        if case_files:
            step['coverage_before'] = {p: coverage(a['snap'], p, files[p]['sha256']) for p in case_files[0]['files']}
            step['coverage_after'] = {p: coverage(b['snap'], p, files[p]['sha256']) for p in case_files[0]['files']}
        if r['id'] == 'root-native-account-bypass':
            etc = b['snap']['filesystem']['etc']['declaration']
            step['account_rows'] = [x for x in etc.get('account_rows', []) if 'v4raw' in json.dumps(x)]
            step['account'] = r.get('account')
            step['etc_parse_error'] = etc.get('account_parse_error')
        result['steps'].append(step); pending = None
    elif r.get('phase') in ('fixture_result', 'dispatcher_install', 'case_error', 'summary'):
        result['steps'].append({k: r.get(k) for k in ('phase', 'path', 'passed', 'rc', 'stdout', 'stderr', 'error', 'results')})
print(json.dumps(result, indent=1))

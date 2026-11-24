"""Offline reading of saved snapshot/diff outputs. Compares each required value with its native observation and
classifies saved pair differences. Decides no outcome. usage:
  judge.py fulfil SNAPSHOT.json BUNDLE.json        -> mismatches between every line's required values and observations
  judge.py pair DIFF.json                           -> pair differences grouped by where they lie
"""
import json, sys, collections

FILE_KEYS = ('kind', 'mode', 'uid', 'gid', 'sha256', 'target')


def file_mismatch(req, obs):
    if 'error' in obs:
        return {'path': req.get('path'), 'observed_error': obs.get('error')}
    d = {k: {'required': req[k], 'observed': obs.get(k)} for k in FILE_KEYS if k in req and obs.get(k) != req[k]}
    return {'path': req.get('path'), **d} if d else None


def fulfil(snap, bundle):
    files = bundle['files']
    out = []
    def bad(line, what, **kw):
        out.append({'line': line, 'what': what, **kw})
    if not snap.get('current_machine_byte_identical'):
        bad('*', 'machine.jsonl not byte-identical to requested')
    for name, pf in snap['primary_files'].items():
        if not pf.get('byte_identical'):
            bad('*', 'primary file not byte-identical', file=name)
    for lid, r in snap['rows'].items():
        req, obs = r['required'], r['observed']
        t = req['type']
        if isinstance(obs, dict) and 'QUERY_ERROR' in obs:
            bad(lid, 'query error', detail=obs); continue
        if t in ('program', 'base', 'code'):
            reqfiles = req.get('files', [])
            if 'files_manifest' in req:
                reqfiles = json.loads(files['/var/lib/stand/current/' + req['files_manifest']])
            if len(reqfiles) != len(obs['files']):
                bad(lid, 'file count differs', required=len(reqfiles), observed=len(obs['files']))
            for f, o in zip(reqfiles, obs['files']):
                m = file_mismatch(f, o)
                if m: bad(lid, 'file', detail=m)
            pi = req.get('package_identity')
            if pi and pi.get('backend') == 'dpkg':
                # dpkg prints ${Package} without a multi-arch qualifier; strip it only when it equals the stated arch
                name = pi['name'].removesuffix(':' + pi['architecture'])
                want = f"{name}\t{pi['version']}\t{pi['architecture']}\tinstalled\n"
                if obs.get('package_registration', {}).get('stdout') != want:
                    bad(lid, 'dpkg identity', required=want, observed=obs.get('package_registration'))
            elif pi:
                regs = obs.get('package_registration')
                if not (isinstance(regs, list) and any(e.get('identity', {}).get('version') == pi.get('version') for e in regs)):
                    bad(lid, 'stand registration', required=pi, observed=regs)
            for dep in req.get('package_dependencies', []):
                regs = obs.get('dependency_registrations', {}).get(dep['name'])
                if not (isinstance(regs, list) and any(e.get('identity', {}).get('version') == dep.get('version') for e in regs)):
                    bad(lid, 'dependency registration', required=dep, observed=regs)
        elif t == 'account':
            for k in ('name', 'uid', 'gid', 'shell', 'home', 'gecos'):
                if obs.get(k) != req.get(k): bad(lid, 'account ' + k, required=req.get(k), observed=obs.get(k))
            if sorted(obs.get('groups') or []) != sorted(req.get('groups') or []):
                bad(lid, 'account groups', required=req.get('groups'), observed=obs.get('groups'))
        elif t == 'group':
            for k in ('gid',):
                if obs.get(k) != req.get(k): bad(lid, 'group ' + k, required=req.get(k), observed=obs.get(k))
            if sorted(obs.get('members') or []) != sorted(req.get('members') or []):
                bad(lid, 'group members', required=req.get('members'), observed=obs.get('members'))
        elif t in ('service', 'timer', 'socket'):
            if obs.get('enabled') != req.get('enabled'): bad(lid, 'enabled', required=req.get('enabled'), observed=obs.get('enabled'))
            uf = obs.get('unit_file') or {}
            if 'unit_sha256' in req and uf.get('sha256') != req['unit_sha256']:
                bad(lid, 'unit checksum', required=req['unit_sha256'], observed=uf.get('sha256') or uf)
            if 'unit_text' in req and obs.get('unit_text') != req['unit_text']: bad(lid, 'unit text')
            if 'active' in req and obs.get('active') != req['active']: bad(lid, 'active', required=req['active'], observed=obs.get('active'))
        elif t in ('privilege', 'login-key'):
            m = file_mismatch({k: req[k] for k in ('path', 'mode', 'uid', 'gid') if k in req}, obs['file'])
            if m: bad(lid, 'file', detail=m)
            if obs.get('text') != req.get('text'): bad(lid, 'text')
        elif t == 'password-login':
            want = 'no' if req.get('allowed') is False else 'yes'
            for k, v in obs.items():
                if v != want: bad(lid, k, required=want, observed=v)
        elif t == 'port':
            if obs.get('listening') != req.get('listening'): bad(lid, 'listening', required=req.get('listening'), observed=obs)
        elif t == 'rule':
            b = req.get('backend', 'nft')
            if b == 'mount':
                eff = set((obs.get('effective') or '').split(','))
                miss = [o for o in req['required_options'] if o not in eff]
                if miss or obs.get('query_exit') != 0: bad(lid, 'mount options', missing=miss, observed=obs)
            elif b == 'dac':
                for f, o in zip(req['paths'], obs['paths']):
                    m = file_mismatch(f, o)
                    if m: bad(lid, 'path', detail=m)
            elif b == 'nft-chain':
                ch = obs.get('chain') or []
                if len(ch) != 1 or any(ch[0].get(k) != v for k, v in req['chain'].items()):
                    bad(lid, 'chain', required=req['chain'], observed=ch)
            elif b == 'code-boundary':
                bad(lid, 'NOT DECIDABLE BY READBACK (prose requirement; collector limitation)', limitation=obs.get('limitation'))
            else:
                eff = obs.get('effective') or []
                if obs.get('query_exit') != 0 or not any(req['expression'] in e for e in eff):
                    bad(lid, 'rule effective text', required=req['expression'], observed=eff)
        elif t == 'setting':
            if 'name' in req and obs.get('value') != req.get('value'): bad(lid, 'setting value', required=req.get('value'), observed=obs.get('value'))
        elif t == 'boot':
            bad(lid, 'NOT DECIDABLE FROM GUEST (host VM argv required)', guest_cmdline=obs.get('guest_cmdline'))
        else:
            bad(lid, 'type not checked by this reader', type=t)
    for key, fs in snap.get('filesystems', {}).items():
        if not fs.get('selected_declaration_byte_identical'): bad('fs:' + key, 'selected declaration not byte-identical')
        if not fs.get('stable_during_readback'): bad('fs:' + key, 'declaration changed during readback')
        for p, v in fs['paths'].items():
            if v['declared_field_differences']:
                bad('fs:' + key, 'declared field differences', path=p, fields=v['declared_field_differences'])
        for aid, a in fs.get('account_rows', {}).items():
            req, obs = a['required'], a['observed']
            if req.get('type') == 'setting' and 'path' in req:
                if obs.get('sha256') != req.get('sha256'): bad('fs:' + key, 'account database bytes', id=aid, required=req.get('sha256'), observed=obs.get('sha256'))
            elif req.get('type') == 'account':
                for k in ('name', 'uid', 'gid', 'shell', 'home', 'gecos'):
                    if obs.get(k) != req.get(k): bad('fs:' + key, 'account ' + k, id=aid, required=req.get(k), observed=obs.get(k))
            elif req.get('type') == 'group':
                if obs.get('gid') != req.get('gid'): bad('fs:' + key, 'group gid', id=aid, required=req.get('gid'), observed=obs.get('gid'))
    return out


def area(path):
    parts = path.split('/')
    if parts[1] == 'rows':
        sub = '/'.join(parts[3:5])
        return 'rows:' + sub
    if parts[1] == 'filesystems':
        if len(parts) > 5 and parts[3] == 'paths':
            return 'filesystems:paths:' + '/'.join(p for p in parts[-2:] if not p.startswith('st_') or True)[-40:].split('/')[-1]
        return 'filesystems:' + '/'.join(parts[3:4])
    return parts[1] + ':' + '/'.join(parts[2:3])


if __name__ == '__main__':
    if sys.argv[1] == 'fulfil':
        snap = json.load(open(sys.argv[2])); bundle = json.load(open(sys.argv[3]))
        res = fulfil(snap, bundle)
        c = collections.Counter((r['line'] if not r['line'].startswith('fs:') else r['line'], r['what']) for r in res)
        print(json.dumps({'mismatch_count': len(res), 'by_line_and_kind': [[k[0], k[1], n] for k, n in sorted(c.items())],
                          'mismatches': res}, indent=1, default=str))
    else:
        d = json.load(open(sys.argv[2]))['all_differences']
        c = collections.Counter(area(x['path']) for x in d)
        print(json.dumps({'difference_count': len(d), 'by_area': sorted(c.items())}, indent=1))

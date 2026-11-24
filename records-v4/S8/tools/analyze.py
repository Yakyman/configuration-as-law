#!/usr/bin/env python3
"""Offline summary of one step-8 observation JSON (performer's reading aid, S8).

Reads the raw collector output; changes nothing. Prints a compact JSON summary:
identity/authority, declaration entry counts, (b) line-to-state mismatches,
(a) census entries without any own claim, split by whether they changed after
a given UTC boundary (the history's guest creation), and package/account/unit
entries without an own line. No outcome is computed.
"""
import collections
import hashlib
import json
import sys

FILE_KEYS = ('kind', 'mode', 'uid', 'gid', 'sha256', 'target')


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def cmp_file(want, got):
    if 'error' in got:
        return {'missing_or_error': got.get('error')}
    d = {}
    for k in FILE_KEYS:
        if k in want and got.get(k) != want[k]:
            d[k] = {'required': want[k], 'observed': got.get(k)}
    return d


def cmp_package(identity, observed):
    if identity.get('backend') == 'dpkg':
        if not isinstance(observed, dict) or observed.get('exit') != 0:
            return {'package_query': observed}
        parts = observed.get('stdout', '').strip().split('\t')
        if len(parts) != 4:
            return {'package_query_unparsed': observed.get('stdout')}
        name, version, arch, status = parts
        d = {}
        if version != identity.get('version'):
            d['version'] = {'required': identity.get('version'), 'observed': version}
        if identity.get('architecture') and arch != identity['architecture']:
            d['architecture'] = {'required': identity['architecture'], 'observed': arch}
        if status != 'installed':
            d['status'] = status
        return d
    if not isinstance(observed, list):
        return {'ledger_query': observed}
    match = [e for e in observed if e.get('identity', {}).get('version') == identity.get('version')]
    return {} if match else {'ledger': {'required': identity, 'observed': observed}}


def p2_row(row, obs):
    t = row['type']
    if 'QUERY_ERROR' in obs:
        return {'query_error': obs}
    if t in ('program', 'base', 'code'):
        d = {}
        files = row.get('files', [])
        return d, files
    if t == 'account':
        if obs.get('missing'):
            return {'missing': True}
        d = {}
        for k in ('name', 'uid', 'gid', 'shell', 'home', 'gecos'):
            if k in row and obs.get(k) != row[k]:
                d[k] = {'required': row[k], 'observed': obs.get(k)}
        if 'groups' in row and sorted(obs.get('groups', [])) != sorted(row['groups']):
            d['groups'] = {'required': sorted(row['groups']), 'observed': obs.get('groups')}
        return d
    if t == 'group':
        if obs.get('missing'):
            return {'missing': True}
        return {k: {'required': row[k], 'observed': obs.get(k)} for k in ('name', 'gid', 'members')
                if k in row and obs.get(k) != (sorted(row[k]) if k == 'members' else row[k])}
    if t in ('service', 'timer', 'socket'):
        d = {}
        if 'enabled' in row and obs.get('enabled') != row['enabled']:
            d['enabled'] = {'required': row['enabled'], 'observed': obs.get('enabled')}
        if 'unit_sha256' in row:
            got = obs.get('unit_file', {}).get('sha256')
            if got != row['unit_sha256']:
                d['unit_sha256'] = {'required': row['unit_sha256'], 'observed': got}
        if 'active' in row and obs.get('active') != row['active']:
            d['active'] = {'required': row['active'], 'observed': obs.get('active')}
        return d
    if t in ('privilege', 'login-key'):
        d = cmp_file({'kind': 'file', 'mode': row['mode'], 'uid': row['uid'], 'gid': row['gid'],
                      'sha256': sha(row['text'])}, obs.get('file', {}))
        if obs.get('text') != row['text']:
            d['text'] = 'differs'
        return d
    if t == 'password-login':
        want = 'yes' if row.get('allowed') else 'no'
        return {k: {'required': want, 'observed': v} for k, v in obs.items() if v != want}
    if t == 'rule':
        b = row.get('backend', 'nft')
        if b == 'dac':
            d = {}
            for want, got in zip(row['paths'], obs.get('paths', [])):
                x = cmp_file(want, got)
                if x:
                    d[want['path']] = x
            return d
        if b == 'mount':
            eff = set(obs.get('effective', '').split(','))
            miss = [o for o in row['required_options'] if o not in eff]
            return {'missing_options': miss, 'effective': obs.get('effective')} if miss else {}
        if b == 'code-boundary':
            return {'UNPROVED_PROSE_OBLIGATION': 'semantic prose requirement; reader states it does not prove it'}
        if b == 'nft-chain':
            want = row['chain']
            ok = any(all(c.get(k) == v for k, v in want.items()) for c in obs.get('chain', []))
            return {} if ok else {'chain': {'required': want, 'observed': obs.get('chain')}}
        rules = obs.get('rules', [])
        if not rules:
            return {'rule_absent': True}
        if 'expr' in row and not any(r.get('expr') == row['expr'] for r in rules):
            return {'expr': 'differs'}
        return {}
    if t == 'port':
        return {} if obs.get('listening') == row.get('listening') else {
            'listening': {'required': row.get('listening'), 'observed': obs.get('listening')}}
    if t == 'setting':
        return {} if obs.get('value') == row.get('value') else {
            'value': {'required': row.get('value'), 'observed': obs.get('value')}}
    if t == 'boot':
        return {'UNPROVED_HOST_OBLIGATION': 'boot order/firmware are host facts; guest cmdline only'}
    return {'UNQUERIED_TYPE': t}


def main():
    path, boundary = sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else None
    o = json.load(open(path))
    s = {'evidence': path, 'format': o.get('format'), 'collection_error': (o.get('collection_error') or '')[-600:] or None,
         'boot_id': (o.get('identity_before') or {}).get('boot_id', '').strip(),
         'started_utc': o.get('started_utc'), 'ended_utc': o.get('ended_utc'),
         'declaration_stable': o.get('declaration_stable'), 'success_reports_stable': o.get('success_reports_stable')}
    auth = o.get('declaration_authority', {})
    m = auth.get('machine', {})
    s['authority'] = {'machine_generation': (m.get('receipt') or {}).get('declaration'),
                      'machine_receipt_status': (m.get('receipt') or {}).get('status'),
                      'selected_pointer_matches': m.get('selected_pointer_matches'),
                      'content_identity_matches_receipt': m.get('content_identity_matches_receipt'),
                      'machine_FACT_UNKNOWN': m.get('FACT_UNKNOWN'),
                      'filesystems': {k: v.get('authority', v.get('FACT_UNKNOWN')) for k, v in auth.get('filesystems', {}).items()}}
    ident = o.get('identity_at_comparison') or {}
    try:
        rcpt = json.loads(ident['reports']['/var/lib/stand/last-success.json'])
        s['authority']['last_success_report'] = rcpt
        if s['authority']['machine_generation'] is None:
            s['authority']['machine_generation'] = rcpt.get('declaration')
            s['authority']['machine_receipt_status'] = rcpt.get('status')
        s['authority']['current_pointer'] = ident.get('pointers', {}).get('/var/lib/stand/current')
    except Exception as e:
        s['authority']['last_success_report'] = 'unavailable: ' + type(e).__name__
    s['primary_sha256'] = {k: v.get('sha256') for k, v in ident.get('files', {}).items()}
    s['reports'] = {k: (v if isinstance(v, dict) else v[:300]) for k, v in ident.get('reports', {}).items()}
    decl = (o.get('complete_declaration') or {}).get('files', {})
    rows = [json.loads(x) for x in decl.get('/var/lib/stand/current/machine.jsonl', '').splitlines() if x.strip()]
    counts = {'machine_rows': len(rows), 'machine_rows_by_type': dict(collections.Counter(r['type'] for r in rows))}
    fsd = {}
    for k, v in decl.items():
        if k.startswith('/var/lib/stand-fs/'):
            j = json.loads(v)
            fsd[k.split('/')[4]] = j
            counts['fs_paths_' + k.split('/')[4]] = len(j.get('paths', {}))
            counts['fs_account_rows_' + k.split('/')[4]] = len(j.get('account_rows', []))
            counts['fs_generation_' + k.split('/')[4]] = j.get('generation')
    counts['total_entries'] = counts['machine_rows'] + sum(v for k, v in counts.items() if k.startswith('fs_paths_') or k.startswith('fs_account_rows_'))
    s['declaration_counts'] = counts
    try:
        names = sorted({'machine.jsonl'} | {r['files_manifest'] for r in rows if 'files_manifest' in r})
        blob = b''.join(n.encode() + b'\0' + decl['/var/lib/stand/current/' + n].encode() for n in names)
        s['authority']['machine_identity_recomputed_offline'] = hashlib.sha256(blob).hexdigest()
        s['authority']['machine_identity_matches_receipt_offline'] = (
            hashlib.sha256(blob).hexdigest() == s['authority']['machine_generation'])
    except Exception as e:
        s['authority']['machine_identity_recomputed_offline'] = 'unavailable: ' + type(e).__name__
    s['machine_rows_ids_by_type'] = {}
    # (b) machine lines
    mism = {}
    unproved = {}
    for rid, rec in o.get('p2_rows', {}).items():
        row, obs = rec['required'], rec['observed']
        if row['type'] in ('program', 'base', 'code'):
            if 'QUERY_ERROR' in obs:
                mism[rid] = {'query_error': obs}
                continue
            files = row.get('files', [])
            if 'files_manifest' in row:
                files = json.loads(decl['/var/lib/stand/current/' + row['files_manifest']])
            d = {}
            for want, got in zip(files, obs.get('files', [])):
                x = cmp_file(want, got)
                if x:
                    d[want['path']] = x
            if len(files) != len(obs.get('files', [])):
                d['_file_count'] = {'required': len(files), 'observed': len(obs.get('files', []))}
            if row.get('package_identity'):
                x = cmp_package(row['package_identity'], obs.get('package_registration'))
                if x:
                    d['_package'] = x
            for dep in row.get('package_dependencies', []):
                x = cmp_package(dep, obs.get('dependency_registrations', {}).get(dep['name']))
                if x:
                    d['_dependency_' + dep['name']] = x
        else:
            d = p2_row(row, obs)
        if d:
            if any(k.startswith('UNPROVED') for k in d):
                unproved[rid] = d
            else:
                mism[rid] = d
    s['p2_machine_rows_checked'] = len(o.get('p2_rows', {}))
    s['p2_machine_mismatches'] = mism
    s['p2_machine_unproved'] = unproved
    # (b) filesystem lines
    fsm = {}
    field_counter = collections.Counter()
    for key, rec in o.get('p2_filesystems', {}).items():
        for p, prec in rec.get('paths', {}).items():
            diff = prec.get('differences') or {}
            if diff:
                fsm[key + ':' + p] = {k: v for k, v in diff.items()}
                for k in diff:
                    field_counter[k] += 1
        for aid, arec in rec.get('account_rows', {}).items():
            d = p2_row(arec['required'], arec['observed'])
            if d:
                fsm[key + ':account:' + aid] = d
                field_counter['account_row'] += 1
        if rec.get('unreachable_objects'):
            s.setdefault('fs_unreachable_objects', {})[key] = list(rec['unreachable_objects'])
    s['p2_filesystem_paths_checked'] = sum(len(r.get('paths', {})) for r in o.get('p2_filesystems', {}).values())
    s['p2_filesystem_mismatch_fields'] = dict(field_counter)
    non_time = {k: v for k, v in fsm.items() if set(v) - {'st_atime', 'st_ctime', 'st_mtime'}}
    s['p2_filesystem_mismatches_non_timestamp'] = non_time
    s['p2_filesystem_mismatches_timestamp_only'] = sorted(k for k in fsm if k not in non_time)
    # (a) census entries without any own claim
    census = o.get('independent_census', {})
    files = census.get('files', {})
    rel = o.get('p1_file_relations', {})
    unclaimed = [p for p, r in rel.items() if not r.get('own_line_comparisons')]
    claimed_mismatch = [p for p, r in rel.items() if r.get('own_line_comparisons')
                        and not any(c['state_matches'] for c in r['own_line_comparisons'])]
    # package membership from dpkg .list files (membership is not proof of unchanged receipt)
    members = {}
    for rp, text in census.get('installer_records', {}).items():
        if rp.endswith('.list') and isinstance(text, str):
            pkg = rp.rsplit('/', 1)[1][:-5]
            for line in text.splitlines():
                members.setdefault(line, []).append(pkg)
    new = []
    old_groups = collections.Counter()
    old_kinds = collections.Counter()
    old_nondir = []
    for p in unclaimed:
        st = files.get(p, {})
        changed = boundary is not None and max(st.get('st_ctime', 0), st.get('st_mtime', 0)) >= boundary
        if changed:
            new.append({'path': p, 'kind': st.get('kind'), 'mode': st.get('mode'), 'uid': st.get('uid'),
                        'size': st.get('st_size'), 'sha256': st.get('sha256'), 'dpkg_member_of': members.get(p),
                        'mtime': st.get('st_mtime'), 'ctime': st.get('st_ctime'),
                        'executable_bit': bool((st.get('mode') or 0) & 0o111) and st.get('kind') == 'file'})
        else:
            old_groups['/'.join(p.split('/')[:3])] += 1
            old_kinds[st.get('kind')] += 1
            if st.get('kind') != 'directory':
                old_nondir.append([p, st.get('kind'), bool(members.get(p))])
    s['unclaimed_unchanged_by_kind'] = dict(old_kinds)
    s['unclaimed_unchanged_non_directories'] = old_nondir
    # system-built copies under the code root: same bytes as a declared original of the same path?
    cr = '/var/lib/stand/code-root'
    dstat = collections.Counter()
    dbad = []
    for p in unclaimed:
        if not p.startswith(cr + '/'):
            continue
        rest = p[len(cr):]
        comps = rel.get(rest, {}).get('own_line_comparisons', [])
        if not comps:
            kind = files.get(p, {}).get('kind')
            dstat['no_declared_counterpart_' + str(kind)] += 1
            if kind != 'directory':
                dbad.append(p)
            continue
        orig, st = files.get(rest, {}), files.get(p, {})
        same = all(orig.get(k) == st.get(k) for k in ('kind', 'sha256', 'target'))
        ok = same and any(c['state_matches'] for c in comps)
        dstat['same_as_declared_original' if ok else 'differs_from_declared_original'] += 1
        if not ok:
            dbad.append(p)
    s['code_root_copies'] = dict(dstat)
    s['code_root_copies_not_matching'] = dbad[:300]
    badset = set(dbad)
    s['unclaimed_changed_outside_code_root_copies'] = [
        e for e in new if not e['path'].startswith(cr + '/') or e['path'] in badset]
    s['unclaimed_changed_since_boundary'] = [e['path'] for e in new][:50]
    s['census_entries'] = len(files)
    s['census_scan_errors'] = census.get('scan_errors', [])[:50]
    s['unclaimed_total'] = len(unclaimed)
    s['unclaimed_changed_since_boundary_count'] = len(new)
    s['unclaimed_unchanged_by_top_directory'] = dict(old_groups.most_common())
    s['claimed_but_no_matching_claim'] = claimed_mismatch[:400]
    s['claimed_but_no_matching_claim_count'] = len(claimed_mismatch)
    # packages without own line
    s['packages_without_own_line'] = [r['actual'] for r in o.get('p1_package_relations', []) if not r['own_lines']]
    s['packages_installed'] = len(o.get('p1_package_relations', []))
    # accounts and groups versus account rows
    declared_accounts = {r['name'] for r in rows if r['type'] == 'account'}
    for j in fsd.values():
        declared_accounts |= {r.get('name') for r in j.get('account_rows', []) if r.get('type') == 'account'}
    declared_groups = {r['name'] for r in rows if r['type'] == 'group'}
    for j in fsd.values():
        declared_groups |= {r.get('name') for r in j.get('account_rows', []) if r.get('type') == 'group'}
    s['accounts_without_account_row'] = sorted(a['name'] for a in census.get('accounts', []) if a['name'] not in declared_accounts)
    s['groups_without_group_row'] = sorted(g['name'] for g in census.get('groups', []) if g['name'] not in declared_groups)
    # enabled system units versus unit rows
    declared_units = {r['unit'] for r in rows if r['type'] in ('service', 'timer', 'socket')}
    q = census.get('queries', [])
    enabled = []
    if q and len(q) > 1 and q[1].get('exit') == 0:
        for line in q[1]['stdout'].splitlines():
            f = line.split()
            if len(f) >= 2 and f[1] in ('enabled', 'enabled-runtime', 'linked', 'linked-runtime', 'alias') and f[0] not in declared_units:
                enabled.append(f[:2])
    s['enabled_units_without_unit_row'] = enabled
    s['query_failures'] = [{'argv': x['argv'], 'exit': x.get('exit'), 'error': x.get('error'),
                            'stderr': (x.get('stderr') or '')[:200]} for x in q
                           if x.get('exit') not in (0,) and '/usr/bin/sudo' not in x['argv'][0]][:60]
    print(json.dumps(s, indent=1, sort_keys=True, default=str))


if __name__ == '__main__':
    main()

"""Snapshot-specific RPM evidence and current MicroOS configuration sources.

No classification or historical creator is inferred from a matching current value.
"""
import base64
import json
import re
import shlex
import subprocess
import shutil
import resource
import time
from main import write_tsv

ALGORITHMS = {'(none)': 'md5', '0': 'md5', '1': 'md5', '2': 'sha1',
              '8': 'sha256', '9': 'sha384', '10': 'sha512'}


def collect(ctx):
    if ctx.meta.get('system') != 'microos':
        return
    rows = []
    roots = sorted({m.group(1) for p in ctx.entries
                    if (m := re.match(r'(/\.snapshots/[^/]+/snapshot)(?:/|$)', p))})
    fmt = '[%{=NAME}@%{=VERSION}-%{=RELEASE}.%{=ARCH}\\t%{FILENAMES}\\t%{FILESIZES}\\t%{FILEDIGESTS}\\t%{=FILEDIGESTALGO}\\t%{FILEMODES}\\t%{FILELINKTOS}\\n]'
    for root in roots:
        data, rc, ev = ctx.query('s4-snapshot-rpm', 'rpm --root ' + shlex.quote(root) +
                                ' -qa --qf ' + shlex.quote(fmt), 120)
        manifest = []
        for line in data.decode(errors='replace').splitlines():
            fields = line.split('\t')
            if len(fields) != 7:
                continue
            pkg, path, size, expected, algorithm, mode, target = fields
            if not path.startswith('/') or '..' in path.split('/'):
                continue
            physical = root + path
            alg = ALGORITHMS.get(algorithm)
            typ = int(mode) & 0o170000 if mode.isdigit() else 0
            manifest.append((pkg, path, physical, size, expected, alg, typ, target))
        requests = [(physical, alg) for pkg,path,physical,size,expected,alg,typ,target in manifest
                    if physical in ctx.entries and typ == 0o100000 and alg and expected]
        digests = ctx.digests(requests, 1073741824)
        for pkg, path, physical, size, expected, alg, typ, target in manifest:
            if physical not in ctx.entries:
                continue
            entry = ctx.entries[physical]
            actual = digests.get((physical, alg), {})
            status = 'unknown'
            observed = actual.get('digest', '')
            if typ == 0o100000 and actual.get('status') == 'ok':
                status = 'equal' if observed.lower() == expected.lower() and str(entry.get('size')) == size else 'different'
            elif typ == 0o120000 and entry.get('type') == 'symlink':
                observed = entry.get('target', '')
                expected = target
                status = 'equal' if observed == target else 'different'
            elif typ == 0o040000:
                status = 'directory-membership-only'
            rows.append([root, physical, path, pkg, alg or '', expected, observed, status,
                         ev, actual.get('evidence', ''), rc])
        ctx.scan_counts['s4:microos:snapshot-manifest-roots'] += int(rc == 0 and bool(manifest))
    write_tsv(ctx.out/'s4-microos-snapshot-files.tsv',
              ['snapshot_root','path','package_path','package','algorithm','expected','observed',
               'comparison','manifest_evidence','digest_evidence','manifest_exit'], rows)
    ctx.scan_counts['s4:microos:snapshot-file-rows'] = len(rows)
    ctx.scan_counts['s4:microos:snapshot-full-comparisons'] = sum(r[7] in ('equal','different') for r in rows)
    # Current-path equality is an independent fact, never an installation receipt.
    pairs = []
    for path, entry in ctx.entries.items():
        match = re.match(r'(/\.snapshots/[^/]+/snapshot)(/.*)', path)
        if match and entry.get('type') == 'file':
            current = match.group(2)
            if ctx.entries.get(current, {}).get('type') == 'file':
                pairs.append((path, current))
    requests = sorted({(path, 'sha256') for pair in pairs for path in pair})
    hashes = ctx.digests(requests, 1073741824)
    comparisons = []
    for path, current in pairs:
        saved = hashes.get((path, 'sha256'), {})
        active = hashes.get((current, 'sha256'), {})
        known = saved.get('status') == active.get('status') == 'ok'
        state = ('equal' if saved.get('digest') == active.get('digest') else 'different') if known else 'unknown'
        comparisons.append([path, current, saved.get('digest', ''), active.get('digest', ''),
                            state, saved.get('evidence', ''), active.get('evidence', '')])
    write_tsv(ctx.out/'s4-microos-snapshot-current.tsv',
              ['snapshot_path','current_path','snapshot_sha256','current_sha256','comparison',
               'snapshot_evidence','current_evidence'], comparisons)
    ctx.scan_counts['s4:microos:snapshot-current-total'] = len(comparisons)
    ctx.scan_counts['s4:microos:snapshot-current-known'] = sum(r[4] != 'unknown' for r in comparisons)
    ctx.scan_counts['s4:microos:active-etc-descendants'] = sum(p.startswith('/etc/') for p in ctx.entries)
    ctx.scan_counts['s4:microos:active-etc-traversed'] = int(any(p.startswith('/etc/') for p in ctx.entries))
    # Read source content and preserve raw bytes. No shell evaluation of configuration.
    paths = []
    for p, entry in ctx.entries.items():
        if entry.get('type') != 'file':
            continue
        if (p.startswith(('/etc/systemd/', '/usr/etc/systemd/', '/usr/lib/systemd/system/',
                          '/usr/lib/systemd/user/', '/etc/sysusers.d/', '/usr/lib/sysusers.d/',
                          '/etc/sudoers.d/', '/usr/etc/sudoers.d/', '/run/systemd/system/',
                          '/run/systemd/generator/', '/run/systemd/generator.early/',
                          '/run/systemd/generator.late/')) or
                p in ('/etc/sudoers','/usr/etc/sudoers','/boot/grub2/grubenv','/etc/selinux/semanage.conf') or
                (p.endswith('/lang_ext') and '/active/modules/' in p)):
            paths.append(p)
    contents = ctx.safe_reads(sorted(paths), 16777216)
    write_tsv(ctx.out/'s4-microos-sources.tsv', ['path','status','content_base64','evidence'],
              [[p,'ok' if rc == 0 else 'unknown',base64.b64encode(b).decode() if rc == 0 else '',ev]
               for p,(b,rc,ev) in contents.items()])
    ctx.scan_counts['s4:microos:source-files-read'] = sum(rc == 0 for b,rc,ev in contents.values())
    links = [[p,r.get('target',''),r.get('target_error','')] for p,r in ctx.entries.items()
             if r.get('type') == 'symlink' and p.startswith(('/etc/systemd/','/usr/etc/systemd/',
                                                           '/usr/lib/systemd/', '/run/systemd/system/',
                                                           '/run/systemd/generator/', '/run/systemd/generator.early/',
                                                           '/run/systemd/generator.late/'))]
    write_tsv(ctx.out/'s4-microos-unit-links.tsv', ['path','target','error'], links)
    selected = []
    for kind in ('unit-file','user-unit-file'):
        groups = {}
        for obj in ctx.objects:
            if obj[3] != kind:
                continue
            user, unit = obj[4].split(':',1) if kind == 'user-unit-file' and ':' in obj[4] else ('',obj[4])
            groups.setdefault(user, []).append((obj[0],unit))
        for user, units in groups.items():
            templates = [(i,u) for i,u in units if '@.' in u]
            units = [(i,u) for i,u in units if '@.' not in u]
            for ident, unit in templates:
                command = 'systemctl ' + ('--user ' if user else '') + 'cat --no-pager ' + shlex.quote(unit)
                if user:
                    command = ctx.as_user(user,command)
                data,rc,ev = ctx.query('s4-unit-template-source',command,60)
                paths = [line[2:] for line in data.decode(errors='replace').splitlines() if line.startswith('# /')]
                props = [{'Id':unit,'FragmentPath':paths[0] if paths else '', 'SourceFiles':paths, 'reader':'systemctl cat'}] if rc == 0 and paths else []
                selected.append([ident,user,unit,json.dumps(props,sort_keys=True),rc,ev])
            if not units:
                continue
            command = 'systemctl ' + ('--user ' if user else '') + 'show --no-pager --property=Id,Names,FragmentPath,SourcePath,DropInPaths,UnitFileState,UnitFilePreset,LoadState ' + shlex.join([u for _,u in units])
            if user:
                command = ctx.as_user(user,command)
            data,rc,ev = ctx.query('s4-unit-selected',command,120)
            records=[]
            for block in data.decode(errors='replace').strip().split('\n\n'):
                records.append(dict(line.split('=',1) for line in block.splitlines() if '=' in line))
            for ident,unit in units:
                matches=[r for r in records if unit == r.get('Id') or unit in r.get('Names','').split()]
                selected.append([ident,user,unit,json.dumps(matches,sort_keys=True),rc,ev])
    write_tsv(ctx.out/'s4-microos-unit-selected.tsv', ['object_id','user','unit','properties_json','query_exit','evidence'], selected)
    ctx.scan_counts['s4:microos:unit-selection-rows'] = len(selected)
    ctx.scan_counts['s4:microos:unit-selections-known'] = sum(r[3] != '[]' for r in selected)
    data,rc,ev = ctx.query('s4-microos-scriptlet-sources',
                          "rpm -qa --qf '%{NAME}\\n%{PREIN}\\n%{POSTIN}\\n'",120)
    write_tsv(ctx.out/'s4-microos-scriptlet-query.tsv',['query_exit','evidence'],[[rc,ev]])
    # These queries disclose current storage and stored installation logs, without
    # assigning a causal history when none is retained.
    ctx.query('s4-microos-mounts','findmnt --json --output TARGET,SOURCE,FSTYPE,OPTIONS',60)
    ctx.query('s4-microos-subvolume','btrfs subvolume show /etc; btrfs subvolume list /',60)

    stores = sorted({(m.group(1),m.group(2)) for p in ctx.entries
                     if (m := re.match(r'(.*/(?:etc|var/lib)/selinux)/([^/]+)/active/modules/', p))})
    store_queries = []
    for store, policy in stores:
        data, rc, ev = ctx.query('s4-selinux-modules',
                                'semodule -S ' + shlex.quote(store) + ' -s ' + shlex.quote(policy) + ' -lfull -m', 120)
        store_queries.append([store, policy, rc, ev])
    write_tsv(ctx.out/'s4-microos-selinux-stores.tsv', ['store_root','policy','query_exit','evidence'], store_queries)
    ctx.scan_counts['s4:microos:selinux-stores-listed'] = sum(r[2] == 0 for r in store_queries)

    solver_paths = sorted(p for p,r in ctx.entries.items()
                          if '/var/cache/zypp/solv/@System/' in p and r.get('type') == 'file')
    solver_rows = []
    for path in solver_paths:
        digest = ctx.digests([(path,'sha256')],1073741824).get((path,'sha256'),{})
        if path.endswith('/solv'):
            data, read_rc, read_ev = ctx.safe_read(path,16777216)
            reader = shutil.which('dumpsolv')
            number = len(solver_rows)
            ev = f'raw/s4-solv-host-{number}.out'
            err_ev = f'raw/s4-solv-host-{number}.err'
            rc = 127 if not reader else read_rc
            begin = time.monotonic()
            if reader and read_rc == 0:
                def bounds():
                    resource.setrlimit(resource.RLIMIT_FSIZE,(67108864,67108864))
                with (ctx.out/ev).open('wb') as stdout, (ctx.out/err_ev).open('wb') as stderr:
                    try:
                        result = subprocess.run([reader],input=data,stdout=stdout,stderr=stderr,
                                                timeout=60,preexec_fn=bounds)
                        rc = result.returncode
                    except subprocess.TimeoutExpired:
                        rc = 124
            else:
                (ctx.out/ev).write_bytes(b'')
                (ctx.out/err_ev).write_text('Host dumpsolv or complete input unavailable.\n')
            ctx.coverage.append(['s4-solv-host-decode',rc,round(time.monotonic()-begin,3),0,
                                 (ctx.out/ev).stat().st_size,ev,err_ev,'ok' if rc == 0 else 'not-collected',0])
            ctx.flush()
            status = 'decoded' if rc == 0 else 'unavailable'
            ev = read_ev + ';' + ev
        else:
            data,rc,ev = ctx.safe_read(path,16777216)
            status = 'read' if rc == 0 else 'unavailable'
        solver_rows.append([path,status,rc,ev,digest.get('status','unknown'),digest.get('digest',''),digest.get('evidence','')])
    write_tsv(ctx.out/'s4-microos-solver-cache.tsv',
              ['path','content_status','query_exit','content_evidence','digest_status','sha256','digest_evidence'],solver_rows)
    ctx.scan_counts['s4:microos:solver-cache-files'] = len(solver_rows)
    ctx.scan_counts['s4:microos:solver-cache-decodes'] = sum(r[1] == 'decoded' for r in solver_rows)

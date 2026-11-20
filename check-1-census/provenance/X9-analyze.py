#!/usr/bin/env python3
"""Analyze frozen X9 pathname measurements; stdlib only, no experiment execution.

Trace evidence establishes an observed run attribution, never semantic ownership.
All attempts remain in the TSV; primary metrics use the latest complete verified
attempt per label. Run with --self-test for small synthetic parser checks.
"""
import argparse
import ast
import csv
import gzip
import json
import posixpath as pp
import re
from collections import Counter, defaultdict
from pathlib import Path

SIGNATURE = ('type', 'size', 'mtime_ns', 'ctime_ns', 'mode', 'uid', 'gid', 'target')
FILE_TYPES = {'file', 'symlink'}
EXCLUDED = ('/proc', '/sys', '/dev', '/x9')


def beneath(path, root):
    return path == root or path.startswith(root.rstrip('/') + '/')


def included(path):
    return path.startswith('/') and not any(beneath(path, r) for r in EXCLUDED)


def arguments(text):
    """Split strace arguments outside quoted strings and nested structures."""
    result, start, depth, quoted, escape = [], 0, 0, False, False
    for i, c in enumerate(text):
        if quoted:
            if escape:
                escape = False
            elif c == '\\':
                escape = True
            elif c == '"':
                quoted = False
        elif c == '"':
            quoted = True
        elif c in '([{<':
            depth += 1
        elif c in ')]}>':
            depth -= 1
        elif c == ',' and depth == 0:
            result.append(text[start:i].strip())
            start = i + 1
    result.append(text[start:].strip())
    return result


def quoted(token):
    match = re.match(r'"(?:\\.|[^"\\])*"', token)
    if not match or token[match.end():].startswith('...'):
        return None
    try:
        return ast.literal_eval(match.group())
    except (ValueError, SyntaxError):
        return None


def decoded_fd(token):
    match = re.search(r'<(/.*)>', token)
    if not match:
        return None
    path = match.group(1)
    # strace marks unlinked descriptors; this is a pathname alias, not a new name.
    if path.endswith(' (deleted)'):
        path = path[:-10]
    return pp.normpath(path)


def events(lines):
    pending = {}
    stats = Counter()
    unknown_syscall_details = []
    for lineno, raw in enumerate(lines, 1):
        line = raw.rstrip('\n')
        match = re.match(r'^(?:\[pid\s+(\d+)\]\s+|(\d+)\s+)?(?:\d+\.\d+\s+)?(.*)$', line)
        pid = match.group(1) or match.group(2) or 'root'
        body = match.group(3)
        numbered = re.match(r'^\[\s*(\d+)\s*\]\s*(.*)$', body)
        syscall_number = int(numbered.group(1)) if numbered else None
        if numbered:
            body = numbered.group(2)
        startline = lineno
        resume = re.match(r'<\.\.\. (\w+) resumed>(.*)', body)
        if resume:
            old = pending.pop(pid, None)
            if old is None:
                stats['orphan_resumed'] += 1
                continue
            body, startline = old[0] + resume.group(2), old[1]
            if old[2] is not None:
                if syscall_number is not None and syscall_number != old[2]:
                    stats['resumed_syscall_number_mismatches'] += 1
                syscall_number = old[2]
        if '<unfinished ...>' in body:
            pending[pid] = (body.split('<unfinished ...>')[0], startline, syscall_number)
            continue
        call = re.match(r'^(\w+)\((.*)\)\s+=\s+(.+)$', body)
        if not call:
            if body.startswith('???('):
                stats['unknown_syscall_count'] += 1
                unknown_syscall_details.append({'pid': pid, 'line': startline, 'end_line': lineno,
                                               'syscall_number': syscall_number, 'prefix': body[:120]})
            if not any(x in body for x in ('+++', '---', 'strace:', 'Process ')):
                stats['unparsed_lines'] += 1
            continue
        name, args, result = call.groups()
        if result.startswith('-1 ') or result.startswith('?'):
            stats['failed_or_unknown_return'] += 1
            continue
        stats['successful_syscalls'] += 1
        yield pid, name, arguments(args), result, startline, lineno, syscall_number
    stats['unfinished_at_eof'] = len(pending)
    stats['unfinished_syscalls_at_eof'] = dict(Counter(re.match(r'(\w+)', body.lstrip()).group(1) if re.match(r'(\w+)', body.lstrip()) else 'unknown' for body, line, number in pending.values()))
    stats['unfinished_nonexit_at_eof'] = sum(not body.lstrip().startswith(('exit(', 'exit_group(')) for body, line, number in pending.values())
    stats['unfinished_details'] = [{'pid': pid, 'line': line, 'prefix': body[:120], 'syscall_number': number} for pid, (body, line, number) in pending.items()]
    stats['unknown_syscall_details'] = unknown_syscall_details
    yield None, stats


def parse_trace(path, initial_cwd):
    parsed = list(events(path.read_text(errors='replace').splitlines()))
    stats = parsed.pop()[1]
    parents = {}
    for pid, name, args, result, first, last, syscall_number in parsed:
        if name in ('clone', 'clone3', 'fork', 'vfork'):
            m = re.match(r'(\d+)', result)
            if m and int(m.group(1)) > 0:
                parents[m.group(1)] = (pid, 'CLONE_FS' in ','.join(args))
    cwd, candidates = {}, defaultdict(list)

    def state(pid):
        if pid not in cwd:
            if pid in parents:
                parent, shared = parents[pid]
                source = state(parent)
                cwd[pid] = source if shared else [source[0], source[1], list(source[2]), list(source[3])]
            else:
                # Host-guest pathname cwd, explicit process root, root evidence,
                # and mount targets with no established host mapping.
                cwd[pid] = [initial_cwd, '/', [], []]
        return cwd[pid]

    for pid, name, args, result, first, last, syscall_number in parsed:
        current = state(pid)

        def host_path(namespace_path):
            if namespace_path is None:
                return None
            if '(unreachable)' in namespace_path:
                stats['unresolved_namespace_paths'] += 1
                return None
            translated = pp.normpath(pp.join(current[1], namespace_path.lstrip('/')))
            if any(beneath(translated, blocked) for blocked in current[3]):
                stats['unresolved_namespace_paths'] += 1
                return None
            return translated

        def fd_path(token):
            return host_path(decoded_fd(token))

        def resolve(index, dirindex=None):
            if index >= len(args):
                return None
            pathpart = quoted(args[index])
            if pathpart is None:
                stats['unresolved_path_arguments'] += 1
                return None
            if pathpart.startswith('/'):
                return host_path(pp.normpath(pathpart))
            base = current[0]
            if dirindex is not None:
                fd = args[dirindex]
                decoded = fd_path(fd)
                if decoded:
                    base = decoded
                elif not fd.startswith('AT_FDCWD'):
                    stats['unresolved_dirfd'] += 1
                    return None
            resolved = pp.normpath(pp.join(base, pathpart))
            if any(beneath(resolved, blocked) for blocked in current[3]):
                stats['unresolved_namespace_paths'] += 1
                return None
            return resolved

        paths = []
        creation_paths = set()
        if name == 'chdir':
            new = resolve(0)
            if new:
                current[0] = new
        elif name == 'fchdir':
            new = fd_path(args[0])
            if new:
                current[0] = new
            else:
                stats['unresolved_fchdir'] += 1
        elif name in ('clone', 'clone3', 'fork', 'vfork'):
            child = re.match(r'(\d+)', result)
            if child and child.group(1) not in cwd:
                cwd[child.group(1)] = current if 'CLONE_FS' in ','.join(args) else [current[0], current[1], list(current[2]), list(current[3])]
        elif name == 'unshare':
            if 'CLONE_FS' in ','.join(args):
                cwd[pid] = [current[0], current[1], list(current[2]), list(current[3])]
            stats['namespace_unshare_events'] += 1
        elif name == 'setns':
            # A namespace entered by fd has no proven correspondence to snapshots.
            current[3].append('/')
            stats['unsupported_setns_events'] += 1
        elif name in ('chroot', 'pivot_root'):
            newroot = resolve(0)
            if newroot is None:
                current[3].append('/')
                stats['unsupported_root_changes'] += 1
            else:
                oldroot_target = resolve(1) if name == 'pivot_root' else None
                current[1] = newroot
                current[2].append({'operation': name, 'line': first, 'end_line': last, 'root': newroot, 'syscall_number': syscall_number})
                if oldroot_target:
                    current[3].append(oldroot_target)
                stats['explicit_root_changes'] += 1
        elif name == 'mount' and len(args) >= 4:
            target = resolve(1)
            source = resolve(0) if quoted(args[0]) and quoted(args[0]).startswith('/') else None
            flags = args[3]
            propagation_only = any(flag in flags for flag in ('MS_PRIVATE', 'MS_SLAVE', 'MS_SHARED', 'MS_UNBINDABLE'))
            same_path_bind = 'MS_BIND' in flags and source is not None and source == target
            if target and not propagation_only and not same_path_bind and 'MS_REMOUNT' not in flags:
                current[3].append(target)
                stats['unsupported_mount_mappings'] += 1
        elif name in ('open', 'openat', 'openat2', 'creat'):
            flags = args[2] if name.startswith('openat') else args[1]
            if name == 'creat' or re.search(r'\bO_(WRONLY|RDWR|CREAT|TRUNC)\b', flags):
                paths = [fd_path(result) if decoded_fd(result) is not None else (resolve(1, 0) if name.startswith('openat') else resolve(0))]
                if name == 'creat' or re.search(r'\bO_CREAT\b', flags):
                    creation_paths.update(paths)
        elif name in ('write', 'writev', 'pwrite64', 'pwritev', 'pwritev2', 'ftruncate', 'fchmod', 'fchown'):
            if name.startswith(('write', 'pwrite')) and re.match(r'0(?:\s|$)', result):
                continue
            paths = [fd_path(args[0])]
            if paths[0] is None:
                stats['unresolved_or_nonfile_fd_mutations'] += 1
        elif name in ('mmap', 'mmap2'):
            if len(args) > 4 and 'PROT_WRITE' in args[2] and 'MAP_SHARED' in args[3]:
                paths = [fd_path(args[4])]
        elif name in ('rename', 'renameat', 'renameat2'):
            paths = [resolve(0), resolve(1)] if name == 'rename' else [resolve(1, 0), resolve(3, 2)]
            creation_paths.add(paths[1])
            if name == 'renameat2' and 'RENAME_EXCHANGE' in ','.join(args):
                creation_paths.add(paths[0])
        elif name in ('link', 'symlink'):
            paths = [resolve(1)]
            creation_paths.update(paths)
        elif name == 'linkat':
            paths = [resolve(3, 2)]
            creation_paths.update(paths)
        elif name == 'symlinkat':
            paths = [resolve(2, 1)]
            creation_paths.update(paths)
        elif name in ('unlinkat', 'mkdirat', 'mknodat', 'fchmodat', 'fchmodat2', 'fchownat', 'utimensat', 'futimesat'):
            paths = [resolve(1, 0)]
        elif name in ('unlink', 'rmdir', 'mkdir', 'mknod', 'truncate', 'chmod', 'chown', 'lchown', 'utime', 'utimes', 'lutimes', 'setxattr', 'lsetxattr', 'removexattr', 'lremovexattr'):
            paths = [resolve(0)]
        for candidate in set(paths):
            if candidate and included(candidate):
                # First evidence per operation is sufficient; bounded output.
                evidence = {'operation': name, 'line': first, 'end_line': last, 'pid': pid,
                            'creation_candidate': candidate in creation_paths,
                            'syscall_number': syscall_number,
                            'root_mapping': list(current[2])}
                if not any(e['operation'] == name and e['creation_candidate'] == evidence['creation_candidate'] for e in candidates[candidate]):
                    candidates[candidate].append(evidence)
    stats['candidate_paths'] = len(candidates)
    return candidates, dict(stats)


def convention(path, environment):
    env = environment if isinstance(environment, dict) else {}
    roots = []
    home = env.get('HOME')
    if home and home.startswith('/'):
        for key, suffix in (('XDG_CONFIG_HOME', '.config'), ('XDG_DATA_HOME', '.local/share'),
                            ('XDG_STATE_HOME', '.local/state'), ('XDG_CACHE_HOME', '.cache')):
            root = env.get(key)
            if root and not root.startswith('/'):
                root = None
            roots.append((root or home + '/' + suffix, key))
    if env.get('XDG_RUNTIME_DIR'):
        roots.append((env['XDG_RUNTIME_DIR'], 'XDG_RUNTIME_DIR'))
    for key, default in (('XDG_CONFIG_DIRS', '/etc/xdg'), ('XDG_DATA_DIRS', '/usr/local/share:/usr/share')):
        roots.extend((root, key) for root in env.get(key, default).split(':') if root.startswith('/'))
    roots.append(('/var/lib', 'var-lib'))
    return next((label for root, label in roots if beneath(path, root)), 'outside')


def snapshot(path):
    with gzip.open(path, 'rt') as stream:
        return json.load(stream)


def tsv(path, fields, rows):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fields, delimiter='\t', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def mapping_reference(evidence, trace_ref):
    number_ref = f";syscall_nr={evidence['syscall_number']}" if evidence.get('syscall_number') is not None else ''
    return number_ref + ''.join(f";root-map={trace_ref}:{mapping['line']} ({mapping['operation']} -> {mapping['root']}" + (f";syscall_nr={mapping['syscall_number']}" if mapping.get('syscall_number') is not None else '') + ')' for mapping in evidence.get('root_mapping', []))


def analyze(root):
    raw = root / 'raw-X9'
    runs = []
    for directory in sorted(raw.glob('guest*/runs/*')):
        if not directory.is_dir():
            continue
        meta_path = directory / 'run.json'
        if not meta_path.exists():
            runs.append({'directory': directory, 'label': directory.name, 'verified': False, 'complete': False, 'missing': ['run.json']})
            continue
        meta = json.loads(meta_path.read_text())
        missing = [name for name in ('before.json.gz', 'after.json.gz', 'trace.log') if not (directory / name).exists()]
        runs.append({**meta, 'directory': directory, 'complete': not missing, 'missing': missing})
    chosen = {}
    for run in runs:
        if run.get('verified') and run['complete']:
            old = chosen.get(run['label'])
            if old is None or int(run.get('attempt', 1)) >= int(old.get('attempt', 1)):
                chosen[run['label']] = run
    rows, candidate_rows, summaries = [], [], []
    creators, mutators, created = defaultdict(set), defaultdict(set), set()
    outside, program_outside = set(), defaultdict(set)
    observed_outside, program_observed_outside = set(), defaultdict(set)
    for run in runs:
        directory, label = run['directory'], run['label']
        primary = chosen.get(label) is run
        summary = {k: v for k, v in run.items() if k != 'directory'}
        summary.update(directory=str(directory.relative_to(root)), campaign=directory.parent.parent.name, primary=primary)
        summaries.append(summary)
        if not run['complete']:
            continue
        before, after = snapshot(directory / 'before.json.gz'), snapshot(directory / 'after.json.gz')
        candidates, stats = parse_trace(directory / 'trace.log', run.get('cwd', '/home/subject/work'))
        summary.update(trace_stats=stats, before_errors=before.get('errors', []), after_errors=after.get('errors', []))
        b, a = before['paths'], after['paths']
        counts = Counter()
        traced_snapshot = set()
        for path in sorted(b.keys() | a.keys()):
            if not included(path):
                continue
            old, new = b.get(path), a.get(path)
            if old is not None and new is not None and all(old.get(k) == new.get(k) for k in SIGNATURE):
                continue
            action = 'created' if old is None else 'deleted' if new is None else 'changed'
            entry = new if new is not None else old
            if entry.get('type') not in FILE_TYPES:
                counts['nonfile_' + action] += 1
                continue
            evidence = list(candidates.get(path, []))
            # A directory rename changes names of descendants without per-file syscalls.
            ancestor = pp.dirname(path)
            while ancestor != '/':
                matches = [e for e in candidates.get(ancestor, []) if e['operation'] in ('rename', 'renameat', 'renameat2')]
                if matches and (b.get(ancestor, {}).get('type') == 'dir' or a.get(ancestor, {}).get('type') == 'dir'):
                    evidence.extend({**e, 'via_directory': ancestor} for e in matches)
                    break
                ancestor = pp.dirname(ancestor)
            attributed = bool(evidence)
            creator_supported = action == 'created' and any(e['creation_candidate'] for e in evidence)
            if attributed:
                traced_snapshot.add(path)
            location = convention(path, run.get('environment', {}))
            directed = 'yes' if path in run.get('caller_directed_paths', []) or any(beneath(path, r) for r in run.get('caller_directed_prefixes', [])) else 'unknown'
            ref = str(directory.relative_to(root))
            trace_ref = ';'.join(f"{ref}/trace.log:{e['line']}" + (f"-{e['end_line']}" if e['end_line'] != e['line'] else '') + f" ({e['operation']}" + (' creation-candidate' if e['creation_candidate'] else ' mutation-only') + (f" via {e['via_directory']}" if 'via_directory' in e else '') + ')' + mapping_reference(e, f'{ref}/trace.log') for e in evidence)
            rows.append(dict(program=label, attempt=run.get('attempt', 1), primary_run=int(primary), path=path, action=action,
                             type=entry['type'], attribution='trace-supported' if attributed else 'unattributed', creator_supported=int(creator_supported), convention=location,
                             caller_directed=directed, snapshot_evidence=f'{ref}/before.json.gz;{ref}/after.json.gz;key={path}', trace_evidence=trace_ref))
            counts[action] += 1
            counts['attributed' if attributed else 'unattributed'] += 1
            if primary:
                if location == 'outside':
                    observed_outside.add(path)
                    program_observed_outside[label].add(path)
                if action == 'created':
                    created.add(path)
                    if creator_supported:
                        creators[path].add(label)
                if attributed:
                    mutators[path].add(label)
                    if location == 'outside':
                        outside.add(path)
                        program_outside[label].add(path)
        for path, evidence in sorted(candidates.items()):
            candidate_rows.append(dict(program=label, attempt=run.get('attempt', 1), primary_run=int(primary), path=path,
                                       creation_candidate=int(any(e['creation_candidate'] for e in evidence)),
                                       snapshot_mutation=int(path in traced_snapshot), operations=','.join(e['operation'] for e in evidence),
                                       trace_evidence=';'.join(f"{directory.relative_to(root)}/trace.log:{e['line']}" + mapping_reference(e, f'{directory.relative_to(root)}/trace.log') for e in evidence)))
        summary['counts'] = dict(counts)
    def distribution(mapping):
        counts = Counter(len(mapping[path]) for path in created)
        return dict(zero=counts[0], exactly_one=counts[1], multiple=sum(v for k, v in counts.items() if k >= 2),
                    exactly_one_fraction=counts[1] / len(created) if created else None)
    shared = [dict(path=p, program_count=len(labels), programs=','.join(sorted(labels))) for p, labels in sorted(mutators.items()) if len(labels) >= 2]
    result = dict(schema_version=1, measurement_status='?', selected_verified_programs=len(chosen), expected_programs=25,
                  primary_selection='highest verified complete attempt per label; all attempts retained in paths.tsv',
                  created_unique_paths=len(created), creators=distribution(creators), mutators=distribution(mutators),
                  shared_exactly_two=sum(len(s) == 2 for s in mutators.values()), shared_at_least_two=len(shared),
                  shared_more_than_two=sum(len(s) > 2 for s in mutators.values()),
                  outside_attributed_unique_paths=len(outside), outside_per_program={k: len(v) for k, v in sorted(program_outside.items())},
                  outside_observed_unique_paths=len(observed_outside),
                  outside_observed_per_program={k: len(v) for k, v in sorted(program_observed_outside.items())},
                  runs=summaries,
                  limitations=['Attribution is to run labels, not semantic program ownership.',
                               'Writable opens and MAP_SHARED writable mappings require snapshot mutation to enter primary statistics.',
                               'Snapshot signature detects metadata changes; transient files occur only in trace candidates.',
                               'CLONE_FS and successful explicit chroot/pivot_root are modeled; root-map evidence cites root-changing syscalls. Arbitrary mounts/setns and descriptor path escapes remain unsupported diagnostics.',
                               'Collection status requires external review of all 25 verifications, inventory errors and trace diagnostics.'])
    tsv(root / 'X9-paths.tsv', ['program', 'attempt', 'primary_run', 'path', 'action', 'type', 'attribution', 'creator_supported', 'convention', 'caller_directed', 'snapshot_evidence', 'trace_evidence'], rows)
    tsv(raw / 'shared.tsv', ['path', 'program_count', 'programs'], shared)
    tsv(raw / 'trace-candidates.tsv', ['program', 'attempt', 'primary_run', 'path', 'snapshot_mutation', 'creation_candidate', 'operations', 'trace_evidence'], candidate_rows)
    (raw / 'analysis.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('runs', 'limitations')}, indent=2))


def self_test(root):
    directory = root / 'raw-X9' / 'analyzer-test'
    directory.mkdir(parents=True, exist_ok=True)
    trace = directory / 'synthetic-trace.log'
    trace.write_text('''100 1.000001 chdir("/home/subject") = 0
100 1.000002 clone(child_stack=NULL, flags=SIGCHLD <unfinished ...>
101 1.000003 openat(AT_FDCWD, "new", O_WRONLY|O_CREAT, 0666) = 3</home/subject/new>
100 1.000004 <... clone resumed>) = 101
101 1.000005 renameat(AT_FDCWD, "new", AT_FDCWD, "final") = 0
101 1.000006 unlink("missing") = -1 ENOENT (No such file or directory)
101 1.000007 openat(AT_FDCWD, "read-only", O_RDONLY) = 4</home/subject/read-only>
101 1.000008 symlink("/arbitrary/target", "link") = 0
101 1.000009 write(3</home/subject/final>, "a", 1) = 1
101 1.000010 openat(5</tmp>, "x", O_RDWR|O_CREAT, 0600) = 6</tmp/x>
101 1.000011 write(6</tmp/x>, "b", 1 <unfinished ...>
101 1.000012 <... write resumed>) = 1
101 1.000013 openat(AT_FDCWD, "final", O_RDWR) = 7</home/subject/final>
''')
    paths, stats = parse_trace(trace, '/home/subject/work')
    assert set(paths) == {'/home/subject/new', '/home/subject/final', '/home/subject/link', '/tmp/x'}, paths
    assert next(e for e in paths['/tmp/x'] if e['operation'] == 'write')['line'] == 11
    assert next(e for e in paths['/home/subject/new'] if e['operation'] == 'openat')['creation_candidate']
    assert not next(e for e in paths['/home/subject/new'] if e['operation'] == 'renameat')['creation_candidate']
    assert next(e for e in paths['/home/subject/final'] if e['operation'] == 'renameat')['creation_candidate']
    assert not next(e for e in paths['/home/subject/final'] if e['operation'] == 'write')['creation_candidate']
    assert not next(e for e in paths['/home/subject/final'] if e['operation'] == 'openat')['creation_candidate']
    assert convention('/home/subject/.config/app', {'HOME': '/home/subject'}) == 'XDG_CONFIG_HOME'
    assert convention('/home/subject/.configuration', {}) == 'outside'
    assert convention('/root/.cache/app', {'HOME': '/home/subject'}) == 'outside'
    assert convention('/home/subject/.cache/app', {'HOME': '/root'}) == 'outside'
    assert convention('/root/.cache/app', {'HOME': '/root'}) == 'XDG_CACHE_HOME'
    assert convention('/run/user/1000/cache', {'XDG_RUNTIME_DIR': '/run/user/1000'}) == 'XDG_RUNTIME_DIR'
    namespace_trace = directory / 'synthetic-namespace-trace.log'
    namespace_trace.write_text('''200 1.000001 pivot_root("/var/lib/testroot", "/var/lib/testroot/old") = 0
200 1.000002 chdir("/") = 0
200 1.000003 openat(AT_FDCWD</>, "/bin/tool", O_CREAT|O_WRONLY, 0755) = 3</bin/tool>
200 1.000004 clone(child_stack=NULL, flags=SIGCHLD) = 201
201 1.000005 openat(AT_FDCWD</>, "child", O_CREAT|O_WRONLY, 0600) = 4</child>
200 1.000006 mount("tmpfs", "/opaque", "tmpfs", 0, NULL) = 0
200 1.000007 openat(AT_FDCWD</>, "/opaque/hidden", O_CREAT|O_WRONLY, 0600) = 5</opaque/hidden>
300 1.000008 openat(AT_FDCWD</>, "/bin/tool", O_CREAT|O_WRONLY, 0600) = 6</bin/tool>
300 1.000009 chroot("/var/lib/chroot") = 0
300 1.000010 chdir("/") = 0
300 1.000011 openat(AT_FDCWD</>, "/new", O_CREAT|O_WRONLY, 0600) = 7</new>
300 1.000012 chroot("/invalid") = -1 ENOENT (No such file or directory)
300 1.000013 write(7</new>, "a", 1) = 1
300 1.000014 exit(0) <unfinished ...>
''')
    mapped, namespace_stats = parse_trace(namespace_trace, '/')
    assert set(mapped) == {'/var/lib/testroot/bin/tool', '/var/lib/testroot/child', '/bin/tool', '/var/lib/chroot/new'}, mapped
    assert mapped['/var/lib/testroot/child'][0]['root_mapping'][0]['line'] == 1
    assert not mapped['/bin/tool'][0]['root_mapping']
    assert namespace_stats['unresolved_namespace_paths'] > 0
    assert namespace_stats['unfinished_syscalls_at_eof'] == {'exit': 1}
    assert namespace_stats['unfinished_nonexit_at_eof'] == 0
    numbered_trace = directory / 'synthetic-numbered-trace.log'
    numbered_trace.write_text('''400 1.000001 [ 257] openat(AT_FDCWD</>, "/numbered", O_CREAT|O_WRONLY, 0600) = 3</numbered>
400 1.000002 [   1] write(3</numbered>, "a", 1 <unfinished ...>
400 1.000003 [   1] <... write resumed>) = 1
401 1.000004 [ 999] ???( <unfinished ...>
402 1.000005 [   9] ???() = ?
''')
    numbered_paths, numbered_stats = parse_trace(numbered_trace, '/')
    assert set(numbered_paths) == {'/numbered'}
    assert numbered_paths['/numbered'][0]['syscall_number'] == 257
    assert numbered_paths['/numbered'][1]['syscall_number'] == 1
    assert numbered_paths['/numbered'][1]['line'] == 2
    assert numbered_paths['/numbered'][1]['end_line'] == 3
    assert numbered_stats['unfinished_syscalls_at_eof'] == {'unknown': 1}
    assert numbered_stats['unfinished_details'][0]['syscall_number'] == 999
    assert numbered_stats['unknown_syscall_count'] == 1
    assert numbered_stats['unknown_syscall_details'] == [{'pid': '402', 'line': 5, 'end_line': 5, 'syscall_number': 9, 'prefix': '???() = ?'}]
    assert numbered_stats['unparsed_lines'] == 1
    assert 'syscall_nr=257' in mapping_reference(numbered_paths['/numbered'][0], 'synthetic.log')
    fixture_root = directory / 'synthetic-analysis'
    x, y, z = '/home/subject/x', '/tmp/background', '/home/subject/.config/z'
    value = {'type': 'file', 'size': 1, 'mtime_ns': 1, 'ctime_ns': 1, 'mode': 33188, 'uid': 1000, 'gid': 1000}
    for number, label, before, after, traced in (
        (1, 'alpha', {}, {x: value, y: value}, [x]),
        (2, 'beta', {x: value, y: value}, {x: {**value, 'size': 2}, y: value, z: value}, [x, z]),
    ):
        run_dir = fixture_root / 'raw-X9' / 'guest' / 'runs' / f'{number:02d}-{label}'
        run_dir.mkdir(parents=True, exist_ok=True)
        for filename, paths in (('before', before), ('after', after)):
            with gzip.open(run_dir / f'{filename}.json.gz', 'wt') as stream:
                json.dump({'paths': paths, 'errors': []}, stream)
        (run_dir / 'run.json').write_text(json.dumps({'label': label, 'verified': True, 'attempt': 1, 'cwd': '/home/subject', 'environment': {'HOME': '/home/subject'}}))
        trace_text = ''.join(f'100 1.000001 openat(AT_FDCWD, "{p}", O_WRONLY|O_CREAT, 0600) = 3<{p}>\n' for p in traced)
        if label == 'alpha':
            # Background creation followed only by a traced chmod: mutator, not creator.
            trace_text += f'100 1.000002 chmod("{y}", 0600) = 0\n'
        (run_dir / 'trace.log').write_text(trace_text)
    analyze(fixture_root)
    measurement = json.loads((fixture_root / 'raw-X9' / 'analysis.json').read_text())
    assert measurement['created_unique_paths'] == 3
    assert measurement['creators']['exactly_one'] == 2
    assert measurement['creators']['zero'] == 1
    assert measurement['mutators']['exactly_one'] == 2
    assert measurement['mutators']['zero'] == 0
    assert measurement['mutators']['multiple'] == 1
    assert measurement['shared_exactly_two'] == 1
    with (fixture_root / 'X9-paths.tsv').open() as stream:
        y_row = next(row for row in csv.DictReader(stream, delimiter='\t') if row['path'] == y)
    assert y_row['attribution'] == 'trace-supported' and y_row['creator_supported'] == '0'
    (directory / 'result.json').write_text(json.dumps({'synthetic_only': True, 'passed': True, 'stats': stats}, indent=2) + '\n')
    print('Synthetic parser checks passed; no real measurements executed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--self-test', action='store_true')
    options = parser.parse_args()
    self_test(options.root) if options.self_test else analyze(options.root)

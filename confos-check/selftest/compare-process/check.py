#!/usr/bin/env python3
"""Checks of test.sh ([f7]): prints PASS/FAIL per check and RESULT; exit 0 only if every check passes.

check.py BASELINE_COMPARE_TSV DERIVED_COMPARE_TSV
"""
import sys


def rows(path):
    out = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            p = line.rstrip('\n').split('\t')
            out.append((p[0], p[1], p[2], p[3] if len(p) > 3 else ''))
    return out


def main():
    base = rows(sys.argv[1])
    with open(sys.argv[1][:-4] + '-excluded.tsv', encoding='utf-8') as f:
        excl = [line.rstrip('\n').split('\t') for line in f]
    der = rows(sys.argv[2])
    rep = {(r[1], r[2]) for r in base}
    G = '/usr/bin/cat#sha256=' + '9' * 64
    F = '/usr/bin/cat#sha256=' + 'f' * 64
    want = {('process', '/tmp/ns-planted'), ('process', '/usr/bin/tail'), ('process', G),
            ('port', 'tcp/0.0.0.0:7002'), ('unit', 'system/session-9.scope'), ('process', '/opt/unread'),
            ('process', '/usr/bin/sleep (deleted)')}
    ex = {(r[0], r[1]): '\t'.join(r) for r in excl}
    checks = [
        ('a: the process of the recorded application (path /app/bin/mpv, its file stored elsewhere) is placed '
         'by the checksum', ('process', '/app/bin/mpv') not in rep and
         'placed by the checksum' in ex.get(('process', '/app/bin/mpv'), '')),
        ('b1: a process whose file is no stored object is reported', ('process', '/tmp/ns-planted') in rep),
        ('b2: a process at a stored path whose file differs is not placed by the path',
         ('process', '/usr/bin/tail') in rep),
        ('a process at a stored path with the same file is placed by the path',
         ('process', '/usr/bin/sleep') not in rep and ('process', '/usr/bin/sleep') in ex),
        ('a process whose file could not be read is not placed by its path (only the reference could accept it)',
         ('process', '/opt/unread') in rep),
        ('a process whose executable was deleted is no stored object, even if its content equals one',
         ('process', '/usr/bin/sleep (deleted)') in rep),
        ('split object: the process with the stored file is placed, the other reported',
         ('process', F) not in rep and ('process', G) in rep),
        ('a port held by the recorded application is placed, one held by the unrecorded file reported',
         ('port', 'tcp/0.0.0.0:7001') not in rep and ('port', 'tcp/0.0.0.0:7002') in rep),
        ('a login scope is decided with the placement of its members',
         ('unit', 'system/session-8.scope') not in rep and ('unit', 'system/session-9.scope') in rep),
        ('nothing else is reported', rep == want),
        ('service line: the process that runs the stored file matches it',
         not any(r[1:3] == ('unit', 'service:sleeper') for r in der)),
        ('service line: a process at the path that runs another file does not match it (MISSING)',
         any(r[0] == 'MISSING' and r[1:3] == ('unit', 'service:tailer') for r in der)),
        ('service line: a process whose file could not be read is UNVERIFIED, never matched',
         any(r[0] == 'UNVERIFIED' and r[1:3] == ('unit', 'service:unreader') for r in der)),
    ]
    for r in base:
        print('reported: ' + '\t'.join(r)[:300])
    ok = True
    for name, c in checks:
        print(('PASS  ' if c else 'FAIL  ') + name)
        ok = ok and bool(c)
    print('RESULT: ' + ('PASS' if ok else 'FAIL'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())

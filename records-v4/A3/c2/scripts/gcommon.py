#!/usr/bin/env python3
"""Shared helpers for part-gaming (classification c2): package ownership through the merged-/usr aliases."""
import csv, json

NIGHT = '<HOME>/Projects/ideas/cal-paper/night-1123/'
IN = NIGHT + 'A3/in/'
RAW = IN + 'raw/gaming/'
csv.field_size_limit(10**9)
ALIASES = ['bin', 'sbin', 'lib', 'lib64']

_own = None
_pkg = None


def variants(p):
    v = [p]
    for a in ALIASES:
        if p.startswith('/usr/' + a + '/') or p == '/usr/' + a:
            v.append(p[4:])
        if p.startswith('/' + a + '/') or p == '/' + a:
            v.append('/usr' + p)
    return v


def packages():
    """object id -> (name, members dict)"""
    global _pkg
    if _pkg is None:
        _pkg = {}
        for x in csv.DictReader(open(RAW + 'objects.tsv'), delimiter='\t'):
            if x['kind'] == 'package':
                _pkg[x['id']] = (x['name'], json.loads(x['members']))
    return _pkg


def owner(p):
    """list of (package name, reason, integrity) for path p (through aliases), or []"""
    global _own
    if _own is None:
        pk = packages()
        _own = {}
        for x in csv.DictReader(open(RAW + 'package-files.tsv'), delimiter='\t'):
            n, m = pk.get(x['package'], (x['package'], {}))
            _own.setdefault(x['path'], []).append((n, m.get('reason', ''), x['integrity']))
    for v in variants(p):
        if v in _own:
            return _own[v]
    return []


def program_decision(exe):
    """Decision of an executable named by a runtime object."""
    o = owner(exe)
    if not o:
        return None
    n, reason, integ = o[0]
    if integ == 'unchanged':
        return '%s: file of %s, unchanged -> INSTALLED-PACKAGE' % (exe, n)
    return '%s: file of %s, integrity %s' % (exe, n, integ)


if __name__ == '__main__':
    import sys
    for a in sys.argv[1:]:
        a = a.replace('@', '/')
        print(a, owner(a))

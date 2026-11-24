#!/usr/bin/env python3
"""[n3-D]: are the components pinned by a release the latest on a given day?

lock-check.py --source confos-V-source.tar.gz --lock components/20261123T000000Z.txt --at 20261124T150000Z \
              --cache DIR [--out lock-check.tsv]

Reads the component lock (NAME=VERSION lines) from the published source archive of the release, resolves the newest
state of each archive of `derive` (debian, debian-security) at or before --at on snapshot.debian.org (the state that
the archive redirects that time to), and for every component prints the newest version of that name in the suites that
`derive` reads (trixie, trixie-updates, trixie-security) at that state. The indexes are read and checked with the
code of `derive` (its class Archive: the Release file's SHA256 of each Packages.xz). Output, tab-separated:
NAME  LOCKED  NEWEST  STATE   where STATE is `same`, `newer` (the archive has a newer version), `older`, or `absent`
(no such package in the suites, for example a component that the release ships itself). Last line: the counts.
Python 3 standard library only.
"""
import argparse
import importlib.machinery
import os
import sys
import tarfile
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))


def load_derive():
    return importlib.machinery.SourceFileLoader('cases_derive', os.path.join(HERE, '..', 'derive')).load_module()


def resolve(base, archive, at):
    """The timestamp of the newest state of ARCHIVE at or before AT (snapshot.debian.org redirects to it)."""
    url = f'{base}/archive/{archive}/{at}/'
    req = urllib.request.Request(url, headers={'User-Agent': 'lock-check/1'})
    with urllib.request.urlopen(req, timeout=120) as r:
        final = r.geturl()
    return final.rstrip('/').rsplit('/', 1)[-1], final


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', required=True)
    ap.add_argument('--lock', required=True, help='path of the lock inside the source archive')
    ap.add_argument('--at', required=True, help='a UTC time YYYYMMDDTHHMMSSZ')
    ap.add_argument('--cache', required=True)
    ap.add_argument('--out')
    ap.add_argument('--arch', default='amd64')
    a = ap.parse_args()
    d = load_derive()
    d.LOG = open((a.out or 'lock-check') + '.reads.jsonl', 'w')   # every fetch of derive, with its final URL
    with tarfile.open(a.source) as t:
        member = next((m for m in t.getmembers() if m.name.endswith('/' + a.lock) or m.name == a.lock), None)
        if member is None:
            print(f'lock-check: {a.lock} not in {a.source}', file=sys.stderr)
            return 2
        text = t.extractfile(member).read().decode()
    lock = []
    for raw in text.splitlines():
        raw = raw.strip()
        if raw and not raw.startswith('#') and '=' in raw:
            n, _, v = raw.partition('=')
            lock.append((n, v))
    states = {}
    for archive in sorted({x for x, _ in d.SUITES}):
        ts, final = resolve(d.SNAPSHOT, archive, a.at)
        states[archive] = ts
        print(f'# {archive}: newest state at or before {a.at}: {ts} ({final})', file=sys.stderr)
    tables = []
    for archive, suite in d.SUITES:
        arc = d.Archive(a.cache, states[archive], a.arch)
        tables.append(arc.index(archive, suite) or {})
    rows, counts = [], {}
    for name, ver in lock:
        cands = [st.get('Version') for t in tables for st in t.get(name, [])
                 if st.get('Architecture') in (a.arch, 'all')]
        if not cands:
            newest, state = '-', 'absent'
        else:
            newest = cands[0]
            for c in cands[1:]:
                if d.vercmp(c, newest) > 0:
                    newest = c
            cmp = d.vercmp(newest, ver)
            state = 'same' if cmp == 0 else 'newer' if cmp > 0 else 'older'
        counts[state] = counts.get(state, 0) + 1
        rows.append(f'{name}\t{ver}\t{newest}\t{state}')
    out = '\n'.join(rows) + '\n' + f'# {len(lock)} components; ' + ', '.join(
        f'{k} {v}' for k, v in sorted(counts.items())) + '; states ' + ', '.join(
        f'{k} {v}' for k, v in sorted(states.items())) + '\n'
    if a.out:
        with open(a.out, 'w') as f:
            f.write(out)
    sys.stdout.write(out)
    return 0


if __name__ == '__main__':
    sys.exit(main())

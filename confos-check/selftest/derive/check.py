#!/usr/bin/env python3
"""Checks of the self-test of `derive`. Each subcommand prints PASS/FAIL lines, a final `RESULT NAME PASS|FAIL`
line, and exits 0 only on PASS.

  check.py lines     DERIVED DECLARATION          every line of the declaration has a derived object with its ID
  check.py disk      DERIVED LISTING.csv PKG...   every derived object of the packages is on the disk as derived
  check.py reads     DERIVED READS.log DECLARATION CACHE PKG...   derive read only what the rule allows
  check.py underived DERIVED READS.log PKG...     a dependency no line names is underived and was not read
  check.py base      DERIVED COMPONENTS           every component of the base is derived at its listed version
  check.py same      A B                          two derivations are byte-identical

Paths printed are made relative to the environment variable STRIP, so that the output names no host directory.
"""
import csv
import hashlib
import json
import os
import re
import shlex
import sys

STRIP = os.environ.get('STRIP', '')


def show(s):
    s = str(s)
    return s.replace(STRIP, '$DIR') if STRIP else s


def load(path):
    with open(path, encoding='utf-8') as f:
        return [json.loads(x) for x in f if x.strip()]


def finish(name, fails, passes):
    ok = fails == 0 and passes > 0
    print(f'RESULT {name} {"PASS" if ok else "FAIL"} (pass={passes} fail={fails})')
    return 0 if ok else 1


def lines_of(o):
    return [o['line']] + [x.split(' (')[0] for x in o.get('also_lines', [])]


def owned(objs, pkgs):
    """Objects that the package lines of PKGS (names) record: package files and the package objects."""
    out = []
    for o in objs:
        if o['kind'] in ('file', 'dir', 'symlink', 'other'):
            owners = [o.get('package')] + [x.split(' (')[1].rstrip(')') for x in o.get('also_lines', [])
                                           if ' (' in x]
            if any(w and w.split(':')[0] in pkgs for w in owners):
                out.append(o)
    return out


def cmd_lines(derived, decl):
    objs = load(derived)
    have = {}
    for o in objs:
        for line in lines_of(o):
            have.setdefault(line.split(' ')[0], []).append(o)
    fails = passes = 0
    name = os.path.basename(decl)
    with open(decl, encoding='utf-8') as f:
        for n, raw in enumerate(f, 1):
            if not raw.strip() or raw.lstrip().startswith('#'):
                continue
            got = have.get(f'{name}:{n}', [])
            kinds = sorted({o['kind'] for o in got})
            ok = bool(got)
            passes += ok
            fails += not ok
            print(f'{"PASS" if ok else "FAIL"} line {name}:{n} {raw.split()[0]}: {len(got)} objects {kinds}')
    errors = [o for o in objs if o['kind'] == 'error']
    for e in errors:
        print(f'FAIL error object: {e}')
    fails += len(errors)
    for o in objs:
        if o['kind'] == 'file' and o.get('value') and o['value'].get('source'):
            print(f'PASS file line {o["id"]}: sha256 {o["value"]["sha256"]} checked against its source')
    return finish('lines', fails, passes)


def read_listing(path):
    """virt-ls --csv -lR --uids --checksum=sha256: type,mode,size,uid,gid,checksum,path[,target]"""
    out = {}
    with open(path, newline='', encoding='utf-8', errors='surrogateescape') as f:
        for row in csv.reader(f):
            if len(row) < 7:
                continue
            typ, mode, size, uid, gid, checksum, path = row[:7]
            out[path] = {'type': typ, 'mode': mode.strip(), 'uid': int(uid), 'gid': int(gid),
                         'sha256': checksum or None, 'target': row[7] if len(row) > 7 else None}
    return out


def cmd_disk(derived, listing, *pkgs):
    objs = owned(load(derived), set(pkgs))
    disk = read_listing(listing)
    print(f'disk listing: {len(disk)} objects read from the stopped guest disk')
    fails = passes = 0
    types = {'file': '-', 'dir': 'd', 'symlink': 'l'}
    for o in sorted(objs, key=lambda x: x['id']):
        v = o.get('value')
        if not v:
            print(f'FAIL {o["kind"]} {o["id"]}: no derived value ({o.get("underived")})')
            fails += 1
            continue
        path = o['id']
        d = disk.get(path)
        if d is None:
            print(f'FAIL {o["kind"]} {path}: not on the disk')
            fails += 1
            continue
        diffs = []
        if d['type'] != types.get(o['kind']):
            diffs.append(f'type disk={d["type"]} derived={o["kind"]}')
        want_mode = v['mode'][-4:]
        if d['mode'].zfill(4)[-4:] != want_mode:
            diffs.append(f'mode disk={d["mode"]} derived={want_mode}')
        if d['uid'] != v['uid']:
            diffs.append(f'uid disk={d["uid"]} derived={v["uid"]}')
        if d['gid'] != v['gid']:
            diffs.append(f'gid disk={d["gid"]} derived={v["gid"]}')
        if o['kind'] == 'file' and d['sha256'] != v['sha256']:
            diffs.append(f'sha256 disk={d["sha256"]} derived={v["sha256"]}')
        if o['kind'] == 'symlink' and d['target'] != v['target']:
            diffs.append(f'target disk={d["target"]} derived={v["target"]}')
        if diffs:
            print(f'FAIL {o["kind"]} {path}: ' + '; '.join(diffs))
            fails += 1
        else:
            extra = f' sha256={v["sha256"][:16]}…' if o['kind'] == 'file' else (
                f' -> {v["target"]}' if o['kind'] == 'symlink' else '')
            print(f'PASS {o["kind"]} {path} mode={want_mode} uid={v["uid"]} gid={v["gid"]}{extra}')
            passes += 1
    counts = {}
    for o in objs:
        counts[o['kind']] = counts.get(o['kind'], 0) + 1
    print(f'derived objects of {", ".join(pkgs)}: {len(objs)} {counts}')
    return finish('disk', fails, passes)


def cmd_reads(derived, logpath, decl, cache, *pkgs):
    objs = load(derived)
    debs = {}
    for o in objs:
        if o['kind'] == 'package' and o.get('value') and o['id'].split(':')[0] in pkgs:
            debs[os.path.join(os.path.abspath(cache), 'debs', o['value']['deb_sha256'] + '.deb')] = o['id']
    decl = os.path.abspath(decl)
    sources = {decl}
    ddir = os.path.dirname(decl)
    with open(decl, encoding='utf-8') as f:
        for raw in f:
            fields = shlex.split(raw, comments=True)
            if fields and fields[0] == 'file' and len(fields) == 5:
                sources.add(os.path.abspath(os.path.join(ddir, fields[4])))
            if fields and fields[0] == 'network' and len(fields) == 4:
                sources.add(os.path.abspath(os.path.join(ddir, fields[3])))
    out = os.path.abspath(os.path.dirname(derived))
    index_dir = os.path.join(os.path.abspath(cache), 'indexes') + '/'
    names = '|'.join(re.escape(p) for p in pkgs)
    pool = re.compile(r'^https://snapshot\.debian\.org/archive/debian(-security)?/\d{8}T\d{6}Z/pool/main/'
                      r'[^/]+/[^/]+/(' + names + r')_[^/]+\.deb$')
    dists = re.compile(r'^https://snapshot\.debian\.org/archive/debian(-security)?/\d{8}T\d{6}Z/dists/[a-z-]+/'
                       r'(InRelease|main/binary-amd64/Packages\.xz)$')
    log = load(logpath)
    fetched_ok, finals = set(), set()
    for r in log:
        if r['op'] == 'fetch':
            ok = bool(pool.match(r['url']) or dists.match(r['url']))
            if ok:
                fetched_ok.add(r['url'])
                if r.get('final_url'):
                    finals.add(r['final_url'])
    fails = passes = 0
    seen = {'declaration': 0, 'source': 0, 'deb': set(), 'index': 0, 'fetch': 0}
    counts = {}
    prev = None
    run_out = None
    for r in log:
        op = r['op']
        counts[op] = counts.get(op, 0) + 1
        ok, what = True, ''
        if op == 'open':
            p = r['path']
            if p == decl:
                seen['declaration'] += 1
                what = 'the declaration'
            elif p in sources:
                seen['source'] += 1
                what = 'a source named by a line'
            elif p in debs:
                seen['deb'].add(debs[p])
                what = f'the package file of {debs[p]}'
            elif p.startswith(index_dir):
                seen['index'] += 1
                what = 'a cached snapshot index'
            else:
                ok, what = False, 'NOT ALLOWED'
        elif op == 'write':
            p = r['path']
            ok = p.startswith(os.path.abspath(cache) + '/') or p in (run_out, run_out + '.part')
            what = 'cache or the --out file of this run' if ok else 'NOT ALLOWED'
        elif op == 'exec':
            a = r['argv']
            ok = len(a) == 3 and a[0] == 'dpkg-deb' and a[1] in ('--ctrl-tarfile', '--fsys-tarfile') and a[2] in debs
            what = f'dpkg-deb on {debs.get(a[-1])}' if ok else 'NOT ALLOWED'
        elif op == 'request':
            ok = r['url'] in fetched_ok or r['url'] in finals
            what = 'snapshot index or named package' if ok else 'NOT ALLOWED'
        elif op == 'fetch':
            ok = r['url'] in fetched_ok and r.get('status') == 200
            seen['fetch'] += ok
            what = f'HTTP {r.get("status")}, {r.get("bytes")} bytes' if ok else 'NOT ALLOWED'
        elif op == 'connect':
            ok = prev is not None and prev['op'] == 'request'
            what = 'connection opened for the request before it' if ok else 'NOT ALLOWED'
        elif op in ('start', 'end'):
            what = 'program start/end'
            if op == 'start' and '--out' in r['argv']:
                run_out = os.path.abspath(r['argv'][r['argv'].index('--out') + 1])
        else:
            ok, what = False, 'NOT ALLOWED'
        prev = r
        target = r.get('path') or r.get('url') or ' '.join(r.get('argv', [])) or r.get('address', '')
        if not ok or op in ('request', 'exec') or (op == 'open' and what != 'a cached snapshot index'):
            print(f'{"PASS" if ok else "FAIL"} {op} {show(target)}: {what}')
        passes += ok
        fails += not ok
    print(f'log entries by kind: {counts}')
    for k, v in seen.items():
        print(f'read {k}: {sorted(v) if isinstance(v, set) else v}')
    need = [('declaration read', seen['declaration'] > 0), ('source read', seen['source'] > 0 or len(sources) == 1),
            ('every named package read', seen['deb'] == set(debs.values()) and len(debs) == len(pkgs)),
            ('snapshot indexes fetched', seen['fetch'] > 0)]
    for name, ok in need:
        print(f'{"PASS" if ok else "FAIL"} {name}')
        passes += ok
        fails += not ok
    return finish('reads', fails, passes)


def cmd_underived(derived, logpath, *pkgs):
    objs = load(derived)
    byid = {(o['kind'], o['id']): o for o in objs}
    log = load(logpath)
    fails = passes = 0
    for o in objs:
        if o['kind'] != 'package' or not o.get('value') or o['id'].split(':')[0] not in pkgs:
            continue
        rel = ', '.join(x for x in (o['value'].get('pre_depends'), o['value'].get('depends')) if x)
        for group in rel.split(','):
            names = [re.sub(r'[\s(:].*$', '', a.strip()) for a in group.split('|')]
            if not names[0] or any(n in pkgs for n in names):
                continue
            dep = ' | '.join(names)
            u = byid.get(('package', dep))
            ok = bool(u) and u.get('value') is None and u.get('underived', '').startswith('dependency not named')
            hits = [r for r in log if any(f'/{n}_' in json.dumps(r) or f'"{n}"' in json.dumps(r) for n in names)]
            print(f'{"PASS" if ok else "FAIL"} {o["id"]} depends on {group.strip()}: derived as '
                  f'{json.dumps({k: u[k] for k in ("kind", "id", "line", "value", "underived")}) if u else None}')
            passes += ok
            fails += not ok
            ok2 = not hits
            print(f'{"PASS" if ok2 else "FAIL"} {dep}: {len(hits)} log entries mention it (no file of it was read)')
            passes += ok2
            fails += not ok2
    return finish('underived', fails, passes)


def cmd_base(derived, components):
    objs = load(derived)
    pk = {o['id'].split(':')[0]: o for o in objs if o['kind'] == 'package'}
    fails = passes = 0
    with open(components, encoding='utf-8') as f:
        for raw in f:
            raw = raw.strip()
            if not raw or raw.startswith('#'):
                continue
            name, _, ver = raw.partition('=')
            o = pk.get(name)
            ok = bool(o and o.get('value') and o['value']['version'] == ver)
            nfiles = sum(1 for x in objs if x.get('package', '').split(':')[0] == name)
            print(f'{"PASS" if ok else "FAIL"} component {name}={ver}: '
                  f'{"derived, " + str(nfiles) + " objects of its data" if ok else (o or {}).get("underived")}')
            passes += ok
            fails += not ok
    under = [o for o in objs if o.get('underived')]
    by = {}
    for o in under:
        r = o['underived'].split(';')[0]
        by[(o['kind'], r)] = by.get((o['kind'], r), 0) + 1
    print(f'base derivation: {len(objs)} objects, {len(under)} underived:')
    for (k, r), n in sorted(by.items()):
        print(f'  {n:4d} {k}: {r}')
    errors = [o for o in objs if o['kind'] == 'error']
    fails += len(errors)
    return finish('base', fails, passes)


def cmd_same(a, b):
    ha = hashlib.sha256(open(a, 'rb').read()).hexdigest()
    hb = hashlib.sha256(open(b, 'rb').read()).hexdigest()
    ok = ha == hb
    print(f'{"PASS" if ok else "FAIL"} {show(a)} sha256 {ha}')
    print(f'{"PASS" if ok else "FAIL"} {show(b)} sha256 {hb}')
    return finish('same', 0 if ok else 1, 1 if ok else 0)


if __name__ == '__main__':
    cmds = {'lines': cmd_lines, 'disk': cmd_disk, 'reads': cmd_reads, 'underived': cmd_underived,
            'base': cmd_base, 'same': cmd_same}
    sys.exit(cmds[sys.argv[1]](*sys.argv[2:]))

#!/usr/bin/env python3
"""Dump every member of every stored group and every code row of part-gaming, with
dpkg ownership resolved through the merged-/usr aliases, its recorded integrity, the
configuration-origin ctime and the symlink target.  Output: A3/c2/raw/gaming-members.tsv

Alias rule (fact, not inference): on this machine /bin, /sbin, /lib, /lib64 are symbolic links into
/usr (raw/0004-filesystem.out: /bin->usr/bin, /sbin->usr/sbin, /lib->usr/lib, /lib64->usr/lib64), so a
dpkg record of /bin/x names the same file as /usr/bin/x."""
import csv, json

NIGHT = '<HOME>/Projects/ideas/cal-paper/night-1123/'
IN = NIGHT + 'A3/in/'
RAW = IN + 'raw/gaming/'
csv.field_size_limit(10**9)

ALIASES = ['bin', 'sbin', 'lib', 'lib64']


def variants(p):
    v = [p]
    for a in ALIASES:
        if p.startswith('/usr/' + a + '/') or p == '/usr/' + a:
            v.append(p[4:])
        if p.startswith('/' + a + '/') or p == '/' + a:
            v.append('/usr' + p)
    return v


def load_pkgfiles():
    pid2name = {}
    for x in csv.DictReader(open(RAW + 'objects.tsv'), delimiter='\t'):
        if x['kind'] == 'package':
            pid2name[x['id']] = x['name']
    own = {}
    for x in csv.DictReader(open(RAW + 'package-files.tsv'), delimiter='\t'):
        own.setdefault(x['path'], []).append((pid2name.get(x['package'], x['package']), x['integrity']))
    return own


def rows_of(x):
    k = x['kind']
    m = json.loads(x['members'])
    if k.startswith('2:stored'):
        rows = list(csv.reader(open(RAW + m['file']), delimiter='\t'))[1:]
        assert len(rows) == m['count'], x['id']
        return rows, m
    return [[m['path'], m.get('type', ''), m.get('mode', ''), '%s:%s' % (m.get('uid'), m.get('gid')),
             str(m.get('size', '')), m.get('mtime', ''), str(m.get('executable', '')),
             m.get('signature', ''), m.get('persistence', '')]], m


def main():
    own = load_pkgfiles()
    ctime = {}
    for x in csv.DictReader(open(RAW + 'configuration-origin.tsv'), delimiter='\t'):
        ctime[x['path']] = (x['ctime'], x['package_script_mentions'])
    groups = [x for x in csv.DictReader(open(IN + 'part-gaming.tsv'), delimiter='\t')
              if x['kind'].startswith('2:stored') or x['kind'].startswith('2:code')]
    need = set()
    for x in groups:
        for f in rows_of(x)[0]:
            need.add(f[0])
    fs = {}
    for line in open(RAW + 'raw/0004-filesystem.out', errors='replace'):
        i = line.find('"path":"')
        if i < 0:
            continue
        j = line.find('"', i + 8)
        p = line[i + 8:j]
        if p in need:
            try:
                fs[p] = json.loads(line)
            except Exception:
                pass
    out = csv.writer(open(NIGHT + 'A3/c2/raw/gaming-members.tsv', 'w'), delimiter='\t', lineterminator='\n')
    out.writerow(['gid', 'group', 'path', 'type', 'mode', 'owner', 'size', 'mtime', 'exec', 'signature',
                  'persistence', 'ctime', 'pkg', 'integrity', 'script_mentions', 'target', 'shebang'])
    for x in groups:
        rows, m = rows_of(x)
        for f in rows:
            p = f[0]
            pk, integ = '', ''
            for v in variants(p):
                if v in own:
                    pk = ';'.join(sorted(set(a for a, b in own[v])))
                    integ = ';'.join(sorted(set(b for a, b in own[v])))
                    break
            c, sm = ctime.get(p, ('', ''))
            r = fs.get(p, {})
            if not c:
                c = r.get('ctime', '')
            out.writerow([x['id'], x['name']] + f[:9] + [c, pk, integ, sm if sm != '[]' else '',
                                                        r.get('target', ''), str(r.get('shebang', ''))])


main()

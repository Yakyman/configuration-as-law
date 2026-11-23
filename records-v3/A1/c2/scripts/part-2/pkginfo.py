"""Run on the server: for each package name in names.txt, print the Debian description and
counts of code-like files from Contents-amd64 (bookworm main)."""
import re, sys, gzip
names = [l.strip().split(':')[0] for l in open('names.txt') if l.strip()]
want = set(names)
desc = {}
cur = None; buf = []; field = None
for line in open('Packages', encoding='utf-8', errors='replace'):
    if line.startswith('Package: '):
        cur = line[9:].strip(); buf = []; field = None
    elif line.startswith('Description: ') and cur in want and cur not in desc:
        buf = [line[13:].strip()]; field = 'd'
    elif field == 'd' and line.startswith(' '):
        buf.append(line.strip())
    elif field == 'd':
        desc[cur] = ' '.join(buf)[:700]; field = None
pat = {
    'bin': re.compile(r'^(usr/)?s?bin/'),
    'lib_so': re.compile(r'\.so(\.\d+)*$'),
    'libexec': re.compile(r'^usr/(lib|libexec)/.*/(?!.*\.)[^/]+$'),
    'py': re.compile(r'\.py$'),
    'pm': re.compile(r'\.pm$'),
    'ko': re.compile(r'\.ko(\.xz|\.zst)?$'),
    'vmlinuz': re.compile(r'^boot/vmlinuz'),
    'efi': re.compile(r'\.(efi|mod)(\.signed)?$'),
    'unit': re.compile(r'systemd/system/[^/]+\.(service|socket|timer|target|mount|path)$'),
    'etc': re.compile(r'^etc/'),
    'doc': re.compile(r'^usr/share/(doc|man|info)/'),
}
cnt = {n: {k: 0 for k in pat} for n in want}
tot = {n: 0 for n in want}
ex = {n: [] for n in want}
for fn in ('Contents-amd64.gz', 'Contents-all.gz'):
  with gzip.open(fn, 'rt', encoding='utf-8', errors='replace') as f:
    for line in f:
        m = line.rstrip('\n').rsplit(None, 1)
        if len(m) != 2:
            continue
        path, pkgs = m
        for p in pkgs.split(','):
            n = p.split('/')[-1]
            if n in want:
                tot[n] += 1
                for k, r in pat.items():
                    if r.search(path):
                        cnt[n][k] += 1
                if len(ex[n]) < 4 and not pat['doc'].search(path):
                    ex[n].append(path)
for n in names:
    c = ' '.join('%s=%d' % (k, v) for k, v in cnt[n].items() if v)
    print('\t'.join([n, str(tot[n]), c, ' | '.join(ex[n]), desc.get(n, 'NO-DESCRIPTION')]))

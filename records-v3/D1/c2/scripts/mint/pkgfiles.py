#!/usr/bin/env python3
"""Per-package file classes from public archive indexes (Ubuntu noble + Linux Mint zena).
Usage: pkgfiles.py <workdir>  ; writes pkgclass.tsv and pkgfiles.tsv.gz into workdir."""
import sys, os, gzip, lzma, re, json
wd = sys.argv[1]
pk = {}
for line in open(os.path.join(wd, 'pkgs.tsv')):
    n, v, s = line.rstrip('\n').split('\t')
    pk[n.split(':')[0]] = v
want = set(pk)
files = {n: set() for n in want}
srcs = {n: set() for n in want}
def contents(path, tag):
    with gzip.open(path, 'rt', errors='replace') as f:
        for line in f:
            line = line.rstrip('\n')
            m = re.match(r'^(.*\S)\s+(\S+)$', line)
            if not m: continue
            p, locs = m.group(1), m.group(2)
            for loc in locs.split(','):
                name = loc.rsplit('/', 1)[-1]
                if name in want:
                    files[name].add(p); srcs[name].add(tag)
for fn in sorted(os.listdir(wd)):
    if fn.startswith('Contents-') or fn.endswith('-Contents.gz'):
        contents(os.path.join(wd, fn), fn)
meta = {}
def packages(path, opener, tag):
    with opener(path, 'rt', errors='replace') as f:
        rec = {}
        for line in f.read().split('\n\n'):
            d = {}; key = None
            for l in line.split('\n'):
                if l.startswith((' ', '\t')) and key: d[key] += '\n' + l; continue
                if ':' in l:
                    key, val = l.split(':', 1); d[key] = val.strip()
            n = d.get('Package')
            if n in want:
                exact = d.get('Version') == pk[n]
                old = meta.get(n)
                if old is None or (exact and not old['exact']):
                    meta[n] = {'exact': exact, 'repo': tag, 'version': d.get('Version'),
                               'desc': d.get('Description', '').split('\n')[0],
                               'section': d.get('Section', ''), 'depends': d.get('Depends', ''),
                               'source': d.get('Source', n)}
for fn in sorted(os.listdir(wd)):
    if fn.endswith('Packages.xz'): packages(os.path.join(wd, fn), lzma.open, fn)
    elif fn.endswith('Packages.gz'): packages(os.path.join(wd, fn), gzip.open, fn)
CODE = [r'^(usr/)?s?bin/', r'^usr/games/', r'^usr/libexec/', r'\.so(\.[0-9.]+)?$', r'\.ko(\.(zst|xz|gz))?$',
        r'^(usr/)?lib/firmware/', r'^(usr/)?lib/systemd/', r'^etc/systemd/', r'^etc/init\.d/', r'^etc/cron', r'^(usr/)?lib/udev/',
        r'^etc/udev/', r'^etc/pam\.d/', r'^usr/share/polkit-1/rules\.d/', r'^etc/polkit-1/', r'^etc/profile\.d/', r'^etc/X11/Xsession\.d/',
        r'\.(py|pl|pm|rb|sh|lua|jar|js|pyc|tcl|bash)$', r'^usr/lib/python3/', r'^usr/lib/python3\.\d+/', r'^usr/share/perl5?/', r'^usr/lib/x86_64-linux-gnu/perl',
        r'\.typelib$', r'^usr/lib/x86_64-linux-gnu/.*\.(so|a)', r'^usr/share/dbus-1/(system-)?services/', r'^etc/xdg/autostart/', r'^etc/sudoers',
        r'^etc/apparmor\.d/', r'^usr/share/gnome-shell/', r'^usr/share/cinnamon/', r'^(usr/)?lib/modules/', r'^boot/', r'^usr/lib/grub/', r'^etc/grub\.d/',
        r'^usr/share/dbus-1/system\.d/', r'^etc/dbus-1/', r'^etc/modprobe\.d/', r'^(usr/)?lib/modprobe\.d/', r'^etc/sysctl\.d/', r'^usr/lib/sysctl\.d/',
        r'^usr/lib/tmpfiles\.d/', r'^usr/lib/sysusers\.d/', r'^etc/network/', r'^etc/NetworkManager/', r'^usr/lib/NetworkManager/', r'^usr/share/applications/', r'^etc/apt/', r'^usr/share/keyrings/', r'^etc/ssl/', r'^usr/share/ca-certificates/', r'^usr/share/zoneinfo/']
CRE = [re.compile(x) for x in CODE]
DOC = re.compile(r'^usr/share/(doc|doc-base|man|info|help|gtk-doc|lintian|bug)/')
CLS = [('locale', r'^usr/share/(locale|locale-langpack)/'), ('font', r'^(usr/share/fonts|etc/fonts|usr/share/fontconfig)/'),
       ('icon', r'^usr/share/(icons|pixmaps)/'), ('theme', r'^usr/share/themes/'), ('background', r'^usr/share/(backgrounds|wallpapers)/'),
       ('sound', r'^usr/share/sounds/')]
CLS = [(a, re.compile(b)) for a, b in CLS]
with open(os.path.join(wd, 'pkgclass.tsv'), 'w') as out, gzip.open(os.path.join(wd, 'pkgfiles.tsv.gz'), 'wt') as fo:
    out.write('pkg\tversion\tfound_files\tn_files\tn_code\tn_doc\tdata_classes\tcode_example\trepo\texact\tsection\tdesc\n')
    for n in sorted(want):
        fs = sorted(files[n]); m = meta.get(n, {})
        code = [p for p in fs if any(r.search(p) for r in CRE)]
        doc = [p for p in fs if DOC.search(p)]
        rest = [p for p in fs if p not in code and p not in doc]
        dc = {}
        for p in rest:
            c = next((a for a, r in CLS if r.search(p)), 'other')
            dc[c] = dc.get(c, 0) + 1
        out.write('\t'.join([n, pk[n], 'yes' if fs else 'no', str(len(fs)), str(len(code)), str(len(doc)),
                             ','.join(f'{k}:{v}' for k, v in sorted(dc.items())), code[0] if code else '',
                             m.get('repo', ''), str(m.get('exact', '')), m.get('section', ''), m.get('desc', '').replace('\t', ' ')]) + '\n')
        for p in fs: fo.write(f'{n}\t{p}\n')

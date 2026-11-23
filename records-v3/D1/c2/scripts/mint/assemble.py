#!/usr/bin/env python3
"""Assemble D1/c2/part-mint.tsv from rules and hand tables. Run from D1/c2."""
import csv, gzip, json, re, sys
from collections import defaultdict
IN = '../in/part-mint.tsv'
rows = list(csv.DictReader(open(IN, encoding='utf-8'), delimiter='\t'))
cls = {x['pkg']: x for x in csv.DictReader(open('raw/mint/pkgclass.tsv'), delimiter='\t')}
files = defaultdict(list)
for l in gzip.open('raw/mint/pkgfiles.tsv.gz', 'rt'):
    n, p = l.rstrip('\n').split('\t', 1); files[n].append(p)
STRONG = re.compile(r'^(usr/)?s?bin/|^usr/games/|^usr/libexec/|\.so(\.[0-9.]+)?$|\.ko(\.(zst|xz|gz))?$|^(usr/)?lib/firmware/|^(usr/)?lib/modules/|\.(py|pl|pm|rb|sh|lua|jar|pyc|tcl|bash)$|^usr/lib/python3|^usr/share/perl|^(usr/)?lib/systemd/|^etc/init\.d/|^boot/|^usr/lib/grub/')
DOC = re.compile(r'^usr/share/(doc|doc-base|man|info|help|gtk-doc|lintian|bug)/')
def contents_url(repo):
    if repo.startswith('mint-'):
        return 'doc:http://packages.linuxmint.com/dists/zena/%s/Contents-amd64.gz' % repo.split('-')[1]
    m = re.match(r'ub-(noble(?:-updates|-security)?)-', repo)
    return 'doc:http://archive.ubuntu.com/ubuntu/dists/%s/Contents-amd64.gz' % m.group(1)
GSET = 'doc:https://docs.gtk.org/gio/ctor.Settings.new.html'
GIDOC = 'doc:https://gi.readthedocs.io/en/latest/'
T = {
 'CODE': ('MUST', 'S2.2-1,S2.2-2,S2.2-9,S2.2-10', 'Ships executable code run on the computer or by its programs with their rights; removing it makes that function impossible.'),
 'XCODE': ('MUST', 'S2.2-10,S2.2-13,S2.2-2', 'Holds files executed as code (shell fragment, crontab lines or scripts) with the executing program\'s rights; S2.2-13 counts them as code, S2.2-10 requires recording.'),
 'GIR': ('MUST', 'S2.2-1,S2.2-2,S2.2-13', 'Typelib read as values (setting) by any GObject-introspection program, not one program; removal makes programs importing this namespace fail.'),
 'SCHEMA': ('MUST', 'S2.2-1,S2.2-2,S2.2-13', 'Settings schemas read by several programs; GLib treats a missing schema as an error stopping the requesting program, so removal makes them fail.'),
 'FUNC': ('MUST', 'S2.2-1,S2.2-2,S2.2-13', 'Values read by several programs or the system, not one program (S2.2-13); removal makes {X} impossible (S2.2-2).'),
 'DB': ('HOLE', 'S2.2-2,S2.2-4,S2.2-13', 'Called a database: S2.2-4 exempts database contents, but programs read it as values (S2.2-13) and removal stops {X} (S2.2-2); no precedence.'),
 'APPEAR': ('HOLE', 'S2.2-1,S2.2-7,S2.2-13', 'Presentation data shared by many programs; removal changes only look, sound or language. S2.2-7 exempts such settings only inside one program; whether appearance is behaviour is undecided.'),
 'ONEPROG': ('NOT', 'S2.2-7,S2.2-13', 'Values read by one program only (setting, S2.2-13) that change its look, language or defaults; S2.2-7 exempts settings in force only inside one program.'),
 'EXT': ('NOT', 'S2.2-7', 'Language packs installed as extensions of one program; S2.2-7 names extensions of a web browser among settings in force only inside one program.'),
 'ONEFUNC': ('HOLE', 'S2.2-2,S2.2-7,S2.2-13', 'Data read only by one program (setting, S2.2-13) that it needs to work: S2.2-7 exempts it, S2.2-2 requires it; no sentence says which prevails.'),
 'DOC': ('NOT', 'S2.2-4', 'Documentation only; documents are content: after removal the computer does and can do the same, only the documents are unavailable.'),
 'PHOTO': ('NOT', 'S2.2-4', 'Photographs are content: after removal the computer does and can do the same; only the pictures are unavailable.'),
 'DBG': ('HOLE', 'S2.2-2,S2.2-4', 'Removal makes symbolic debugging impossible (S2.2-2), yet only the data itself becomes unavailable, as S2.2-4 says of content; content is defined only by examples.'),
 'META': ('HOLE', 'S2.2-1,S2.2-2', 'Removal stops nothing now; later package-manager runs would autoremove or stop upgrading its dependencies. Text does not say whether that counts as behaviour.'),
 'EMPTY': ('NOT', 'S2.2-1,S2.2-2', 'No working file and no dependencies: after removal the computer does and can do the same, so its behaviour does not depend on it.'),
 'WEB': ('NOT', 'S2.2-11', 'Pages and JavaScript run inside a web browser page; S2.2-11: code the program confines to its interface, such as a web page, need not be recorded.'),
 'TRUST': ('MUST', 'S2.2-1,S2.2-2,S2.2-13', 'apt reads these keys as values to verify repository signatures; removal makes installing and updating from the signed repository impossible.'),
 'RIGHTS': ('MUST', 'S2.2-1,S2.2-10,S2.2-13', 'polkit .rules files are JavaScript run by polkitd (code, S2.2-13) and grant users actions; what users can do depends on them.'),
 'UNK': ('UNKNOWN', 'S3-1,S3-2', '{X}'),
}
hand = {}
for line in open('work/mint/hand-packages.tsv', encoding='utf-8'):
    f = line.rstrip('\n').split('\t')
    hand[f[0]] = f[1:]
hgroups = {}
for line in open('work/mint/hand-groups.tsv', encoding='utf-8'):
    f = line.rstrip('\n').split('\t'); hgroups[f[0]] = f[1:]
out = []; rulelog = defaultdict(list)
def words(s): return len(s.split())
for r in rows:
    i, kind, name = r['id'], r['kind'], r['name']
    if kind == 'L1:account':
        dec, sen, what, basis, reason = 'MUST', 'S2.2-15', 'System account %s (%s)' % (name, json.loads(r['members'])[0].split(':')[-1]), 'evidence', 'S2.2-15 states accounts must be recorded; this row is an existing account in the account database.'
        what = 'Account %s in the account database, login shell %s' % (name, json.loads(r['members'])[0].split(':')[-1])
        rulelog['R1-account'].append(i)
    elif kind == 'L1:group':
        if name in hgroups:
            dec, sen, what, basis, reason = hgroups[name]
        else:
            m = json.loads(r['members'])[0]
            dec, sen, basis = 'UNKNOWN', 'S3-1,S3-2', 'evidence'
            what = 'Group %s (gid %s) without listed members; names a gid for name lookups' % (name, m.split(':')[2])
            reason = 'Removal only drops the name and no member loses it; which udev, tmpfiles, unit or PAM rules resolve this name here is not established (filesystem query failed).'
            rulelog['R4-group-no-members'].append(i)
    else:
        pkg = name.split(':', 1)[1].split(':')[0]
        c = cls[pkg]; fs = files[pkg]
        basis = contents_url(c['repo'])
        if pkg in hand:
            h = hand[pkg]; tpl, what = h[0], h[1]; x = h[2] if len(h) > 2 else ''
            dec, sen, reason = T[tpl]; reason = reason.replace('{X}', x)
            if tpl == 'SCHEMA': basis = GSET
            if tpl == 'GIR': basis = GIDOC
        else:
            code = [p for p in fs if STRONG.search(p) and not DOC.search(p)]
            if pkg.startswith('gir1.2-') and not code:
                dec, sen, reason = T['GIR']; basis = GIDOC
                what = 'GObject introspection typelib: %s' % c['desc']
                rulelog['R3-typelib'].append(i)
            elif code:
                dec, sen, reason = T['CODE']
                d = ' '.join(c['desc'].split()[:9]).rstrip(' -')
                what = '%s; code e.g. /%s' % (d, code[0])
                rulelog['R2-code'].append(i)
            else:
                sys.exit('undecided package ' + pkg)
    for fld in (what, reason, sen, basis):
        if '\t' in fld or '\n' in fld: sys.exit('tab/newline in ' + i)
    if words(what) > 15: print('WHAT>15', i, name, words(what), what)
    if words(reason) > 30: print('REASON>30', i, name, words(reason), reason)
    out.append([i, dec, sen, what, basis, reason])
with open('part-mint.tsv', 'w', encoding='utf-8', newline='') as f:
    f.write('id\tdecision\tsentences\twhat_it_does\tbasis\treason\n')
    for o in out: f.write('\t'.join(o) + '\n')
json.dump(rulelog, open('work/mint/rule-ids.json', 'w'), indent=0)
print({k: len(v) for k, v in rulelog.items()}, 'rows', len(out))

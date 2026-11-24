#!/usr/bin/env python3
"""Decide every row of A3/in/part-gaming.tsv (classification c2) and write A3/c2/part-gaming.tsv.
Rows already present in the output are kept; only missing ids are appended."""
import collections, csv, json, os, re, sys
sys.path.insert(0, '<HOME>/Projects/ideas/cal-paper/night-1123/A3/c2/scripts')
from gcommon import IN, RAW, NIGHT, owner
from gclassify import classify, DOC_FLATPAK, DOC_GEN, LOG

OUT = sys.argv[1] if len(sys.argv) > 1 else NIGHT + 'A3/c2/part-gaming.tsv'
HEAD = ['id', 'decision', 'sentences', 'what_it_does', 'basis', 'reason']
csv.field_size_limit(10**9)


def clean(s):
    return re.sub(r'[\t\r\n]+', ' ', s).strip()


def words(s, n):
    w = clean(s).split()
    return ' '.join(w[:n])


def prog(exe):
    o = owner(exe)
    if not o:
        return None
    n, reason, integ = o[0]
    n = n.replace('dpkg:', '')
    if integ == 'unchanged':
        return '%s (file of package %s, unchanged): INSTALLED-PACKAGE' % (exe, n)
    return '%s (file of package %s, integrity %s)' % (exe, n, integ)


# ---------------------------------------------------------------- members of stored groups / code rows
members = collections.defaultdict(list)
for x in csv.DictReader(open(NIGHT + 'A3/c2/raw/gaming-members.tsv'), delimiter='\t'):
    members[x['gid']].append(x)


def mclass(x):
    m = dict(path=x['path'], type=x['type'], exec=x['exec'], ctime=x['ctime'], pkg=x['pkg'], integrity=x['integrity'],
             target=x['target'], size=x['size'], persistence=x['persistence'], shebang=x['shebang'])
    r = classify(m)
    assert r is not None, x['path']
    return r


SHORT = {'INSTALLED-PACKAGE': 'package files', 'RECORD': 'records', 'RUNTIME': 'runtime', 'MATERIAL': 'material',
         'PROGRAM-OWN': 'programs', 'PROGRAM-DERIVED': 'derived programs', 'SETTING-OWN': 'settings',
         'SETTING-DEFAULT': 'default settings', 'UNKNOWN': 'unknown', 'GAP-TWO': 'gap'}


def group_row(row):
    ms = members[row['id']]
    rs = [(x, mclass(x)) for x in ms]
    decs = collections.Counter(r[0] for x, r in rs)
    labels = collections.Counter((r[0], r[5]) for x, r in rs)
    sents = []
    for x, r in rs:
        for s in r[1].split(','):
            if s not in sents:
                sents.append(s)
    mf = 'raw:members/%s.tsv' % row['id'].split('-', 1)[1]
    if len(labels) == 1:
        (d, lab), = labels.keys()
        x, r = rs[0]
        what = r[2] if len(rs) == 1 else '%d members: %s' % (len(rs), r[5])
        basis = r[3] if len(rs) == 1 else (r[3] if r[3].startswith('doc:') else mf)
        return [row['id'], d, ','.join(sents), words(what, 15), basis, words(r[4], 30)]
    if len(decs) == 1:
        d = next(iter(decs))
        # same decision, several kinds of member
        if d == 'GAP-TWO':
            reason = ('INSTALLED-PACKAGE if the Steam client, which Steam (documented installer) installs and --reset '
                      'removes whole, is a package; else PROGRAM-OWN (code) or RECORD (data, directories).')
            if any(lab == 'Lutris installer script' for _, lab in labels):
                reason = 'Members differ in the two readings; see member rules in notes.'
        else:
            top = labels.most_common(1)[0][0][1]
            reason = 'All members %s: %s.' % (d, '; '.join('%s (%d)' % (lab, n) for (dd, lab), n in labels.most_common(4)))
        what = '%d members of %s' % (len(rs), row['name'])
        return [row['id'], d, ','.join(sents), words(what, 15), mf, words(reason, 30)]
    parts = []
    for d, n in decs.most_common():
        lab = max(((l, c) for (dd, l), c in labels.items() if dd == d), key=lambda t: t[1])[0]
        lw = lab.split()[:4]
        while lw and lw[-1].lower().strip('(,') in ('by', 'of', 'to', 'from', 'the', 'for', 'a', 'on', 'in', 'and', 'with'):
            lw.pop()
        parts.append('%s %d (%s)' % (d, n, ' '.join(lw).rstrip(',(')))
    reason = '; '.join(parts)
    what = '%d members of %s' % (len(rs), row['name'])
    return [row['id'], 'MIXED', ','.join(sents), words(what, 15), mf, words(reason, 30)]


def code_row(row):
    ms = members[row['id']]
    assert len(ms) == 1, row['id']
    r = mclass(ms[0])
    return [row['id'], r[0], r[1], words(r[2], 15), r[3], words(r[4], 30)]


# ---------------------------------------------------------------- level-1 rows
def package_row(row):
    m = json.loads(row['members'])
    mgr, reason = m.get('manager'), m.get('reason')
    name = row['name']
    if mgr == 'dpkg':
        if reason == 'explicit':
            return ['INSTALLED-OWN', 'S8.2-7,S8.2-8,S8.2-16', 'Debian package installed on the computer', 'raw:raw/0079-package-reasons-apt-manual.out',
                    'Package installed by dpkg/apt, marked manually installed: installed object not obtained through another line, so its own line.']
        if reason == 'dependency':
            return ['INSTALLED-DERIVED', 'S8.2-7,S8.2-8,S8.2-16', 'Debian package installed as a dependency', 'raw:raw/0080-package-reasons-apt-auto.out',
                    'Package marked automatically installed: a package installed as a dependency of a recorded package, covered by that line.']
    if mgr == 'flatpak':
        if reason == 'explicit':
            return ['INSTALLED-OWN', 'S8.2-7,S8.2-8,S8.2-16', 'Flatpak application installed by the person', LOG + 'gaming_flatpak_game.log',
                    'Flatpak installs and removes apps as a whole; the app the person installed: installed object needing its own line.']
        return ['INSTALLED-DERIVED', 'S8.2-7,S8.2-8,S8.2-16', 'Flatpak runtime or extension installed with the app', LOG + 'gaming_flatpak_game.log',
                'Installed by flatpak in the same transaction as the app (log), as its runtime or related extension: dependency of a recorded package.']
    if mgr == 'python':
        nid = (m.get('native_package_ids') or [''])[0]
        loc = m.get('location') or name.split('@', 1)[1]
        o = owner(loc)
        if not o:
            import gcommon
            sub = [v for pth, v in gcommon._own.items() if pth.startswith(loc + '/')]
            if sub and all(v[0][2] == 'unchanged' for v in sub):
                o = [(sub[0][0][0], '', 'unchanged (all files)')]
        if o and (o[0][2].startswith('unchanged') or (o[0][2] == 'unknown' and loc.endswith('.dist-info'))):
            return ['INSTALLED-PACKAGE', 'S8.2-7,S8.2-8,S8.2-16', 'Python distribution metadata of a Debian package', 'raw:package-files.tsv',
                    'Metadata path belongs to %s (manifest, %s); obtained as part of that package: its line covers it; pip reason irrelevant.' % (o[0][0].replace('dpkg:', ''), o[0][2])]
        return ['UNKNOWN', 'S8.2-7', 'Python distribution metadata of a Debian package', 'raw:package-files.tsv',
                'Owned by native package %s; whether the metadata remains as received is not recorded.' % nid]
    return ['GAP-NONE', 'S8.2-7', 'package of unhandled manager', 'evidence', 'Manager not covered.']


TIMER_TMPFILES = ('systemd-tmpfiles-clean.timer',)


def level1(row):
    k = row['kind'][2:]
    if k == 'package':
        return [row['id']] + package_row(row)
    rec = json.loads(row['members']).get('record', '')
    if k == 'process':
        pid, exe = rec.split('\t', 1)
        if exe == 'unknown':
            reason = 'Process %s; executable link not readable (kernel thread or exited). Whatever creates it, S8.2-5 makes it RUNTIME.' % pid
            basis = 'raw:raw/0433-process-executables.out'
        elif exe.startswith('/tmp/c1-collector/'):
            reason = 'Process of the collector probe %s, brought by the operator: that program is PROGRAM-OWN.' % exe
            basis = 'raw:raw/0433-process-executables.out'
        else:
            pr = prog(exe)
            reason = 'Process of %s.' % (pr or exe + ' (owner not recorded)')
            basis = 'raw:package-files.tsv'
        return [row['id'], 'RUNTIME', 'S8.2-5', 'running process ' + pid, basis, words(reason, 30)]
    if k == 'port':
        return [row['id'], 'RUNTIME', 'S8.2-5', 'open network port: ' + ' '.join(rec.split()[:1] + rec.split()[4:5]), 'raw:raw/0423-port.out',
                'Open port exists only while running; ss ran without -p, so the owning program is not recorded; any owner gives RUNTIME.']
    if k in ('timer', 'user-timer'):
        unit = [w for w in rec.split() if w.endswith('.timer')][0]
        if unit in TIMER_TMPFILES:
            own = 'link timers.target.wants/%s shipped in package systemd: INSTALLED-PACKAGE' % unit
        elif k == 'user-timer':
            own = 'enablement link created by deb-systemd-user-helper at package installation: SETTING-DEFAULT'
        else:
            own = 'enablement link created by deb-systemd-helper at package installation: SETTING-DEFAULT'
        return [row['id'], 'RUNTIME', 'S8.2-5,S8.1-11,S8.2-17', 'active timer schedule of ' + unit, 'raw:raw/0004-filesystem.out',
                words('Next/last elapse of a loaded timer exists only while running; belongs to %s, %s.' % (unit, own), 30)]
    if k == 'service':
        unit = rec.split()[0]
        return [row['id'], 'RUNTIME', 'S8.2-5', 'state of one-shot boot service ' + unit, 'raw:raw/0004-filesystem.out',
                words('Active/exited unit state exists only while running; belongs to %s, pulled in by sysinit.target.wants link shipped in package systemd: INSTALLED-PACKAGE.' % unit, 30)]
    if k == 'user-service':
        return [row['id'], 'RUNTIME', 'S8.2-5,S8.2-17', 'failed state of user unit fluidsynth.service', 'raw:raw/0442-user-user-service.out',
                'Unit state exists only while running; belongs to fluidsynth.service enablement created by package installation (11:15:49): SETTING-DEFAULT.']
    if k == 'user-unit-file':
        if 'fluidsynth' in row['name']:
            return [row['id'], 'SETTING-DEFAULT', 'S8.1-11,S8.2-11,S8.2-13,S8.2-17', 'global user-service enablement of FluidSynth daemon', 'raw:raw/0004-filesystem.out',
                    'Service enabled state is a setting; link in /etc/systemd/user created by deb-systemd-user-helper during fluidsynth installation: package default.']
        return [row['id'], 'RUNTIME', 'S8.2-5,S8.2-14', 'unit generated from autostart entry lutris.desktop', DOC_GEN,
                'Generated into the runtime directory (tmpfs) by systemd-xdg-autostart-generator; belongs to ~/.config/autostart/lutris.desktop: SETTING-OWN.']
    if k == 'saved-network':
        return [row['id'], 'RUNTIME', 'S8.2-5', 'loopback connection profile generated by NetworkManager', 'raw:raw/0004-filesystem.out',
                'Profile file is on tmpfs (/run/NetworkManager), new UUID each boot; belongs to NetworkManager (package network-manager, unchanged): INSTALLED-PACKAGE.']
    if k == 'image-container-store':
        return [row['id'], 'MIXED', 'S8.2-7,S8.2-9,S8.2-15,S8.2-16', 'Flatpak per-user installation: repository, deployed apps and runtimes, exports', DOC_FLATPAK,
                'app/, runtime/ deployments: INSTALLED-PACKAGE, but integrity not collected (UNKNOWN); repo/ OSTree objects, .changed: RECORD; exports/ launchers: PROGRAM-DERIVED.']
    return [row['id'], 'GAP-NONE', '', 'unhandled kind', 'evidence', 'Kind not handled.']


def main():
    done = set()
    if os.path.exists(OUT) and os.path.getsize(OUT) > 0:
        for x in csv.DictReader(open(OUT), delimiter='\t'):
            done.add(x['id'])
        f = open(OUT, 'a')
    else:
        f = open(OUT, 'w')
        f.write('\t'.join(HEAD) + '\n')
    n = 0
    for row in csv.DictReader(open(IN + 'part-gaming.tsv'), delimiter='\t'):
        if row['id'] in done:
            continue
        k = row['kind']
        if k.startswith('2:stored'):
            out = group_row(row)
        elif k.startswith('2:code'):
            out = code_row(row)
        else:
            out = level1(row)
        out = [clean(v) for v in out]
        f.write('\t'.join(out) + '\n')
        n += 1
        if n % 2000 == 0:
            f.flush()
    f.close()
    print('written', n)


if __name__ == '__main__':
    main()

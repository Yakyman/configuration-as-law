#!/usr/bin/env python3
"""Build A3/c2/part-developer.tsv (classification c2). Appends rows for ids not yet present."""
import csv, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from members_rules import classify, load_shebang
from system_groups import member_rule

NIGHT = '<HOME>/Projects/ideas/cal-paper/night-1123/'
IN = NIGHT + 'A3/in/'
RAW = IN + 'raw/developer/'
OUT = sys.argv[1] if len(sys.argv) > 1 else NIGHT + 'A3/c2/part-developer.tsv'
csv.field_size_limit(10**9)

SENT = {
    'INSTALLED-OWN': 'S8.2-6,S8.2-7,S8.2-8,S8.2-16',
    'INSTALLED-PACKAGE': 'S8.2-6,S8.2-7,S8.2-8,S8.2-16',
    'INSTALLED-DERIVED': 'S8.2-6,S8.2-7,S8.2-8,S8.2-16',
    'PROGRAM-OWN': 'S8.2-6,S8.2-9,S8.2-10,S8.2-16',
    'PROGRAM-DERIVED': 'S8.2-6,S8.2-9,S8.2-10,S8.2-16',
    'SETTING-OWN': 'S8.2-11,S8.2-12,S8.2-13,S8.2-17',
    'SETTING-DEFAULT': 'S8.2-8,S8.2-17',
    'RECORD': 'S8.2-15,S8.2-2',
    'MATERIAL': 'S8.2-15,S8.2-2',
    'RUNTIME': 'S8.2-5',
    'ACTION': 'S8.2-3,S8.2-4',
    'UNKNOWN': 'S8.2-11,S8.2-14,S8.2-17',
    'GAP-TWO': 'S8.1-4,S8.1-6,S8.2-7,S8.2-17',
}
EXTRA = [
    (r'not installed|not executable here|foreign', 'S8.2-20'),
    (r'link', 'S8.2-23'),
    (r'executed by bash|evaluated by|sourced by', 'S8.2-23'),
    (r'installer|plugin manager|lefthook|juliaup|brew install|bun add|gem install|uv tool', 'S8.1-4,S8.1-5,S8.1-6'),
    (r'launch|obeyed only', 'S8.2-14'),
    (r'directory', 'S8.2-3'),
]

DECISIONS = {'INSTALLED-OWN', 'INSTALLED-PACKAGE', 'INSTALLED-DERIVED', 'PROGRAM-OWN', 'PROGRAM-DERIVED',
             'SETTING-OWN', 'SETTING-DEFAULT', 'RECORD', 'MATERIAL', 'RUNTIME', 'ACTION', 'GAP-NONE',
             'GAP-TWO', 'UNKNOWN', 'MIXED'}


def sentences_for(dec, label=''):
    if dec == 'GAP-TWO':
        if 'juliaup binary' in label:
            ids = ['S8.1-4', 'S8.1-6', 'S8.2-7', 'S8.2-9']
        elif 'self-update' in label:
            ids = ['S8.1-6', 'S8.2-14', 'S8.2-17']
        else:
            ids = ['S8.2-11', 'S8.2-15', 'S8.2-17']
    elif dec == 'UNKNOWN':
        if '#!' in label:
            ids = ['S8.2-9', 'S8.2-15', 'S8.2-20']
        elif 'SSH' in label:
            ids = ['S8.2-14', 'S8.2-15']
        else:
            ids = ['S8.2-11', 'S8.2-13', 'S8.2-17']
    else:
        ids = SENT.get(dec, '').split(',')
        for rx, extra in EXTRA:
            if re.search(rx, label, re.I):
                ids += extra.split(',')
    seen = []
    for i in ids:
        if i and i not in seen:
            seen.append(i)
    return ','.join(sorted(seen, key=lambda s: (s.split('-')[0], int(s.split('-')[1]))))


def words(s, n):
    w = s.split()
    return ' '.join(w[:n])


def clean(s):
    return s.replace('\t', ' ').replace('\n', ' ')


# --------------------------------------------------------------------------------------------------
def load_members():
    by_group = collections.defaultdict(list)
    by_path = {}
    for m in csv.DictReader(open('/tmp/c2dev/members.tsv'), delimiter='\t'):
        by_group[m['gid']].append(m)
        by_path[m['path']] = m
    return by_group, by_path


def member_decision(group_name, m):
    if group_name.startswith('/home'):
        r = classify(m)
    else:
        r = member_rule(group_name, m)
    if r is None:
        raise SystemExit('no rule for member %s of %s' % (m['path'], group_name))
    return r


def group_row(x, members):
    name = x['name']
    decs = [member_decision(name, m) for m in members]
    cnt = collections.Counter(d for d, _ in decs)
    labels = collections.defaultdict(collections.Counter)
    for d, l in decs:
        labels[d][l] += 1
    basis = 'raw:' + json.loads(x['members'])['file']
    if len(cnt) == 1:
        dec = next(iter(cnt))
        lab = labels[dec].most_common(1)[0][0]
        allabs = '; '.join(l for l, _ in labels[dec].most_common(3))
        bn = os.path.basename(name) or name
        if bn in ('.claude', '.codex', '.cursor'):
            bn = '(hidden tool-configuration directory)'
        what = words('Directory %s: %d members; %s' % (bn, len(members), lab), 15)
        sent = sentences_for(dec, ' '.join(labels[dec]))
        if dec == 'RUNTIME':
            reason = 'All %d members exist only while running (tmpfs, pseudo file system or service lifetime); %s' % (len(members), lab.split('; ', 1)[-1])
        elif dec in ('GAP-TWO', 'UNKNOWN'):
            reason = 'All members: ' + allabs
        else:
            reason = 'All %d members: %s' % (len(members), allabs)
        return dec, sent, what, basis, words(reason, 30)
    # MIXED
    parts = []
    sent_ids = set()
    for d, n in cnt.most_common():
        lab = labels[d].most_common(1)[0][0]
        parts.append((d, n, lab))
        sent_ids.update(sentences_for(d, ' '.join(labels[d])).split(','))
    budget = 30
    pieces = []
    k = len(parts)
    per = max(2, (budget - 1 - 2 * k) // k)
    for d, n, lab in parts:
        pieces.append('%d %s (%s)' % (n, d, words(lab, per)))
    reason = 'MIXED: ' + '; '.join(pieces)
    if len(reason.split()) > 30:
        pieces = ['%d %s' % (n, d) for d, n, _ in parts]
        reason = 'MIXED: ' + '; '.join(pieces)
        # add first label words while room remains
        room = 30 - len(reason.split())
        if room > 3:
            reason += ' - ' + words(parts[0][2], room - 1)
    what = words('Directory %s: %d members of differing kinds' % (os.path.basename(name) or name, len(members)), 15)
    sent = ','.join(sorted((s for s in sent_ids if s), key=lambda s: (s.split('-')[0], int(s.split('-')[1]))))
    return 'MIXED', sent, what, basis, words(reason, 30)


# --------------------------------------------------------------------------------------------------
def package_row(x):
    m = json.loads(x['members'])
    n = x['name']
    reason_v = m.get('reason')
    nat = m.get('native_reason')
    ev = 'evidence'
    if n.startswith('rpm:gpg-pubkey'):
        key = 'Docker' if '060a61c5' in n else 'Fedora 45'
        return ('INSTALLED-DERIVED', 'S8.1-6,S8.2-7,S8.2-8,S8.2-16',
                'rpm pseudo-package holding the %s repository signing key' % key,
                'raw:../../operator/developer/actions-logs/actions-logs/developer_%s.stderr' % ('container' if key == 'Docker' else 'prerequisites'),
                'rpm keeps the key as a package; dnf imported it itself from the gpgkey of the repository line (log: Importing OpenPGP key), so the repository line covers it')
    if n.startswith('rpm:'):
        pkg = n[4:].split('@')[0]
        if reason_v == 'explicit':
            return ('INSTALLED-OWN', 'S8.2-6,S8.2-7,S8.2-8,S8.2-16', 'rpm package %s installed by dnf at a person\'s request' % pkg, ev,
                    'Q1: a package installed on the computer; dnf records reason user (explicit), so no other line obtains it: a line of its own')
        if reason_v == 'dependency':
            return ('INSTALLED-DERIVED', 'S8.2-6,S8.2-7,S8.2-8,S8.2-16', 'rpm package %s installed as a dependency' % pkg, ev,
                    'Q1: a package installed on the computer; dnf records %s, so it is a package installed as a dependency of a recorded package' % nat)
        if nat == 'group':
            return ('INSTALLED-DERIVED', 'S8.2-6,S8.2-7,S8.2-8,S8.2-16', 'rpm package %s installed by a group selection' % pkg, ev,
                    'Q1: a package; dnf native reason group: obtained by the system from a group (a list), not chosen individually, so the group line covers it')
    if n.startswith('gem:'):
        g = n[4:]
        if g.startswith('lefthook-'):
            return ('INSTALLED-OWN', 'S8.1-4,S8.1-6,S8.2-7,S8.2-8,S8.2-16', 'lefthook gem: Git hooks manager installed with gem install --user-install',
                    'raw:../../operator/developer/actions-logs/actions-logs/developer_global_tools.log',
                    'Q1: a gem is a package of the RubyGems installer; log shows "Successfully installed lefthook-2.2.2, 1 gem installed": requested by a person, not a dependency')
        return ('INSTALLED-PACKAGE', 'S8.2-6,S8.2-7,S8.2-8,S8.2-16', 'Ruby default/bundled gem %s shipped inside Fedora ruby rpm packages' % g,
                'raw:raw/0017-package-files-rpm.out',
                'Q1: gem obtained as part of an installed rpm (ruby-default-gems, ruby-bundled-gems, rubygem-*); covered by that rpm package line')
    if n.startswith('npm:'):
        loc = m.get('location', '')
        nm = n[4:].split('@/')[0]
        if loc.endswith('/global/node_modules/eslint'):
            return ('INSTALLED-OWN', 'S8.1-4,S8.1-6,S8.2-7,S8.2-8,S8.2-16', 'eslint JavaScript linter installed globally with bun add -g',
                    'raw:../../operator/developer/actions-logs/actions-logs/developer_global_tools.log',
                    'Q1: package of the bun installer; log "installed eslint@10.15.0 with binaries": requested by a person, so a line of its own')
        return ('INSTALLED-DERIVED', 'S8.1-4,S8.1-6,S8.2-7,S8.2-8,S8.2-16', 'npm package %s pulled in by bun for eslint' % nm,
                'raw:../../operator/developer/actions-logs/actions-logs/developer_global_tools.log',
                'Q1: package installed by bun; only eslint was requested ("78 packages installed"), so this one is a dependency of the recorded eslint package')
    if n.startswith('python:ruff@/home/user/.local/share/uv/tools'):
        return ('INSTALLED-OWN', 'S8.1-4,S8.1-6,S8.2-7,S8.2-8,S8.2-16', 'ruff Python linter installed with uv tool install', ev,
                'Q1: package installed by the uv installer; reason_source python-requested (explicit), so a line of its own')
    if n.startswith('python:ruff@/home/user/.cache/uv'):
        return ('RECORD', 'S8.2-7,S8.2-9,S8.2-15', 'metadata directory of an unpacked ruff wheel in the uv cache', ev,
                'Not installed (cache copy), dist-info holds metadata only (not code), no person chose it; uv recorded it as cache: program record')
    raise SystemExit('package without rule: ' + n)


PROC_OWNER = {
    '/usr/bin/containerd-shim-runc-v2': 'containerd shim (containerd.io file, INSTALLED-PACKAGE) for the container',
    '/bin/httpd': 'httpd inside the container (container PROGRAM-OWN)',
    '/usr/bin/docker-proxy': 'docker-proxy (docker-ce file, INSTALLED-PACKAGE) for the container port',
    '/usr/bin/containerd': 'containerd (containerd.io file, INSTALLED-PACKAGE)',
    '/usr/bin/dockerd': 'dockerd (docker-ce file, INSTALLED-PACKAGE), docker.service SETTING-OWN',
    '/tmp/c1-collector/probe': 'the inventory probe started by the operator\'s command (ACTION)',
    '/usr/bin/python3.15': 'the python3 interpreter (INSTALLED-PACKAGE) running a system daemon',
}


def level1_row(x):
    k, n = x['kind'], x['name']
    m = json.loads(x['members'])
    rec = m.get('record', '')
    if k == '1:package':
        return package_row(x)
    if k == '1:group':
        return ('SETTING-DEFAULT', 'S8.2-13,S8.2-17', 'system group docker, gives socket access to members (none)',
                'raw:configuration-origin.tsv',
                'Account/rights setting created during docker-ce installation (group file rewritten 11:14:48 inside the dnf transaction); default created at installation: package line')
    if k == '1:process':
        exe = rec.split('\t', 1)[1] if '\t' in rec else 'unknown'
        if exe == 'unknown':
            return ('RUNTIME', 'S8.2-5', 'process without executable link (kernel thread)', 'doc:https://man7.org/linux/man-pages/man5/proc_pid_exe.5.html',
                    'A process exists only while running; readlink of /proc/PID/exe failed (kernel thread); it belongs to the kernel (kernel package, INSTALLED-PACKAGE)')
        owner = PROC_OWNER.get(exe, '%s (package file, INSTALLED-PACKAGE)' % exe)
        return ('RUNTIME', 'S8.2-5', 'running process of %s' % exe, 'evidence',
                words('A process exists only while running; it belongs to ' + owner, 30))
    if k == '1:port':
        port = rec.split()[4] if len(rec.split()) > 4 else rec
        own = {
            '5353': 'avahi-daemon (INSTALLED-PACKAGE; service enabled by preset, SETTING-DEFAULT)',
            '5355': 'systemd-resolved LLMNR (INSTALLED-PACKAGE; SETTING-DEFAULT)',
            '53': 'systemd-resolved stub resolver (INSTALLED-PACKAGE; SETTING-DEFAULT)',
            '323': 'chronyd (INSTALLED-PACKAGE; SETTING-DEFAULT)',
            '22': 'sshd, enabled by sshd.service link (SETTING-OWN)',
            '18080': 'docker-proxy publishing the container port (container PROGRAM-OWN)',
        }[port.rsplit(':', 1)[1]]
        return ('RUNTIME', 'S8.2-5', 'listening socket %s' % port, 'evidence',
                'An open port exists only while running; it belongs to ' + own)
    if k == '1:service':
        u = n
        own = {
            'containerd.service': 'containerd.service, started as a dependency of docker.service (SETTING-OWN)',
            'docker.service': 'docker.service enablement (SETTING-OWN)',
            'virtqemud.service': 'virtqemud unit of libvirt (INSTALLED-PACKAGE; enabled by preset, SETTING-DEFAULT)',
        }[u]
        return ('RUNTIME', 'S8.2-5,S8.1-11', 'loaded/active state of %s' % u, 'evidence',
                'Active or loaded state exists only while running; it belongs to ' + own)
    if k == '1:unit-file':
        if n == 'docker.service':
            return ('SETTING-OWN', 'S8.1-11,S8.2-12,S8.2-13,S8.2-17', 'docker.service enabled although vendor preset disabled', 'evidence',
                    'A service is a setting; enabled while preset says disabled, so a person chose it (action enabled docker): line of its own')
        return ('SETTING-DEFAULT', 'S8.1-11,S8.2-13,S8.2-17', 'containerd.service disabled, as its vendor preset', 'evidence',
                'Service state equals the vendor preset (disabled) from installation of containerd.io: a default covered by the package line')
    if k == '1:timer':
        t = rec.split()[-2]
        own = {
            'systemd-tmpfiles-clean.timer': 'static systemd timer (INSTALLED-PACKAGE)',
            'dnf-makecache.timer': 'dnf-makecache.timer enabled by preset (SETTING-DEFAULT)',
            'logrotate.timer': 'logrotate.timer enabled by preset (SETTING-DEFAULT)',
            'plocate-updatedb.timer': 'plocate-updatedb.timer enabled by preset (SETTING-DEFAULT)',
            'fstrim.timer': 'fstrim.timer enabled by preset (SETTING-DEFAULT)',
        }[t]
        return ('RUNTIME', 'S8.2-5', 'next/last trigger times of %s' % t, 'evidence',
                'Scheduled trigger times exist only while running; they belong to ' + own)
    if k == '1:user-timer':
        t = rec.split()[-2]
        own = {
            'systemd-tmpfiles-clean.timer': 'static systemd user timer (INSTALLED-PACKAGE)',
            'cal-project-summary.timer': 'user timer cal-project-summary (SETTING-OWN)',
            'grub-boot-success.timer': 'grub2 user timer enabled by preset (SETTING-DEFAULT)',
        }[t]
        return ('RUNTIME', 'S8.2-5', 'trigger times of user timer %s' % t, 'evidence',
                'Scheduled trigger times exist only while running; they belong to ' + own)
    if k == '1:user-service':
        return ('RUNTIME', 'S8.2-5', 'loaded state of user service cal-project-summary', 'evidence',
                'Loaded/inactive state exists only while running; it belongs to the user service cal-project-summary (SETTING-OWN)')
    if k == '1:user-unit-file':
        return ('SETTING-OWN', 'S8.1-11,S8.2-12,S8.2-13,S8.2-14', 'user unit %s enabled by a person' % n.split(':', 1)[1], 'evidence',
                'Service enablement is a setting; the unit timer launches the summary script; created and enabled at a person\'s command: line of its own')
    if k == '1:module-name':
        return ('RUNTIME', 'S8.2-5', 'loaded kernel module %s' % n, 'evidence',
                'A loaded module exists only while running; loaded on demand for docker networking by dockerd (docker-ce, INSTALLED-PACKAGE; docker.service SETTING-OWN)')
    if k == '1:saved-network':
        dev = n.split(':')[0]
        own = 'dockerd creating bridge docker0 (docker-ce, INSTALLED-PACKAGE)' if dev == 'docker0' else 'NetworkManager loopback handling (INSTALLED-PACKAGE)'
        return ('RUNTIME', 'S8.2-5', 'NetworkManager in-memory connection for %s' % dev, 'raw:members/130507d632cdd51fdf840931.tsv',
                'Connection file lies in /run/NetworkManager/system-connections (tmpfs): exists only while running; generated by NetworkManager for ' + own)
    if k == '1:docker-container':
        return ('PROGRAM-OWN', 'S8.2-9,S8.2-10,S8.2-16,S8.2-22', 'container running busybox httpd on port 8080, published 127.0.0.1:18080', 'evidence',
                'A program running as its own process in a container is a program; created by a person\'s docker run, no line builds it: line of its own')
    if k == '1:docker-image':
        return ('PROGRAM-OWN', 'S8.2-9,S8.2-10,S8.2-16', 'locally built image cal-development-web:local with httpd', 'evidence',
                'Image code is executable through docker; built by a person\'s docker build, not by an installer or a declaration line: line of its own')
    if k.startswith('1:firewall'):
        fam_tab = n.split('/')
        if k in ('1:firewall-ipv4', '1:firewall-ipv6') and rec.startswith('#'):
            return ('ACTION', 'S8.2-3,S8.2-4', 'comment line printed by iptables-save for the inventory', 'evidence',
                    'The line records the inventory command and its time, not an object on the computer; it is a trace of a person\'s command')
        if n.startswith('inet/') or 'firewalld' in n:
            own = 'firewalld (INSTALLED-PACKAGE; service SETTING-DEFAULT) from its zone/policy configuration'
            what = 'firewalld nftables %s in the running kernel' % k.split('-', 1)[1]
        else:
            own = 'dockerd (docker-ce, INSTALLED-PACKAGE) started by docker.service (SETTING-OWN)'
            what = 'Docker iptables/nftables %s in the running kernel' % k.split('-', 1)[1]
        return ('RUNTIME', 'S8.2-5', what, 'evidence',
                'Kernel netfilter state exists only while running; created by ' + own)
    raise SystemExit('no level-1 rule: %s %s' % (k, n))


def store_row(x):
    n = x['name']
    if n == '/var/lib/docker':
        return ('MIXED', 'S8.2-5,S8.2-9,S8.2-10,S8.2-15,S8.2-16,S8.2-22', 'Docker engine data: containers, networks, buildkit state', 'doc:https://docs.docker.com/engine/storage/containerd/',
                'MIXED (store not traversed): container of the docker-container row PROGRAM-OWN; network, buildkit and engine state RECORD')
    if n == '/var/lib/containerd':
        return ('MIXED', 'S8.2-9,S8.2-10,S8.2-15,S8.2-16', 'containerd content store and snapshots holding image layers', 'doc:https://docs.docker.com/engine/storage/containerd/',
                'MIXED (store not traversed): image content/snapshots of the docker-image row PROGRAM-OWN; containerd metadata RECORD')
    raise SystemExit(n)


def code_row(x, by_path):
    p = x['name']
    m = by_path[p]
    d, lab = member_decision('/home' if p.startswith('/home') else os.path.dirname(p), m)
    md = json.loads(x['members'])
    what = words(lab, 15)
    reason = {
        'INSTALLED-PACKAGE': 'Q1 first: obtained as part of an installed package and unchanged since installation (ctime inside install window): installed object, package line',
        'INSTALLED-OWN': 'Q1: a package of an installer, installed at a person\'s command: line of its own',
        'PROGRAM-OWN': 'Not part of a package; executable code (Q2); placed at a person\'s command, no line builds it: line of its own',
        'PROGRAM-DERIVED': 'Not part of a package; code (Q2) built or obtained by the system itself from a recorded line',
        'GAP-TWO': lab,
        'RECORD': 'Not code here; written by a program as it ran: program record',
        'MATERIAL': 'Not executable here; brought at a person\'s command: material',
        'UNKNOWN': lab,
    }[d]
    if d == 'PROGRAM-OWN':
        reason = 'Not part of a package; code executable here (Q2): ' + lab + '; no line builds it: line of its own'
    if d == 'PROGRAM-DERIVED':
        reason = 'Not part of a package; code (Q2): ' + lab
    basis = 'raw:configuration-origin.tsv' if d.startswith('INSTALLED') else ('doc:https://github.com/oven-sh/bun/blob/main/src/install/npm.rs' if 'manifest cache' in lab else 'evidence')
    return d, sentences_for(d, lab), what, basis, words(reason, 30)


def main():
    rows = list(csv.DictReader(open(IN + 'part-developer.tsv'), delimiter='\t'))
    load_shebang(rows)
    by_group, by_path = load_members()
    done = set()
    if os.path.exists(OUT):
        for r in csv.DictReader(open(OUT), delimiter='\t'):
            done.add(r['id'])
    new = not os.path.exists(OUT)
    f = open(OUT, 'a', newline='')
    w = csv.writer(f, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_NONE, escapechar=None)
    if new:
        f.write('id\tdecision\tsentences\twhat_it_does\tbasis\treason\n')
    for x in rows:
        if x['id'] in done:
            continue
        k = x['kind']
        if k == '2:stored-ownership-unresolved':
            mem = by_group[x['id']]
            assert len(mem) == json.loads(x['members'])['count']
            r = group_row(x, mem)
        elif k == '2:code-ownership-unresolved':
            r = code_row(x, by_path)
        elif k == '2:image-container-store':
            r = store_row(x)
        else:
            r = level1_row(x)
        dec, sent, what, basis, reason = r
        assert dec in DECISIONS, dec
        f.write('\t'.join(clean(v) for v in (x['id'], dec, sent, words(what, 15), basis, words(reason, 30))) + '\n')
    f.close()


if __name__ == '__main__':
    main()

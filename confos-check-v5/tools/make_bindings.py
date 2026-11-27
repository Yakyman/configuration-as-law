# SPDX-License-Identifier: MIT
"""Generate bindings/release-0.68.json: semantic binding slots -> native 0.68 lines.

Usage: python3 -I tools/make_bindings.py [--interface FILE --base-conf FILE]
The two optional files are the release's INTERFACE.md and declarations/base.conf;
their SHA-256 values are recorded, and the package list is taken from base.conf.
Without them, the frozen values already in the output file are kept.
Every slot is either bound to native lines or 'unsupported' with the reason and
the section of the interface that says so. Nothing is guessed silently.
"""
import argparse, hashlib, json, shlex
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / 'bindings' / 'release-0.68.json'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def package(name, version, recipe, sources):
    return {'native': ['package %s %s %s' % (name, version, recipe)],
            'inputs': {recipe: 'payloads/' + recipe, **{s: 'payloads/' + s for s in sources}}}


def unsupported(reason):
    return {'unsupported': reason}


def release_layout(a, old):
    """Objects the base itself contributes, derived from the SOURCES of named base packages.

    files/confos/confos (package confos): BASE_PASSWD, BASE_GROUPS, STARTUP_FILES, render();
    files/confos-boot/rc.boot and initramfs-init.c (package confos-boot): the mounts.
    Never from a machine. Returns (layout objects, derivation table).
    """
    import ast
    if not a.base_conf:
        return old['layout'], old['derivation']
    tree = Path(a.base_conf).resolve().parent.parent
    src = tree / 'files/confos/confos'
    mod = ast.parse(src.read_text())
    consts = {}
    for node in mod.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and \
                node.targets[0].id in ('BASE_PASSWD', 'BASE_GROUPS', 'STARTUP_FILES'):
            consts[node.targets[0].id] = ast.literal_eval(node.value)
    layout = []
    for line in consts['BASE_PASSWD']:
        n, _, uid, gid, _, home, shell = line.split(':')
        layout.append({'kind': 'account', 'id': n, 'value': {'uid': int(uid), 'gid': int(gid), 'home': home, 'shell': shell}})
    for n, g in consts['BASE_GROUPS'].items():
        layout.append({'kind': 'group', 'id': n, 'value': {'gid': g}})
    layout += [{'kind': 'network', 'id': '127.0.0.1/8', 'value': {}}, {'kind': 'network', 'id': '::1/128', 'value': {}}]
    # rc.boot and initramfs-init.c: every mount the base makes, with its noexec flag.
    mounts = {'/': (False, 'squashfs'), '/system': (True, 'ext4'), '/dev': (True, 'devtmpfs'), '/proc': (True, 'proc'),
              '/sys': (True, 'sysfs'), '/run': (True, 'tmpfs'), '/tmp': (True, 'tmpfs'), '/run/root-view': (False, 'squashfs'),
              '/var': (True, 'tmpfs'), '/dev/pts': (True, 'devpts'), '/dev/shm': (True, 'tmpfs'), '/data': (True, 'ext4'),
              '/home': (True, 'ext4'), '/root': (True, 'ext4'), '/sys/kernel/security': (False, 'securityfs')}
    for mp, (noexec, fs) in mounts.items():
        layout.append({'kind': 'mount', 'id': mp, 'value': {'fstype': fs} if mp in ('/sys/kernel/security',) else {'fstype': fs, 'noexec': noexec}})
    layout += [{'kind': 'partition-root', 'id': '/system', 'value': {}}, {'kind': 'partition-root', 'id': '/data', 'value': {}}]
    for d in ('/data/home', '/data/root', '/data/confos'):
        layout.append({'kind': 'dir', 'id': d, 'value': {}})
    rendered = ['/etc/passwd', '/etc/group', '/etc/shadow', '/etc/hostname', '/etc/hosts', '/etc/timezone',
                '/etc/locale.conf', '/etc/network.conf', '/etc/confos/sysctls.json', '/etc/confos/services.json',
                '/etc/confos/rules.nft', '/etc/confos/open.json', '/etc/confos/home-files.json',
                '/etc/confos/session.apparmor', '/etc/confos/identity', '/etc/confos/system.json',
                '/usr/lib/confpkg/declaration.passport']
    derivation = {'source_sha256': {'files/confos/confos': sha(src), 'files/confos-boot/rc.boot': sha(tree / 'files/confos-boot/rc.boot'),
                                    'files/confos-boot/initramfs-init.c': sha(tree / 'files/confos-boot/initramfs-init.c')},
                  'rendered_files': rendered, 'rendered_links': ['/etc/localtime'], 'startup_files': list(consts['STARTUP_FILES']),
                  'per_account': ['/etc/dropbear/authorized_keys/{account}'], 'declaration_copy': '/etc/confos/declaration/{rel}',
                  'home_file_mounts': True, 'open_mounts': True,
                  'note': 'rendered paths replace package files of the same path (render(): put() unlinks first); '
                          'their exact bytes are implementation output, so only presence is derived; the values they carry '
                          'are derived as account/group/setting/key/service/rule objects and observed live'}
    return layout, derivation


def update_slots(a, old, base):
    """INTERFACE 9: an update is an edit of the declaration. T0 is the release itself; T1 and
    T2 are the update states (tags of the builder's tree, made by scripts/update-states.py).
    The line `base RELEASE FOLDER SHA256` names the tree the person brings beside the
    declaration; the package lines that differ from the release in force are replaced."""
    if not a.update:
        return {k: v for k, v in old.get('lines', {}).items() if k in ('T1', 'T2') or k.startswith('system-update-state-')}
    import subprocess, sys
    sys.path.insert(0, str(HERE))
    t0 = {r.split()[1]: r.split()[2] for r in base if r.startswith('package ')}
    t0_base = [r for r in base if r.startswith('base ')][0]
    out = {'system-update-state-T0': {'native': [t0_base], 'note': 'INTERFACE 9: T0 is the release itself'}}
    for state, release, folder in a.update:
        tree = Path(folder).resolve()
        tsum = subprocess.run([sys.executable, '-I', str(tree / 'tools/confpkg'), 'treesum', str(tree)],
                              capture_output=True, text=True, check=True).stdout.split()[0]
        rows = [shlex.split(l, comments=True) for l in (tree / 'declarations/base.conf').read_text().splitlines()]
        new = {r[1]: r[2] for r in rows if r and r[0] == 'package'}
        if set(new) != set(t0):
            raise SystemExit('update state %s names other packages than the release' % state)
        changed = sorted(n for n in new if new[n] != t0[n])
        import adapter_native
        whole = adapter_native.whole_tree_digest(tree)
        sources = {}
        for n in changed:
            for row in (tree / 'recipes' / (n + '.recipe')).read_text().splitlines():
                if row.startswith('source:'):
                    fname, fsha = row.split()[1:3]
                    if '/' not in fname and fname != 'tools':
                        sources[fname] = fsha
        folder_name = 'rel-' + release
        slot = {'native': ['base %s %s %s' % (release, folder_name, tsum)] + ['package %s %s' % (n, new[n]) for n in changed],
                'replaces': {'base': True, 'packages': changed},
                'tree_input': {'folder': folder_name, 'state': state, 'release': release, 'treesum': tsum,
                               'whole_tree_sha256': whole['digest'], 'files': whole['files']},
                'source_inputs': sources,
                'note': 'INTERFACE 9: the tree of %s (git archive of the tag) and the sources it adds are brought beside '
                        'the declaration; the base line and the package lines that differ from %s are replaced' % (release, t0_base)}
        out['system-update-state-' + state] = slot
        out[state] = slot
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--interface')
    ap.add_argument('--base-conf')
    ap.add_argument('--update', nargs=3, action='append', metavar=('STATE', 'RELEASE', 'TREE'),
                    help='an update state: T1 0.68.1 DIR (DIR = git archive of the tag)')
    a = ap.parse_args()
    old = json.loads(OUT.read_text()) if OUT.exists() else {}
    if a.base_conf:
        rows = [shlex.split(l, comments=True) for l in Path(a.base_conf).read_text().splitlines()]
        base = [' '.join(r) for r in rows if r and r[0] in ('base', 'package', 'network')]
        sources = {'INTERFACE.md': sha(a.interface), 'declarations/base.conf': sha(a.base_conf)}
    else:
        base = old['lines']['base-source-lock']['native']
        sources = old['sources']
    rule = (HERE / 'payloads' / 'case-rule.sudoers')
    lines = {
        'base-source-lock': {'native': base,
            'note': 'base, package and network lines of the release base.conf; its account, '
                    'sudo file and keys are replaced by the case bindings below'},
        'test-account-and-login': {'native': [
            'account user 1000 1000 users /bin/bash /home/user',
            'authorized-key user @KEY_TYPE@ @KEY@',
            'authorized-key root @KEY_TYPE@ @KEY@',
            'open /home/user/control',
            'open /root/control',
            "rule case-ssh 'add rule inet confos input tcp dport 22 accept'"],
            'note': 'role user = account user over SSH; role root = root over SSH (INTERFACE 4); '
                    '/home/user/control and /root/control are the opened folders of the positive controls (A18); '
                    'the rule case-ssh records the SSH port, the recorded rule of G-FIREWALL "remove recorded rule"'},
        'case-probe-package': package('case-probe', '1', 'case-probe-1.recipe', ['case-probe.c']),
        'case-small-v1-package': package('case-small', '1', 'case-small-1.recipe', ['case-small.c']),
        'test-service': {'native': ['service case-service enabled /usr/bin/case-probe listen 7071'],
            'requires': ['case-probe-package']},
        'test-access-rule': {'native': ['file /etc/sudoers.d/case-rule 0440 0:0 %s case-rule.sudoers' % sha(rule)],
            'inputs': {'case-rule.sudoers': 'payloads/case-rule.sudoers'}},
        'test-hostname': {'native': ['setting hostname case-test']},
        'test-timezone': {'native': ['setting timezone Etc/GMT-3']},
        'small-v1': package('case-small', '1', 'case-small-1.recipe', ['case-small.c']),
        'small-v2': package('case-small', '2', 'case-small-2.recipe', ['case-small.c']),
        'probe': package('case-probe', '1', 'case-probe-1.recipe', ['case-probe.c']),
        'case-extra-a': package('case-extra-a', '1', 'case-extra-a-1.recipe', ['case-small.c']),
        'case-extra-b': package('case-extra-b', '1', 'case-extra-b-1.recipe', ['case-small.c']),
        'case-extra-service': {'native': ['package case-extra-service 1 case-extra-service-1.recipe',
            'service case-extra enabled /usr/bin/case-extra-service listen 7073'],
            'inputs': {'case-extra-service-1.recipe': 'payloads/case-extra-service-1.recipe', 'case-probe.c': 'payloads/case-probe.c'}},
        'case-sleeper': package('case-sleeper', '1', 'case-sleeper-1.recipe', ['case-probe.c']),
        'case-firewall-4446': {'native': ["rule case-fw 'add rule inet confos input tcp dport 4446 accept'"]},
        'case-firewall-4447': {'native': ["rule case-fw 'add rule inet confos input tcp dport 4447 accept'"]},
        'case-hostname-changed': {'native': ['setting hostname case-chg'], 'replaces': 'test-hostname'},
        'case-account-shell': {'native': ['account user 1000 1000 users /bin/sh /home/user'],
            'replaces_line': 'account user 1000 1000 users /bin/bash /home/user'},
        'test-user-timer': unsupported('INTERFACE 5: no timers and no per-user services; a service line runs a program at boot'),
        'D-accounts-fixed-native-lines': {'order_items': {
            'a': ['account case-a 1101 1101 - /bin/bash @HOME_ROOT@/case-a'],
            'b': ['account case-b 1102 1102 - /bin/bash @HOME_ROOT@/case-b']}},
        'D-accounts-open-native-lines': {'order_items': {
            'a': ['account case-a auto auto - /bin/bash @HOME_ROOT@/case-a'],
            'b': ['account case-b auto auto - /bin/bash @HOME_ROOT@/case-b']},
            'note': 'INTERFACE 5: auto numbers are assigned in line order and not promised'},
        'D-latest-native-lines': unsupported('INTERFACE 5: no "newest version" selector; a package line always names a version'),
        'D-external-accounts-native-lines': unsupported('INTERFACE 5: no account server (question 9)'),
        'D-radio-native-lines': unsupported('INTERFACE 5: no saved Wi-Fi networks or Bluetooth pairings; no radio stack in the virtual machine base'),
        'D-shared-native-lines': unsupported('INTERFACE 5 and 8: a package line installs exactly that package; '
            'there is no run-time dependency between package lines, so no package is shared by two owners'),
        'optional-no-exec': unsupported('INTERFACE 5: there is no prohibition line; the default already refuses (EXECUTORS.md)'),
        'case-child': unsupported('INTERFACE 5 and EXECUTORS.md: no container runtime in 0.68'),
        'slow-package': unsupported('INTERFACE 5 and 8: confos apply builds a package from a recipe and sources that lie '
            'beside the declaration; an installation by a line transfers nothing over the network, so it cannot be '
            'interrupted by losing the network'),
    }
    lines.update(update_slots(a, old, base))
    layout, derivation = release_layout(a, old)
    data = {'schema': 1, 'release': '0.68', 'sources': sources, 'layout': layout, 'derivation': derivation,
            'account': {'name': 'user', 'uid': 1000, 'gid': 1000, 'home': '/home/user', 'shell': '/bin/bash'},
            'control_folder': '/home/user/control',
            'candidate': '/data/confos/declaration.conf',
            'private_tokens': ['@KEY_TYPE@', '@KEY@', '@SERVER@'],
            'lines': lines,
            'payload_sha256': {p.name: sha(p) for p in sorted((HERE / 'payloads').iterdir()) if p.is_file()}}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1, sort_keys=True) + '\n')
    print('wrote', OUT.relative_to(HERE), len(lines), 'slots,',
          sum('unsupported' in v for v in lines.values()), 'unsupported')


if __name__ == '__main__':
    main()

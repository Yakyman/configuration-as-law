"""c2, part 2: rule-decided rows (accounts, kernel modules, code packages, package-shipped system units).
Usage: python3 -I c2/scripts/part-2/rules.py   (run from A1/). Appends rows whose id is not yet in c2/part-2.tsv."""
import csv, os, re

IN = 'in/part-2.tsv'
OUT = 'c2/part-2.tsv'
HDR = ['id', 'decision', 'sentences', 'what_it_does', 'basis', 'reason']

rows = [r for r in csv.reader(open(IN, encoding='utf-8'), delimiter='\t')][1:]
done = set()
if os.path.exists(OUT):
    done = {r[0] for r in csv.reader(open(OUT, encoding='utf-8'), delimiter='\t')}

pinfo = {}
for l in open('c2/raw/part-2/package-info.tsv', encoding='utf-8'):
    f = l.rstrip('\n').split('\t')
    pinfo[f[0]] = f
CODE = re.compile(r'\b(bin|lib_so|libexec|py|pm|ko|vmlinuz|efi)=')

# packages decided row by row (not by the rule)
MANUAL_PKG = {'base-files', 'cloud-initramfs-growroot', 'cloud-utils', 'dbus-session-bus-common',
              'dbus-system-bus-common', 'debian-archive-keyring', 'distro-info-data', 'gcc-12-base',
              'grub-cloud-amd64', 'init', 'libaudit-common', 'libc-l10n', 'libmagic-mgc', 'libpython3-stdlib',
              'libsemanage-common', 'libtirpc-common', 'linux-image-6.1.0-56-cloud-amd64',
              'linux-image-cloud-amd64', 'manpages', 'media-types', 'ncurses-base', 'netbase', 'pci.ids',
              'python-apt-common', 'readline-common', 'runit-helper', 'systemd-timesyncd', 'tzdata',
              'usr-is-merged'}
# system units decided row by row
MANUAL_UNIT = re.compile(r'^(initrd|systemd-pcrphase|netplan-ovs-cleanup|systemd-growfs@)')


def words(s, n=15):
    w = s.replace('\t', ' ').split()
    return ' '.join(w[:n])


def decide(r):
    rid, part, machine, kind, name, members, ev = r
    if kind == 'account':
        uid = re.search(r'uid=(\d+)', ev).group(1)
        return ['MUST', 'S2.2-15', words('account %s (uid %s): identity under which processes run and files are owned' % (name, uid)),
                'raw:accounts.txt', 'S2.2-15 states that accounts must be recorded; this is an account of the system account database.']
    if kind == 'kernel-module':
        return ['MUST', 'S2.2-10,S2.1-3', words('loaded kernel module %s: kernel code running with kernel rights' % name),
                'raw:modules.txt', 'A loaded module is code the kernel executes with its own rights, so it can do whatever the kernel can (S2.2-10).']
    if kind == 'package':
        pn = name.split(':')[0]
        if pn in MANUAL_PKG:
            return None
        f = pinfo[pn]
        if not CODE.search(f[2]):
            raise SystemExit('package without code not in MANUAL_PKG: ' + pn)
        return ['MUST', 'S2.2-9,S2.2-10,S2.2-2', words('installs ' + f[4].split('  ')[0], 15),
                'doc:https://packages.debian.org/bookworm/' + pn,
                'Ships programs or libraries/modules (file list: %s); programs that can run and code programs execute must be recorded; removal makes them impossible.'
                % ' '.join(x.split('=')[0] for x in f[2].split() if CODE.search(x + ' '))]
    if kind == 'system-unit':
        if MANUAL_UNIT.search(name):
            return None
        m = re.search(r'loaded (\S+) (\S+) (.*?); fragment=(\S+);', ev)
        desc = m.group(3); frag = m.group(4)
        if not (frag.startswith('/lib/systemd/system/') or frag.startswith('/usr/lib/systemd/system/')):
            raise SystemExit('unexpected fragment ' + rid)
        return ['MUST', 'S2.1-3,S2.2-1,S2.2-2', words('systemd unit "%s" (%s %s), defined by packaged unit file' % (desc, m.group(1), m.group(2))),
                'raw:units.txt',
                'Unit the service manager loaded and can start on this machine; removal makes starting its service, mount, socket, timer or target impossible (S2.2-2).']
    return None


new = []
for r in rows:
    if r[0] in done:
        continue
    d = decide(r)
    if d:
        new.append([r[0]] + d)
write_hdr = not os.path.exists(OUT) or os.path.getsize(OUT) == 0
with open(OUT, 'a', encoding='utf-8', newline='') as f:
    pass
    if write_hdr:
        f.write("\t".join(HDR) + "\n")
    for n in new:
        assert all('\t' not in x and '\n' not in x for x in n), n
        f.write("\t".join(n) + "\n")
print('appended', len(new))

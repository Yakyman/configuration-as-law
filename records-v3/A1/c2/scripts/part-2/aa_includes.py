"""Run on the server: recursive include closure of the AppArmor profiles shipped in /etc/apparmor.d (from extracted debs)."""
import os, re, sys
root = 'debs/all/etc/apparmor.d'
profiles = ['lsb_release', 'nvidia_modprobe', 'sbin.dhclient', 'usr.bin.man', 'usr.bin.tcpdump']
inc = re.compile(r'^\s*#?include\s+(?:if exists\s+)?[<"]([^>"]+)[>"]')
seen = set()
def walk(rel):
    p = os.path.join(root, rel)
    targets = []
    if os.path.isdir(p):
        targets = [os.path.join(rel, f) for f in sorted(os.listdir(p))]
    elif os.path.isfile(p):
        targets = [rel]
    for t in targets:
        if t in seen:
            continue
        seen.add(t)
        if os.path.isdir(os.path.join(root, t)):
            walk(t); continue
        for line in open(os.path.join(root, t), errors='replace'):
            m = inc.match(line)
            if m:
                walk(m.group(1))
for pr in profiles:
    walk(pr)
for s in sorted(seen):
    print(s)

import gzip, re
from collections import defaultdict
files=defaultdict(list)
for l in gzip.open('raw/mint/pkgfiles.tsv.gz','rt'):
    n,p=l.rstrip('\n').split('\t',1); files[n].append(p)
STRONG=re.compile(r'^(usr/)?s?bin/|^usr/games/|^usr/libexec/|\.so(\.[0-9.]+)?$|\.ko(\.(zst|xz|gz))?$|^(usr/)?lib/firmware/|^(usr/)?lib/modules/|\.(py|pl|pm|rb|sh|lua|jar|pyc|tcl|bash)$|^usr/lib/python3|^usr/share/perl|^(usr/)?lib/systemd/|^etc/init\.d/|^boot/|^usr/lib/grub/')
DOC=re.compile(r'^usr/share/(doc|doc-base|man|info|help|gtk-doc|lintian|bug)/')
for n,fs in sorted(files.items()):
    s=[p for p in fs if STRONG.search(p)]
    s2=[p for p in s if not DOC.search(p)]
    if s and not s2: print('DOCONLY-STRONG',n,s[:2])
    if s2 and re.search(r'-(dbg|dbgsym|doc)$',n): print('DBG/DOC',n,s2[:2])
    if s2 and all(re.search(r'\.so$',p) and '/x86_64-linux-gnu/' in p for p in s2): print('DEVSO',n,s2[:1])

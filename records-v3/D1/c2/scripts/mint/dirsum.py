import csv, sys, gzip, re
from collections import defaultdict, Counter
r={x['pkg']:x for x in csv.DictReader(open('raw/mint/pkgclass.tsv'),delimiter='\t')}
files=defaultdict(list)
for l in gzip.open('raw/mint/pkgfiles.tsv.gz','rt'):
    n,p=l.rstrip('\n').split('\t',1); files[n].append(p)
STRONG=re.compile(r'^(usr/)?s?bin/|^usr/games/|^usr/libexec/|\.so(\.[0-9.]+)?$|\.ko(\.(zst|xz|gz))?$|^(usr/)?lib/firmware/|^(usr/)?lib/modules/|\.(py|pl|pm|rb|sh|lua|jar|pyc|tcl|bash)$|^usr/lib/python3|^usr/share/perl|^(usr/)?lib/systemd/|^etc/init\.d/|^boot/|^usr/lib/grub/')
out=open('raw/mint/nonstrong-dirsum.txt','w')
for n,x in sorted(r.items()):
    fs=files[n]
    if any(STRONG.search(p) for p in fs): continue
    c=Counter()
    for p in fs:
        if p.startswith('usr/share/doc/'): continue
        parts=p.split('/')
        k='/'.join(parts[:min(4,len(parts)-1)]) if len(parts)>1 else p
        c[k]+=1
    ex=[p for p in fs if not p.startswith('usr/share/doc/')][:3]
    out.write(f"{n} [{x['section']}] {x['desc']}\n   " + '; '.join(f'{k}:{v}' for k,v in c.most_common(8)) + '\n   ex: ' + ' '.join(ex)[:220] + '\n')

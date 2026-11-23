import csv, sys, gzip, re
from collections import defaultdict
r={x['pkg']:x for x in csv.DictReader(open('raw/mint/pkgclass.tsv'),delimiter='\t')}
files=defaultdict(list)
for l in gzip.open('raw/mint/pkgfiles.tsv.gz','rt'):
    n,p=l.rstrip('\n').split('\t',1); files[n].append(p)
mode=sys.argv[1]
STRONG=re.compile(r'^(usr/)?s?bin/|^usr/games/|^usr/libexec/|\.so(\.[0-9.]+)?$|\.ko(\.(zst|xz|gz))?$|^(usr/)?lib/firmware/|^(usr/)?lib/modules/|\.(py|pl|pm|rb|sh|lua|jar|pyc|tcl|bash)$|^usr/lib/python3|^usr/share/perl|^(usr/)?lib/systemd/|^etc/init\.d/|^boot/|^usr/lib/grub/')
for n,x in sorted(r.items()):
    nc=int(x['n_code'])
    if mode=='doc' and nc==0 and x['data_classes']=='':
        print(n, x['n_files'], '|', x['desc'], '|', ' '.join(p for p in files[n] if not p.startswith('usr/share/doc/')
)[:150])
    if mode=='data' and nc==0 and x['data_classes']!='':
        print(n, x['data_classes'], '|', x['desc'])
    if mode=='weak' and nc>0 and not any(STRONG.search(p) for p in files[n]):
        cp=[p for p in files[n] if not p.startswith('usr/share/doc')]
        print(n, '|', x['desc'], '|', ' '.join(cp)[:200])

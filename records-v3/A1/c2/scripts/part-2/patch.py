"""Patch fields of rows already in c2/part-2.tsv (own corrections). Usage: python3 -I c2/scripts/part-2/patch.py"""
OUT = 'c2/part-2.tsv'
DCI = 'doc:https://salsa.debian.org/cloud-team/debian-cloud-images/-/tree/cc29a4adc3366b4739b388dc862fd17bad6c2835/config_space/12/files/etc'
TMPF = 'doc:https://packages.debian.org/bookworm/systemd'
patch = {
    'debian-b20e807939': {1: 'NOT', 5: 'Package indexes and lock behave as cache apt fetches again (S2.2-5); extended_states is apt\'s program state, outside the definition (S2.5-1).'},
    'debian-7b1b0b20fe': {5: 'MUST: five loaded profiles, abi/3.0, the 29 abstraction and tunable files they include, and their directories (access rules applied). NOT: about 120 never-included files and empty directories.'},
}
lines = open(OUT, encoding='utf-8').read().split('\n')
out = []
for l in lines:
    if not l:
        continue
    f = l.split('\t')
    if f[0] in patch:
        for k, v in patch[f[0]].items():
            f[k] = v
    if f[4] == 'raw:../../c2/raw/part-2/debian-cloud-images-files.txt':
        f[4] = DCI
    if f[4] == 'raw:../../c2/raw/part-2/debian12-tmpfiles.txt':
        f[4] = TMPF
    assert len(f[5].split()) <= 30, f[0]
    out.append('\t'.join(f))
open(OUT, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('rows', len(out))

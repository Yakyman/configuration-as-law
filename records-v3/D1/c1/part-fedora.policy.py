import csv
import json
from pathlib import Path
from collections import Counter

base = Path('D1/c1')
kinds = {'L1:group', 'L1:polkit-actions', 'L1:firewall-table', 'L1:firewall-chain', 'L1:firewall-ct helper', 'L1:firewall-rule'}
rows = [r for r in csv.DictReader(open('D1/in/part-fedora.tsv'), delimiter='\t') if r['kind'] in kinds]
rules = [json.loads(r['members'])[0] for r in rows if r['kind'] == 'L1:firewall-rule']
counts = Counter(r['chain'] for r in rules)
targets = Counter(e[k]['target'] for r in rules for e in r['expr'] for k in ('jump', 'goto') if k in e)
raw = json.load(open('D1/in/raw/fedora/raw/080-firewall-nft.out'))['nftables']
for r in rows:
    if r['kind'].startswith('L1:firewall-'):
        k = r['kind'].removeprefix('L1:firewall-')
        assert {k: json.loads(r['members'])[0]} in raw

out = base / 'part-fedora.policy.tsv'
header = ['id', 'decision', 'sentences', 'what_it_does', 'basis', 'reason']
done = set()
if out.exists():
    done = {r['id'] for r in csv.DictReader(out.open(), delimiter='\t')}
with out.open('a', newline='') as f:
    writer = csv.writer(f, delimiter='\t', lineterminator='\n')
    if f.tell() == 0:
        writer.writerow(header)
    for r in rows:
        if r['id'] in done:
            continue
        kind = r['kind']
        sentences = 'S2.2-1,S2.2-2'
        basis = 'raw:D1/in/' + r['evidence'].split(':')[0]
        if kind == 'L1:group':
            what = 'Defines a system group identity, numeric identifier, and supplementary membership list.'
            reason = 'Removing this identity prevents resolving its group name for ownership and group selection; these are system operations, not merely unavailable content.'
        elif kind == 'L1:polkit-actions':
            what = 'Registers an operation for cross-process authorization checks through polkit.'
            basis = 'doc:https://polkit.pages.freedesktop.org/polkit/polkit.8.html'
            reason = 'Mechanisms must declare actions to use polkit; removal prevents authorization checks for this operation. Registration does not itself grant permission.'
        elif kind == 'L1:firewall-rule':
            sentences = 'S2.2-15'
            what = 'Applies a kernel firewall matching, verdict, dispatch, or connection-tracking instruction.'
            reason = 'Firewall rules are explicitly required, including dispatch rules whose target currently contains no filtering rules.'
        elif kind == 'L1:firewall-chain':
            c = json.loads(r['members'])[0]
            if 'hook' in c:
                assert counts[c['name']]
                what = 'Connects firewall rules to a packet-processing hook with priority and default verdict.'
                reason = 'Removal disconnects its existing firewall instructions from the networking stack, changing packet processing.'
            else:
                assert targets[c['name']]
                what = 'Provides the target for existing firewall jumps and holds an ordered rule sequence.'
                reason = 'Existing firewall jumps require this target; removing it makes those instructions impossible, even when its rule sequence is empty.'
        elif kind == 'L1:firewall-table':
            what = 'Contains the active firewall chains, rules, and connection-tracking helper.'
            reason = 'Removing this populated table removes its packet-processing configuration and therefore stops the computer applying those firewall decisions.'
        else:
            what = 'Defines the NetBIOS UDP connection-tracking helper selected by a firewall rule.'
            reason = 'The existing UDP port 137 rule selects this helper; removing it prevents that protocol-specific connection-tracking operation.'
        assert len(what.split()) <= 15
        assert len(reason.split()) <= 30
        writer.writerow([r['id'], 'MUST', sentences, what, basis, reason])
        f.flush()

written = list(csv.DictReader(out.open(), delimiter='\t'))
assert Counter(r['id'] for r in rows) == Counter(r['id'] for r in written)
assert all(r['decision'] in {'MUST', 'NOT', 'HOLE', 'UNKNOWN', 'MIXED'} for r in written)
assert all(n == 1 for n in Counter(r['id'] for r in written).values())
print(len(written), dict(Counter(r['decision'] for r in written)))

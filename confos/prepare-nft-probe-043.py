#!/usr/bin/python3
"""Prepare a canonical accept/drop probe without changing the proven candidate."""
from pathlib import Path
source = Path('nft-recording-probe.py').read_text()
assert source.count("add=['nft','add','rule','inet','confos','input','tcp','dport','32124','accept']") == 1
source = source.replace("add=['nft'", "verdict=sys.argv[2] if len(sys.argv)>2 else 'accept'\nassert verdict in ('accept','drop')\nadd=['nft'")
source = source.replace("'32124','accept']", "'32124',verdict]")
source = source.replace("b'add rule inet confos input tcp dport 32124 accept'", "('add rule inet confos input tcp dport 32124 '+verdict).encode()")
source = source.replace("rule=selected();assert len(rule)==1", "rule=selected();assert len(rule)==1 and rule[0]['expr'][-1]=={verdict:None}")
source = source.replace('duplicate=before+b"rule duplicate \'add rule inet confos input tcp dport 32124 accept\'\\n"', 'duplicate=before+("rule duplicate \'add rule inet confos input tcp dport 32124 "+verdict+"\'\\n").encode()')
source = source.replace("elif mode=='removed':", "elif mode=='verified':\n rule=selected();assert len(rule)==1 and rule[0]['expr'][-1]=={verdict:None}\n assert ('add rule inet confos input tcp dport 32124 '+verdict).encode() in declaration()\nelif mode=='removed':")
assert '32124 accept' not in source
compile(source, 'nft-recording-probe-043.py', 'exec')
Path('nft-recording-probe-043.py').write_text(source)
print('CANONICAL43 NFT ACCEPT DROP PROBE PREPARED; NOT RUN')

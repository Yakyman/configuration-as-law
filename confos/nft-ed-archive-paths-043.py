#!/usr/bin/python3
"""NUL-separated exact native inputs and portable proof for canonical43."""
import hashlib,json,sys
from pathlib import Path
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
assert Path('VERSION').read_text().strip() in ('0.43','0.44','0.45','0.46','0.47','0.48','0.49')
metadata=Path('ed-reader-metadata-draft.json')
assert digest(metadata)=='4b2f8944bc7bcfa3ac82212039ceca6b508f77909ca56ad50faf6158271350e1'
ed=json.loads(metadata.read_text());work=Path('interpreter-inputs/ed-reader-draft')
assert not (work/'guest').exists() and not list(work.glob('build-tree*'))
assert not list(work.rglob('*.qcow2'))
for item in ed['inputs']+ed['licences']+ed['recipe']+[ed['reader_policy']]:
    assert digest(Path(item['path']))==item['sha256'],item['path']
assert digest(Path(ed['candidate_path']))==ed['sha256']
nft=json.loads(Path('nft-recording-metadata.json').read_text())
assert digest(Path('nft-recording-query-draft'))==nft['nft-recording-query-draft']=='ce46c183470ca81f20436f0c92850a741b9adddbbad3b6236cd8fff0c8b0d140'
names=['prepare-nft-ed-component-043.py','check-reader-inheritance-043.py',
 'advance-nft-ed-043.py','document-nft-ed-043.py','sync-nft-ed-043.sh',
 'prepare-nft-ed-043.sh','archive-nft-ed-043.sh','cleanup-nft-ed-043.sh','fetch-nft-ed-evidence-043.sh',
 'build-nft-ed-fixture-043.py','nft-ed-archive-paths-043.py','probe-nft-ed-043.sh',
 'ed-root-probe-043.py','nft-recording-probe-043.py','prepare-nft-probe-043.py',
 'ed-reader-metadata-draft.json','ed-reader-draft.md',
 'nft-recording-query-draft','nft-recording-metadata.json','nft-recording-evidence.tar.gz',
 'NFT-RECORDING-DRAFT.md','NFT-RECORDING-RESULTS.md','nft-recording-private-build.py',
 'nft-recording-private-run.sh','nft-recording-probe.py','nft-recording-collect.py',
 'packages/confos-code-readers_0.42_amd64.deb','packages/confos-code-readers_0.42_amd64.deb.sha256',
 'records/reader-inheritance-0.43.json']
names += [item['path'] for item in ed['inputs']+ed['recipe']]
names += [str(work/name) for name in ('candidate','original','source','evidence','input-pins.json',
 'source-index.txt','binary-index.txt','metadata.json','comparison.json','build-provenance.json',
 'ed-reader.patch','code-file-policy.h','original-dynamic.txt','candidate-dynamic.txt',
 'original-symbols.txt','candidate-symbols.txt',ed['guest_libraries']['archive'])]
# Raw private build logs are deliberately excluded; evidence contains normalized copies.
for name in dict.fromkeys(names):
    assert Path(name).exists(),name
    sys.stdout.buffer.write(name.encode()+b'\0')

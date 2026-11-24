from pathlib import Path
import hashlib,shutil,subprocess as sp,tarfile,json
root=Path(__file__).resolve().parent;work=root/'nft-recording-private';log=root/'logs/nft-recording-private.log'
assert 'NFT RECORDING PRIVATE MATRIX PASS' in log.read_text()
assert sp.run(['systemctl','--user','is-active','--quiet','confos-nft-recording-private-retry']).returncode!=0
for proc in Path('/proc').glob('[0-9]*'):
 try:
  if proc.joinpath('comm').read_text().strip().startswith('qemu-system'):
   assert str(work/'disk.qcow2').encode() not in proc.joinpath('cmdline').read_bytes(),'private guest remains'
 except (FileNotFoundError,PermissionError):pass
paths=[root/'nft-recording-query-draft',root/'nft-recording-private-build.py',root/'nft-recording-private-run.sh',root/'nft-recording-probe.py',log,root/'logs/nft-recording-private.serial',root/'logs/nft-recording-launch-failure.log',work/'inputs/declaration.conf',work/'source/packages/confos-runtime_0.41_all.deb',work/'source/packages/confos-runtime_0.41_all.deb.sha256']
meta={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
(root/'nft-recording-metadata.json').write_text(json.dumps(meta,indent=2)+'\n');paths.append(root/'nft-recording-metadata.json')
with tarfile.open(root/'nft-recording-evidence.tar.gz','w:gz') as tar:
 for p in paths:tar.add(p,arcname=str(p.relative_to(root)),recursive=False)
print('EVIDENCE SHA256',hashlib.sha256((root/'nft-recording-evidence.tar.gz').read_bytes()).hexdigest())
print('CLEANING',work);shutil.rmtree(work)

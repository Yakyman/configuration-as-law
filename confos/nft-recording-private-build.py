from pathlib import Path
import hashlib,shutil,subprocess as sp,tarfile
root=Path(__file__).resolve().parent;work=root/'nft-recording-private';source=work/'source'
used=int(sp.check_output(['du','-s','--block-size=1',str(root)]).split()[0]);print('BUILD TREE BYTES',used,flush=True)
assert used<51*1024**3
assert not work.exists();source.mkdir(parents=True)
archive=root/'releases/confos-0.41-source.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='2c73f6a664a2754cc78a7244d31bb77c7ac3d5253f45653a3c12cdfb418e4ca9'
with tarfile.open(archive) as tar:
 members=[m for m in tar.getmembers() if len(Path(m.name).parts)==1 or Path(m.name).parts[0] in ('components','examples','packages')]
 assert sum(m.size for m in members)<2*1024**3
 tar.extractall(source,members=members,filter='data')
assert (source/'VERSION').read_text()=='0.41\n'
print('ORIGINAL NFT QUERY',hashlib.sha256((source/'nft-query').read_bytes()).hexdigest(),flush=True)
shutil.copyfile(root/'nft-recording-query-draft',source/'nft-query')
sp.run(['python3','package-base.py','packages/confos-runtime_0.41_all.deb'],cwd=source,check=True)
inputs=work/'inputs';shutil.copytree(source/'examples',inputs)
shutil.copyfile(inputs/'development.conf',inputs/'declaration.conf')
sp.run(['bash','build.sh',str(inputs/'declaration.conf'),str(work/'disk.qcow2')],cwd=source,check=True)
print('NFT RECORDING PRIVATE IMAGE BUILT',flush=True)

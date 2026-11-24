from pathlib import Path
import hashlib,shutil,subprocess as sp,tarfile
root=Path(__file__).resolve().parent;work=root/'visudo-recording-private';source=work/'source'
used=int(sp.check_output(['du','-s','--block-size=1',str(root)]).split()[0]);print('BUILD TREE BYTES',used,flush=True);assert used<51*1024**3
assert not work.exists();source.mkdir(parents=True)
archive=root/'releases/confos-0.41-source.tar.gz';assert hashlib.sha256(archive.read_bytes()).hexdigest()=='2c73f6a664a2754cc78a7244d31bb77c7ac3d5253f45653a3c12cdfb418e4ca9'
with tarfile.open(archive) as tar:
 members=[m for m in tar.getmembers() if len(Path(m.name).parts)==1 or Path(m.name).parts[0] in ('components','examples','packages')];assert sum(m.size for m in members)<2*1024**3;tar.extractall(source,members=members,filter='data')
shutil.copyfile(root/'visudo-recording-command-draft',source/'visudo-recording-command')
def change(file,old,new):
 p=source/file;s=p.read_text();assert s.count(old)==1,(file,old);print('PATCH INPUT',file,hashlib.sha256(p.read_bytes()).hexdigest(),flush=True);p.write_text(s.replace(old,new))
change('package-base.py',"RUNTIME = (", "RUNTIME = ('visudo-recording-command', ")
change('package-base.py',"{'apt': 'apt-command'", "{'visudo': 'visudo-recording-command', 'apt': 'apt-command'")
change('package-base.py', "if command in ('nft',", "if command in ('visudo', 'nft',")
change('recording.py',"'usermod', 'userdel', 'systemctl')", "'usermod', 'userdel', 'systemctl', 'visudo')")
change('assemble.py',"installers.run_in_root(root, '/usr/sbin/visudo', '-c')", "installers.run_in_root(root, '/usr/lib/confos/native/visudo', '-c')")
sp.run(['python3','package-base.py','packages/confos-runtime_0.41_all.deb'],cwd=source,check=True)
inputs=work/'inputs';shutil.copytree(source/'examples',inputs);shutil.copyfile(inputs/'development.conf',inputs/'declaration.conf')
editor=b'#!/bin/sh\ncat /proc/self/attr/current >&2\ncat > "$1"\n'
(inputs/'test-editor').write_bytes(editor)
with (inputs/'declaration.conf').open('a') as stream:stream.write('file /usr/local/bin/visudo-test-editor 0755 0:0 '+hashlib.sha256(editor).hexdigest()+' test-editor\n')
sp.run(['bash','build.sh',str(inputs/'declaration.conf'),str(work/'disk.qcow2')],cwd=source,check=True)
print('VISUDO RECORDING PRIVATE IMAGE BUILT',flush=True)

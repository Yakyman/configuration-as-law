#!/usr/bin/python3
import hashlib,shutil,subprocess
from pathlib import Path
base=source=Path.cwd()
assert Path('VERSION').read_text().strip()=='0.39'
declaration=source/'examples/flatpak-readers-039.conf'
text=(source/'examples/development.conf').read_text()
text+='package flatpak 1.16.6-1~deb13u3\npackage util-linux 2.41.5-0+deb13u1\npackage gpg 2.4.7-21+deb13u1+b5\npackage gpg-agent 2.4.7-21+deb13u1+b5\n'
for name,ref,commit in [('runtime','runtime/org.freedesktop.Platform/x86_64/26.08','df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c'),('mpv','app/io.mpv.Mpv/x86_64/stable','13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc')]:
 p=base/'flatpak-inputs'/f'{name}.flatpak'
 shutil.copyfile(p,source/'examples'/p.name)
 text+=f'flatpak {ref} {commit} {hashlib.sha256(p.read_bytes()).hexdigest()} {p.name}\n'
for name,data,target in [('recorded-flatpak-bash.sh',b'echo RECORDED-BASH-RAN\n','/home/user/bin/recorded-flatpak-bash.sh'),('recorded-flatpak-python.py',b'print("RECORDED-PYTHON-RAN")\n','/home/user/bin/recorded-flatpak-python.py'),('recorded_flatpak_module.py',b'print("RECORDED-PYTHON-RAN")\n','/home/user/bin/recorded_flatpak_module.py')]:
 (source/'examples'/name).write_bytes(data)
 text+=f'file {target} 0644 0:0 {hashlib.sha256(data).hexdigest()} {name}\n'
 if name=='recorded-flatpak-bash.sh':
  text+=f'file /home/user/bin/login/.bash_profile 0644 0:0 {hashlib.sha256(data).hexdigest()} {name}\n'
declaration.write_text(text)
print('CANONICAL39 FIXTURE DECLARATION',hashlib.sha256(declaration.read_bytes()).hexdigest(),flush=True)
subprocess.run(['bash',source/'build.sh',declaration,source/'images/flatpak-readers-039.qcow2'],check=True)
print('CANONICAL39 FLATPAK FIXTURE IMAGE BUILT',flush=True)


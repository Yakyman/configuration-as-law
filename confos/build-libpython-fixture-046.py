#!/usr/bin/python3
import hashlib,json,shutil,subprocess as sp
from pathlib import Path
root=Path.cwd();source=root;work=root/'libpython-046-fixture'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
assert Path('VERSION').read_text()=='0.46\n'
assert not work.exists();work.mkdir()
inputs=work/'inputs';shutil.copytree(source/'examples',inputs)
sp.run(['gcc','-O2','-Wall','-Wextra','-Werror','-Wl,--build-id=none','-o',str(inputs/'embedded-python'),str(root/'embedded-python-probe.c'),'-ldl'],check=True)
sp.run(['readelf','-d',str(inputs/'embedded-python')],check=True)
code=b'import os\nprint("EMBEDDED-CODE",os.geteuid(),open("/proc/self/attr/current").read().strip())\nopen("/tmp/embedded-python-marker","w").close()\n'
(inputs/'recorded.py').write_bytes(code)
shutil.copyfile(root/'libpython-guest-private-probe.py',inputs/'probe.py')
rows=[r for r in (inputs/'development.conf').read_text().splitlines() if r.startswith(('base ','snapshot ','account ','authorized-key '))]
rows.append('package libpython3.13 3.13.5-2+deb13u5')
for name,target,mode in [('embedded-python','/usr/local/bin/embedded-python','0755'),('recorded.py','/usr/local/share/embedded-recorded.py','0644'),('probe.py','/usr/local/bin/embedded-python-private-probe.py','0644')]:
 rows.append(f'file {target} {mode} 0:0 {sha(inputs/name)} {name}')
for name in ('recorded-filename-reader.py','probe-recorded-filename-reader.py'):
 shutil.copyfile(root/name,inputs/name)
 rows.append(f'file /usr/local/share/{name} 0644 0:0 {sha(inputs/name)} {name}')
(inputs/'declaration.conf').write_text('\n'.join(rows)+'\n')
sp.run(['bash','build.sh',str(inputs/'declaration.conf'),'images/libpython-046.qcow2'],check=True)
assert sha(root/'images/libpython-046.work/root/usr/lib/x86_64-linux-gnu/libpython3.13.so.1.0')=='e21f94b1ccdaed10a83120d9150a4efd162e847d484383f57e79ff777e29328b'
print('CANONICAL46 LIBPYTHON FIXTURE BUILT')

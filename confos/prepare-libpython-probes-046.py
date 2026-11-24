#!/usr/bin/python3
from pathlib import Path
text=Path('embedded-python-private-build.py').read_text()
tail=text[text.index("inputs=work/'inputs'"):text.index("(work/'composition.json')")]
tail=tail.replace("root/'embedded-python-private-probe.py'","root/'libpython-guest-private-probe.py'")
tail=tail.replace("(inputs/'declaration.conf').write_text",'''for name in ('recorded-filename-reader.py','probe-recorded-filename-reader.py'):
 shutil.copyfile(root/name,inputs/name)
 rows.append(f'file /usr/local/share/{name} 0644 0:0 {sha(inputs/name)} {name}')
(inputs/'declaration.conf').write_text''')
prefix='''#!/usr/bin/python3
import hashlib,json,shutil,subprocess as sp
from pathlib import Path
root=Path.cwd();source=root;work=root/'libpython-046-fixture'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
assert Path('VERSION').read_text()=='0.46\\n'
assert not work.exists();work.mkdir()
'''
suffix='''sp.run(['bash','build.sh',str(inputs/'declaration.conf'),'images/libpython-046.qcow2'],check=True)
assert sha(root/'images/libpython-046.work/root/usr/lib/x86_64-linux-gnu/libpython3.13.so.1.0')=='e21f94b1ccdaed10a83120d9150a4efd162e847d484383f57e79ff777e29328b'
print('CANONICAL46 LIBPYTHON FIXTURE BUILT')
'''
Path('build-libpython-fixture-046.py').write_text(prefix+tail+suffix)
print('CANONICAL46 FIXTURE RECIPE PREPARED')

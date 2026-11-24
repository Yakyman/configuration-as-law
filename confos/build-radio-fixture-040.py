#!/usr/bin/python3
from pathlib import Path
import hashlib,json,shutil,subprocess as sp
assert Path('VERSION').read_text()=='0.40\n'
work=Path('radio-040-fixture');work.mkdir(exist_ok=True)
for p in Path('radio-public-fixture').iterdir():
    if p.is_file(): shutil.copyfile(p,work/p.name)
probe=Path('radio-mutation-probe.py').read_bytes();(work/'radio-mutation-probe.py').write_bytes(probe)
rows=[line for line in Path('examples/development.conf').read_text().splitlines() if line.startswith(('base ','snapshot ','account ','authorized-key '))]
rows+=(work/'packages.conf').read_text().splitlines()
rows+=(work/'radio-draft.conf').read_text().splitlines()
rows.append('file /usr/local/bin/radio-mutation-probe.py 0644 0:0 '+hashlib.sha256(probe).hexdigest()+' radio-mutation-probe.py')
# Alternative client address exercises a real setting change, with exact saved input.
client=json.loads((work/'client.json').read_text());client['address']='192.0.2.3/24'
alt=(json.dumps(client,sort_keys=True)+'\n').encode();(work/'client-alt.json').write_bytes(alt)
rows.append('file /usr/local/share/radio-client-alt.json 0600 0:0 '+hashlib.sha256(alt).hexdigest()+' client-alt.json')
(work/'normal.conf').write_text('\n'.join(rows)+'\n')
unit=b'[Unit]\nDescription=ConfOS radio control confinement probe\n[Service]\nType=oneshot\nRemainAfterExit=yes\nExecStart=/usr/bin/python3 /usr/local/bin/radio-mutation-probe.py\n'
(work/'radio-controls.service').write_bytes(unit)
systemd=rows+['package systemd 257.13-1~deb13u1','package util-linux 2.41.5-0+deb13u1','user-unit user radio-controls.service enabled '+hashlib.sha256(unit).hexdigest()+' radio-controls.service']
(work/'systemd.conf').write_text('\n'.join(systemd)+'\n')
for kind in ('normal','systemd','replica'):
    declaration = 'normal' if kind == 'replica' else kind
    sp.run(['bash','build.sh',str(work/(declaration+'.conf')),'images/radio-040-'+kind+'.qcow2'],check=True)
sp.run(['python3','compare-clean-trees.py','images/radio-040-normal.work','images/radio-040-replica.work'],check=True)
assert Path('images/radio-040-normal.work/root.sqfs').read_bytes() == Path('images/radio-040-replica.work/root.sqfs').read_bytes()
assert Path('images/radio-040-normal.work/initramfs').read_bytes() == Path('images/radio-040-replica.work/initramfs').read_bytes()
print('RADIO INDEPENDENT CLEAN PAYLOAD EQUALITY PASS',flush=True)

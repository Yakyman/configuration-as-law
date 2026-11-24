#!/usr/bin/python3
import hashlib,json,os,shutil,subprocess as sp
from pathlib import Path
root=Path.cwd();source=root;work=root/'radio-045-fixture'
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert Path('VERSION').read_text()=='0.45\n'
assert not work.exists();work.mkdir()
draft=root/'nmcli-command'
assert draft.read_bytes()==(root/'radio-recording-command-draft').read_bytes()
inputs=work/'inputs';shutil.copytree(source/'examples',inputs)
for p in (source/'radio-public-fixture').iterdir():
 if p.is_file():shutil.copyfile(p,inputs/p.name)
rows=[r for r in (inputs/'development.conf').read_text().splitlines() if r.startswith(('base ','snapshot ','account ','authorized-key '))]
rows+=(inputs/'packages.conf').read_text().splitlines()
rows += [r for r in (inputs/'radio-draft.conf').read_text().splitlines() if not r.startswith('network ')]
assert sum(r.startswith('radio-fixture ') for r in rows)==1 and sum(r.startswith('bluetooth-pair ') for r in rows)==2
for name,path in [('radio-recording-private-probe.py',root/'radio-recording-private-probe.py'),('radio-mutation-probe.py',source/'radio-mutation-probe.py')]:
 shutil.copyfile(path,inputs/name)
 rows.append(f'file /usr/local/bin/{name} 0644 0:0 {digest(inputs/name)} {name}')
meta={'draft_sha256':digest(draft),'fixture':json.loads((inputs/'fixture.json').read_text()),
      'radio_rows':[r for r in rows if r.startswith(('radio-fixture ','bluetooth-pair '))]}
(inputs/'radio-expected.json').write_text(json.dumps(meta,sort_keys=True)+'\n')
rows.append(f'file /usr/local/share/radio-recording-expected.json 0644 0:0 {digest(inputs/"radio-expected.json")} radio-expected.json')
(inputs/'declaration.conf').write_text('\n'.join(rows)+'\n')
sp.run(['bash','build.sh',str(inputs/'declaration.conf'),'images/radio-045.qcow2'],check=True)
guest=root/'images/radio-045.work/root'
assert digest(guest/'usr/lib/confos/commands/nmcli')==digest(draft)
assert os.readlink(guest/'usr/local/bin/nmcli')=='/usr/lib/confos/commands/nmcli'
print('CANONICAL45 RADIO FIXTURE BUILT',flush=True)

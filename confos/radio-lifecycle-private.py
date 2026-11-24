#!/usr/bin/python3
"""Worker-only bounded derivative of current source, not a numbered release."""
from pathlib import Path
import hashlib, importlib.util, shutil, subprocess as sp

root = Path(__file__).resolve().parent
work = root/'radio-lifecycle-private'
assert not work.exists(), 'inspect prior derivative before rerunning'
source = work/'source'
source.mkdir(parents=True)
for path in root.iterdir():
    if path.is_file():
        shutil.copy2(path, source/path.name)
for name in ('components', 'examples'):
    shutil.copytree(root/name, source/name)
for name in ('interpreter-inputs', 'appimage-inputs', 'flatpak-inputs'):
    if (root/name).exists(): (source/name).symlink_to(root/name, target_is_directory=True)
(source/'packages').mkdir()
version = (source/'VERSION').read_text().strip()
for path in (root/'packages').iterdir():
    if not path.name.startswith('confos-runtime_'):
        (source/'packages'/path.name).symlink_to(path)
spec = importlib.util.spec_from_file_location('draft',source/'advance-radio-release-040.py')
draft = importlib.util.module_from_spec(spec); spec.loader.exec_module(draft)
for name, text in draft.integrate().items():
    (source/name).write_text(text)
p=source/'runtime-init';text=p.read_text()
anchor='apparmor_parser -r /etc/confos/session.apparmor || exec /bin/bash\n'
assert text.count(anchor)==1
inject='''# PRIVATE LIFECYCLE TEST ONLY.
(
 while [ ! -f /run/radio-fault-request ]; do sleep 1; done
 radio_pid=$(cat /run/confos-radio.pid)
 kill -KILL "$radio_pid" || exit 1
 echo "RADIO TRUSTED FAULT INJECTED $radio_pid"
 for fault_attempt in {1..20}; do
  if [ ! -e /run/confos-ready ] && [ ! -e /run/confos-radio-ready.json ] && [ ! -e /run/confos-radio.pid ]; then
   echo 'RADIO TRUSTED READINESS FILES REVOKED'
   exit 0
  fi
  sleep 1
 done
 echo 'RADIO TRUSTED READINESS REVOCATION FAILED'
) &
'''
p.write_text(text.replace(anchor,anchor+inject))
inputs=work/'inputs';shutil.copytree(root/'radio-public-fixture',inputs)
rows=[r for r in (source/'examples/development.conf').read_text().splitlines() if r.startswith(('base ','snapshot ','account ','authorized-key '))]
rows+=(inputs/'packages.conf').read_text().splitlines()
rows+=(inputs/'radio-draft.conf').read_text().splitlines()
probe=(root/'radio-mutation-probe.py').read_bytes();(inputs/'probe.py').write_bytes(probe)
rows.append('file /usr/local/bin/radio-mutation-probe.py 0644 0:0 '+hashlib.sha256(probe).hexdigest()+' probe.py')
unit=b'[Service]\nType=oneshot\nRemainAfterExit=yes\nExecStart=/usr/bin/python3 /usr/local/bin/radio-mutation-probe.py\n'
(inputs/'probe.service').write_bytes(unit)
rows+=['package systemd 257.13-1~deb13u1','package util-linux 2.41.5-0+deb13u1','user-unit user radio-controls.service enabled '+hashlib.sha256(unit).hexdigest()+' probe.service']
(inputs/'declaration.conf').write_text('\n'.join(rows)+'\n')
sp.run(['python3','package-base.py','packages/confos-runtime_'+version+'_all.deb'],cwd=source,check=True)
sp.run(['bash','build.sh',str(inputs/'declaration.conf'),str(work/'disk.qcow2')],cwd=source,check=True)
print('PRIVATE RADIO LIFECYCLE DISK BUILT',flush=True)

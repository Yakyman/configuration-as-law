#!/bin/bash
# External builder fixture only; final delivery always uses build.py from source.
set -eu
cd "$(dirname "$0")/.."
export STAND_PREP_VM="${1:-prepare}"
python3 - <<'PY'
import json,os,pathlib,subprocess,tarfile
r=pathlib.Path.cwd();meta=json.loads((r/'vms'/os.environ['STAND_PREP_VM']/'meta.json').read_text())
base=['scp','-F','/dev/null','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','-i',str(r/'keys/guest'),'-P',str(meta['port'])]
files=[str(p) for p in (r/'build').iterdir() if p.is_file()]
subprocess.run(base+files+['root@127.0.0.1:/tmp/'],check=True)
archive=r/'build/channel-inputs.tar'
with tarfile.open(archive,'w') as tar:
 for folder,name in [('language','language'),('system','system-inputs'),('channels','channels')]:
  for p in (r/'downloads'/folder).iterdir():
   if p.is_file():tar.add(p,arcname=name+'/'+p.name)
subprocess.run(base+[str(archive),'root@127.0.0.1:/tmp/'],check=True);archive.unlink()
PY
python3 lab.py run "$STAND_PREP_VM" --root <<'GUEST'
set -eu
/usr/bin/systemctl stop stand-watchdog.timer
install -m 755 /tmp/stand.py /tmp/guard.py /tmp/codeboundary.py /tmp/codeverify.py /tmp/transactions.py /tmp/import_channels.py /tmp/job_channels.py /tmp/language_channels.py /tmp/app_channels.py /tmp/system_channels.py /tmp/language-selftest.py /tmp/app-selftest.py /tmp/system-selftest.py /tmp/round4-selftest.py /usr/local/lib/stand/
tar -xf /tmp/channel-inputs.tar -C /usr/local/share/stand
/usr/bin/python3 -B /tmp/language-native-fixture.py /usr/local/share/stand/language
test -f /usr/local/share/stand/channels/oci-hold.json || /usr/bin/python3 -B /tmp/app-fixtures.py
test -f /usr/local/share/stand/system/catalog.json || /usr/bin/python3 -B /tmp/system-fixtures.py catalog /usr/local/share/stand/system-inputs
/usr/bin/python3 - <<'PY'
import json,pathlib
p=pathlib.Path('/usr/local/share/stand/system/catalog.json');v=json.loads(p.read_text())
v['updates']['ed']['row']['native_arguments']={'/usr/bin/ed':['--version']}
p.write_text(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n')
PY
cp /etc/stand/authorized_keys /home/stand/.ssh/authorized_keys
/usr/bin/python3 -I /tmp/install-guard.py
/usr/bin/python3 -I /tmp/install-channels.py
/usr/bin/python3 -I /tmp/install-code-boundary.py
rm -rf /usr/local/share/stand/system-inputs
rm -f /tmp/channel-inputs.tar /var/lib/stand/current /var/lib/stand/last-success.json /var/lib/stand/pending.json
/usr/bin/python3 -B /usr/local/lib/stand/capture.py
stand-apply /etc/stand/factory
/usr/bin/systemctl start stand-watchdog.timer
GUEST

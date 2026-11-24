#!/usr/bin/python3
"""Prepare release45 plumbing; promotion itself requires the private guest pass."""
from pathlib import Path

private=Path('radio-recording-private-build.py').read_text()
tail=private[private.index("inputs=work/'inputs'"):private.index('composition={')]
tail=tail.replace("shutil.copytree(source/'examples',inputs)","shutil.copytree(source/'examples',inputs)")
prefix='''#!/usr/bin/python3
import hashlib,json,os,shutil,subprocess as sp
from pathlib import Path
root=Path.cwd();source=root;work=root/'radio-045-fixture'
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert Path('VERSION').read_text()=='0.45\\n'
assert not work.exists();work.mkdir()
draft=root/'nmcli-command'
assert draft.read_bytes()==(root/'radio-recording-command-draft').read_bytes()
'''
suffix='''sp.run(['bash','build.sh',str(inputs/'declaration.conf'),'images/radio-045.qcow2'],check=True)
guest=root/'images/radio-045.work/root'
assert digest(guest/'usr/lib/confos/commands/nmcli')==digest(draft)
assert os.readlink(guest/'usr/local/bin/nmcli')=='/usr/lib/confos/commands/nmcli'
print('CANONICAL45 RADIO FIXTURE BUILT',flush=True)
'''
Path('build-radio-recording-045.py').write_text(prefix+tail+suffix)
text=Path('radio-recording-private-run.sh').read_text()
start=text.index('[[ $#');end=text.index('confos_reserve_guest\n')
text=text[:start]+'''test "$(cat VERSION)" = 0.45
exec >logs/radio-recording-0.45.log 2>&1
source slots.sh
trap confos_stop_reserved EXIT
python3 build-radio-recording-045.py
'''+text[end:]
text=text.replace('radio-recording-private/disk.qcow2','images/radio-045.qcow2').replace('radio-recording-private/','radio-045-fixture/')
text=text.replace('22457','22458').replace('RADIO_RECORDING_PRIVATE44_SIX_CUT_MATRIX_PASS','CANONICAL45 RADIO RECORDING SIX CUTS PASS')
Path('probe-radio-recording-045.sh').write_text(text)
print('45 RECIPES PREPARED; NO PROMOTION')

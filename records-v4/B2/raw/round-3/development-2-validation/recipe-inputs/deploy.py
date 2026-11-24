#!/usr/bin/env python3
"""Host-side builder copy, derived paths and disposable VM metadata only."""
import json,pathlib,subprocess,sys
r=pathlib.Path(__file__).resolve().parent.parent
m=json.loads((r/'vms/builder/meta.json').read_text())
files=sys.argv[1:] or ['stand.py','policy.py','capture.py','install.sh']
base=['-F','/dev/null','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','-i',str(r/'keys/guest')]
subprocess.run(['ssh']+base+['-p',str(m['port']),'stand@127.0.0.1','sudo -n /usr/bin/systemctl stop fapolicyd'],check=True)
subprocess.run(['scp']+base+['-P',str(m['port'])]+[str(r/'build'/n) for n in files]+['stand@127.0.0.1:/tmp/'],check=True)

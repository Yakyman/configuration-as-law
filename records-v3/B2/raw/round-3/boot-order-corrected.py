from pathlib import Path
import subprocess,json
def lab(*args,**kw):return subprocess.run(['python3','lab.py',*args],check=True,**kw)
script="""python3 -I - <<'GUEST'
import json,pathlib,subprocess
def prop(unit,name):
 return subprocess.check_output(['/usr/bin/systemctl','show',unit,'-p',name,'--value'],text=True).strip()
gate=any('account' in line and 'requisite' in line and 'pam_exec.so' in line and '/run/stand-ready' in line for line in pathlib.Path('/etc/pam.d/common-account').read_text().splitlines() if not line.lstrip().startswith('#'))
assert gate and pathlib.Path('/run/stand-ready').exists() and int(prop('stand-replay.service','ActiveEnterTimestampMonotonic'))>0
print(json.dumps({'id':'BOOT-ORDER-READINESS','pam_account_gate':gate,'ready':True,'passed':True}))
for unit in ('getty@tty1.service','serial-getty@ttyS0.service','systemd-logind.service','systemd-user-sessions.service'):
 values={name:prop(unit,name).split() for name in ('Requires','After')}
 passed=all('stand-replay.service' in value for value in values.values())
 print(json.dumps({'id':'BOOT-ORDER-INSTANCE','unit':unit,'values':values,'passed':passed}),flush=True)
 assert passed
GUEST
"""
print('EXPECTED: fresh final-image VM has PAM/READY gate and replay in both Requires and After for four specified session entry instances.',flush=True)
try:
 lab('new','bc3-boot-order','stand')
 lab('run','bc3-boot-order','--root',input=script,text=True)
finally:
 lab('destroy','bc3-boot-order')

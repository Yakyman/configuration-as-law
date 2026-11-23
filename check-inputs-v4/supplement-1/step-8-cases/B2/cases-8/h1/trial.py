#!/usr/bin/env python3
"""Preparation compatibility trial, never a second-party history runner."""
import sys, pathlib, subprocess, json, time
sys.path.insert(0,str(pathlib.Path.cwd()))
import lab
out=pathlib.Path('raw/step-8-prep/h1'); vm=pathlib.Path('vms/prep-h1').resolve()
commands=[]
def run(label,script):
 p=subprocess.run(lab.ssh(vm,root=True)+['sh'],input=script,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
 (out/(label+'.stdout')).write_text(p.stdout);(out/(label+'.stderr')).write_text(p.stderr)
 commands.append(dict(label=label,utc=time.strftime('%FT%TZ',time.gmtime()),stdin=script,exit=p.returncode))
 (out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 return p.returncode
run('initial',"/usr/bin/dpkg-query -W '-f=${Package} ${Version} ${db:Status-Status}\\n' ed libc6\n")
for n,v,h in ((1,'1.21.1-1','b5498068d8ac54ad004bacbde2223a348fee781f9bb94328b01d8bfcbd179b48'),(2,'1.22.5-1','593a7915c2ec0e3c87f824c2b11b4f72d3d74d654183c6833a18c4320e5df6a0')):
 script="""python3 - <<'FETCH'
import urllib.request,pathlib,hashlib
u='https://deb.debian.org/debian/pool/main/e/ed/ed_VERSION_amd64.deb'
b=urllib.request.urlopen(u,timeout=60).read()
assert hashlib.sha256(b).hexdigest()=='HASH'
pathlib.Path('/tmp/ed_VERSION_amd64.deb').write_bytes(b)
FETCH
""".replace('VERSION',v).replace('HASH',h)
 if run('fetch-'+str(n),script):break
 if run('upgrade-'+str(n),'/usr/bin/dpkg --install /tmp/ed_'+v+'_amd64.deb\n'):break
 run('version-'+str(n),"/usr/bin/dpkg-query -W '-f=${Package} ${Version} ${db:Status-Status}\\n' ed\n/usr/bin/ed --version\n")
 run('reboot-'+str(n),'/usr/bin/systemctl reboot\n')
 time.sleep(12)
 deadline=time.monotonic()+120
 while time.monotonic()<deadline:
  p=subprocess.run(lab.ssh(vm,root=True)+['true'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  if p.returncode==0:break
  time.sleep(2)
 else:raise RuntimeError('observation SSH did not return')
 run('after-reboot-'+str(n),"cat /proc/sys/kernel/random/boot_id\n/usr/bin/dpkg-query -W '-f=${Package} ${Version} ${db:Status-Status}\\n' ed\n/usr/bin/systemctl show stand-replay.service -p ActiveState -p Result\n")

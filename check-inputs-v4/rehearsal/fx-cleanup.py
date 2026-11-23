#!/usr/bin/env python3
"""Certify completed rehearsal cleanup without reading guest inventory."""
import csv,datetime,pathlib,shutil,subprocess
C=pathlib.Path(__file__).resolve().parents[1]
certificate=C/'rehearsal/cleanup-final.tsv'
temporary=certificate.with_suffix('.tsv.tmp')
certificate.unlink(missing_ok=True)
temporary.unlink(missing_ok=True)
systems=('alma','void','gentoo','microos','talos','nixos','guix','fedora','mint','debian-server')
clones=list((C/'vms').glob('reh-*'))
transients=[p for system in systems for p in (C/'rehearsal'/system).glob('.unread*')]
def active_units():
 result=subprocess.run(['systemctl','--user','list-units','--all','--plain','--no-legend','--state=active,activating,deactivating','c1-*'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,text=True)
 return sum(bool(line.strip()) for line in result.stdout.splitlines())
active=active_units()
if clones or transients or active:
 raise SystemExit(f'Cleanup blocked: clone directories={len(clones)}, unread directories={len(transients)}, active preparation units={active}')
shutil.rmtree(C/'collector/build',ignore_errors=True)
(C/'collector/probe-linux-amd64').unlink(missing_ok=True)
for directory in ('collector','actions','rehearsal','install'):
 for cache in (C/directory).rglob('__pycache__'):
  shutil.rmtree(cache)
checks={'rehearsal-clone-directories':len(list((C/'vms').glob('reh-*'))),'transient-unread-directories':sum(len(list((C/'rehearsal'/system).glob('.unread*'))) for system in systems),'active-preparation-units':active_units(),'temporary-probe-build-directory':int((C/'collector/build').exists()),'uncompressed-probe-build-output':int((C/'collector/probe-linux-amd64').exists())}
if any(checks.values()):
 raise SystemExit('Cleanup final checks contain a nonzero remainder; no certificate written')
with temporary.open('w') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(('utc','check','remaining'))
 stamp=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
 for key,value in checks.items():w.writerow((stamp,key,value))
temporary.replace(certificate)
print('cleanup_checks',len(checks),'remaining',sum(checks.values()))

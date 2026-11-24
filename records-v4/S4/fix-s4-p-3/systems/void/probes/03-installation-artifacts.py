import pathlib,re,json,gzip,plistlib,subprocess
out={'route':'installation-artifacts-and-package-scripts','installer_records':0,'account_backups':0,'package_metadata':0,'package_scripts':0,'V03_source_hits':0,'V07_source_hits':0,'errors':0,'oversize':0}
for root in ['/root/void-install','/var/log/void-installer','/etc/void-installer','/var/lib/void-installer']:
 p=pathlib.Path(root)
 if p.exists():out['installer_records']+=1
for p in ['/etc/passwd-','/etc/group-','/etc/passwd.bak','/etc/group.bak']:
 if pathlib.Path(p).is_file():out['account_backups']+=1
for p in pathlib.Path('/var/db/xbps').glob('.*.plist'):
 try:
  b=p.read_bytes()
  if b.startswith(b'\x1f\x8b'):b=gzip.decompress(b)
  if len(b)>16777216:out['oversize']+=1;continue
  o=plistlib.loads(b);out['package_metadata']+=1
  for key in ['install-script','remove-script']:
   b=o.get(key,b'')
   if isinstance(b,str):b=b.encode()
   if not b:continue
   out['package_scripts']+=1
   out['V03_source_hits']+=len(re.findall(rb'useradd|usermod|groupadd|wheel|sudoers',b,re.I))
   out['V07_source_hits']+=len(re.findall(rb'live\.conf|modules-load|sudoers|xbps/keys|/mnt',b,re.I))
 except (OSError,ValueError):out['errors']+=1
# Source presence or account backups do not identify who executed a creation/change.
print(json.dumps(out,sort_keys=True))

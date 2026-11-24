import pathlib,re,json,gzip
patterns={'V03':rb'useradd|usermod|groupadd|gpasswd|chsh|sudoers|wheel|/etc/passwd|/etc/group|adduser|addgroup','V07':rb'live\.conf|modules-load|sudoers|xbps/keys|(?:mkdir|mount).{0,80}/mnt','V09':rb'ca-certificates|update-ca|/etc/ssl/certs|SSL_CA_CERT|trust anchor'}
roots=['/var/log/audit','/var/log/socklog','/var/log/messages','/var/log/auth.log','/var/log/secure','/var/log/xbps.log','/var/log/installer','/var/log/install.log']
out={'route':'retained-event-logs','files_read':0,'absent_roots':0,'errors':0,'oversize':0,'matches':{k:0 for k in patterns},'matching_files':{k:0 for k in patterns}}
for root in roots:
 p=pathlib.Path(root)
 if not p.exists():out['absent_roots']+=1;continue
 for f in ([p] if p.is_file() else p.rglob('*')):
  if not f.is_file():continue
  try:
   if f.stat().st_size>16777216:out['oversize']+=1;continue
   b=gzip.open(f,'rb').read(16777217) if f.suffix=='.gz' else f.read_bytes()
   if len(b)>16777216:out['oversize']+=1;continue
   out['files_read']+=1
   for k,pat in patterns.items():
    n=len(re.findall(pat,b,re.I));out['matches'][k]+=n;out['matching_files'][k]+=bool(n)
  except OSError:out['errors']+=1
print(json.dumps(out,sort_keys=True))

import pathlib,re,json
patterns={'V03':rb'useradd|usermod|groupadd|gpasswd|chsh|sudoers|wheel|/etc/passwd|/etc/group|adduser|addgroup','V07':rb'live\.conf|modules-load|sudoers|xbps/keys|(?:mkdir|mount).{0,80}/mnt','V09':rb'ca-certificates|update-ca|/etc/ssl/certs|SSL_CA_CERT|trust anchor'}
out={'route':'command-histories','histories_read':0,'errors':0,'oversize':0,'matches':{k:0 for k in patterns},'timestamped_matching_lines':{k:0 for k in patterns}}
homes=[pathlib.Path('/root')]+list(pathlib.Path('/home').glob('*'))
for home in homes:
 for rel in ['.bash_history','.zsh_history','.sh_history','.local/share/fish/fish_history']:
  p=home/rel
  if not p.is_file():continue
  try:
   if p.stat().st_size>4194304:out['oversize']+=1;continue
   b=p.read_bytes();out['histories_read']+=1
   for k,pat in patterns.items():
    lines=[line for line in b.splitlines() if re.search(pat,line,re.I)];out['matches'][k]+=len(lines)
    out['timestamped_matching_lines'][k]+=sum(bool(re.match(rb': [0-9]{10}:',line)) for line in lines)
  except OSError:out['errors']+=1
print(json.dumps(out,sort_keys=True))

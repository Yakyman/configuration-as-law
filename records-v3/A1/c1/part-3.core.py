import csv
from pathlib import Path
root=Path('A1/c1')
rows=list(csv.DictReader(open('A1/in/part-3.tsv'),delimiter='\t'))
header=['id','decision','sentences','what_it_does','basis','reason']
out=root/'part-3.tsv'
seen={r['id'] for r in csv.DictReader(out.open(),delimiter='\t')} if out.exists() else set()
with out.open('a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not out.stat().st_size: w.writerow(header)
 for r in rows:
  if r['id'] in seen: continue
  kind=r['kind']
  if kind=='account':
   fields=['MUST','S2.2-15','Defines an operating-system account and its user identity.','raw:A1/in/raw/nixos/accounts.txt','Accounts are explicitly required; interactive login eligibility does not limit that requirement.']
  elif kind=='account-group':
   fields=['MUST','S2.2-15','Defines 32 separate operating-system identities for package builds.','raw:A1/in/raw/nixos/nix-builder-accounts.txt','Every listed build identity is an account; S2.2-15 requires each account.']
  elif kind=='kernel-module':
   fields=['MUST','S2.2-10','Executes '+r['name']+' module code inside the kernel with kernel privileges.','raw:A1/in/raw/nixos/modules.txt','Loaded module code executes with the kernel\'s own rights; it is not confined to an application interface.']
  elif kind=='process' and r['name']!='kernel threads':
   fields=['MUST','S2.2-9,S2.2-12','Runs '+r['name'].split('/')[-1]+' as an operating-system process.','raw:A1/in/raw/nixos/processes.txt','The inventory observes a running program; programs running as their own processes must be recorded.']
  elif kind=='process':
   fields=['MUST','S2.2-1,S2.2-10','Executes kernel code in background kernel threads.','raw:A1/in/raw/nixos/processes.txt','All observed members are kernel threads executing kernel code with kernel rights; this code controls computer behavior.']
  else: continue
  if r['id'] in ['nixos-344126e1ba','nixos-791fcf298c']: fields[3]='raw:A1/in/raw/nixos/process-executables.tsv'
  assert len(fields[2].split())<=15 and len(fields[4].split())<=30
  w.writerow([r['id']]+fields); f.flush()
print('Core rows appended:',sum(r['kind'] in ['account','account-group','kernel-module','process'] for r in rows))

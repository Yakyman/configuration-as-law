import csv
from pathlib import Path
rows=list(csv.DictReader(open('A1/in/part-4.tsv'),delimiter='\t'))
p=Path('A1/c1/part-4.tsv')
header=['id','decision','sentences','what_it_does','basis','reason']
seen={r['id'] for r in csv.DictReader(p.open(),delimiter='\t')} if p.exists() else set()
with p.open('a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not p.stat().st_size:w.writerow(header)
 for r in rows:
  if r['id'] in seen:continue
  k=r['kind']; name=r['name'].split('/')[-1]
  if k=='account':
   o=['MUST','S2.2-15','Defines an operating-system account and its identity.','raw:guix/accounts.txt','Accounts are explicitly required; a non-login shell does not exempt an account.']
  elif k=='account-group':
   o=['MUST','S2.2-15','Provides ten distinct accounts for package builds.','raw:guix/guix-builder-accounts.txt','All ten members are accounts, which the sentence explicitly requires.']
  elif k=='kernel-module':
   o=['MUST','S2.2-10','Executes '+name+' code within the kernel with kernel privileges.','raw:guix/modules.txt','A loaded kernel module executes with the kernel’s rights, rather than within a confined application interface.']
  elif k=='process' and r['name']!='kernel threads':
   o=['MUST','S2.2-9,S2.2-12','Runs '+name+' as an operating-system process.','raw:guix/processes.txt','The observed executable runs as its own process; programs running on the computer must be recorded.']
  elif r['name']=='kernel threads':
   o=['MUST','S2.2-1,S2.2-2','Executes kernel background work, memory management, scheduling, and device tasks.','raw:guix/processes.txt','Removing these execution contexts prevents kernel work, including queued work and memory management; their functions determine computer behaviour.']
  else:continue
  w.writerow([r['id']]+o); f.flush()

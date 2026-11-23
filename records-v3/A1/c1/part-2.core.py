import csv
from pathlib import Path
root=Path(__file__).resolve().parents[2]
rows=list(csv.DictReader((root/'A1/in/part-2.tsv').open(), delimiter='\t'))
out=root/'A1/c1/part-2.tsv'
header=['id','decision','sentences','what_it_does','basis','reason']
old=list(csv.DictReader(out.open(),delimiter='\t')) if out.exists() else []
seen={r['id'] for r in old}
with out.open('a',encoding='utf-8',newline='') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not out.stat().st_size: w.writerow(header)
 for r in rows:
  if r['id'] in seen: continue
  k=r['kind']
  if k=='account':
   v=['MUST','S2.2-15','Defines a system account identity and its user and group identifiers.','raw:debian/accounts.txt','Accounts are explicitly required; the sentence does not exempt service accounts or accounts with disabled interactive login.']
  elif k=='kernel-module':
   v=['MUST','S2.2-10','Executes loaded native module code with kernel privileges.','raw:debian/modules.txt','The kernel executes this loaded module with its own privileges; the explicit code requirement applies.']
  elif k=='process' and r['name']=='kernel threads':
   v=['MUST','S2.2-1,S2.2-10','Executes kernel functions as background kernel tasks.','doc:https://docs.kernel.org/driver-api/basics.html','These tasks execute kernel code with kernel privileges; their executing code satisfies the explicit code requirement.']
  elif k=='process':
   v=['MUST','S2.2-9,S2.2-12','Runs an executable as an operating-system process.','raw:debian/processes.txt','The inventory observes this program running as its own process, which both sentences explicitly require recording.']
  else: continue
  assert len(v[2].split())<=15 and len(v[4].split())<=30
  w.writerow([r['id']]+v)
  f.flush()

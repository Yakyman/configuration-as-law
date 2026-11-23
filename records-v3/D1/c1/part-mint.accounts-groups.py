import csv, json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
rows=list(csv.DictReader((root/'D1/in/part-mint.tsv').open(),delimiter='\t'))
out=root/'D1/c1/part-mint.tsv'
fields=['id','decision','sentences','what_it_does','basis','reason']
existing=list(csv.DictReader(out.open(),delimiter='\t')) if out.exists() else []
seen={r['id'] for r in existing}
with out.open('a',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n')
 if f.tell()==0:w.writeheader();f.flush()
 for r in rows:
  if r['id'] in seen or r['kind'] not in ('L1:account','L1:group'):continue
  member=json.loads(r['members']);assert len(member)==1
  if r['kind']=='L1:account':
   assert len(member[0].split(':'))==7
   result=['MUST','S2.2-15','Defines a system account, its numeric identity, primary group, and login environment.','raw:'+r['evidence'],'Accounts are explicitly required; a disabled interactive login does not remove the account.']
  else:
   assert len(member[0].split(':'))==4
   result=['MUST','S2.2-1,S2.2-2','Defines a system group identity and its supplementary membership.','raw:'+r['evidence'],'Removing this definition prevents resolving the group for named ownership and identity operations across programs.']
  w.writerow(dict(zip(fields,[r['id']]+result)));f.flush()
print('Account and group rows appended:',sum(r['kind'] in ('L1:account','L1:group') for r in rows))

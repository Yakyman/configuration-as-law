import csv, pathlib
base=pathlib.Path('A1/c1')
rows=list(csv.DictReader(open('A1/in/part-1.tsv'),delimiter='\t'))
fields=['id','decision','sentences','what_it_does','basis','reason']
out=base/'part-1.tsv'
seen={r['id'] for r in csv.DictReader(out.open(),delimiter='\t')} if out.exists() else set()
f=out.open('a'); w=csv.DictWriter(f,fields,delimiter='\t',lineterminator='\n')
if not seen:w.writeheader()
def add(r,d,s,what,b,why):
 if r['id'] in seen:return
 assert len(what.split())<=15 and len(why.split())<=30
 w.writerow(dict(zip(fields,[r['id'],d,s,what,b,why])));f.flush();seen.add(r['id'])
for r in rows:
 if r['kind']=='account':add(r,'MUST','S2.2-15','Defines a system account and its identity.','evidence','Accounts are explicitly required, including service accounts with login disabled.')
 if r['kind']=='kernel-module':add(r,'MUST','S2.2-1,S2.2-10','Executes loaded kernel code providing driver or kernel subsystem functionality.','evidence','Loaded module code executes with kernel rights; it is not confined to an application interface.')
 if r['kind']=='process':
  if r['name']=='kernel threads':add(r,'MUST','S2.2-1,S2.2-9','Runs kernel tasks providing operating system functionality.','evidence','These running kernel tasks implement computer behaviour and are executing program code.')
  else:add(r,'MUST','S2.2-9,S2.2-12','Runs program code as an independent operating system process.','evidence','Observed program processes must be recorded regardless of installation method.')
f.close()

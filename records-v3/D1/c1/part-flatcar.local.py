import csv,json,re,pathlib,collections
src=list(csv.DictReader(open('D1/in/part-flatcar.tsv'),delimiter='\t'))
fields=['id','decision','sentences','what_it_does','basis','reason']
out=pathlib.Path('D1/c1/part-flatcar.tsv')
seen={r['id'] for r in csv.DictReader(out.open(),delimiter='\t')} if out.exists() else set()
f=out.open('a'); w=csv.writer(f,delimiter='\t',lineterminator='\n')
if not out.stat().st_size:w.writerow(fields)
checks=collections.defaultdict(list)
def emit(x,d,s,what,reason,rule=None,basis=None):
 assert len(what.split())<=15 and len(reason.split())<=30,(x['id'],what,reason)
 if x['id'] not in seen:
  w.writerow([x['id'],d,s,what,basis or 'raw:'+x['evidence'],reason]);f.flush();seen.add(x['id'])
 if rule:checks[rule].append(x)
for x in src:
 k=x['kind'];m=json.loads(x['members'])[0]
 if k=='L1:account':emit(x,'MUST','S2.2-15','Defines a system account.','Accounts must be recorded, including service accounts without interactive login.','accounts')
 elif k=='L1:group':emit(x,'MUST','S2.2-1,S2.2-2','Defines a system group identity and membership.','Removing the group prevents assigning that named group and supplying its supplementary membership to processes.','groups')
 elif k=='L1:module':emit(x,'MUST','S2.2-10','Runs loaded kernel module code.','Loaded modules execute with kernel rights; this is code, not cached data or settings.','modules')
 elif k=='L1:driver':emit(x,'UNKNOWN','S3-2','Exposes driver identity; downstream use is not established.','Inventory identifies a metadata link, not driver code; evidence does not establish whether consumers use this link operationally or only display its contents.','driver-links')
 elif k=='L1:polkit-actions':emit(x,'MUST','S2.2-1,S2.2-2','Declares an operation for authorization across programs.','Removing this action prevents its registered authorization lookup; the policy mediates operations in other programs.','polkit-actions')
 elif k=='L1:process':
  p=m.split('\t')
  if len(p)==2 and p[1].startswith('/'):
   emit(x,'MUST','S2.2-9,S2.2-12','Executes '+p[1].rsplit('/',1)[-1]+' as a process.','A directly identified running program must be recorded.','identified-processes')
  else:
   emit(x,'UNKNOWN','S3-2','Process identity is unresolved in concatenated inventory output.','Collector omits newlines after failed executable lookups; this row names an unresolved PID, not the later executable.','unresolved-processes')
f.close()
# These samples were inspected in raw output and the inventory before applying the rules.
with open('D1/c1/part-flatcar.local-checks.json','w') as f:
 json.dump({k:[{'id':x['id'],'name':x['name'],'evidence':x['evidence']} for x in [v[round(i*(len(v)-1)/9)] for i in range(10)]] for k,v in checks.items()},f,indent=2)
print(collections.Counter(r['decision'] for r in csv.DictReader(out.open(),delimiter='\t')))

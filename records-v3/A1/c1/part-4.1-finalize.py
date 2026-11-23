import csv,json,re,collections
rs=[r for r in csv.DictReader(open('A1/in/part-4.tsv'),delimiter='\t') if r['kind']=='system-closure-store-object'][:431];p='A1/c1/part-4.1.tsv';old={r['id'] for r in csv.DictReader(open(p),delimiter='\t')};f=open(p,'a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
def add(i,d,s,what,b,why):
 if rs[i]['id'] not in old:w.writerow([rs[i]['id'],d,s,what,b,why]);f.flush();old.add(rs[i]['id'])
m=json.load(open('A1/c1/part-4.1-metadata.json'))
for i,k in [(145,'llvm'),(220,'ntfs-3g'),(233,'libcloudproviders-minimal'),(235,'vte'),(245,'bash'),(286,'guile'),(349,'libcamera-minimal')]:
 a=next((x for x in m if k in x[:2] and not x[2].startswith('INHERIT:')),None)
 if a:add(i,'MUST','S2.2-1,S2.2-2,S2.2-9,S2.2-10','Provides '+k+' executable runtime functionality.','doc:'+a[3],'The variant retains the documented executable runtime role; removal removes that installed code and its functionality.')
for i,what,u in [(145,'Provides compiler infrastructure for graphics execution.','https://llvm.org/'),(349,'Provides camera capture and processing routines.','https://libcamera.org/')]:add(i,'MUST','S2.2-1,S2.2-2,S2.2-10',what,'doc:'+u,'The documented library supplies executable functionality; removing it removes that code and capability.')
add(29,'MUST','S2.2-1,S2.2-2,S2.2-9','Exposes the installed package-manager program through its package profile.','raw:guix/system-profile.txt','The package listing identifies this exact profile as the package-manager installation; removing it removes the exposed program.')
# Boot observation explicitly adds these module paths before loading boot code.
boot=open('A1/in/raw/guix/system-boot.scm').read()
for i in [309,322]:
 if rs[i]['name'] in boot:add(i,'MUST','S2.2-2,S2.2-10','Supplies Scheme modules to the observed boot interpreter.','raw:guix/system-boot.scm','The boot script places this exact directory on its source or compiled module path and imports executable system modules.')
# Record individual unresolved objects: inventory names do not supply their missing contents or consumer relationships.
for i,r in enumerate(rs):
 if r['id'] in old:continue
 n=r['name'][44:]
 if re.search(r'-\d',n) and not n.startswith('guix-'):
  what='Exact installed output contents and executable role remain unestablished.'
  reason='Available inventory gives only the store path; retrieved package documentation did not establish this particular output’s role or contents.'
 elif n=='guile-launcher.c':
  what='Holds launcher source; its use beyond stored source is unestablished.'
  reason='The source filename does not establish compilation, execution, or use; no contents or consuming references were captured.'
 else:
  what='Specific generated object contents and effective consumer behavior remain unestablished.'
  reason='Only a store name or link target is available; missing generated contents and consumer relationships prevent establishing its function without guessing.'
 add(i,'UNKNOWN','S3-1,S3-2',what,'evidence',reason)
f.close()
rows=list(csv.DictReader(open(p),delimiter='\t'))
assert len(rows)==len(rs)==len({r['id'] for r in rows})
assert {r['id'] for r in rows}=={r['id'] for r in rs}
for r in rows:
 assert r['decision'] in ['MUST','NOT','HOLE','UNKNOWN','MIXED']
 assert len(r['what_it_does'].split())<=15,(r['id'],'what')
 assert len(r['reason'].split())<=30,(r['id'],'reason')
print(collections.Counter(r['decision'] for r in rows))

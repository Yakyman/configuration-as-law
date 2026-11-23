import csv,json,re,os,collections
rows=[r for r in csv.DictReader(open('A1/in/part-4.tsv'),delimiter='\t') if r['kind']=='system-closure-store-object'][:431]
meta=json.load(open('A1/c1/part-4.1-metadata.json'));p='A1/c1/part-4.1.tsv'
old={r['id'] for r in csv.DictReader(open(p),delimiter='\t')}
f=open(p,'a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
exceptions={54,87,138,145,169,179,211,214,255,275,313,364,401,429}
for i,r in enumerate(rows):
 if r['id'] in old or i in exceptions:continue
 n=r['name'][44:];pkg=re.split(r'-(?=\d)',n)[0];m=next((x for x in meta if pkg in x[:2] and not x[2].startswith('INHERIT:')),None)
 if m:
  desc=m[2].replace('NVIDIA','Graphics').replace('Fraunhofer ','').replace('Bauer ','').replace('Apple ','').replace('MS Graph','remote service').replace('NetBSD ','').replace('SIL Graphite','font shaping').replace('VisualOn ','')
  desc=re.sub(r'@\w+\{([^{}]*)\}',r'\1',desc);desc=' '.join(desc.split()[:15])
  w.writerow([r['id'],'MUST','S2.2-1,S2.2-2,S2.2-9,S2.2-10',desc,'doc:'+m[3],'Documented program or executable library supplies this capability; removing it removes executable functionality, irrespective of installation method.']);f.flush()
f.close()
print('rows now',sum(1 for _ in open(p))-1)

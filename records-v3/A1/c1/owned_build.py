import csv,collections,pathlib,json
base=pathlib.Path('A1/c1'); rows=[r for r in csv.DictReader(open('A1/in/part-1.tsv'),delimiter='\t') if r['kind']=='package-owned-paths'];aliases=list(csv.reader(open('A1/in/raw/coreos/path-aliases.tsv'),delimiter='\t'))
def norm(p):
 for a,b in sorted(aliases,key=lambda v:-len(v[0])):
  if p==a or p.startswith(a+'/'): return b+p[len(a):]
 return p
pkg={norm(p.strip()) for p in open('A1/in/raw/coreos/package-files.txt')}; fs=[x for x in csv.reader(open('A1/in/raw/coreos/files.tsv'),delimiter='\t') if x[1] in pkg]; groups={}
for row in rows:
 name=row['name']; nested=[o['name'] for o in rows if o['name']!=name and o['name'].startswith(name+'/')]
 m=[x for x in fs if (x[1]==name or x[1].startswith(name+'/')) and not any(x[1]==n or x[1].startswith(n+'/') for n in nested)]
 assert len(m)==int(row['members']),(name,len(m),row['members']);groups[row['id']]=m
out=base/'part-1.owned.tsv'; header=['id','decision','sentences','what_it_does','basis','reason']
seen={r['id'] for r in csv.DictReader(out.open(),delimiter='\t')} if out.exists() else set()
def append(row,decision,sentences,what,basis,reason):
 assert len(what.split())<=15,(row['id'],what)
 assert len(reason.split())<=30,(row['id'],reason)
 if row['id'] in seen:return
 exists=out.exists()
 with out.open('a') as f:
  w=csv.writer(f,delimiter='\t',lineterminator='\n');
  if not exists:w.writerow(header)
  w.writerow([row['id'],decision,sentences,what,basis,reason]);f.flush()
 seen.add(row['id'])
if __name__=='__main__':
 for row in rows:
  m=groups[row['id']]
  if all(x[0]=='d' for x in m):append(row,'UNKNOWN','S2.2-1,S2.2-2,S3-2','Provides directory entries; operational consumers are not established','raw:coreos/files.tsv','Directory ownership and existence do not establish operational consumers or reconstruction behavior; general hierarchy documentation does not establish this instance’s function.')
 print(collections.Counter(r['decision'] for r in csv.DictReader(out.open(),delimiter='\t')))

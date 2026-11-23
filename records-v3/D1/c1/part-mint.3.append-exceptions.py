import csv,json
P='D1/c1/part-mint.3.tsv';rows=[x for x in csv.DictReader(open('D1/in/part-mint.tsv'),delimiter='\t') if x['kind']=='L1:package:dpkg-query'][1270:1905]
m={}
for p in ['D1/c1/part-mint.3.full-metadata.json','D1/c1/part-mint.public-mint-metadata.json','D1/c1/part-mint.public-mint-extra.json','D1/c1/part-mint.3.kernel-metadata.json','D1/c1/part-mint.3.extra-metadata.json']:m.update(json.load(open(p)))
fl=json.load(open('D1/c1/part-mint.3.filelists.json'))
existing={x['id'] for x in csv.DictReader(open(P),delimiter='\t')}
f=open(P,'a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
for i,dec,what,reason in csv.reader(open('D1/c1/part-mint.3.exceptions.txt'),delimiter='|'):
 i=int(i);r=rows[i];n=r['name'].split(':')[1]
 if r['id'] in existing:continue
 d=m[n];u=fl.get(n,{}).get('url',d['url'])
 ids={'MUST':'S2.2-1,S2.2-2','NOT':'S2.2-2,S2.2-4','HOLE':'S2.2-1,S2.2-2,S2.2-4,S2.2-7','UNKNOWN':'S3-2'}[dec]
 if i in [18,252,253,280,290,503,508,542,606,610]:ids='S2.2-1,S2.2-2'
 if i in [125,127,130,179,180,273,438,597,604]:ids='S2.2-1,S2.2-2'
 if i in [126,128,131,137,181,210,211,262,278,319,465,492,536,546,548,587,588,590,601,621]:ids='S2.2-1,S2.2-2,S2.2-4'
 if i in [171,178,182,184,200,209,231,244,277,286,287,586,631]:ids='S2.2-1,S2.2-2,S2.2-7,S2.2-13'
 if i in [129,132,133,138,164,172,174,196,217,218,219,268,303,309,333,433,434,435,436,437,446,447,448,453,484,487,522,543,559,571,622]:ids='S2.2-1,S2.2-2,S2.2-9,S2.2-10'
 if i==292:ids='S2.2-1,S2.2-2,S2.2-15'
 if i==460:ids='S2.2-1,S2.2-2,S2.2-16'
 if i==514:ids='S2.2-11'
 if i==628:ids='S2.2-10,S2.2-11,S2.2-13'
 assert len(what.split())<=15,(i,what)
 assert len(reason.split())<=30,(i,reason)
 w.writerow([r['id'],dec,ids,what,'doc:'+u,reason]);f.flush()
f.close()

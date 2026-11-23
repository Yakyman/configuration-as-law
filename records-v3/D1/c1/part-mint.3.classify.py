import csv,json,re,os
P='D1/c1/part-mint.3.tsv'
rows=[x for x in csv.DictReader(open('D1/in/part-mint.tsv'),delimiter='\t') if x['kind']=='L1:package:dpkg-query'][1270:1905]
m={}
for p in ['D1/c1/part-mint.3.full-metadata.json','D1/c1/part-mint.public-mint-metadata.json','D1/c1/part-mint.public-mint-extra.json']:m.update(json.load(open(p)))
exclude=set([1,18,21,30,119,125,126,127,128,129,130,131,132,133,134,135,137,138,146,152,154,157,159,162,163,164,171]+list(range(172,187))+[200,209,210,211,213,214,217,218,219,226,231,243,244,252,253,256,262,268,273,277,278,280,286,287,290,292,294,303,309,316,318,319,321,333,433,434,435,436,437,438,439,441,446,447,448,453,460,465,466,472,484,487,492,493,495,503,507,508,513,514,516,517,518,520,521,522,535,536,542,543,546,548,553,559,570,571,572,575,586,587,588,589,590,595,597,598,600,601,602,604,606,610,621,622,626,628,631])
existing={r['id'] for r in csv.DictReader(open(P),delimiter='\t')} if os.path.exists(P) else set()
f=open(P,'a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
if not existing:w.writerow(['id','decision','sentences','what_it_does','basis','reason'])
for i,r in enumerate(rows):
 if i in exclude or r['id'] in existing:continue
 n=r['name'].split(':')[1];d=m.get(n)
 if not d:print('missing',i,n);continue
 desc=d['Description'].split('\n')[0]
 if n=='perl':desc='Perl language interpreter and core utilities'
 if n=='libwrap0':desc='TCP access control wrapper library'
 what=' '.join(desc.split()[:15])
 w.writerow([r['id'],'MUST','S2.2-1,S2.2-2,S2.2-9,S2.2-10',what,'doc:'+d['url'],'Executable program or runtime library supplies this capability; removal removes runnable code required for that operation.'])
 f.flush()
f.close()
print('rows',sum(1 for _ in open(P))-1)

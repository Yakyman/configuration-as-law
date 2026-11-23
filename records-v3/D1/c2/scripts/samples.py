import csv,sys,random
csv.field_size_limit(10**9)
inp={r['id']:r for r in csv.DictReader(open(sys.argv[1]),delimiter='\t')}
groups={}
for line in open(sys.argv[2]):
    a=line.rstrip('\n').split('\t')
    if a[0]=='id': continue
    r=inp[a[0]]
    if r['kind']=='L2:stored-outside-packages': continue
    key=(r['kind'].split(':')[0] if r['kind'].startswith('L2') else r['kind'], a[1], a[5])
    groups.setdefault(key,[]).append((a[0],r['name'],a[3]))
random.seed(1122)
for k,v in sorted(groups.items(), key=lambda x:-len(x[1])):
    if len(v)<2: continue
    s=v if len(v)<=10 else random.sample(v,10)
    print('##',len(v),k[0],k[1],'|',k[2][:90])
    for i in s: print('  ',i[0],i[1][:70],'|',i[2][:60])

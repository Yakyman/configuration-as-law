import csv,random,json
random.seed(1122)
inp={r[0]:r for r in csv.reader(open('in/part-1.tsv'),delimiter='\t')}
out={r[0]:r for r in csv.reader(open('c2/part-1.tsv'),delimiter='\t')}
pc=json.load(open('c2/work/pkgclass.json'))
for k in ['account','kernel-module','process','system-unit','user-unit','package']:
    ids=[i for i,r in inp.items() if len(r)>3 and r[3]==k and (k!='package' or pc[r[4]]['nex']>0)]
    s=random.sample(ids,min(10,len(ids)))
    print('==',k,' '.join(s))
    for i in s:
        r=inp[i]; extra=pc[r[4]]['ex'][:2] if k=='package' else r[6][:110]
        print('  ',i,r[4][:40],'|',out[i][1],'|',extra)

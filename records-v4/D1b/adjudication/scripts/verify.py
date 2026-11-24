import csv,sys,collections
csv.field_size_limit(sys.maxsize)
a=[r['id'] for r in csv.DictReader(open('D1b/compare/to-adjudicate.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE)]
f=open('D1b/adjudication/rows.tsv'); hdr=f.readline().rstrip('\n')
assert hdr=='id\tverdict\tsentence_id\tquote\terred\thole\tnote', hdr
b=[l.rstrip('\n').split('\t') for l in f]
assert all(len(x)==7 for x in b)
ids=[x[0] for x in b]
print('input',len(a),'rows',len(ids),'unique',len(set(ids)),'same set',set(a)==set(ids),'same order',a==ids)
print(collections.Counter(x[1] for x in b)); print(collections.Counter(x[4] for x in b)); print(collections.Counter(x[5] for x in b if x[1]=='GAP'))

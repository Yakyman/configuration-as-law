import csv,sys,collections,json
csv.field_size_limit(sys.maxsize)
inp=[r['id'] for r in csv.DictReader(open('D1b/compare/to-adjudicate.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE)]
labels=json.load(open('D1b/adjudication/raw/hole-map.json'))  # gap_label -> card number
res={}
for p in 'ABC',:
    pass
for p in ['A','B','C','SELF']:
    for r in csv.DictReader(open(f'D1b/adjudication/raw/out-{p}.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE):
        assert r['id'] not in res, r['id']
        res[r['id']]=r
missing=[i for i in inp if i not in res]; extra=set(res)-set(inp)
assert not missing and not extra, (len(missing),len(extra))
with open('D1b/adjudication/rows.tsv','w') as f:
    f.write('id\tverdict\tsentence_id\tquote\terred\thole\tnote\n')
    for i in inp:
        r=res[i]
        hole='-'
        if r['verdict']=='GAP':
            hole=str(labels[r['gap_label']])
        note=' '.join(r['note'].split())
        f.write('\t'.join([i,r['verdict'],r['sentence_id'],r['quote'],r['erred'],hole,note])+'\n')
c=collections.Counter(res[i]['verdict'] for i in inp)
print(c)
long=[i for i in inp if len(res[i]['note'].split())>30]
print('notes over 30 words:',len(long))

import csv,sys
csv.field_size_limit(sys.maxsize)
inp={r['id']:r for r in csv.DictReader(open('D1b/compare/to-adjudicate.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE)}
for r in csv.DictReader(open('D1b/adjudication/rows.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE):
    if r['verdict']=='GAP':
        i=inp[r['id']]; print(r['hole'],r['id'],i['kind'],i['name'][:90],'|',i['c1_decision'],i['c2_decision'],'|',r['note'][:150])

import csv,sys,json,collections
csv.field_size_limit(sys.maxsize)
r=list(csv.DictReader(open('D1/compare/joined.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE));a={x['id']:x for x in csv.DictReader(open('D1/adjudication/rows.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE)}
for x in r:
 if a.get(x['id'],{}).get('hole')=='2' and not x['name'].startswith('user:'):
  print(x['id'],x['name'],a[x['id']]['note'])

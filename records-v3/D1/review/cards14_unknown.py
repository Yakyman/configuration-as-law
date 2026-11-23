import csv,sys,json
csv.field_size_limit(sys.maxsize)
r=list(csv.DictReader(open('D1/compare/joined.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE));ex=list(csv.DictReader(open('D1/review/cards-1-4-extent.tsv'),delimiter='\t'))
ids={x['id'] for x in ex if x['membership']=='UNCERTAIN'}
for x in r:
 if x['id'] in ids and not x['name'].startswith('user:'):print(x['machine'],x['name'], '\nc1',x['c1_what'],x['c1_reason'],'\nc2',x['c2_what'],x['c2_reason'])

import csv,sys,collections,json,re
csv.field_size_limit(sys.maxsize)
r=list(csv.DictReader(open('D1/compare/joined.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE)); a={x['id']:x for x in csv.DictReader(open('D1/adjudication/rows.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE)}
for h in ['1','2','3','4']:
 print('\n###',h)
 groups=collections.defaultdict(list)
 for x in r:
  if a.get(x['id'],{}).get('hole')==h:groups[(x['machine'],x['kind'],x['name'].split(':',1)[-1])].append(x)
 for (m,k,n),rs in groups.items():print(m,k,n,len(rs),a[rs[0]['id']]['note'])
print('\nEXTRA NAME CANDIDATES')
for x in r:
 if x['id'] in a and a[x['id']].get('hole') in ['1','2']:continue
 if re.search(r'font|theme|lang|l10n|i18n|data|dict|terminfo|ncurses-base|poppler|netconfig|gpg-pubkey|color|colour|wallpaper|artwork|sound|branding|locale|zone|database|hwdata',x['name'],re.I): print(x['id'],x['kind'],x['name'],x['c1_decision'],x['c2_decision'],a.get(x['id'],{}).get('verdict'),a.get(x['id'],{}).get('note',''))

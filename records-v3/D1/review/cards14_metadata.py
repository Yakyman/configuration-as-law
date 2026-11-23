import csv,json,sys,collections
csv.field_size_limit(sys.maxsize)
a={x['id']:x for x in csv.DictReader(open('D1/adjudication/rows.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE)}
r=list(csv.DictReader(open('D1/compare/joined.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE));d=json.load(open('D1/adjudication/work/A/deps-A.json'))
for n in ['abattis-cantarell-vf-fonts','gnulib-l10n','adwaita-icon-theme-legacy','ncurses-base','poppler-data','glibc-all-langpacks','google-noto-sans-vf-fonts']:
 print(n,d.get(n,{}).get('req'),d.get(n,{}).get('rec'))
groups=collections.Counter();zero=[]
for x in r:
 if x['machine']=='fedora' and a.get(x['id'],{}).get('hole') in ['1','2']:
  n=x['name'].split(':',1)[1];v=d.get(n,{});req=[t for t in v.get('req',[]) if not t.startswith('rpmlib(')]
  groups[bool(req)]+=1
  if not req:zero.append(n)
print(groups,'NO_REQ',sorted(set(zero)))

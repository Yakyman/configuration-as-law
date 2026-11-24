"""Reproduce full-table kind/name search and reviewed scope; no input changes."""
from pathlib import Path
import csv,re,collections
ROOT=Path(__file__).resolve().parents[2]
def read(p):
 return list(csv.DictReader(open(ROOT/p),delimiter='\t',quoting=csv.QUOTE_NONE))
J=read('A3/compare/joined.tsv'); R={x['id']:x for x in read('A3/adjudication/rows.tsv')}
rows=[]
for x in J:
 n=x['name'];k=x['kind'];rid=x['id'];base=[rid,x['machine'],k,n,R.get(rid,{}).get('verdict','AGREED:'+x['c1_decision'])]
 if k.startswith('2:') and '/.git' in n:
  inside=bool(re.search(r'/\.git(?:/(?:objects|refs)(?:/|$)|$)',n))
  reason='Non-executable repository objects/references or a .git group containing them; Q4 overlap.' if inside else ('Executable hooks reach Q2; operational logs/cache/info are generated working records, not fetched repository history.' if re.search(r'/\.git(?:/|$)',n) else 'Name search matched a different path such as .github or .gitignore; not a repository-history object.')
  status='CONFIRMED' if inside else 'EXCLUDED'
  if '/.git/objects/info' in n:
   status='FACT_UNKNOWN';reason='Commit-graph metadata: fetched versus locally generated provenance is not established; not a confirmed fetched-history example.'
  rows.append(['C2',*base,status,reason])
 if k.startswith('1:firewall') or (k.startswith('2:') and any(p in n for p in ['/etc/firewalld','/system.control','/.config/pulse','/etc/rancher','/var/lib/rancher'])):
  status='EXCLUDED';reason='Directory/container/code row does not itself establish a generated computer-wide value; no additional confirmed member inferred.'
  if k.startswith('1:firewall'):reason='Runtime firewall object: S8.2-5 follows the creating program/setting; not a separate persistent value.'
  elif n in ['/etc/firewalld/policies','/etc/firewalld/zones']:
   status='REFUTED';reason='Persistent Docker-generated docker-forwarding.xml or docker.xml; Q3 chosen-by-person is negative, Q4 yields RECORD under fixed question order.'
  elif '/.config/pulse' in n:reason='Authentication cookie: S8.2-14 expressly decides SETTING; no chosen-by-person prerequisite added to this clause.'
  elif '/data/' in n:reason='Executable extracted tools: Q2 PROGRAM; own line expressly permitted by S8.2-16.'
  elif R.get(rid,{}).get('hole')=='6':
   status='FACT_UNKNOWN';reason='Actual origin, chosen/default/generated status or effective member contents not established; cannot promote a whole group from name alone.'
   if n.endswith('/static/charts'):status='EXCLUDED';reason='Members are three .tgz archives, not the alleged active generated value files; package/deployment facts needed for any further decision.'
   if n=='/etc/systemd/system.control':status='EXCLUDED';reason='Immediate members are directories; concrete resource values are separate child groups, whose provenance is unknown.'
  rows.append(['C6',*base,status,reason])
p=ROOT/'A3/review/gap-scope.tsv'
with p.open('w') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['card','id','machine','kind','name','input_verdict','review_status','reason']);w.writerows(rows)
print(collections.Counter((r[0],r[6],r[2]) for r in rows))

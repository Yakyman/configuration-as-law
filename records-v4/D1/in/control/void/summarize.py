import csv,json,collections,pathlib
csv.field_size_limit(1024*1024*128)
base=pathlib.Path('D1/in');raw=base/'raw/void';control=base/'control/void'
def read(path):
 with path.open(newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
objects=read(raw/'objects.tsv') if (raw/'objects.tsv').exists() else []
with (base/'part-void.tsv').open('w',newline='') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['id','part','machine','kind','name','members','evidence'])
 for r in objects:w.writerow(['void-'+r['id'],'void',r['machine'],'L'+r['level']+':'+r['kind'],r['name'],r['members'],r['evidence']])
packages=[r for r in objects if r['kind']=='package'];reasons=collections.Counter()
for r in packages:
 m=json.loads(r['members'])
 if isinstance(m,str):m=json.loads(m)
 reasons[m.get('reason','unknown')]+=1
files=read(raw/'package-files.tsv') if (raw/'package-files.tsv').exists() else []
integrity=collections.Counter(r['integrity'] for r in files)
actions=[]
if (control/'actions-status.tsv/actions-status.tsv').exists():
 for row in csv.reader((control/'actions-status.tsv/actions-status.tsv').open(),delimiter='\t'):
  actions.append(dict(zip(['action','exit_status','elapsed_seconds'],row)))
summary={'machine':'void','release':'20250202 (rolling-release installation image)','inventory_obtained':bool(objects),'objects':len(objects),'kinds':dict(sorted(collections.Counter('L'+r['level']+':'+r['kind'] for r in objects).items())),'levels':dict(collections.Counter(r['level'] for r in objects)),'second_level_obtained':any(r['level']=='2' for r in objects),'package_reasons':{'total':len(packages),'known':reasons['explicit']+reasons['dependency'],'counts':dict(reasons)},'packaged_file_integrity':{'total':len(files),'known':sum(integrity[k] for k in ['unchanged','changed','missing']),'counts':dict(integrity)},'actions':actions,'deviations':[]}
summary['lifecycle']=[dict(zip(['utc','operation','exit_status'],r)) for r in csv.reader((control/'lifecycle.tsv').open(),delimiter='\t')]
(base/'void-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))

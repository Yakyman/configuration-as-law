import csv,json,collections,pathlib,datetime
csv.field_size_limit(2**31-1)
base=pathlib.Path('D1/in'); raw=base/'raw/alma'; control=base/'control/alma'
def read(path):
    with path.open(newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
objects=read(raw/'objects.tsv') if (raw/'objects.tsv').exists() else []
with (base/'part-alma.tsv').open('w',newline='') as f:
    w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['id','part','machine','kind','name','members','evidence'])
    for r in objects:w.writerow(['alma-'+r['id'],'alma',r['machine'],'L'+r['level']+':'+r['kind'],r['name'],r['members'],r['evidence']])
packages=[json.loads(r['members']) for r in objects if r['kind']=='package']
files=read(raw/'package-files.tsv') if (raw/'package-files.tsv').exists() else []
actions=[]
if (control/'actions-status.tsv').exists():
    for line in (control/'actions-status.tsv').read_text().splitlines():
        name,rc,elapsed=line.split('\t');actions.append({'action':name,'exit_status':int(rc),'elapsed_seconds':int(elapsed)})
summary={'machine':'alma','release':'10.3','objects':len(objects),'by_kind':dict(sorted(collections.Counter('L'+r['level']+':'+r['kind'] for r in objects).items())),'levels':dict(collections.Counter(r['level'] for r in objects)),'second_level_obtained':any(r['level']=='2' for r in objects),'package_reason':{'known':sum(p.get('reason') in ('explicit','dependency') for p in packages),'total':len(packages)},'packaged_file_integrity':{'known':sum(f['integrity'] in ('unchanged','changed','missing') for f in files),'total':len(files),'counts':dict(collections.Counter(f['integrity'] for f in files))},'actions':actions,'lifecycle_status':(control/'status.tsv').read_text() if (control/'status.tsv').exists() else '', 'deviations':[]}
(base/'alma-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))

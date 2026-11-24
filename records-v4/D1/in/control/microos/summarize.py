import pathlib,csv,json,collections
csv.field_size_limit(536870912)
root=pathlib.Path(__file__).resolve().parents[2];r=root/'raw/microos'
read=lambda p:list(csv.DictReader(p.open(),delimiter='\t'))
rows=read(r/'objects.tsv')
with (root/'part-microos.tsv').open('w') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['id','part','machine','kind','name','members','evidence'])
 for a in rows:w.writerow(['microos-'+a['id'],'microos',a['machine'],'L'+a['level']+':'+a['kind'],a['name'],a['members'],a['evidence']])
pkgs=[json.loads(a['members']) for a in rows if a['kind']=='package'];known=sum(x.get('reason') in ('explicit','dependency') for x in pkgs)
files=read(r/'package-files.tsv');fk=sum(x['integrity'] in ('changed','unchanged','missing') for x in files)
meta=json.loads((r/'metadata.json').read_text());cov=read(r/'coverage.tsv')
s={'machine':'microos','release':'Snapshot20261121 plain x86_64 KVM/XEN image','inventory':True,'total':len(rows),'counts':dict(sorted(collections.Counter('L'+a['level']+':'+a['kind'] for a in rows).items())),'levels':dict(collections.Counter(a['level'] for a in rows)),'packages_total':len(pkgs),'package_reasons_known':known,'package_reason_share':f'{known}/{len(pkgs)} ({100*known/len(pkgs):.2f}%)','packaged_files_total':len(files),'packaged_file_integrity_known':fk,'packaged_file_integrity_share':f'{fk}/{len(files)} ({100*fk/len(files):.2f}%)','ordinary_actions':'Not prescribed','lifecycle_statuses':{'new':0,'collector':0,'destroy':0},'failed_queries':sum(int(a['exit_status'])!=0 for a in cov),'metadata':meta}
(root/'microos-summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s,indent=2))

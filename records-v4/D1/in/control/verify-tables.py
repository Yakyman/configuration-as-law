"""Verify only saved table preservation and evidence links; make no inventory queries."""
import csv,json,pathlib,collections,datetime
root=pathlib.Path(__file__).resolve().parents[1]
csv.field_size_limit(536870912)
header=['id','part','machine','kind','name','members','evidence']
allids=set(); result={}
for machine in ('alma','void','gentoo','microos','talos'):
 part=root/f'part-{machine}.tsv'; raw=root/'raw'/machine
 if not part.exists():continue
 with part.open(newline='') as f:
  reader=csv.DictReader(f,delimiter='\t');assert reader.fieldnames==header; rows=list(reader)
 if not (raw/'objects.tsv').exists():assert not rows;result[machine]={'objects':0,'inventory':False};continue
 with (raw/'objects.tsv').open(newline='') as f: original=list(csv.DictReader(f,delimiter='\t'))
 assert len(rows)==len(original)
 for a,b in zip(rows,original):
  assert a=={'id':machine+'-'+b['id'],'part':machine,'machine':b['machine'],'kind':'L'+b['level']+':'+b['kind'],'name':b['name'],'members':b['members'],'evidence':b['evidence']}
  assert a['id'] not in allids;allids.add(a['id'])
 groups=members=0
 for b in original:
  try: details=json.loads(b['members'])
  except (ValueError,TypeError):continue
  if isinstance(details,dict) and 'file' in details and details['file'].startswith('members/'):
   with (raw/details['file']).open(newline='') as f: contents=list(csv.DictReader(f,delimiter='\t'))
   assert len(contents)==details['count'];groups+=1;members+=len(contents)
 with (raw/'coverage.tsv').open(newline='') as f:
  coverage=list(csv.DictReader(f,delimiter='\t'))
 for r in coverage:assert (raw/r['stdout']).is_file() and (raw/r['stderr']).is_file()
 result[machine]={'inventory':True,'objects':len(rows),'levels':dict(collections.Counter(x['level'] for x in original)),'member_files':groups,'members':members,'coverage_rows':len(coverage),'failed_queries':sum(int(x['exit_status'])!=0 for x in coverage),'table_preservation':'exact one-to-one in collector order'}
(root/'control/table-verification.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'machines':result},indent=2)+'\n')
print(json.dumps(result,indent=2))

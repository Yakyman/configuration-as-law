import csv,pathlib,collections,re
base=pathlib.Path('D1/c1');output=base/'part-flatcar.tsv'
fields=['id','decision','sentences','what_it_does','basis','reason']
existing=list(csv.DictReader(output.open(),delimiter='\t')) if output.exists() else []
seen={r['id']:r for r in existing}
with output.open('a') as f:
 w=csv.DictWriter(f,fields,delimiter='\t',lineterminator='\n')
 if not existing:w.writeheader()
 for label in ['units','code','stored']:
  p=base/f'part-flatcar.{label}.tsv'
  if not p.exists():continue
  reader=csv.DictReader(p.open(),delimiter='\t');assert reader.fieldnames==fields
  for row in reader:
   if row['id'] in seen:
    assert seen[row['id']]==row,('conflicting completed row',row['id'])
    continue
   assert set(row)==set(fields) and None not in row.values()
   assert row['decision'] in ['MUST','NOT','HOLE','UNKNOWN','MIXED']
   assert len(row['what_it_does'].split())<=15,(row['id'],'what')
   assert len(row['reason'].split())<=30,(row['id'],'reason')
   w.writerow(row);f.flush();seen[row['id']]=row
print(len(seen),dict(collections.Counter(r['decision'] for r in seen.values())))

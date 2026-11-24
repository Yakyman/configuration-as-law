"""Verify changed accounting, frozen-input integrity and unchanged sample draws."""
import csv,hashlib,json
from collections import Counter
from pathlib import Path
O=Path('D1/fix-d1-h-2/raw')
csv.field_size_limit(10000000)
def read(p):
    with Path(p).open() as f:return list(csv.DictReader(f,delimiter='\t'))
checks={}
for label,path in [('previous_23','D1/fix-d1-h-1/raw/frozen-input-hashes.json'),('scanned','D1/fix-d1-h-2/raw/scan-input-hashes.json')]:
    hashes=json.loads(Path(path).read_text()); changed=[p for p,h in hashes.items() if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h]
    checks[label]={'files':len(hashes),'changed':changed};assert not changed
ledger=read(O/'gap-row-dispositions.tsv'); checks['ledger_rows']=len(ledger);checks['ledger_statuses']=dict(Counter(r['fix_status'] for r in ledger))
assert len(ledger)==len({r['id'] for r in ledger})==1364
ids=[]
for c in ('card2-extent.tsv','card4-boot-extent.tsv','card5-extent.tsv'):
    rows=read(O/c);si={r['id'] for r in rows};assert len(si)==len(rows);ids.append(si)
checks['confirmed_union']=len(set.union(*ids));assert checks['confirmed_union']==111
checks['changed_sample_ids']={}
for sample in ('agreed','resolved'):
    old=read('D1/review/'+sample+'-sample.tsv');new=read(O/(sample+'-sample.tsv'))
    assert [r['id'] for r in old]==[r['id'] for r in new]
    changes=[b['id'] for a,b in zip(old,new) if a!=b];checks['changed_sample_ids'][sample]=changes
    assert len(changes)==1
checks['card2_original_statuses']=dict(Counter(r['status'] for r in read(O/'card2-original-rows.tsv')))
newunknown=[r for r in read('D1/fix-d1-h-2/generated/dispositions.tsv') if r['suggested_extent_status']=='FACT_UNKNOWN']
oldunknown={r['id'] for p in ('D1/review/unknown-rows.tsv','D1/review/additional-unknown-rows.tsv') for r in read(p)}
checks['previous_fact_limited']=len(oldunknown);checks['additional_generated_extent_fact_limits']=len(newunknown)
checks['overlap_with_previous_fact_limits']=sorted(oldunknown & {r['id'] for r in newunknown})
assert len(oldunknown)==2007 and len(newunknown)==5 and not checks['overlap_with_previous_fact_limits']
checks['status']='Mechanical checks passed; independent acceptance not claimed.'
with (O/'verification.json').open('x') as f:json.dump(checks,f,indent=2);f.write('\n')
print(json.dumps(checks,indent=2))

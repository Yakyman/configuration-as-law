import argparse,collections,csv,json,re
from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--finish',action='store_true');args=p.parse_args()
fields=['id','decision','sentences','what_it_does','basis','reason']
allowed={'MUST','NOT','HOLE','UNKNOWN','MIXED'}
inputs=list(csv.DictReader((root/'D1/in/part-mint.tsv').open(),delimiter='\t'))
input_ids=[r['id'] for r in inputs]
assert len(input_ids)==len(set(input_ids))
sentences=set(re.findall(r'\*\*(S(?:2\.2|3)-\d+)\*\*',(root/'SENTENCES.md').read_text()))
sentences &= {'S2.2-'+str(i) for i in range(1,17)}|{'S3-1','S3-2'}
out=root/'D1/c1/part-mint.tsv'
correction_path=root/'D1/c1/part-mint.corrections.json'
corrections=json.loads(correction_path.read_text()) if correction_path.exists() else {}
def corrected(r):
 return {**r,**corrections.get(r['id'],{})}
def read(path):
 with path.open(newline='',encoding='utf-8') as f:
  rd=csv.DictReader(f,delimiter='\t');assert rd.fieldnames==fields,(path,rd.fieldnames)
  return list(rd)
def check(r):
 assert set(r)==set(fields) and all(isinstance(v,str) and v for v in r.values()),r
 assert r['id'] in input_ids,r
 assert r['decision'] in allowed,r
 assert set(r['sentences'].split(','))<=sentences,r
 assert len(r['what_it_does'].split())<=15,r
 assert len(r['reason'].split())<=30,r
 assert r['basis'] in ('evidence','none') or r['basis'].startswith(('raw:','doc:')),r
 assert not any('\t' in v or '\n' in v or '\r' in v for v in r.values()),r
records=read(out) if out.exists() else []
for r in records:check(r)
seen={r['id']:corrected(r) for r in records};assert len(seen)==len(records)
with out.open('a',encoding='utf-8',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n')
 if f.tell()==0:writer.writeheader();f.flush()
 for k in (1,2,3):
  shard=root/f'D1/c1/part-mint.{k}.tsv'
  if not shard.exists():continue
  new=read(shard);assert len(new)==len({r['id'] for r in new}),shard
  for r in new:
   r=corrected(r)
   check(r)
   if r['id'] in seen:
    assert r==seen[r['id']],('conflicting duplicate',r['id'])
   else:
    writer.writerow(r);f.flush();seen[r['id']]=r
counts=collections.Counter(r['decision'] for r in seen.values())
print(json.dumps({'written':len(seen),'expected':len(input_ids),'counts':dict(counts)},sort_keys=True))
if args.finish:
 original=read(out)
 final=[corrected(r) for r in original]
 for r in final:check(r)
 if final!=original:
  audit=[{'before':a,'after':b} for a,b in zip(original,final) if a!=b]
  (root/'D1/c1/part-mint.correction-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
  with out.open('w',encoding='utf-8',newline='') as f:
   writer=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n')
   writer.writeheader();writer.writerows(final)
 final=read(out);ids=[r['id'] for r in final]
 assert len(ids)==len(input_ids)==len(set(ids)) and set(ids)==set(input_ids)
 for r in final:check(r)
 done=''.join(f'{d}\t{counts[d]}\n' for d in ('MUST','NOT','HOLE','UNKNOWN','MIXED'))
 (root/'D1/c1/part-mint.done').write_text(done,encoding='utf-8')
 print(done,end='')

import csv
import collections
import pathlib
import re
root=pathlib.Path(__file__).resolve().parents[2]
source=root/'A1/in/part-6.tsv'
out=root/'A1/c1/part-6.tsv'
expected=['id','decision','sentences','what_it_does','basis','reason']
with source.open(encoding='utf-8',newline='') as f:
 inputs=list(csv.DictReader(f,delimiter='\t'))
with out.open(encoding='utf-8',newline='') as f:
 reader=csv.DictReader(f,delimiter='\t')
 assert reader.fieldnames==expected,reader.fieldnames
 rows=list(reader)
valid={'MUST','NOT','HOLE','UNKNOWN','MIXED'}
source_ids=[r['id'] for r in inputs]
output_ids=[r['id'] for r in rows]
assert len(source_ids)==len(set(source_ids)), 'Duplicate input IDs'
assert len(output_ids)==len(set(output_ids)), 'Duplicate output IDs'
assert set(source_ids)==set(output_ids), {'missing':set(source_ids)-set(output_ids),'extra':set(output_ids)-set(source_ids)}
assert len(source_ids)==len(output_ids)
allowed=set(re.findall(r'\*\*(S(?:2\.2|3)-\d+)\*\*',(root/'SENTENCES.md').read_text()))
for r in rows:
 assert set(r)==set(expected),(r['id'],'bad columns')
 assert r['decision'] in valid,(r['id'],'bad decision')
 assert all(isinstance(v,str) and v and '\t' not in v and '\n' not in v and '\r' not in v for v in r.values()),r['id']
 assert len(r['what_it_does'].split())<=15,(r['id'],'description length')
 assert len(r['reason'].split())<=30,(r['id'],'reason length')
 assert set(r['sentences'].split(','))<=allowed,(r['id'],'sentence IDs')
 assert r['basis'] in {'evidence','none'} or r['basis'].startswith(('raw:','doc:http://','doc:https://')),(r['id'],'basis')
counts=collections.Counter(r['decision'] for r in rows)
done=root/'A1/c1/part-6.done'
done.write_text(''.join(f'{d}\t{counts[d]}\n' for d in ['MUST','NOT','HOLE','UNKNOWN','MIXED']),encoding='utf-8')
print(f'PASS: {len(rows)} rows, exact input ID set and count, each once; decisions and field constraints valid.')
print(done.read_text(),end='')

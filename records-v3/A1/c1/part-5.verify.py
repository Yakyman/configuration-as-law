"""Mechanical validation of the completed classification table."""
import csv
import re
from collections import Counter
from pathlib import Path

root=Path(__file__).resolve().parents[2]
source_path=root/'A1/in/part-5.tsv'
output_path=root/'A1/c1/part-5.tsv'
expected_header=['id','decision','sentences','what_it_does','basis','reason']
with source_path.open(encoding='utf-8',newline='') as f:
    source=list(csv.DictReader(f,delimiter='\t'))
with output_path.open(encoding='utf-8',newline='') as f:
    reader=csv.DictReader(f,delimiter='\t')
    assert reader.fieldnames==expected_header,reader.fieldnames
    output=list(reader)
source_ids=Counter(r['id'] for r in source)
output_ids=Counter(r['id'] for r in output)
assert all(n==1 for n in source_ids.values()),'Repeated input id'
assert all(n==1 for n in output_ids.values()),'Repeated output id'
assert output_ids==source_ids,{'missing':list(source_ids-output_ids),'extra':list(output_ids-source_ids)}
assert len(output)==len(source)
choices=('MUST','NOT','HOLE','UNKNOWN','MIXED')
sentence_ids=set(re.findall(r'\*\*(S[\d.]+-\d+)\*\*',(root/'SENTENCES.md').read_text()))
for row in output:
    assert set(row)==set(expected_header),row
    assert row['decision'] in choices,row
    assert row['sentences'] and set(row['sentences'].split(','))<=sentence_ids,row
    assert len(row['what_it_does'].split())<=15,row
    assert len(row['reason'].split())<=30,row
    assert row['basis'] in {'evidence','none'} or row['basis'].startswith(('raw:','doc:')),row
    assert all(v and not any(c in v for c in '\t\r\n') for v in row.values()),row
counts=Counter(row['decision'] for row in output)
report=''.join(f'{decision}\t{counts[decision]}\n' for decision in choices)
(root/'A1/c1/part-5.done').write_text(report,encoding='utf-8')
print(report,end='')

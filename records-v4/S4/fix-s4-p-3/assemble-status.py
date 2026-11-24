#!/usr/bin/env python3
"""Combine the four bounded rehearsal reports without changing other groups."""
import collections
import csv
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def read(path):
    with path.open(newline='') as stream:
        return list(csv.DictReader(stream,delimiter='\t'))

def write(path,rows,fields=None):
    with path.open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields or list(rows[0]),delimiter='\t',lineterminator='\n')
        writer.writeheader();writer.writerows(rows)

states=read(ROOT/'S4/fix-s4-p-2/tables/fact-status.tsv')
updates={}
for system in ('alma','void','microos','talos'):
    for row in read(HERE/'systems'/system/'fact-status.tsv'):
        row['evidence']=';'.join(p.strip() for p in row['evidence'].split(';'))
        updates[row['fact_id']]=row
write(HERE/'tables/fact-status.tsv',[updates.get(row['fact_id'],row) for row in states])
attempts=[]
base='S4/fix-s4-p-3/systems/alma/'
for line in (HERE/'systems/alma/raw/fact-diagnostics.jsonl').read_text().splitlines():
    d=json.loads(line)
    evidence=[base+'raw/fact-diagnostics.jsonl',base+'result.md']
    if d['method']=='application-installer-event-records':
        if d['fact_id'] in ('A07','A11'):
            evidence.append(base+'raw2/fact-diagnostics.jsonl')
        if d['fact_id']=='A07':
            evidence.extend([base+'raw3/fact-diagnostics.jsonl',base+'raw5/fact-summary.json'])
    attempts.append({'fact_id':d['fact_id'],'method':d['method'],'status':'failed-to-record-complete-fact','evidence':';'.join(evidence)})
for system,status_column in [('void','fact_status'),('microos','status'),('talos','result')]:
    for row in read(HERE/'systems'/system/'attempts.tsv'):
        status=row[status_column]
        if status in ('complete-fact-not-obtained','failed-to-complete-fact'):
            status='failed-to-record-complete-fact'
        attempts.append({key:row[key] for key in ('fact_id','method','evidence')}|{'status':status})
write(HERE/'checks/attempt-basis.tsv',attempts,['fact_id','method','status','evidence'])
counts=collections.Counter(r['status'] for r in attempts)
assert counts['failed-to-record-complete-fact']==42,counts
print(json.dumps({'updated_groups':len(updates),'attempt_rows':dict(counts)}))

#!/usr/bin/env python3
import hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from casedefs import CASES,PORT
from engine import validate
validate(CASES)
lock=json.loads((ROOT/'declarations/payloads.lock.json').read_text())
for name,expected in lock.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,name
ids=[r['old'] for r in PORT]
assert len(ids)==len(set(ids))
assert len([i for i in ids if i.startswith('P4-S-')])==19
# Published labels, never invented stand sentence IDs.
snapshot=json.loads((ROOT/'STATEMENT-LABELS.json').read_text())
labels=set(snapshot['labels'])
assert len(labels)==len(snapshot['labels'])==34
assert not labels & {'E1','E2','E3'}
used={s for c in CASES for s in c['statements']}
assert not used-labels,used-labels
assert not labels-used,labels-used
print('CATALOGUE PASS:',len(CASES),'cases;',len(PORT),'source IDs;',len(labels),'statement labels')

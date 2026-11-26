#!/usr/bin/env python3
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.dont_write_bytecode=True
from casedefs import BY_ID
from core import COVERAGE
case=BY_ID['G-SHELL']
empty={'schema':1,'lines':[]}
inv={'objects':[],'errors':[],'coverage':{k:{'status':'complete','evidence':'fixture '+k} for k in COVERAGE}}
replies=[{'returncode':0,'boot_id':'fixture-boot-1'},
         {'returncode':0,'stdout':'shell-ok','stderr':''},
         {'declaration':empty,'sha256':'fixture-law'},inv]
events=[{'request':s['request'],'reply':r} for s,r in zip(case['steps'],replies)]
(ROOT/'fixtures/shell-pass.json').write_text(json.dumps({'fixture':True,'events':events},indent=2)+'\n')
bad=copy.deepcopy(events[:2]);bad[1]['reply']['stdout']='wrong'
(ROOT/'fixtures/shell-fail.json').write_text(json.dumps({'fixture':True,'events':bad},indent=2)+'\n')
(ROOT/'fixtures/empty-declaration.json').write_text(json.dumps(empty,indent=2)+'\n')
(ROOT/'fixtures/empty-inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
print('Fixture transcripts written; no system evidence')

"""usage: analyze_pair.py CASEDIR BUNDLE  -> writes judge-left/right-fulfil.json and judge-pair.json into CASEDIR"""
import json,sys,subprocess,os
case,bundle=sys.argv[1],sys.argv[2]
here=os.path.dirname(os.path.abspath(__file__))
for s in ('left','right'):
    r=subprocess.run(['/usr/bin/python3','-I',f'{here}/judge.py','fulfil',f'{case}/{s}-snapshot.stdout',bundle],capture_output=True,text=True)
    open(f'{case}/judge-{s}-fulfil.json','w').write(r.stdout+r.stderr)
    d=json.loads(r.stdout); print(s,'mismatches',d['mismatch_count'],d['by_line_and_kind'])
r=subprocess.run(['/usr/bin/python3','-I',f'{here}/judge.py','pair',f'{case}/pair-diff.stdout'],capture_output=True,text=True)
open(f'{case}/judge-pair.json','w').write(r.stdout+r.stderr); print(json.loads(r.stdout))

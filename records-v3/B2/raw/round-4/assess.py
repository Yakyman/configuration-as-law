#!/usr/bin/env python3
"""Summarize saved final evidence without converting failed observations to passes."""
import hashlib,json,pathlib,sys
root=pathlib.Path(__file__).resolve().parent
out={"scope":[*("C2."+str(n) for n in range(1,7)),*("C3."+str(n) for n in range(1,6)),*("C9."+str(n) for n in range(1,7))],"suites":{},"variants":{}}
def records(path):
    for line in path.read_text().splitlines():
        try:yield json.loads(line)
        except ValueError:continue
for name in ('language','applications','system','ordinary'):
    path=root/'rebuilt'/(name+'.jsonl');rows=list(records(path));expected={}
    for r in rows:
        if r.get('phase')=='expected':expected[r['id']]=r
    results=[r for r in rows if r.get('phase')=='result' and isinstance(r.get('passed'),bool)]
    out['suites'][name]={"evidence":str(path.relative_to(root)),"results":len(results),"failed":[r['id'] for r in results if not r['passed']]}
    for r in results:
        for variant in expected.get(r['id'],{}).get('variants',r.get('variants',[])):
            value=out['variants'].setdefault(variant,{"passed":[],"failed":[]})
            value['passed' if r['passed'] else 'failed'].append(name+':'+r['id'])
for name in ('round1','round2','round3','powercuts','inventory','boot-order'):
    path=root/'rebuilt/regressions'/(name+'.jsonl')
    if not path.exists():continue
    rows=list(records(path));results=[r for r in rows if r.get('id') and (isinstance(r.get('passed'),bool) or isinstance(r.get('ok'),bool))]
    out['suites'][name]={"evidence":str(path.relative_to(root)),"results":len(results),"failed":[r.get('id','summary') for r in results if not r.get('passed',r.get('ok'))]}
for label,relative in [('rebuilt','rebuilt/summary.json'),('regressions','rebuilt/regressions/summary.json'),('combined','combined/summary.json')]:
    out[label]=json.loads((root/relative).read_text())
for name in ('applications-helper-availability.jsonl',):
    out[name]=list(records(root/'rebuilt'/name))
combine=list(records(root/'combined/events.jsonl'))
out['combined_assertions']=[r for r in combine if r.get('phase')=='assertion']
out['all_required_summaries_zero']=all(out[name]['suite_exit']==0 for name in ('rebuilt','regressions','combined'))
out['all_observed_assertions_pass']=not any(s['failed'] for s in out['suites'].values()) and all(r['passed'] for r in out['combined_assertions'])
out['all_scoped_variants_have_passing_evidence']=all(out['variants'].get(v,{}).get('passed') and not out['variants'][v]['failed'] for v in out['scope'])
factory=root/'rebuilt/factory-export/factory'
factory_rows=list(records(factory/'machine.jsonl'))
base_files=json.loads((factory/'base-files.json').read_text())
source_root=root.parents[1]/'build'
installed={}
for value in base_files:
    path=pathlib.Path(value['path'])
    source=source_root/path.name
    if path.parent==pathlib.Path('/usr/local/lib/stand') and source.is_file() and value['kind']=='file':
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        installed[path.name]={'recipe_sha256':digest,'installed_sha256':value['sha256'],'equal':digest==value['sha256']}
out['factory']={'rows':len(factory_rows),'base_file_entries':len(base_files),
                'packages':sum(r['id'].startswith('package:') for r in factory_rows),
                'installed_recipe_sources':installed}
out['installed_recipe_sources_match']=bool(installed) and all(r['equal'] for r in installed.values())
out['acceptance']='requires independent review of mechanisms and evidence; this script only aggregates saved results'
(root/'ASSESSMENT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('variants','combined_assertions')},indent=2,sort_keys=True))
sys.exit(not all(out[k] for k in ('all_required_summaries_zero','all_observed_assertions_pass','all_scoped_variants_have_passing_evidence','installed_recipe_sources_match')))

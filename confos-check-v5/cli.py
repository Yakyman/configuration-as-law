#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
from adapter import Transcript,StandPlan,collect_tree,fixture_package_reader
from core import read_json,derive,compare,outcome
from engine import validate,execute,report,request_entries


def main(tool=None):
    tool=tool or Path(sys.argv[0]).name
    p=argparse.ArgumentParser(description='ConfOS portable checks; fixture mode is never a system run.')
    if tool=='derive':
        p.add_argument('--declaration',required=True); p.add_argument('--fixture-packages')
        a=p.parse_args(); reader=fixture_package_reader(a.fixture_packages) if a.fixture_packages else None
        result=derive(read_json(a.declaration),reader)
    elif tool=='inventory':
        p.add_argument('--fixture-root',required=True); p.add_argument('--force')
        a=p.parse_args(); result=collect_tree(a.fixture_root)
        if a.force:
            force=read_json(a.force); result['objects']+=force['objects']; result['errors']+=force.get('errors',[])
            result['coverage'].update(force.get('coverage',{}))
    elif tool=='compare':
        p.add_argument('--derived',required=True); p.add_argument('--inventory',required=True)
        a=p.parse_args(); issues=compare(read_json(a.derived),read_json(a.inventory))
        result={'outcome':outcome(issues),'issues':issues}
    elif tool=='run':
        from casedefs import CASES,BY_ID
        p.add_argument('--list',action='store_true'); p.add_argument('--validate',action='store_true')
        p.add_argument('--case'); p.add_argument('--fixture'); p.add_argument('--fixture-packages')
        p.add_argument('--plan',action='store_true'); p.add_argument('--out'); p.add_argument('--variant')
        a=p.parse_args(); validate(CASES)
        if a.list:
            print('\n'.join(BY_ID)); return 0
        if a.validate:
            print('VALID: '+str(len(CASES))+' portable case definitions'); return 0
        if not a.case or a.case not in BY_ID: p.error('--case must name a known case')
        case=BY_ID[a.case]
        if a.plan:
            print(json.dumps(case,indent=2)); return 0
        if not a.fixture: p.error('no release interface bound: only --fixture, --plan, --list or --validate in part 1')
        if case.get('variants') and a.variant not in case['variants']: p.error('select a listed --variant; each variant is a separate execution')
        backend=Transcript(a.fixture)
        reader=fixture_package_reader(a.fixture_packages) if a.fixture_packages else None
        rows,evidence=execute(case,backend,reader,a.variant)
        backend.finish()
        result={'fixture':True,'case':case['id'],'rows':rows,'evidence':evidence,'requests':request_entries(rows,evidence)}
        if a.out:
            out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
            (out/'report.md').write_text(report(rows,'fixture',True))
            (out/'evidence.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2)); return 1 if any(r['outcome']=='fail' for r in rows) else 2 if any(r['outcome']=='unobserved' for r in rows) else 3 if any(r['outcome']=='undecided' for r in rows) else 0
    else: raise ValueError('unknown entry point '+tool)
    print(json.dumps(result,indent=2)); return 1 if result.get('outcome')=='fail' else 2 if result.get('errors') or result.get('outcome')=='unobserved' else 0

if __name__=='__main__': raise SystemExit(main())

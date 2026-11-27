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
        p.add_argument('--native',help='local.env with a "native" section: run on a named release (part 2)')
        p.add_argument('--all',action='store_true',help='with --native: every case and variant')
        p.add_argument('--shard',help='with --native: K/N, every N-th execution from K (own ports K)')
        a=p.parse_args(); validate(CASES)
        if a.native:
            return native_run(a, CASES, BY_ID, p)
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

def native_run(a, CASES, BY_ID, p):
    """Part 2 only: performs cases on the release named in local.env. Writes raw outputs."""
    import adapter_native as N
    from engine import execute_suite
    env=read_json(a.native); cfg=env.get('native')
    if not cfg or env.get('release') in (None,'UNBOUND'): p.error('local.env names no release and no native section')
    if not a.out: p.error('--out is required for a native run')
    shard=(0,1)
    if a.shard:
        k,n=map(int,a.shard.split('/')); shard=(k,n)
        cfg=dict(cfg,ssh_port=int(cfg['ssh_port'])+k,server_port=int(cfg['server_port'])+k,
                 server_url=cfg['server_url'].rsplit(':',1)[0]+':'+str(int(cfg['server_port'])+k))
    b=N.Bindings({'@SERVER@':cfg['server_url'],'@KEY_TYPE@':cfg['key_type'],'@KEY@':cfg['key']})
    b.local=cfg
    names=(a.case or '').split(',')
    cases=CASES if a.all else [BY_ID[c] for c in names] if a.case and all(c in BY_ID for c in names) else p.error('--case (one or several, comma-separated) or --all')
    if not a.all and cases[0].get('variants') and a.variant:
        cases=[dict(cases[0],variants=[a.variant])]
    if shard[1]>1:
        from engine import execution_matrix
        matrix=execution_matrix(cases)
        first={c['id']:i for i,(c,v) in reversed(list(enumerate(matrix)))}
        # OW-2 then OW-3 on one installation: OW-3 goes to the shard of OW-2, right after it
        def owner(i,c): return first['OW-2'] if c.get('sequence') and c['id']!='OW-2' and 'OW-2' in first else i
        mine=[cv for i,cv in enumerate(matrix) if owner(i,cv[0])%shard[1]==shard[0]]
        if any(c['id']=='OW-3' for c,v in mine):
            mine=[cv for cv in mine if cv[0]['id']!='OW-3']
            k=next(j for j,cv in enumerate(mine) if cv[0]['id']=='OW-2')+1
            mine.insert(k,next(cv for cv in matrix if cv[0]['id']=='OW-3'))
        cases=[dict(c,variants=[v]) if v is not None else c for c,v in mine]
    out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    index,built=N.build_derive_store(cfg,b,out/'derive-store')
    bad=[k for k,v in built.items() if v['returncode']]
    if bad: print('independent payload builds failed: '+json.dumps({k:built[k] for k in bad})[:2000],file=sys.stderr)
    cfg=dict(cfg,derive_store=str(out/'derive-store'),derive_index=index)
    files=N.make_server_files(b,out/'server',str(out/'derive-store'))
    server=N.PayloadServer(out/'server',cfg['server_port'])
    def factory(case,variant):
        class Lazy:
            def __init__(s): s.n=None; s.err=None
            def perform(s,request):
                if s.n is None: s.n=N.Native(dict(cfg,work=str(out/'work')),b,case,variant)
                return s.n.perform(request)
            def finish(s):
                if s.n: s.n.finish()
        return Lazy()
    try:
        reader=N.Native(dict(cfg,work=str(out/'work')),b,{'id':'-','steps':[]}).package_reader()
    except Exception as exc:
        reader=None; print('package reader unavailable: '+str(exc),file=sys.stderr)
    from engine import execute, execution_matrix, request_entries
    result={'rows':[],'evidence':[],'requests':[]}
    progress=open(out/'progress.jsonl','a')
    try:
        for case,variant in execution_matrix(cases):
            backend=factory(case,variant)
            try:
                cr,ce=execute(case,backend,reader,variant)
            finally:
                backend.finish()
            rq=request_entries(cr,ce)
            result['rows']+=cr; result['evidence'].append({'case':case['id'],'variant':variant,'events':ce}); result['requests']+=rq
            progress.write(json.dumps({'case':case['id'],'variant':variant,'rows':cr,'events':ce,'requests':rq},default=str)+'\n'); progress.flush()
    finally:
        server.close(); progress.close()
    result['release']=env['release']; result['server_files']=files; result['server_log']=server.log
    (out/'evidence.json').write_text(json.dumps(result,indent=1,default=str)+'\n')
    (out/'report.md').write_text(report(result['rows'],env['release']))
    (out/'requests.json').write_text(json.dumps(result['requests'],indent=1,default=str)+'\n')
    print('rows',len(result['rows']),'requests',len(result['requests']))
    return 1 if any(r['outcome']=='fail' for r in result['rows']) else 0

if __name__=='__main__': raise SystemExit(main())

"""Scenario execution and per-check reports; the adapter supplies observations only."""
import json
from collections import Counter
from pathlib import Path
from adapter import Unavailable
from core import check, compare, derive, resolve, outcome, aggregate, evaluate_query


def validate(cases):
    ids=set()
    for case in cases:
        if case['id'] in ids: raise ValueError('duplicate case')
        ids.add(case['id']); names=set()
        if not case['statements']: raise ValueError('case without statement')
        if not case['steps'] and case['kind']!='logic': raise ValueError('empty system case')
        for step in case['steps']:
            if step['name'] in names: raise ValueError(case['id']+': duplicate step '+step['name'])
            names.add(step['name'])
            if not step['request'].get('op'): raise ValueError('missing operation')
            for c in step.get('checks',[]):
                if c['op'] not in ('eq','ne','match','not-match','contains','gt','in'):
                    raise ValueError('unknown assertion')
        if len(set(case.get('variants',[])))!=len(case.get('variants',[])):
            raise ValueError('duplicate variant')
    return True


def execute(case, backend, package_reader=None, variant=None):
    captures={}; rows=[]; evidence=[]; blocked=None
    def row(name,result,detail,part='case'):
        rows.append({'case':case['id'],'variant':variant,'check':name,'part':part,'outcome':result,'detail':detail})
    if case['kind']=='logic':
        matrix=[([], '?'),([{'outcome':'pass'}],'1'),([{'outcome':'fail'}],'0'),
                ([{'outcome':'unobserved'}],'?'),([{'outcome':'undecided'}],'?'),
                ([{'outcome':'fail'},{'outcome':'unobserved'}],'0')]
        for i,(test,want) in enumerate(matrix):
            row('logic-'+str(i),'pass' if aggregate(test)==want else 'fail',{'expected':want,'actual':aggregate(test)},'logic')
        return rows,evidence
    for s in case['steps']:
        name=s['name']
        if blocked:
            evidence.append({'step':name,'request':s['request'],'unavailable':blocked})
            row(name,'unobserved',{'reason':blocked})
            for part in s.get('companion_parts',[]): row(name,'unobserved',{'reason':blocked},part)
            continue
        try:
            request=resolve(s['request'],captures)
            if variant is not None: request=dict(request,variant=variant,case=case['id'])
            reply=backend.perform(request)
            if reply.get('availability')=='unsupported':
                raise Unavailable(reply.get('reason','documented capability unavailable'))
            if request['op']=='query':
                reply=evaluate_query(request['subject'],reply)
            if request['op']=='apply-cut':
                # Exact success is checked by the case; ordering is derived here.
                reply=dict(reply,cut_after_success=(reply['cut_monotonic']>=reply['success_monotonic']
                     and reply['success_observed'] is True))
            captures[name]=reply
            evidence.append({'step':name,'request':request,'reply':reply})
            for i,c in enumerate(s.get('checks',[])):
                result,detail=check(reply,c,captures)
                row(name+':'+str(i+1),result,detail)
                # Failed setup, missing tools, unconfirmed application are not a valid basis
                # for later negative observations. Preserve that failure and stop dependents.
                if result!='pass': blocked='dependency '+name+' did not pass'
            if not s.get('checks') and not s.get('compare_to'):
                row(name,'pass',{'capture':name,'meaning':'action/capture completed; not a policy verdict'})
            if s.get('compare_to'):
                declaration=resolve(s['compare_to'],captures)
                expected=derive(declaration,package_reader)
                issues=compare(expected,reply)
                for part in s['companion_parts']:
                    relevant=issues
                    if part=='P1': relevant=[x for x in issues if x['status']!='MISSING']
                    if part=='P2': relevant=[x for x in issues if x['status']!='UNRECORDED']
                    row(name,outcome(relevant),{'issues':relevant,'declaration':expected['declaration_sha256']},part)
        except Unavailable as exc:
            blocked=str(exc)
            evidence.append({'step':name,'request':s['request'],'unavailable':blocked})
            row(name,'unobserved',{'reason':blocked})
            for part in s.get('companion_parts',[]): row(name,'unobserved',{'reason':blocked},part)
        except (KeyError,ValueError,TypeError,OSError) as exc:
            blocked='checker/adapter error: '+str(exc)
            row(name,'unobserved',{'reason':blocked})
            evidence.append({'step':name,'error':blocked})
            for part in s.get('companion_parts',[]): row(name,'unobserved',{'reason':blocked},part)
    results=[r['outcome'] for r in rows]
    summary=('fail' if 'fail' in results else 'unobserved' if 'unobserved' in results
             else 'undecided' if 'undecided' in results else 'pass')
    row('case-result',summary,{'question':case.get('question'),'checks':len(rows)},'case-summary')
    return rows,evidence


def report(rows, release, fixture=False):
    counts=Counter(r['outcome'] for r in rows)
    title='Fixture checker report' if fixture else 'Case report'
    lines=['# '+title,'', 'Release: '+release+'. '+('FIXTURE ONLY; no system observation.' if fixture else 'Raw check outcomes; independent acceptance is separate.'),'',
           'Counts: '+', '.join(k+' '+str(counts[k]) for k in ('pass','fail','undecided','unobserved'))+'.',
           'Operational check verdict: '+aggregate(rows)+'. This is not a proof of impossibility or final plan acceptance.','',
           '| Case | Variant | Check | Part | Outcome | Evidence / reason |','|---|---|---|---|---|---|']
    def safe(v): return str(v).replace('|','\\|').replace('\n',' ')
    for r in rows:
        lines.append('| '+' | '.join(safe(x) for x in [r['case'],r.get('variant') or '-',r['check'],r['part'],r['outcome'],json.dumps(r['detail'],sort_keys=True)])+' |')
    return '\n'.join(lines)+'\n'


def request_entries(rows,evidence):
    """Every fail/unobserved gets an entry; no suppressed setup/companion failures."""
    entries=[]
    for r in rows:
        if r['outcome'] not in ('fail','unobserved'): continue
        name=r['check'].split(':')[0]
        ev=next((e for e in evidence if e.get('step')==name),{})
        entries.append({'case':r['case'],'check':r['check'],'part':r['part'],
                        'command':ev.get('request',{'blocked-step':name}),
                        'output':ev.get('reply',ev.get('unavailable',ev.get('error','not reached'))),
                        'expected':r['detail']})
    return entries


def execution_matrix(cases):
    """No variant disappears into a family-level pass."""
    return [(c,v) for c in cases for v in c.get('variants',[]) or [None]]


def execute_suite(cases,backend_factory,package_reader=None):
    """Part-2 orchestration; factory owns transport lifecycle and cleanup.

    A factory must preserve explicit sequence installations for OW-2/OW-3;
    all other fresh operations are independent clean installations.
    """
    rows=[]; evidence=[]; requests=[]
    for case,variant in execution_matrix(cases):
        backend=backend_factory(case,variant)
        try:
            cr,ce=execute(case,backend,package_reader,variant)
            rows.extend(cr)
            evidence.append({'case':case['id'],'variant':variant,'events':ce})
            requests.extend(request_entries(cr,ce))
        finally:
            backend.finish()
    return {'rows':rows,'evidence':evidence,'requests':requests}

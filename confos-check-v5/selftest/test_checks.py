#!/usr/bin/env python3
"""Adversarial fixtures test checking programs, never claim a system observation."""
import copy, hashlib, io, json, os, subprocess, sys, tarfile, tempfile, unittest
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core import *
from adapter import Transcript,StandPlan,Unavailable,collect_tree,fixture_package_reader
from engine import validate,execute,report,request_entries
from casedefs import CASES,BY_ID,PORT

def coverage():
    return {k:{'status':'complete','evidence':'fixture raw capture '+k} for k in COVERAGE}
def declaration():
    return {'lines':[{'id':'binary','kind':'file','path':'/bin/probe','text':'known executable bytes',
                     'mode':'0755','uid':0,'gid':0},
                    {'id':'host','kind':'object','object':{'kind':'hostname','id':'system','value':{'name':'test'}}}]}
def clean():
    d=derive(declaration())
    return d,{'objects':copy.deepcopy([{k:v for k,v in o.items() if k!='owners'} for o in d['objects']]),
              'coverage':coverage(),'errors':[]}
def fixture_case():
    return {'id':'FIXTURE','kind':'system','statements':['K1'],'steps':[
        {'name':'old','request':{'op':'read-law'},'checks':[]},
        {'name':'attempt','request':{'op':'command','command':'attempt'},'checks':[]},
        {'name':'marker','request':{'op':'query','subject':'marker'},'checks':[{'field':'value','op':'eq','value':False}]},
        {'name':'inventory','request':{'op':'inventory'},'checks':[],
         'compare_to':{'ref':'old.declaration'},'companion_parts':['P1','UND','P2']} ]}

class Comparisons(unittest.TestCase):
    def test_clean(self):
        e,o=clean(); self.assertEqual(compare(e,o),[])
    def test_unrecorded_file(self):
        e,o=clean(); o['objects'].append({'kind':'file','id':'/bin/rogue','value':{'sha256':'bad'}})
        self.assertEqual(outcome(compare(e,o)),'fail')
    def test_changed_named_value(self):
        e,o=clean(); o['objects'][1]['value']['name']='changed'
        self.assertTrue(any(i['status']=='DIFFERS' for i in compare(e,o)))
    def test_missing_declared_file(self):
        e,o=clean(); o['objects'].pop(0)
        self.assertTrue(any(i['status']=='MISSING' for i in compare(e,o)))
    def test_no_inventory_cannot_pass(self):
        e,o=clean(); self.assertNotEqual(outcome(compare(e,{})),'pass')
    def test_capture_error(self):
        e,o=clean(); o['errors']=[{'kind':'sysctl','reason':'permission denied'}]
        self.assertEqual(outcome(compare(e,o)),'unobserved')
    def test_coverage_omission(self):
        e,o=clean(); del o['coverage']['module']
        self.assertEqual(outcome(compare(e,o)),'unobserved')
    def test_missing_field_not_equal_to_empty(self):
        e,o=clean(); del o['objects'][0]['value']['sha256']
        self.assertEqual(outcome(compare(e,o)),'unobserved')
    def test_duplicate_object(self):
        e,o=clean(); o['objects'].append(o['objects'][0])
        self.assertEqual(outcome(compare(e,o)),'unobserved')
    def test_namespace_recorded_hash(self):
        e,o=clean(); h=o['objects'][0]['value']['sha256']
        o['objects'].append({'kind':'process','id':'/sandbox/bin/probe','value':{'exe_sha256':h,'exe_evidence':'read process root'}})
        self.assertEqual(compare(e,o),[])
    def test_namespace_same_path_different_bytes(self):
        e,o=clean(); o['objects'].append({'kind':'process','id':'/bin/probe','value':{'exe_sha256':'rogue','exe_evidence':'read process root'}})
        self.assertEqual(outcome(compare(e,o)),'fail')
    def test_port_hash_attribution(self):
        e,o=clean(); h=o['objects'][0]['value']['sha256']
        o['objects'].append({'kind':'port','id':'tcp:9876','value':{'exe_sha256':h,'exe_evidence':'socket owner -> process root'}})
        self.assertEqual(compare(e,o),[])
    def test_port_no_owner(self):
        e,o=clean(); o['objects'].append({'kind':'port','id':'tcp:9876','value':{}})
        self.assertEqual(outcome(compare(e,o)),'unobserved')
    def test_material_data_route(self):
        e,o=clean(); o['objects'].append({'kind':'file','id':'/home/user/document','value':{},'classification':'material',
            'origin_evidence':'typed write','route_evidence':'routes.json','routes':[
                {'kind':'direct','observed':True,'executed':False},
                {'kind':'data','observed':True,'executed':True}]})
        self.assertEqual(compare(e,o),[])
    def test_material_direct_execution_not_ignored(self):
        e,o=clean(); o['objects'].append({'kind':'file','id':'/home/user/script','value':{},'classification':'material',
            'origin_evidence':'typed write','route_evidence':'routes.json','routes':[{'kind':'direct','observed':True,'executed':True}]})
        self.assertEqual(outcome(compare(e,o)),'fail')
    def test_material_installs_cannot_pass(self):
        e,o=clean(); o['objects'].append({'kind':'file','id':'/home/user/script','value':{},'classification':'material',
            'origin_evidence':'typed write','route_evidence':'routes.json','routes':[{'kind':'data','observed':True,'installed':True}]})
        self.assertEqual(outcome(compare(e,o)),'fail')
    def test_no_blanket_home_exemption(self):
        e,o=clean(); o['objects'].append({'kind':'file','id':'/home/user/hidden','value':{}})
        self.assertEqual(outcome(compare(e,o)),'fail')
    def test_open_folder_exact_boundary(self):
        e,o=clean(); e['openings']=['/home/user/open']
        item={'kind':'file','id':'/home/user/open/script','value':{'resolved_path':'/home/user/open/script'},
              'classification':'opened-material','route_evidence':'direct route'}
        o['objects'].append(item); self.assertEqual(compare(e,o),[])
        item['value']['resolved_path']='/home/user/open-sibling/script'
        self.assertEqual(outcome(compare(e,o)),'fail')
    def test_symlink_escape_not_opened(self):
        e,o=clean(); e['openings']=['/home/user/open']
        o['objects'].append({'kind':'file','id':'/home/user/open/link','value':{'resolved_path':'/home/user/closed/script'},
            'classification':'opened-material','route_evidence':'resolved symlink'})
        self.assertEqual(outcome(compare(e,o)),'fail')
    def test_opening_not_settings_blanket(self):
        e,o=clean(); e['openings']=['/']
        o['objects'].append({'kind':'sysctl','id':'forward','value':{'resolved_path':'/proc/sys/net/ip_forward'},
            'classification':'opened-material','route_evidence':'direct route'})
        self.assertEqual(outcome(compare(e,o)),'fail')
    def test_radio_sysctl_module_in_inventory(self):
        for kind in ('wifi','bluetooth','sysctl','module','saved-network'):
            e,o=clean(); o['objects'].append({'kind':kind,'id':'unrecorded','value':{'active':True}})
            self.assertEqual(outcome(compare(e,o)),'fail',kind)
    def test_external_accounts_named_source(self):
        d=declaration(); d['lines'].append({'id':'source','kind':'external-accounts','source':'fixture://accounts'})
        e=derive(d); _,o=clean(); o['objects']+=copy.deepcopy(e['objects'][2:]); o['objects'].append(
            {'kind':'account','id':'external-user','value':{'external_source':'fixture://accounts','source_evidence':'actual query'}})
        self.assertEqual(compare(e,o),[])
        o['objects'][-1]['value']['external_source']='fixture://other'
        self.assertEqual(outcome(compare(e,o)),'fail')

class Derivation(unittest.TestCase):
    def test_shared_owners(self):
        d={'lines':[{'id':'a','kind':'object','object':{'kind':'file','id':'/shared','value':{'sha256':'same'}}},
                    {'id':'b','kind':'object','object':{'kind':'file','id':'/shared','value':{'sha256':'same'}}}]}
        self.assertEqual(derive(d)['objects'][0]['owners'],['a','b'])
        d['lines'].pop(0); self.assertEqual(derive(d)['objects'][0]['owners'],['b'])
        d['lines'].clear(); self.assertEqual(derive(d)['objects'],[])
    def test_conflicting_owners_rejected(self):
        obj={'kind':'hostname','id':'system','value':{'name':'a'}}
        d={'lines':[{'id':'a','kind':'object','object':obj},{'id':'b','kind':'object','object':dict(obj,value={'name':'b'})}]}
        with self.assertRaises(ValueError): derive(d)
    def test_unknown_kind_is_underived(self):
        self.assertTrue(derive({'lines':[{'id':'x','kind':'unknown'}]})['errors'])
    def test_binding_cannot_pass(self):
        self.assertTrue(derive({'lines':[{'id':'x','kind':'binding','name':'release'}]})['errors'])
    def test_open_values_not_promised(self):
        d={'lines':[{'id':'a','kind':'object','object':{'kind':'account','id':'test','value':{'shell':'/bin/sh'}}}]}
        e=derive(d); o={'objects':[{'kind':'account','id':'test','value':{'shell':'/bin/sh','uid':984}}], 'coverage':coverage()}
        self.assertEqual(compare(e,o),[])
        o['objects'][0]['value']['shell']='/other'; self.assertEqual(outcome(compare(e,o)),'fail')
    def test_package_hash_and_members(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'selftest') as tmp:
            p=Path(tmp)/'fixture.tar'
            with tarfile.open(p,'w') as t:
                m=tarfile.TarInfo('usr/bin/one'); m.size=3; m.mode=0o755;t.addfile(m,io.BytesIO(b'one'))
            line={'id':'pkg','kind':'package','name':'one','version':'1','source_sha256':'source',
                  'recipe_sha256':'recipe','archive':'fixture.tar','archive_sha256':digest(p.read_bytes())}
            e=derive({'lines':[line]},fixture_package_reader(tmp))
            self.assertEqual(e['objects'][1]['value']['sha256'],digest(b'one'))
            line['archive_sha256']='bad'; self.assertTrue(derive({'lines':[line]},fixture_package_reader(tmp))['errors'])
    def test_archive_traversal_and_duplicates(self):
        for names in (['../escape'],['x','x'],['/absolute']):
            with tempfile.TemporaryDirectory(dir=ROOT/'selftest') as tmp:
                p=Path(tmp)/'fixture.tar'
                with tarfile.open(p,'w') as t:
                    for name in names:
                        m=tarfile.TarInfo(name);m.size=1;t.addfile(m,io.BytesIO(b'x'))
                with self.assertRaises(ValueError): fixture_package_reader(tmp)({'archive':'fixture.tar','archive_sha256':digest(p.read_bytes())})

class Runner(unittest.TestCase):
    def test_all_cases_valid(self): self.assertTrue(validate(CASES))
    def test_all_origins_have_target(self):
        self.assertEqual(len({r['old'] for r in PORT}),153)
        self.assertTrue(all(r['target'] in BY_ID for r in PORT))
    def test_all_untested_statements(self):
        labels={x for c in CASES for x in c['statements']}
        self.assertFalse(set('N W1d W3d W4a W4c W5b Q1 Q9'.split())-labels)
    def test_fixture_success_and_failure(self):
        for ran in (False,True):
            c=fixture_case(); _,inv=clean()
            events=[{'request':c['steps'][0]['request'],'reply':{'declaration':declaration()}},
                    {'request':c['steps'][1]['request'],'reply':{'returncode':0,'stdout':'','stderr':''}},
                    {'request':c['steps'][2]['request'],'reply':{'value':ran}}]
            if not ran: events.append({'request':c['steps'][3]['request'],'reply':inv})
            with tempfile.TemporaryDirectory(dir=ROOT/'selftest') as tmp:
                p=Path(tmp)/'t.json'; p.write_text(json.dumps({'events':events}))
                backend=Transcript(p); rows,ev=execute(c,backend);backend.finish()
                self.assertEqual(rows[-1]['outcome'],'fail' if ran else 'pass')
                if ran:
                    self.assertTrue(any(r['outcome']=='unobserved' and r['part']=='UND' for r in rows))
                    self.assertEqual(len(request_entries(rows,ev)),sum(r['outcome'] in ('fail','unobserved') for r in rows))
                    self.assertTrue(all('op' in r['command'] for r in request_entries(rows,ev) if r['check']!='case-result'))
                self.assertIn('FIXTURE ONLY',report(rows,'fixture',True))
    def test_unavailable_no_false_pass(self):
        rows,_=execute(fixture_case(),StandPlan())
        self.assertTrue(all(r['outcome']=='unobserved' for r in rows))
    def test_request_mismatch(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'selftest') as tmp:
            p=Path(tmp)/'t.json';p.write_text(json.dumps({'events':[{'request':{'op':'wrong'},'reply':{}}]}))
            rows,_=execute(fixture_case(),Transcript(p))
            self.assertEqual(rows[-1]['outcome'],'unobserved')
    def test_no_unused_transcript(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'selftest') as tmp:
            p=Path(tmp)/'t.json';p.write_text(json.dumps({'events':[{'request':{'op':'x'},'reply':{}}]}))
            with self.assertRaises(ValueError): Transcript(p).finish()
    def test_missing_probe_not_refusal(self):
        result,_=check({'returncode':127},{'field':'returncode','op':'eq','value':1},{})
        self.assertEqual(result,'fail')
        result,_=check({}, {'field':'value','op':'eq','value':False},{})
        self.assertEqual(result,'unobserved')
    def test_two_readings(self):
        condition={'field':'value','op':'eq','value':'strict','alternative':{'field':'value','op':'eq','value':'broad'},'question':'Q-DERIVE'}
        self.assertEqual(check({'value':'broad'},condition,{})[0],'undecided')
        self.assertEqual(check({'value':'neither'},condition,{})[0],'fail')
    def test_stand_plan_not_execution(self):
        a=StandPlan(); self.assertEqual(a.plan({'op':'apply'})['argv'],['confos','apply'])
        with self.assertRaises(Unavailable): a.render_line({'kind':'open-folder'})
        with self.assertRaises(Unavailable): a.perform({'op':'command','command':'touch host'})
    def test_unknown_status_never_success(self):
        condition={'field':'status','op':'eq','value':'APPLIED '+'a'*64}
        self.assertEqual(check({'status':'REBOOTING'},condition,{})[0],'fail')
    def test_every_failure_kept_despite_later_prohibition(self):
        rows=[{'outcome':'fail'},{'outcome':'pass'}]
        self.assertEqual(aggregate(rows),'0')

class Collector(unittest.TestCase):
    def test_symlinks_are_not_followed(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'selftest') as tmp:
            p=Path(tmp); (p/'file').write_text('data');(p/'link').symlink_to('/outside-do-not-read')
            o=collect_tree(p)
            self.assertEqual(len(o['objects']),2); self.assertEqual(o['errors'],[])
            self.assertEqual(o['objects'][1]['value']['target'],'/outside-do-not-read')
    def test_no_live_coverage_in_tree_fixture(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'selftest') as tmp:
            o=collect_tree(tmp);e=derive({'lines':[]})
            self.assertEqual(outcome(compare(e,o)),'unobserved')

class IndependentPredicates(unittest.TestCase):
    def test_adapter_boolean_cannot_replace_operands(self):
        with self.assertRaises(KeyError): evaluate_query('named-state-equal',{'value':True})
        reply=evaluate_query('named-state-equal',{'value':True,'left':{'source':'a'},'right':{'source':'b'},'evidence':'raw captures'})
        self.assertFalse(reply['value'])
    def test_candidate_delta_extra_line_fails(self):
        r={'before_lines':['base'],'after_lines':['base','wanted','unexpected'],
           'expected_added':['wanted'],'expected_removed':[], 'binding_evidence':'frozen case input'}
        self.assertFalse(evaluate_query('request-delta-valid',r)['value'])
        r['after_lines']=['base'];self.assertTrue(evaluate_query('request-delta-valid',r)['value'])
    def test_payload_update_is_not_system_update(self):
        r={'before_components':{'kernel':'a','case-small':'1'},'after_components':{'kernel':'a','case-small':'2'},
           'system_components':['kernel'],'binding_evidence':'system source lock'}
        self.assertFalse(evaluate_query('system-components-changed',r)['value'])
    def test_missing_object_in_partial_capture_is_unobserved(self):
        e,o=clean();o['objects'].pop(0);o['coverage']['stored']['status']='incomplete'
        self.assertEqual(outcome(compare(e,o)),'unobserved')
    def test_unknown_derivation_does_not_false_accuse(self):
        e,o=clean();e['errors']=[{'line':'base','reason':'unresolved'}]
        o['objects'].append({'kind':'file','id':'/unknown','value':{}})
        self.assertEqual(outcome(compare(e,o)),'unobserved')

if __name__=='__main__': unittest.main(verbosity=2)

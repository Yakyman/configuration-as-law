#!/usr/bin/python3 -I
"""Fixed finite rule expectations. Pure tests; no machine census or acceptance.

The fixture states semantic facts explicitly; it does not demonstrate that any
real interpreter, module or sandbox has the stated capabilities.
"""
import json
import pathlib
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import object_rules

NOT_PACKAGE={'package_installed':False,'package_member':False}
CONTAINED={**NOT_PACKAGE,'executable':True,'inside_recorded_program':True,
           'cannot_launch_programs':True,'cannot_change_installed':True,'cannot_change_settings':True}
VALUE={**NOT_PACKAGE,'executable':False}
MATERIAL={**VALUE,'setting':False,'creator_kind':'person'}
PROGRAM={**NOT_PACKAGE,'executable':True,'own_process':True}
SETTING={**VALUE,'setting':True}
FILE={'path':'/opt/stand/pkgs/fixture/object','kind':'file','sha256':'a'*64,'mode':420,'uid':0,'gid':0}
# Frozen expected categories, required flags and deciding questions.
CLASS_CASES=[
    ('unknown-q1-blocks-known-code',{'executable':True,'own_process':True},'FACT_UNKNOWN',None,None),
    ('unknown-unchanged-blocks-material',{**MATERIAL,'package_member':True},'FACT_UNKNOWN',None,None),
    ('package-first-over-contained-code',{**CONTAINED,'package_installed':True},'installed object',True,1),
    ('package-first-over-cache',{**VALUE,'package_member':True,'remains_as_received':True,'creator_kind':'program'},'installed object',True,1),
    ('dependency-only-package',{'package_installed':True,'executable':False},'installed object',True,1),
    ('changed-package-member-falls-through',{**MATERIAL,'package_member':True,'remains_as_received':False},'material',False,4),
    ('unknown-executable-blocks-material',{**NOT_PACKAGE,'setting':False,'creator_kind':'person'},'FACT_UNKNOWN',None,None),
    ('actual-own-process',PROGRAM,'program',True,2),
    ('contained-code-all-capabilities',CONTAINED,'contained code',False,2),
    ('can-launch-is-not-contained',{**CONTAINED,'cannot_launch_programs':False},'program',True,2),
    ('can-change-installed-is-not-contained',{**CONTAINED,'cannot_change_installed':False},'program',True,2),
    ('unknown-settings-capability',{**CONTAINED,'cannot_change_settings':None},'FACT_UNKNOWN',None,None),
    ('own-process-over-contained-claim',{**CONTAINED,'own_process':True},'program',True,2),
    ('chosen-system-value',{**VALUE,'chosen_value':True,'computer_obeys':True},'setting',True,3),
    ('personal-launch-setting',{**VALUE,'personal_program_value':True,'launches':True},'setting',True,3),
    ('personal-access-setting',{**VALUE,'personal_program_value':True,'grants_access':True},'setting',True,3),
    ('material-after-earlier-negatives',MATERIAL,'material',False,4),
    ('program-record-after-earlier-negatives',{**MATERIAL,'creator_kind':'program'},'program record',False,4),
    ('unknown-setting-blocks-record',{**VALUE,'creator_kind':'program'},'FACT_UNKNOWN',None,None),
    ('runtime-without-creator',{'runtime_only':True},'runtime',False,'S8.2-5'),
]

def claim(relation='own',**changes):
    return dict(line='fixture',relation=relation,required=dict(FILE),provenance_verified=True,**changes)

# Exact state and valid provenance are separate necessary conditions.
COVER_CASES=[
    ('own-exact-program',PROGRAM,FILE,[claim()],'covered',['fixture']),
    ('derived-exact-program',PROGRAM,FILE,[claim('derived')],'covered',['fixture']),
    ('package-exact-installed',{'package_installed':True},FILE,[claim('package')],'covered',['fixture']),
    ('changed-content-mismatch',PROGRAM,{**FILE,'sha256':'b'*64},[claim()],'mismatch',[]),
    ('changed-mode-mismatch',PROGRAM,{**FILE,'mode':493},[claim()],'mismatch',[]),
    ('unverified-path-does-not-cover',PROGRAM,FILE,[{**claim(),'provenance_verified':False}],'mismatch',[]),
    ('unknown-never-covered',{},FILE,[claim()],'FACT_UNKNOWN',[]),
    ('own-setting',SETTING,FILE,[claim()],'covered',['fixture']),
    ('derived-setting-not-permitted',SETTING,FILE,[claim('derived')],'mismatch',[]),
    ('package-setting-needs-default-proof',SETTING,FILE,[claim('package')],'mismatch',[]),
    ('package-default-setting',SETTING,FILE,[claim('package',package_default=True)],'covered',['fixture']),
    ('material-without-line',MATERIAL,FILE,[],'not-required',[]),
    ('runtime-without-line',{'runtime_only':True},FILE,[],'diagnostic',[]),
    ('runtime-line-does-not-create-duty',{'runtime_only':True},FILE,[claim()],'diagnostic',[]),
    ('missing-program-line',PROGRAM,FILE,[],'unrecorded',[]),
]

def run(emit=True):
    results=[]
    for name,facts,category,required,question in CLASS_CASES:
        actual=object_rules.classify(facts)
        expected={'category':category,'required':required,'question':question}
        passed=all(actual.get(key)==value for key,value in expected.items())
        if category=='FACT_UNKNOWN':passed=passed and bool(actual['missing'])
        results.append(dict(name=name,pass_=passed,expected=expected,observed=actual))
    for name,facts,observed,claims,status,lines in COVER_CASES:
        actual=object_rules.coverage(object_rules.classify(facts),observed,claims)
        expected={'status':status,'lines':lines}
        passed=all(actual.get(key)==value for key,value in expected.items())
        results.append(dict(name=name,pass_=passed,expected=expected,observed=actual))
    summary={'kind':'rules-selftest-summary','cases':len(results),
             'passed':sum(row['pass_'] for row in results),'failed':[row['name'] for row in results if not row['pass_']],
             'scope':'Finite pure rule fixtures; real capability evidence remains separately required'}
    if emit:
        for row in results:print(json.dumps(row,sort_keys=True))
        print(json.dumps(summary,sort_keys=True))
    return results,summary

def main():
    _,summary=run()
    return 1 if summary['failed'] else 0

if __name__=='__main__':raise SystemExit(main())

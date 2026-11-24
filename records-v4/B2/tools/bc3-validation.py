#!/usr/bin/env python3
"""One-shot BC3 full rebuilt-image validation, run by a server user service."""
import concurrent.futures,hashlib,json,os,pathlib,shutil,subprocess,sys,threading,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
phase=sys.argv[1]
if phase not in ('development-1','development-2','final-1','final-2','final-3'):
    raise SystemExit('unused named phase required')
OUT=ROOT/'raw/round-3'/(phase+'-validation')
OUT.mkdir(parents=True,exist_ok=False)
ENV={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','STAND_V4_CHANNELS':'1','LAB_RUN_TIMEOUT':'7200'}
steps=[];owned=[];peer=ROOT/'bc3-peer';record_lock=threading.RLock();lane_results={};lane_context=threading.local()
def utc():return time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
def save(name,value):
    with record_lock:(OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def run(argv,log,script=None,root=ROOT,legacy=False,required=True,lane=None):
    rec={'argv':[str(a).replace(str(ROOT),'[stand-root]') for a in argv],
         'started_utc':utc(),'log':log,'expected_exit':0,'legacy_protocol':legacy,
         'lane':lane or getattr(lane_context,'name','controller')}
    with record_lock:print(json.dumps({'phase':'expected',**rec}),flush=True)
    with (OUT/log).open('wb') as stream:
        result=subprocess.run(argv,cwd=root,input=script.encode() if script else None,
            stdout=stream,stderr=subprocess.STDOUT,
            env={**ENV,'STAND_ROOT':str(root),'STAND_LEGACY':'1' if legacy else '0'})
    with record_lock:
        rec.update(exit=result.returncode,ended_utc=utc());steps.append(rec);save('steps.json',steps)
        print(json.dumps({'phase':'result',**rec}),flush=True)
    if required and result.returncode:raise RuntimeError('stage failed: '+log)
    return result.returncode
def lab(op,name,log,script=None,extra=()):
    return run(['python3','lab.py',op,name,*extra],log,script)
def destroy(name):
    if (ROOT/'vms'/name).exists():
        if run(['python3','lab.py','destroy',name],name+'-destroy.log',required=False):
            lab('kill',name,name+'-kill.log');lab('destroy',name,name+'-destroy-after-kill.log')
def components(suites):
    lane_context.name='components'
    for suite in suites:
        name='bc3-'+phase+'-'+suite
        with record_lock:owned.append(name)
        lab('new',name,suite+'-new.log',extra=['stand'])
        if suite=='cases':
            run(['python3','lab.py','run',name,'--root'],'cases.jsonl',
                'python3 -B /usr/local/lib/stand/bc3-selftest.py\n',required=False)
            lab('copy-out',name,'cases-export.log',extra=['/var/lib/stand/bc3-evidence',str(OUT/'cases-evidence')])
            run(['python3','lab.py','run',name,'--root'],'cases-filesystem-verify.jsonl',
                'python3 -B /usr/local/lib/stand/bc3-state.py verify\n',required=False)
        elif suite=='supplement':
            for part in ('direct','extra'):
                run(['python3','lab.py','run',name,'--root'],'supplement-'+part+'.jsonl',
                    (ROOT/'tools'/('v4-'+part+'-selftest.py')).read_text(),required=False)
        else:
            run(['python3','lab.py','run',name,'--root'],suite+'.jsonl',
                'python3 -B /usr/local/lib/stand/v4-'+suite+'-selftest.py\n',required=False)
        if suite in ('objects','shell','supplement'):
            lab('run',name,suite+'-before-verify.log','stand-verify\n',extra=['--root'])
            lab('stop',name,suite+'-stop.log');lab('start',name,suite+'-start.log')
            if suite in ('objects','shell'):
                run(['python3','lab.py','run',name,'--root'],suite+'-reboot.jsonl',
                    'python3 -B /usr/local/lib/stand/v4-'+suite+'-selftest.py --after\n',required=False)
        run(['python3','lab.py','run',name,'--root'],suite+'-verify.log','stand-verify\n',required=False)
        if suite=='objects':
            lab('copy-out',name,'objects-export.log',extra=['/var/lib/stand/round2-evidence',str(OUT/'objects-evidence')])
            lab('copy-out',name,'factory-export.log',extra=['/etc/stand/factory',str(OUT/'factory-export')])
        destroy(name)
    with record_lock:return int(any(step['exit'] for step in steps if step['lane']=='components'))

status=1
try:
    shutil.copytree(ROOT/'build',OUT/'recipe-inputs')
    shutil.copytree(ROOT/'tools',OUT/'controller-inputs')
    save('input-sha256.json',{str(p.relative_to(ROOT)):sha(p) for folder in ('build','tools')
        for p in sorted((ROOT/folder).iterdir()) if p.is_file()})
    save('validated-build.json',json.loads((ROOT/'raw/round-3'/phase/'image.json').read_text()))
    if sha(ROOT/'base/stand.qcow2')!=json.loads((ROOT/'raw/round-3'/phase/'image.json').read_text())['sha256']:raise RuntimeError('frozen image changed')
    shutil.copyfile(ROOT/'raw/recipe.log',OUT/'recipe.log')
    save('image.json',{'sha256':sha(ROOT/'base/stand.qcow2'),'mode':oct((ROOT/'base/stand.qcow2').stat().st_mode&0o777)})
    if phase.startswith('final'):
        if peer.exists():raise RuntimeError('peer collision')
        peer.mkdir()
        for folder in ('build','downloads','keys'):shutil.copytree(ROOT/folder,peer/folder)
        run(['python3','build/build.py','--server'],'peer-build.log',root=peer)
        ident='bc3-final-'+phase
        regression_ident=ident+'-regressions'
        carried=ROOT/'raw/round-4'/ident
        regressions=ROOT/'raw/round-3'/regression_ident
        if carried.exists() or regressions.exists():raise RuntimeError('carried evidence phase collision')
        # Three independent guest lanes, each sequential and with distinct names.
        # Test drivers and their inputs remain unchanged. No regression case is
        # dropped: the complete BC3 chain runs beside the four-suite BC4 lane.
        save('lane-plan.json',{'utc':utc(),'max_lanes':3,'peer_built_before_lanes':True,
            'components':['cases','objects','shell','gate','tools','supplement'],
            'round4_phase':ident,'round3_phase':regression_ident,
            'round4_destination':'carried-suite','round3_destination':'carried-suite/regressions'})
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            tasks={
                'components':executor.submit(components,('cases','objects','shell','gate','tools','supplement')),
                'round4':executor.submit(run,['python3','build/round4-driver.py',ident],
                    'carried-console.jsonl',legacy=True,required=False,lane='round4'),
                'round3':executor.submit(run,['python3','build/round3-driver.py',regression_ident,
                    '--peer-root','bc3-peer'],'regressions-console.jsonl',legacy=True,required=False,lane='round3'),
            }
            labels={future:label for label,future in tasks.items()}
            for future in concurrent.futures.as_completed(labels):
                label=labels[future]
                try:lane_results[label]={'exit':future.result()}
                except Exception as error:
                    lane_results[label]={'exit':1,'error':str(error).replace(str(ROOT),'[stand-root]')}
                save('whole-suite-ledger.json',{'utc':utc(),'lanes':lane_results})
        # Join all lanes before relocating raw evidence or composing exports.
        # Original child summary files are not rewritten by this controller.
        destination=OUT/'carried-suite'
        if destination.exists():raise RuntimeError('carried destination collision')
        if carried.exists():shutil.move(carried,destination)
        if regressions.exists():
            destination.mkdir(exist_ok=True)
            if (destination/'regressions').exists():raise RuntimeError('regression destination collision')
            shutil.move(regressions,destination/'regressions')
        example_name='bc3-example-'+phase
        run(['python3','build/assemble-channel-examples.py',str(OUT/'carried-suite'),example_name],'assemble.log',legacy=True)
        complete=ROOT/example_name/'combined/machine.jsonl'
        combined_rows=[json.loads(line) for line in complete.read_text().splitlines() if line]
        extras=[]
        exported=OUT/'objects-evidence/round2-evidence'
        for name in ('fixture-rows.json','generated-unit-rows.json'):
            extras.extend(json.loads((exported/name).read_text()))
        if {row['id'] for row in combined_rows}&{row['id'] for row in extras}:
            raise RuntimeError('round 2 example ID collision')
        combined_rows+=extras
        complete.write_text(''.join(json.dumps(row,sort_keys=True,separators=(',',':'))+'\n' for row in combined_rows))
        example=ROOT/example_name
        (example/'provenance.json').rename(example/'carried-provenance.json')
        (example/'provenance.json').write_text(json.dumps({
            'source':'carried exports plus target-interpreter round 2 fixtures',
            'carried_object_source_sha256':{name:sha(exported/name) for name in ('fixture-rows.json','generated-unit-rows.json')},
            'files_sha256':{str(p.relative_to(example)):sha(p) for p in sorted(example.rglob('*')) if p.is_file()}},indent=2,sort_keys=True)+'\n')
        save('complete-example.json',{'rows':len(combined_rows),'added_rows':[row['id'] for row in extras],
             'machine_sha256':sha(complete),'source':'target-interpreter fixture and generated-unit exports'})
        run(['python3','build/combined-selftest.py',ident+'-combined',example_name+'/combined',
             '--peer-root','bc3-peer','--reboot'],'combined-console.jsonl',legacy=True,required=False)
        combined=ROOT/'raw/round-4'/(ident+'-combined')
        if combined.exists():shutil.move(combined,OUT/'combined')
        save('peer-image.json',{'sha256':sha(peer/'base/stand.qcow2')})
    else:
        components(('cases',))
    status=int(any(step['exit'] for step in steps) or any(lane['exit'] for lane in lane_results.values()))
except Exception as error:
    save('failure.json',{'utc':utc(),'error':str(error).replace(str(ROOT),'[stand-root]')})
finally:
    for name in owned:
        try:destroy(name)
        except Exception:status=1
    if peer.exists() and not any((peer/'vms').glob('*')):shutil.rmtree(peer)
    save('summary.json',{'utc':utc(),'controller_exit':status,'steps':steps,
        'lanes':lane_results,'remaining_vms':[p.name for p in (ROOT/'vms').glob('*')],
        'peer_remaining':peer.exists(),'hypothesis_outcome':'?'})
sys.exit(status)

#!/usr/bin/python3 -B
"""Round 2 object coverage integration, disposable guest only. Expected cases fixed in source."""
import base64,copy,hashlib,io,json,os,pathlib,runpy,shlex,shutil,socket,subprocess,sys,tarfile,time
P=pathlib.Path
sys.dont_write_bytecode=True
sys.path.insert(0,'/usr/local/lib/stand')
import stand,inventory,object_rules,recorded_objects
OUT=P('/var/lib/stand/round2-evidence')
LIB=P('/usr/local/lib/stand')
results=[]
def emit(**record):
    record['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    print(json.dumps(record,sort_keys=True),flush=True)
def check(ident,passed,variants,required=True,**evidence):
    row=dict(id=ident,passed=bool(passed),variants=variants,required=required,**evidence)
    results.append(row);emit(phase='result',**row)
def save(name,value):(OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def report():return json.loads((stand.ROOT/'last-success.json').read_text())
def call(ident,command,expected,variants,root=False):
    emit(phase='expected',id=ident,command=command,expected=expected,authority='root' if root else 'ordinary',variants=variants)
    argv=['/usr/bin/bash','-c',command] if root else ['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-shell','-c',command]
    try:
        p=subprocess.run(argv,text=True,capture_output=True,timeout=300)
        value=dict(exit=p.returncode,stdout=p.stdout,stderr=p.stderr)
    except subprocess.TimeoutExpired:value=dict(exit=124,stdout='',stderr='timeout')
    emit(phase='command',id=ident,**value)
    return value
def add(row):
    path=P('/tmp')/(row['id'].replace(':','-')+'.json');path.write_text(json.dumps(row))
    r=call('ADD-'+row['id'],'stand-line add '+str(path),'exact row applied with successful report',['M5.01'])
    check('ADD-'+row['id'],r['exit']==0 and row in stand.load(stand.current_dir()),['M5.01'],command=r)
def remove(ident):
    r=call('REMOVE-'+ident,'stand-line remove '+ident,'own line removed through declaration application',['M5.01'])
    check('REMOVE-'+ident,r['exit']==0 and ident not in {x['id'] for x in stand.load(stand.current_dir())},['M5.01'],command=r)
def scan(name,d=None):
    emit(phase='expected',id='CENSUS-'+name,expected='independent census before declaration; unknowns never covered')
    items,summary=inventory.v4_inventory(d,emit=False)
    with (OUT/(name+'.jsonl')).open('w') as stream:
        for item in items+[summary]:stream.write(json.dumps(item,sort_keys=True)+'\n')
    emit(phase='census',id=name,summary=summary,evidence=name+'.jsonl')
    return {item['object']:item for item in items},summary
def verify(ident):
    values=stand.verify(emit=False);save(ident+'.json',values)
    check(ident,all(r['ok'] for r in values),['M5.01'],rows=len(values),failed=[r['id'] for r in values if not r['ok']])
def main():
    if os.getuid()!=0:raise RuntimeError('disposable guest operator required')
    if '--after' in sys.argv:
        previous=json.loads((OUT/'before-reboot.json').read_text())
        check('OBJECTS-AFTER-REBOOT',report()==previous['report'],['M5.01'],report_unchanged=report()==previous['report'])
        verify('after-reboot-verify')
        return int(any(not r['passed'] for r in results if r['required']))
    OUT.mkdir(exist_ok=False)
    rules=runpy.run_path(str(LIB/'v4-rules-selftest.py'))
    rule_rows,rule_summary=rules['run'](emit=True);save('rule-cases.json',rule_rows)
    check('ORDERED-RULES',all(r['pass_'] for r in rule_rows),['M5.01'],summary=rule_summary)
    initial,initial_summary=scan('initial')
    native=[r for r in initial.values() if r['kind']=='package' and r['object'].startswith('dpkg:')]
    check('NATIVE-PACKAGE-CENSUS',bool(native) and all(r['status']=='covered' for r in native),['M5.01'],count=len(native),uncovered=[r['object'] for r in native if r['status']!='covered'])
    fixtures=runpy.run_path(str(LIB/'v4-object-fixtures.py'));rows=fixtures['rows']()
    original=' '.join(P('/proc/sys/kernel/printk').read_text().split())
    rows[-1]['value']=('3' if original.split()[0]!='3' else '4')+' '+' '.join(original.split()[1:])
    save('fixture-rows.json',rows)
    for row in rows:add(row)
    worker=json.loads(P('/usr/local/share/stand/dev/worker-1.json').read_text())
    add(worker)
    generated=fixtures['generated_unit']('/opt/stand/pkgs/dev-worker/bin/worker')
    for row in generated:add(row)
    save('generated-unit-rows.json',generated)
    current,summary=scan('installed')
    for obj,owner in [('package:stand:v4-objects','v4:objects'),('package:stand:v4-meta','v4:meta'),('package:stand:v4-noncode','v4:noncode'),('package:stand:v4-dependency','v4:meta')]:
        value=current.get(obj,{})
        check('PACKAGE-'+obj,value.get('status')=='covered' and owner in value.get('lines',[]),['M5.01'],observation=value)
    for suffix in ('default.conf','source.py','copy.py','source.pyc'):
        obj='/opt/stand/pkgs/v4-objects/'+suffix;value=current.get(obj,{})
        check('FILE-'+suffix,value.get('status')=='covered' and 'v4:objects' in value.get('lines',[]),['C7.18','C8.08','M5.01'],observation=value)
    val=current.get('sysctl:kernel.printk',{})
    check('CHOSEN-SYSTEM-SETTING',val.get('status')=='covered' and val.get('observed',{}).get('value')==rows[-1]['value'],['C8.08','M5.01'],observation=val)
    verify('installed-verify')
    unitpath='/etc/systemd/system/stand-v4-generated.service'
    value=current.get(unitpath,{})
    check('GENERATED-UNIT',value.get('status')=='covered' and 'v4:generated-unit' in value.get('lines',[]) and stand.observe(generated[-1],stand.current_dir())[0],['C6.5','M5.01'],observation=value,actual_file=stand.filevalue(unitpath))
    before_unit=report()
    r=call('UNDECLARED-GENERATOR',"mkdir -p .config/systemd/user-generators; printf '#!/usr/bin/bash\\nprintf GENERATOR-RAN\\n' > .config/systemd/user-generators/round2; chmod +x .config/systemd/user-generators/round2; systemctl --user daemon-reload",'unrecorded user generator must not become an enabled job or loaded code',['C6.5'])
    check('UNDECLARED-GENERATOR',r['exit']!=0 and report()==before_unit,['C6.5'],command=r,scope='supplied manager path only')
    r=call('BYTECODE-RUN','python3 -B /opt/stand/pkgs/v4-objects/source.pyc','recorded generated bytecode executes',['C7.18'])
    check('BYTECODE-RUN',r['exit']==0 and r['stdout'].strip()=='RECORDED-BYTECODE',['C7.18'],command=r)
    before=report()
    r=call('LOOSE-NONCODE-COPY','cp /opt/stand/pkgs/v4-noncode/lookup.txt loose-lookup.txt','ordinary non-code material remains writable',['M5.01'])
    check('LOOSE-NONCODE-COPY',r['exit']==0 and report()==before,['M5.01'],command=r)
    for ident,command,obj in [
        ('DEFAULT-WRITE',"printf 'language=xx\\n' > /opt/stand/pkgs/v4-objects/default.conf",'/opt/stand/pkgs/v4-objects/default.conf'),
        ('SYSTEM-VALUE-WRITE',"printf '1 4 1 7\\n' > /proc/sys/kernel/printk",'sysctl:kernel.printk')]:
        r=call(ident,command,'ordinary direct mutation denied, exact readback/report unchanged',['C8.08','M5.01'])
        same=recorded_objects.read_setting(rows[-1])['value']==rows[-1]['value'] if obj.startswith('sysctl:') else stand.filevalue(obj)==stand.desired_file(rows[0]['files'][3])
        check(ident,r['exit']!=0 and same and report()==before,['C8.08','M5.01'],command=r,readback_unchanged=same)
    # Negative declaration input: valid inline payload checksum, false source derivation.
    bad=copy.deepcopy(rows[0]);bad['files'][1]=fixtures['file'](bad['files'][1]['path'],b'not the source\n')
    badpath=P('/tmp/v4-bad-derivation.json');badpath.write_text(json.dumps(bad))
    r=call('FALSE-DERIVATION','stand-pkg install '+str(badpath),'false source/output edge refused without report change',['C7.18','M5.01'])
    check('FALSE-DERIVATION',r['exit']!=0 and report()==before,['C7.18','M5.01'],command=r)
    # Root direct mutation is breaking: test reader sensitivity, not a P4 claim.
    target=P('/opt/stand/pkgs/v4-noncode/lookup.txt');original_bytes=target.read_bytes();original_mode=target.stat().st_mode&0o777
    emit(phase='expected',id='BREAKING-READBACK',expected='direct root byte/mode alteration detected; restore exact bytes',classification='breaking')
    target.write_bytes(b'alpha=99\n');target.chmod(0o600)
    badstate=stand.observe(rows[2],stand.current_dir())
    check('BREAKING-READBACK',not badstate[0],['M5.01'],classification='breaking',observation=badstate[1])
    target.write_bytes(original_bytes);target.chmod(original_mode)
    # Matching an unapplied candidate lacking owners must expose actual residuals.
    candidate=OUT/'without-owners';shutil.copytree(stand.current_dir(),candidate)
    base=[r for r in stand.load(stand.current_dir()) if r['id'] not in {r['id'] for r in rows}]
    (candidate/'machine.jsonl').write_text(''.join(stand.canonical(r)+'\n' for r in base))
    residual,_=scan('unapplied-without-owners',candidate)
    for obj in ('package:stand:v4-meta','package:stand:v4-dependency','/opt/stand/pkgs/v4-noncode/lookup.txt'):
        value=residual.get(obj,{})
        check('MISSING-OWNER-'+obj,value.get('status')=='unrecorded' and not value.get('lines'),['M5.01'],observation=value,candidate_applied=False)
    # Ordinary material/personal values. No blanket exemption for arbitrary files.
    before=report()
    r=call('PERSONAL-VALUES',"printf 'tabstop 4\\n' > values.conf; printf '<html><body>Ordinary document</body></html>\\n' > values.html; w3m -dump -config values.conf values.html",'ordinary values-only browser work, unchanged declaration',['C8.08'])
    check('PERSONAL-VALUES',r['exit']==0 and 'Ordinary document' in r['stdout'] and report()==before,['C8.08'],command=r)
    # Actual unrecorded bytecode from saved source remains a boundary observation.
    r=call('UNRECORDED-BYTECODE',"printf 'print(\"UNCOVERED-BYTECODE\")\\n' > loose.py; python3 -B -c 'import py_compile; py_compile.compile(\"loose.py\",cfile=\"loose.pyc\",doraise=True)'; python3 -B loose.pyc",'required boundary: unrecorded executable bytecode does not execute',['C7.18'])
    check('UNRECORDED-BYTECODE','UNCOVERED-BYTECODE' not in r['stdout'].splitlines(),['C7.18'],required=False,command=r,report_unchanged=report()==before)
    # Archive extraction is ordinary work; inspect the saved executable effect.
    payload=b'print("EXTRACTED-CODE")\n';archive=P('/tmp/v4-extracted.tar')
    with tarfile.open(archive,'w') as tar:
        entry=tarfile.TarInfo('program.py');entry.size=len(payload);entry.mode=0o644;tar.addfile(entry,io.BytesIO(payload))
    r=call('EXTRACTED-CODE',"mkdir -p extracted; tar -xf /tmp/v4-extracted.tar -C extracted; python3 -B extracted/program.py",'required boundary: extracted saved code cannot execute uncovered',['C1.3'])
    check('EXTRACTED-CODE','EXTRACTED-CODE' not in r['stdout'].splitlines(),['C1.3'],required=False,command=r,report_unchanged=report()==before,actual_file=stand.filevalue('/home/stand/extracted/program.py'))
    # Actual built-in native package installation in alternate root/database.
    pkg=P('/tmp/v4-alt-package');(pkg/'DEBIAN').mkdir(parents=True);(pkg/'usr/share/v4-alt').mkdir(parents=True)
    (pkg/'DEBIAN/control').write_text('Package: v4-alt\nVersion: 1\nArchitecture: all\nMaintainer: Builder <<REDACTED>>\nDescription: round 2 non-code package\n')
    (pkg/'usr/share/v4-alt/data.txt').write_text('installed non-code\n')
    setup=subprocess.run(['/usr/bin/dpkg-deb','--build',str(pkg),'/tmp/v4-alt.deb'],capture_output=True,text=True)
    check('ALT-FIXTURE',setup.returncode==0,['C1.3'],output=setup.stdout,stderr=setup.stderr)
    r=call('ALTERNATE-DATABASE','/usr/bin/dpkg --root=/tmp/v4-alt-root --admindir=/tmp/v4-alt-db --install /tmp/v4-alt.deb','required boundary: built-in root installer records exact installed package',['C1.3'],root=True)
    q=subprocess.run(['/usr/bin/dpkg-query','--admindir=/tmp/v4-alt-db','-W','-f=${Status} ${Version}','v4-alt'],capture_output=True,text=True)
    extra=stand.filevalue('/tmp/v4-alt-root/usr/share/v4-alt/data.txt')
    bypass=r['exit']==0 and q.stdout=='install ok installed 1' and not extra.get('missing') and report()==before
    check('ALTERNATE-DATABASE',not bypass,['C1.3'],required=False,command=r,package_readback=q.stdout,file_readback=extra,classification='built-in-tool path',report_unchanged=report()==before)
    # No supplied executable web renderer or WASI runtime is silently counted as denial.
    availability={name:shutil.which(name) for name in ('chromium','chromium-browser','firefox','wasmtime','wasmer')}
    emit(phase='observation',id='INTERNAL-CODE-CAPABILITIES',variants=['C7.19','C7.21'],status='UNTESTED',availability=availability,reason='No executable browser/WASI capability fixture established; passive document rendering is not internal-code confinement')
    # Runtime listener follows its creator; lack of exact creation provenance stays unknown.
    listener=socket.socket();listener.bind(('127.0.0.1',0));listener.listen(1)
    endpoint='tcp:127.0.0.1:'+str(listener.getsockname()[1])
    observed,_=scan('with-attempts')
    value=observed.get(endpoint,{})
    check('RUNTIME-NO-SEPARATE-LINE',value.get('status')=='diagnostic' and value.get('classification',{}).get('required') is False,['C7.25'],observation=value)
    listener.close()
    check('UNKNOWN-DOES-NOT-COVER',all(not r['lines'] for r in observed.values() if r['status']=='FACT_UNKNOWN'),['M5.01'],unknown_count=sum(r['status']=='FACT_UNKNOWN' for r in observed.values()))
    # Unsupported arbitrary algorithm remains a named finite-format limitation.
    path=P('/tmp/v4-algorithm.json');path.write_text(json.dumps({'id':'v4:algorithm','type':'algorithm','program':'arbitrary desired-state semantics'}))
    r=call('UNSUPPORTED-ALGORITHM','stand-line add '+str(path),'unsupported algorithm rejected explicitly; M5.02 remains open',['M5.02'])
    check('UNSUPPORTED-ALGORITHM',r['exit']!=0 and 'unsupported line type algorithm' in r['stderr'],['M5.02'],command=r,scope='finite format only')
    # Restore chosen value explicitly; complete removal/recovery is owned by round 3.
    restored=copy.deepcopy(rows[-1]);restored['value']=original;add(restored)
    for row in reversed(generated):remove(row['id'])
    remove(worker['id'])
    for row in reversed(rows):remove(row['id'])
    after,_=scan('removed')
    for obj in ('package:stand:v4-meta','package:stand:v4-dependency','/opt/stand/pkgs/v4-noncode/lookup.txt','/opt/stand/pkgs/v4-objects/source.pyc'):
        check('REMOVAL-'+obj,obj not in after,['M5.01'],observation=after.get(obj))
    save('residual-setting.json',after.get('sysctl:kernel.printk'))
    loose=after.get('/home/stand/loose-lookup.txt',{})
    check('LOOSE-COPY-NO-PACKAGE-MEMBERSHIP',loose.get('facts',{}).get('package_member') is False and not loose.get('lines') and P('/home/stand/loose-lookup.txt').read_bytes()==original_bytes,['M5.01'],observation=loose,interpretation='Observed copy is material by known fixture provenance; autonomous reader remains conservative')
    verify('final-verify')
    save('before-reboot.json',{'report':report(),'original_printk':original})
    save('results.json',results)
    emit(phase='summary',assertions=len(results),implementation_failures=[r['id'] for r in results if not r['passed'] and r['required']],boundary_failures=[r['id'] for r in results if not r['passed'] and not r['required']],hypothesis_outcome='?')
    return int(any(not r['passed'] for r in results if r['required']))
if __name__=='__main__':sys.exit(main())

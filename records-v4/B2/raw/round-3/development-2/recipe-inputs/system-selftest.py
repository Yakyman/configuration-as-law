#!/usr/bin/python3
"""Fresh image repository and actual base update integration tests."""
import json,pathlib,shutil,subprocess,sys,tempfile,time
P=pathlib.Path
out=P(sys.argv[1] if len(sys.argv)>1 else '/var/lib/stand/system-selftest.jsonl');log=out.open('w',buffering=1);failed=[]
def record(o):
    o['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());s=json.dumps(o,sort_keys=True);log.write(s+'\n');print(s,flush=True)
def run(ident,args,positive=False,contains=None):
    record(dict(phase='expected',id=ident,command=args,expected='success' if positive else 'refusal',source='B2/raw/round-4/system-notes.md'))
    try:
        p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
        ok=(p.returncode==0 if positive else p.returncode!=0) and (contains is None or contains in p.stdout)
        record(dict(phase='result',id=ident,rc=p.returncode,output=p.stdout,passed=ok))
    except subprocess.TimeoutExpired:
        ok=False;record(dict(phase='result',id=ident,passed=False,error='timeout'))
    if not ok:failed.append(ident)
def session(ident,fields,**kw):run(ident,['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-session','-c','\t'.join(fields)],**kw)
with tempfile.TemporaryDirectory(prefix='system-before-',dir='/var/lib/stand') as baseline:
    shutil.copytree(P('/var/lib/stand/current').resolve(),baseline,dirs_exist_ok=True)
    session('SYSTEM-REPOSITORY-INSTALL',['broker','apt-get','install','hello=2.10-5'],positive=True)
    session('SYSTEM-REPOSITORY-RUN',['run','/opt/stand/pkgs/repository-hello/usr/bin/hello'],positive=True,contains='Hello, world!')
    run('SYSTEM-REPOSITORY-SUDO',['/usr/bin/sudo','-n','/usr/local/bin/apt','install','hello=2.10-5'],positive=True)
    run('SYSTEM-BASE-OLD',['/usr/bin/dpkg-query','-W','-f=${Version}','ed'],positive=True,contains='1.19-1')
    session('SYSTEM-BASE-UPDATE',['broker','apt-get','upgrade','--stand-catalog','ed'],positive=True)
    run('SYSTEM-BASE-NEW',['/usr/bin/dpkg-query','-W','-f=${Version}','ed'],positive=True,contains='1.21.1-1')
    session('SYSTEM-BASE-NEW-EXEC',['run','/usr/bin/ed'],positive=True,contains='GNU ed 1.21.1')
    run('SYSTEM-BASE-SUDO',['/usr/bin/sudo','-n','/usr/local/bin/apt-get','upgrade','--stand-catalog','ed'],positive=True)
    run('SYSTEM-NEW-VERIFY',['/usr/local/bin/stand-verify'],positive=True)
    examples=P('/var/lib/stand/channel-examples');examples.mkdir(exist_ok=True)
    rows=[json.loads(line) for line in (P('/var/lib/stand/current')/'machine.jsonl').read_text().splitlines() if line.strip()]
    for channel in ('repository','system-update'):
        exported=[r for r in rows if r.get('channel')==channel]
        if len(exported)!=1:raise RuntimeError('successful system example row missing')
        (examples/(channel+'.jsonl')).write_text(json.dumps(exported[0],sort_keys=True)+'\n')
    target=P('/var/lib/stand/channel-system-state')
    if target.exists():shutil.rmtree(target)
    shutil.copytree(P('/var/lib/stand/current').resolve(),target)
    for i,args in enumerate([['install','hello'],['install','hello=0'],['-o','DPkg::Pre-Invoke::=/tmp/hook','install','hello'],['install','--root=/tmp/root','hello'],['upgrade','--stand-catalog','unknown'],['upgrade'],['install','/tmp/unrecorded.deb']]):
        session('SYSTEM-BYPASS-'+str(i),['broker','apt-get',*args])
        run('SYSTEM-SUDO-BYPASS-'+str(i),['/usr/bin/sudo','-n','/usr/local/bin/apt-get',*args])
    c=json.loads(P('/usr/local/share/stand/system/catalog.json').read_text());row=c['updates']['ed']['row'];row['base_packages']['ed']='9.9'
    bad=P('/var/lib/stand/system-tampered.json');bad.write_text(json.dumps(row));bad.chmod(0o644)
    session('SYSTEM-CATALOG-TAMPER',['broker','stand-line','add',str(bad)])
    bad.unlink()
    session('SYSTEM-UPDATE-REMOVE',['broker','apt-get','remove','system:base-state'],positive=True)
    run('SYSTEM-REMOVED-VERSION',['/usr/bin/dpkg-query','-W','-f=${Version}','ed'],positive=True,contains='1.19-1')
    session('SYSTEM-UPDATE-REAPPLY',['broker','apt-get','upgrade','--stand-catalog','ed'],positive=True)
    run('SYSTEM-RESTORE-DECLARATION',['/usr/local/bin/stand-apply',baseline],positive=True)
    run('SYSTEM-BASE-RESTORED',['/usr/bin/dpkg-query','-W','-f=${Version}','ed'],positive=True,contains='1.19-1')
    session('SYSTEM-REMOVED-HELLO',['run','/opt/stand/pkgs/repository-hello/usr/bin/hello'])
    session('SYSTEM-REMOVED-ED-LAUNCH',['run','/usr/bin/ed'])
    run('SYSTEM-RESTORE-VERIFY',['/usr/local/bin/stand-verify'],positive=True)
record(dict(summary=True,failed=failed));sys.exit(bool(failed))

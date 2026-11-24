#!/usr/bin/python3 -I
"""Fresh-guest typed tool tests. Run as root; optional JSONL output path.

Every expected command and generated fixture is logged before its invocation.
This suite modifies only disposable guest state and removes its added rows.
"""
import hashlib,json,os,pathlib,pwd,grp,shlex,shutil,subprocess,sys,tempfile,time
sys.dont_write_bytecode=True
sys.path.insert(0,'/usr/local/lib/stand')
import stand
import codeboundary
stand.POLICY=codeboundary
P=pathlib.Path
failures=[]
output=P(sys.argv[1] if len(sys.argv)>1 else '/var/lib/stand/v4-tools-selftest.jsonl')
log=output.open('w',buffering=1)

def record(**value):
    value['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    text=json.dumps(value,sort_keys=True)
    log.write(text+'\n');print(text,flush=True)

def result(ident,ok,**details):
    record(phase='result',id=ident,passed=bool(ok),**details)
    if not ok:failures.append(ident)

def rows():return {r['id']:r for r in stand.load(stand.current_dir())}

def identity():
    report=stand.ROOT/'last-success.json'
    return {'current':stand.current_dir().name,'report':json.loads(report.read_text()) if report.exists() else None}

def invoke(mode,argv,data=None):
    argv=list(map(str,argv))
    if mode=='ordinary':argv=['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-shell','-c',shlex.join(argv)]
    return subprocess.run(argv,input=data,capture_output=True,timeout=600)

def absence(row):
    kind=row['type']
    if kind in ('program','code'):
        return all(not P(f['path']).exists() for f in row.get('files',[]))
    if kind=='account':
        try:pwd.getpwnam(row['name']);return False
        except KeyError:return True
    if kind=='group':
        try:grp.getgrnam(row['name']);return False
        except KeyError:return True
    if kind in ('service','timer','socket'):
        return not P('/etc/systemd/system',row['unit']).exists() and stand.run('systemctl','is-active',row['unit'],check=False).stdout.strip() not in ('active','activating')
    if kind=='wifi':return not stand.profile_path(row).exists() and stand.run('nmcli','connection','show',row['uuid'],check=False).returncode!=0
    if kind=='bluetooth':return not stand.bt_path(row).exists()
    if kind=='rule':return row['id'] not in stand.run('nft','list','table','inet','stand',check=False).stdout
    return False

def mutation(ident,mode,tool,args,want=None,remove=None,positive=True):
    before=rows();previous=identity()
    command=['/usr/local/bin/'+tool,*map(str,args)]
    record(phase='expected',id=ident,mode=mode,command=command,
           expected='applied exact rows and complete readback' if positive else 'refusal with unchanged declaration',
           exact_required_row=want,removed_id=remove,before_identity=previous)
    try:
        completed=invoke(mode,command)
        after=rows();current=identity()
        added={k:v for k,v in after.items() if before.get(k)!=v}
        deleted={k:v for k,v in before.items() if k not in after}
        checks=stand.verify(emit=False)
        bad=[c for c in checks if not c['ok']]
        ok=(completed.returncode==0 if positive else completed.returncode!=0)
        if positive:
            report=current['report']
            ok=ok and not bad and bool(report) and report.get('declaration')==current['current']
            if want is not None:ok=ok and after.get(want['id'])==want
            if remove is not None:ok=ok and remove not in after and remove in before and absence(before[remove])
        else:ok=ok and before==after and current==previous
        result(ident,ok,rc=completed.returncode,stdout=completed.stdout.decode(errors='replace')[-3000:],
               stderr=completed.stderr.decode(errors='replace')[-2000:],declaration_added_or_changed=added,
               declaration_removed=deleted,after_identity=current,readback_count=len(checks),readback_failures=bad,
               readback=[{'id':c['id'],'ok':c['ok'],'observed_sha256':hashlib.sha256(stand.canonical(c['observed']).encode()).hexdigest()} for c in checks],
               required_observation=stand.observe(want,stand.current_dir()) if want is not None and want['id'] in after else None)
        return bool(ok)
    except Exception as error:
        result(ident,False,error=str(error));return False

def fixture(directory,name,row):
    path=directory/(name+'.json');path.write_text(json.dumps(row)+'\n');path.chmod(0o644)
    record(phase='fixture',name=name,path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),exact_input=row)
    return path

def command_test(ident,mode,argv,data=None,expected=None):
    record(phase='expected',id=ident,mode=mode,command=argv,stdin_sha256=hashlib.sha256(data).hexdigest() if data is not None else None,expected='successful command with exact document bytes' if expected is not None else 'successful command')
    try:
        p=invoke(mode,argv,data)
        result(ident,p.returncode==0 and (expected is None or p.stdout==expected),rc=p.returncode,stdout=p.stdout.decode(errors='replace')[-1000:],stderr=p.stderr.decode(errors='replace')[-1000:])
    except Exception as error:result(ident,False,error=str(error))

def main():
    if os.geteuid()!=0:raise RuntimeError('root controller required')
    dev=P('/usr/local/share/stand/dev')
    initial=rows()
    with tempfile.TemporaryDirectory(prefix='v4-tools-',dir='/tmp') as temp:
        directory=P(temp);directory.chmod(0o755)
        # All material fixtures are caller-readable before testing starts.
        worker=json.loads((dev/'worker-1.json').read_text())
        service=json.loads((dev/'service.json').read_text())
        account=json.loads((dev/'account.json').read_text())
        rule=json.loads((dev/'rule.json').read_text())
        wifi=json.loads((dev/'wifi.json').read_text())
        bluetooth=json.loads((dev/'bluetooth.json').read_text())
        group={'id':'v4:group','type':'group','managed':True,'name':'v4group','gid':1901,'members':[]}
        timertext='[Unit]\nDescription=Recorded test timer\n[Timer]\nOnBootSec=1h\nOnUnitActiveSec=1h\nUnit='+service['unit']+'\nPersistent=false\n[Install]\nWantedBy=timers.target\n'
        timer={'id':'v4:timer','type':'timer','managed':True,'unit':'stand-v4.timer','enabled':'enabled','active':True,'unit_text':timertext,'unit_sha256':hashlib.sha256(timertext.encode()).hexdigest()}
        sockettext='[Unit]\nDescription=Recorded test socket\n[Socket]\nListenStream=/run/stand-sockets/v4.sock\nService='+service['unit']+'\nAccept=no\nRemoveOnStop=yes\nSocketMode=0600\n[Install]\nWantedBy=sockets.target\n'
        socket={'id':'v4:socket','type':'socket','managed':True,'unit':'stand-v4.socket','enabled':'enabled','active':True,'unit_text':sockettext,'unit_sha256':hashlib.sha256(sockettext.encode()).hexdigest()}
        objects={'worker':worker,'service':service,'account':account,'rule':rule,'wifi':wifi,'bluetooth':bluetooth,'group':group,'timer':timer,'socket':socket}
        files={name:fixture(directory,name,row) for name,row in objects.items()}
        changed=dict(account,gecos='Changed declared account')
        files['account-change']=fixture(directory,'account-change',changed)
        high=json.loads((dev/'worker-3.json').read_text())
        files['worker-high']=fixture(directory,'worker-high',high)
        bad=json.loads(json.dumps(worker));bad['files'][0]['sha256']='0'*64
        files['worker-bad']=fixture(directory,'worker-bad',bad)
        badgroup=dict(group,members=['stand']);files['bad-group']=fixture(directory,'bad-group',badgroup)
        for mode in ('ordinary','root'):
            prefix=mode+'-'
            mutation(prefix+'worker',mode,'stand-pkg',['install',files['worker']],want=worker)
            if mode=='ordinary':
                target=P(worker['files'][0]['path'])
                required=worker['files'][0]['sha256'];before=identity()
                record(phase='expected',id='recorded-native-overwrite',variants=['C5.4'],
                       command=['cp','/usr/bin/true',str(target)],expected='ordinary copy cannot replace recorded native bytes; required hash and successful declaration stay exact')
                p=invoke('ordinary',['/usr/bin/cp','/usr/bin/true',str(target)])
                actual=hashlib.sha256(target.read_bytes()).hexdigest()
                file_state=stand.filevalue(target);wanted=stand.desired_file(worker['files'][0])
                covered=rows().get(worker['id'])==worker
                result('recorded-native-overwrite',p.returncode!=0 and actual==required and file_state==wanted and covered and identity()==before,
                       variants=['C5.4'],rc=p.returncode,stderr=p.stderr.decode(),required_sha256=required,
                       actual_sha256=actual,required_file=wanted,actual_file=file_state,covering_line=worker,
                       coverage_unchanged=covered,report_unchanged=identity()==before)
            mutation(prefix+'service',mode,'systemctl',['add',files['service']],want=service)
            # Every job adapter gets a positive actual activation and removal.
            for tool in ('systemd-run','crontab','at'):
                mutation(prefix+tool+'-add',mode,tool,['add',files['timer']],want=timer)
                mutation(prefix+tool+'-remove',mode,tool,['remove',timer['id']],remove=timer['id'])
            mutation(prefix+'socket-add',mode,'systemctl',['add',files['socket']],want=socket)
            mutation(prefix+'socket-remove',mode,'systemctl',['remove',socket['id']],remove=socket['id'])
            mutation(prefix+'useradd',mode,'useradd',['add',files['account']],want=account)
            mutation(prefix+'usermod',mode,'usermod',['add',files['account-change']],want=changed)
            mutation(prefix+'userdel',mode,'userdel',['remove',account['id']],remove=account['id'])
            mutation(prefix+'groupadd',mode,'groupadd',['add',files['group']],want=group)
            mutation(prefix+'groupdel',mode,'groupdel',['remove',group['id']],remove=group['id'])
            for tool,key in (('nft','rule'),('nmcli','wifi'),('bluetoothctl','bluetooth')):
                row=objects[key]
                mutation(prefix+tool+'-add',mode,tool,['add',files[key]],want=row)
                mutation(prefix+tool+'-remove',mode,tool,['remove',row['id']],remove=row['id'])
            mutation(prefix+'wrong-kind',mode,'nft',['add',files['account']],positive=False)
            mutation(prefix+'group-members',mode,'groupadd',['add',files['bad-group']],positive=False)
            mutation(prefix+'service-remove',mode,'systemctl',['remove',service['id']],remove=service['id'])
            mutation(prefix+'worker-remove',mode,'stand-pkg',['remove',worker['id']],remove=worker['id'])
            for tool in ('apt','apt-get'):
                mutation(prefix+tool+'-install',mode,tool,['install',files['worker-high']],want=high)
                mutation(prefix+tool+'-reinstall',mode,tool,['reinstall',files['worker-high']],want=high)
                mutation(prefix+tool+'-downgrade',mode,tool,['downgrade',files['worker']],want=worker)
                mutation(prefix+tool+'-remove',mode,tool,['remove',worker['id']],remove=worker['id'])
            document=directory/(mode+'-document.txt')
            document.write_bytes(b'');document.chmod(0o600)
            if mode=='ordinary':os.chown(document,1000,1000)
            editor='/usr/local/bin/v4-editor'
            command_test(prefix+'editor-write',mode,[editor,'write',str(document)],b'First line\n')
            command_test(prefix+'editor-append',mode,[editor,'append',str(document)],b'Second line\n')
            command_test(prefix+'editor-read',mode,[editor,'read',str(document)],expected=b'First line\nSecond line\n')
            mutation(prefix+'editor-install',mode,'v4-editor',['package-install',files['worker']],want=worker)
            command_test(prefix+'editor-installed-run',mode,[worker['files'][0]['path']])
            mutation(prefix+'editor-remove',mode,'v4-editor',['package-remove',worker['id']],remove=worker['id'])
            mutation(prefix+'editor-hash-refusal',mode,'v4-editor',['package-install',files['worker-bad']],positive=False)
        # Direct root document editing around built-in tools is breaking, not a
        # denial test. Restore the harmless marker immediately.
        marker=P('/etc/stand/v4-breaking-document-test')
        record(phase='expected',id='root-editor-breaking',expected='root general editor writes outside declaration; classified breaking; remove marker immediately')
        try:
            p=invoke('root',['/usr/local/bin/v4-editor','write',str(marker)],b'breaking marker\n')
            result('root-editor-breaking',p.returncode==0 and marker.read_bytes()==b'breaking marker\n',classification='breaking',rc=p.returncode)
        finally:marker.unlink(missing_ok=True)
    # The native account tool is still a built-in tool when run as root.
    # Its bypass is a failed boundary observation, not privileged breaking.
    before_rows=rows();before_identity=identity()
    raw_name='v4raw'
    record(phase='expected',id='root-native-account-bypass',variants=['C10.1'],
           command=['/usr/sbin/useradd','-M','-u','1998','-s','/usr/sbin/nologin',raw_name],
           expected_property='no account created by a built-in tool without a covering declaration',
           implementation_prediction='native root account tool bypasses the declaration broker',
           classification='built-in tool bypass',before_identity=before_identity)
    created=False
    try:
        try:pwd.getpwnam(raw_name)
        except KeyError:pass
        else:raise RuntimeError('raw bypass fixture account already exists')
        try:grp.getgrnam(raw_name)
        except KeyError:pass
        else:raise RuntimeError('raw bypass fixture group already exists')
        try:pwd.getpwuid(1998)
        except KeyError:pass
        else:raise RuntimeError('raw bypass fixture uid already exists')
        p=invoke('root',['/usr/sbin/useradd','-M','-u','1998','-s','/usr/sbin/nologin',raw_name])
        try:
            actual=stand.account_value(raw_name);created=not actual.get('missing',False)
        except KeyError:actual={'missing':True}
        after_rows=rows();after_identity=identity()
        covered=any(r['type']=='account' and r.get('name')==raw_name for r in after_rows.values())
        bypass=created and not covered
        record(phase='boundary_result',id='root-native-account-bypass',variants=['C10.1'],
               passed=not bypass,classification='built-in tool bypass',rc=p.returncode,
               account=actual,covered_by_declaration=covered,
               declaration_unchanged=before_rows==after_rows,
               last_success_unchanged=before_identity==after_identity,
               stdout=p.stdout.decode(errors='replace'),stderr=p.stderr.decode(errors='replace'),
               included_in_implemented_check_exit=False)
    except Exception as error:
        record(phase='boundary_result',id='root-native-account-bypass',passed=False,
               classification='built-in tool bypass',error=str(error),
               included_in_implemented_check_exit=False)
    finally:
        if created:
            cleanup=invoke('root',['/usr/sbin/userdel',raw_name])
            try:grp.getgrnam(raw_name)
            except KeyError:group_cleanup=None
            else:group_cleanup=invoke('root',['/usr/sbin/groupdel',raw_name]).returncode
            try:pwd.getpwnam(raw_name);absent=False
            except KeyError:absent=True
            result('root-native-account-cleanup',cleanup.returncode==0 and absent and group_cleanup in (None,0),
                   rc=cleanup.returncode,account_absent=absent,group_cleanup_rc=group_cleanup)
    remaining=rows()
    result('final-declaration-restored',remaining==initial,extra_ids=sorted(set(remaining)-set(initial)),missing_ids=sorted(set(initial)-set(remaining)))
    checks=stand.verify(emit=False)
    result('final-readback',all(c['ok'] for c in checks),count=len(checks),failures=[c for c in checks if not c['ok']])
    record(phase='summary',passed=not failures,failures=failures,radio_hardware_tested=False)
    return int(bool(failures))

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as error:
        record(phase='summary',passed=False,failures=failures,error=str(error));sys.exit(1)

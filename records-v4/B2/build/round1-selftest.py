#!/usr/bin/python3 -B
"""Bounded BC1 regression suite; external fixture operator, disposable guest only."""
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import tarfile
import time

DEV = Path('/usr/local/share/stand/dev')
ROOT = Path('/var/lib/stand')
RESULTS = []
DENIAL = ('permission denied', 'access denied', 'accessdenied', 'not authorized',
          'not permitted', 'not allowed', 'a password is required', 'authentication is required',
          'refused', 'operation not permitted', 'authorization failed', 'must be superuser',
          'only root can')


def record(ident, variant, mode, argv, expected, predicate, input=None):
    prefix = ['/usr/sbin/runuser', '-u', 'stand', '--']
    if mode == 'sudo':
        prefix += ['/usr/bin/sudo', '-n']
    command = prefix + list(map(str, argv)) if mode != 'operator' else list(map(str, argv))
    started = time.monotonic()
    try:
        p = subprocess.run(command, input=input, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=150)
        code, output = p.returncode, p.stdout
    except subprocess.TimeoutExpired as e:
        code, output = 124, 'TEST TIMEOUT ' + str(e)
    except OSError as e:
        code, output = 127, str(e)
    ok = bool(predicate(code, output))
    if ident.startswith('application-lock-'):
        ok = ok and time.monotonic()-started < 5
    row = dict(id=ident, variant=variant, mode=mode, command=command,
               expected=expected, exit=code, output=output, ok=ok,
               elapsed_seconds=round(time.monotonic()-started, 4))
    RESULTS.append(row)
    print(json.dumps(row, sort_keys=True), flush=True)
    return ok


def denied(code, output):
    return code != 0 and any(s in output.lower() for s in DENIAL)


def absent_or_denied(path):
    return lambda code, output: denied(code, output) or (not Path(path).exists() and code != 0)


def both(ident, variant, args, predicate=denied, expected='authority refusal', input=None):
    for mode in ('ordinary', 'sudo'):
        record(ident, variant, mode, args, expected, predicate, input)


def positive(ident, args, needle=None, input=None):
    return record(ident, 'ordinary-work', 'ordinary', args, 'success' + (': '+needle if needle else ''),
                  lambda c, o: c == 0 and (needle is None or needle in o), input)


def main():
    if os.geteuid() != 0:
        raise SystemExit('External fixture operator root required')
    print(json.dumps({'event':'start', 'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}), flush=True)
    with tempfile.TemporaryDirectory(prefix='round1-', dir='/tmp') as temp:
        td = Path(temp)
        td.chmod(0o755)
        hook = td/'hook.sh'
        hook.write_text('#!/bin/sh\ntouch /tmp/round1-undeclared-hook\n')
        hook.chmod(0o755)
        config = td/'apt.conf'
        config.write_text('DPkg::Pre-Invoke { "'+str(hook)+'"; };\n')
        # A real local package makes extraction and maintainer-script probes substantive.
        def archive(members):
            out=io.BytesIO()
            with tarfile.open(fileobj=out,mode='w:gz') as tar:
                for name,data,mode in members:
                    info=tarfile.TarInfo(name);info.size=len(data);info.mode=mode
                    tar.addfile(info,io.BytesIO(data))
            return out.getvalue()
        control=archive([('control',b'Package: round1-fixture\nVersion: 1\nArchitecture: all\nMaintainer: Fixture <<REDACTED>>\nDescription: Local regression fixture\n',0o644),
                         ('postinst',b'#!/bin/sh\ntouch /tmp/round1-undeclared-hook\n',0o755)])
        data=archive([('usr/bin/round1-fixture',b'#!/bin/sh\necho undeclared-fixture\n',0o755)])
        package=td/'fixture.deb'
        body=b'!<arch>\n'
        for name,part in [('debian-binary',b'2.0\n'),('control.tar.gz',control),('data.tar.gz',data)]:
            body+=(f'{name+"/":<16}{0:<12}{0:<6}{0:<6}{"100644":<8}{len(part):<10}`\n').encode()+part
            if len(part)%2:body+=b'\n'
        package.write_bytes(body)
        calls = [
            ('root-shell','C10.2',['/bin/sh','-c','id -u']),
            ('apt-direct','C1.1',['/usr/bin/apt-get','install','ed']),
            ('apt-alternate-root','C1.3',['/usr/bin/apt-get','-o','Dir='+str(td/'aptroot'),'install','ed']),
            ('dpkg-direct','C1.2',['/usr/bin/dpkg','--configure','-a']),
            ('dpkg-package-hook','C1.4',['/usr/bin/dpkg','--install',str(package)]),
            ('dpkg-extract','C1.3',['/usr/bin/dpkg-deb','--extract',str(package),str(td/'extracted')]),
            ('dpkg-alternate-db','C1.3',['/usr/bin/dpkg','--admindir='+str(td/'db'),'--configure','-a']),
            ('dpkg-alternate-root','C1.3',['/usr/bin/dpkg','--root='+str(td/'root'),'--configure','-a']),
            ('apt-hook','C1.4',['/usr/bin/apt-get','-c',str(config),'install','ed']),
            ('apt-hook-override','C1.5',['/usr/bin/apt-get','-o','DPkg::Pre-Invoke::='+str(hook),'install','ed']),
            ('account-add','C10.1',['/usr/sbin/useradd','round1-undeclared']),
            ('account-alternate-root','C10.1',['/usr/sbin/useradd','--root',str(td),'round1-undeclared']),
            ('service-enable','C6.2',['/usr/bin/systemctl','enable','ssh.service']),
            ('service-property','C6.2',['/usr/bin/systemctl','set-property','ssh.service','CPUWeight=77']),
            ('transient','C6.3',['/usr/bin/systemd-run','--unit=round1-undeclared','/usr/bin/true']),
            ('user-manager','C6.1',['/usr/lib/systemd/systemd','--user']),
            ('user-manager-cli','C6.2',['/usr/bin/systemctl','--user','daemon-reload']),
            ('user-enable-template','C6.1',['/usr/bin/systemctl','--user','enable','round1@fixture.service']),
            ('user-enable-alias','C6.1',['/usr/bin/systemctl','--user','enable','round1-alias.service']),
            ('user-transient-timer','C6.3',['/usr/bin/systemd-run','--user','--on-active=1h','--unit=round1-timer','/usr/bin/true']),
            ('network','C10.1',['/usr/bin/nmcli','connection','add','type','dummy','con-name','round1-undeclared','ifname','r1dummy']),
            ('bluetooth','C10.1',['/usr/bin/bluetoothctl','power','off']),
            ('firewall','C10.1',['/usr/sbin/nft','add','table','inet','round1_undeclared']),
            ('guard-remount','C10.2',['/usr/bin/mount','-o','remount,exec','/home']),
        ]
        for ident, variant, args in calls:
            if ident == 'root-shell':
                record(ident,variant,'sudo',args,'general root shell refused',denied)
            else:
                both(ident,variant,args)
        for path in ('/usr/bin/crontab','/usr/bin/at'):
            both('scheduler-'+Path(path).name,'C6.4',[path,'-'],absent_or_denied(path),
                 'authority refusal or scheduler removed', '@reboot /usr/bin/true\n')
        for path in ('/usr/bin/apt-get','/usr/bin/dpkg','/usr/lib/systemd/systemd'):
            dest=Path('/home/stand/round1-backend-copy')
            if path=='/usr/bin/apt-get' and Path(path).resolve()==Path('/usr/local/lib/stand/stand.py'):
                # BC4 replaces this backend with a readable declaration frontend.
                # Copying data is allowed; the copied bytes acquire no execution
                # entry or extra sudo authority. Keep both properties substantive.
                previous=str((ROOT/'current').resolve())
                print(json.dumps({'phase':'expected','id':'copy-apt-get-inert',
                    'variant':'C1.2','expected':'ordinary copy equals the real frontend; copied direct/sudo/launcher/interpreter execution refuses; declaration unchanged'},sort_keys=True),flush=True)
                record('copy-apt-get','C1.2','ordinary',['/bin/cp',path,str(dest)],
                       'readable broker copied as inert bytes',lambda c,o:c==0)
                record('copy-apt-get-exact','C1.2','operator',['/usr/bin/cmp','--',path,str(dest)],
                       'copied bytes exactly equal installed declaration frontend',lambda c,o:c==0)
                record('copy-apt-get','C1.2','sudo',['/bin/cp',path,str(dest)],
                       'no general privileged file-copy grant',denied)
                both('copied-apt-direct','C1.2',[str(dest),'install','ed'])
                for ident,request in (
                    ('copied-apt-launch','run\t'+str(dest)),
                    ('copied-apt-interpreter','run\t/usr/bin/python3.13\t'+str(dest)+'\tinstall\ted')):
                    record(ident,'C1.2','ordinary',['/usr/local/bin/stand-session','-c',request],
                           'copied frontend has no launch or interpreter authority',denied)
                record('copied-apt-no-change','C1.2','operator',
                       ['/usr/bin/test',str((ROOT/'current').resolve()),'=',previous],
                       'refused copied frontend did not change the selected declaration',lambda c,o:c==0)
            else:
                both('copy-'+Path(path).name,'C1.2',['/bin/cp',path,str(dest)])
            dest.unlink(missing_ok=True)
        for ident, command in [
            ('apt-library', 'import apt_pkg; print(apt_pkg.VERSION)'),
            ('apt-native-library', 'import ctypes; ctypes.CDLL("/usr/lib/x86_64-linux-gnu/libapt-pkg.so.7.0")'),
            ('nft-library', 'import ctypes; lib=ctypes.CDLL("libnftables.so.1"); lib.nft_ctx_new.restype=ctypes.c_void_p; p=lib.nft_ctx_new(0); lib.nft_run_cmd_from_buffer.argtypes=[ctypes.c_void_p,ctypes.c_char_p]; raise SystemExit(lib.nft_run_cmd_from_buffer(p,b"add table inet round1_library"))'),
        ]:
            pred = denied if ident != 'apt-library' else lambda c,o: c != 0 and (any(s in o.lower() for s in DENIAL) or 'ModuleNotFoundError' in o)
            both(ident,'C1.2' if ident=='apt-library' else 'C10.1',['/usr/bin/python3','-I','-c',command],pred)
        both('apt-environment','C1.5',['/usr/bin/env','APT_CONFIG='+str(config),'/usr/bin/apt-get','install','ed'])
        poison=td/'noexec.py';poison.write_text('open("/tmp/round1-undeclared-hook","w").write("poison")\n')
        positive('isolated-environment',['/usr/bin/env','PYTHONPATH='+str(td),'DBUS_SYSTEM_BUS_ADDRESS=unix:path=/tmp/absent-bus','/usr/local/bin/stand-verify'])
        record('sudo-setenv','C1.5','ordinary',['/usr/bin/sudo','-n','PYTHONPATH='+str(td),'/usr/local/bin/stand-verify'],'environment override refused',denied)
        record('sudo-preserve-environment','C1.5','ordinary',['/usr/bin/sudo','-n','-E','/usr/local/bin/stand-verify'],'preserve environment refused',denied)
        both('frontend-config-override','C1.5',['/usr/local/bin/apt','-c',str(config),'install','ed'])
        dbus = [
            ('manager-start','C6.2','org.freedesktop.systemd1','/org/freedesktop/systemd1','org.freedesktop.systemd1.Manager','StartUnit','ss','ssh.service','replace'),
            ('manager-enable','C6.2','org.freedesktop.systemd1','/org/freedesktop/systemd1','org.freedesktop.systemd1.Manager','EnableUnitFiles','asbb','1','ssh.service','false','false'),
            ('manager-reload','C6.2','org.freedesktop.systemd1','/org/freedesktop/systemd1','org.freedesktop.systemd1.Manager','Reload'),
            ('manager-link','C6.2','org.freedesktop.systemd1','/org/freedesktop/systemd1','org.freedesktop.systemd1.Manager','LinkUnitFiles','asbb','1','/tmp/round1.service','false','false'),
            ('manager-properties','C6.2','org.freedesktop.systemd1','/org/freedesktop/systemd1','org.freedesktop.systemd1.Manager','SetUnitProperties','sba(sv)','ssh.service','false','1','CPUWeight','t','77'),
            ('manager-transient','C6.3','org.freedesktop.systemd1','/org/freedesktop/systemd1','org.freedesktop.systemd1.Manager','StartTransientUnit','ssa(sv)a(sa(sv))','round1-undeclared.service','replace','1','Description','s','Undeclared','0'),
            ('network-dbus','C10.1','org.freedesktop.NetworkManager','/org/freedesktop/NetworkManager','org.freedesktop.NetworkManager','Enable','b','false'),
            ('network-add','C10.1','org.freedesktop.NetworkManager','/org/freedesktop/NetworkManager/Settings','org.freedesktop.NetworkManager.Settings','AddConnection2','a{sa{sv}}ua{sv}','0','1','0'),
            ('bluez-dbus','C10.1','org.bluez','/org/bluez/hci0','org.freedesktop.DBus.Properties','Set','ssv','org.bluez.Adapter1','Powered','b','false'),
            ('bluez-profile','C10.1','org.bluez','/org/bluez','org.bluez.ProfileManager1','RegisterProfile','osa{sv}','/round1/profile','<REDACTED>','0'),
        ]
        for ident,variant,*args in dbus:
            both(ident,variant,['/usr/bin/busctl','--system','call',*args])
        userbase='/home/stand/.config/systemd'
        for ident,path,content in [
            ('persistent-unit',userbase+'/user/round1.service','[Service]\nExecStart=/usr/bin/touch /tmp/round1-undeclared-hook\n'),
            ('drop-in',userbase+'/user/round1.service.d/round1.conf','[Service]\nEnvironment=ROUND1=1\n'),
            ('template',userbase+'/user/round1@.service','[Service]\nExecStart=/usr/bin/touch /tmp/round1-undeclared-hook\n'),
            ('generator',userbase+'/user-generators/round1','#!/bin/sh\ntouch /tmp/round1-undeclared-hook\n'),
            ('environment-generator',userbase+'/user-environment-generators/round1','#!/bin/sh\ntouch /tmp/round1-undeclared-hook\n')]:
            positive('write-'+ident,['/bin/sh','-c','mkdir -p "$(dirname "$1")" && cat > "$1" && chmod 755 "$1"','sh',path],input=content)
        positive('user-alias',['/bin/ln','-s','round1.service',userbase+'/user/round1-alias.service'])
        both('written-user-manager','C6.5',['/usr/lib/systemd/systemd','--user'])
        both('written-user-unit-start','C6.1',['/usr/bin/systemctl','--user','start','round1.service'])
        record('user-manager-inactive','C6.1','operator',['/usr/bin/systemctl','is-active','user@1000.service'],
               'user manager inactive',lambda c,o:c!=0 and o.strip() in ('inactive','failed','unknown'))
        both('cron-spool','C6.4',['/bin/sh','-c','printf "@reboot /usr/bin/true\\n" > /var/spool/cron/crontabs/stand'])
        lock = (ROOT/'apply.lock').open('a')
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try:
            for name,args in [('stand-apply',['/etc/stand/factory']),('stand-line',['remove','absent']),
                              ('stand-pkg',['install',str(DEV/'worker-1.json')]),('stand-verify',[]),
                              ('stand-compare',[str(td/'left.json'),str(td/'right.json')]),
                              ('apt',['install',str(DEV/'worker-1.json')]),('systemctl',['enable','ssh.service'])]:
                both('application-lock-'+name,'M1.02',['/usr/local/bin/'+name,*args],
                     lambda c,o: c != 0 and any(s in o.lower() for s in ('busy','in progress','locked','refused')),
                     'immediate refusal while application lock held')
        finally:
            lock.close()
        positive('install',['/usr/local/bin/stand-pkg','install',DEV/'worker-1.json'],'SUCCESS')
        positive('run',['/opt/stand/pkgs/dev-worker/bin/worker'],'development-version-1')
        positive('service',['/usr/local/bin/stand-line','add',DEV/'service.json'],'SUCCESS')
        timer='[Unit]\nDescription=Declared regression timer\n[Timer]\nOnBootSec=1h\nUnit=stand-development.service\nPersistent=false\n[Install]\nWantedBy=timers.target\n'
        timerfile=td/'timer.json'
        timerfile.write_text(json.dumps(dict(id='dev-timer',type='timer',managed=True,unit='stand-regression.timer',enabled='enabled',active=True,unit_text=timer,unit_sha256=hashlib.sha256(timer.encode()).hexdigest())))
        positive('timer',['/usr/local/bin/stand-line','add',timerfile],'SUCCESS')
        positive('account',['/usr/local/bin/stand-line','add',DEV/'account.json'],'SUCCESS')
        positive('rule',['/usr/local/bin/stand-line','add',DEV/'rule.json'],'SUCCESS')
        positive('wifi-saved',['/usr/local/bin/stand-line','add',DEV/'wifi.json'],'SUCCESS')
        positive('bluetooth-prepared',['/usr/local/bin/stand-line','add',DEV/'bluetooth.json'],'SUCCESS')
        positive('update',['/usr/local/bin/stand-pkg','update',DEV/'worker-2.json'],'SUCCESS')
        positive('verify',['/usr/local/bin/stand-verify'])
        retained=Path('/home/stand/round1-retained-worker')
        positive('retain-worker-copy',['/bin/cp','/opt/stand/pkgs/dev-worker/bin/worker',retained])
        both('generation-read','C1.6',['/bin/ls','/var/lib/stand/generations'])
        both('cache-read','C1.6',['/bin/ls','/var/cache/apt/archives'])
        before = (ROOT/'current').resolve()
        bad = json.loads((DEV/'worker-1.json').read_text())
        bad['files'][0]['sha256'] = '0'*64
        fixtures = [('invalid-payload',bad)]
        for ident, changes in [('root-service',{'User=stand':'User=root'}),
                               ('service-hook',{'[Service]':'[Service]\nExecStartPre=/usr/bin/touch /tmp/round1-undeclared-hook'})]:
            row=json.loads((DEV/'service.json').read_text())
            for a,b in changes.items(): row['unit_text']=row['unit_text'].replace(a,b)
            row['unit_sha256']=hashlib.sha256(row['unit_text'].encode()).hexdigest()
            fixtures.append((ident,row))
        row=json.loads((DEV/'worker-1.json').read_text());row['files'][0]['mode']=0o777
        fixtures.append(('mutable-program',row))
        fixtures.append(('privilege-path',dict(id='round1-privilege',type='privilege',managed=True,path='/etc/sudoers.d/round1',text='stand ALL=(ALL) NOPASSWD:ALL\n',mode=0o440,uid=0,gid=0)))
        for ident,row in fixtures:
            path=td/(ident+'.json');path.write_text(json.dumps(row))
            both('admission-'+ident,'C10.3',['/usr/local/bin/stand-line','add',path],
                 lambda c,o: c != 0 and ('FAILED' in o or 'REFUSED' in o), 'admission failure')
        record('previous-selected','M1.01','operator',['/usr/bin/readlink','-f',ROOT/'current'],
               'failed preparation preserves previous declaration',lambda c,o:c==0 and o.strip()==str(before))
        row=json.loads((DEV/'service.json').read_text())
        row['unit_text']=row['unit_text'].replace('worker --wait','worker')
        row['unit_sha256']=hashlib.sha256(row['unit_text'].encode()).hexdigest()
        path=td/'readback-mismatch.json';path.write_text(json.dumps(row))
        record('readback-mismatch','M1.02','ordinary',['/usr/local/bin/stand-line','add',path],
               'failed readback, no success report',lambda c,o:c!=0 and 'FAILED' in o and 'SUCCESS' not in o)
        positive('after-readback-failure',['/usr/local/bin/stand-verify'])
        positive('browser',['/usr/bin/w3m','-dump',str(DEV/'worker-1.c')])
        doc=Path('/home/stand/round1-document.txt');doc.write_text('Before\n');os.chown(doc,1000,1000)
        positive('editor',['/usr/bin/ed','-s',str(doc)],input='1c\nAfter\n.\nw\nq\n')
        doc.unlink(missing_ok=True)
        for ident in ('dev-timer','dev-service','dev-account','dev-rule','dev-wifi','dev-bluetooth','dev-worker'):
            positive('remove-'+ident,['/usr/local/bin/stand-line','remove',ident],'SUCCESS')
        both('retained-native','C1.6',[retained])
        both('retained-loader','C1.6',['/lib64/ld-linux-x86-64.so.2',retained],
             lambda c,o:denied(c,o) or (c!=0 and 'failed to map segment' in o), 'retained native mapping refused')
        retained.unlink(missing_ok=True)
        positive('final-verify',['/usr/local/bin/stand-verify'])
        marker=Path('/tmp/round1-undeclared-hook')
        record('hook-marker','C1.4','operator',['/usr/bin/test','!','-e',marker],
               'no undeclared hook executed',lambda c,o:c==0)
        marker.unlink(missing_ok=True)
        for path in (Path(userbase)/'user/round1.service',Path(userbase)/'user/round1@.service',
                     Path(userbase)/'user/round1-alias.service',Path(userbase)/'user-generators/round1',
                     Path(userbase)/'user-environment-generators/round1'):
            path.unlink(missing_ok=True)
        shutil.rmtree(Path(userbase)/'user/round1.service.d',ignore_errors=True)
    failed=[r['id']+':'+r['mode'] for r in RESULTS if not r['ok']]
    print(json.dumps({'event':'summary','tests':len(RESULTS),'failed':failed,'ok':not failed}),flush=True)
    return int(bool(failed))


if __name__ == '__main__':
    raise SystemExit(main())

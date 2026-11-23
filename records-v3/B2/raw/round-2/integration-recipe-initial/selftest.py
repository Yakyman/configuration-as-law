#!/usr/bin/python3 -B
"""Guest development observations. Each named operation is a separate planned question."""
import json,os,pathlib,shutil,subprocess,sys,tempfile,time
sys.path.insert(0,'/usr/local/lib/stand')
import stand
DEV=pathlib.Path('/usr/local/share/stand/dev')
OUT=pathlib.Path('/var/lib/stand/evidence');OUT.mkdir(exist_ok=True)
def cmd(args,expected=0):
    print('$ '+' '.join(map(str,args)),flush=True)
    p=subprocess.run(list(map(str,args)),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    print(p.stdout,end='');print('EXIT '+str(p.returncode),flush=True)
    if expected is not None and p.returncode!=expected:raise RuntimeError('unexpected return status')
    return p
def build_candidate(name,add=(),remove=()):
    d=pathlib.Path('/var/lib/stand')/name
    if d.exists():shutil.rmtree(d)
    shutil.copytree(stand.current_dir(),d)
    rows=stand.load(d);rows=[r for r in rows if r['id'] not in remove]
    for p in add:
        r=json.loads((DEV/p).read_text());rows=[old for old in rows if old['id']!=r['id']]+[r]
    stand.atomic(d/'machine.jsonl',''.join(stand.canonical(r)+'\n' for r in rows))
    return d
def main():
    op=sys.argv[1]
    print('UTC '+time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())+' OP '+op,flush=True)
    if op=='factory':
        cmd(['stand-verify']);cmd(['stand-compare','--snapshot',OUT/'factory.json'])
    elif op=='add':
        d=build_candidate('dev-add',['worker-1.json','service.json','rule.json','account.json'])
        cmd(['stand-apply',d]);cmd(['stand-verify']);cmd(['/opt/stand/pkgs/dev-worker/bin/worker'])
        cmd(['stand-compare','--snapshot',OUT/'added.json'])
    elif op=='invalid':
        before=stand.current_dir().name;d=build_candidate('dev-invalid',['worker-2.json'])
        rows=stand.load(d)
        for r in rows:
            if r['id']=='dev-worker':r['files'][0]['sha256']='0'*64
        stand.atomic(d/'machine.jsonl',''.join(stand.canonical(r)+'\n' for r in rows))
        cmd(['stand-apply',d],1)
        print('PREVIOUS_UNCHANGED '+str(stand.current_dir().name==before));cmd(['stand-verify'])
    elif op=='admission':
        cmd(['sudo','-u','stand','cp','/opt/stand/pkgs/dev-worker/bin/worker','/home/stand/undeclared-worker'])
        cmd(['sudo','-u','stand','/home/stand/undeclared-worker'],expected=None)
        loader=pathlib.Path('/lib64/ld-linux-x86-64.so.2')
        cmd(['sudo','-u','stand',loader,'/home/stand/undeclared-worker'],expected=None)
        cmd(['/opt/stand/pkgs/dev-worker/bin/worker'])
        cmd(['/usr/bin/findmnt','-n','-o','OPTIONS','--target','/home/stand'])
    elif op=='frontends':
        for name,args in [('apt',['install','unselected-package']),('pip',['install','unselected-package']),('npm',['install','unselected-package']),('flatpak',['install','unselected-package']),('systemctl',['enable','unselected.service']),('nmcli',['connection','add']),('nft',['flush','ruleset']),('useradd',['unselected']),('podman',['run','unselected']),('crontab',['-'])]:
            for mode in (['sudo','-u','stand'],['sudo']):
                cmd(mode+['/usr/local/bin/'+name]+args,expected=None)
        print('Direct original backend paths remain present; source-level P4 gap, not breaking')
    elif op=='work':
        cmd(['sudo','-u','stand','/usr/local/bin/stand-pkg','update',DEV/'worker-3.json'])
        cmd(['/opt/stand/pkgs/dev-worker/bin/worker'])
        cmd(['stand-verify'])
        # The editor receives document-edit commands, not a host-language macro.
        pathlib.Path('/home/stand/document.txt').write_text('Before\n');os.chown('/home/stand/document.txt',1000,1000)
        p=subprocess.run(['sudo','-u','stand','ed','-s','/home/stand/document.txt'],input='1c\nAfter\n.\nw\nq\n',text=True,capture_output=True)
        print('EDITOR_EXIT '+str(p.returncode));print(pathlib.Path('/home/stand/document.txt').read_text())
        pathlib.Path('/home/stand/page.html').write_text('<html><title>Development page</title><body><h1>Browser path works</h1><p>Passive content.</p></body></html>')
        os.chown('/home/stand/page.html',1000,1000)
        cmd(['sudo','-u','stand','w3m','-dump','/home/stand/page.html'])
        cmd(['/usr/bin/systemctl','is-active','stand-noexec'])
    elif op=='radio':
        d=build_candidate('dev-radio',['wifi.json','bluetooth.json'])
        cmd(['stand-apply',d]);cmd(['stand-verify'])
        cmd(['/usr/bin/nmcli','-f','connection.id,connection.uuid,802-11-wireless.ssid','connection','show','<REDACTED>'])
        print('Wi-Fi connection and Bluetooth pairing: not tested on hardware; Bluetooth profile prepared, no bond claimed')
    elif op=='remove':
        pid_result=cmd(['/usr/bin/systemctl','show','stand-development.service','-p','MainPID'])
        previous_pid=pid_result.stdout.strip().partition('=')[2]
        d=build_candidate('dev-remove',remove=['dev-worker','dev-service','dev-rule','dev-account'])
        cmd(['stand-apply',d]);cmd(['stand-verify'])
        cmd(['/usr/bin/systemctl','is-active','stand-development.service'],expected=None)
        cmd(['/usr/bin/systemctl','is-enabled','stand-development.service'],expected=None)
        print('PREVIOUS_PROCESS_EXISTS '+str(pathlib.Path('/proc',previous_pid).exists()))
        print('FORMER_PATH_EXISTS '+str(pathlib.Path('/opt/stand/pkgs/dev-worker/bin/worker').exists()))
        cmd(['sudo','-u','stand','/home/stand/undeclared-worker'],expected=None)
        cmd(['/usr/sbin/nft','list','table','inet','stand'])
        print('ACCOUNT '+stand.canonical(stand.account_value('fixture')))
    elif op.startswith('prepare-'):
        phase=op[len('prepare-'):]
        if phase=='add':d=build_candidate('cut-add',['worker-1.json','service.json','rule.json'])
        elif phase=='change':d=build_candidate('cut-change',['worker-2.json'])
        elif phase=='remove':d=build_candidate('cut-remove',remove=['dev-worker','dev-service','dev-rule'])
        else:raise ValueError(phase)
        print('CANDIDATE '+str(d))
    else:raise ValueError(op)
if __name__=='__main__':main()

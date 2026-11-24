"""Finite user-job and saved-radio frontends, all through declaration application."""
import hashlib,json,pathlib,re

def prepare(name,args):
    if name=='systemctl' and len(args)==3 and args[:2]==['--user','add']:
        row=json.loads(pathlib.Path(args[2]).read_text())
        if row['type']!='service' or not row.get('managed'):raise ValueError('declared managed user service required')
        return [row]
    if name=='systemd-run' and len(args)==3 and args[:2]==['--user','add-timer']:
        row=json.loads(pathlib.Path(args[2]).read_text())
        if row['type']!='timer' or not row.get('managed'):raise ValueError('declared managed user timer required')
        return [row]
    if name=='crontab' and len(args)==2 and args[0]=='add':
        spec=json.loads(pathlib.Path(args[1]).read_text())
        if set(spec)!={'id','command','on_boot','interval'} or not re.fullmatch('[a-zA-Z0-9_-]+',spec['id']):raise ValueError('exact scheduled command specification required')
        if not re.fullmatch(r'/opt/stand/pkgs/[a-zA-Z0-9_./-]+',spec['command']):raise ValueError('recorded managed command required')
        for field in ('on_boot','interval'):
            if not re.fullmatch(r'[1-9][0-9]*(s|min|h)',spec[field]):raise ValueError('explicit monotonic interval required')
        base='stand-'+spec['id'];unit=base+'.service'
        service='[Unit]\nDescription=Declared scheduled user command\n[Service]\nType=simple\nUser=stand\nExecStart='+spec['command']+'\nRestart=no\nKillMode=control-group\nTimeoutStopSec=5\nMemoryDenyWriteExecute=yes\nNoNewPrivileges=yes\nProtectSystem=strict\nPrivateTmp=yes\n[Install]\nWantedBy=multi-user.target\n'
        timer='[Unit]\nDescription=Declared user schedule\n[Timer]\nOnBootSec='+spec['on_boot']+'\nOnUnitActiveSec='+spec['interval']+'\nUnit='+unit+'\nPersistent=false\n[Install]\nWantedBy=timers.target\n'
        def row(kind,text):return {'id':'schedule:'+spec['id']+':'+kind,'type':kind,'managed':True,'unit':base+'.'+kind,'enabled':'enabled','unit_text':text,'unit_sha256':hashlib.sha256(text.encode()).hexdigest()}
        a=row('service',service);b=row('timer',timer);b['active']=True
        return [a,b]
    if name in ('nmcli','bluetoothctl') and len(args)==2 and args[0]=='add':
        row=json.loads(pathlib.Path(args[1]).read_text())
        if row['type']!=('wifi' if name=='nmcli' else 'bluetooth') or not row.get('managed'):raise ValueError('saved radio requirement line required')
        return [row]
    return None

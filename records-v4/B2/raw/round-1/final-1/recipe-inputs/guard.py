"""Admission limits for the finite broker; unsupported authority is refused."""
import base64
import struct
import configparser
import pathlib
import re
import shlex

FRONTENDS = ('stand-apply stand-verify stand-inventory stand-compare stand-pkg stand-line stand-import stand-build stand-appimage stand-update apt apt-get '
             'pip pip3 npm flatpak podman crontab at systemd-run systemctl nmcli nft '
             'useradd usermod userdel groupadd groupdel bluetoothctl').split()

def clean(value):
    if not isinstance(value, str) or any(ord(c)<32 for c in value):
        raise ValueError('control characters refused')
    return value

def unit(row, rows, directory):
    from stand import manifest
    text=row['unit_text']
    if any(x in text for x in ('\\', '%', '\r', '\x00')):
        raise ValueError('unit continuation/specifier refused')
    parser=configparser.ConfigParser(interpolation=None, strict=True)
    parser.optionxform=str
    parser.read_string(text)
    allowed={'Unit':{'Description'}, 'Install':{'WantedBy'}}
    if row['type']=='service':
        allowed['Service']={'Type','User','ExecStart','Restart','KillMode','TimeoutStopSec',
                            'MemoryDenyWriteExecute','NoNewPrivileges','ProtectSystem','PrivateTmp'}
        required={'Type':'simple','User':'stand','Restart':'no','KillMode':'control-group',
                  'TimeoutStopSec':'5','MemoryDenyWriteExecute':'yes','NoNewPrivileges':'yes',
                  'ProtectSystem':'strict','PrivateTmp':'yes'}
        for k,v in required.items():
            if parser.get('Service',k,fallback=None)!=v:raise ValueError('required service default '+k)
        argv=shlex.split(parser.get('Service','ExecStart',fallback=''))
        if not argv or not argv[0].startswith('/opt/stand/pkgs/'):
            raise ValueError('service requires a declared managed executable')
        if any('|' in arg for arg in argv):
            raise ValueError('service argument delimiter refused')
        files=[f for r in rows if r['type']=='program' and r.get('managed') for f in manifest(r,directory)]
        matches=[f for f in files if f['path']==argv[0] and f['mode'] & 0o111]
        if not matches:raise ValueError('service executable not recorded')
        if any(r.get('application_entry')==argv[0] for r in rows):raise ValueError('application/container service activation requires a separate supported configuration')
        # No shell, prefix escape or shell-like systemd substitutions.
        if any(not re.fullmatch(r'[a-zA-Z0-9_./:=+,-]+',arg) for arg in argv):
            raise ValueError('unsupported service argument')
        wanted='multi-user.target'
    elif row['type']=='timer':
        allowed['Timer']={'OnBootSec','OnUnitActiveSec','Unit','Persistent'}
        target=parser.get('Timer','Unit',fallback='')
        if target not in {r['unit'] for r in rows if r['type']=='service' and r.get('managed')}:
            raise ValueError('timer target must be declared')
        for key in ('OnBootSec','OnUnitActiveSec'):
            value=parser.get('Timer',key,fallback=None)
            if value is not None and not re.fullmatch(r'[1-9][0-9]*(s|min|h)',value):
                raise ValueError('unsupported timer interval')
        if not any(parser.has_option('Timer',k) for k in ('OnBootSec','OnUnitActiveSec')):
            raise ValueError('timer interval required')
        if parser.get('Timer','Persistent',fallback='false')!='false':raise ValueError('persistent timer unsupported')
        wanted='timers.target'
    else:
        allowed['Socket']={'ListenStream','Service','Accept','RemoveOnStop','SocketMode'}
        target=parser.get('Socket','Service',fallback='')
        if target not in {r['unit'] for r in rows if r['type']=='service' and r.get('managed')}:
            raise ValueError('socket target must be declared')
        if not re.fullmatch(r'/run/stand-sockets/[a-zA-Z0-9_-]+\.sock',parser.get('Socket','ListenStream',fallback='')):
            raise ValueError('socket path must be in managed runtime tree')
        for key,value in {'Accept':'no','RemoveOnStop':'yes','SocketMode':'0600'}.items():
            if parser.get('Socket',key,fallback=None)!=value:raise ValueError('required socket default '+key)
        wanted='sockets.target'
    for section in parser.sections():
        if section not in allowed or set(parser[section])-allowed[section]:
            raise ValueError('unsupported unit directive or hook')
    if parser.defaults() or parser.get('Install','WantedBy',fallback=None)!=wanted:
        raise ValueError('unsupported activation edge')
    if row['enabled'] not in ('enabled','disabled') or ('active' in row and type(row['active']) is not bool):
        raise ValueError('explicit enabled/active state required')
    if row.get('scope') not in (None,'system'):
        raise ValueError('user jobs use declared system units with User=stand')

def validate(rows, directory):
    from stand import load, manifest
    factory_dir=pathlib.Path('/etc/stand/factory')
    # Loading the factory itself is trusted only because it is root-owned.
    if pathlib.Path(directory).resolve()==factory_dir.resolve():return
    import system_channels
    factory=system_channels.expected_factory(rows,directory) if (factory_dir/'machine.jsonl').exists() else {}
    claims={}
    for row in rows:
        key=(row['type'],row.get('unit') or row.get('name'))
        if row['type'] in ('service','timer','socket','account','group'):
            value={k:v for k,v in row.items() if k!='id'}
            if key in claims and claims[key]!=value:raise ValueError('conflicting object contributions')
            claims[key]=value
        if row['id'] in factory:
            if row!=factory[row['id']]:raise ValueError('factory line change/removal unsupported: '+row['id'])
            continue
        typ=row['type']
        if row.get('channel')=='system-update':
            system_channels.validate(row)
            continue
        if typ not in ('program','code','account','group','service','timer','socket','rule','wifi','bluetooth') or not row.get('managed'):
            raise ValueError('unsupported authority-bearing line')
        if typ in ('program','code'):
            native_arguments=row.get('native_arguments',{})
            if not isinstance(native_arguments,dict):raise ValueError('native arguments must be a path map')
            native_files={f['path']:f for f in manifest(row,directory)}
            for path,args in native_arguments.items():
                f=native_files.get(path)
                if not f or not f['mode']&0o111 or not base64.b64decode(f['content_b64'],validate=True).startswith(b'\x7fELF'):
                    raise ValueError('native arguments require own recorded executable')
                if not isinstance(args,list) or len(args)>32 or any(not isinstance(a,str) or not a or len(a)>512 or '|' in a or any(ord(c)<32 for c in a) for a in args):
                    raise ValueError('invalid fixed native arguments')
            for ep in row.get('entrypoints',[]):
                if not re.fullmatch(r'/[a-zA-Z0-9_./:+,@=-]+',ep.get('path','')):raise ValueError('unsupported entrypoint path')
                if set(ep)!={'path','interpreter'} or ep['interpreter'] not in ('/usr/bin/python3.13','/usr/bin/bash','/usr/bin/dash','/usr/bin/perl','/usr/bin/node'):
                    raise ValueError('unsupported fixed script runner')
                if ep['path'] not in {f['path'] for f in manifest(row,directory)}:raise ValueError('entry script must belong to its line')
            for f in manifest(row,directory):
                content=base64.b64decode(f['content_b64'],validate=True)
                if content.startswith(b'\x7fELF'):
                    if len(content)<64 or content[4:6]!=b'\x02\x01' or struct.unpack_from('<H',content,18)[0]!=62:
                        raise ValueError('only native ELF64 is supported')
                    offset=struct.unpack_from('<Q',content,32)[0];size,count=struct.unpack_from('<HH',content,54)
                    if size<56 or offset+size*count>len(content):raise ValueError('invalid ELF headers')
                    for n in range(count):
                        typ,flags=struct.unpack_from('<II',content,offset+n*size)
                        if (typ==1 and flags&3==3) or (typ==0x6474e551 and flags&1):
                            raise ValueError('writable executable ELF segment or stack refused')
                if f['uid']!=0 or f['gid']!=0 or f['mode'] & 0o022:
                    raise ValueError('managed code must remain root-owned and not caller-writable')
                p=pathlib.Path(f['path'])
                if any(parent.is_symlink() for parent in p.parents):raise ValueError('symlink payload parent refused')
        elif typ=='group':
            if not re.fullmatch(r'[a-z][a-z0-9_-]{0,30}',row['name']) or not 1100<=row['gid']<=60000 or row['members']!=[]:
                raise ValueError('managed group requires a supported name, numeric gid and empty membership')
            if any(r['type']=='account' and (r['name']==row['name'] or r['gid']==row['gid']) for r in rows):
                raise ValueError('independent group conflicts with account primary group')
        elif typ=='account':
            name=row['name']
            if not re.fullmatch(r'[a-z][a-z0-9_-]{0,30}',name) or row['groups']!=[name]:
                raise ValueError('managed accounts have only their own primary group')
            if not 1100<=row['gid']<=60000 or row['home']!='/home/'+name or row['shell']!='/usr/sbin/nologin':
                raise ValueError('unsupported account authority')
            clean(row['gecos'])
        elif typ in ('service','timer','socket'):unit(row,rows,directory)
        elif typ=='rule':
            if row.get('backend','nft')!='nft':raise ValueError('guard changes unsupported')
        elif typ=='wifi':
            for key in ('name','ssid'):clean(row[key])
            if not re.fullmatch(r'[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}',row['uuid']):
                raise ValueError('invalid network UUID')
            if row['state'] not in ('saved','connected') or type(row['autoconnect']) is not bool:
                raise ValueError('unsupported network requirement')
        elif typ=='bluetooth':
            for key in ('adapter','address'):
                if not re.fullmatch(r'(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}',row[key]):raise ValueError('invalid radio address')
            clean(row['name'])
            if row['state'] not in ('prepared','paired') or type(row['trusted']) is not bool:
                raise ValueError('unsupported Bluetooth requirement')
        if row.get('channel') in ('pip','npm'):
            import language_channels
            language_channels.validate(row)
        if row.get('channel')=='repository':system_channels.validate(row)
    import app_channels
    app_channels.validate(rows,directory)
    if set(factory)-{r['id'] for r in rows}:raise ValueError('factory line removal unsupported')

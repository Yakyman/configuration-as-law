"""Admission limits for the finite broker; unsupported authority is refused."""
import configparser
import pathlib
import re
import shlex

FRONTENDS = ('stand-apply stand-verify stand-compare stand-pkg stand-line apt apt-get '
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
        files=[f for r in rows if r['type']=='program' and r.get('managed') for f in manifest(r,directory)]
        matches=[f for f in files if f['path']==argv[0] and f['mode'] & 0o111]
        if len(matches)!=1:raise ValueError('service executable not recorded')
        # No shell, prefix escape or shell-like systemd substitutions.
        if any(not re.fullmatch(r'[a-zA-Z0-9_./:=+,-]+',arg) for arg in argv):
            raise ValueError('unsupported service argument')
        wanted='multi-user.target'
    else:
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
    for section in parser.sections():
        if section not in allowed or set(parser[section])-allowed[section]:
            raise ValueError('unsupported unit directive or hook')
    if parser.defaults() or parser.get('Install','WantedBy',fallback=None)!=wanted:
        raise ValueError('unsupported activation edge')
    if row['enabled'] not in ('enabled','disabled') or type(row.get('active')) is not bool:
        raise ValueError('explicit enabled/active state required')
    if row.get('scope') not in (None,'system'):
        raise ValueError('user jobs use declared system units with User=stand')

def validate(rows, directory):
    from stand import load, manifest
    factory_dir=pathlib.Path('/etc/stand/factory')
    # Loading the factory itself is trusted only because it is root-owned.
    if pathlib.Path(directory).resolve()==factory_dir.resolve():return
    factory={r['id']:r for r in load(factory_dir, guarded=False)} if (factory_dir/'machine.jsonl').exists() else {}
    for row in rows:
        if row['id'] in factory:
            if row!=factory[row['id']]:raise ValueError('factory line change/removal unsupported: '+row['id'])
            continue
        typ=row['type']
        if typ not in ('program','code','account','service','timer','rule','wifi','bluetooth') or not row.get('managed'):
            raise ValueError('unsupported authority-bearing line')
        if typ in ('program','code'):
            for ep in row.get('entrypoints',[]):
                if set(ep)!={'path','interpreter'} or ep['interpreter'] not in ('/usr/bin/python3.13','/usr/bin/bash','/usr/bin/dash','/usr/bin/perl'):
                    raise ValueError('unsupported fixed script runner')
                if ep['path'] not in {f['path'] for f in manifest(row,directory)}:raise ValueError('entry script must belong to its line')
            for f in manifest(row,directory):
                if f['uid']!=0 or f['gid']!=0 or f['mode'] & 0o022:
                    raise ValueError('managed code must remain root-owned and not caller-writable')
                p=pathlib.Path(f['path'])
                if any(parent.is_symlink() for parent in p.parents):raise ValueError('symlink payload parent refused')
        elif typ=='account':
            name=row['name']
            if not re.fullmatch(r'[a-z][a-z0-9_-]{0,30}',name) or row['groups']!=[name]:
                raise ValueError('managed accounts have only their own primary group')
            if not 1100<=row['gid']<=60000 or row['home']!='/home/'+name or row['shell']!='/usr/sbin/nologin':
                raise ValueError('unsupported account authority')
            clean(row['gecos'])
        elif typ in ('service','timer'):unit(row,rows,directory)
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
    if set(factory)-{r['id'] for r in rows}:raise ValueError('factory line removal unsupported')

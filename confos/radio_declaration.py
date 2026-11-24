"""Isolated proposal: validate radio rows and derive immutable bytes; no execution.

Not imported by ConfOS. One optional simulated fixture, WPA2-PSK IPv4 and BR/EDR
bonds only. Inputs follow the existing relative-path/checksum declaration contract.
"""
import configparser
import hashlib
import ipaddress
import json
from pathlib import Path
import re
import shlex

ADAPTERS = ('00:AA:01:00:00:00', '00:AA:01:01:00:01')
PREFIX = '/usr/lib/confos/radio'
PINS = {'bluez': '5.82-1.1', 'bluez-test-tools': '5.82-1.1',
        'hostapd': '2:2.10-24', 'wpasupplicant': '2:2.10-24', 'iw': '6.9-1',
        'wireless-regdb': '2026.09.03-1~deb13u1', 'dbus': '1.16.2-2',
        'iproute2': '6.15.0-1'}


def fail(message):
    raise ValueError(message)


def exact(value, keys):
    if not isinstance(value, dict) or set(value) != set(keys):
        fail('unknown or missing JSON fields')


def hexbytes(value, minimum, maximum):
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]+', value):
        fail('lowercase hex required')
    if len(value) % 2 or not minimum <= len(value)//2 <= maximum:
        fail('invalid hex byte length')
    return value


def address(value):
    if not isinstance(value, str):
        fail('IPv4 interface required')
    try:
        result = ipaddress.IPv4Interface(value)
    except ValueError:
        fail('IPv4 interface required')
    if str(result) != value or result.ip in (result.network.network_address, result.network.broadcast_address):
        fail('canonical usable IPv4 host/prefix required')
    if not result.ip.is_private or result.network.prefixlen < 24:
        fail('prototype requires private IPv4 subnet /24 or narrower')
    return result


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail('duplicate JSON key')
        result[key] = value
    return result


def read_input(directory, sha, source):
    if not re.fullmatch('[0-9a-f]{64}', sha):
        fail('SHA256 required')
    path = Path(source)
    if path.is_absolute() or not path.parts or '..' in path.parts:
        fail('input must be relative beneath declaration')
    root = Path(directory).resolve()
    full = root/path
    # Disallow symlinks at every component, including links back inside the tree.
    current = root
    for part in path.parts:
        current = current/part
        if current.is_symlink():
            fail('symlink input refused')
    if not full.is_file() or full.stat().st_size > 65536:
        fail('input must be a regular file no larger than 64KiB')
    data = full.read_bytes()
    if hashlib.sha256(data).hexdigest() != sha:
        fail('input checksum mismatch')
    return data


def bond(data):
    try:
        text = data.decode('ascii')
        if any(ord(c) < 32 and c != '\n' for c in text):
            fail('control byte in bond input')
        parser = configparser.ConfigParser(interpolation=None, strict=True,
                                           empty_lines_in_values=False)
        parser.optionxform = str
        parser.read_string(text)
    except (UnicodeError, configparser.Error) as e:
        fail('invalid BlueZ info: '+str(e))
    if parser.defaults() or not {'General', 'LinkKey'} <= set(parser.sections()) or set(parser.sections())-{'General','LinkKey','DeviceID'}:
        fail('unsupported BlueZ info groups')
    general = dict(parser['General'])
    required = {'Name', 'Class', 'SupportedTechnologies', 'Trusted', 'Blocked'}
    if not required <= set(general) or set(general)-required-{'Services'}:
        fail('unsupported BlueZ General fields')
    if general['SupportedTechnologies'] != 'BR/EDR;' or general['Blocked'] != 'false' or general['Trusted'] not in ('true','false'):
        fail('only unblocked BR/EDR bonds supported')
    if not re.fullmatch('[A-Za-z0-9 ._-]{1,64}', general['Name']) or not re.fullmatch('0x[0-9a-f]{6}', general['Class']):
        fail('unsupported name/class')
    if 'Services' in general and not re.fullmatch('(?:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12};)*', general['Services']):
        fail('invalid services')
    key = dict(parser['LinkKey'])
    exact(key, ('Key','Type','PINLength'))
    hexbytes(key['Key'],16,16)
    if key['Type'] != '5' or key['PINLength'] != '0':
        fail('only authenticated P-192 type5 SSP key supported')
    if 'DeviceID' in parser:
        dev = dict(parser['DeviceID'])
        exact(dev, ('Source','Vendor','Product','Version'))
        if any(not re.fullmatch('[0-9]{1,5}', v) or int(v)>65535 for v in dev.values()) or dev['Source'] not in ('1','2'):
            fail('invalid DeviceID')
    return key['Key']


def derive(text, directory):
    """Read radio-only rows; return files (bytes/mode/uid/gid), plan, required pins.

    Caller must filter full parsed rows, check all global path collisions, stage
    input bytes, and check resolved package closure. This does no disk mutation.
    """
    rows = []
    identities = set()
    for number, line in enumerate(text.splitlines(),1):
        row = shlex.split(line, comments=True)
        if not row:
            continue
        arity = {'radio-fixture':4,'network':4,'bluetooth-pair':5}.get(row[0])
        if len(row) != arity:
            fail(f'line {number}: unsupported radio kind/arity')
        identity = tuple(row[:3] if row[0]=='bluetooth-pair' else row[:2])
        if identity in identities:
            fail('duplicate radio identity')
        identities.add(identity)
        rows.append(row)
    files, fixtures, networks, bonds = {}, {}, {}, {}
    def emit(path, data, mode=0o600):
        if path in files:
            fail('duplicate output path')
        files[path] = {'data':data,'mode':mode,'uid':0,'gid':0}
    for row in sorted(rows):
        kind = row[0]
        data = read_input(directory, row[-2], row[-1])
        if kind == 'bluetooth-pair':
            adapter, peer = row[1:3]
            if adapter not in ADAPTERS or peer not in ADAPTERS or adapter == peer:
                fail('pair must name opposite declared simulated adapters')
            bonds[adapter,peer] = bond(data)
            emit(f'{PREFIX}/bluez/{adapter}/{peer}/info', data)
            continue
        name = row[1]
        if not re.fullmatch('[a-z][a-z0-9-]{0,31}',name):
            fail('invalid radio name')
        try:
            obj = json.loads(data, object_pairs_hook=unique_object)
        except (UnicodeError,json.JSONDecodeError) as e:
            fail('invalid JSON: '+str(e))
        if kind == 'radio-fixture':
            exact(obj, ('format','wifi','bluetooth'))
            if type(obj['format']) is not int or obj['format'] != 1 or type(obj['bluetooth']) is not bool:
                fail('unsupported fixture format')
            wifi = obj['wifi']
            if wifi is not None:
                exact(wifi, ('ssid_hex','psk','address','channel'))
                hexbytes(wifi['ssid_hex'],1,32); hexbytes(wifi['psk'],32,32)
                address(wifi['address'])
                if type(wifi['channel']) is not int or not 1 <= wifi['channel'] <= 11:
                    fail('fixture channel must be 1..11')
            fixtures[name] = obj
        else:
            exact(obj, ('format','fixture','ssid_hex','psk','address'))
            if type(obj['format']) is not int or obj['format'] != 1 or not isinstance(obj['fixture'],str):
                fail('unsupported network format')
            hexbytes(obj['ssid_hex'],1,32);hexbytes(obj['psk'],32,32);address(obj['address'])
            networks[name] = obj
    if len(fixtures)>1 or len(networks)>1:
        fail('one simulated fixture/client supported')
    plan = {'format':1,'fixture':None,'network':None,'bonds':[]}
    pins = {}
    if fixtures:
        fixture_name, fixture = next(iter(fixtures.items()))
        plan['fixture'] = {'name':fixture_name, **fixture}
        wifi = fixture['wifi']
        if wifi:
            emit(PREFIX+'/hostapd.conf', ('interface=wlan0\ndriver=nl80211\nssid2='+wifi['ssid_hex']+'\nhw_mode=g\nchannel='+str(wifi['channel'])+'\nwpa=2\nwpa_key_mgmt=WPA-PSK\nrsn_pairwise=CCMP\nwpa_psk='+wifi['psk']+'\n').encode())
            pins.update({k:PINS[k] for k in ('hostapd','iw','wireless-regdb','iproute2')})
        if fixture['bluetooth']:
            pins.update({k:PINS[k] for k in ('bluez','bluez-test-tools','dbus')})
            for adapter in ADAPTERS:
                emit(f'{PREFIX}/bluez/{adapter}/settings',b'[General]\nDiscoverable=false\n')
    else:
        fixture_name, fixture = None, None
    for name, obj in networks.items():
        if not fixture or obj['fixture'] != fixture_name or fixture['wifi'] is None:
            fail('network requires its Wi-Fi fixture')
        wifi = fixture['wifi']
        if any(obj[k]!=wifi[k] for k in ('ssid_hex','psk')):
            fail('network security differs from declared AP')
        client, ap = address(obj['address']), address(wifi['address'])
        if client.network != ap.network or client.ip == ap.ip:
            fail('client requires distinct address in AP subnet')
        plan['network'] = {'name':name,**obj}
        emit(PREFIX+'/wpa.conf', ('ctrl_interface=/run/confos-radio/wpa\nupdate_config=0\nnetwork={\n ssid='+obj['ssid_hex']+'\n psk='+obj['psk']+'\n key_mgmt=WPA-PSK\n proto=RSN\n pairwise=CCMP\n group=CCMP\n}\n').encode())
        pins['wpasupplicant'] = PINS['wpasupplicant']
    if bonds and (not fixture or not fixture['bluetooth']):
        fail('bond requires declared Bluetooth fixture')
    for (adapter,peer),key in sorted(bonds.items()):
        reverse = bonds.get((peer,adapter))
        if reverse is not None and reverse != key:
            fail('opposite endpoint bond keys differ')
        plan['bonds'].append({'adapter':adapter,'peer':peer})
    # One-way bond state is legal (e.g. after one line removal); boot verifies
    # its loaded key, but must not claim mutual authentication without both rows.
    emit(PREFIX+'/plan.json', (json.dumps(plan,sort_keys=True,separators=(',',':'))+'\n').encode())
    return {'files':files,'plan':plan,'required_packages':pins}

#!/usr/bin/python3
"""UNINTEGRATED boot supervisor draft. Must run before READY in private mount NS.

Fixed immutable inputs only. No recording, pairing, key generation, or live apply.
Running this module changes radios: import/test is safe; main is root-only.
"""
import ctypes
import errno
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import select
import shutil
import signal
import socket
import struct
import subprocess as sp
import time

IMMUTABLE = Path('/usr/lib/confos/radio')
RUN = Path('/run/confos-radio')
STORE = Path('/var/lib/bluetooth')
AP_NS = 'confos-radio-ap'
ADDRESSES = ['00:AA:01:00:00:00', '00:AA:01:01:00:01']
READY = Path('/run/confos-radio-ready.json')
BASE_ENV = {'PATH':'/usr/bin:/usr/sbin','LC_ALL':'C','HOME':'/root'}


def load_plan():
    # Caller must mount generated tree read-only; no path/input overrides accepted.
    if not os.statvfs(IMMUTABLE).f_flag & os.ST_RDONLY:
        raise ValueError('radio inputs must be on read-only mounted system storage')
    info = (IMMUTABLE/'plan.json').stat()
    if info.st_uid != 0 or info.st_mode & 0o022:
        raise ValueError('plan must be root-owned and not writable by group/other')
    raw = (IMMUTABLE/'plan.json').read_bytes()
    plan = json.loads(raw)
    if set(plan) != {'format','fixture','network','bonds'} or plan['format'] != 1:
        raise ValueError('invalid immutable radio plan')
    fixture = plan['fixture']
    network = plan['network']
    if fixture is not None:
        if set(fixture) != {'name','format','wifi','bluetooth'} or fixture['format'] != 1 or type(fixture['bluetooth']) is not bool:
            raise ValueError('invalid fixture plan')
        if not re.fullmatch('[a-z][a-z0-9-]{0,31}',fixture['name']):
            raise ValueError('invalid fixture name')
        wifi = fixture['wifi']
        if wifi is not None:
            if set(wifi) != {'ssid_hex','psk','address','channel'} or type(wifi['channel']) is not int or not 1<=wifi['channel']<=11:
                raise ValueError('invalid Wi-Fi fixture')
            validate_wifi(wifi)
    if network is not None:
        if not fixture or fixture['wifi'] is None or set(network) != {'name','format','fixture','ssid_hex','psk','address'}:
            raise ValueError('orphan/invalid network')
        validate_wifi(network)
        if network['format'] != 1 or network['fixture'] != fixture['name']:
            raise ValueError('network fixture mismatch')
        ap = fixture['wifi']
        if any(network[k] != ap[k] for k in ('ssid_hex','psk')):
            raise ValueError('network credentials differ')
        a,b = ipaddress.IPv4Interface(network['address']),ipaddress.IPv4Interface(ap['address'])
        if a.network!=b.network or a.ip==b.ip:
            raise ValueError('network address conflict')
    if not isinstance(plan['bonds'],list):
        raise ValueError('invalid bond list')
    seen = set()
    for pair in plan['bonds']:
        if not fixture or not fixture['bluetooth'] or set(pair) != {'adapter','peer'}:
            raise ValueError('orphan/invalid bond')
        identity = pair['adapter'],pair['peer']
        if identity in seen or set(identity) != set(ADDRESSES):
            raise ValueError('invalid/duplicate bond identity')
        seen.add(identity)
    return plan,hashlib.sha256(raw).hexdigest()


def validate_wifi(obj):
    if not re.fullmatch('(?:[0-9a-f]{2}){1,32}',obj['ssid_hex']) or not re.fullmatch('[0-9a-f]{64}',obj['psk']):
        raise ValueError('invalid Wi-Fi bytes')
    addr = ipaddress.IPv4Interface(obj['address'])
    if str(addr)!=obj['address'] or not addr.ip.is_private or addr.network.prefixlen<24 or addr.ip in (addr.network.network_address,addr.network.broadcast_address):
        raise ValueError('invalid fixture IPv4 address')


def command(*argv, check=True, env=None):
    # No shell and no caller-supplied environment/argv passthrough.
    return sp.run(argv,env=env or BASE_ENV,text=True,stdout=sp.PIPE,stderr=sp.STDOUT,
                  timeout=15,check=check)


class Supervisor:
    def __init__(self,plan,digest):
        self.plan=plan;self.digest=digest;self.children=[];self.mounted=False
        self.namespace=False;self.hwsim=False;self.client_address=False
        self.bus=None;self.adapters=[];self.running=True
        self.owned_run=False;self.machine_mount=False;self.failure=False;self.vhci=False;self.run_mounted=False
        self.status={'plan_sha256':digest,'wifi':'absent','bluetooth':'absent'}

    def launch(self,name,*argv,env=None):
        log=(RUN/(name+'.log')).open('wb')
        try:
            process=sp.Popen(argv,stdin=sp.DEVNULL,stdout=log,stderr=sp.STDOUT,
                             env=env or BASE_ENV,start_new_session=True)
        finally: log.close()
        self.children.append((name,process))
        return process

    def check_children(self):
        for name,process in self.children:
            if process.poll() is not None:
                raise RuntimeError('radio child exited: '+name)

    def wait_for(self,predicate,label,seconds=20):
        deadline=time.monotonic()+seconds
        while time.monotonic()<deadline:
            if not self.running: raise RuntimeError('radio startup interrupted')
            self.check_children()
            if predicate(): return
            time.sleep(.2)
        raise RuntimeError('radio readiness timeout: '+label)

    def prepare(self):
        if RUN.exists():
            # Never delete another supervisor's state or silently reuse keys.
            raise RuntimeError('stale/active radio runtime directory')
        RUN.mkdir(mode=0o700)
        self.owned_run=True
        # A private mount namespace contains the native BlueZ storage alias.
        libc=ctypes.CDLL(None,use_errno=True)
        if libc.unshare(0x00020000) != 0:
            raise OSError(ctypes.get_errno(),'unshare mount namespace')
        command('/usr/bin/mount','--make-rprivate','/')
        command('/usr/bin/mount','-t','tmpfs','-o','mode=0700,nosuid,nodev,noexec','confos-radio-private',str(RUN))
        self.run_mounted=True
        fixture=self.plan['fixture']
        if fixture is None:
            self.status['fixture']='absent'
            return
        if fixture['wifi'] is not None: self.start_wifi(fixture['wifi'])
        if fixture['bluetooth']: self.start_bluetooth()

    def start_wifi(self,wifi):
        if Path('/sys/module/mac80211_hwsim').exists():
            raise RuntimeError('preexisting hwsim devices refused')
        command('/usr/sbin/modprobe','mac80211_hwsim','radios=2')
        self.hwsim=True
        output=command('/usr/sbin/iw','dev').stdout
        if set(re.findall(r'Interface (\S+)',output)) != {'wlan0','wlan1'}:
            raise RuntimeError('unexpected Wi-Fi device enumeration')
        command('/usr/sbin/ip','netns','add',AP_NS);self.namespace=True
        command('/usr/sbin/iw','phy','phy0','set','netns','name',AP_NS)
        command('/usr/sbin/ip','netns','exec',AP_NS,'/usr/sbin/ip','link','set','lo','up')
        command('/usr/sbin/ip','netns','exec',AP_NS,'/usr/sbin/ip','addr','add',wifi['address'],'dev','wlan0')
        self.launch('hostapd','/usr/sbin/ip','netns','exec',AP_NS,'/usr/sbin/hostapd',str(IMMUTABLE/'hostapd.conf'))
        def ap_ready():
            result=command('/usr/sbin/ip','netns','exec',AP_NS,'/usr/sbin/iw','dev','wlan0','info',check=False)
            return result.returncode==0 and 'type AP' in result.stdout and 'channel '+str(wifi['channel'])+' ' in result.stdout
        self.wait_for(ap_ready,'AP native interface')
        network=self.plan['network']
        if network is None:
            self.status['wifi']='fixture-AP-ready; client absent'
            return
        command('/usr/sbin/ip','addr','add',network['address'],'dev','wlan1');self.client_address=True
        self.launch('supplicant','/usr/sbin/wpa_supplicant','-Dnl80211','-iwlan1','-c',str(IMMUTABLE/'wpa.conf'))
        self.wait_for(self.wifi_connected,'client WPA2 connection')
        peer=str(ipaddress.IPv4Interface(wifi['address']).ip)
        command('/usr/bin/ping','-n','-c','3','-W','2','-I','wlan1',peer)
        self.status['wifi']='WPA2-CCMP connected; AP traffic verified'

    def wifi_connected(self):
        result=command('/usr/sbin/wpa_cli','-p',str(RUN/'wpa'),'-i','wlan1','status',check=False)
        values=dict(line.split('=',1) for line in result.stdout.splitlines() if '=' in line)
        # Exact network config is immutable; status verifies negotiated parameters.
        if not (values.get('wpa_state')=='COMPLETED' and values.get('key_mgmt')=='WPA2-PSK' and values.get('pairwise_cipher')=='CCMP'):
            return False
        expected=str(ipaddress.IPv4Interface(self.plan['network']['address']).ip)
        return (values.get('ip_address')==expected and values.get('id')=='0'
                and values.get('bssid')=='02:00:00:00:00:00'
                and values.get('group_cipher')=='CCMP')

    def start_bluetooth(self):
        import dbus
        from dbus.mainloop.glib import DBusGMainLoop
        DBusGMainLoop(set_as_default=True)
        if list(Path('/sys/class/bluetooth').glob('hci*')):
            raise RuntimeError('preexisting Bluetooth controllers refused')
        self.vhci=not Path('/sys/module/hci_vhci').exists()
        command('/usr/sbin/modprobe','hci_vhci')
        immutable=IMMUTABLE/'bluez'
        expected={a+'/settings' for a in ADDRESSES}
        expected.update(p['adapter']+'/'+p['peer']+'/info' for p in self.plan['bonds'])
        actual={str(p.relative_to(immutable)) for p in immutable.rglob('*') if p.is_file()}
        if actual != expected or any(p.is_symlink() for p in immutable.rglob('*')):
            raise RuntimeError('unexpected immutable BlueZ files')
        shutil.copytree(immutable,RUN/'bluez')
        STORE.mkdir(mode=0o700,parents=True,exist_ok=True)
        command('/usr/bin/mount','--bind',str(RUN/'bluez'),str(STORE));self.mounted=True
        # Private bus: BlueZ sees this explicit address through libdbus, not /run/dbus.
        # Same explicit deterministic bus identity as native fixture; no UUID tool.
        machine=RUN/'machine-id'
        machine.write_text(hashlib.sha256(b'ConfOS simulated radio fixture bus').hexdigest()[:32]+'\n')
        target=Path('/var/lib/dbus/machine-id')
        target.parent.mkdir(parents=True,exist_ok=True);target.touch(exist_ok=True)
        command('/usr/bin/mount','--bind',str(machine),str(target));self.machine_mount=True
        config=RUN/'bus.conf'
        config.write_text('<busconfig><type>system</type><listen>unix:path=/run/confos-radio/bus</listen>'
                          '<policy context="default"><deny user="*"/><allow user="root"/></policy>'
                          '<policy user="root"><allow own="*"/><allow send_destination="*"/>'
                          '<allow receive_sender="*"/></policy></busconfig>\n')
        self.launch('dbus','/usr/bin/dbus-daemon','--config-file='+str(config),'--nofork','--nopidfile')
        self.wait_for(lambda:(RUN/'bus').exists(),'private bus')
        env={**BASE_ENV,'DBUS_SYSTEM_BUS_ADDRESS':'unix:path='+str(RUN/'bus')}
        self.launch('btvirt','/usr/bin/btvirt','-B','-l2')
        self.launch('bluetoothd','/usr/libexec/bluetooth/bluetoothd','--nodetach',env=env)
        self.bus=dbus.bus.BusConnection(env['DBUS_SYSTEM_BUS_ADDRESS'])
        self.bus.set_exit_on_disconnect(False)
        def adapters_ready():
            try:
                objects=dbus.Interface(self.bus.get_object('org.bluez','/'),'org.freedesktop.DBus.ObjectManager').GetManagedObjects()
                found=sorted((str(path),str(ifaces['org.bluez.Adapter1']['Address'])) for path,ifaces in objects.items() if 'org.bluez.Adapter1' in ifaces)
                if [a for _,a in found] != ADDRESSES: return False
                self.adapters=found
                return True
            except dbus.DBusException: return False
        self.wait_for(adapters_ready,'exact Bluetooth controller identities')
        for path,_ in self.adapters:
            props=dbus.Interface(self.bus.get_object('org.bluez',path),'org.freedesktop.DBus.Properties')
            for key,value in (('Powered',True),('Pairable',False),('Discoverable',True)):
                props.Set('org.bluez.Adapter1',key,dbus.Boolean(value),signature='ssv')
        def bonds_ready():
            objects=dbus.Interface(self.bus.get_object('org.bluez','/'),'org.freedesktop.DBus.ObjectManager').GetManagedObjects()
            for pair in self.plan['bonds']:
                path=dict((a,p) for p,a in self.adapters)[pair['adapter']]+'/dev_'+pair['peer'].replace(':','_')
                if not objects.get(path,{}).get('org.bluez.Device1',{}).get('Paired',False): return False
            return True
        self.wait_for(bonds_ready,'native saved bond states')
        if len(self.plan['bonds'])==2:
            authenticated_traffic(self.adapters,'boot')
            self.status['bluetooth']='both bonds; authenticated bidirectional traffic verified'
        else:
            self.status['bluetooth']=str(len(self.plan['bonds']))+' native saved bond(s); no mutual-link claim'

    def verify_recorded_state(self):
        if self.bus:
            expected={p['adapter']+'/'+p['peer']+'/info' for p in self.plan['bonds']}
            actual={str(p.relative_to(STORE)) for p in STORE.glob('*/*/info')}
            if actual!=expected: raise RuntimeError('native bond membership changed')
            for relative in expected:
                if (STORE/relative).read_bytes()!=(IMMUTABLE/'bluez'/relative).read_bytes():
                    raise RuntimeError('native declared bond bytes changed')
        if self.plan['fixture'] and self.plan['fixture']['wifi'] and not self.plan['network']:
            addresses=json.loads(command('/usr/sbin/ip','-j','addr','show','dev','wlan1').stdout)
            if any(a['family']=='inet' for entry in addresses for a in entry['addr_info']):
                raise RuntimeError('client IPv4 address remains without network row')
        # Trusted serial evidence contains status/digests only, never key material.
        print('RADIO VERIFIED '+json.dumps(self.status,sort_keys=True),flush=True)

    def publish_ready(self):
        self.check_children()
        pending=READY.with_suffix('.pending')
        pending.write_text(json.dumps(self.status,sort_keys=True)+'\n')
        pending.chmod(0o600);os.replace(pending,READY)
        print('RADIO READY '+self.digest,flush=True)
        notify = os.environ.get('NOTIFY_SOCKET')
        if notify:
            # Only the trusted PID1 service provides this socket. Native child
            # environments are rebuilt and never inherit it.
            address = '\0'+notify[1:] if notify.startswith('@') else notify
            with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as endpoint:
                endpoint.connect(address)
                endpoint.sendall(b'READY=1')

    def cleanup(self):
        errors=[]
        if not self.owned_run: return
        # Always revoke readiness before stopping children or deleting state.
        READY.unlink(missing_ok=True)
        for name,process in reversed(self.children):
            if process.poll() is None:
                try:
                    os.killpg(process.pid,signal.SIGTERM)
                    process.wait(timeout=5)
                except (ProcessLookupError,sp.TimeoutExpired):
                    try: os.killpg(process.pid,signal.SIGKILL)
                    except ProcessLookupError: pass
                    try: process.wait(timeout=5)
                    except sp.TimeoutExpired: errors.append('child did not exit: '+name)
        self.children=[]
        def attempt(*argv):
            try: command(*argv)
            except (OSError,sp.SubprocessError) as error: errors.append(str(error))
        if self.client_address:
            attempt('/usr/sbin/ip','addr','del',self.plan['network']['address'],'dev','wlan1')
            # Supplicant is already stopped; owned hwsim unload clears links.
        if self.namespace: attempt('/usr/sbin/ip','netns','del',AP_NS)
        if self.hwsim: attempt('/usr/sbin/modprobe','-r','mac80211_hwsim')
        if self.mounted:
            attempt('/usr/bin/umount',str(STORE))
            if errors: self.mounted=os.path.ismount(STORE)
            else: self.mounted=False
        if self.bus:
            try: self.bus.close()
            except Exception as error: errors.append('private bus close: '+str(error))
        if self.machine_mount: attempt('/usr/bin/umount','/var/lib/dbus/machine-id')
        if self.vhci: attempt('/usr/sbin/modprobe','-r','hci_vhci')
        if not self.mounted and (RUN/'bluez').exists(): shutil.rmtree(RUN/'bluez')
        if self.failure:
            for log in sorted(RUN.glob('*.log')):
                print('RADIO FAILURE LOG '+log.name+' '+log.read_text(errors='replace')[-4000:],flush=True)
        if self.run_mounted:
            attempt('/usr/bin/umount',str(RUN))
            self.run_mounted=os.path.ismount(RUN)
        if not errors and not self.run_mounted: shutil.rmtree(RUN)
        # Retain root-only volatile diagnostics on failure, never recursively erase
        # any still-mounted store. Next start deliberately refuses stale state.
        if errors: print('RADIO CLEANUP ERRORS '+repr(errors),flush=True)

    def run(self):
        def stop(signum,frame): self.running=False
        signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
        try:
            self.prepare();self.verify_recorded_state();self.publish_ready()
            next_verify=time.monotonic()+10
            while self.running:
                self.check_children()
                if self.plan['network'] and not self.wifi_connected():
                    raise RuntimeError('declared Wi-Fi association lost')
                if self.bus:
                    import dbus
                    for path,_ in self.adapters:
                        properties=dbus.Interface(self.bus.get_object('org.bluez',path),'org.freedesktop.DBus.Properties').GetAll('org.bluez.Adapter1')
                        if not properties.get('Powered') or properties.get('Pairable') or not properties.get('Discoverable'):
                            raise RuntimeError('declared Bluetooth adapter state changed')
                if time.monotonic()>=next_verify:
                    self.verify_recorded_state();next_verify=time.monotonic()+10
                time.sleep(1)
        except BaseException:
            self.failure=True
            raise
        finally: self.cleanup()


def authenticated_traffic(adapters, label):
    # Linux BT_SECURITY_HIGH=3 requires authenticated encryption, not just a bond flag.
    local, peer = adapters[0][1], adapters[1][1]
    # This guest's rebuilt CPython lacks Bluetooth sockaddr converters. Use the
    # native Linux socket ABI (BlueZ5.82 lib/l2cap.h), not an emulated transport.
    libc = ctypes.CDLL(None, use_errno=True)
    libc.bind.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint]
    libc.connect.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint]
    libc.accept.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
    def address(addr, psm):
        return struct.pack('<HH6sHBx', 31, psm, bytes.fromhex(addr.replace(':', ''))[::-1], 0, 0)
    def bind(endpoint, addr, psm):
        native_address = address(addr, psm)
        if libc.bind(endpoint.fileno(), native_address, len(native_address)) != 0:
            number = ctypes.get_errno()
            raise OSError(number, 'native L2CAP bind')
    server = socket.socket(31, socket.SOCK_SEQPACKET, 0)
    client = socket.socket(31, socket.SOCK_SEQPACKET, 0)
    server.settimeout(10)
    client.settimeout(10)
    accepted = None
    try:
        for endpoint in (server, client):
            endpoint.setsockopt(274, 4, struct.pack('BB', 3, 0))
        bind(server, peer, 0x1001)
        server.listen(1)
        bind(client, local, 0)
        native_address = address(peer, 0x1001)
        result = libc.connect(client.fileno(), native_address, len(native_address))
        if result != 0:
            number = ctypes.get_errno()
            if number != errno.EINPROGRESS:
                raise OSError(number, 'native L2CAP connect')
            if not select.select([], [client], [], 10)[1]:
                raise TimeoutError('native L2CAP connect timeout')
            number = client.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            if number:
                raise OSError(number, 'native L2CAP connect completion')
        if not select.select([server], [], [], 10)[0]:
            raise TimeoutError('native L2CAP accept timeout')
        accepted_fd = libc.accept(server.fileno(), None, None)
        if accepted_fd < 0:
            raise OSError(ctypes.get_errno(), 'native L2CAP accept')
        accepted = socket.socket(31, socket.SOCK_SEQPACKET, 0, fileno=accepted_fd)
        accepted.settimeout(10)
        message = ('ConfOS authenticated fixture '+label).encode()
        client.send(message)
        assert accepted.recv(1024) == message
        accepted.send(message[::-1])
        assert client.recv(1024) == message[::-1]
        for name, endpoint in [('client', client), ('server', accepted)]:
            level, key_size = struct.unpack('BB', endpoint.getsockopt(274, 4, 2))
            print('LINK SECURITY', label, name, level, key_size, flush=True)
            assert level == 3 and key_size == 16
        print('AUTHENTICATED BIDIRECTIONAL L2CAP PASS', label, flush=True)
    finally:
        if accepted:
            accepted.close()
        client.close()
        server.close()


if __name__ == '__main__':
    if os.geteuid()!=0: raise SystemExit('radio supervisor requires root at boot')
    os.umask(0o077)
    selected,identity=load_plan()
    Path('/run/confos-radio.pid').write_text(str(os.getpid())+'\n')
    Supervisor(selected,identity).run()

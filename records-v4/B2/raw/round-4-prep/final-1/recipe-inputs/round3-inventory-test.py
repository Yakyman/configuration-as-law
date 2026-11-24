#!/usr/bin/python3 -B
"""Disposable-VM-only direct-superuser planting test. No production invocation."""
import json, os, pathlib, shutil, socket, subprocess, sys
sys.path.insert(0,'/usr/local/lib/stand')
import inventory

def run(*args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:raise RuntimeError(str(args)+': '+p.stderr)
    return p.stdout

def main():
    if os.getuid()!=0:raise RuntimeError('disposable VM root required')
    print('EXPECTED: direct-superuser unrecorded program, unclassified bytes without suffix, container code, unit, timer, socket, cron, account, group, rights, login key, firewall, listener, saved network, and boot configuration each appear without coverage.',flush=True)
    files={
        '/dev/shm/round3-inventory-code':b'#!/bin/sh\nexit 0\n',
        '/opt/round3-inventory/program':b'#!/bin/sh\nexit 0\n',
        '/var/tmp/round3-inventory/without-suffix':b'print(42)\n',
        '/var/lib/containers/round3-inventory/rootfs/opt/program':b'#!/bin/sh\nexit 0\n',
        '/etc/systemd/system/round3-inventory.service':b'[Unit]\nDescription=Inventory fixture\n[Service]\nExecStart=/usr/bin/sleep 300\n',
        '/etc/systemd/system/round3-inventory.timer':b'[Timer]\nOnBootSec=1h\nUnit=round3-inventory.service\n',
        '/etc/systemd/system/round3-inventory.socket':b'[Socket]\nListenStream=127.0.0.1:39873\n',
        '/etc/cron.d/round3-inventory':b'0 0 1 1 * root /usr/bin/true\n',
        '/etc/sudoers.d/round3-inventory':b'round3inv ALL=(ALL) NOPASSWD: /usr/bin/true\n',
        '/var/tmp/round3-inventory/.ssh/authorized_keys':b'ssh-ed25519 <REDACTED> inventory-fixture\n',
        '/etc/NetworkManager/system-connections/round3-inventory.nmconnection':b'[connection]\nid=round3-inventory\nuuid=<REDACTED>\ntype=wifi\n[wifi]\nssid=round3-inventory\n[ipv4]\nmethod=auto\n',
        '/boot/loader/entries/round3-inventory.conf':b'title Inventory fixture\nlinux /missing-inventory-kernel\n'}
    backups={p:pathlib.Path(p).read_bytes() for p in ('/etc/passwd','/etc/group','/etc/shadow','/etc/gshadow')}
    listener=socket.socket();listener.bind(('127.0.0.1',0));listener.listen(1)
    try:
        for name,data in files.items():
            p=pathlib.Path(name)
            if p.exists():raise RuntimeError('fixture collision '+name)
            p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);p.chmod(0o600 if 'nmconnection' in name else 0o644)
        pathlib.Path('/opt/round3-inventory/program').chmod(0o755)
        with open('/etc/passwd','a') as f:f.write('round3inv:x:28971:28971::/nonexistent:/usr/sbin/nologin\n')
        with open('/etc/group','a') as f:f.write('round3inv:x:28971:\n')
        with open('/etc/shadow','a') as f:f.write('round3inv:!:1:0:99999:7:::\n')
        with open('/etc/gshadow','a') as f:f.write('round3inv:!::\n')
        # Native backend invoked directly by root is the test fixture, not a broker claim.
        run('/usr/sbin/nft','add','table','inet','round3_inventory')
        run('/usr/sbin/nft','add','chain','inet','round3_inventory','input','{ type filter hook input priority 7; policy accept; }')
        run('/usr/sbin/nft','add','rule','inet','round3_inventory','input','tcp','dport','39874','drop')
        run('/usr/bin/systemctl','daemon-reload')
        run('/usr/bin/nmcli','connection','reload')
        objects,summary=inventory.inventory(emit=True)
        def found(kind=None,identity=None):
            return any((kind is None or x['kind']==kind) and (identity is None or x['object']==identity) and not x['lines'] and x['status'] in ('unknown','unrecorded') for x in objects)
        for name in files:assert found(identity=name),name
        assert found('account','round3inv')
        assert found('group','round3inv')
        assert found('port','tcp:127.0.0.1:'+str(listener.getsockname()[1]))
        assert any(x['kind']=='firewall-rule' and x['observed'].get('table')=='round3_inventory' and not x['lines'] for x in objects)
        assert found('saved-network','<REDACTED>')
        assert summary['complete'] is False
        print('ROUND3 INVENTORY PASS: all planted objects surfaced; unsuffixed bytes remain unclassified; semantic completeness remains unknown.',flush=True)
    finally:
        listener.close()
        for name,data in backups.items():pathlib.Path(name).write_bytes(data)
        for name in files:pathlib.Path(name).unlink(missing_ok=True)
        subprocess.run(['/usr/sbin/nft','delete','table','inet','round3_inventory'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.run(['/usr/bin/systemctl','daemon-reload'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.run(['/usr/bin/nmcli','connection','reload'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        for name in ('/opt/round3-inventory','/var/tmp/round3-inventory','/var/lib/containers/round3-inventory'):shutil.rmtree(name,ignore_errors=True)
if __name__=='__main__':main()

#!/usr/bin/python3
"""Recorded ordinary-session test. It may attempt mutations; never unconfined."""
import errno
import os
from pathlib import Path
import socket
import subprocess as sp

count=0

def denied(name,fn,missing=False):
    global count
    try: fn()
    except OSError as error:
        print('DENIED',name,error.errno,str(error),flush=True)
        if error.errno not in ((errno.EACCES,errno.EPERM,errno.ENOENT) if missing else (errno.EACCES,errno.EPERM)): raise
        count+=1
    else: raise AssertionError('ordinary mutation control unexpectedly accessible: '+name)

print('PROFILE',open('/proc/self/attr/current').read().strip(),'EUID',os.geteuid(),flush=True)
for kind,proto in ((socket.SOCK_RAW,1),(socket.SOCK_SEQPACKET,0)):
    def create(kind=kind,proto=proto):
        endpoint=socket.socket(31,kind,proto);endpoint.close()
    denied('Bluetooth socket '+str((kind,proto)),create)
for address in ('/run/confos-radio/bus','/run/confos-radio/wpa/wlan1'):
    def connect(address=address):
        endpoint=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM if address.endswith('bus') else socket.SOCK_DGRAM)
        try: endpoint.connect(address)
        finally: endpoint.close()
    denied('private Unix '+address,connect,missing=True)
for path in ('/dev/vhci','/run/netns/confos-radio-ap'):
    def op(path=path):
        descriptor=os.open(path,os.O_RDWR);os.close(descriptor)
    denied('native control '+path,op)
# The controls are real but privately mounted: require proc-root/fd aliases to fail.
radio_pids=[]
for proc in Path('/proc').glob('[0-9]*'):
    try:
        args=(proc/'cmdline').read_bytes()
        if b'/usr/lib/confos/radio_runtime.py' in args: radio_pids.append(proc.name)
    except OSError: pass
assert radio_pids, 'could not identify supervisor for alias probes'
for pid in radio_pids:
    for suffix in ('root/run/confos-radio/bus','fd/0'):
        path='/proc/'+pid+'/'+suffix
        def alias(path=path,suffix=suffix):
            if suffix=='fd/0':
                descriptor=os.open(path,os.O_RDWR);os.close(descriptor)
            else:
                endpoint=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
                try: endpoint.connect(path)
                finally: endpoint.close()
        denied('private proc alias '+path,alias)
commands=[
 ['/usr/bin/aa-exec','-p','confos-radio','--','/usr/bin/true'],
 ['/usr/sbin/wpa_cli','-p','/run/confos-radio/wpa','-i','wlan1','set_network','0','psk','"undeclared-change"'],
 ['/usr/bin/dbus-send','--bus=unix:path=/run/confos-radio/bus','--print-reply','--dest=org.bluez','/org/bluez/hci0','org.freedesktop.DBus.Properties.Set','string:org.bluez.Adapter1','string:Powered','variant:boolean:false'],
 ['/usr/bin/btmgmt','--index','0','power','off'],
]
for command in commands:
    result=sp.run(command,stdout=sp.PIPE,stderr=sp.STDOUT,text=True,timeout=10)
    print('NATIVE',command,'RC',result.returncode,result.stdout,flush=True)
    assert result.returncode!=0,command
print('RADIO ORDINARY CONTROL DENIAL PROBE PASS',count,flush=True)

#!/usr/bin/python3
"""Recorded app-context probes. Missing endpoints are reported, never denials."""
import ctypes
import errno
import os
from pathlib import Path
import socket

profile=Path('/proc/self/attr/current').read_text().strip()
print('FLATPAK RADIO PROFILE',profile,'EUID',os.geteuid(),flush=True)
assert profile == 'confos-flatpak (enforce)',profile
assert os.geteuid()!=0
assert Path('/.flatpak-info').is_file(), 'not an actual Flatpak sandbox'
assert 'Seccomp:\t2' in Path('/proc/self/status').read_text(), 'native seccomp filter missing'
assert Path('/usr/bin/bash').is_file()
assert Path('/app/bin/mpv').is_file()
# Positive primitive controls distinguish a working interpreter/libc/network
# stack from missing modules or an unconditional inability to create sockets.
with socket.socket(socket.AF_INET,socket.SOCK_STREAM): pass
a,b=socket.socketpair();a.sendall(b'positive');assert b.recv(8)==b'positive';a.close();b.close()
libc=ctypes.CDLL(None,use_errno=True)
libc.socket.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_int]
libc.socket.restype=ctypes.c_int
for kind,protocol in ((socket.SOCK_RAW,1),(socket.SOCK_SEQPACKET,0)):
    ctypes.set_errno(0)
    fd=libc.socket(31,kind,protocol)
    if fd>=0:
        os.close(fd)
        raise AssertionError('Bluetooth socket accessible in app context')
    error=ctypes.get_errno()
    assert error in (errno.EACCES,errno.EPERM,errno.EAFNOSUPPORT),(kind,protocol,error)
    # Flatpak1.16.6 deliberately returns EAFNOSUPPORT from its socket-family
    # seccomp filter. Host native authenticated traffic is a required positive
    # control in the harness; absence of kernel Bluetooth cannot pass it.
    mechanism = 'SECCOMP-FAMILY-FILTER' if error == errno.EAFNOSUPPORT else 'ACCESS-DENIED'
    print('NATIVE BLUETOOTH SOCKET BLOCKED',mechanism,kind,protocol,error,flush=True)

denied=hidden=0
for path in ('/run/confos-radio/bus','/run/confos-radio/wpa/wlan1',
             '/run/host/run/confos-radio/bus','/run/host/run/confos-radio/wpa/wlan1'):
    try:
        with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM if path.endswith('bus') else socket.SOCK_DGRAM) as endpoint:
            endpoint.connect(path)
    except OSError as error:
        if error.errno==errno.ENOENT:
            hidden+=1;print('UNEXPOSED UNIX ENDPOINT',path,flush=True)
        else:
            assert error.errno in (errno.EACCES,errno.EPERM),(path,error)
            denied+=1;print('UNIX CONTROL DENIED',path,error.errno,flush=True)
    else: raise AssertionError('native Unix control accessible: '+path)
for path in ('/dev/vhci','/dev/rfkill','/run/netns/confos-radio-ap',
             '/run/host/dev/vhci','/run/host/run/netns/confos-radio-ap'):
    try:
        fd=os.open(path,os.O_RDWR);os.close(fd)
    except OSError as error:
        if error.errno==errno.ENOENT:
            hidden+=1;print('UNEXPOSED DEVICE OR NAMESPACE',path,flush=True)
        else:
            assert error.errno in (errno.EACCES,errno.EPERM),(path,error)
            denied+=1;print('DEVICE OR NAMESPACE DENIED',path,error.errno,flush=True)
    else: raise AssertionError('native device/namespace accessible: '+path)
print('FLATPAK RADIO CONTROL PROBE PASS blocked-sockets=2 path-denials='+str(denied)+' unexposed-paths='+str(hidden),flush=True)

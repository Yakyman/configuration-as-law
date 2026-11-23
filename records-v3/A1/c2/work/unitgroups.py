import sys
sys.path.insert(0,'c2/work')
from emit import emit
U='raw:raw/coreos/units.txt'; UU='raw:raw/coreos/user-list-units.txt'
DEV=('HOLE','S2.2-1,S2.2-2,S3-1','Device units systemd generates from udev for present disks, ttys, NIC',
 'doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.device.html',
 'Mounts depend on them (S2.2-1), but they exist exactly while the hardware exists; removal cannot be applied and 2.2 says nothing about objects generated from hardware.')
rows=[
['coreos-a3f2270221',*DEV[:3],DEV[3],DEV[4]],
['coreos-88335c6c87',DEV[0],DEV[1],'User-manager view of device units generated from udev devices',DEV[3],DEV[4]],
['coreos-18fb2985ed','MUST','S2.2-1,S2.2-2','Active mounts: /, /boot, /etc, /sysroot, /var, /run/user/1001 tmpfs','raw:raw/coreos/mounts.txt',
 'Unmounting any of them stops the system or the user session from working (S2.2-2); behaviour depends on them (S2.2-1).'],
['coreos-565df89b5f','MUST','S2.2-1,S2.2-2','User-manager view of mounts incl. /tmp, debugfs, credential mounts, rpc_pipefs','raw:raw/coreos/mounts.txt',
 'Unmounting any member removes a filesystem or service credentials that programs use, so something stops or becomes impossible (S2.2-2).'],
['coreos-9994d7ebc4','NOT','S2.2-1,S2.2-2','Names referenced by other units but with no unit file on the machine',U,
 'Nothing exists behind these names and nothing runs; there is nothing whose removal changes what the computer does (S2.2-1, S2.2-2).'],
['coreos-97fdaec6aa','NOT','S2.2-1,S2.2-2','Template instances referenced in the user manager with no unit file',UU,
 'No unit file exists in the user manager; nothing runs, so removal changes nothing (S2.2-1, S2.2-2).'],
['coreos-0ff15b2741','MUST','S2.2-2','Runtime scopes: init.scope holds PID 1; session-4.scope holds an SSH session',U,
 'Stopping a scope kills its processes, so the computer stops doing something (S2.2-2); no sentence of 2.2 exempts runtime groupings.'],
['coreos-3bc8c8458c','MUST','S2.2-2','init.scope of the user manager, holding the user systemd process',UU,
 'Stopping it stops the user manager and its services (S2.2-2); no sentence of 2.2 exempts runtime groupings.'],
['coreos-253d752b01','MUST','S2.2-2','Implicit slices grouping system services, gettys and user-1001 processes',U,
 'Stopping a slice stops every unit inside it, so the computer stops doing something (S2.2-2).'],
['coreos-b855166ba5','MUST','S2.2-2','Root slice of the user manager',UU,
 'Stopping it stops all user-manager units (S2.2-2).'],
['coreos-eb57ff0e5c','MUST','S2.2-15,S2.2-2','Generated sshd sockets: local AF_UNIX and AF_VSOCK SSH listeners',
 'doc:https://www.freedesktop.org/software/systemd/man/latest/systemd-ssh-generator.html',
 'They are endpoints open for SSH connections; S2.2-15 states open ports must be recorded, and removal makes these logins impossible.'],
]
print(emit(rows))

#!/usr/bin/env python3
"""Group-level and member-level rules for stored groups outside /home (classification c2).

member_rule(group, member) -> (decision, label) or None
"""
import re

RT = 'RUNTIME'

# Creators of runtime objects (tmpfs /run, /tmp, pseudo file systems). Decision of the creator in brackets.
RUN_CREATORS = [
    (r'^/run/udev', 'systemd-udevd (systemd-udev package file, INSTALLED-PACKAGE)'),
    (r'^/run/systemd/generator', 'systemd generators from fstab and package units (INSTALLED-PACKAGE / SETTING-OWN fstab)'),
    (r'^/run/systemd/transient/docker', 'systemd scope requested by dockerd for the container (PROGRAM-OWN container)'),
    (r'^/run/systemd', 'systemd and its services (systemd package files, INSTALLED-PACKAGE)'),
    (r'^/run/user/1000/pulse', 'PipeWire/pulse user service (INSTALLED-PACKAGE)'),
    (r'^/run/user', 'the user systemd instance user@1000.service (INSTALLED-PACKAGE)'),
    (r'^/run/containerd', 'containerd (containerd.io file, INSTALLED-PACKAGE), started for docker.service (SETTING-OWN)'),
    (r'^/run/docker', 'dockerd (docker-ce file, INSTALLED-PACKAGE) started by docker.service (SETTING-OWN)'),
    (r'^/run/NetworkManager', 'NetworkManager (INSTALLED-PACKAGE; service enabled by preset, SETTING-DEFAULT)'),
    (r'^/run/libvirt', 'libvirt daemons via socket units (INSTALLED-PACKAGE; SETTING-DEFAULT presets)'),
    (r'^/run/credentials', 'systemd credentials for units (INSTALLED-PACKAGE)'),
    (r'^/run/initramfs', 'initramfs systemd (dracut image, INSTALLED-DERIVED)'),
    (r'^/run/varlink', 'systemd varlink registry (INSTALLED-PACKAGE)'),
    (r'^/run/chrony', 'chronyd (INSTALLED-PACKAGE)'),
    (r'^/run/avahi-daemon', 'avahi-daemon (INSTALLED-PACKAGE)'),
    (r'^/run/cockpit', 'cockpit issue units (INSTALLED-PACKAGE)'),
    (r'^/run/cups', 'cups socket unit (INSTALLED-PACKAGE)'),
    (r'^/run/dbus', 'dbus-broker socket (INSTALLED-PACKAGE)'),
    (r'^/run/fsck', 'systemd-fsck (INSTALLED-PACKAGE)'),
    (r'^/run/irqbalance', 'irqbalance (INSTALLED-PACKAGE)'),
    (r'^/run/log', 'systemd-journald (INSTALLED-PACKAGE)'),
    (r'^/run/lvm', 'lvm2 (INSTALLED-PACKAGE)'),
    (r'^/run/pcscd', 'pcscd socket unit (INSTALLED-PACKAGE)'),
    (r'^/run/ssh-unix-local', 'sshd-unix-local socket from a systemd generator (INSTALLED-PACKAGE)'),
    (r'^/run/stratisd', 'stratisd (INSTALLED-PACKAGE)'),
    (r'^/run/sudo', 'sudo (INSTALLED-PACKAGE)'),
    (r'^/run/tmpfiles.d', 'systemd-tmpfiles (INSTALLED-PACKAGE)'),
    (r'^/run/tpm2-tss', 'systemd-tmpfiles from tpm2-tss config (INSTALLED-PACKAGE)'),
    (r'^/run/tuned', 'tuned (INSTALLED-PACKAGE)'),
    (r'^/run$', 'systemd, systemd-tmpfiles and running services (INSTALLED-PACKAGE files; docker.service SETTING-OWN)'),
    (r'^/tmp', 'systemd PrivateTmp= of service units and systemd-tmpfiles (INSTALLED-PACKAGE)'),
    (r'^/var/tmp/systemd-private', 'systemd PrivateTmp= of the service unit, removed at service stop (INSTALLED-PACKAGE)'),
    (r'^/var/tmp$', 'systemd PrivateTmp= of service units, removed at service stop (INSTALLED-PACKAGE)'),
    (r'^/var/lib/nfs/rpc_pipefs', 'rpc_pipefs kernel file system mounted by nfs-utils unit (INSTALLED-PACKAGE)'),
]


def run_creator(group):
    for rx, who in RUN_CREATORS:
        if re.search(rx, group):
            return who
    return None


def member_rule(g, m):
    p, typ = m['path'], m['type']
    b = p.rsplit('/', 1)[1]
    who = run_creator(g)
    if who:
        return (RT, 'exists only while running; created by ' + who)

    if g == '/etc':
        t = {
            '.pwd.lock': ('RECORD', 'lock file written by shadow-utils'),
            '.updated': ('RECORD', 'systemd update-done stamp'),
            'debuginfod': ('RECORD', 'directory written by a program (not in any package list)'),
            'dhcp': ('RECORD', 'directory written by a program'),
            'kmscon': ('RECORD', 'directory written by a program'),
            'gnome-remote-desktop': ('RECORD', 'directory written by systemd-tmpfiles at boot'),
            'fstab.script': ('PROGRAM-OWN', 'executable script left by the OS installation, not in any package'),
            'group-': ('RECORD', 'backup copy written by shadow-utils'),
            'gshadow-': ('RECORD', 'backup copy written by shadow-utils'),
            'passwd-': ('RECORD', 'backup copy written by shadow-utils'),
            'shadow-': ('RECORD', 'backup copy written by shadow-utils'),
            'subgid-': ('RECORD', 'backup copy written by shadow-utils'),
            'subuid-': ('RECORD', 'backup copy written by shadow-utils'),
            'resolv.conf': ('UNKNOWN', 'DNS link; creator not recorded: SETTING-DEFAULT if tmpfiles, SETTING-OWN if a person'),
        }
        return t.get(b)
    if g == '/etc/alternatives':
        return ('SETTING-DEFAULT', 'system-wide alternative link set by package scriptlets at installation')
    if g == '/var/lib/alternatives':
        return ('SETTING-DEFAULT', 'alternatives state written by package scriptlets at installation')
    if g == '/etc/firewalld/policies' or (g == '/etc/firewalld/zones' and b == 'docker.xml'):
        return ('GAP-TWO', 'firewall zone/policy written by dockerd at first start: SETTING-DEFAULT (default obtained with docker-ce) or RECORD (no person chose it)')
    if g == '/etc/firewalld/zones':
        if b == 'FedoraWorkstation.xml':
            return ('UNKNOWN', 'zone file written at OS installation (04:40:36); who chose its values not recorded')
        if b.endswith('.old'):
            return ('RECORD', 'backup copy written by firewalld')
    if g.startswith('/etc/systemd/system.control'):
        if typ == 'directory':
            return ('RECORD', 'drop-in directory written by systemd for runtime property changes')
        return ('GAP-TWO', 'resource drop-in written by a daemon as it ran: SETTING-DEFAULT (default obtained with package) or RECORD (no person chose it)')
    if g == '/etc/systemd/system/multi-user.target.wants':
        if b == 'docker.service':
            return ('SETTING-OWN', 'docker.service enabled at a person\'s command (systemctl enable)')
        if b == 'sshd.service':
            return ('SETTING-OWN', 'sshd enablement link created 06:21:35, after OS installation, so not an installation default')
        return ('SETTING-DEFAULT', 'service enablement link created from package presets at installation')
    if g == '/etc/yum.repos.d':
        return ('SETTING-OWN', 'repository configuration added at a person\'s command (dnf config-manager)')
    if g in ('/opt', '/opt/containerd'):
        return ('RECORD', 'directory written by containerd at its start')
    if g == '/root':
        return {
            '.cache': ('RECORD', 'cache directory'),
            '.docker': ('RECORD', 'docker CLI state directory'),
            '.ssh': ('RECORD', 'empty directory written at OS installation'),
            'anaconda-ks.cfg': ('RECORD', 'kickstart record written by the OS installer'),
            'original-ks.cfg': ('RECORD', 'kickstart copy written by the OS installer'),
        }.get(b)
    if g.startswith('/root/.docker'):
        return ('RECORD', 'docker CLI/buildx state written as it ran')
    if g == '/usr/lib64':
        if typ in ('file', 'symlink'):
            return ('INSTALLED-PACKAGE', 'library in a package file list (/lib64 alias), unchanged or link with packaged mtime')
        return ('RECORD', 'parent directory created by rpm, not in any package list')
    if g.startswith('/usr/'):
        return ('RECORD', 'parent directory created by rpm, not in any package list')
    if g == '/var/lib':
        return ('RECORD', 'state directory or link written by a program')
    if g == '/var/lib/NetworkManager':
        return ('RECORD', 'NetworkManager working state, leases and generated key')
    if g.startswith('/var/lib/dnf/repos'):
        return ('RECORD', 'dnf countme state')
    if g == '/var/lib/lastlog':
        return ('RECORD', 'login history')
    if g == '/var/lib/rsyslog':
        return ('RECORD', 'rsyslog journal cursor')
    if g == '/var/lib/selinux':
        return ('RECORD', 'policy build directory written by semodule')
    if g == '/var/lib/selinux/targeted/active' and b == 'booleans.local':
        return ('UNKNOWN', 'SELinux booleans file rewritten during docker-ce install; who chose the values not recorded')
    if g.startswith('/var/lib/selinux/targeted/active'):
        if typ == 'directory' and g in ('/var/lib/selinux/targeted/active', '/var/lib/selinux/targeted/active/modules'):
            return ('SETTING-DEFAULT', 'policy module store directory rewritten by semodule during package installation')
        return ('SETTING-DEFAULT', 'SELinux policy module (access rules) installed by package scriptlet at installation')
    if g.startswith('/var/cache'):
        return ('RECORD', 'package-manager / man-db cache')
    if g.startswith('/var/log'):
        if b == 'README':
            return ('RECORD', 'link written by systemd at installation')
        return ('RECORD', 'log written by a program')
    return None

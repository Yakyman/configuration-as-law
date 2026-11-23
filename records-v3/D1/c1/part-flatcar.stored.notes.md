# Stored objects: independent classification notes

Scope: only L2:stored-outside-packages rows. Inventory labels were disregarded. The raw filesystem snapshot stores path, type, mode, uid, gid, and link target in six NUL-delimited fields. It does not contain arbitrary file contents. Directories listed as members are considered with their contents; grouping never implies homogeneous membership. No objects were removed. UNKNOWN identifies unavailable actual consumers or contents, not a defect concerning system-design treatment of state.

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-11** Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.
- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- **S3-2** If what the object does remains unknown, the case yields ?.

## Rule U: udev link-stack entries
For each group strictly under /run/udev/links/, every member is the recorded priority/device association used when udev chooses the target of a device alias. Removing it eliminates that candidate during subsequent link updates. Device alias behavior is therefore dependent on these objects (S2.2-1, S2.2-2), and they are neither historical records nor a speed-only cache. MUST. This is runtime device-management state, not a user setting confined to an application.
Source: https://raw.githubusercontent.com/systemd/systemd/main/src/udev/udev-node.c
Exact quote: “This reads priority and device node from the symlink under /run/udev/links/ directory.”
The function stack_directory_find_prioritized_devnode selects among these candidates; link_search_and_update deletes the alias when no reference remains.
Hand-checked 10 groups against both raw type/target and the input members:
- flatcar-4c7805e498936e7ae1a37d41: /run/udev/links/cdrom; -100:/dev/sr0. All members are priority/device links; the multi-candidate group also fits.
- flatcar-bd0133edb221e27985df2227: /run/udev/links/disk\x2fby-designator\x2fesp; 0:/dev/vda1. All members are priority/device links; the multi-candidate group also fits.
- flatcar-10a0bb9519b190ffc2487d7d: /run/udev/links/disk\x2fby-id\x2fata-QEMU_DVD-ROM_QM00003; -100:/dev/sr0. All members are priority/device links; the multi-candidate group also fits.
- flatcar-8d598cebee188f04355c53a0: /run/udev/links/disk\x2fby-label\x2fEFI-SYSTEM; 0:/dev/vda1. All members are priority/device links; the multi-candidate group also fits.
- flatcar-bf1a27b86060d3ef4c7eb4fc: /run/udev/links/disk\x2fby-partlabel\x2froot-x86-64; 0:/dev/loop2p1, 0:/dev/loop7p1, 0:/dev/loop1p1, 0:/dev/loop3p1. All members are priority/device links; the multi-candidate group also fits.
- flatcar-5a6a824d018649210bec1e4f: /run/udev/links/disk\x2fby-path\x2fpci-0000:00:01.1-ata-2; -100:/dev/sr0. All members are priority/device links; the multi-candidate group also fits.
- flatcar-bd2da87ed0efb70dddab1085: /run/udev/links/disk\x2fby-uuid\x2f38565143-560c-4c39-8c57-658effcbfe8c; 0:/dev/loop1p2. All members are priority/device links; the multi-candidate group also fits.
- flatcar-bc6c22f3322ab9f6bac92165: /run/udev/links/input\x2fby-path\x2fplatform-i8042-serio-0-event-kbd; 0:/dev/input/event0. All members are priority/device links; the multi-candidate group also fits.
- flatcar-0d0039dc3b2bb330f490ad2a: /run/udev/links/mapper\x2floop1p1-45-verity; 0:/dev/dm-3. All members are priority/device links; the multi-candidate group also fits.
- flatcar-c189e7cb14a12c396c78de5f: /run/udev/links/rtc; -100:/dev/rtc0. All members are priority/device links; the multi-candidate group also fits.

## Rule K: empty-directory package markers
A group consisting entirely of .keep_* regular files contains package bookkeeping markers, not settings, executable code or device/access rules. Removing the marker alone leaves the directory and program functions intact. NOT (S2.2-2, S2.2-4).
Source: https://devmanual.gentoo.org/function-reference/install-functions/index.html
Exact quote: “This is accomplished by installing a hidden file prefixed with `.keep` to the directory in question.”
Hand-checked IDs below:
- flatcar-75eb1fe98f314da284effa3a: ["/etc/binfmt.d/.keep_sys-apps_systemd-0"]; raw records regular .keep files, with no other group members.
- flatcar-8a343b5a4d44aaa4822d1249: ["/etc/dbus-1/session.d/.keep_sys-apps_dbus-0"]; raw records regular .keep files, with no other group members.
- flatcar-c37ad6485aad0bfd3e16c136: ["/etc/dbus-1/system.d/.keep_sys-apps_dbus-0"]; raw records regular .keep files, with no other group members.
- flatcar-1a3c31d650cc1876ccc51362: ["/etc/kernel/install.d/.keep_sys-apps_systemd-0"]; raw records regular .keep files, with no other group members.
- flatcar-4aa44cbec033da59c6990315: ["/etc/lessfilter.d/.keep_sys-apps_less-0"]; raw records regular .keep files, with no other group members.
- flatcar-f69f27e0da9e77c1433fd5f1: ["/etc/modules-load.d/.keep_sys-apps_systemd-0"]; raw records regular .keep files, with no other group members.
- flatcar-0d03a9e02b07f43c129a7bb5: ["/etc/pam.d/.keep_sys-libs_pam-0"]; raw records regular .keep files, with no other group members.
- flatcar-e42a68dbfdaa8487079efbc9: ["/etc/polkit-1/rules.d/.keep_sys-auth_polkit-0"]; raw records regular .keep files, with no other group members.
- flatcar-cc0a6306432086897d0e99af: ["/etc/sasl2/.keep_dev-libs_cyrus-sasl-2"]; raw records regular .keep files, with no other group members.
- flatcar-2b3d55863d26e28bc1e9cdd3: ["/etc/security/.keep_sys-libs_pam-0"]; raw records regular .keep files, with no other group members.

### flatcar-01d1a51570df35156d65b6b7
Member numbers are one-based input-array positions. Behavioral trees are required; unused directory consumers are unestablished.
- 1: `/` — MUST
- 2: `/.systemd-etc-workdir` — MUST
- 3: `/boot` — MUST
- 4: `/etc` — MUST
- 5: `/home` — MUST
- 6: `/lost+found` — UNKNOWN
- 7: `/media` — UNKNOWN
- 8: `/mnt` — UNKNOWN
- 9: `/oem` — MUST
- 10: `/opt` — MUST
- 11: `/root` — UNKNOWN
- 12: `/run` — MUST
- 13: `/srv` — UNKNOWN
- 14: `/tmp` — MUST
- 15: `/var` — MUST

### flatcar-7955ed3fbebf581406d0ce57
Member numbers are one-based input-array positions. Account/code/system effects require recording; historical and display content do not; uncaptured settings remain unknown.
- 1: `/etc/.ignition-result.json` — NOT
- 2: `/etc/.pwd.lock` — UNKNOWN
- 3: `/etc/.systemd-confext` — MUST
- 4: `/etc/.updated` — UNKNOWN
- 5: `/etc/X11` — MUST
- 6: `/etc/audit` — MUST
- 7: `/etc/azure-ephemeral-disk-setup.conf` — UNKNOWN
- 8: `/etc/bash` — MUST
- 9: `/etc/bindresvport.blacklist` — UNKNOWN
- 10: `/etc/binfmt.d` — UNKNOWN
- 11: `/etc/cifs-utils` — UNKNOWN
- 12: `/etc/cni` — UNKNOWN
- 13: `/etc/conntrackd` — UNKNOWN
- 14: `/etc/coreos` — UNKNOWN
- 15: `/etc/credstore` — UNKNOWN
- 16: `/etc/credstore.encrypted` — UNKNOWN
- 17: `/etc/dbus-1` — MUST
- 18: `/etc/default` — MUST
- 19: `/etc/dracut.conf` — UNKNOWN
- 20: `/etc/e2scrub.conf` — UNKNOWN
- 21: `/etc/environment.d` — MUST
- 22: `/etc/ethertypes` — UNKNOWN
- 23: `/etc/extension-release.d` — MUST
- 24: `/etc/extensions` — MUST
- 25: `/etc/flatcar` — UNKNOWN
- 26: `/etc/group` — MUST
- 27: `/etc/group-` — NOT
- 28: `/etc/gshadow` — MUST
- 29: `/etc/gshadow-` — NOT
- 30: `/etc/hosts` — MUST
- 31: `/etc/idmapd.conf` — UNKNOWN
- 32: `/etc/init.d` — UNKNOWN
- 33: `/etc/iscsi` — UNKNOWN
- 34: `/etc/isns` — UNKNOWN
- 35: `/etc/issue` — NOT
- 36: `/etc/kernel` — MUST
- 37: `/etc/kexec.conf` — UNKNOWN
- 38: `/etc/keyutils` — UNKNOWN
- 39: `/etc/krb5.conf.example` — NOT
- 40: `/etc/ld.so.cache` — UNKNOWN
- 41: `/etc/ldap.conf.sudo` — UNKNOWN
- 42: `/etc/lessfilter.d` — UNKNOWN
- 43: `/etc/libaudit.conf` — UNKNOWN
- 44: `/etc/locale.conf` — MUST
- 45: `/etc/login.defs` — MUST
- 46: `/etc/logrotate.conf` — UNKNOWN
- 47: `/etc/logrotate.d` — UNKNOWN
- 48: `/etc/lvm` — UNKNOWN
- 49: `/etc/machine-id` — MUST
- 50: `/etc/mke2fs.conf` — UNKNOWN
- 51: `/etc/modules-load.d` — MUST
- 52: `/etc/motd` — NOT
- 53: `/etc/mtab` — UNKNOWN
- 54: `/etc/netconfig` — UNKNOWN
- 55: `/etc/nscd.conf` — UNKNOWN
- 56: `/etc/ntp.conf` — UNKNOWN
- 57: `/etc/nvme` — UNKNOWN
- 58: `/etc/openldap` — UNKNOWN
- 59: `/etc/pam.d` — UNKNOWN
- 60: `/etc/passwd` — MUST
- 61: `/etc/passwd-` — NOT
- 62: `/etc/pkcs11` — UNKNOWN
- 63: `/etc/polkit-1` — UNKNOWN
- 64: `/etc/profile.d` — MUST
- 65: `/etc/quotagrpadmins` — UNKNOWN
- 66: `/etc/quotatab` — UNKNOWN
- 67: `/etc/request-key.conf` — MUST
- 68: `/etc/request-key.d` — MUST
- 69: `/etc/resolv.conf` — MUST
- 70: `/etc/runlevels` — UNKNOWN
- 71: `/etc/sasl2` — UNKNOWN
- 72: `/etc/securetty` — MUST
- 73: `/etc/security` — MUST
- 74: `/etc/selinux` — MUST
- 75: `/etc/sestatus.conf` — UNKNOWN
- 76: `/etc/shadow` — UNKNOWN
- 77: `/etc/shadow-` — NOT
- 78: `/etc/skel` — MUST
- 79: `/etc/ssh` — MUST
- 80: `/etc/ssl` — MUST
- 81: `/etc/sssd` — MUST
- 82: `/etc/subgid` — MUST
- 83: `/etc/subgid-` — NOT
- 84: `/etc/subuid` — MUST
- 85: `/etc/subuid-` — NOT
- 86: `/etc/sudo_logsrvd.conf` — UNKNOWN
- 87: `/etc/sudoers.d` — MUST
- 88: `/etc/sudoers.dist` — UNKNOWN
- 89: `/etc/sysconfig` — UNKNOWN
- 90: `/etc/systemd` — MUST
- 91: `/etc/tcsd.conf` — UNKNOWN
- 92: `/etc/tmpfiles.d` — MUST
- 93: `/etc/tpm2-tss` — UNKNOWN
- 94: `/etc/udev` — MUST
- 95: `/etc/user` — UNKNOWN
- 96: `/etc/vim` — UNKNOWN
- 97: `/etc/warnquota.conf` — UNKNOWN
- 98: `/etc/whois.conf` — UNKNOWN
- 99: `/etc/wireguard` — UNKNOWN
- 100: `/etc/xattr.conf` — UNKNOWN
- 101: `/etc/xdg` — MUST

### flatcar-3e3328fa5aa3c0625e5e872a
Member numbers are one-based input-array positions. Marker is bookkeeping; audit rules alter kernel event collection.
- 1: `/etc/audit/rules.d/.keep_sys-process_audit-0` — NOT
- 2: `/etc/audit/rules.d/00-clear.rules` — MUST
- 3: `/etc/audit/rules.d/80-selinux.rules` — MUST
- 4: `/etc/audit/rules.d/99-default.rules` — MUST

### flatcar-bd2c4559f2056871a7ff8f03
Member numbers are one-based input-array positions. Bus rules govern multiple processes; marker-only subdirectories carry bookkeeping.
- 1: `/etc/dbus-1/session.conf` — MUST
- 2: `/etc/dbus-1/session.d` — NOT
- 3: `/etc/dbus-1/system.conf` — MUST
- 4: `/etc/dbus-1/system.d` — NOT

### flatcar-8ab92d58c9a88869f7e5408d
Member numbers are one-based input-array positions. Example is content; active-name configuration governs remote block-storage access.
- 1: `/etc/iscsi/initiatorname.iscsi.example` — NOT
- 2: `/etc/iscsi/iscsid.conf` — MUST

### flatcar-95f8a1273692407a1adfef04
Member numbers are one-based input-array positions. Marker is bookkeeping; rotation rules remove or rotate filesystem logs, beyond one program.
- 1: `/etc/logrotate.d/.keep_app-admin_logrotate-0` — NOT
- 2: `/etc/logrotate.d/iscsiuiolog` — MUST
- 3: `/etc/logrotate.d/qemu-guest-agent` — MUST
- 4: `/etc/logrotate.d/rsyncd` — MUST
- 5: `/etc/logrotate.d/sssd` — MUST

### flatcar-f9ff8d878016884d80dadb98
Member numbers are one-based input-array positions. Example is content; actual client defaults and their scope are unavailable.
- 1: `/etc/openldap/ldap.conf` — UNKNOWN
- 2: `/etc/openldap/ldap.conf.default` — NOT

### flatcar-67eb2395438dce162f6560f5
Member numbers are one-based input-array positions. Text mappings control security labels; compiled equivalents accelerate lookup.
- 1: `/etc/selinux/mcs/contexts/files/file_contexts` — MUST
- 2: `/etc/selinux/mcs/contexts/files/file_contexts.bin` — NOT
- 3: `/etc/selinux/mcs/contexts/files/file_contexts.homedirs` — MUST
- 4: `/etc/selinux/mcs/contexts/files/file_contexts.homedirs.bin` — NOT
- 5: `/etc/selinux/mcs/contexts/files/file_contexts.local` — MUST
- 6: `/etc/selinux/mcs/contexts/files/file_contexts.local.bin` — NOT
- 7: `/etc/selinux/mcs/contexts/files/file_contexts.subs_dist` — MUST
- 8: `/etc/selinux/mcs/contexts/files/media` — MUST

### flatcar-8e7f275dda3033c6764dbce1
Member numbers are one-based input-array positions. Text mappings control security labels; compiled equivalents accelerate lookup.
- 1: `/etc/selinux/mls/contexts/files/file_contexts` — MUST
- 2: `/etc/selinux/mls/contexts/files/file_contexts.bin` — NOT
- 3: `/etc/selinux/mls/contexts/files/file_contexts.homedirs` — MUST
- 4: `/etc/selinux/mls/contexts/files/file_contexts.homedirs.bin` — NOT
- 5: `/etc/selinux/mls/contexts/files/file_contexts.local` — MUST
- 6: `/etc/selinux/mls/contexts/files/file_contexts.local.bin` — NOT
- 7: `/etc/selinux/mls/contexts/files/file_contexts.subs_dist` — MUST
- 8: `/etc/selinux/mls/contexts/files/media` — MUST

### flatcar-fe7d9160ddf88a1ab47b648a
Member numbers are one-based input-array positions. Text mappings control security labels; compiled equivalents accelerate lookup.
- 1: `/etc/selinux/targeted/contexts/files/file_contexts` — MUST
- 2: `/etc/selinux/targeted/contexts/files/file_contexts.bin` — NOT
- 3: `/etc/selinux/targeted/contexts/files/file_contexts.homedirs` — MUST
- 4: `/etc/selinux/targeted/contexts/files/file_contexts.homedirs.bin` — NOT
- 5: `/etc/selinux/targeted/contexts/files/file_contexts.local` — MUST
- 6: `/etc/selinux/targeted/contexts/files/file_contexts.local.bin` — NOT
- 7: `/etc/selinux/targeted/contexts/files/file_contexts.subs_dist` — MUST
- 8: `/etc/selinux/targeted/contexts/files/media` — MUST

### flatcar-3546abab943996de0d498da5
Member numbers are one-based input-array positions. Marker is bookkeeping; binary policy controls system-wide access.
- 1: `/etc/selinux/mcs/policy/.keep_sec-policy_selinux-base-0` — NOT
- 2: `/etc/selinux/mcs/policy/policy.35` — MUST

### flatcar-2172ae44cbb0a923ab9ba6fb
Member numbers are one-based input-array positions. Marker is bookkeeping; binary policy controls system-wide access.
- 1: `/etc/selinux/mls/policy/.keep_sec-policy_selinux-base-0` — NOT
- 2: `/etc/selinux/mls/policy/policy.35` — MUST

### flatcar-19aaf19227695fbd77af5cca
Member numbers are one-based input-array positions. Marker is bookkeeping; binary policy controls system-wide access.
- 1: `/etc/selinux/targeted/policy/.keep_sec-policy_selinux-base-0` — NOT
- 2: `/etc/selinux/targeted/policy/policy.35` — MUST

### flatcar-fc09a47fdb5636cbf6b1fb22
Member numbers are one-based input-array positions. Client defaults remain inside SSH; host authentication and server access enable login.
- 1: `/etc/ssh/moduli` — MUST
- 2: `/etc/ssh/ssh_config` — NOT
- 3: `/etc/ssh/ssh_config.d` — NOT
- 4: `/etc/ssh/ssh_host_ecdsa_key` — MUST
- 5: `/etc/ssh/ssh_host_ecdsa_key.pub` — MUST
- 6: `/etc/ssh/ssh_host_ed25519_key` — MUST
- 7: `/etc/ssh/ssh_host_ed25519_key.pub` — MUST
- 8: `/etc/ssh/ssh_host_mldsa44_ed25519_key` — MUST
- 9: `/etc/ssh/ssh_host_mldsa44_ed25519_key.pub` — MUST
- 10: `/etc/ssh/ssh_host_rsa_key` — MUST
- 11: `/etc/ssh/ssh_host_rsa_key.pub` — MUST
- 12: `/etc/ssh/ssh_revoked_hosts` — MUST
- 13: `/etc/ssh/sshd_config` — MUST
- 14: `/etc/ssh/sshd_config.d` — MUST

### flatcar-b3531e524e85d4c2cc907fb8
Member numbers are one-based input-array positions. Markers/examples are content; SSSD configuration governs system identity and authentication.
- 1: `/etc/sssd/conf.d` — NOT
- 2: `/etc/sssd/pki` — NOT
- 3: `/etc/sssd/sssd-example.conf` — NOT
- 4: `/etc/sssd/sssd.conf` — MUST

### flatcar-1dbf7846e77a20c7624142e9
Member numbers are one-based input-array positions. Marker is bookkeeping; wants-directory links control service timer activation.
- 1: `/etc/systemd/system/.keep_sys-apps_systemd-0` — NOT
- 2: `/etc/systemd/system/timers.target.wants` — MUST

### flatcar-776158c873d0ec65315d36b4
Member numbers are one-based input-array positions. Hardware properties affect devices; markers are bookkeeping; uncaptured configuration values remain unknown.
- 1: `/etc/udev/hwdb.bin` — MUST
- 2: `/etc/udev/hwdb.d` — NOT
- 3: `/etc/udev/iocost.conf` — UNKNOWN
- 4: `/etc/udev/rules.d` — NOT
- 5: `/etc/udev/udev.conf` — UNKNOWN

### flatcar-68768e2b26f1fba2d8bcc15a
Member numbers are one-based input-array positions. Startup code and login keys require recording; empty home-directory dependency is unestablished.
- 1: `/home/core` — UNKNOWN
- 2: `/home/user` — MUST

### flatcar-47598385be793e3487e3ae2f
Member numbers are one-based input-array positions. Startup code and login keys are required; lock behavior is not established.
- 1: `/home/user/.authorized_keys.d.lock` — UNKNOWN
- 2: `/home/user/.bash_logout` — MUST
- 3: `/home/user/.bash_profile` — MUST
- 4: `/home/user/.bashrc` — MUST
- 5: `/home/user/.ssh` — MUST

### flatcar-7976e0ab6cbbb8450088916a
Member numbers are one-based input-array positions. Old copy records past authorization; current key files enable account login.
- 1: `/home/user/.ssh/.authorized_keys.d.old` — NOT
- 2: `/home/user/.ssh/authorized_keys` — MUST
- 3: `/home/user/.ssh/authorized_keys.d` — MUST

### flatcar-025b74d903a537ca1a129ee2
Member numbers are one-based input-array positions. Boot rules/extensions alter execution; release text identifies content.
- 1: `/oem/grub.cfg` — MUST
- 2: `/oem/oem-release` — NOT
- 3: `/oem/sysext` — MUST

### flatcar-8d354bdc3e8042522678923e
Member numbers are one-based input-array positions. Live endpoints/rules affect interprocess behavior; caches/content/history are exempt; other runtime uses are unestablished.
- 1: `/run/blkid` — NOT
- 2: `/run/containerd` — MUST
- 3: `/run/coreos` — NOT
- 4: `/run/credentials` — UNKNOWN
- 5: `/run/cryptsetup` — UNKNOWN
- 6: `/run/dbus` — MUST
- 7: `/run/docker` — MUST
- 8: `/run/docker.pid` — UNKNOWN
- 9: `/run/docker.sock` — MUST
- 10: `/run/faillock` — UNKNOWN
- 11: `/run/flatcar` — NOT
- 12: `/run/fsck` — UNKNOWN
- 13: `/run/ignition.env` — UNKNOWN
- 14: `/run/initramfs` — UNKNOWN
- 15: `/run/issue` — NOT
- 16: `/run/issue.d` — NOT
- 17: `/run/lock` — UNKNOWN
- 18: `/run/log` — NOT
- 19: `/run/lvm` — UNKNOWN
- 20: `/run/mdadm` — UNKNOWN
- 21: `/run/modprobe.d` — UNKNOWN
- 22: `/run/mount` — UNKNOWN
- 23: `/run/multipath` — UNKNOWN
- 24: `/run/nri` — MUST
- 25: `/run/nscd` — UNKNOWN
- 26: `/run/saslauthd` — UNKNOWN
- 27: `/run/ssh-unix-local` — MUST
- 28: `/run/sshd` — UNKNOWN
- 29: `/run/sssd` — UNKNOWN
- 30: `/run/sudo` — UNKNOWN
- 31: `/run/systemd` — MUST
- 32: `/run/tmpfiles.d` — MUST
- 33: `/run/tpm2-tss` — UNKNOWN
- 34: `/run/udev` — MUST
- 35: `/run/update-engine` — UNKNOWN
- 36: `/run/user` — MUST
- 37: `/run/utmp` — NOT
- 38: `/run/varlink` — MUST
- 39: `/run/xtables.lock` — UNKNOWN

### flatcar-0a2f5f184ea0098c30af81ef
Member numbers are one-based input-array positions. Sockets enable IPC; directory contents and actual database effects are not captured.
- 1: `/run/containerd/containerd.sock` — MUST
- 2: `/run/containerd/containerd.sock.ttrpc` — MUST
- 3: `/run/containerd/io.containerd.grpc.v1.cri` — UNKNOWN
- 4: `/run/containerd/io.containerd.mount-manager.v1.bolt` — UNKNOWN
- 5: `/run/containerd/io.containerd.runtime.v2.task` — UNKNOWN
- 6: `/run/containerd/io.containerd.sandbox.controller.v1.shim` — UNKNOWN

### flatcar-cc7f234ea5320af7c211fb4a
Member numbers are one-based input-array positions. IPC paths enable interprocess functions; empty plugin-directory dependence is unknown.
- 1: `/run/docker/libcontainerd` — MUST
- 2: `/run/docker/libnetwork` — MUST
- 3: `/run/docker/metrics.sock` — MUST
- 4: `/run/docker/plugins` — UNKNOWN

### flatcar-591f3f4c191b1e17b6e0632f
Member numbers are one-based input-array positions. Past logs are exempt; actual uses of other retained directories are unknown.
- 1: `/run/initramfs/cmdline.d` — UNKNOWN
- 2: `/run/initramfs/log` — NOT
- 3: `/run/initramfs/systemd` — UNKNOWN

### flatcar-7db1d507b1da0e5b91f46577
Member numbers are one-based input-array positions. Sockets and unit rules enable system behavior; identification content is exempt; other state consumers remain unknown.
- 1: `/run/systemd/ask-password` — UNKNOWN
- 2: `/run/systemd/coredump` — MUST
- 3: `/run/systemd/default-hostname` — NOT
- 4: `/run/systemd/dissect-root` — UNKNOWN
- 5: `/run/systemd/generator` — MUST
- 6: `/run/systemd/generator.late` — MUST
- 7: `/run/systemd/inaccessible` — MUST
- 8: `/run/systemd/inhibit` — UNKNOWN
- 9: `/run/systemd/io.systemd.AskPassword` — MUST
- 10: `/run/systemd/io.systemd.Credentials` — MUST
- 11: `/run/systemd/io.systemd.FactoryReset` — MUST
- 12: `/run/systemd/io.systemd.Hostname` — MUST
- 13: `/run/systemd/io.systemd.Import` — MUST
- 14: `/run/systemd/io.systemd.JournalAccess` — MUST
- 15: `/run/systemd/io.systemd.Login` — MUST
- 16: `/run/systemd/io.systemd.ManagedOOM` — MUST
- 17: `/run/systemd/io.systemd.Manager` — MUST
- 18: `/run/systemd/io.systemd.MountFileSystem` — MUST
- 19: `/run/systemd/io.systemd.MuteConsole` — MUST
- 20: `/run/systemd/io.systemd.NamespaceResource` — MUST
- 21: `/run/systemd/io.systemd.Repart` — MUST
- 22: `/run/systemd/io.systemd.sysext` — MUST
- 23: `/run/systemd/journal` — MUST
- 24: `/run/systemd/machine` — MUST
- 25: `/run/systemd/machines` — UNKNOWN
- 26: `/run/systemd/mount-rootfs` — UNKNOWN
- 27: `/run/systemd/netif` — MUST
- 28: `/run/systemd/network` — MUST
- 29: `/run/systemd/notify` — MUST
- 30: `/run/systemd/nspawn` — UNKNOWN
- 31: `/run/systemd/nsresource` — UNKNOWN
- 32: `/run/systemd/oom` — MUST
- 33: `/run/systemd/private` — MUST
- 34: `/run/systemd/propagate` — NOT
- 35: `/run/systemd/report` — MUST
- 36: `/run/systemd/resolve` — MUST
- 37: `/run/systemd/resolve.hook` — MUST
- 38: `/run/systemd/seats` — UNKNOWN
- 39: `/run/systemd/sessions` — UNKNOWN
- 40: `/run/systemd/show-status` — UNKNOWN
- 41: `/run/systemd/shutdown` — UNKNOWN
- 42: `/run/systemd/sysext` — UNKNOWN
- 43: `/run/systemd/system` — UNKNOWN
- 44: `/run/systemd/systemd-units-load` — UNKNOWN
- 45: `/run/systemd/timesync` — UNKNOWN
- 46: `/run/systemd/transient` — MUST
- 47: `/run/systemd/units` — UNKNOWN
- 48: `/run/systemd/userdb` — MUST
- 49: `/run/systemd/users` — UNKNOWN

### flatcar-27ab5a6b2bcd37afb4af1e52
Member numbers are one-based input-array positions. Sockets enable logging IPC; sequence/stream-state contents and consumers are not fully established.
- 1: `/run/systemd/journal/dev-log` — MUST
- 2: `/run/systemd/journal/flushed` — UNKNOWN
- 3: `/run/systemd/journal/io.systemd.journal` — MUST
- 4: `/run/systemd/journal/kernel-seqnum` — UNKNOWN
- 5: `/run/systemd/journal/seqnum` — UNKNOWN
- 6: `/run/systemd/journal/socket` — MUST
- 7: `/run/systemd/journal/stdout` — MUST
- 8: `/run/systemd/journal/streams` — UNKNOWN

### flatcar-96a67fde1ac33b125a79bea0
Member numbers are one-based input-array positions. IPC and current network state serve other programs; empty server-lease-directory use is unknown.
- 1: `/run/systemd/netif/dhcp-server-lease` — UNKNOWN
- 2: `/run/systemd/netif/io.systemd.Network` — MUST
- 3: `/run/systemd/netif/leases` — MUST
- 4: `/run/systemd/netif/links` — MUST
- 5: `/run/systemd/netif/state` — MUST

### flatcar-ace9f82cde7b45781f45ea71
Member numbers are one-based input-array positions. IPC and device metadata support system access; empty lock/rule-directory dependencies are unknown.
- 1: `/run/udev/control` — MUST
- 2: `/run/udev/data` — MUST
- 3: `/run/udev/io.systemd.Udev` — MUST
- 4: `/run/udev/links` — MUST
- 5: `/run/udev/links.lock` — UNKNOWN
- 6: `/run/udev/rules.d` — UNKNOWN
- 7: `/run/udev/tags` — MUST
- 8: `/run/udev/watch` — MUST

### flatcar-9b9193a7e1c17f5ead59b1aa
Member numbers are one-based input-array positions. Active IPC enables programs to communicate; empty users directory dependencies are not established.
- 1: `/run/user/1000` — MUST
- 2: `/run/user/500` — UNKNOWN

### flatcar-c0a30ba689b29442ff194133
Member numbers are one-based input-array positions. IPC/sandbox nodes affect other processes; release text is content; invocation consumer behavior remains unestablished.
- 1: `/run/user/1000/systemd/inaccessible` — MUST
- 2: `/run/user/1000/systemd/io.systemd.AskPassword` — MUST
- 3: `/run/user/1000/systemd/io.systemd.Import` — MUST
- 4: `/run/user/1000/systemd/io.systemd.JournalAccess` — MUST
- 5: `/run/user/1000/systemd/io.systemd.Manager` — MUST
- 6: `/run/user/1000/systemd/machine` — MUST
- 7: `/run/user/1000/systemd/notify` — MUST
- 8: `/run/user/1000/systemd/private` — MUST
- 9: `/run/user/1000/systemd/propagate` — NOT
- 10: `/run/user/1000/systemd/report` — MUST
- 11: `/run/user/1000/systemd/units` — UNKNOWN

### flatcar-e8bc19ab63b2f5950a9671af
Member numbers are one-based input-array positions. Private directories back process isolation; empty display-server directory consumers are unestablished.
- 1: `/tmp/.ICE-unix` — UNKNOWN
- 2: `/tmp/.X11-unix` — UNKNOWN
- 3: `/tmp/.XIM-unix` — UNKNOWN
- 4: `/tmp/.font-unix` — UNKNOWN
- 5: `/tmp/systemd-private-399ee384a85947e5802aa24624a28b03-polkit.service-b91ISC` — MUST
- 6: `/tmp/systemd-private-399ee384a85947e5802aa24624a28b03-systemd-logind.service-dAxW1L` — MUST

### flatcar-b5baa09f5c3f8794557bf857
Member numbers are one-based input-array positions. Runtime/service dependencies require recording; cache/log stores are exempt; remaining directory consumers are unestablished.
- 1: `/var/.updated` — UNKNOWN
- 2: `/var/cache` — NOT
- 3: `/var/db` — UNKNOWN
- 4: `/var/empty` — UNKNOWN
- 5: `/var/kubernetes` — UNKNOWN
- 6: `/var/lib` — MUST
- 7: `/var/lock` — MUST
- 8: `/var/log` — NOT
- 9: `/var/run` — MUST
- 10: `/var/spool` — UNKNOWN
- 11: `/var/tmp` — MUST

### flatcar-7a63c430cdc959f1b261bfa0
Member numbers are one-based input-array positions. Auxiliary linker cache only accelerates rebuilding; private directory dependency is unestablished.
- 1: `/var/cache/ldconfig` — NOT
- 2: `/var/cache/private` — UNKNOWN

### flatcar-f91c1f2c90de95c5b942a889
Member numbers are one-based input-array positions. Configuration/identity aliases serve programs; cache storage is exempt; actual state contents and other directory dependencies are unavailable.
- 1: `/var/lib/cache` — NOT
- 2: `/var/lib/containerd` — UNKNOWN
- 3: `/var/lib/dbus` — MUST
- 4: `/var/lib/docker` — UNKNOWN
- 5: `/var/lib/etcd` — UNKNOWN
- 6: `/var/lib/extensions.mutable` — MUST
- 7: `/var/lib/ip6tables` — UNKNOWN
- 8: `/var/lib/ipset` — UNKNOWN
- 9: `/var/lib/iptables` — UNKNOWN
- 10: `/var/lib/iscsi` — UNKNOWN
- 11: `/var/lib/isns` — UNKNOWN
- 12: `/var/lib/krb5kdc` — UNKNOWN
- 13: `/var/lib/lib` — UNKNOWN
- 14: `/var/lib/machines` — UNKNOWN
- 15: `/var/lib/misc` — UNKNOWN
- 16: `/var/lib/nfs` — UNKNOWN
- 17: `/var/lib/nftables` — UNKNOWN
- 18: `/var/lib/ntp` — UNKNOWN
- 19: `/var/lib/polkit-1` — UNKNOWN
- 20: `/var/lib/portables` — UNKNOWN
- 21: `/var/lib/private` — UNKNOWN
- 22: `/var/lib/sss` — UNKNOWN
- 23: `/var/lib/systemd` — UNKNOWN
- 24: `/var/lib/tpm` — UNKNOWN
- 25: `/var/lib/tpm2-tss` — UNKNOWN

### flatcar-ff709a51aa4d7980d98fc060
Member numbers are one-based input-array positions. Cache/history are exempt; other databases lack contents establishing their actual effects.
- 1: `/var/lib/docker/buildkit/cache.db` — NOT
- 2: `/var/lib/docker/buildkit/containerdmeta.db` — UNKNOWN
- 3: `/var/lib/docker/buildkit/executor` — UNKNOWN
- 4: `/var/lib/docker/buildkit/history.db` — NOT
- 5: `/var/lib/docker/buildkit/metadata_v2.db` — UNKNOWN
- 6: `/var/lib/docker/buildkit/snapshots.db` — UNKNOWN

### flatcar-186acdd6733c226cced3c6d3
Member numbers are one-based input-array positions. Block node provides storage access; volume database contents and actual effects remain unknown.
- 1: `/var/lib/docker/volumes/backingFsBlockDev` — MUST
- 2: `/var/lib/docker/volumes/metadata.db` — UNKNOWN

### flatcar-d11cff71d6ec6e8beafbf4e9
Member numbers are one-based input-array positions. Timing records both describe past events and affect future actions; remaining states have distinct functions.
- 1: `/var/lib/systemd/catalog` — NOT
- 2: `/var/lib/systemd/coredump` — NOT
- 3: `/var/lib/systemd/ephemeral-trees` — UNKNOWN
- 4: `/var/lib/systemd/linger` — UNKNOWN
- 5: `/var/lib/systemd/network` — UNKNOWN
- 6: `/var/lib/systemd/pstore` — NOT
- 7: `/var/lib/systemd/random-seed` — MUST
- 8: `/var/lib/systemd/timers` — HOLE
- 9: `/var/lib/systemd/timesync` — HOLE

### Correction flatcar-b63a60e710980988400f52f9
MUST → MIXED. Modules execute; separate memdisk/configuration inputs lack established later consumers.
Corrected complete member map (supersedes earlier map):
- 1: `/boot/flatcar/grub/grub.cfg.tar` — UNKNOWN
- 2: `/boot/flatcar/grub/i386-pc` — MUST
- 3: `/boot/flatcar/grub/x86_64-efi` — UNKNOWN
- 4: `/boot/flatcar/grub/x86_64-xen` — MUST

### Correction flatcar-aa489ee21d27f0b113d367ca
MUST → MIXED. Code requires recording; indexes/history have exemption conflicts; construction inputs lack established later consumers.
Corrected complete member map (supersedes earlier map):
- 1: `/boot/flatcar/grub/i386-pc/acpi.mod` — MUST
- 2: `/boot/flatcar/grub/i386-pc/adler32.mod` — MUST
- 3: `/boot/flatcar/grub/i386-pc/affs.mod` — MUST
- 4: `/boot/flatcar/grub/i386-pc/afs.mod` — MUST
- 5: `/boot/flatcar/grub/i386-pc/afsplitter.mod` — MUST
- 6: `/boot/flatcar/grub/i386-pc/ahci.mod` — MUST
- 7: `/boot/flatcar/grub/i386-pc/all_video.mod` — MUST
- 8: `/boot/flatcar/grub/i386-pc/aout.mod` — MUST
- 9: `/boot/flatcar/grub/i386-pc/appendedsig.mod` — MUST
- 10: `/boot/flatcar/grub/i386-pc/archelp.mod` — MUST
- 11: `/boot/flatcar/grub/i386-pc/asn1.mod` — MUST
- 12: `/boot/flatcar/grub/i386-pc/at_keyboard.mod` — MUST
- 13: `/boot/flatcar/grub/i386-pc/ata.mod` — MUST
- 14: `/boot/flatcar/grub/i386-pc/backtrace.mod` — MUST
- 15: `/boot/flatcar/grub/i386-pc/bfs.mod` — MUST
- 16: `/boot/flatcar/grub/i386-pc/bitmap.mod` — MUST
- 17: `/boot/flatcar/grub/i386-pc/bitmap_scale.mod` — MUST
- 18: `/boot/flatcar/grub/i386-pc/blocklist.mod` — MUST
- 19: `/boot/flatcar/grub/i386-pc/blscfg.mod` — MUST
- 20: `/boot/flatcar/grub/i386-pc/boot.img` — UNKNOWN
- 21: `/boot/flatcar/grub/i386-pc/boot.mod` — MUST
- 22: `/boot/flatcar/grub/i386-pc/bsd.mod` — MUST
- 23: `/boot/flatcar/grub/i386-pc/bufio.mod` — MUST
- 24: `/boot/flatcar/grub/i386-pc/cat.mod` — MUST
- 25: `/boot/flatcar/grub/i386-pc/cbfs.mod` — MUST
- 26: `/boot/flatcar/grub/i386-pc/cbls.mod` — MUST
- 27: `/boot/flatcar/grub/i386-pc/cbmemc.mod` — MUST
- 28: `/boot/flatcar/grub/i386-pc/cbtable.mod` — MUST
- 29: `/boot/flatcar/grub/i386-pc/cbtime.mod` — MUST
- 30: `/boot/flatcar/grub/i386-pc/chain.mod` — MUST
- 31: `/boot/flatcar/grub/i386-pc/cmosdump.mod` — MUST
- 32: `/boot/flatcar/grub/i386-pc/cmostest.mod` — MUST
- 33: `/boot/flatcar/grub/i386-pc/cmp.mod` — MUST
- 34: `/boot/flatcar/grub/i386-pc/command.lst` — HOLE
- 35: `/boot/flatcar/grub/i386-pc/core.img` — MUST
- 36: `/boot/flatcar/grub/i386-pc/cpio.mod` — MUST
- 37: `/boot/flatcar/grub/i386-pc/cpio_be.mod` — MUST
- 38: `/boot/flatcar/grub/i386-pc/cpuid.mod` — MUST
- 39: `/boot/flatcar/grub/i386-pc/crc64.mod` — MUST
- 40: `/boot/flatcar/grub/i386-pc/crypto.lst` — HOLE
- 41: `/boot/flatcar/grub/i386-pc/crypto.mod` — MUST
- 42: `/boot/flatcar/grub/i386-pc/cryptodisk.mod` — MUST
- 43: `/boot/flatcar/grub/i386-pc/cs5536.mod` — MUST
- 44: `/boot/flatcar/grub/i386-pc/date.mod` — MUST
- 45: `/boot/flatcar/grub/i386-pc/datehook.mod` — MUST
- 46: `/boot/flatcar/grub/i386-pc/datetime.mod` — MUST
- 47: `/boot/flatcar/grub/i386-pc/disk.mod` — MUST
- 48: `/boot/flatcar/grub/i386-pc/diskfilter.mod` — MUST
- 49: `/boot/flatcar/grub/i386-pc/div.mod` — MUST
- 50: `/boot/flatcar/grub/i386-pc/dm_nv.mod` — MUST
- 51: `/boot/flatcar/grub/i386-pc/drivemap.mod` — MUST
- 52: `/boot/flatcar/grub/i386-pc/efiemu.mod` — MUST
- 53: `/boot/flatcar/grub/i386-pc/ehci.mod` — MUST
- 54: `/boot/flatcar/grub/i386-pc/elf.mod` — MUST
- 55: `/boot/flatcar/grub/i386-pc/eval.mod` — MUST
- 56: `/boot/flatcar/grub/i386-pc/exfat.mod` — MUST
- 57: `/boot/flatcar/grub/i386-pc/ext2.mod` — MUST
- 58: `/boot/flatcar/grub/i386-pc/extcmd.mod` — MUST
- 59: `/boot/flatcar/grub/i386-pc/f2fs.mod` — MUST
- 60: `/boot/flatcar/grub/i386-pc/fdt.lst` — HOLE
- 61: `/boot/flatcar/grub/i386-pc/file.mod` — MUST
- 62: `/boot/flatcar/grub/i386-pc/font.mod` — MUST
- 63: `/boot/flatcar/grub/i386-pc/freedos.mod` — MUST
- 64: `/boot/flatcar/grub/i386-pc/fs.lst` — HOLE
- 65: `/boot/flatcar/grub/i386-pc/fshelp.mod` — MUST
- 66: `/boot/flatcar/grub/i386-pc/gcry_arcfour.mod` — MUST
- 67: `/boot/flatcar/grub/i386-pc/gcry_blowfish.mod` — MUST
- 68: `/boot/flatcar/grub/i386-pc/gcry_camellia.mod` — MUST
- 69: `/boot/flatcar/grub/i386-pc/gcry_cast5.mod` — MUST
- 70: `/boot/flatcar/grub/i386-pc/gcry_crc.mod` — MUST
- 71: `/boot/flatcar/grub/i386-pc/gcry_des.mod` — MUST
- 72: `/boot/flatcar/grub/i386-pc/gcry_dsa.mod` — MUST
- 73: `/boot/flatcar/grub/i386-pc/gcry_idea.mod` — MUST
- 74: `/boot/flatcar/grub/i386-pc/gcry_md4.mod` — MUST
- 75: `/boot/flatcar/grub/i386-pc/gcry_md5.mod` — MUST
- 76: `/boot/flatcar/grub/i386-pc/gcry_rfc2268.mod` — MUST
- 77: `/boot/flatcar/grub/i386-pc/gcry_rijndael.mod` — MUST
- 78: `/boot/flatcar/grub/i386-pc/gcry_rmd160.mod` — MUST
- 79: `/boot/flatcar/grub/i386-pc/gcry_rsa.mod` — MUST
- 80: `/boot/flatcar/grub/i386-pc/gcry_seed.mod` — MUST
- 81: `/boot/flatcar/grub/i386-pc/gcry_serpent.mod` — MUST
- 82: `/boot/flatcar/grub/i386-pc/gcry_sha1.mod` — MUST
- 83: `/boot/flatcar/grub/i386-pc/gcry_sha256.mod` — MUST
- 84: `/boot/flatcar/grub/i386-pc/gcry_sha512.mod` — MUST
- 85: `/boot/flatcar/grub/i386-pc/gcry_tiger.mod` — MUST
- 86: `/boot/flatcar/grub/i386-pc/gcry_twofish.mod` — MUST
- 87: `/boot/flatcar/grub/i386-pc/gcry_whirlpool.mod` — MUST
- 88: `/boot/flatcar/grub/i386-pc/gdb.mod` — MUST
- 89: `/boot/flatcar/grub/i386-pc/geli.mod` — MUST
- 90: `/boot/flatcar/grub/i386-pc/gettext.mod` — MUST
- 91: `/boot/flatcar/grub/i386-pc/gfxmenu.mod` — MUST
- 92: `/boot/flatcar/grub/i386-pc/gfxterm.mod` — MUST
- 93: `/boot/flatcar/grub/i386-pc/gfxterm_background.mod` — MUST
- 94: `/boot/flatcar/grub/i386-pc/gpt.mod` — MUST
- 95: `/boot/flatcar/grub/i386-pc/gptrepair.mod` — MUST
- 96: `/boot/flatcar/grub/i386-pc/gptsync.mod` — MUST
- 97: `/boot/flatcar/grub/i386-pc/gzio.mod` — MUST
- 98: `/boot/flatcar/grub/i386-pc/halt.mod` — MUST
- 99: `/boot/flatcar/grub/i386-pc/hashsum.mod` — MUST
- 100: `/boot/flatcar/grub/i386-pc/hdparm.mod` — MUST
- 101: `/boot/flatcar/grub/i386-pc/hello.mod` — MUST
- 102: `/boot/flatcar/grub/i386-pc/help.mod` — MUST
- 103: `/boot/flatcar/grub/i386-pc/hexdump.mod` — MUST
- 104: `/boot/flatcar/grub/i386-pc/hfs.mod` — MUST
- 105: `/boot/flatcar/grub/i386-pc/hfsplus.mod` — MUST
- 106: `/boot/flatcar/grub/i386-pc/hfspluscomp.mod` — MUST
- 107: `/boot/flatcar/grub/i386-pc/http.mod` — MUST
- 108: `/boot/flatcar/grub/i386-pc/increment.mod` — MUST
- 109: `/boot/flatcar/grub/i386-pc/iorw.mod` — MUST
- 110: `/boot/flatcar/grub/i386-pc/iso9660.mod` — MUST
- 111: `/boot/flatcar/grub/i386-pc/jfs.mod` — MUST
- 112: `/boot/flatcar/grub/i386-pc/jpeg.mod` — MUST
- 113: `/boot/flatcar/grub/i386-pc/json.mod` — MUST
- 114: `/boot/flatcar/grub/i386-pc/keylayouts.mod` — MUST
- 115: `/boot/flatcar/grub/i386-pc/keystatus.mod` — MUST
- 116: `/boot/flatcar/grub/i386-pc/ldm.mod` — MUST
- 117: `/boot/flatcar/grub/i386-pc/legacycfg.mod` — MUST
- 118: `/boot/flatcar/grub/i386-pc/linux.mod` — MUST
- 119: `/boot/flatcar/grub/i386-pc/load.cfg` — UNKNOWN
- 120: `/boot/flatcar/grub/i386-pc/loadenv.mod` — MUST
- 121: `/boot/flatcar/grub/i386-pc/loopback.mod` — MUST
- 122: `/boot/flatcar/grub/i386-pc/ls.mod` — MUST
- 123: `/boot/flatcar/grub/i386-pc/lsacpi.mod` — MUST
- 124: `/boot/flatcar/grub/i386-pc/lsapm.mod` — MUST
- 125: `/boot/flatcar/grub/i386-pc/lsmmap.mod` — MUST
- 126: `/boot/flatcar/grub/i386-pc/lspci.mod` — MUST
- 127: `/boot/flatcar/grub/i386-pc/luks.mod` — MUST
- 128: `/boot/flatcar/grub/i386-pc/luks2.mod` — MUST
- 129: `/boot/flatcar/grub/i386-pc/lvm.mod` — MUST
- 130: `/boot/flatcar/grub/i386-pc/lzopio.mod` — MUST
- 131: `/boot/flatcar/grub/i386-pc/macbless.mod` — MUST
- 132: `/boot/flatcar/grub/i386-pc/macho.mod` — MUST
- 133: `/boot/flatcar/grub/i386-pc/mbr.bin` — HOLE
- 134: `/boot/flatcar/grub/i386-pc/mda_text.mod` — MUST
- 135: `/boot/flatcar/grub/i386-pc/mdraid09.mod` — MUST
- 136: `/boot/flatcar/grub/i386-pc/mdraid09_be.mod` — MUST
- 137: `/boot/flatcar/grub/i386-pc/mdraid1x.mod` — MUST
- 138: `/boot/flatcar/grub/i386-pc/memrw.mod` — MUST
- 139: `/boot/flatcar/grub/i386-pc/minicmd.mod` — MUST
- 140: `/boot/flatcar/grub/i386-pc/minix.mod` — MUST
- 141: `/boot/flatcar/grub/i386-pc/minix2.mod` — MUST
- 142: `/boot/flatcar/grub/i386-pc/minix2_be.mod` — MUST
- 143: `/boot/flatcar/grub/i386-pc/minix3.mod` — MUST
- 144: `/boot/flatcar/grub/i386-pc/minix3_be.mod` — MUST
- 145: `/boot/flatcar/grub/i386-pc/minix_be.mod` — MUST
- 146: `/boot/flatcar/grub/i386-pc/mmap.mod` — MUST
- 147: `/boot/flatcar/grub/i386-pc/moddep.lst` — HOLE
- 148: `/boot/flatcar/grub/i386-pc/morse.mod` — MUST
- 149: `/boot/flatcar/grub/i386-pc/mpi.mod` — MUST
- 150: `/boot/flatcar/grub/i386-pc/msdospart.mod` — MUST
- 151: `/boot/flatcar/grub/i386-pc/multiboot.mod` — MUST
- 152: `/boot/flatcar/grub/i386-pc/multiboot2.mod` — MUST
- 153: `/boot/flatcar/grub/i386-pc/nativedisk.mod` — MUST
- 154: `/boot/flatcar/grub/i386-pc/net.mod` — MUST
- 155: `/boot/flatcar/grub/i386-pc/newc.mod` — MUST
- 156: `/boot/flatcar/grub/i386-pc/nilfs2.mod` — MUST
- 157: `/boot/flatcar/grub/i386-pc/ntfs.mod` — MUST
- 158: `/boot/flatcar/grub/i386-pc/ntfscomp.mod` — MUST
- 159: `/boot/flatcar/grub/i386-pc/ntldr.mod` — MUST
- 160: `/boot/flatcar/grub/i386-pc/odc.mod` — MUST
- 161: `/boot/flatcar/grub/i386-pc/offsetio.mod` — MUST
- 162: `/boot/flatcar/grub/i386-pc/ohci.mod` — MUST
- 163: `/boot/flatcar/grub/i386-pc/part_acorn.mod` — MUST
- 164: `/boot/flatcar/grub/i386-pc/part_amiga.mod` — MUST
- 165: `/boot/flatcar/grub/i386-pc/part_apple.mod` — MUST
- 166: `/boot/flatcar/grub/i386-pc/part_bsd.mod` — MUST
- 167: `/boot/flatcar/grub/i386-pc/part_dfly.mod` — MUST
- 168: `/boot/flatcar/grub/i386-pc/part_dvh.mod` — MUST
- 169: `/boot/flatcar/grub/i386-pc/part_msdos.mod` — MUST
- 170: `/boot/flatcar/grub/i386-pc/part_plan.mod` — MUST
- 171: `/boot/flatcar/grub/i386-pc/part_sun.mod` — MUST
- 172: `/boot/flatcar/grub/i386-pc/part_sunpc.mod` — MUST
- 173: `/boot/flatcar/grub/i386-pc/partmap.lst` — HOLE
- 174: `/boot/flatcar/grub/i386-pc/parttool.lst` — HOLE
- 175: `/boot/flatcar/grub/i386-pc/parttool.mod` — MUST
- 176: `/boot/flatcar/grub/i386-pc/password.mod` — MUST
- 177: `/boot/flatcar/grub/i386-pc/password_pbkdf2.mod` — MUST
- 178: `/boot/flatcar/grub/i386-pc/pata.mod` — MUST
- 179: `/boot/flatcar/grub/i386-pc/pbkdf2.mod` — MUST
- 180: `/boot/flatcar/grub/i386-pc/pci.mod` — MUST
- 181: `/boot/flatcar/grub/i386-pc/pcidump.mod` — MUST
- 182: `/boot/flatcar/grub/i386-pc/pgp.mod` — MUST
- 183: `/boot/flatcar/grub/i386-pc/pkcs1_v15.mod` — MUST
- 184: `/boot/flatcar/grub/i386-pc/plainmount.mod` — MUST
- 185: `/boot/flatcar/grub/i386-pc/plan9.mod` — MUST
- 186: `/boot/flatcar/grub/i386-pc/play.mod` — MUST
- 187: `/boot/flatcar/grub/i386-pc/png.mod` — MUST
- 188: `/boot/flatcar/grub/i386-pc/priority_queue.mod` — MUST
- 189: `/boot/flatcar/grub/i386-pc/probe.mod` — MUST
- 190: `/boot/flatcar/grub/i386-pc/procfs.mod` — MUST
- 191: `/boot/flatcar/grub/i386-pc/progress.mod` — MUST
- 192: `/boot/flatcar/grub/i386-pc/pxe.mod` — MUST
- 193: `/boot/flatcar/grub/i386-pc/pxechain.mod` — MUST
- 194: `/boot/flatcar/grub/i386-pc/raid5rec.mod` — MUST
- 195: `/boot/flatcar/grub/i386-pc/raid6rec.mod` — MUST
- 196: `/boot/flatcar/grub/i386-pc/random.mod` — MUST
- 197: `/boot/flatcar/grub/i386-pc/rdmsr.mod` — MUST
- 198: `/boot/flatcar/grub/i386-pc/reboot.mod` — MUST
- 199: `/boot/flatcar/grub/i386-pc/regexp.mod` — MUST
- 200: `/boot/flatcar/grub/i386-pc/reiserfs.mod` — MUST
- 201: `/boot/flatcar/grub/i386-pc/relocator.mod` — MUST
- 202: `/boot/flatcar/grub/i386-pc/romfs.mod` — MUST
- 203: `/boot/flatcar/grub/i386-pc/scsi.mod` — MUST
- 204: `/boot/flatcar/grub/i386-pc/search_fs_file.mod` — MUST
- 205: `/boot/flatcar/grub/i386-pc/search_label.mod` — MUST
- 206: `/boot/flatcar/grub/i386-pc/search_part_uuid.mod` — MUST
- 207: `/boot/flatcar/grub/i386-pc/sendkey.mod` — MUST
- 208: `/boot/flatcar/grub/i386-pc/setjmp.mod` — MUST
- 209: `/boot/flatcar/grub/i386-pc/setpci.mod` — MUST
- 210: `/boot/flatcar/grub/i386-pc/sfs.mod` — MUST
- 211: `/boot/flatcar/grub/i386-pc/sleep.mod` — MUST
- 212: `/boot/flatcar/grub/i386-pc/smbios.mod` — MUST
- 213: `/boot/flatcar/grub/i386-pc/spkmodem.mod` — MUST
- 214: `/boot/flatcar/grub/i386-pc/squash4.mod` — MUST
- 215: `/boot/flatcar/grub/i386-pc/syslinuxcfg.mod` — MUST
- 216: `/boot/flatcar/grub/i386-pc/terminal.lst` — HOLE
- 217: `/boot/flatcar/grub/i386-pc/terminfo.mod` — MUST
- 218: `/boot/flatcar/grub/i386-pc/testload.mod` — MUST
- 219: `/boot/flatcar/grub/i386-pc/testspeed.mod` — MUST
- 220: `/boot/flatcar/grub/i386-pc/tftp.mod` — MUST
- 221: `/boot/flatcar/grub/i386-pc/tga.mod` — MUST
- 222: `/boot/flatcar/grub/i386-pc/time.mod` — MUST
- 223: `/boot/flatcar/grub/i386-pc/tr.mod` — MUST
- 224: `/boot/flatcar/grub/i386-pc/trig.mod` — MUST
- 225: `/boot/flatcar/grub/i386-pc/true.mod` — MUST
- 226: `/boot/flatcar/grub/i386-pc/truecrypt.mod` — MUST
- 227: `/boot/flatcar/grub/i386-pc/udf.mod` — MUST
- 228: `/boot/flatcar/grub/i386-pc/ufs1.mod` — MUST
- 229: `/boot/flatcar/grub/i386-pc/ufs1_be.mod` — MUST
- 230: `/boot/flatcar/grub/i386-pc/ufs2.mod` — MUST
- 231: `/boot/flatcar/grub/i386-pc/uhci.mod` — MUST
- 232: `/boot/flatcar/grub/i386-pc/usb.mod` — MUST
- 233: `/boot/flatcar/grub/i386-pc/usb_keyboard.mod` — MUST
- 234: `/boot/flatcar/grub/i386-pc/usbms.mod` — MUST
- 235: `/boot/flatcar/grub/i386-pc/usbserial_common.mod` — MUST
- 236: `/boot/flatcar/grub/i386-pc/usbserial_ftdi.mod` — MUST
- 237: `/boot/flatcar/grub/i386-pc/usbserial_pl2303.mod` — MUST
- 238: `/boot/flatcar/grub/i386-pc/usbserial_usbdebug.mod` — MUST
- 239: `/boot/flatcar/grub/i386-pc/usbtest.mod` — MUST
- 240: `/boot/flatcar/grub/i386-pc/vbe.mod` — MUST
- 241: `/boot/flatcar/grub/i386-pc/version.mod` — MUST
- 242: `/boot/flatcar/grub/i386-pc/vga.mod` — MUST
- 243: `/boot/flatcar/grub/i386-pc/vga_text.mod` — MUST
- 244: `/boot/flatcar/grub/i386-pc/video.lst` — HOLE
- 245: `/boot/flatcar/grub/i386-pc/video.mod` — MUST
- 246: `/boot/flatcar/grub/i386-pc/video_bochs.mod` — MUST
- 247: `/boot/flatcar/grub/i386-pc/video_cirrus.mod` — MUST
- 248: `/boot/flatcar/grub/i386-pc/video_colors.mod` — MUST
- 249: `/boot/flatcar/grub/i386-pc/video_fb.mod` — MUST
- 250: `/boot/flatcar/grub/i386-pc/videoinfo.mod` — MUST
- 251: `/boot/flatcar/grub/i386-pc/videotest.mod` — MUST
- 252: `/boot/flatcar/grub/i386-pc/wrmsr.mod` — MUST
- 253: `/boot/flatcar/grub/i386-pc/xfs.mod` — MUST
- 254: `/boot/flatcar/grub/i386-pc/xnu.mod` — MUST
- 255: `/boot/flatcar/grub/i386-pc/xnu_uuid.mod` — MUST
- 256: `/boot/flatcar/grub/i386-pc/zfs.mod` — MUST
- 257: `/boot/flatcar/grub/i386-pc/zfscrypt.mod` — MUST
- 258: `/boot/flatcar/grub/i386-pc/zfsinfo.mod` — MUST
- 259: `/boot/flatcar/grub/i386-pc/zstd.mod` — MUST

### Correction flatcar-e202fef092ca215c5aa60869
MUST → MIXED. Code requires recording; indexes/history have exemption conflicts; construction inputs lack established later consumers.
Corrected complete member map (supersedes earlier map):
- 1: `/boot/flatcar/grub/x86_64-xen/adler32.mod` — MUST
- 2: `/boot/flatcar/grub/x86_64-xen/affs.mod` — MUST
- 3: `/boot/flatcar/grub/x86_64-xen/afs.mod` — MUST
- 4: `/boot/flatcar/grub/x86_64-xen/afsplitter.mod` — MUST
- 5: `/boot/flatcar/grub/x86_64-xen/all_video.mod` — MUST
- 6: `/boot/flatcar/grub/x86_64-xen/appendedsig.mod` — MUST
- 7: `/boot/flatcar/grub/x86_64-xen/archelp.mod` — MUST
- 8: `/boot/flatcar/grub/x86_64-xen/asn1.mod` — MUST
- 9: `/boot/flatcar/grub/x86_64-xen/backtrace.mod` — MUST
- 10: `/boot/flatcar/grub/x86_64-xen/bfs.mod` — MUST
- 11: `/boot/flatcar/grub/x86_64-xen/bitmap.mod` — MUST
- 12: `/boot/flatcar/grub/x86_64-xen/bitmap_scale.mod` — MUST
- 13: `/boot/flatcar/grub/x86_64-xen/blocklist.mod` — MUST
- 14: `/boot/flatcar/grub/x86_64-xen/blscfg.mod` — MUST
- 15: `/boot/flatcar/grub/x86_64-xen/bufio.mod` — MUST
- 16: `/boot/flatcar/grub/x86_64-xen/cat.mod` — MUST
- 17: `/boot/flatcar/grub/x86_64-xen/cbfs.mod` — MUST
- 18: `/boot/flatcar/grub/x86_64-xen/cmp.mod` — MUST
- 19: `/boot/flatcar/grub/x86_64-xen/command.lst` — HOLE
- 20: `/boot/flatcar/grub/x86_64-xen/cpio.mod` — MUST
- 21: `/boot/flatcar/grub/x86_64-xen/cpio_be.mod` — MUST
- 22: `/boot/flatcar/grub/x86_64-xen/cpuid.mod` — MUST
- 23: `/boot/flatcar/grub/x86_64-xen/crc64.mod` — MUST
- 24: `/boot/flatcar/grub/x86_64-xen/crypto.lst` — HOLE
- 25: `/boot/flatcar/grub/x86_64-xen/crypto.mod` — MUST
- 26: `/boot/flatcar/grub/x86_64-xen/cryptodisk.mod` — MUST
- 27: `/boot/flatcar/grub/x86_64-xen/date.mod` — MUST
- 28: `/boot/flatcar/grub/x86_64-xen/datehook.mod` — MUST
- 29: `/boot/flatcar/grub/x86_64-xen/datetime.mod` — MUST
- 30: `/boot/flatcar/grub/x86_64-xen/disk.mod` — MUST
- 31: `/boot/flatcar/grub/x86_64-xen/diskfilter.mod` — MUST
- 32: `/boot/flatcar/grub/x86_64-xen/div.mod` — MUST
- 33: `/boot/flatcar/grub/x86_64-xen/dm_nv.mod` — MUST
- 34: `/boot/flatcar/grub/x86_64-xen/elf.mod` — MUST
- 35: `/boot/flatcar/grub/x86_64-xen/eval.mod` — MUST
- 36: `/boot/flatcar/grub/x86_64-xen/exfat.mod` — MUST
- 37: `/boot/flatcar/grub/x86_64-xen/ext2.mod` — MUST
- 38: `/boot/flatcar/grub/x86_64-xen/f2fs.mod` — MUST
- 39: `/boot/flatcar/grub/x86_64-xen/fdt.lst` — HOLE
- 40: `/boot/flatcar/grub/x86_64-xen/file.mod` — MUST
- 41: `/boot/flatcar/grub/x86_64-xen/font.mod` — MUST
- 42: `/boot/flatcar/grub/x86_64-xen/fs.lst` — HOLE
- 43: `/boot/flatcar/grub/x86_64-xen/fshelp.mod` — MUST
- 44: `/boot/flatcar/grub/x86_64-xen/gcry_arcfour.mod` — MUST
- 45: `/boot/flatcar/grub/x86_64-xen/gcry_blowfish.mod` — MUST
- 46: `/boot/flatcar/grub/x86_64-xen/gcry_camellia.mod` — MUST
- 47: `/boot/flatcar/grub/x86_64-xen/gcry_cast5.mod` — MUST
- 48: `/boot/flatcar/grub/x86_64-xen/gcry_crc.mod` — MUST
- 49: `/boot/flatcar/grub/x86_64-xen/gcry_des.mod` — MUST
- 50: `/boot/flatcar/grub/x86_64-xen/gcry_dsa.mod` — MUST
- 51: `/boot/flatcar/grub/x86_64-xen/gcry_idea.mod` — MUST
- 52: `/boot/flatcar/grub/x86_64-xen/gcry_md4.mod` — MUST
- 53: `/boot/flatcar/grub/x86_64-xen/gcry_md5.mod` — MUST
- 54: `/boot/flatcar/grub/x86_64-xen/gcry_rfc2268.mod` — MUST
- 55: `/boot/flatcar/grub/x86_64-xen/gcry_rijndael.mod` — MUST
- 56: `/boot/flatcar/grub/x86_64-xen/gcry_rmd160.mod` — MUST
- 57: `/boot/flatcar/grub/x86_64-xen/gcry_rsa.mod` — MUST
- 58: `/boot/flatcar/grub/x86_64-xen/gcry_seed.mod` — MUST
- 59: `/boot/flatcar/grub/x86_64-xen/gcry_serpent.mod` — MUST
- 60: `/boot/flatcar/grub/x86_64-xen/gcry_sha1.mod` — MUST
- 61: `/boot/flatcar/grub/x86_64-xen/gcry_sha256.mod` — MUST
- 62: `/boot/flatcar/grub/x86_64-xen/gcry_sha512.mod` — MUST
- 63: `/boot/flatcar/grub/x86_64-xen/gcry_tiger.mod` — MUST
- 64: `/boot/flatcar/grub/x86_64-xen/gcry_twofish.mod` — MUST
- 65: `/boot/flatcar/grub/x86_64-xen/gcry_whirlpool.mod` — MUST
- 66: `/boot/flatcar/grub/x86_64-xen/geli.mod` — MUST
- 67: `/boot/flatcar/grub/x86_64-xen/gettext.mod` — MUST
- 68: `/boot/flatcar/grub/x86_64-xen/gfxmenu.mod` — MUST
- 69: `/boot/flatcar/grub/x86_64-xen/gfxterm.mod` — MUST
- 70: `/boot/flatcar/grub/x86_64-xen/gfxterm_background.mod` — MUST
- 71: `/boot/flatcar/grub/x86_64-xen/gpt.mod` — MUST
- 72: `/boot/flatcar/grub/x86_64-xen/gptrepair.mod` — MUST
- 73: `/boot/flatcar/grub/x86_64-xen/gptsync.mod` — MUST
- 74: `/boot/flatcar/grub/x86_64-xen/gzio.mod` — MUST
- 75: `/boot/flatcar/grub/x86_64-xen/halt.mod` — MUST
- 76: `/boot/flatcar/grub/x86_64-xen/hashsum.mod` — MUST
- 77: `/boot/flatcar/grub/x86_64-xen/hello.mod` — MUST
- 78: `/boot/flatcar/grub/x86_64-xen/help.mod` — MUST
- 79: `/boot/flatcar/grub/x86_64-xen/hexdump.mod` — MUST
- 80: `/boot/flatcar/grub/x86_64-xen/hfs.mod` — MUST
- 81: `/boot/flatcar/grub/x86_64-xen/hfsplus.mod` — MUST
- 82: `/boot/flatcar/grub/x86_64-xen/hfspluscomp.mod` — MUST
- 83: `/boot/flatcar/grub/x86_64-xen/http.mod` — MUST
- 84: `/boot/flatcar/grub/x86_64-xen/increment.mod` — MUST
- 85: `/boot/flatcar/grub/x86_64-xen/iso9660.mod` — MUST
- 86: `/boot/flatcar/grub/x86_64-xen/jfs.mod` — MUST
- 87: `/boot/flatcar/grub/x86_64-xen/jpeg.mod` — MUST
- 88: `/boot/flatcar/grub/x86_64-xen/json.mod` — MUST
- 89: `/boot/flatcar/grub/x86_64-xen/keystatus.mod` — MUST
- 90: `/boot/flatcar/grub/x86_64-xen/ldm.mod` — MUST
- 91: `/boot/flatcar/grub/x86_64-xen/legacycfg.mod` — MUST
- 92: `/boot/flatcar/grub/x86_64-xen/linux.mod` — MUST
- 93: `/boot/flatcar/grub/x86_64-xen/load.cfg` — UNKNOWN
- 94: `/boot/flatcar/grub/x86_64-xen/loadenv.mod` — MUST
- 95: `/boot/flatcar/grub/x86_64-xen/loopback.mod` — MUST
- 96: `/boot/flatcar/grub/x86_64-xen/ls.mod` — MUST
- 97: `/boot/flatcar/grub/x86_64-xen/lsmmap.mod` — MUST
- 98: `/boot/flatcar/grub/x86_64-xen/lsxen.mod` — MUST
- 99: `/boot/flatcar/grub/x86_64-xen/luks.mod` — MUST
- 100: `/boot/flatcar/grub/x86_64-xen/luks2.mod` — MUST
- 101: `/boot/flatcar/grub/x86_64-xen/lvm.mod` — MUST
- 102: `/boot/flatcar/grub/x86_64-xen/lzopio.mod` — MUST
- 103: `/boot/flatcar/grub/x86_64-xen/macbless.mod` — MUST
- 104: `/boot/flatcar/grub/x86_64-xen/macho.mod` — MUST
- 105: `/boot/flatcar/grub/x86_64-xen/mdraid09.mod` — MUST
- 106: `/boot/flatcar/grub/x86_64-xen/mdraid09_be.mod` — MUST
- 107: `/boot/flatcar/grub/x86_64-xen/mdraid1x.mod` — MUST
- 108: `/boot/flatcar/grub/x86_64-xen/memrw.mod` — MUST
- 109: `/boot/flatcar/grub/x86_64-xen/minicmd.mod` — MUST
- 110: `/boot/flatcar/grub/x86_64-xen/minix.mod` — MUST
- 111: `/boot/flatcar/grub/x86_64-xen/minix2.mod` — MUST
- 112: `/boot/flatcar/grub/x86_64-xen/minix2_be.mod` — MUST
- 113: `/boot/flatcar/grub/x86_64-xen/minix3.mod` — MUST
- 114: `/boot/flatcar/grub/x86_64-xen/minix3_be.mod` — MUST
- 115: `/boot/flatcar/grub/x86_64-xen/minix_be.mod` — MUST
- 116: `/boot/flatcar/grub/x86_64-xen/moddep.lst` — HOLE
- 117: `/boot/flatcar/grub/x86_64-xen/mpi.mod` — MUST
- 118: `/boot/flatcar/grub/x86_64-xen/msdospart.mod` — MUST
- 119: `/boot/flatcar/grub/x86_64-xen/net.mod` — MUST
- 120: `/boot/flatcar/grub/x86_64-xen/newc.mod` — MUST
- 121: `/boot/flatcar/grub/x86_64-xen/nilfs2.mod` — MUST
- 122: `/boot/flatcar/grub/x86_64-xen/ntfs.mod` — MUST
- 123: `/boot/flatcar/grub/x86_64-xen/ntfscomp.mod` — MUST
- 124: `/boot/flatcar/grub/x86_64-xen/odc.mod` — MUST
- 125: `/boot/flatcar/grub/x86_64-xen/offsetio.mod` — MUST
- 126: `/boot/flatcar/grub/x86_64-xen/part_acorn.mod` — MUST
- 127: `/boot/flatcar/grub/x86_64-xen/part_amiga.mod` — MUST
- 128: `/boot/flatcar/grub/x86_64-xen/part_apple.mod` — MUST
- 129: `/boot/flatcar/grub/x86_64-xen/part_bsd.mod` — MUST
- 130: `/boot/flatcar/grub/x86_64-xen/part_dfly.mod` — MUST
- 131: `/boot/flatcar/grub/x86_64-xen/part_dvh.mod` — MUST
- 132: `/boot/flatcar/grub/x86_64-xen/part_msdos.mod` — MUST
- 133: `/boot/flatcar/grub/x86_64-xen/part_plan.mod` — MUST
- 134: `/boot/flatcar/grub/x86_64-xen/part_sun.mod` — MUST
- 135: `/boot/flatcar/grub/x86_64-xen/part_sunpc.mod` — MUST
- 136: `/boot/flatcar/grub/x86_64-xen/partmap.lst` — HOLE
- 137: `/boot/flatcar/grub/x86_64-xen/parttool.lst` — HOLE
- 138: `/boot/flatcar/grub/x86_64-xen/parttool.mod` — MUST
- 139: `/boot/flatcar/grub/x86_64-xen/password.mod` — MUST
- 140: `/boot/flatcar/grub/x86_64-xen/password_pbkdf2.mod` — MUST
- 141: `/boot/flatcar/grub/x86_64-xen/pbkdf2.mod` — MUST
- 142: `/boot/flatcar/grub/x86_64-xen/pgp.mod` — MUST
- 143: `/boot/flatcar/grub/x86_64-xen/pkcs1_v15.mod` — MUST
- 144: `/boot/flatcar/grub/x86_64-xen/plainmount.mod` — MUST
- 145: `/boot/flatcar/grub/x86_64-xen/png.mod` — MUST
- 146: `/boot/flatcar/grub/x86_64-xen/priority_queue.mod` — MUST
- 147: `/boot/flatcar/grub/x86_64-xen/probe.mod` — MUST
- 148: `/boot/flatcar/grub/x86_64-xen/procfs.mod` — MUST
- 149: `/boot/flatcar/grub/x86_64-xen/progress.mod` — MUST
- 150: `/boot/flatcar/grub/x86_64-xen/raid5rec.mod` — MUST
- 151: `/boot/flatcar/grub/x86_64-xen/raid6rec.mod` — MUST
- 152: `/boot/flatcar/grub/x86_64-xen/reboot.mod` — MUST
- 153: `/boot/flatcar/grub/x86_64-xen/regexp.mod` — MUST
- 154: `/boot/flatcar/grub/x86_64-xen/reiserfs.mod` — MUST
- 155: `/boot/flatcar/grub/x86_64-xen/relocator.mod` — MUST
- 156: `/boot/flatcar/grub/x86_64-xen/romfs.mod` — MUST
- 157: `/boot/flatcar/grub/x86_64-xen/scsi.mod` — MUST
- 158: `/boot/flatcar/grub/x86_64-xen/search_fs_file.mod` — MUST
- 159: `/boot/flatcar/grub/x86_64-xen/search_label.mod` — MUST
- 160: `/boot/flatcar/grub/x86_64-xen/search_part_uuid.mod` — MUST
- 161: `/boot/flatcar/grub/x86_64-xen/setjmp.mod` — MUST
- 162: `/boot/flatcar/grub/x86_64-xen/sfs.mod` — MUST
- 163: `/boot/flatcar/grub/x86_64-xen/sleep.mod` — MUST
- 164: `/boot/flatcar/grub/x86_64-xen/squash4.mod` — MUST
- 165: `/boot/flatcar/grub/x86_64-xen/syslinuxcfg.mod` — MUST
- 166: `/boot/flatcar/grub/x86_64-xen/terminal.lst` — HOLE
- 167: `/boot/flatcar/grub/x86_64-xen/testload.mod` — MUST
- 168: `/boot/flatcar/grub/x86_64-xen/testspeed.mod` — MUST
- 169: `/boot/flatcar/grub/x86_64-xen/tftp.mod` — MUST
- 170: `/boot/flatcar/grub/x86_64-xen/tga.mod` — MUST
- 171: `/boot/flatcar/grub/x86_64-xen/time.mod` — MUST
- 172: `/boot/flatcar/grub/x86_64-xen/tr.mod` — MUST
- 173: `/boot/flatcar/grub/x86_64-xen/trig.mod` — MUST
- 174: `/boot/flatcar/grub/x86_64-xen/true.mod` — MUST
- 175: `/boot/flatcar/grub/x86_64-xen/udf.mod` — MUST
- 176: `/boot/flatcar/grub/x86_64-xen/ufs1.mod` — MUST
- 177: `/boot/flatcar/grub/x86_64-xen/ufs1_be.mod` — MUST
- 178: `/boot/flatcar/grub/x86_64-xen/ufs2.mod` — MUST
- 179: `/boot/flatcar/grub/x86_64-xen/version.mod` — MUST
- 180: `/boot/flatcar/grub/x86_64-xen/video.lst` — HOLE
- 181: `/boot/flatcar/grub/x86_64-xen/video.mod` — MUST
- 182: `/boot/flatcar/grub/x86_64-xen/video_colors.mod` — MUST
- 183: `/boot/flatcar/grub/x86_64-xen/video_fb.mod` — MUST
- 184: `/boot/flatcar/grub/x86_64-xen/videoinfo.mod` — MUST
- 185: `/boot/flatcar/grub/x86_64-xen/videotest.mod` — MUST
- 186: `/boot/flatcar/grub/x86_64-xen/xfs.mod` — MUST
- 187: `/boot/flatcar/grub/x86_64-xen/xnu_uuid.mod` — MUST
- 188: `/boot/flatcar/grub/x86_64-xen/zfs.mod` — MUST
- 189: `/boot/flatcar/grub/x86_64-xen/zfscrypt.mod` — MUST
- 190: `/boot/flatcar/grub/x86_64-xen/zfsinfo.mod` — MUST
- 191: `/boot/flatcar/grub/x86_64-xen/zstd.mod` — MUST

### Correction flatcar-ea240c7b8257d2e5ce718e32
MUST → UNKNOWN. Inspected grub_install.sh: grub-mkimage consumes load.cfg with --config; the separately retained copy has no established runtime consumer.

### Correction flatcar-f4ec5e1afe79e8134ad617be
MUST → UNKNOWN. useradd documents copying templates, not executing them. The inventory has no contents of these templates.

### Correction flatcar-e20b758d51ecb8b4bc396bfb
UNKNOWN → MIXED. Kernel rules affect system auditing; plugin and daemon setting values remain unavailable.
Corrected complete member map (supersedes earlier map):
- 1: `/etc/audit/audisp-filter.conf` — UNKNOWN
- 2: `/etc/audit/audisp-remote.conf` — UNKNOWN
- 3: `/etc/audit/audit-stop.rules` — MUST
- 4: `/etc/audit/audit.rules` — MUST
- 5: `/etc/audit/auditd.conf` — UNKNOWN
- 6: `/etc/audit/plugins.d` — UNKNOWN
- 7: `/etc/audit/rules.d` — MUST

### Correction flatcar-6af53e326cce5228408a6307
UNKNOWN → MIXED. Policy trees supply system access controls; uncaptured selection and management values remain unknown.
Corrected complete member map (supersedes earlier map):
- 1: `/etc/selinux/config` — UNKNOWN
- 2: `/etc/selinux/mcs` — MUST
- 3: `/etc/selinux/mls` — MUST
- 4: `/etc/selinux/semanage.conf` — UNKNOWN
- 5: `/etc/selinux/targeted` — MUST

### Correction flatcar-73e390997be4f5bde0ca5a28
UNKNOWN → MIXED. Trust store serves multiple programs; marker is bookkeeping; cryptographic configuration values are uncaptured.
Corrected complete member map (supersedes earlier map):
- 1: `/etc/ssl/certs` — MUST
- 2: `/etc/ssl/fipsmodule.cnf` — UNKNOWN
- 3: `/etc/ssl/openssl.cnf` — UNKNOWN
- 4: `/etc/ssl/private` — NOT

### Correction flatcar-43d0c22d212a2cad83c0bab0
UNKNOWN → MIXED. Timer enablement affects execution; marker directories are bookkeeping; actual service-configuration values are uncaptured.
Corrected complete member map (supersedes earlier map):
- 1: `/etc/systemd/coredump.conf` — UNKNOWN
- 2: `/etc/systemd/journal-remote.conf` — UNKNOWN
- 3: `/etc/systemd/journal-upload.conf` — UNKNOWN
- 4: `/etc/systemd/journald.conf` — UNKNOWN
- 5: `/etc/systemd/logind.conf` — UNKNOWN
- 6: `/etc/systemd/network` — NOT
- 7: `/etc/systemd/networkd.conf` — UNKNOWN
- 8: `/etc/systemd/oomd.conf` — UNKNOWN
- 9: `/etc/systemd/pstore.conf` — UNKNOWN
- 10: `/etc/systemd/resolved.conf` — UNKNOWN
- 11: `/etc/systemd/sleep.conf` — UNKNOWN
- 12: `/etc/systemd/system` — MUST
- 13: `/etc/systemd/system.conf` — UNKNOWN
- 14: `/etc/systemd/timesyncd.conf` — UNKNOWN
- 15: `/etc/systemd/user` — NOT
- 16: `/etc/systemd/user.conf` — UNKNOWN

### Correction flatcar-7955ed3fbebf581406d0ce57
MIXED → MIXED. Account/code/system effects require recording; markers/history/content are exempt; other uncaptured effects remain unknown.
Corrected complete member map (supersedes earlier map):
- 1: `/etc/.ignition-result.json` — NOT
- 2: `/etc/.pwd.lock` — UNKNOWN
- 3: `/etc/.systemd-confext` — MUST
- 4: `/etc/.updated` — UNKNOWN
- 5: `/etc/X11` — MUST
- 6: `/etc/audit` — MUST
- 7: `/etc/azure-ephemeral-disk-setup.conf` — UNKNOWN
- 8: `/etc/bash` — MUST
- 9: `/etc/bindresvport.blacklist` — UNKNOWN
- 10: `/etc/binfmt.d` — NOT
- 11: `/etc/cifs-utils` — UNKNOWN
- 12: `/etc/cni` — UNKNOWN
- 13: `/etc/conntrackd` — UNKNOWN
- 14: `/etc/coreos` — UNKNOWN
- 15: `/etc/credstore` — UNKNOWN
- 16: `/etc/credstore.encrypted` — UNKNOWN
- 17: `/etc/dbus-1` — MUST
- 18: `/etc/default` — MUST
- 19: `/etc/dracut.conf` — UNKNOWN
- 20: `/etc/e2scrub.conf` — UNKNOWN
- 21: `/etc/environment.d` — MUST
- 22: `/etc/ethertypes` — UNKNOWN
- 23: `/etc/extension-release.d` — MUST
- 24: `/etc/extensions` — MUST
- 25: `/etc/flatcar` — UNKNOWN
- 26: `/etc/group` — MUST
- 27: `/etc/group-` — NOT
- 28: `/etc/gshadow` — MUST
- 29: `/etc/gshadow-` — NOT
- 30: `/etc/hosts` — MUST
- 31: `/etc/idmapd.conf` — UNKNOWN
- 32: `/etc/init.d` — UNKNOWN
- 33: `/etc/iscsi` — UNKNOWN
- 34: `/etc/isns` — UNKNOWN
- 35: `/etc/issue` — NOT
- 36: `/etc/kernel` — NOT
- 37: `/etc/kexec.conf` — UNKNOWN
- 38: `/etc/keyutils` — UNKNOWN
- 39: `/etc/krb5.conf.example` — NOT
- 40: `/etc/ld.so.cache` — UNKNOWN
- 41: `/etc/ldap.conf.sudo` — UNKNOWN
- 42: `/etc/lessfilter.d` — UNKNOWN
- 43: `/etc/libaudit.conf` — UNKNOWN
- 44: `/etc/locale.conf` — MUST
- 45: `/etc/login.defs` — MUST
- 46: `/etc/logrotate.conf` — UNKNOWN
- 47: `/etc/logrotate.d` — UNKNOWN
- 48: `/etc/lvm` — UNKNOWN
- 49: `/etc/machine-id` — MUST
- 50: `/etc/mke2fs.conf` — UNKNOWN
- 51: `/etc/modules-load.d` — NOT
- 52: `/etc/motd` — NOT
- 53: `/etc/mtab` — UNKNOWN
- 54: `/etc/netconfig` — UNKNOWN
- 55: `/etc/nscd.conf` — UNKNOWN
- 56: `/etc/ntp.conf` — UNKNOWN
- 57: `/etc/nvme` — UNKNOWN
- 58: `/etc/openldap` — UNKNOWN
- 59: `/etc/pam.d` — NOT
- 60: `/etc/passwd` — MUST
- 61: `/etc/passwd-` — NOT
- 62: `/etc/pkcs11` — NOT
- 63: `/etc/polkit-1` — NOT
- 64: `/etc/profile.d` — MUST
- 65: `/etc/quotagrpadmins` — UNKNOWN
- 66: `/etc/quotatab` — UNKNOWN
- 67: `/etc/request-key.conf` — MUST
- 68: `/etc/request-key.d` — MUST
- 69: `/etc/resolv.conf` — MUST
- 70: `/etc/runlevels` — UNKNOWN
- 71: `/etc/sasl2` — UNKNOWN
- 72: `/etc/securetty` — MUST
- 73: `/etc/security` — NOT
- 74: `/etc/selinux` — MUST
- 75: `/etc/sestatus.conf` — UNKNOWN
- 76: `/etc/shadow` — UNKNOWN
- 77: `/etc/shadow-` — NOT
- 78: `/etc/skel` — UNKNOWN
- 79: `/etc/ssh` — MUST
- 80: `/etc/ssl` — MUST
- 81: `/etc/sssd` — MUST
- 82: `/etc/subgid` — MUST
- 83: `/etc/subgid-` — NOT
- 84: `/etc/subuid` — MUST
- 85: `/etc/subuid-` — NOT
- 86: `/etc/sudo_logsrvd.conf` — UNKNOWN
- 87: `/etc/sudoers.d` — NOT
- 88: `/etc/sudoers.dist` — UNKNOWN
- 89: `/etc/sysconfig` — UNKNOWN
- 90: `/etc/systemd` — MUST
- 91: `/etc/tcsd.conf` — UNKNOWN
- 92: `/etc/tmpfiles.d` — NOT
- 93: `/etc/tpm2-tss` — UNKNOWN
- 94: `/etc/udev` — MUST
- 95: `/etc/user` — UNKNOWN
- 96: `/etc/vim` — UNKNOWN
- 97: `/etc/warnquota.conf` — UNKNOWN
- 98: `/etc/whois.conf` — UNKNOWN
- 99: `/etc/wireguard` — UNKNOWN
- 100: `/etc/xattr.conf` — UNKNOWN
- 101: `/etc/xdg` — NOT

## Documentation record and interpretation details

The following short quotations establish program roles. Row `basis` identifies either the raw member snapshot or the primary documentation used; this section supplies additional role documentation. UNKNOWN is not an inference that no public documentation exists: the documentation establishes the file format or generic facility, while the actual captured object's contents or consumer dependency remains unavailable. Empty directories are not equated with the programs whose names appear in their paths. No design question about retaining or migrating state is used as a HOLE.

- https://raw.githubusercontent.com/flatcar/scripts/main/build_library/grub_install.sh — “Generate a memdisk containing the appropriately generated grub.cfg.” The script embeds load.cfg and grub.cfg.tar into separate boot images. Its i386 branch also saves patched boot bytes. Therefore separately retained construction inputs are not assumed active merely from their names. In the corrected module groups: `.mod` and `core.img` MUST; `.lst` NOT (program-local values under S2.2-7 and S2.2-13); `mbr.bin` HOLE (past bytes versus restoration capability); `boot.img` and `load.cfg` UNKNOWN (installed-copy consumer unestablished). The source establishes image construction, not runtime use of every intermediate file.
- https://raw.githubusercontent.com/rhboot/grub2/master/docs/grub.texi — “a flexible and powerful boot loader program”. GRUB executable images and modules supply native boot functionality. Native code is not confined web-page/guest code under S2.2-11.
- https://raw.githubusercontent.com/shadow-maint/shadow/master/man/useradd.8.xml — “The files and directories contained in the skeleton directory”. The surrounding documentation specifies copying into new homes. Copying alone does not establish that these particular templates contain commands; their contents were not captured. This narrows the initial template decision to UNKNOWN.
- https://docs.kernel.org/filesystems/overlayfs.html — “the result of overlaying one filesystem on top of the other.” The recorded configuration work directory supports the overlay mount; this is filesystem behavior shared across programs.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-sysext.html — “systemd-sysext activates/deactivates system extension images.” Extension references and compatibility information select resources merged into system directories. The separately stored image group remains UNKNOWN where image and selection-marker contents are absent.
- https://dbus.freedesktop.org/doc/dbus-daemon.1.html — “Multiple programs connect to the message bus daemon and can exchange messages with one another.” Bus sockets and access/activation configuration serve interprocess behavior.
- https://raw.githubusercontent.com/linux-audit/audit-userspace/master/docs/audit.rules.7 — “a set of rules loaded in the kernel audit system”. Audit rule files have kernel effects; uncaptured plugin settings are not assumed equivalent to those rules.
- https://raw.githubusercontent.com/logrotate/logrotate/main/logrotate.8.in — “It allows automatic rotation, compression, removal, and mailing of log files.” Rotation configuration controls filesystem actions, unlike the logs themselves.
- https://raw.githubusercontent.com/SSSD/sssd/master/src/man/sssd.conf.5.xml — “the configuration file for SSSD”. Authentication/identity configuration affects account access. Empty state/IPC directories do not prove populated databases or active sockets.
- https://raw.githubusercontent.com/SELinuxProject/selinux/master/libselinux/man/man5/selabel_file.5 — “The file contexts backend maps from pathname/mode combinations into security contexts.” The three policy trees were inspected individually: contexts and user mappings affect labels/access; compiled `.bin` equivalents accelerate lookup; `.keep` files are markers. The mcs/mls/targeted counterpart groups were each checked against the raw member list; they were not inferred from a shared directory name alone.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html — “Unit configuration”. Its documented search paths include transient, generated and administrator units. Unit definitions, dependencies and enablement change processes/mounts beyond the manager interface.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html — “for socket-based activation”. Actual socket inodes and their observed aliases provide connection paths; they are not cached or historical descriptions of those paths.
- https://www.freedesktop.org/software/systemd/man/latest/varlinkctl.html — “Directory containing `AF_UNIX` entrypoint socket inodes (or symlinks to them)”. The registry files identify public IPC endpoints. All members of the two registry groups were verified as symlinks to recorded sockets.
- https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.exec.xml — “a new file system namespace will be set up for the executed processes”. Private temporary directories and inaccessible nodes implement cross-process filesystem separation. They are not merely presentation settings of one application.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.network.html — “Networks are applied to links whenever the links appear.” Network rules, generated resolver configuration and shared interface status concern system connectivity outside the reader.
- https://www.freedesktop.org/software/systemd/man/latest/udev.html — “All device information udev processes is stored in the udev database and sent out to possible event subscribers.” Database entries and tags supply information to other programs. They are not assumed speed-only caches.
- https://raw.githubusercontent.com/systemd/systemd/v260/src/udev/udev-node.c — “With the new format, the devnode and priority can be obtained from symlink itself.” The matching version also implements the link-stack association behavior used for Rule U; raw symlinks use this priority:device format.
- https://raw.githubusercontent.com/systemd/systemd/v260/src/udev/udev-watch.c — `udev_watch_begin`. Device watches and their saved associations map notifications to affected devices. The raw group contains reciprocal watch/device symlinks.
- https://man.openbsd.org/sshd.8 — “The forked daemons handle key exchange, encryption, authentication, command execution, and data exchange.” Host authentication keys and server settings enable account login; client default settings are program-local values. Current authorized-key files are distinct from the named old directory.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html — “collects and stores logging data”. Journal files and conventional login/audit logs retain past events; live logging sockets are not historical records.
- https://www.freedesktop.org/software/systemd/man/latest/os-release.html — “contain operating system identification data.” Staged release files supply content, not executable commands. Extension compatibility metadata has a different selection role, covered separately.
- https://www.freedesktop.org/software/systemd/man/latest/machine-id.html — “This machine ID adheres to the same format and logic as the D-Bus machine ID.” The recorded D-Bus alias exposes shared identity to programs.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-tmpfiles.html — “creates, deletes, and cleans up files and directories”. The generated static-node rules affect system device availability.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html — “the time when the service unit was last triggered is stored on disk.” Persistent timers use this historical timestamp to determine catch-up activation. S2.2-1 requires behavioral dependencies while S2.2-6 exempts history; neither states precedence for a past-event record that drives future execution.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-timesyncd.service.html — “A file that is touched on each successful synchronization”. The synchronization marker informs dependent services, while the saved clock timestamp advances the next boot's clock. Their HOLE is the explicit history/behavior intersection, not a general objection to program state.
- https://raw.githubusercontent.com/containerd/containerd/main/docs/ops.md — “containerd is a high performance container runtime”. This establishes the runtime role, but does not reveal captured Bolt database entries; those groups remain UNKNOWN.
- https://docs.docker.com/engine/storage/drivers/overlayfs-driver/ — “OverlayFS storage driver”. Documented layer-storage roles cannot establish actual images or network/volume database contents in the inventory; empty directories and undecoded databases remain UNKNOWN.

## Per-row verification

The only bulk homogeneous decisions are Rule U and Rule K, each with ten named hand checks above. Other rows were inspected individually, including corresponding SELinux policy directories with separately enumerated memberships. The script is a transcription helper, not authority for inference from a path prefix. MIXED positions always refer to the input's one-based member array; complete mappings are recorded above. Correction sections supersede earlier mappings, preserving the audit of narrowed claims.

Validation passed: 386 exact unique assigned IDs; allowed decisions; 15/30-word limits; every MIXED member assigned exactly once. Counts: {'NOT': 41, 'MUST': 237, 'MIXED': 45, 'UNKNOWN': 60, 'HOLE': 3}.
Corrected complete member map (supersedes earlier map):
- 1: `/boot/flatcar/grub/grub.cfg.tar` — UNKNOWN
- 2: `/boot/flatcar/grub/i386-pc` — MUST
- 3: `/boot/flatcar/grub/x86_64-efi` — UNKNOWN
- 4: `/boot/flatcar/grub/x86_64-xen` — MUST

### Correction flatcar-aa489ee21d27f0b113d367ca
MIXED → MIXED. Code requires recording; indexes are program-local values; saved boot bytes conflict with history exemption; construction-input consumers are unknown.
Corrected complete member map (supersedes earlier map):
- 1: `/boot/flatcar/grub/i386-pc/acpi.mod` — MUST
- 2: `/boot/flatcar/grub/i386-pc/adler32.mod` — MUST
- 3: `/boot/flatcar/grub/i386-pc/affs.mod` — MUST
- 4: `/boot/flatcar/grub/i386-pc/afs.mod` — MUST
- 5: `/boot/flatcar/grub/i386-pc/afsplitter.mod` — MUST
- 6: `/boot/flatcar/grub/i386-pc/ahci.mod` — MUST
- 7: `/boot/flatcar/grub/i386-pc/all_video.mod` — MUST
- 8: `/boot/flatcar/grub/i386-pc/aout.mod` — MUST
- 9: `/boot/flatcar/grub/i386-pc/appendedsig.mod` — MUST
- 10: `/boot/flatcar/grub/i386-pc/archelp.mod` — MUST
- 11: `/boot/flatcar/grub/i386-pc/asn1.mod` — MUST
- 12: `/boot/flatcar/grub/i386-pc/at_keyboard.mod` — MUST
- 13: `/boot/flatcar/grub/i386-pc/ata.mod` — MUST
- 14: `/boot/flatcar/grub/i386-pc/backtrace.mod` — MUST
- 15: `/boot/flatcar/grub/i386-pc/bfs.mod` — MUST
- 16: `/boot/flatcar/grub/i386-pc/bitmap.mod` — MUST
- 17: `/boot/flatcar/grub/i386-pc/bitmap_scale.mod` — MUST
- 18: `/boot/flatcar/grub/i386-pc/blocklist.mod` — MUST
- 19: `/boot/flatcar/grub/i386-pc/blscfg.mod` — MUST
- 20: `/boot/flatcar/grub/i386-pc/boot.img` — UNKNOWN
- 21: `/boot/flatcar/grub/i386-pc/boot.mod` — MUST
- 22: `/boot/flatcar/grub/i386-pc/bsd.mod` — MUST
- 23: `/boot/flatcar/grub/i386-pc/bufio.mod` — MUST
- 24: `/boot/flatcar/grub/i386-pc/cat.mod` — MUST
- 25: `/boot/flatcar/grub/i386-pc/cbfs.mod` — MUST
- 26: `/boot/flatcar/grub/i386-pc/cbls.mod` — MUST
- 27: `/boot/flatcar/grub/i386-pc/cbmemc.mod` — MUST
- 28: `/boot/flatcar/grub/i386-pc/cbtable.mod` — MUST
- 29: `/boot/flatcar/grub/i386-pc/cbtime.mod` — MUST
- 30: `/boot/flatcar/grub/i386-pc/chain.mod` — MUST
- 31: `/boot/flatcar/grub/i386-pc/cmosdump.mod` — MUST
- 32: `/boot/flatcar/grub/i386-pc/cmostest.mod` — MUST
- 33: `/boot/flatcar/grub/i386-pc/cmp.mod` — MUST
- 34: `/boot/flatcar/grub/i386-pc/command.lst` — NOT
- 35: `/boot/flatcar/grub/i386-pc/core.img` — MUST
- 36: `/boot/flatcar/grub/i386-pc/cpio.mod` — MUST
- 37: `/boot/flatcar/grub/i386-pc/cpio_be.mod` — MUST
- 38: `/boot/flatcar/grub/i386-pc/cpuid.mod` — MUST
- 39: `/boot/flatcar/grub/i386-pc/crc64.mod` — MUST
- 40: `/boot/flatcar/grub/i386-pc/crypto.lst` — NOT
- 41: `/boot/flatcar/grub/i386-pc/crypto.mod` — MUST
- 42: `/boot/flatcar/grub/i386-pc/cryptodisk.mod` — MUST
- 43: `/boot/flatcar/grub/i386-pc/cs5536.mod` — MUST
- 44: `/boot/flatcar/grub/i386-pc/date.mod` — MUST
- 45: `/boot/flatcar/grub/i386-pc/datehook.mod` — MUST
- 46: `/boot/flatcar/grub/i386-pc/datetime.mod` — MUST
- 47: `/boot/flatcar/grub/i386-pc/disk.mod` — MUST
- 48: `/boot/flatcar/grub/i386-pc/diskfilter.mod` — MUST
- 49: `/boot/flatcar/grub/i386-pc/div.mod` — MUST
- 50: `/boot/flatcar/grub/i386-pc/dm_nv.mod` — MUST
- 51: `/boot/flatcar/grub/i386-pc/drivemap.mod` — MUST
- 52: `/boot/flatcar/grub/i386-pc/efiemu.mod` — MUST
- 53: `/boot/flatcar/grub/i386-pc/ehci.mod` — MUST
- 54: `/boot/flatcar/grub/i386-pc/elf.mod` — MUST
- 55: `/boot/flatcar/grub/i386-pc/eval.mod` — MUST
- 56: `/boot/flatcar/grub/i386-pc/exfat.mod` — MUST
- 57: `/boot/flatcar/grub/i386-pc/ext2.mod` — MUST
- 58: `/boot/flatcar/grub/i386-pc/extcmd.mod` — MUST
- 59: `/boot/flatcar/grub/i386-pc/f2fs.mod` — MUST
- 60: `/boot/flatcar/grub/i386-pc/fdt.lst` — NOT
- 61: `/boot/flatcar/grub/i386-pc/file.mod` — MUST
- 62: `/boot/flatcar/grub/i386-pc/font.mod` — MUST
- 63: `/boot/flatcar/grub/i386-pc/freedos.mod` — MUST
- 64: `/boot/flatcar/grub/i386-pc/fs.lst` — NOT
- 65: `/boot/flatcar/grub/i386-pc/fshelp.mod` — MUST
- 66: `/boot/flatcar/grub/i386-pc/gcry_arcfour.mod` — MUST
- 67: `/boot/flatcar/grub/i386-pc/gcry_blowfish.mod` — MUST
- 68: `/boot/flatcar/grub/i386-pc/gcry_camellia.mod` — MUST
- 69: `/boot/flatcar/grub/i386-pc/gcry_cast5.mod` — MUST
- 70: `/boot/flatcar/grub/i386-pc/gcry_crc.mod` — MUST
- 71: `/boot/flatcar/grub/i386-pc/gcry_des.mod` — MUST
- 72: `/boot/flatcar/grub/i386-pc/gcry_dsa.mod` — MUST
- 73: `/boot/flatcar/grub/i386-pc/gcry_idea.mod` — MUST
- 74: `/boot/flatcar/grub/i386-pc/gcry_md4.mod` — MUST
- 75: `/boot/flatcar/grub/i386-pc/gcry_md5.mod` — MUST
- 76: `/boot/flatcar/grub/i386-pc/gcry_rfc2268.mod` — MUST
- 77: `/boot/flatcar/grub/i386-pc/gcry_rijndael.mod` — MUST
- 78: `/boot/flatcar/grub/i386-pc/gcry_rmd160.mod` — MUST
- 79: `/boot/flatcar/grub/i386-pc/gcry_rsa.mod` — MUST
- 80: `/boot/flatcar/grub/i386-pc/gcry_seed.mod` — MUST
- 81: `/boot/flatcar/grub/i386-pc/gcry_serpent.mod` — MUST
- 82: `/boot/flatcar/grub/i386-pc/gcry_sha1.mod` — MUST
- 83: `/boot/flatcar/grub/i386-pc/gcry_sha256.mod` — MUST
- 84: `/boot/flatcar/grub/i386-pc/gcry_sha512.mod` — MUST
- 85: `/boot/flatcar/grub/i386-pc/gcry_tiger.mod` — MUST
- 86: `/boot/flatcar/grub/i386-pc/gcry_twofish.mod` — MUST
- 87: `/boot/flatcar/grub/i386-pc/gcry_whirlpool.mod` — MUST
- 88: `/boot/flatcar/grub/i386-pc/gdb.mod` — MUST
- 89: `/boot/flatcar/grub/i386-pc/geli.mod` — MUST
- 90: `/boot/flatcar/grub/i386-pc/gettext.mod` — MUST
- 91: `/boot/flatcar/grub/i386-pc/gfxmenu.mod` — MUST
- 92: `/boot/flatcar/grub/i386-pc/gfxterm.mod` — MUST
- 93: `/boot/flatcar/grub/i386-pc/gfxterm_background.mod` — MUST
- 94: `/boot/flatcar/grub/i386-pc/gpt.mod` — MUST
- 95: `/boot/flatcar/grub/i386-pc/gptrepair.mod` — MUST
- 96: `/boot/flatcar/grub/i386-pc/gptsync.mod` — MUST
- 97: `/boot/flatcar/grub/i386-pc/gzio.mod` — MUST
- 98: `/boot/flatcar/grub/i386-pc/halt.mod` — MUST
- 99: `/boot/flatcar/grub/i386-pc/hashsum.mod` — MUST
- 100: `/boot/flatcar/grub/i386-pc/hdparm.mod` — MUST
- 101: `/boot/flatcar/grub/i386-pc/hello.mod` — MUST
- 102: `/boot/flatcar/grub/i386-pc/help.mod` — MUST
- 103: `/boot/flatcar/grub/i386-pc/hexdump.mod` — MUST
- 104: `/boot/flatcar/grub/i386-pc/hfs.mod` — MUST
- 105: `/boot/flatcar/grub/i386-pc/hfsplus.mod` — MUST
- 106: `/boot/flatcar/grub/i386-pc/hfspluscomp.mod` — MUST
- 107: `/boot/flatcar/grub/i386-pc/http.mod` — MUST
- 108: `/boot/flatcar/grub/i386-pc/increment.mod` — MUST
- 109: `/boot/flatcar/grub/i386-pc/iorw.mod` — MUST
- 110: `/boot/flatcar/grub/i386-pc/iso9660.mod` — MUST
- 111: `/boot/flatcar/grub/i386-pc/jfs.mod` — MUST
- 112: `/boot/flatcar/grub/i386-pc/jpeg.mod` — MUST
- 113: `/boot/flatcar/grub/i386-pc/json.mod` — MUST
- 114: `/boot/flatcar/grub/i386-pc/keylayouts.mod` — MUST
- 115: `/boot/flatcar/grub/i386-pc/keystatus.mod` — MUST
- 116: `/boot/flatcar/grub/i386-pc/ldm.mod` — MUST
- 117: `/boot/flatcar/grub/i386-pc/legacycfg.mod` — MUST
- 118: `/boot/flatcar/grub/i386-pc/linux.mod` — MUST
- 119: `/boot/flatcar/grub/i386-pc/load.cfg` — UNKNOWN
- 120: `/boot/flatcar/grub/i386-pc/loadenv.mod` — MUST
- 121: `/boot/flatcar/grub/i386-pc/loopback.mod` — MUST
- 122: `/boot/flatcar/grub/i386-pc/ls.mod` — MUST
- 123: `/boot/flatcar/grub/i386-pc/lsacpi.mod` — MUST
- 124: `/boot/flatcar/grub/i386-pc/lsapm.mod` — MUST
- 125: `/boot/flatcar/grub/i386-pc/lsmmap.mod` — MUST
- 126: `/boot/flatcar/grub/i386-pc/lspci.mod` — MUST
- 127: `/boot/flatcar/grub/i386-pc/luks.mod` — MUST
- 128: `/boot/flatcar/grub/i386-pc/luks2.mod` — MUST
- 129: `/boot/flatcar/grub/i386-pc/lvm.mod` — MUST
- 130: `/boot/flatcar/grub/i386-pc/lzopio.mod` — MUST
- 131: `/boot/flatcar/grub/i386-pc/macbless.mod` — MUST
- 132: `/boot/flatcar/grub/i386-pc/macho.mod` — MUST
- 133: `/boot/flatcar/grub/i386-pc/mbr.bin` — HOLE
- 134: `/boot/flatcar/grub/i386-pc/mda_text.mod` — MUST
- 135: `/boot/flatcar/grub/i386-pc/mdraid09.mod` — MUST
- 136: `/boot/flatcar/grub/i386-pc/mdraid09_be.mod` — MUST
- 137: `/boot/flatcar/grub/i386-pc/mdraid1x.mod` — MUST
- 138: `/boot/flatcar/grub/i386-pc/memrw.mod` — MUST
- 139: `/boot/flatcar/grub/i386-pc/minicmd.mod` — MUST
- 140: `/boot/flatcar/grub/i386-pc/minix.mod` — MUST
- 141: `/boot/flatcar/grub/i386-pc/minix2.mod` — MUST
- 142: `/boot/flatcar/grub/i386-pc/minix2_be.mod` — MUST
- 143: `/boot/flatcar/grub/i386-pc/minix3.mod` — MUST
- 144: `/boot/flatcar/grub/i386-pc/minix3_be.mod` — MUST
- 145: `/boot/flatcar/grub/i386-pc/minix_be.mod` — MUST
- 146: `/boot/flatcar/grub/i386-pc/mmap.mod` — MUST
- 147: `/boot/flatcar/grub/i386-pc/moddep.lst` — NOT
- 148: `/boot/flatcar/grub/i386-pc/morse.mod` — MUST
- 149: `/boot/flatcar/grub/i386-pc/mpi.mod` — MUST
- 150: `/boot/flatcar/grub/i386-pc/msdospart.mod` — MUST
- 151: `/boot/flatcar/grub/i386-pc/multiboot.mod` — MUST
- 152: `/boot/flatcar/grub/i386-pc/multiboot2.mod` — MUST
- 153: `/boot/flatcar/grub/i386-pc/nativedisk.mod` — MUST
- 154: `/boot/flatcar/grub/i386-pc/net.mod` — MUST
- 155: `/boot/flatcar/grub/i386-pc/newc.mod` — MUST
- 156: `/boot/flatcar/grub/i386-pc/nilfs2.mod` — MUST
- 157: `/boot/flatcar/grub/i386-pc/ntfs.mod` — MUST
- 158: `/boot/flatcar/grub/i386-pc/ntfscomp.mod` — MUST
- 159: `/boot/flatcar/grub/i386-pc/ntldr.mod` — MUST
- 160: `/boot/flatcar/grub/i386-pc/odc.mod` — MUST
- 161: `/boot/flatcar/grub/i386-pc/offsetio.mod` — MUST
- 162: `/boot/flatcar/grub/i386-pc/ohci.mod` — MUST
- 163: `/boot/flatcar/grub/i386-pc/part_acorn.mod` — MUST
- 164: `/boot/flatcar/grub/i386-pc/part_amiga.mod` — MUST
- 165: `/boot/flatcar/grub/i386-pc/part_apple.mod` — MUST
- 166: `/boot/flatcar/grub/i386-pc/part_bsd.mod` — MUST
- 167: `/boot/flatcar/grub/i386-pc/part_dfly.mod` — MUST
- 168: `/boot/flatcar/grub/i386-pc/part_dvh.mod` — MUST
- 169: `/boot/flatcar/grub/i386-pc/part_msdos.mod` — MUST
- 170: `/boot/flatcar/grub/i386-pc/part_plan.mod` — MUST
- 171: `/boot/flatcar/grub/i386-pc/part_sun.mod` — MUST
- 172: `/boot/flatcar/grub/i386-pc/part_sunpc.mod` — MUST
- 173: `/boot/flatcar/grub/i386-pc/partmap.lst` — NOT
- 174: `/boot/flatcar/grub/i386-pc/parttool.lst` — NOT
- 175: `/boot/flatcar/grub/i386-pc/parttool.mod` — MUST
- 176: `/boot/flatcar/grub/i386-pc/password.mod` — MUST
- 177: `/boot/flatcar/grub/i386-pc/password_pbkdf2.mod` — MUST
- 178: `/boot/flatcar/grub/i386-pc/pata.mod` — MUST
- 179: `/boot/flatcar/grub/i386-pc/pbkdf2.mod` — MUST
- 180: `/boot/flatcar/grub/i386-pc/pci.mod` — MUST
- 181: `/boot/flatcar/grub/i386-pc/pcidump.mod` — MUST
- 182: `/boot/flatcar/grub/i386-pc/pgp.mod` — MUST
- 183: `/boot/flatcar/grub/i386-pc/pkcs1_v15.mod` — MUST
- 184: `/boot/flatcar/grub/i386-pc/plainmount.mod` — MUST
- 185: `/boot/flatcar/grub/i386-pc/plan9.mod` — MUST
- 186: `/boot/flatcar/grub/i386-pc/play.mod` — MUST
- 187: `/boot/flatcar/grub/i386-pc/png.mod` — MUST
- 188: `/boot/flatcar/grub/i386-pc/priority_queue.mod` — MUST
- 189: `/boot/flatcar/grub/i386-pc/probe.mod` — MUST
- 190: `/boot/flatcar/grub/i386-pc/procfs.mod` — MUST
- 191: `/boot/flatcar/grub/i386-pc/progress.mod` — MUST
- 192: `/boot/flatcar/grub/i386-pc/pxe.mod` — MUST
- 193: `/boot/flatcar/grub/i386-pc/pxechain.mod` — MUST
- 194: `/boot/flatcar/grub/i386-pc/raid5rec.mod` — MUST
- 195: `/boot/flatcar/grub/i386-pc/raid6rec.mod` — MUST
- 196: `/boot/flatcar/grub/i386-pc/random.mod` — MUST
- 197: `/boot/flatcar/grub/i386-pc/rdmsr.mod` — MUST
- 198: `/boot/flatcar/grub/i386-pc/reboot.mod` — MUST
- 199: `/boot/flatcar/grub/i386-pc/regexp.mod` — MUST
- 200: `/boot/flatcar/grub/i386-pc/reiserfs.mod` — MUST
- 201: `/boot/flatcar/grub/i386-pc/relocator.mod` — MUST
- 202: `/boot/flatcar/grub/i386-pc/romfs.mod` — MUST
- 203: `/boot/flatcar/grub/i386-pc/scsi.mod` — MUST
- 204: `/boot/flatcar/grub/i386-pc/search_fs_file.mod` — MUST
- 205: `/boot/flatcar/grub/i386-pc/search_label.mod` — MUST
- 206: `/boot/flatcar/grub/i386-pc/search_part_uuid.mod` — MUST
- 207: `/boot/flatcar/grub/i386-pc/sendkey.mod` — MUST
- 208: `/boot/flatcar/grub/i386-pc/setjmp.mod` — MUST
- 209: `/boot/flatcar/grub/i386-pc/setpci.mod` — MUST
- 210: `/boot/flatcar/grub/i386-pc/sfs.mod` — MUST
- 211: `/boot/flatcar/grub/i386-pc/sleep.mod` — MUST
- 212: `/boot/flatcar/grub/i386-pc/smbios.mod` — MUST
- 213: `/boot/flatcar/grub/i386-pc/spkmodem.mod` — MUST
- 214: `/boot/flatcar/grub/i386-pc/squash4.mod` — MUST
- 215: `/boot/flatcar/grub/i386-pc/syslinuxcfg.mod` — MUST
- 216: `/boot/flatcar/grub/i386-pc/terminal.lst` — NOT
- 217: `/boot/flatcar/grub/i386-pc/terminfo.mod` — MUST
- 218: `/boot/flatcar/grub/i386-pc/testload.mod` — MUST
- 219: `/boot/flatcar/grub/i386-pc/testspeed.mod` — MUST
- 220: `/boot/flatcar/grub/i386-pc/tftp.mod` — MUST
- 221: `/boot/flatcar/grub/i386-pc/tga.mod` — MUST
- 222: `/boot/flatcar/grub/i386-pc/time.mod` — MUST
- 223: `/boot/flatcar/grub/i386-pc/tr.mod` — MUST
- 224: `/boot/flatcar/grub/i386-pc/trig.mod` — MUST
- 225: `/boot/flatcar/grub/i386-pc/true.mod` — MUST
- 226: `/boot/flatcar/grub/i386-pc/truecrypt.mod` — MUST
- 227: `/boot/flatcar/grub/i386-pc/udf.mod` — MUST
- 228: `/boot/flatcar/grub/i386-pc/ufs1.mod` — MUST
- 229: `/boot/flatcar/grub/i386-pc/ufs1_be.mod` — MUST
- 230: `/boot/flatcar/grub/i386-pc/ufs2.mod` — MUST
- 231: `/boot/flatcar/grub/i386-pc/uhci.mod` — MUST
- 232: `/boot/flatcar/grub/i386-pc/usb.mod` — MUST
- 233: `/boot/flatcar/grub/i386-pc/usb_keyboard.mod` — MUST
- 234: `/boot/flatcar/grub/i386-pc/usbms.mod` — MUST
- 235: `/boot/flatcar/grub/i386-pc/usbserial_common.mod` — MUST
- 236: `/boot/flatcar/grub/i386-pc/usbserial_ftdi.mod` — MUST
- 237: `/boot/flatcar/grub/i386-pc/usbserial_pl2303.mod` — MUST
- 238: `/boot/flatcar/grub/i386-pc/usbserial_usbdebug.mod` — MUST
- 239: `/boot/flatcar/grub/i386-pc/usbtest.mod` — MUST
- 240: `/boot/flatcar/grub/i386-pc/vbe.mod` — MUST
- 241: `/boot/flatcar/grub/i386-pc/version.mod` — MUST
- 242: `/boot/flatcar/grub/i386-pc/vga.mod` — MUST
- 243: `/boot/flatcar/grub/i386-pc/vga_text.mod` — MUST
- 244: `/boot/flatcar/grub/i386-pc/video.lst` — NOT
- 245: `/boot/flatcar/grub/i386-pc/video.mod` — MUST
- 246: `/boot/flatcar/grub/i386-pc/video_bochs.mod` — MUST
- 247: `/boot/flatcar/grub/i386-pc/video_cirrus.mod` — MUST
- 248: `/boot/flatcar/grub/i386-pc/video_colors.mod` — MUST
- 249: `/boot/flatcar/grub/i386-pc/video_fb.mod` — MUST
- 250: `/boot/flatcar/grub/i386-pc/videoinfo.mod` — MUST
- 251: `/boot/flatcar/grub/i386-pc/videotest.mod` — MUST
- 252: `/boot/flatcar/grub/i386-pc/wrmsr.mod` — MUST
- 253: `/boot/flatcar/grub/i386-pc/xfs.mod` — MUST
- 254: `/boot/flatcar/grub/i386-pc/xnu.mod` — MUST
- 255: `/boot/flatcar/grub/i386-pc/xnu_uuid.mod` — MUST
- 256: `/boot/flatcar/grub/i386-pc/zfs.mod` — MUST
- 257: `/boot/flatcar/grub/i386-pc/zfscrypt.mod` — MUST
- 258: `/boot/flatcar/grub/i386-pc/zfsinfo.mod` — MUST
- 259: `/boot/flatcar/grub/i386-pc/zstd.mod` — MUST

### Correction flatcar-e202fef092ca215c5aa60869
MIXED → MIXED. Code requires recording; indexes are program-local values; saved boot bytes conflict with history exemption; construction-input consumers are unknown.
Corrected complete member map (supersedes earlier map):
- 1: `/boot/flatcar/grub/x86_64-xen/adler32.mod` — MUST
- 2: `/boot/flatcar/grub/x86_64-xen/affs.mod` — MUST
- 3: `/boot/flatcar/grub/x86_64-xen/afs.mod` — MUST
- 4: `/boot/flatcar/grub/x86_64-xen/afsplitter.mod` — MUST
- 5: `/boot/flatcar/grub/x86_64-xen/all_video.mod` — MUST
- 6: `/boot/flatcar/grub/x86_64-xen/appendedsig.mod` — MUST
- 7: `/boot/flatcar/grub/x86_64-xen/archelp.mod` — MUST
- 8: `/boot/flatcar/grub/x86_64-xen/asn1.mod` — MUST
- 9: `/boot/flatcar/grub/x86_64-xen/backtrace.mod` — MUST
- 10: `/boot/flatcar/grub/x86_64-xen/bfs.mod` — MUST
- 11: `/boot/flatcar/grub/x86_64-xen/bitmap.mod` — MUST
- 12: `/boot/flatcar/grub/x86_64-xen/bitmap_scale.mod` — MUST
- 13: `/boot/flatcar/grub/x86_64-xen/blocklist.mod` — MUST
- 14: `/boot/flatcar/grub/x86_64-xen/blscfg.mod` — MUST
- 15: `/boot/flatcar/grub/x86_64-xen/bufio.mod` — MUST
- 16: `/boot/flatcar/grub/x86_64-xen/cat.mod` — MUST
- 17: `/boot/flatcar/grub/x86_64-xen/cbfs.mod` — MUST
- 18: `/boot/flatcar/grub/x86_64-xen/cmp.mod` — MUST
- 19: `/boot/flatcar/grub/x86_64-xen/command.lst` — NOT
- 20: `/boot/flatcar/grub/x86_64-xen/cpio.mod` — MUST
- 21: `/boot/flatcar/grub/x86_64-xen/cpio_be.mod` — MUST
- 22: `/boot/flatcar/grub/x86_64-xen/cpuid.mod` — MUST
- 23: `/boot/flatcar/grub/x86_64-xen/crc64.mod` — MUST
- 24: `/boot/flatcar/grub/x86_64-xen/crypto.lst` — NOT
- 25: `/boot/flatcar/grub/x86_64-xen/crypto.mod` — MUST
- 26: `/boot/flatcar/grub/x86_64-xen/cryptodisk.mod` — MUST
- 27: `/boot/flatcar/grub/x86_64-xen/date.mod` — MUST
- 28: `/boot/flatcar/grub/x86_64-xen/datehook.mod` — MUST
- 29: `/boot/flatcar/grub/x86_64-xen/datetime.mod` — MUST
- 30: `/boot/flatcar/grub/x86_64-xen/disk.mod` — MUST
- 31: `/boot/flatcar/grub/x86_64-xen/diskfilter.mod` — MUST
- 32: `/boot/flatcar/grub/x86_64-xen/div.mod` — MUST
- 33: `/boot/flatcar/grub/x86_64-xen/dm_nv.mod` — MUST
- 34: `/boot/flatcar/grub/x86_64-xen/elf.mod` — MUST
- 35: `/boot/flatcar/grub/x86_64-xen/eval.mod` — MUST
- 36: `/boot/flatcar/grub/x86_64-xen/exfat.mod` — MUST
- 37: `/boot/flatcar/grub/x86_64-xen/ext2.mod` — MUST
- 38: `/boot/flatcar/grub/x86_64-xen/f2fs.mod` — MUST
- 39: `/boot/flatcar/grub/x86_64-xen/fdt.lst` — NOT
- 40: `/boot/flatcar/grub/x86_64-xen/file.mod` — MUST
- 41: `/boot/flatcar/grub/x86_64-xen/font.mod` — MUST
- 42: `/boot/flatcar/grub/x86_64-xen/fs.lst` — NOT
- 43: `/boot/flatcar/grub/x86_64-xen/fshelp.mod` — MUST
- 44: `/boot/flatcar/grub/x86_64-xen/gcry_arcfour.mod` — MUST
- 45: `/boot/flatcar/grub/x86_64-xen/gcry_blowfish.mod` — MUST
- 46: `/boot/flatcar/grub/x86_64-xen/gcry_camellia.mod` — MUST
- 47: `/boot/flatcar/grub/x86_64-xen/gcry_cast5.mod` — MUST
- 48: `/boot/flatcar/grub/x86_64-xen/gcry_crc.mod` — MUST
- 49: `/boot/flatcar/grub/x86_64-xen/gcry_des.mod` — MUST
- 50: `/boot/flatcar/grub/x86_64-xen/gcry_dsa.mod` — MUST
- 51: `/boot/flatcar/grub/x86_64-xen/gcry_idea.mod` — MUST
- 52: `/boot/flatcar/grub/x86_64-xen/gcry_md4.mod` — MUST
- 53: `/boot/flatcar/grub/x86_64-xen/gcry_md5.mod` — MUST
- 54: `/boot/flatcar/grub/x86_64-xen/gcry_rfc2268.mod` — MUST
- 55: `/boot/flatcar/grub/x86_64-xen/gcry_rijndael.mod` — MUST
- 56: `/boot/flatcar/grub/x86_64-xen/gcry_rmd160.mod` — MUST
- 57: `/boot/flatcar/grub/x86_64-xen/gcry_rsa.mod` — MUST
- 58: `/boot/flatcar/grub/x86_64-xen/gcry_seed.mod` — MUST
- 59: `/boot/flatcar/grub/x86_64-xen/gcry_serpent.mod` — MUST
- 60: `/boot/flatcar/grub/x86_64-xen/gcry_sha1.mod` — MUST
- 61: `/boot/flatcar/grub/x86_64-xen/gcry_sha256.mod` — MUST
- 62: `/boot/flatcar/grub/x86_64-xen/gcry_sha512.mod` — MUST
- 63: `/boot/flatcar/grub/x86_64-xen/gcry_tiger.mod` — MUST
- 64: `/boot/flatcar/grub/x86_64-xen/gcry_twofish.mod` — MUST
- 65: `/boot/flatcar/grub/x86_64-xen/gcry_whirlpool.mod` — MUST
- 66: `/boot/flatcar/grub/x86_64-xen/geli.mod` — MUST
- 67: `/boot/flatcar/grub/x86_64-xen/gettext.mod` — MUST
- 68: `/boot/flatcar/grub/x86_64-xen/gfxmenu.mod` — MUST
- 69: `/boot/flatcar/grub/x86_64-xen/gfxterm.mod` — MUST
- 70: `/boot/flatcar/grub/x86_64-xen/gfxterm_background.mod` — MUST
- 71: `/boot/flatcar/grub/x86_64-xen/gpt.mod` — MUST
- 72: `/boot/flatcar/grub/x86_64-xen/gptrepair.mod` — MUST
- 73: `/boot/flatcar/grub/x86_64-xen/gptsync.mod` — MUST
- 74: `/boot/flatcar/grub/x86_64-xen/gzio.mod` — MUST
- 75: `/boot/flatcar/grub/x86_64-xen/halt.mod` — MUST
- 76: `/boot/flatcar/grub/x86_64-xen/hashsum.mod` — MUST
- 77: `/boot/flatcar/grub/x86_64-xen/hello.mod` — MUST
- 78: `/boot/flatcar/grub/x86_64-xen/help.mod` — MUST
- 79: `/boot/flatcar/grub/x86_64-xen/hexdump.mod` — MUST
- 80: `/boot/flatcar/grub/x86_64-xen/hfs.mod` — MUST
- 81: `/boot/flatcar/grub/x86_64-xen/hfsplus.mod` — MUST
- 82: `/boot/flatcar/grub/x86_64-xen/hfspluscomp.mod` — MUST
- 83: `/boot/flatcar/grub/x86_64-xen/http.mod` — MUST
- 84: `/boot/flatcar/grub/x86_64-xen/increment.mod` — MUST
- 85: `/boot/flatcar/grub/x86_64-xen/iso9660.mod` — MUST
- 86: `/boot/flatcar/grub/x86_64-xen/jfs.mod` — MUST
- 87: `/boot/flatcar/grub/x86_64-xen/jpeg.mod` — MUST
- 88: `/boot/flatcar/grub/x86_64-xen/json.mod` — MUST
- 89: `/boot/flatcar/grub/x86_64-xen/keystatus.mod` — MUST
- 90: `/boot/flatcar/grub/x86_64-xen/ldm.mod` — MUST
- 91: `/boot/flatcar/grub/x86_64-xen/legacycfg.mod` — MUST
- 92: `/boot/flatcar/grub/x86_64-xen/linux.mod` — MUST
- 93: `/boot/flatcar/grub/x86_64-xen/load.cfg` — UNKNOWN
- 94: `/boot/flatcar/grub/x86_64-xen/loadenv.mod` — MUST
- 95: `/boot/flatcar/grub/x86_64-xen/loopback.mod` — MUST
- 96: `/boot/flatcar/grub/x86_64-xen/ls.mod` — MUST
- 97: `/boot/flatcar/grub/x86_64-xen/lsmmap.mod` — MUST
- 98: `/boot/flatcar/grub/x86_64-xen/lsxen.mod` — MUST
- 99: `/boot/flatcar/grub/x86_64-xen/luks.mod` — MUST
- 100: `/boot/flatcar/grub/x86_64-xen/luks2.mod` — MUST
- 101: `/boot/flatcar/grub/x86_64-xen/lvm.mod` — MUST
- 102: `/boot/flatcar/grub/x86_64-xen/lzopio.mod` — MUST
- 103: `/boot/flatcar/grub/x86_64-xen/macbless.mod` — MUST
- 104: `/boot/flatcar/grub/x86_64-xen/macho.mod` — MUST
- 105: `/boot/flatcar/grub/x86_64-xen/mdraid09.mod` — MUST
- 106: `/boot/flatcar/grub/x86_64-xen/mdraid09_be.mod` — MUST
- 107: `/boot/flatcar/grub/x86_64-xen/mdraid1x.mod` — MUST
- 108: `/boot/flatcar/grub/x86_64-xen/memrw.mod` — MUST
- 109: `/boot/flatcar/grub/x86_64-xen/minicmd.mod` — MUST
- 110: `/boot/flatcar/grub/x86_64-xen/minix.mod` — MUST
- 111: `/boot/flatcar/grub/x86_64-xen/minix2.mod` — MUST
- 112: `/boot/flatcar/grub/x86_64-xen/minix2_be.mod` — MUST
- 113: `/boot/flatcar/grub/x86_64-xen/minix3.mod` — MUST
- 114: `/boot/flatcar/grub/x86_64-xen/minix3_be.mod` — MUST
- 115: `/boot/flatcar/grub/x86_64-xen/minix_be.mod` — MUST
- 116: `/boot/flatcar/grub/x86_64-xen/moddep.lst` — NOT
- 117: `/boot/flatcar/grub/x86_64-xen/mpi.mod` — MUST
- 118: `/boot/flatcar/grub/x86_64-xen/msdospart.mod` — MUST
- 119: `/boot/flatcar/grub/x86_64-xen/net.mod` — MUST
- 120: `/boot/flatcar/grub/x86_64-xen/newc.mod` — MUST
- 121: `/boot/flatcar/grub/x86_64-xen/nilfs2.mod` — MUST
- 122: `/boot/flatcar/grub/x86_64-xen/ntfs.mod` — MUST
- 123: `/boot/flatcar/grub/x86_64-xen/ntfscomp.mod` — MUST
- 124: `/boot/flatcar/grub/x86_64-xen/odc.mod` — MUST
- 125: `/boot/flatcar/grub/x86_64-xen/offsetio.mod` — MUST
- 126: `/boot/flatcar/grub/x86_64-xen/part_acorn.mod` — MUST
- 127: `/boot/flatcar/grub/x86_64-xen/part_amiga.mod` — MUST
- 128: `/boot/flatcar/grub/x86_64-xen/part_apple.mod` — MUST
- 129: `/boot/flatcar/grub/x86_64-xen/part_bsd.mod` — MUST
- 130: `/boot/flatcar/grub/x86_64-xen/part_dfly.mod` — MUST
- 131: `/boot/flatcar/grub/x86_64-xen/part_dvh.mod` — MUST
- 132: `/boot/flatcar/grub/x86_64-xen/part_msdos.mod` — MUST
- 133: `/boot/flatcar/grub/x86_64-xen/part_plan.mod` — MUST
- 134: `/boot/flatcar/grub/x86_64-xen/part_sun.mod` — MUST
- 135: `/boot/flatcar/grub/x86_64-xen/part_sunpc.mod` — MUST
- 136: `/boot/flatcar/grub/x86_64-xen/partmap.lst` — NOT
- 137: `/boot/flatcar/grub/x86_64-xen/parttool.lst` — NOT
- 138: `/boot/flatcar/grub/x86_64-xen/parttool.mod` — MUST
- 139: `/boot/flatcar/grub/x86_64-xen/password.mod` — MUST
- 140: `/boot/flatcar/grub/x86_64-xen/password_pbkdf2.mod` — MUST
- 141: `/boot/flatcar/grub/x86_64-xen/pbkdf2.mod` — MUST
- 142: `/boot/flatcar/grub/x86_64-xen/pgp.mod` — MUST
- 143: `/boot/flatcar/grub/x86_64-xen/pkcs1_v15.mod` — MUST
- 144: `/boot/flatcar/grub/x86_64-xen/plainmount.mod` — MUST
- 145: `/boot/flatcar/grub/x86_64-xen/png.mod` — MUST
- 146: `/boot/flatcar/grub/x86_64-xen/priority_queue.mod` — MUST
- 147: `/boot/flatcar/grub/x86_64-xen/probe.mod` — MUST
- 148: `/boot/flatcar/grub/x86_64-xen/procfs.mod` — MUST
- 149: `/boot/flatcar/grub/x86_64-xen/progress.mod` — MUST
- 150: `/boot/flatcar/grub/x86_64-xen/raid5rec.mod` — MUST
- 151: `/boot/flatcar/grub/x86_64-xen/raid6rec.mod` — MUST
- 152: `/boot/flatcar/grub/x86_64-xen/reboot.mod` — MUST
- 153: `/boot/flatcar/grub/x86_64-xen/regexp.mod` — MUST
- 154: `/boot/flatcar/grub/x86_64-xen/reiserfs.mod` — MUST
- 155: `/boot/flatcar/grub/x86_64-xen/relocator.mod` — MUST
- 156: `/boot/flatcar/grub/x86_64-xen/romfs.mod` — MUST
- 157: `/boot/flatcar/grub/x86_64-xen/scsi.mod` — MUST
- 158: `/boot/flatcar/grub/x86_64-xen/search_fs_file.mod` — MUST
- 159: `/boot/flatcar/grub/x86_64-xen/search_label.mod` — MUST
- 160: `/boot/flatcar/grub/x86_64-xen/search_part_uuid.mod` — MUST
- 161: `/boot/flatcar/grub/x86_64-xen/setjmp.mod` — MUST
- 162: `/boot/flatcar/grub/x86_64-xen/sfs.mod` — MUST
- 163: `/boot/flatcar/grub/x86_64-xen/sleep.mod` — MUST
- 164: `/boot/flatcar/grub/x86_64-xen/squash4.mod` — MUST
- 165: `/boot/flatcar/grub/x86_64-xen/syslinuxcfg.mod` — MUST
- 166: `/boot/flatcar/grub/x86_64-xen/terminal.lst` — NOT
- 167: `/boot/flatcar/grub/x86_64-xen/testload.mod` — MUST
- 168: `/boot/flatcar/grub/x86_64-xen/testspeed.mod` — MUST
- 169: `/boot/flatcar/grub/x86_64-xen/tftp.mod` — MUST
- 170: `/boot/flatcar/grub/x86_64-xen/tga.mod` — MUST
- 171: `/boot/flatcar/grub/x86_64-xen/time.mod` — MUST
- 172: `/boot/flatcar/grub/x86_64-xen/tr.mod` — MUST
- 173: `/boot/flatcar/grub/x86_64-xen/trig.mod` — MUST
- 174: `/boot/flatcar/grub/x86_64-xen/true.mod` — MUST
- 175: `/boot/flatcar/grub/x86_64-xen/udf.mod` — MUST
- 176: `/boot/flatcar/grub/x86_64-xen/ufs1.mod` — MUST
- 177: `/boot/flatcar/grub/x86_64-xen/ufs1_be.mod` — MUST
- 178: `/boot/flatcar/grub/x86_64-xen/ufs2.mod` — MUST
- 179: `/boot/flatcar/grub/x86_64-xen/version.mod` — MUST
- 180: `/boot/flatcar/grub/x86_64-xen/video.lst` — NOT
- 181: `/boot/flatcar/grub/x86_64-xen/video.mod` — MUST
- 182: `/boot/flatcar/grub/x86_64-xen/video_colors.mod` — MUST
- 183: `/boot/flatcar/grub/x86_64-xen/video_fb.mod` — MUST
- 184: `/boot/flatcar/grub/x86_64-xen/videoinfo.mod` — MUST
- 185: `/boot/flatcar/grub/x86_64-xen/videotest.mod` — MUST
- 186: `/boot/flatcar/grub/x86_64-xen/xfs.mod` — MUST
- 187: `/boot/flatcar/grub/x86_64-xen/xnu_uuid.mod` — MUST
- 188: `/boot/flatcar/grub/x86_64-xen/zfs.mod` — MUST
- 189: `/boot/flatcar/grub/x86_64-xen/zfscrypt.mod` — MUST
- 190: `/boot/flatcar/grub/x86_64-xen/zfsinfo.mod` — MUST
- 191: `/boot/flatcar/grub/x86_64-xen/zstd.mod` — MUST
Corrected complete member map (supersedes earlier map):
- 1: `/etc/audit/audisp-filter.conf` — UNKNOWN
- 2: `/etc/audit/audisp-remote.conf` — UNKNOWN
- 3: `/etc/audit/audit-stop.rules` — MUST
- 4: `/etc/audit/audit.rules` — MUST
- 5: `/etc/audit/auditd.conf` — UNKNOWN
- 6: `/etc/audit/plugins.d` — UNKNOWN
- 7: `/etc/audit/rules.d` — MUST
Corrected complete member map (supersedes earlier map):
- 1: `/etc/selinux/config` — UNKNOWN
- 2: `/etc/selinux/mcs` — MUST
- 3: `/etc/selinux/mls` — MUST
- 4: `/etc/selinux/semanage.conf` — UNKNOWN
- 5: `/etc/selinux/targeted` — MUST
Corrected complete member map (supersedes earlier map):
- 1: `/etc/ssl/certs` — MUST
- 2: `/etc/ssl/fipsmodule.cnf` — UNKNOWN
- 3: `/etc/ssl/openssl.cnf` — UNKNOWN
- 4: `/etc/ssl/private` — NOT
Corrected complete member map (supersedes earlier map):
- 1: `/etc/systemd/coredump.conf` — UNKNOWN
- 2: `/etc/systemd/journal-remote.conf` — UNKNOWN
- 3: `/etc/systemd/journal-upload.conf` — UNKNOWN
- 4: `/etc/systemd/journald.conf` — UNKNOWN
- 5: `/etc/systemd/logind.conf` — UNKNOWN
- 6: `/etc/systemd/network` — NOT
- 7: `/etc/systemd/networkd.conf` — UNKNOWN
- 8: `/etc/systemd/oomd.conf` — UNKNOWN
- 9: `/etc/systemd/pstore.conf` — UNKNOWN
- 10: `/etc/systemd/resolved.conf` — UNKNOWN
- 11: `/etc/systemd/sleep.conf` — UNKNOWN
- 12: `/etc/systemd/system` — MUST
- 13: `/etc/systemd/system.conf` — UNKNOWN
- 14: `/etc/systemd/timesyncd.conf` — UNKNOWN
- 15: `/etc/systemd/user` — NOT
- 16: `/etc/systemd/user.conf` — UNKNOWN
Corrected complete member map (supersedes earlier map):
- 1: `/etc/.ignition-result.json` — NOT
- 2: `/etc/.pwd.lock` — UNKNOWN
- 3: `/etc/.systemd-confext` — MUST
- 4: `/etc/.updated` — UNKNOWN
- 5: `/etc/X11` — MUST
- 6: `/etc/audit` — MUST
- 7: `/etc/azure-ephemeral-disk-setup.conf` — UNKNOWN
- 8: `/etc/bash` — MUST
- 9: `/etc/bindresvport.blacklist` — UNKNOWN
- 10: `/etc/binfmt.d` — NOT
- 11: `/etc/cifs-utils` — UNKNOWN
- 12: `/etc/cni` — UNKNOWN
- 13: `/etc/conntrackd` — UNKNOWN
- 14: `/etc/coreos` — UNKNOWN
- 15: `/etc/credstore` — UNKNOWN
- 16: `/etc/credstore.encrypted` — UNKNOWN
- 17: `/etc/dbus-1` — MUST
- 18: `/etc/default` — MUST
- 19: `/etc/dracut.conf` — UNKNOWN
- 20: `/etc/e2scrub.conf` — UNKNOWN
- 21: `/etc/environment.d` — MUST
- 22: `/etc/ethertypes` — UNKNOWN
- 23: `/etc/extension-release.d` — MUST
- 24: `/etc/extensions` — MUST
- 25: `/etc/flatcar` — UNKNOWN
- 26: `/etc/group` — MUST
- 27: `/etc/group-` — NOT
- 28: `/etc/gshadow` — MUST
- 29: `/etc/gshadow-` — NOT
- 30: `/etc/hosts` — MUST
- 31: `/etc/idmapd.conf` — UNKNOWN
- 32: `/etc/init.d` — UNKNOWN
- 33: `/etc/iscsi` — UNKNOWN
- 34: `/etc/isns` — UNKNOWN
- 35: `/etc/issue` — NOT
- 36: `/etc/kernel` — NOT
- 37: `/etc/kexec.conf` — UNKNOWN
- 38: `/etc/keyutils` — UNKNOWN
- 39: `/etc/krb5.conf.example` — NOT
- 40: `/etc/ld.so.cache` — UNKNOWN
- 41: `/etc/ldap.conf.sudo` — UNKNOWN
- 42: `/etc/lessfilter.d` — UNKNOWN
- 43: `/etc/libaudit.conf` — UNKNOWN
- 44: `/etc/locale.conf` — MUST
- 45: `/etc/login.defs` — MUST
- 46: `/etc/logrotate.conf` — UNKNOWN
- 47: `/etc/logrotate.d` — UNKNOWN
- 48: `/etc/lvm` — UNKNOWN
- 49: `/etc/machine-id` — MUST
- 50: `/etc/mke2fs.conf` — UNKNOWN
- 51: `/etc/modules-load.d` — NOT
- 52: `/etc/motd` — NOT
- 53: `/etc/mtab` — UNKNOWN
- 54: `/etc/netconfig` — UNKNOWN
- 55: `/etc/nscd.conf` — UNKNOWN
- 56: `/etc/ntp.conf` — UNKNOWN
- 57: `/etc/nvme` — UNKNOWN
- 58: `/etc/openldap` — UNKNOWN
- 59: `/etc/pam.d` — NOT
- 60: `/etc/passwd` — MUST
- 61: `/etc/passwd-` — NOT
- 62: `/etc/pkcs11` — NOT
- 63: `/etc/polkit-1` — NOT
- 64: `/etc/profile.d` — MUST
- 65: `/etc/quotagrpadmins` — UNKNOWN
- 66: `/etc/quotatab` — UNKNOWN
- 67: `/etc/request-key.conf` — MUST
- 68: `/etc/request-key.d` — MUST
- 69: `/etc/resolv.conf` — MUST
- 70: `/etc/runlevels` — UNKNOWN
- 71: `/etc/sasl2` — UNKNOWN
- 72: `/etc/securetty` — MUST
- 73: `/etc/security` — NOT
- 74: `/etc/selinux` — MUST
- 75: `/etc/sestatus.conf` — UNKNOWN
- 76: `/etc/shadow` — UNKNOWN
- 77: `/etc/shadow-` — NOT
- 78: `/etc/skel` — UNKNOWN
- 79: `/etc/ssh` — MUST
- 80: `/etc/ssl` — MUST
- 81: `/etc/sssd` — MUST
- 82: `/etc/subgid` — MUST
- 83: `/etc/subgid-` — NOT
- 84: `/etc/subuid` — MUST
- 85: `/etc/subuid-` — NOT
- 86: `/etc/sudo_logsrvd.conf` — UNKNOWN
- 87: `/etc/sudoers.d` — NOT
- 88: `/etc/sudoers.dist` — UNKNOWN
- 89: `/etc/sysconfig` — UNKNOWN
- 90: `/etc/systemd` — MUST
- 91: `/etc/tcsd.conf` — UNKNOWN
- 92: `/etc/tmpfiles.d` — NOT
- 93: `/etc/tpm2-tss` — UNKNOWN
- 94: `/etc/udev` — MUST
- 95: `/etc/user` — UNKNOWN
- 96: `/etc/vim` — UNKNOWN
- 97: `/etc/warnquota.conf` — UNKNOWN
- 98: `/etc/whois.conf` — UNKNOWN
- 99: `/etc/wireguard` — UNKNOWN
- 100: `/etc/xattr.conf` — UNKNOWN
- 101: `/etc/xdg` — NOT

## Final review correction: GRUB indexes
The 18 `.lst` members in the BIOS and Xen groups are NOT under S2.2-7 and S2.2-13: they supply values only to GRUB. General capability dependence does not override the explicit program-local setting exemption. Earlier HOLE mappings for these indexes are superseded by the last corrected complete member maps. Native modules remain MUST, construction inputs UNKNOWN, and saved MBR bytes HOLE. Ancestor directory decisions remain unchanged because each affected directory still contains required native code.

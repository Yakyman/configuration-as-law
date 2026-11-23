# Unix groups on a Debian 13 (trixie) desktop: documented purpose and removal effect

Scope: the 68 groups listed in /etc/group on the examined system. Sources are Debian trixie package sources
(sources.debian.org, matching trixie versions), upstream systemd v257.13 (the version in trixie), and Debian
trixie man pages. Quotes from the base-passwd SGML document have markup and line breaks removed; otherwise they are verbatim.
"Removal" means deleting the group's line from /etc/group (and /etc/gshadow) and leaving everything else as it is.

## How removal works (applies to rows tagged [N1]–[N9])

- [N1] udev resolves `GROUP="name"` when rules load. If the name is unknown, it logs `"Unknown %s '%s', ignoring."` and the node does not get that group.
  Code: https://github.com/systemd/systemd/blob/v257.13/src/udev/udev-rules.c (log_unknown_owner / rule_resolve_group).
  Trixie rules that name groups: https://sources.debian.org/src/systemd/257.13-1~deb13u1/rules.d/50-udev-default.rules.in/ (tty, dialout, kmem, input, video, render, sgx, audio, lp, disk, cdrom, tape, kvm),
  plus https://sources.debian.org/src/systemd/257.13-1~deb13u1/debian/extra/rules/80-debian-compat.rules/ (dialout, kmem, cdrom, video).
  These rules mention neither `floppy` nor `clock` (checked: the trixie 50-udev-default rules, all 41 upstream v257.13 rules.d files, and Debian's extra rules).
- [N2] systemd-tmpfiles rejects a line whose group cannot be resolved: `"Failed to resolve group '%s': %m"`.
  Code: https://github.com/systemd/systemd/blob/v257.13/src/tmpfiles/tmpfiles.c . Lines that name groups:
  https://sources.debian.org/src/systemd/257.13-1~deb13u1/tmpfiles.d/systemd.conf.in/ (utmp, systemd-journal, ACLs for adm; Debian builds with -Dwheel-group=false),
  https://sources.debian.org/src/systemd/257.13-1~deb13u1/tmpfiles.d/var.conf.in/ (utmp),
  https://sources.debian.org/src/systemd/257.13-1~deb13u1/tmpfiles.d/static-nodes-permissions.conf.in/ (audio, disk, kvm),
  https://sources.debian.org/src/systemd/257.13-1~deb13u1/tmpfiles.d/systemd-network.conf/ (systemd-network).
- [N3] An account whose primary GID has no group entry fails a pwck check. pwck(8) lists the check "a valid primary group", and the code prints `"user '%s': no group %lu"` (it uses getgrgid).
  https://manpages.debian.org/trixie/passwd/pwck.8.en.html ; https://sources.debian.org/src/shadow/1:4.17.4-2/src/pwck.c/ .
  For rows that cite only [N3], this is the only effect the documentation establishes. The kernel keeps using the numeric GID.
- [N4] A systemd unit with `Group=name` fails to start when the name cannot be resolved: "216 EXIT_GROUP Failed to determine or change group credentials."
  https://manpages.debian.org/trixie/systemd/systemd.exec.5.en.html
- [N5] dpkg aborts package unpack/install if a statoverride names a group that no longer exists: "unknown system group '%s' in statoverride file; the system group got removed before the override".
  https://sources.debian.org/src/dpkg/1.22.22/lib/dpkg/db-fsys-override.c/ (STATDB_PARSE_NORMAL is used in src/main/archives.c).
- [N6] Some removed entries come back later, and the effects above last only until then:
  - update-passwd "updates all entries in the global system range (that is, 0–99)" (https://manpages.debian.org/trixie/base-passwd/update-passwd.8.en.html).
  - systemd-sysusers recreates groups declared in sysusers.d (basic.conf, debian/udev.debian-udev.sysusers). Its unit runs on `ConditionNeedsUpdate=|/etc` or when a package postinst calls it.
  - Several package postinst scripts re-add their group on the next configure: shadow, _ssh, scanner, netdev, pulse-access, ssl-cert.
- [N7] nss-systemd "ensures that the root and nobody users and groups (i.e. the users/groups with the UIDs/GIDs 0 and 65534) remain resolvable at all times". This holds only if "systemd" is listed in nsswitch.conf; Debian's default nsswitch.conf lists only "files".
  Systemd's own tools also synthesize root and nobody internally (src/basic/user-util.c). Debian builds systemd with -Dnobody-group=nogroup.
  https://manpages.debian.org/trixie/libnss-systemd/nss-systemd.8.en.html
- [N8] CUPS (Debian 2.4.10): FatalErrors defaults to "config". Debian's cups-files.conf sets `LogFileGroup adm` and `SystemGroup root lpadmin` (built with `--with-system-groups="root lpadmin"`).
  An unknown LogFileGroup or SystemGroup makes the config load fail ("Unknown LogFileGroup", "Unknown SystemGroup"), so cupsd does not start.
  The default Group `lp` is looked up with getgrnam. If that fails, cupsd falls back to group "nobody" (absent on Debian) and then to the historical NFS nobody GID.
  https://sources.debian.org/src/cups/2.4.10-3+deb13u2/scheduler/conf.c/ ; https://sources.debian.org/src/cups/2.4.10-3+deb13u2/conf/cups-files.conf.in/ ; https://sources.debian.org/src/cups/2.4.10-3+deb13u2/debian/rules/
- [N9] Exim (Debian 4.98.2): a fixed `group =` option is resolved while the configuration is read, and failure is fatal: `log_write(0, LOG_PANIC_DIE|LOG_CONFIG_IN, "group %s was not found", sptr)`.
  The Debian transport mail_spool sets `group = mail`. EXIM_GROUP=ref:Debian-exim is also looked up at runtime: `exim_fail("exim: failed to find gid for group name ...")`.
  https://sources.debian.org/src/exim4/4.98.2-1+deb13u5/src/readconf.c/ ; https://sources.debian.org/src/exim4/4.98.2-1+deb13u5/src/exim.c/ ; https://sources.debian.org/src/exim4/4.98.2-1+deb13u5/debian/debconf/conf.d/transport/30_exim4-config_mail_spool/

BP below = https://sources.debian.org/src/base-passwd/3.6.7/doc/users-and-groups.sgml/ (base-passwd "Users and Groups in the Debian System", trixie version).

## Table

| group | what it governs (≤15 words) | removal effect | URL | quoted passage (≤25 words) |
|---|---|---|---|---|
| root | Superuser group, GID 0; primary group of root | UNKNOWN: GID 0 stays resolvable only via nss-systemd; otherwise pwck flags root [N7][N3] | BP | "Root is (typically) the superuser." |
| daemon | Legacy shared group for unprivileged daemons that write files (atd, portmap) | CHANGES: account daemon's primary GID 1 dangles; pwck error [N3] | BP | "Some unprivileged daemons that need to be able to write to some files on disk run as daemon.daemon" |
| bin | Legacy; no files documented as owned by it | CHANGES: account bin's primary GID 2 dangles; pwck error [N3] | BP | "No files on my system are owned by user or group bin. What good are they?" |
| sys | Historical owner of kernel sources; obsolete | CHANGES: account sys's primary GID 3 dangles; pwck error [N3] | BP | "Historically, the sys user and group owned the kernel sources and some related items like the include files, but this was obsoleted long ago" |
| adm | Reads logs in /var/log; journal ACLs; CUPS log file group | CHANGES: cupsd fails to start (LogFileGroup adm); journal ACL lines rejected [N8][N2] | BP | "Group adm is used for system monitoring tasks. Members of this group can read many log files in /var/log" |
| tty | Owns tty devices and /dev/vcs*; write and wall use it | CHANGES: udev ignores GROUP="tty" on ptmx/tty/vcs nodes [N1] | BP | "Tty devices and /dev/vcs* are owned by this group. This is used by write and wall to enable them to write to other people's ttys." |
| disk | Raw block device access (udev block, loop-control, btrfs-control) | CHANGES: udev ignores GROUP="disk"; tmpfiles loop-control line rejected [N1][N2] | BP | "Raw access to disks. Mostly equivalent to root access." |
| lp | Parallel/USB printer device nodes; CUPS default filter group | CHANGES: udev ignores GROUP="lp"; cupsd falls back; account lp dangles [N1][N8][N3] | BP | "The lp* devices are writable by this group so that users in it can access the parallel ports directly." |
| mail | Owns/writes mailboxes in /var/mail; Exim mail_spool transport group | CHANGES: Exim config read fails ("group mail was not found"); account mail dangles [N9][N3] | BP | "Mailboxes in /var/mail are owned and writable by group mail, as is explained in Debian Policy." |
| news | News servers and spool; inews sgid news | CHANGES: account news's primary GID 9 dangles; pwck error [N3] | BP | "Various news servers and other associated programs (such as suck) use user and group news in various ways." |
| uucp | UUCP subsystem spool and configuration; members may run uucico | CHANGES: account uucp's primary GID 10 dangles; pwck error [N3] | BP | "The uucp user and group is used by the UUCP subsystem. It owns spool and configuration files." |
| man | man-db cache in /var/cache/man | CHANGES: account man's primary GID 12 dangles; pwck error [N3] | BP | "The man program (sometimes) runs as user man, so it can write cat pages to /var/cache/man and update its databases there." |
| proxy | Proxy daemons without dedicated ids (squid, pdnsd) | CHANGES: account proxy's primary GID 13 dangles; pwck error [N3] | BP | "Like daemon, this user and group is used by some daemons (specifically, proxy daemons) that don't have dedicated user ids" |
| kmem | /dev/mem, /dev/kmem, /dev/port, /dev/nvram readable by group | CHANGES: udev ignores GROUP="kmem" on mem/kmem/port/nvram [N1] | BP | "/dev/kmem and similar files are readable by this group. This is mostly a BSD relic" |
| dialout | Serial ports (ttyS*, ttyUSB*, rfcomm*) via udev | CHANGES: member user loses serial-port group access; udev ignores GROUP="dialout" [N1] | BP | "Full and direct access to serial ports. Members of this group can reconfigure the modem, dial anywhere, etc." |
| fax | Fax software access | UNKNOWN: no members; docs do not name a trixie consumer | BP | "Allows members to use fax software to send or receive faxes." |
| voice | Voicemail on modem answering machines | UNKNOWN: no members; docs do not name a trixie consumer | BP | "Voicemail, useful for systems that use modems as answering machines." |
| cdrom | Optical drives (sr*, pktcdvd) via udev | CHANGES: udev ignores GROUP="cdrom" on optical drive nodes [N1] | BP | "This group can be used locally to give a set of users access to a CD-ROM drive." |
| floppy | Floppy drive access, local use only | NOTHING: no members; no trixie udev rule references it (checked) [N1] | BP | "This group can be used locally to give a set of users access to a floppy drive." |
| tape | SCSI tape and changer nodes via udev | CHANGES: udev ignores GROUP="tape" on scsi_tape/generic tape nodes [N1] | BP | "This group can be used locally to give a set of users access to a tape drive." |
| sudo | Full root via sudo (%sudo in sudoers) and polkit admin | CHANGES: member user loses sudo and polkit admin rights | BP | "Members of this group may run any command as any user when using sudo or pkexec" |
| audio | Sound devices /dev/snd/* via udev and static nodes | CHANGES: member pulse loses audio group; udev/tmpfiles drop GROUP="audio" [N1][N2] | BP | "This group can be used locally to give a set of users access to an audio device." |
| dip | Dialup IP: pppd, pon, poff | UNKNOWN: no members; pppd file group is numeric | BP | "Being in group dip allows you to use tools such as pppd, pon, and poff to make dialup connections to other systems" |
| www-data | Web servers' runtime identity and written data | CHANGES: account www-data's primary GID 33 dangles; pwck error [N3] | BP | "Some web servers run as www-data. Web content should not be owned by this user" |
| backup | Delegating backup/restore without full root (documented with uncertainty) | CHANGES: account backup's primary GID 34 dangles; pwck error [N3] | BP | "Presumably so backup/restore responsibilities can be locally delegated to someone without full root permissions?" |
| operator | Historical: dump -n notifies operators via wall | UNKNOWN: no members; docs give only the historical dump use | BP | "The operator group is used by dump -n to notify logged-in operators via wall when it requires operator attention. This is a historical use" |
| list | Mailing list archives and data | CHANGES: account list's primary GID 38 dangles; pwck error [N3] | BP | "Mailing list archives and data are owned by this user and group." |
| irc | IRC daemons | CHANGES: account irc's primary GID 39 dangles; pwck error [N3] | BP | "Used by IRC daemons." |
| src | Owns source code under /usr/src | UNKNOWN: no members; docs show no name lookup | BP | "This group owns source code, including files in /usr/src. It can be used locally to give a user the ability to manage system source code." |
| shadow | /etc/shadow read access; setgid helpers | UNKNOWN: file GIDs are numeric; passwd postinst re-adds GID 42 [N6] | BP | "/etc/shadow is readable by this group. Some programs that need to be able to access the file are setgid shadow." |
| utmp | Write access to utmp, wtmp, btmp, lastlog | CHANGES: tmpfiles rejects /run/utmp, wtmp, btmp, lastlog lines [N2] | BP | "This group can write to /run/utmp, /var/log/wtmp, /var/log/lastlog, and similar files." |
| video | V4L, DRM card, framebuffer, DVB, media, lirc nodes | CHANGES: udev ignores GROUP="video" on video/DRM/media nodes [N1] | BP | "This group can be used locally to give a set of users access to a video device." |
| sasl | Read/write access to /etc/sasldb2 | UNKNOWN: no members; docs show no name lookup | BP | "Users in this group have read/write access to /etc/sasldb and/or /etc/sasldb2" |
| plugdev | Removable devices without fstab; primary group of usbmux | CHANGES: account usbmux's primary GID 46 dangles; pwck error [N3] | BP | "Members of this group can access removable devices in limited ways without explicit configuration in /etc/fstab." |
| staff | Local modifications in /usr/local and /home | UNKNOWN: no members; docs show no name lookup | BP | "Allows users to add local modifications to the system (/usr/local, /home) without needing root privileges." |
| games | sgid games for high-score files | CHANGES: account games's primary GID 60 dangles; pwck error [N3] | BP | "Many games are sgid to games so they can write their high score files." |
| users | Shared group for non-system users (adduser USERS_GROUP, EXTRA_GROUPS) | UNKNOWN: no members; used only for non-default adduser settings | BP | "In that system, each user is a member of the 'users' group." |
| nogroup | Group for daemons owning no files; primary of nobody, sync | UNKNOWN: stays resolvable only via nss-systemd; otherwise pwck flags nobody/sync [N7][N3] | BP | "Daemons that need not own any files sometimes run as user nobody and group nogroup" |
| systemd-journal | Read access to journal files | CHANGES: tmpfiles rejects /run and /var/log/journal ownership lines [N2] | https://manpages.debian.org/trixie/systemd/systemd-journald.service.8.en.html | "Journal files are, by default, owned and readable by the "systemd-journal" system group but are not writable." |
| systemd-network | systemd-networkd identity; /run/systemd/netif, /var/lib/systemd/network | CHANGES: tmpfiles rejects netif and network lines; account dangles [N2][N3] | https://sources.debian.org/src/systemd/257.13-1~deb13u1/tmpfiles.d/systemd-network.conf/ | "d$ /run/systemd/netif 0755 systemd-network systemd-network -" |
| systemd-timesync | systemd-timesyncd service identity | CHANGES: account systemd-timesync's primary GID dangles; pwck error [N3] | https://sources.debian.org/src/systemd/257.13-1~deb13u1/sysusers.d/systemd-timesync.conf.in/ | "u! systemd-timesync {{SYSTEMD_TIMESYNC_UID}} "systemd Time Synchronization"" |
| uuidd | UUID generation daemon identity | CHANGES: uuidd.service (Group=uuidd) fails, exit 216/GROUP [N4][N3] | https://sources.debian.org/src/util-linux/2.41.5-0+deb13u1/misc-utils/uuidd.service.in/ | "User=uuidd Group=uuidd" |
| messagebus | D-Bus system bus daemon identity | CHANGES: account messagebus's primary GID dangles; pwck error [N3] | BP | "The dbus daemon (dbus-daemon-1) runs as this user and group." |
| tcpdump | Unprivileged identity tcpdump switches to after opening capture | CHANGES: account tcpdump's primary GID dangles; pwck error [N3] | https://manpages.debian.org/trixie/tcpdump/tcpdump.8.en.html | "change the user ID to user and the group ID to the primary group of user. This behavior is enabled by default (-Z tcpdump)" |
| input | Input event devices (/dev/input/*) | CHANGES: udev ignores GROUP="input" on input nodes [N1] | https://sources.debian.org/src/systemd/257.13-1~deb13u1/rules.d/50-udev-default.rules.in/ | "SUBSYSTEM=="input", GROUP="input"" |
| sgx | Intel SGX enclave device nodes | CHANGES: udev ignores GROUP="sgx" on sgx_enclave/sgx_vepc [N1] | https://sources.debian.org/src/systemd/257.13-1~deb13u1/rules.d/50-udev-default.rules.in/ | "SUBSYSTEM=="misc", KERNEL=="sgx_enclave", GROUP="sgx", MODE="0660"" |
| clock | Declared by Debian udev "for PTP rules"; no trixie rule assigns it | NOTHING: no members; no trixie udev rule references it (checked) [N1] | https://sources.debian.org/src/systemd/257.13-1~deb13u1/debian/changelog/ | "udev: add 'clock' system group for PTP rules" |
| kvm | /dev/kvm, vhost-net, vhost-vsock, udmabuf (mode 0660 on Debian) | CHANGES: udev/tmpfiles drop GROUP="kvm" on /dev/kvm, vhost nodes [N1][N2] | https://sources.debian.org/src/systemd/257.13-1~deb13u1/rules.d/50-udev-default.rules.in/ | "KERNEL=="kvm", GROUP="kvm", MODE="{{DEV_KVM_MODE}}", OPTIONS+="static_node=kvm"" |
| render | GPU render nodes renderD*, kfd, accel (mode 0660 on Debian) | CHANGES: udev ignores GROUP="render" on render/kfd/accel nodes [N1] | https://sources.debian.org/src/systemd/257.13-1~deb13u1/rules.d/50-udev-default.rules.in/ | "SUBSYSTEM=="drm", KERNEL=="renderD*", GROUP="render", MODE="{{GROUP_RENDER_MODE}}"" |
| systemd-resolve | systemd-resolved service identity | CHANGES: account systemd-resolve's primary GID dangles; pwck error [N3] | https://sources.debian.org/src/systemd/257.13-1~deb13u1/sysusers.d/systemd-resolve.conf.in/ | "u! systemd-resolve {{SYSTEMD_RESOLVE_UID}} "systemd Resolver"" |
| _ssh | ssh-agent setgid group against ptrace | UNKNOWN: file GID is numeric; openssh-client postinst re-adds it [N6] | BP | "ssh-agent is setgid to _ssh in order to prevent ptrace attacks." |
| polkitd | polkit authority daemon identity | CHANGES: account polkitd's primary GID dangles; pwck error [N3] | https://manpages.debian.org/trixie/polkitd/polkit.8.en.html | "which itself has little privilege as it is running as the polkitd system user." |
| user | Personal group of the login user (adduser USERGROUPS=yes) | CHANGES: account user's primary GID 1000 dangles; pwck error [N3] | https://sources.debian.org/src/adduser/3.152/adduser.conf/ | "Specify whether each created non-system user will be given their own group to use. Default: USERGROUPS=yes" |
| crontab | crontab binary setgid; access to per-user crontab spool | CHANGES: dpkg install/unpack aborts on crontab statoverride [N5] | https://sources.debian.org/src/cron/3.0pl1-197/debian/cron.postinst/ | "dpkg-statoverride --update --add root crontab 2755 /usr/bin/crontab" |
| scanner | Scanner device ACLs (libsane udev rule); saned membership | CHANGES: libsane setfacl g:scanner fails; member saned loses scanner access | https://sources.debian.org/src/sane-backends/1.3.1-3/debian/99-libsane1.rules/ | "ENV{libsane_matched}=="yes", RUN+="/bin/setfacl -m g:scanner:rw $env{DEVNAME}"" |
| rtkit | RealtimeKit daemon identity | CHANGES: account rtkit's primary GID dangles; pwck error [N3] | https://sources.debian.org/src/rtkit/0.13-5.1/debian/rtkit.postinst/ | "--gecos "RealtimeKit" --group rtkit" |
| Debian-exim | Exim MTA runtime group, resolved by name at runtime | CHANGES: exim fails ("failed to find gid for group name") [N9] | https://sources.debian.org/src/exim4/4.98.2-1+deb13u5/debian/EDITME.exim4-light.diff/ | "+EXIM_GROUP=ref:Debian-exim" |
| netdev | D-Bus policy giving full Avahi access, incl. SetHostName | CHANGES: dbus-daemon warns "Unknown group" and drops the policy; no members | https://sources.debian.org/src/avahi/0.8-16/avahi-daemon/avahi-dbus.conf/ | "Allow everything, including access to SetHostName to users of the group "netdev"" |
| ssl-cert | Access to /etc/ssl/private and snakeoil key ownership | CHANGES: dpkg aborts on ssl-cert statoverride; make-ssl-cert chown fails [N5] | https://sources.debian.org/src/ssl-cert/1.1.3/debian/postinst/ | "dpkg-statoverride --update --add root ssl-cert 710 /etc/ssl/private" |
| avahi | avahi-daemon privilege drop target, looked up by name | CHANGES: avahi-daemon fails to drop privileges ("Failed to find group 'avahi'") | https://sources.debian.org/src/avahi/0.8-16/avahi-daemon/main.c/ | "if (!(gr = getgrnam(AVAHI_GROUP))) { avahi_log_error( "Failed to find group '"AVAHI_GROUP"'.");" |
| lpadmin | CUPS printer administration (SystemGroup); primary of cups-pk-helper | CHANGES: cupsd fails to start ("Unknown SystemGroup"); cups-pk-helper dangles [N8][N3] | BP | "Allows a user to add, modify, and remove printers from foomatic, cups, and possibly other printer databases." |
| _flatpak | Unprivileged helper identity for system-wide Flatpak installs | CHANGES: account _flatpak's primary GID dangles; pwck error [N3] | https://sources.debian.org/src/flatpak/1.16.6-1~deb13u3/debian/rules/ | "-Dsystem_helper_user=_flatpak" |
| pulse | PulseAudio daemon account (system mode) | CHANGES: account pulse's primary GID dangles; pwck error [N3] | https://sources.debian.org/src/pulseaudio/17.0+dfsg1-2/debian/pulseaudio.postinst/ | "--gecos "PulseAudio daemon" --group pulse" |
| pulse-access | Clients allowed to use system-wide PulseAudio (auth-group, system mode only) | UNKNOWN: no members; matters only in system mode, which docs cannot confirm here | https://sources.debian.org/src/pulseaudio/17.0+dfsg1-2/src/pulsecore/protocol-native.c/ | "pa_modargs_get_value(ma, "auth-group", pa_in_system_mode() ? PA_ACCESS_GROUP : NULL)" |
| saned | saned network scanner daemon identity | CHANGES: saned@.service (Group=saned) fails, exit 216/GROUP [N4][N3] | https://sources.debian.org/src/sane-backends/1.3.1-3/debian/sane-utils.saned@.service/ | "ExecStart=/usr/sbin/saned User=saned Group=saned" |
| lightdm | LightDM display manager/greeter account | CHANGES: account lightdm's primary GID dangles; pwck error [N3] | https://sources.debian.org/src/lightdm/1.32.0-6/debian/lightdm.postinst/ | "adduser --system --ingroup lightdm --home /var/lib/lightdm lightdm" |
| colord | colord colour management daemon account | CHANGES: account colord's primary GID dangles; pwck error [N3] | https://sources.debian.org/src/colord/1.4.7-3/debian/colord.postinst/ | "--quiet --gecos "colord colour management daemon" colord" |
| netdata | Netdata agent service group (unit runs User=root Group=netdata) | CHANGES: netdata.service (Group=netdata) fails, exit 216/GROUP [N4][N3] | https://github.com/netdata/netdata/blob/v2.13.0/system/systemd/netdata.service.in | "User=root Group=netdata" |

## Notes on specific rows

- sudo: Debian sudoers has `%sudo	ALL=(ALL:ALL) ALL` (https://sources.debian.org/src/sudo/1.9.16p2-3+deb13u5/debian/etc/sudoers/). Polkit 126 is built with `-Dos_type=debian`, which sets `privileged_group = 'sudo'` (https://sources.debian.org/src/policykit-1/126-2/meson.build/).
- saned: BP says the saned user/group "appear to be unused". The trixie sane-utils socket unit still runs saned with Group=saned, so the row follows the unit file.
- scanner, netdev, pulse-access, _ssh, shadow: the creating package's postinst re-adds the group on its next configure ([N6]).
- netdata is not packaged in trixie. The unit file cited is from netdata upstream release v2.13.0, and the installed unit was not inspected.
- floppy and clock are NOTHING only for the shipped systemd/udev rule set. Rules from other packages or local rules were not enumerated.

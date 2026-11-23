# Part 6: boot and system configuration subset

Decisions use Section 2.2 and S3-2. No removal test was run. Inventory file contents are unavailable; listed paths establish roles only where standard documentation identifies them. Evidence n counts sometimes exceed the members field; partial directory inventories are not assumed homogeneous.

## Rules

R1: explicitly enumerated boot executables are MUST under S2.2-1, S2.2-2 and S2.2-9. Their removal eliminates the corresponding available boot code.

R2: Forth scripts and their entrypoints are MUST under S2.2-10 and S2.2-13. The loader executes them; display-producing code remains code.

R3: explicitly enumerated shell scripts and shell-sourced files are MUST under S2.2-10 and S2.2-13. Shell rights are not restricted to a program interface.

R1 hand checks (path and inventory identity checked individually):
- freebsd-3620611c7e — /boot/boot — Provides executable bootstrapping code for a supported boot method.
- freebsd-9df0ab01a4 — /boot/boot0 — Provides executable bootstrapping code for a supported boot method.
- freebsd-3df86f4ce3 — /boot/boot0sio — Provides executable bootstrapping code for a supported boot method.
- freebsd-bd24f6d8a8 — /boot/boot1 — Provides executable bootstrapping code for a supported boot method.
- freebsd-f951e11455 — /boot/boot1.efi — Provides executable bootstrapping code for a supported boot method.
- freebsd-5061ac7aaa — /boot/boot2 — Provides executable bootstrapping code for a supported boot method.
- freebsd-afb66c345b — /boot/cdboot — Provides executable bootstrapping code for a supported boot method.
- freebsd-19d88e1e5a — /boot/gptboot — Provides executable bootstrapping code for a supported boot method.
- freebsd-28ebab0eba — /boot/gptboot.efi — Provides executable bootstrapping code for a supported boot method.
- freebsd-2591769d74 — /boot/gptzfsboot — Provides executable bootstrapping code for a supported boot method.

R2 hand checks (path and inventory identity checked individually):
- freebsd-af28845615 — /boot/beastie.4th — Executes boot-loader commands controlling startup or its display.
- freebsd-32044a825d — /boot/brand-fbsd.4th — Executes boot-loader commands controlling startup or its display.
- freebsd-78668f24af — /boot/brand.4th — Executes boot-loader commands controlling startup or its display.
- freebsd-cfac180345 — /boot/check-password.4th — Executes boot-loader commands controlling startup or its display.
- freebsd-b2efea8f22 — /boot/color.4th — Executes boot-loader commands controlling startup or its display.
- freebsd-bc4212531e — /boot/delay.4th — Executes boot-loader commands controlling startup or its display.
- freebsd-f44593fb1f — /boot/efi.4th — Executes boot-loader commands controlling startup or its display.
- freebsd-72bf4c42a9 — /boot/frames.4th — Executes boot-loader commands controlling startup or its display.
- freebsd-340ff3043f — /boot/loader.4th — Executes boot-loader commands controlling startup or its display.
- freebsd-65db8613c9 — /boot/loader.rc — Executes boot-loader commands controlling startup or its display.

R3 hand checks (path and inventory identity checked individually):
- freebsd-ebed2756ae — /etc/csh.cshrc — Executes shell commands for startup, system management, or environment initialization.
- freebsd-6dfa5e3768 — /etc/csh.login — Executes shell commands for startup, system management, or environment initialization.
- freebsd-edb359c9e6 — /etc/csh.logout — Executes shell commands for startup, system management, or environment initialization.
- freebsd-3543b3a205 — /etc/profile — Executes shell commands for startup, system management, or environment initialization.
- freebsd-891a2e4f4f — /etc/netstart — Executes shell commands for startup, system management, or environment initialization.
- freebsd-f40b077277 — /etc/network.subr — Executes shell commands for startup, system management, or environment initialization.
- freebsd-e4852775db — /etc/pccard_ether — Executes shell commands for startup, system management, or environment initialization.
- freebsd-b28c7e23e4 — /etc/rc — Executes shell commands for startup, system management, or environment initialization.
- freebsd-b30774ba74 — /etc/rc.bsdextended — Executes shell commands for startup, system management, or environment initialization.
- freebsd-e57ad5b3f8 — /etc/rc.conf — Executes shell commands for startup, system management, or environment initialization.

All other mappings are individual decisions. Unknown directory contents are not assigned a homogeneous classification. MIXED identifies already established different members while explicitly leaving unlisted members unresolved.

## Numbered sentences

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-3** The following need not be recorded:
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S3-2** If what the object does remains unknown, the case yields ?.

## Documentation

- https://man.freebsd.org/cgi/man.cgi?query=loader&sektion=8&format=ascii — "The program called loader is the final stage of FreeBSD's kernel bootstrap- ping process. It is responsible for bringing the kernel, kernel modules and other"
- https://man.freebsd.org/cgi/man.cgi?query=loader.conf&sektion=5&format=ascii — "The file loader.conf contains descriptive information on bootstrapping the system. Through it you can specify the kernel to be booted, parameters to be passed to"
- https://man.freebsd.org/cgi/man.cgi?query=loader_4th&sektion=8&format=ascii — "The program called loader_4th is the final stage of FreeBSD's kernel boot- strapping process. On IA32 (i386) architectures, it is a BTX client. It is"
- https://man.freebsd.org/cgi/man.cgi?query=loader_lua&sektion=8&format=ascii — "The program called loader_lua is the final stage of FreeBSD's kernel boot- strapping process. On IA32 (i386) architectures, it is a BTX client. It is"
- https://man.freebsd.org/cgi/man.cgi?query=boot&sektion=8&format=ascii — "Power fail and crash recovery. Normally, the system will reboot itself at power-up or after crashes. An automatic consistency check of the file sys- tems"
- https://man.freebsd.org/cgi/man.cgi?query=boot0cfg&sektion=8&format=ascii — "The FreeBSD `boot0' boot manager permits the operator to select from which disk and slice an i386 machine (PC) is booted. Note that what are"
- https://man.freebsd.org/cgi/man.cgi?query=gptboot&sektion=8&format=ascii — "gptboot is used on BIOS-based computers to boot from a UFS partition on a GPT-partitioned disk. gptboot is installed in a freebsd-boot partition with gpart(8)."
- https://man.freebsd.org/cgi/man.cgi?query=gptzfsboot&sektion=8&format=ascii — "gptzfsboot is used on BIOS-based computers to boot from a filesystem in a ZFS pool. gptzfsboot is installed in a freebsd-boot partition of a GPT-"
- https://man.freebsd.org/cgi/man.cgi?query=pxeboot&sektion=8&format=ascii — "The pxeboot bootloader is a modified version of the system third-stage bootstrap loader(8) configured to run under Intel's Preboot Execution Envi- ronment (PXE) system. PXE"
- https://man.freebsd.org/cgi/man.cgi?query=device.hints&sektion=5&format=ascii — "The device.hints file is read in by the boot loader(8) when the system is about to start, and its contents are passed to the kernel."
- https://man.freebsd.org/cgi/man.cgi?query=save-entropy&sektion=8&format=ascii — "The save-entropy command is used to save entropy data from /dev/random to files in a specified output location. The files saved are used at startup"
- https://man.freebsd.org/cgi/man.cgi?query=rc&sektion=8&format=ascii — "The rc utility is the command script which controls the automatic boot process after being called by init(8). The rc.local script contains com- mands which"
- https://man.freebsd.org/cgi/man.cgi?query=rc.conf&sektion=5&format=ascii — "The file rc.conf contains descriptive information about the local host name, configuration details for any potential network interfaces and which services should be started up"
- https://man.freebsd.org/cgi/man.cgi?query=csh&sektion=1&format=ascii — "tcsh is an enhanced but completely compatible version of the Berkeley UNIX C shell, csh(1). It is a command language interpreter usable both as an"
- https://man.freebsd.org/cgi/man.cgi?query=sh&sektion=1&format=ascii — "The sh utility is the standard command interpreter for the system. The current version of sh is close to the IEEE Std 1003.1 ("POSIX.1") specifi-"
- https://man.freebsd.org/cgi/man.cgi?query=crontab&sektion=5&format=ascii — "A crontab file contains instructions to the cron(8) daemon of the general form: ``run this command at this time on this date''. Each user has"
- https://man.freebsd.org/cgi/man.cgi?query=auto_master&sektion=5&format=ascii — "The automounter configuration consists of the auto_master configuration file, which assigns filesystem paths to map names, and maps, which contain actual mount information. The auto_master"
- https://man.freebsd.org/cgi/man.cgi?query=devd.conf&sektion=5&format=ascii — "General Syntax A devd(8) configuration consists of two general features, statements and comments. All statements end with a semicolon. Many statements can con- tain substatements,"
- https://man.freebsd.org/cgi/man.cgi?query=devfs.conf&sektion=5&format=ascii — "The devfs.conf file provides an easy way to set ownership and permissions, or create links for devices available at boot. It does not work for"
- https://man.freebsd.org/cgi/man.cgi?query=blacklistd.conf&sektion=5&format=ascii — "The blacklistd.conf file contains configuration entries for blacklistd(8) in a fashion similar to inetd.conf(5). Only one entry per line is permit- ted. Every entry must"
- https://man.freebsd.org/cgi/man.cgi?query=ddb&sektion=8&format=ascii — "The ddb utility configures certain aspects of the ddb(4) kernel debugger from user space that are not configured at compile-time or easily via sysctl(8) MIB"
- https://man.freebsd.org/cgi/man.cgi?query=dhclient.conf&sektion=5&format=ascii — "The dhclient.conf file contains configuration information for dhclient(8), the Internet Software Consortium DHCP Client. The dhclient.conf file is a free-form ASCII text file. It is"
- https://man.freebsd.org/cgi/man.cgi?query=disktab&sektion=5&format=ascii — "Disktab is a simple database which describes disk geometries and disk par- tition characteristics. It is used to initialize the disk label on the disk."
- https://man.freebsd.org/cgi/man.cgi?query=dump&sektion=8&format=ascii — "The dump utility examines files on a file system and determines which files need to be backed up. These files are copied to the given"
- https://man.freebsd.org/cgi/man.cgi?query=fbtab&sektion=5&format=ascii — "The fbtab file contains a number of lines specifying a device together with a list of devices with associated protections. Comments start with a `#'"
- https://man.freebsd.org/cgi/man.cgi?query=ftpusers&sektion=5&format=ascii — "The ftpusers file provides user access control for tnftpd(8) by defining which users may login. If the ftpusers file does not exist, all users are"
- https://man.freebsd.org/cgi/man.cgi?query=gettytab&sektion=5&format=ascii — "The gettytab file is a simplified version of the termcap(5) data base used to describe terminal lines. The initial terminal login process getty(8) accesses the"
- https://man.freebsd.org/cgi/man.cgi?query=group&sektion=5&format=ascii — "The group file is the local source of group information. It can be used in conjunction with the Hesiod domain `group', and the NIS maps"
- https://man.freebsd.org/cgi/man.cgi?query=hosts.allow&sektion=5&format=ascii — "This document describes optional extensions to the language described in the hosts_access(5) document. The extensions are enabled at program build time. For example, by editing"
- https://man.freebsd.org/cgi/man.cgi?query=hosts.equiv&sektion=5&format=ascii — "The hosts.equiv and .rhosts files contain information regarding trusted hosts and users on the network. For each host a single line should be present with"
- https://man.freebsd.org/cgi/man.cgi?query=hosts.lpd&sektion=5&format=ascii — "The hosts.lpd file contains a list of hostnames or IP addresses that are allowed to use your local print services. List every hostname or IP"
- https://man.freebsd.org/cgi/man.cgi?query=libalias&sektion=3&format=ascii — "The libalias library is a collection of functions for aliasing and de- aliasing of IP packets, intended for masquerading and network address translation (NAT). INTRODUCTION"
- https://man.freebsd.org/cgi/man.cgi?query=libmap.conf&sektion=5&format=ascii — "The libmap functionality of ld-elf.so.1(1) allows dynamic object dependen- cies to be mapped to arbitrary names. Each line in /etc/libmap.conf can have one of five"
- https://man.freebsd.org/cgi/man.cgi?query=locate.updatedb&sektion=8&format=ascii — "The locate.updatedb utility updates the database used by locate(1). It is typically run once a week by the /etc/periodic/weekly/310.locate script. The contents of the newly"
- https://man.freebsd.org/cgi/man.cgi?query=login.access&sektion=5&format=ascii — "The login.access file specifies (user, host) combinations and/or (user, tty) combinations for which a login will be either accepted or refused. When someone logs in,"
- https://man.freebsd.org/cgi/man.cgi?query=login.conf&sektion=5&format=ascii — "login.conf contains various attributes and capabilities of login classes. A login class (an optional annotation against each record in the user ac- count database, /etc/master.passwd)"
- https://man.freebsd.org/cgi/man.cgi?query=mac.conf&sektion=5&format=ascii — "The mac.conf file configures the default label elements to be used by pol- icy-agnostic applications that operate on MAC labels. A file contains a series"
- https://man.freebsd.org/cgi/man.cgi?query=mail&sektion=1&format=ascii — "MAIL(1) General Commands Manual MAIL(1) NAME mail, Mail, mailx -- send and receive mail SYNOPSIS mail [-dEiInv] [-s subject] [-c cc-addr] [-b bcc-addr] [-F] to-addr"
- https://man.freebsd.org/cgi/man.cgi?query=passwd&sektion=5&format=ascii — "The passwd files are the local source of password information. They can be used in conjunction with the Hesiod domains `passwd' and `uid', and the"
- https://man.freebsd.org/cgi/man.cgi?query=pwd_mkdb&sektion=8&format=ascii — "The pwd_mkdb utility creates db(3) style secure and insecure databases for the specified file. These databases are then installed into /etc/spwd.db and /etc/pwd.db respectively. The"
- https://man.freebsd.org/cgi/man.cgi?query=motd&sektion=5&format=ascii — "The file /var/run/motd is normally displayed by login(1) after a user has logged in but before the shell is run. It is generally used for"
- https://man.freebsd.org/cgi/man.cgi?query=netconfig&sektion=5&format=ascii — "The netconfig file defines a list of "transport names", describing their semantics and protocol. In FreeBSD, this file is only used by the RPC li-"
- https://man.freebsd.org/cgi/man.cgi?query=networks&sektion=5&format=ascii — "The networks file contains information regarding the known networks which comprise the DARPA Internet. For each network a single line should be present with the"
- https://man.freebsd.org/cgi/man.cgi?query=newsyslog.conf&sektion=5&format=ascii — "The newsyslog.conf file is used to set log file rotation configuration for the newsyslog(8) utility. Configuration may designate that logs are ro- tated based on"
- https://man.freebsd.org/cgi/man.cgi?query=nscd.conf&sektion=5&format=ascii — "The nscd.conf file is used by the nscd(8) daemon and is read on its startup. Its syntax is mostly similar to the nscd.conf syntax in"
- https://man.freebsd.org/cgi/man.cgi?query=nsmb.conf&sektion=5&format=ascii — "The nsmb.conf file contains information about the computers, users, and shares or mount points for the SMB network protocol. The configuration files are loaded in"
- https://man.freebsd.org/cgi/man.cgi?query=nsswitch.conf&sektion=5&format=ascii — "The nsswitch.conf file specifies how the nsdispatch(3) (name-service switch dispatcher) routines in the C library should operate. The configuration file controls how a process looks"
- https://man.freebsd.org/cgi/man.cgi?query=pf.os&sektion=5&format=ascii — "The pf(4) firewall and the tcpdump(1) program can both fingerprint the op- erating system of hosts that originate an IPv4 TCP connection. The file consists"
- https://man.freebsd.org/cgi/man.cgi?query=phones&sektion=5&format=ascii — "The file /etc/phones contains the system-wide private phone numbers for the tip(1) program. This file is normally unreadable, and so may contain priv- ileged information."
- https://man.freebsd.org/cgi/man.cgi?query=printcap&sektion=5&format=ascii — "The Printcap function is a simplified version of the termcap(5) data base used to describe line printers. The spooling system accesses the printcap file every"
- https://man.freebsd.org/cgi/man.cgi?query=protocols&sektion=5&format=ascii — "The protocols file contains information regarding the assigned protocol numbers used by IPv4 and IPv6 to identify the next level protocol. For each protocol a"
- https://man.freebsd.org/cgi/man.cgi?query=regdomain&sektion=5&format=ascii — "The regdomain.xml file describes regulations for the operation of IEEE 802.11 wireless radios. This information is used by the ifconfig(8) program to construct regulatory state"
- https://man.freebsd.org/cgi/man.cgi?query=remote&sektion=5&format=ascii — "The systems known by tip(1) and their attributes are stored in an ASCII file which is structured somewhat like the termcap(5) file. Each line in"
- https://man.freebsd.org/cgi/man.cgi?query=resolv.conf&sektion=5&format=ascii — "The resolver(3) is a set of routines in the C library which provide access to the Internet Domain Name System. The resolver configuration file con-"
- https://man.freebsd.org/cgi/man.cgi?query=rmt&sektion=8&format=ascii — "The rmt utility is used by the remote dump and restore programs in manipu- lating a magnetic tape drive through an interprocess communication connec- tion."
- https://man.freebsd.org/cgi/man.cgi?query=rpc&sektion=5&format=ascii — "The rpc file contains user readable names that can be used in place of RPC program numbers. For each RPC program a single line should"
- https://man.freebsd.org/cgi/man.cgi?query=services&sektion=5&format=ascii — "The services file contains information regarding the known services avail- able in the Internet. For each service a single line should be present with the"
- https://man.freebsd.org/cgi/man.cgi?query=shells&sektion=5&format=ascii — "The shells file contains a list of the shells on the system. For each shell a single line should be present, consisting of the shell's"
- https://man.freebsd.org/cgi/man.cgi?query=sysctl.conf&sektion=5&format=ascii — "The /etc/sysctl.conf file is read in when the system goes into multi-user mode to set default settings for the kernel. The /etc/sysctl.conf file is in"
- https://man.freebsd.org/cgi/man.cgi?query=syslog.conf&sektion=5&format=ascii — "The syslog.conf file is the configuration file for the syslogd(8) program. It consists of blocks of lines separated by program, hostname or property-based filter specifications"
- https://man.freebsd.org/cgi/man.cgi?query=termcap&sektion=5&format=ascii — "The termcap file is a data base describing terminals, used, for example, by vi(1) and ncurses(3). Terminals are described in termcap by giving a set"
- https://man.freebsd.org/cgi/man.cgi?query=ttys&sektion=5&format=ascii — "The file ttys contains information that is used by various routines to ini- tialize and control the use of terminal special files. Pseudo-terminals (see pts(4))"
- https://man.freebsd.org/cgi/man.cgi?query=os-release&sektion=5&format=ascii — "The os-release file is a new-line separated list of key value pairs. The syntax of this file is a reduced sh(1) variable assignment with the"
- https://man.freebsd.org/cgi/man.cgi?query=bhyveload&sektion=8&format=ascii — "bhyveload is used to load a FreeBSD guest inside a bhyve(4) virtual ma- chine. bhyveload is based on loader(8) and will present an interface identical"
- https://man.freebsd.org/cgi/man.cgi?query=bsnmpd&sektion=1&format=ascii — "The bsnmpd daemon serves the internet SNMP (Simple Network Management Pro- tocol). It is intended to serve only the absolute basic MIBs and implement all"
- https://man.freebsd.org/cgi/man.cgi?query=inetd&sektion=8&format=ascii — "The inetd utility should be run at boot time by /etc/rc (see rc(8)). It then listens for connections on certain internet sockets. When a connec-"
- https://man.freebsd.org/cgi/man.cgi?query=blacklistd&sektion=8&format=ascii — "blacklistd is a daemon similar to syslogd(8) that listens to sockets at paths specified in the sockpathsfile for notifications from other daemons about successful or"
- https://man.freebsd.org/cgi/man.cgi?query=freebsd-update.conf&sektion=5&format=ascii — "The freebsd-update.conf file controls the behaviour of the freebsd-up- date(8) utility. The file contains lines consisting of a case-sensitive option name and zero or more"
- https://man.freebsd.org/cgi/man.cgi?query=aliases&sektion=5&format=ascii — "This file describes user ID aliases used by sendmail. The file resides in /etc/mail and is formatted as a series of lines of the form"
- https://man.freebsd.org/cgi/man.cgi?query=devfs.rules&sektion=5&format=ascii — "The devfs.rules file provides an easy way to create and apply devfs(8) rules, even for devices that are not available at boot. For devices available"
- https://man.freebsd.org/cgi/man.cgi?query=gssapi&sektion=3&format=ascii — "gssapi(3) Heimdal GSS-API library gssapi(3) NAME gssapi - Heimdal GSS-API functions SYNOPSIS Functions GSSAPI_LIB_FUNCTION OM_uint32 GSSAPI_LIB_CALL gss_add_oid_set_member (OM_uint32 *minor_status, const gss_OID member_oid, gss_OID_set *oid_set) GSSAPI_LIB_FUNCTION"
- https://man.freebsd.org/cgi/man.cgi?query=cap_mkdb&sektion=1&format=ascii — "The cap_mkdb utility builds a hashed database out of the getcap(3) logical database constructed by the concatenation of the specified files. The database is named"
- https://man.freebsd.org/cgi/man.cgi?query=login_cap&sektion=3&format=ascii — "These functions represent a programming interface to the login classes database provided in login.conf(5). This database contains capabilities, attributes and default environment and accounting settings"
- https://man.freebsd.org/cgi/man.cgi?query=periodic&sektion=8&format=ascii — "The periodic utility is intended to be called by cron(8) to execute shell scripts located in the specified directory. One or more of the following"

Additional primary sources:
- https://raw.githubusercontent.com/freebsd/freebsd-src/main/share/man/man7/hier.7 — "defines the UUID for the local system, required for dbus"; "configuration files for the Pluggable Authentication Modules".
- https://raw.githubusercontent.com/freebsd/freebsd-src/main/stand/forth/Makefile — "FILES+= beastie.4th" and "FILES+= loader.4th" identify installed loader script names (whitespace normalized).
- https://raw.githubusercontent.com/freebsd/freebsd-src/main/libexec/rc/rc.d/hostid — "If ${hostid_file} already exists, we take UUID from there."
- https://raw.githubusercontent.com/freebsd/freebsd-src/main/usr.bin/locate/locate/updatedb.sh — ". $LOCATE_CONFIG" demonstrates shell sourcing of locate settings.

Boot script execution, system configuration effects, and directory membership are distinct facts. A documented general directory role does not establish the complete collection actually stored on the inventoried machine.

- https://man.freebsd.org/cgi/man.cgi?query=fstab&sektion=5&format=ascii — "The file fstab contains descriptive information about the various file sys- tems. fstab is only read by programs, and not written; it is the duty"

- https://man.freebsd.org/cgi/man.cgi?query=hosts&sektion=5&format=ascii — "The hosts file contains information regarding the known hosts on the net- work. It can be used in conjunction with DNS, and the NIS maps"

- https://man.freebsd.org/cgi/man.cgi?query=ntp.conf&sektion=5&format=ascii — "The ntp.conf configuration file is read at initial startup by the ntpd(1nt- pdmdoc) daemon in order to specify the synchronization sources, modes and other related"

- https://man.freebsd.org/cgi/man.cgi?query=ftpd&sektion=8&format=ascii — "ent before any file operations may be performed. 2. The login name must not appear in the file /etc/ftpusers. 3. The login name must not"

- https://man.freebsd.org/cgi/man.cgi?query=getcap&sektion=3&format=ascii — "malloc(3)'d copy of it in buf. The cgetent() function will first look for files ending in .db (see cap_mkdb(1)) before accessing the ASCII file. The"

- https://raw.githubusercontent.com/freebsd/freebsd-src/stable/14/libexec/rc/netstart — "#!/bin/sh -" (interpreter directive).

- https://raw.githubusercontent.com/freebsd/freebsd-src/stable/14/libexec/rc/pccard_ether — "#!/bin/sh -" (interpreter directive).

- https://raw.githubusercontent.com/freebsd/freebsd-src/stable/14/libexec/rc/rc — "#!/bin/sh" (interpreter directive).

- https://raw.githubusercontent.com/freebsd/freebsd-src/stable/14/libexec/rc/rc.bsdextended — "#!/bin/sh" (interpreter directive).

- https://raw.githubusercontent.com/freebsd/freebsd-src/stable/14/libexec/rc/rc.firewall — "#!/bin/sh -" (interpreter directive).

- https://raw.githubusercontent.com/freebsd/freebsd-src/stable/14/libexec/rc/rc.initdiskless — "#!/bin/sh" (interpreter directive).

- https://raw.githubusercontent.com/freebsd/freebsd-src/stable/14/libexec/rc/rc.resume — "#!/bin/sh" (interpreter directive).

- https://raw.githubusercontent.com/freebsd/freebsd-src/stable/14/libexec/rc/rc.shutdown — "#!/bin/sh" (interpreter directive).

- https://raw.githubusercontent.com/freebsd/freebsd-src/stable/14/libexec/rc/rc.suspend — "#!/bin/sh" (interpreter directive).

Individual review: aliases format permits both delivery values and executable commands. Its contents are unavailable, so the alias object remains UNKNOWN. The mail directory already establishes MIXED from README content and Makefile commands; aliases and unlisted members remain UNKNOWN. Printcap is used by multiple spooling utilities, so S2.2-7 does not exempt it as settings confined to one program.

#!/usr/bin/env python3
"""Classification c2, part 6 of A1: decide every row of A1/in/part-6.tsv.

Rules (stated in A1/c2/part-6.notes.md) are applied to homogeneous kinds;
everything else is decided row by row in table T below.
Usage: part6_decide.py <in.tsv> <out.tsv>   (appends only ids missing from out)
"""
import csv, os, re, sys

FD = "doc:https://www.freedesktop.org/software/systemd/man/latest/"
M7 = "doc:https://man7.org/linux/man-pages/"
DEB = "doc:https://manpages.debian.org/bookworm/"
BASH = "doc:https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html"


def FB(page, sec):
    return f"doc:https://man.freebsd.org/cgi/man.cgi?query={page}&sektion={sec}"


def R(d, s, w, b, r):
    return (d, s, w, b, r)


# ---------------- rules for homogeneous kinds ----------------
BACKUPS = {"/etc/group-", "/etc/passwd-", "/etc/shadow-", "/etc/gshadow-", "/etc/subuid-", "/etc/subgid-"}
STARTUP = (".bashrc", ".bash_logout", ".profile", ".shrc", ".cshrc", ".login")
STARTUP_ETC = {"/etc/profile", "/etc/csh.cshrc", "/etc/csh.login", "/etc/csh.logout"}
FORTH_LUA = re.compile(r"^/boot/([A-Za-z0-9_-]+\.4th|loader\.rc|menu\.rc|lua)$")
BOOTPROG = {"/boot/" + n for n in (
    "boot boot0 boot0sio boot1 boot1.efi boot2 cdboot gptboot gptboot.efi gptzfsboot isoboot loader "
    "loader.efi loader_4th loader_4th.efi loader_ia32.efi loader_lua loader_lua.efi loader_simp "
    "loader_simp.efi mbr pmbr pxeboot userboot.so userboot_4th.so userboot_lua.so zfsboot zfsloader").split()}
LOG_ROW = {"/var/log/README", "/var/log/x2-install-attempt1.sh", "/var/log/x2-install.done", "/var/log/x1-bootstrap.done"}
CACHE_ROW = {"/var/cache/debconf", "/var/cache/cups", "/var/cache/nuageinit"}


def rule(row):
    kind, name, ev = row["kind"], row["name"], row["evidence"]
    if kind == "account":
        uid = re.search(r"uid=(\d+)", ev).group(1)
        return "A", R("MUST", "S2.2-15", f"account {name}, uid {uid}, in the account database", "evidence",
                      "S2.2-15 states that accounts must be recorded; the object is an existing account.")
    if kind == "process":
        return "P", R("MUST", "S2.2-9", "program running as a process (or kernel threads) on the computer", "evidence",
                      "A program that runs on the computer must be recorded regardless of how it was installed (S2.2-9).")
    if kind == "rc-service":
        return "V", R("MUST", "S2.2-10,S2.2-2", f"enabled rc.d service {name}: shell script rc runs as root at boot",
                      FB("rc", 8),
                      "rc executes the enabled script with root rights (S2.2-10); after removal the service no longer runs at boot (S2.2-2).")
    if kind != "stored":
        return None, None
    if name.startswith("/var/log/") and name not in LOG_ROW:
        return "L", R("NOT", "S2.2-6", "log or login-history file written by a program or the login system", "evidence",
                      "A log or history file is a record of the past; S2.2-6 says records of the past need not be recorded.")
    if (name.startswith("/var/cache/") and name not in CACHE_ROW) or re.match(r"^/home/[^/]+/\.cache/", name):
        return "C", R("NOT", "S2.2-5", "cache of a program: downloaded or derived data it rebuilds", "evidence",
                      "Regenerated or re-downloaded by its program; after removal the computer does the same, only more slowly (S2.2-5).")
    if name in BACKUPS:
        return "B", R("NOT", "S2.2-2,S2.2-6", "previous copy of an account file kept by shadow tools; nothing reads it",
                      M7 + "man8/vipw.8.html",
                      "Only a backup of the previous state; removal changes nothing the computer does (S2.2-2), and it is a record of the past (S2.2-6).")
    if name in STARTUP_ETC or (re.match(r"^/(root|home/[^/]+)/\.[a-z_]+$", name) and name.endswith(STARTUP)):
        return "S", R("MUST", "S2.2-10", "shell startup or logout file executed by sh, bash or csh",
                      BASH if row["machine"] != "freebsd" else FB("csh", 1),
                      "The shell executes this file with the user's rights; S2.2-10 names shell startup files as code that must be recorded.")
    if re.match(r"^/(root|home/[^/]+)/\.ssh$", name) and "authorized_keys" in ev:
        return "K", R("MUST", "S2.2-15", "authorized_keys: public keys allowed to log in to this account over SSH",
                      "doc:https://man.openbsd.org/sshd.8#AUTHORIZED_KEYS_FILE_FORMAT",
                      "These are keys used to log in to an account; S2.2-15 says they must be recorded.")
    if row["machine"] == "freebsd" and FORTH_LUA.match(name):
        return "F", R("MUST", "S2.2-10,S2.2-13", "Forth or Lua code the boot loader executes (menus, logos, config handling)",
                      FB("loader_4th", 8) if name != "/boot/lua" else FB("loader_lua", 8),
                      "The loader executes it as code with full machine rights (S2.2-10); S2.2-13 counts it as code even where it holds settings.")
    if row["machine"] == "freebsd" and name in BOOTPROG:
        return "G", R("MUST", "S2.2-9,S2.2-2", "boot program: boot code or loader started by firmware, boot chain or bhyveload",
                      FB("boot", 8),
                      "A program that can be started at boot (boot prompt, EFI entry, gpart bootcode); after removal starting or installing it is impossible (S2.2-2, S2.2-9).")
    return None, None


# ---------------- row-by-row table ----------------
T = {}


def put(keys, rec):
    for k in keys:
        assert k not in T, k
        T[k] = rec


STAMP_REASON = "Readings: a record of the past (S2.2-6, need not) or something the computer's behaviour depends on (S2.2-1, must); no sentence says which prevails."
HOLE_DB = "S2.2-4,S2.2-2"

# ---- debian-desktop: processes handled by rule P; units ----
put(["d|system-unit|netplan-ovs-cleanup.service"], R("MUST", "S2.2-1,S2.2-2", "service generated by netplan to clean Open vSwitch configuration",
    "doc:https://netplan.readthedocs.io/en/stable/netplan-generate/", "A service the service manager can start; after removal starting it becomes impossible (S2.2-2)."))
put(["d|system-unit|systemd-growfs@-.service"], R("MUST", "S2.2-1,S2.2-2", "generated service growing the root file system to its partition at boot",
    FD + "systemd-growfs.html", "A service run at boot; the usable size of the root file system depends on it (S2.2-1)."))
DEV = R("MUST", "S2.2-1,S2.2-2", "systemd device units for present disks, partitions, CD drive, serial ports, network card",
        FD + "systemd.device.html", "They are the devices the computer uses; removing a disk or its unit's device makes mounts or the network impossible (S2.2-2).")
put(["d|system-units|unpackaged *.device", "d|user-units|unpackaged *.device"], DEV)
put(["d|system-units|unpackaged *.mount", "d|user-units|unpackaged *.mount"], R("MUST", "S2.2-1,S2.2-2",
    "mounted file systems: root, EFI partition, credential and kernel file systems", FD + "systemd.mount.html",
    "The group includes the root file system mount; after its removal the computer can do nothing (S2.2-2)."))
put(["d|system-units|unpackaged *.not-found", "d|user-units|unpackaged *.not-found"], R("NOT", "S2.2-1,S2.2-2",
    "names referenced by other units for which no unit file exists", FD + "systemctl.html",
    "Nothing is loaded, runs or can be started under these names; behaviour does not depend on them and removal changes nothing (S2.2-1, S2.2-2)."))
put(["d|system-units|unpackaged *.scope"], R("MUST", "S2.2-9,S2.2-1", "init.scope holds PID 1; session scope holds a login session's processes",
    FD + "systemd.scope.html", "init.scope contains the running service manager, a program that runs (S2.2-9); the whole computer depends on it."))
put(["d|user-units|unpackaged *.scope"], R("MUST", "S2.2-9", "user manager scope and the running Flatpak GNOME Calculator scope",
    FD + "systemd.scope.html", "They contain programs that run on the computer, including a Flatpak application (S2.2-9)."))
put(["d|system-units|unpackaged *.slice", "d|user-units|unpackaged *.slice"], R("MUST", "S2.2-1,S2.2-2",
    "cgroup slices in which the service manager places and limits units", FD + "systemd.slice.html",
    "The group includes the root slice; services cannot be placed without it, and resource limits are applied through slices (S2.2-1)."))
XU = R("MUST", "S2.2-9,S2.2-10", "transient user service running a workload shell script of the user",
       FD + "systemd-run.html", "A loaded service that runs or ran a bash script with the user's rights: a program that runs (S2.2-9), code bash executes (S2.2-10).")
put(["d|user-unit|x2-complete-workload.service", "d|user-unit|x2-day.service", "d|user-unit|x2-final-apps.service",
     "d|user-unit|x2-repair-desktop.service"], XU)
put(["d|stored-directory-skeleton|directory-only remainder", "f|stored-directory-skeleton|directory-only remainder"],
    R("UNKNOWN", "S3-2", "directories without files belonging to no package; members not available", "none",
      "The listed directories are not available to this classification, so what they do cannot be established; S3-2 gives ?."))

# ---- debian-desktop: stored ----
D = {}
def d(names, rec):
    put(["d|stored|" + n for n in names], rec)

d(["/boot/efi"], R("MUST", "S2.2-1,S2.2-16", "EFI system partition: shim, GRUB EFI binaries, MOK manager, fallback",
   "doc:https://www.gnu.org/software/grub/manual/grub/grub.html", "Firmware starts these binaries to boot; without them the computer does not boot (S2.2-1, S2.2-16)."))
d(["/boot/grub"], R("MUST", "S2.2-1,S2.2-16", "GRUB boot loader files: modules, configuration, fonts, translations",
   "doc:https://www.gnu.org/software/grub/manual/grub/grub.html", "The boot loader and its configuration; the computer boots through it and it sets the boot entries (S2.2-1, S2.2-16)."))
d(["/boot/initrd.img-6.1.0-56-amd64", "/boot/initrd.img-6.1.0-56-cloud-amd64"], R("MUST", "S2.2-1,S2.2-9",
   "initial RAM file system for one installed kernel, executed at boot", DEB + "initramfs-tools/initramfs-tools.7.en.html",
   "Its init program runs at boot of that kernel's GRUB entry; without it that kernel cannot boot (S2.2-9, S2.2-1)."))
d(["/etc/.pwd.lock"], R("NOT", "S2.2-2", "lock file used by lckpwdf while account files are edited",
   M7 + "man3/getspnam.3.html", "Created again when a tool locks the account files; removal changes nothing the computer does (S2.2-2)."))
d(["/etc/.resolv.conf.systemd-resolved.bak"], R("NOT", "S2.2-2,S2.2-6", "backup of resolv.conf made when systemd-resolved was installed",
   "evidence", "Nothing reads the backup; removal changes nothing (S2.2-2); it keeps a past state (S2.2-6)."))
d(["/etc/X11"], R("NOT", "S2.2-2", "default-display-manager: name of the chosen display manager, read by SysV scripts",
   "doc:https://sources.debian.org/data/main/g/gdm3/43.0-3/debian/patches/92_systemd_unit.patch",
   "Under systemd the display-manager.service link selects GDM and the gdm3 unit does not read this file; removal changes nothing (S2.2-2)."))
d(["/etc/alternatives"], R("MUST", "S2.2-1,S2.2-2", "alternatives links choosing which program answers generic command names",
   DEB + "dpkg/update-alternatives.1.en.html", "Commands such as editor or x-www-browser exist only through these links; after removal they cannot be run (S2.2-2)."))
d(["/etc/apparmor.d"], R("MUST", "S2.2-1", "local AppArmor additions included into the shipped profiles",
   DEB + "apparmor/apparmor.d.5.en.html", "They are parts of the access rules applied to confined programs; what those programs may do depends on them (S2.2-1)."))
d(["/etc/apt"], R("MUST", "S2.2-1,S2.2-2", "APT package sources and unattended-upgrades policy",
   DEB + "apt/sources.list.5.en.html", "Without the sources installing packages becomes impossible, and the policy decides automatic upgrades (S2.2-2, S2.2-1)."))
d(["/etc/ca-certificates.conf"], R("MUST", "S2.2-1", "list of CA certificates update-ca-certificates enables",
   DEB + "ca-certificates/update-ca-certificates.8.en.html", "It decides which CAs the generated trust bundle contains, so which TLS servers can be verified (S2.2-1)."))
d(["/etc/ca-certificates.conf.dpkg-old"], R("NOT", "S2.2-2,S2.2-6", "dpkg's copy of the previous ca-certificates.conf",
   DEB + "dpkg/dpkg.1.en.html", "No program reads the old copy; removal changes nothing (S2.2-2); it keeps a past state (S2.2-6)."))
d(["/etc/cloud"], R("MUST", "S2.2-1,S2.2-13", "cloud-init configuration of the Debian cloud image",
   "doc:https://cloudinit.readthedocs.io/en/latest/reference/base_config_reference.html", "cloud-init reads it as values (S2.2-13) at boot; datasource choice and boot configuration depend on it (S2.2-1)."))
d(["/etc/cloud-release"], R("NOT", "S2.2-4,S2.2-2", "text naming the cloud image build", "evidence",
   "Descriptive content; nothing the computer does depends on it (S2.2-4, S2.2-2)."))
d(["/etc/cni"], R("NOT", "S2.2-2", "lock file of the CNI network configuration directory",
   "doc:https://www.cni.dev/docs/spec/", "A lock created again on use; the directory holds no network definition here; removal changes nothing (S2.2-2)."))
d(["/etc/cups"], R("MUST", "S2.2-1,S2.2-2", "CUPS printer definitions, subscriptions and conversion rules",
   "doc:https://www.cups.org/doc/man-cupsd.conf.html", "cupsd serves all programs from printers.conf; after removal printing to the defined printers becomes impossible (S2.2-2)."))
d(["/etc/default"], R("MUST", "S2.2-10,S2.2-13", "GRUB defaults (sourced shell), system locale and keyboard layout",
   "doc:https://www.gnu.org/software/grub/manual/grub/grub.html", "grub-mkconfig sources grub.d snippets as shell code (S2.2-13, S2.2-10); locale and keyboard settings apply to all programs."))
d(["/etc/dictionaries-common"], R("UNKNOWN", "S2.2-7,S3-2", "name of the system default ispell dictionary",
   DEB + "dictionaries-common/update-default-ispell.8.en.html", "Whether any installed spelling program reads it cannot be established from the evidence; its effect is unknown (S3-2)."))
d(["/etc/dpkg"], R("UNKNOWN", "S2.2-1,S3-2", "dpkg vendor origin link naming Debian as the vendor",
   DEB + "dpkg-dev/dpkg-vendor.1.en.html", "Read by dpkg-vendor; whether any installed program uses it cannot be established without the package list (S3-2)."))
d(["/etc/environment"], R("MUST", "S2.2-1,S2.2-13", "system environment variables set by pam_env for every session",
   M7 + "man8/pam_env.8.html", "Read as values (S2.2-13); the environment of every session depends on it (S2.2-1)."))
d(["/etc/fonts"], R("HOLE", "S2.2-1,S2.2-7", "fontconfig rules: slight hinting, bitmap fonts disabled, for all programs",
   "doc:https://www.freedesktop.org/software/fontconfig/fontconfig-user.html", "Appearance shared by all programs: S2.2-7 exempts one-program settings only, S2.2-1 counts behaviour; whether appearance is behaviour is not stated."))
d(["/etc/fstab"], R("MUST", "S2.2-1,S2.2-2", "table of file systems mounted at boot", M7 + "man5/fstab.5.html",
   "Root and EFI mounts come from it; after removal they are not mounted (S2.2-2)."))
d(["/etc/gdm3"], R("MUST", "S2.2-1", "login screen (GDM greeter) settings, including offered login methods",
   "doc:https://help.gnome.org/admin/system-admin-guide/stable/login.html", "The login of every user goes through this screen, so S2.2-7 does not fit; what can be done at login depends on it (S2.2-1)."))
d(["/etc/group", "/etc/gshadow", "/etc/passwd", "/etc/shadow"], R("MUST", "S2.2-15", "account database: accounts, groups, password-login state",
   M7 + "man5/passwd.5.html", "It holds the accounts and whether password login is allowed; S2.2-15 says both must be recorded."))
d(["/etc/grub.d"], R("MUST", "S2.2-10", "grub-mkconfig script executed as root to generate boot entries",
   "doc:https://www.gnu.org/software/grub/manual/grub/grub.html", "A script executed by grub-mkconfig with its rights; S2.2-10 requires such code to be recorded."))
d(["/etc/hostname"], R("MUST", "S2.2-1", "static host name of the computer", FD + "hostname.html",
   "The name the computer uses and announces on the network depends on it (S2.2-1)."))
d(["/etc/hosts"], R("MUST", "S2.2-1", "static host name to address table", M7 + "man5/hosts.5.html",
   "Name resolution of localhost and the host's own name depends on it (S2.2-1)."))
d(["/etc/hosts.allow", "/etc/hosts.deny"], R("MUST", "S2.2-1", "TCP wrappers access rules for wrapped network services",
   DEB + "libwrap0-dev/hosts_access.5.en.html", "They are access rules deciding which hosts may use wrapped services (S2.2-1)."))
d(["/etc/initramfs-tools"], R("MUST", "S2.2-1", "list of modules added to the initramfs", DEB + "initramfs-tools/initramfs-tools.7.en.html",
   "Which drivers the initramfs has at boot depends on it (S2.2-1)."))
d(["/etc/inputrc"], R("MUST", "S2.2-1,S2.2-7,S2.2-13", "system readline init file: key bindings for all readline programs",
   "doc:https://tiswww.case.edu/php/chet/readline/rluserman.html", "Read as values (S2.2-13) by every readline program, not one (S2.2-7 does not fit); command-line editing depends on it (S2.2-1)."))
d(["/etc/kernel-img.conf"], R("MUST", "S2.2-1,S2.2-13", "settings of kernel package scripts: symlinks, initramfs handling",
   DEB + "linux-base/kernel-img.conf.5.en.html", "Read as values (S2.2-13) by kernel maintainer scripts; what kernel installation does depends on it (S2.2-1)."))
d(["/etc/ld.so.cache"], R("NOT", "S2.2-5", "dynamic linker cache of library locations built by ldconfig", M7 + "man8/ld.so.8.html",
   "A cache: without it the linker searches the default directories, so programs start, only more slowly (S2.2-5)."))
d(["/etc/libreoffice"], R("HOLE", "S2.2-7,S2.2-2", "LibreOffice configuration data files (.xcd) for Writer, Python scripting, language",
   "doc:https://wiki.documentfoundation.org/Development/Configuration", "Settings inside one program (S2.2-7, need not), yet without them modules such as Python scripting stop working (S2.2-2, must); no priority stated."))
d(["/etc/locale.gen"], R("MUST", "S2.2-1,S2.2-13", "list of locales locale-gen compiles for the system",
   DEB + "locales/locale.gen.5.en.html", "Read as values (S2.2-13); which locales exist for all programs after generation depends on it (S2.2-1)."))
d(["/etc/localtime"], R("MUST", "S2.2-1", "system time zone link read by libc", FD + "localtime.html",
   "The time zone of every program depends on it (S2.2-1)."))
d(["/etc/machine-id"], R("MUST", "S2.2-1,S2.2-2", "unique machine identifier; its absence makes systemd treat the boot as first boot",
   FD + "machine-id.html", "Removal makes the next boot a first boot and changes identifiers derived from it (S2.2-1)."))
d(["/etc/mailcap"], R("MUST", "S2.2-10,S2.2-13", "MIME type to handler command table; entries are shell command lines",
   DEB + "mime-support/mailcap.5.en.html", "Programs run its entries through the shell with their rights, so it counts as code (S2.2-13) that S2.2-10 requires."))
d(["/etc/modprobe.d"], R("MUST", "S2.2-1", "modprobe blacklist: kernel modules not loaded automatically", M7 + "man5/modprobe.d.5.html",
   "Which drivers the kernel loads depends on it (S2.2-1)."))
d(["/etc/modules"], R("MUST", "S2.2-1", "kernel modules loaded at boot", DEB + "kmod/modules.5.en.html",
   "Which drivers are loaded at boot depends on it (S2.2-1)."))
d(["/etc/motd"], R("NOT", "S2.2-4", "message of the day text shown at login", DEB + "libpam-modules/pam_motd.8.en.html",
   "Text content; after removal the computer does the same, only the text is not shown (S2.2-4)."))
d(["/etc/mtab"], R("MUST", "S2.2-2", "link exposing the kernel mount table at the traditional path", M7 + "man5/fstab.5.html",
   "Programs reading /etc/mtab list mounts through it; after removal they cannot (S2.2-2)."))
d(["/etc/netplan"], R("MUST", "S2.2-1,S2.2-2", "netplan network configuration written by cloud-init",
   "doc:https://netplan.readthedocs.io/en/stable/netplan-yaml/", "The network configuration is generated from it; after removal the interface is not configured (S2.2-2)."))
d(["/etc/networks"], R("MUST", "S2.2-1", "network names database read by getnetbyname", M7 + "man5/networks.5.html",
   "Read as values by the resolver functions; network name lookups depend on it (S2.2-1)."))
d(["/etc/nsswitch.conf"], R("MUST", "S2.2-1,S2.2-2", "name service switch: sources for users, hosts, groups", M7 + "man5/nsswitch.conf.5.html",
   "Account and host lookups follow it; behaviour of logins and resolution depends on it (S2.2-1)."))
d(["/etc/pam.d"], R("MUST", "S2.2-1,S2.2-15", "PAM common configuration for account, auth, password, session",
   DEB + "libpam-runtime/pam-auth-update.8.en.html", "They decide how logins authenticate, including whether password login is allowed (S2.2-15, S2.2-1)."))
d(["/etc/papersize"], R("MUST", "S2.2-1,S2.2-13", "system default paper size for libpaper users",
   DEB + "libpaper1/papersize.5.en.html", "Read as values (S2.2-13) by all printing programs, not one (S2.2-7 does not fit); printed output depends on it (S2.2-1)."))
d(["/etc/python3"], R("NOT", "S2.2-5,S2.2-13", "debian_config: byte-compilation options for Debian's py3compile",
   "doc:https://www.debian.org/doc/packaging-manuals/python-policy/", "Read as values (S2.2-13); it only decides how byte-code caches are built, so after removal programs do the same (S2.2-5)."))
RC = R("MUST", "S2.2-1", "SysV runlevel links: which init scripts start or stop in the runlevel", FD + "systemd-sysv-generator.html",
       "systemd-sysv-generator uses these links to enable init scripts without native units; service enablement depends on them (S2.2-1).")
d(["/etc/rc0.d", "/etc/rc1.d", "/etc/rc2.d", "/etc/rc3.d", "/etc/rc4.d", "/etc/rc5.d", "/etc/rc6.d", "/etc/rcS.d"], RC)
d(["/etc/resolv.conf"], R("MUST", "S2.2-1,S2.2-2", "DNS resolver configuration (link to the resolved file) used by libc",
   M7 + "man5/resolv.conf.5.html", "Without it name resolution through libc falls back to an unconfigured local server and fails (S2.2-2)."))
d(["/etc/runit"], R("MUST", "S2.2-1", "runit service link enabling supervision of the ssh service",
   DEB + "runit/runsvdir.8.en.html", "It enables a service for runsvdir; after removal runit no longer starts or supervises ssh (S2.2-1)."))
d(["/etc/security"], R("NOT", "S2.2-6,S2.2-15", "opasswd: history of old password hashes for reuse checks",
   M7 + "man8/pam_pwhistory.8.html", "A history of past passwords: records of the past (S2.2-6); account passwords need not be recorded (S2.2-15)."))
CAT = R("MUST", "S2.2-1,S2.2-2", "SGML/XML catalog mapping public identifiers to local DTD files",
        DEB + "xml-core/update-xmlcatalog.1.en.html", "Programs resolving these identifiers use the local files through it; after removal offline resolution becomes impossible (S2.2-2).")
d(["/etc/sgml", "/etc/xml", "/var/lib/sgml-base", "/var/lib/xml-core"], CAT)
d(["/etc/shells"], R("MUST", "S2.2-1", "list of valid login shells", M7 + "man5/shells.5.html",
   "chsh and services checking it decide which shells accounts may use (S2.2-1)."))
d(["/etc/ssh"], R("MUST", "S2.2-1,S2.2-2", "SSH server host keys (private and public) and other sshd files",
   "doc:https://man.openbsd.org/sshd.8", "sshd reads its host keys to run and prove the host's identity; removal stops sshd or changes that identity (S2.2-1, S2.2-2)."))
d(["/etc/ssl"], R("MUST", "S2.2-1,S2.2-2", "CA certificate directory, bundle and the host's snakeoil TLS key",
   DEB + "ca-certificates/update-ca-certificates.8.en.html", "TLS clients look up trusted CAs here; after removal verifying TLS servers becomes impossible (S2.2-2)."))
d(["/etc/subgid", "/etc/subuid"], R("MUST", "S2.2-1,S2.2-2", "subordinate ID ranges for user namespaces", M7 + "man5/subuid.5.html",
   "After removal rootless containers of the user become impossible (S2.2-2)."))
d(["/etc/sudoers.d"], R("MUST", "S2.2-15", "rules granting accounts the right to run commands as superuser",
   "doc:https://www.sudo.ws/docs/man/sudoers.man/", "The file grants the right to become superuser; S2.2-15 says this right must be recorded."))
d(["/etc/systemd"], R("MUST", "S2.2-1,S2.2-2", "local systemd units, enablement links and drop-ins",
   FD + "systemd.unit.html", "They decide which services are enabled and how; after removal enabled services stop starting (S2.2-2)."))
d(["/etc/timezone"], R("MUST", "S2.2-1", "Debian time zone name file", "doc:https://wiki.debian.org/TimeZoneChanges",
   "Read as the system time zone name by programs and tzdata configuration (S2.2-1)."))
d(["/etc/tmpfiles.d"], R("MUST", "S2.2-1", "tmpfiles rule for the screen runtime directory", FD + "tmpfiles.d.html",
   "systemd-tmpfiles applies it at boot; the runtime directory screen needs depends on it (S2.2-1)."))
STAMP = R("HOLE", "S2.2-1,S2.2-6", "marker file: its absence makes a program repeat a one-time action", "evidence", STAMP_REASON)
d(["/home/census/.config/.gsd-keyboard.settings-ported", "/home/census/.local/share/gnome-settings-daemon",
   "/home/census/.sudo_as_admin_successful"], STAMP)
d(["/home/census/.local/share/gnome-shell"], R("HOLE", "S2.2-1,S2.2-6", "app usage statistics and the overrides-migration marker of GNOME Shell",
   "evidence", STAMP_REASON))
d(["/home/census/.local/share/nautilus"], R("HOLE", "S2.2-1,S2.2-4,S2.2-6", "starred-files database, ontology cache, tracker migration marker",
   "evidence", "Starred files are database contents (S2.2-4) and the marker a past record (S2.2-6), yet the marker steers a one-time migration (S2.2-1); unresolved."))
d(["/home/census/.config/GIMP"], R("NOT", "S2.2-7,S2.2-5", "GIMP settings: theme, menus, tags, plug-in registry",
   "doc:https://docs.gimp.org/2.10/en/gimp-concepts-setup.html", "Settings in force only inside GIMP (S2.2-7) and a rebuilt plug-in registry (S2.2-5); need not be recorded."))
d(["/home/census/.config/GNOME-xdg-terminals.list", "/home/census/.config/xdg-terminals.list"], R("UNKNOWN", "S2.2-1,S3-2",
   "preferred terminal list for xdg-terminal-exec", "doc:https://man.archlinux.org/man/xdg-terminal-exec.1.en",
   "Only xdg-terminal-exec reads it; whether that program is installed here cannot be established from the evidence (S3-2)."))
d(["/home/census/.config/cni"], R("NOT", "S2.2-2", "user CNI directory holding only a lock file",
   "doc:https://www.cni.dev/docs/spec/", "No network definition, only a lock created again on use; removal changes nothing (S2.2-2)."))
d(["/home/census/.config/dconf"], R("MUST", "S2.2-1,S2.2-7", "user dconf database: settings of GNOME Shell and all GNOME programs",
   "doc:https://help.gnome.org/admin/system-admin-guide/stable/dconf.html", "Read by many programs, not one (S2.2-7 does not fit); input sources, keyboard and desktop behaviour depend on it (S2.2-1)."))
d(["/home/census/.config/evolution"], R("MUST", "S2.2-1", "evolution-data-server network proxy source used by mail, contacts, calendar",
   "doc:https://wiki.gnome.org/Apps/Evolution/ESourceFileFormat", "A network proxy setting shared by several programs (S2.2-7 does not fit); their network access depends on it (S2.2-1)."))
d(["/home/census/.config/geany"], R("NOT", "S2.2-7,S2.2-13", "settings and key bindings of the Geany editor",
   "doc:https://www.geany.org/manual/current/index.html", "Read as values (S2.2-13), not editor code; in force only inside Geany, which S2.2-7 says need not be recorded."))
d(["/home/census/.config/libreoffice"], R("UNKNOWN", "S2.2-7,S2.2-10,S3-2", "LibreOffice user profile; settings, autotext, extension cache visible",
   "doc:https://wiki.documentfoundation.org/UserProfile", "Visible members are one-program settings and content (S2.2-7); the profile's Basic macro libraries, code under S2.2-10, are not visible (S3-2)."))
d(["/home/census/.config/mozilla", "/home/census/.thunderbird"], R("NOT", "S2.2-6,S2.2-7,S2.2-4",
   "browser or mail client profile: preferences, extensions, history, messages, crash records",
   "doc:https://support.mozilla.org/kb/profiles-where-firefox-stores-user-data", "Preferences and extensions in force only inside the program (S2.2-7), history (S2.2-6), messages (S2.2-4): need not be recorded."))
d(["/home/census/.config/pulse"], R("NOT", "S2.2-2", "PulseAudio protocol authentication cookie, created again when missing",
   "doc:https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/", "Clients and server create a new cookie; after removal sound works the same (S2.2-2)."))
d(["/home/census/.local/share/containers"], R("MUST", "S2.2-9,S2.2-12", "rootless Podman storage: container images, layers and containers",
   "doc:https://docs.podman.io/en/latest/markdown/podman.1.html", "Images hold programs that run in containers; S2.2-12 says a program in a container must be recorded."))
d(["/home/census/.local/share/evolution", "/home/census/.local/share/folks"], R("NOT", "S2.2-4",
   "personal address book, tasks and contact links", "evidence", "Contacts and tasks are database contents; S2.2-4 says content need not be recorded."))
d(["/home/census/.local/share/flatpak"], R("MUST", "S2.2-9", "per-user Flatpak installation holding the running GNOME Calculator",
   "doc:https://docs.flatpak.org/en/latest/tips-and-tricks.html", "Holds an application package that runs on the computer; S2.2-9 names Flatpak programs as to be recorded."))
d(["/home/census/.local/share/gvfs-metadata"], R("NOT", "S2.2-4,S2.2-7", "per-file metadata database kept by gvfsd-metadata for file managers",
   "doc:https://gitlab.gnome.org/GNOME/gvfs", "Database contents about files (S2.2-4) used for file manager display (S2.2-7); need not be recorded."))
d(["/home/census/.local/share/icc"], R("NOT", "S2.2-2", "colour profile colord generates from the monitor EDID",
   "doc:https://www.freedesktop.org/software/colord/", "colord generates it again from the monitor data at login; removal changes nothing (S2.2-2)."))
d(["/home/census/.local/share/recently-used.xbel"], R("NOT", "S2.2-6", "list of recently used files", "evidence",
   "A history; S2.2-6 says records of the past need not be recorded."))
d(["/home/census/.local/share/xorg"], R("NOT", "S2.2-6", "Xorg server logs of the user session", "evidence",
   "Logs are records of the past; S2.2-6 says they need not be recorded."))
d(["/home/census/.var"], R("NOT", "S2.2-5,S2.2-7", "per-app Flatpak data of GNOME Calculator: linker cache, settings, cache",
   "doc:https://docs.flatpak.org/en/latest/conventions.html", "Caches (S2.2-5) and settings in force only inside the calculator (S2.2-7); need not be recorded."))
SH = R("MUST", "S2.2-9,S2.2-10", "shell script of the operator's workload, run by bash", "evidence",
       "A program in the home directory or file system that bash can run with its rights (S2.2-9, S2.2-10); after removal running it is impossible.")
d(["/home/census/X2-complete-workload.sh", "/home/census/X2-day.sh", "/home/census/X2-desktop-env.sh",
   "/home/census/X2-final-apps.sh", "/home/census/X2-repair-desktop.sh", "/var/log/x2-install-attempt1.sh"], SH)
d(["/home/census/x2-evidence"], R("NOT", "S2.2-4", "screenshots and text outputs saved by the workload", "evidence",
   "Documents and pictures are content; S2.2-4 says content need not be recorded."))
d(["/usr/local/man"], R("NOT", "S2.2-4,S2.2-2", "link to the local manual page directory", "evidence",
   "Manual pages are documents (S2.2-4); after removal of the link the computer does the same (S2.2-2)."))
d(["/var/cache/cups"], R("MUST", "S2.2-2,S2.2-5", "CUPS caches and the org.cups.cupsd keep-alive file watched by cups.path",
   "doc:https://sources.debian.org/data/main/c/cups/2.4.2-3+deb12u9/scheduler/cups.path.in",
   "ppds.dat and job.cache are cache (S2.2-5), but org.cups.cupsd makes systemd start cupsd; after removal that start stops (S2.2-2)."))
d(["/var/cache/debconf"], R("HOLE", "S2.2-4,S2.2-5,S2.2-2", "debconf database of package configuration answers and templates",
   DEB + "debconf-doc/debconf.conf.5.en.html", "Database contents (S2.2-4) in a cache directory (S2.2-5), need not; but packages reconfigure from these answers (S2.2-2, must); unresolved."))
d(["/var/lib/PackageKit"], R("NOT", "S2.2-6", "PackageKit database of past transactions", "evidence",
   "A history of transactions; S2.2-6 says records of the past need not be recorded."))
d(["/var/lib/app-info", "/var/lib/swcatalog"], R("NOT", "S2.2-5", "AppStream catalog data derived from APT lists",
   "doc:https://www.freedesktop.org/software/appstream/docs/", "Regenerated from package indexes by apt update; after removal software centres do the same, only more slowly (S2.2-5)."))
d(["/var/lib/apt"], R("HOLE", HOLE_DB + ",S2.2-5", "APT package lists (indexes) and extended_states automatic-install marks",
   DEB + "apt/apt-mark.8.en.html", "Lists are cache (S2.2-5); extended_states is database contents (S2.2-4, need not) yet decides what autoremove removes (S2.2-2, must); unresolved."))
d(["/var/lib/cloud"], R("MUST", "S2.2-1,S2.2-2", "cloud-init instance data, per-instance semaphores and scripts",
   "doc:https://cloudinit.readthedocs.io/en/latest/reference/directory_layout.html", "cloud-init decides from it which modules already ran; removal makes it redo first-boot configuration (S2.2-1)."))
d(["/var/lib/colord"], R("NOT", "S2.2-4,S2.2-2", "colord databases mapping devices to colour profiles",
   "doc:https://www.freedesktop.org/software/colord/", "Database contents (S2.2-4); automatic mappings are rebuilt at login, so the computer does the same (S2.2-2)."))
d(["/var/lib/containers"], R("UNKNOWN", "S2.2-9,S3-2", "rootful Podman storage; locks, state database, network backend visible",
   "doc:https://docs.podman.io/en/latest/markdown/podman.1.html", "Stored images or containers would be programs (S2.2-9), but the 18 members are not all visible; what the group holds is unknown (S3-2)."))
d(["/var/lib/dbus"], R("NOT", "S2.2-2", "compatibility link from the D-Bus machine-id path to /etc/machine-id",
   "doc:https://dbus.freedesktop.org/doc/dbus-uuidgen.1.html", "D-Bus also reads /etc/machine-id; after removal of the link it gets the same identifier (S2.2-2)."))
d(["/var/lib/dpkg"], R("HOLE", HOLE_DB + ",S2.2-1", "dpkg database: package state, triggers, alternatives registry",
   DEB + "dpkg/dpkg.1.en.html", "Contents of a database (S2.2-4, need not), but after removal dpkg and alternatives cannot manage packages (S2.2-2, must); unresolved."))
d(["/var/lib/emacsen-common"], R("NOT", "S2.2-4,S2.2-2", "emacsen-common records of installed add-on packages; no Emacs flavour listed",
   "doc:https://www.debian.org/doc/packaging-manuals/debian-emacs-policy", "Database contents (S2.2-4); with no Emacs installed nothing uses them, so removal changes nothing (S2.2-2)."))
d(["/var/lib/flatpak"], R("UNKNOWN", "S2.2-9,S3-2", "system Flatpak installation: repository config and change marker visible",
   "doc:https://docs.flatpak.org/en/latest/flatpak-command-reference.html", "Remotes or applications here would have to be recorded (S2.2-9), but the repository configuration's content is not visible (S3-2)."))
d(["/var/lib/gdm3"], R("NOT", "S2.2-2", "compiled greeter dconf database, rebuilt by generate-config at every GDM start",
   "doc:https://sources.debian.org/data/main/g/gdm3/43.0-3/debian/generate-config", "The gdm3 unit recompiles it before each start; removal changes nothing (S2.2-2)."))
d(["/var/lib/ghostscript"], R("NOT", "S2.2-7,S2.2-13", "Ghostscript font maps generated from installed fonts",
   DEB + "ghostscript/gs.1.en.html", "Read as values (S2.2-13) only by Ghostscript; in force only inside that program (S2.2-7)."))
d(["/var/lib/man-db"], R("NOT", "S2.2-7,S2.2-5", "flag enabling man-db to update its index after package changes", "evidence",
   "A setting in force only inside man-db that affects only its index cache (S2.2-7, S2.2-5)."))
d(["/var/lib/pam"], R("HOLE", HOLE_DB, "pam-auth-update state of enabled and seen profiles",
   DEB + "libpam-runtime/pam-auth-update.8.en.html", "Database contents (S2.2-4, need not), but later package updates rewrite PAM configuration from it (S2.2-2, must); no sentence says which prevails."))
d(["/var/lib/python"], R("NOT", "S2.2-2", "leftover python3.11 install marker that maintainer scripts only delete",
   "doc:https://sources.debian.org/src/python3.11/3.11.2-6%2Bdeb12u6/debian/PVER-minimal.postrm.in", "The package scripts only remove this marker; nothing depends on it, so removal changes nothing (S2.2-2)."))
d(["/var/lib/shells.state"], R("HOLE", HOLE_DB, "update-shells record of shells registered by packages",
   DEB + "debianutils/update-shells.8.en.html", "Database contents (S2.2-4, need not), but update-shells derives /etc/shells from it on package changes (S2.2-2, must); unresolved."))
d(["/var/lib/systemd"], R("MUST", "S2.2-1,S2.2-2", "systemd state: lingering for user census, enablement records, timer stamps",
   FD + "loginctl.html", "linger/census starts the user manager at boot; after removal the user's services stop running without a login (S2.2-2)."))
d(["/var/lib/ucf"], R("HOLE", HOLE_DB + ",S2.2-6", "ucf registry and pristine copies of configuration files",
   DEB + "ucf/ucf.1.en.html", "Past copies and database contents (S2.2-4, S2.2-6, need not), but upgrades decide whether to replace configuration from them (S2.2-2, must)."))
d(["/var/lib/xfonts"], R("NOT", "S2.2-2", "update-fonts-alias list of aliases left out when regenerating fonts.alias",
   DEB + "xfonts-utils/update-fonts-alias.8.en.html", "Read only when aliases are regenerated, not by programs; removal changes nothing the computer does (S2.2-2)."))
d(["/var/log/README"], R("NOT", "S2.2-4,S2.2-2", "link to a systemd documentation file about logs", "evidence",
   "A document (S2.2-4); after removal the computer does and can do the same (S2.2-2)."))
DONE = R("UNKNOWN", "S2.2-6,S2.2-1,S3-2", "completion marker of the operator's install step", "evidence",
         "If unread it is a past record (S2.2-6); if a workload script checks it, behaviour depends on it; which program reads it is not established (S3-2).")
d(["/var/log/x2-install.done"], DONE)
d(["/var/spool/cups"], R("NOT", "S2.2-4,S2.2-2", "CUPS spool: a print job document, its control file, a lock file",
   "doc:https://www.cups.org/doc/spec-design.html", "Print jobs are documents (S2.2-4); the lock is recreated; removal changes only content (S2.2-2)."))
d(["/var/spool/mail"], R("UNKNOWN", "S2.2-2,S3-2", "compatibility link /var/spool/mail -> /var/mail", "evidence",
   "Whether any installed mail program uses this path cannot be established without the package list; the removal effect is unknown (S3-2)."))

# ---- freebsd ----
def f(names, rec):
    put(["f|stored|" + n for n in names], rec)

put(["f|kernel-module|kernel"], R("MUST", "S2.2-9,S2.2-2", "the running FreeBSD kernel", FB("kldstat", 8),
    "The kernel runs the computer (S2.2-9); without it nothing runs (S2.2-2)."))
put(["f|kernel-module|intpm.ko", "f|kernel-module|smbus.ko"], R("MUST", "S2.2-9,S2.2-2",
    "loaded kernel module: Intel PIIX4 SMBus controller driver or SMBus framework", FB("intpm", 4),
    "Kernel code that runs on the computer (S2.2-9); after removal the SMBus controller cannot be used (S2.2-2)."))
put(["f|scheduler-inventory|cron and periodic"], R("MUST", "S2.2-10,S2.2-1", "cron tables and periodic jobs run as root on schedule",
    FB("periodic", 8), "cron and periodic execute these commands and scripts with root rights (S2.2-10); what the computer does daily depends on them."))

f(["/boot/defaults", "/boot/loader.conf"], R("MUST", "S2.2-1,S2.2-13", "loader variables: kernel, modules, console, boot options",
   FB("loader.conf", 5), "Read as values (S2.2-13) by the loader; which kernel and modules boot depends on it (S2.2-1)."))
f(["/boot/device.hints"], R("MUST", "S2.2-1", "kernel device hints: resources and enabling of ISA-style devices",
   FB("device.hints", 5), "The kernel configures devices from these hints at boot (S2.2-1)."))
f(["/boot/efi"], R("MUST", "S2.2-1,S2.2-16", "EFI system partition with the fallback boot loader bootx64.efi",
   FB("uefi", 8), "Firmware starts this loader to boot; without it EFI boot is impossible (S2.2-1, S2.2-16)."))
f(["/boot/entropy"], R("NOT", "S2.2-2,S2.2-5", "saved entropy the loader passes to the kernel for early randomness",
   FB("random", 4), "Rewritten at shutdown; without it the kernel gathers entropy itself, so the computer does the same, only later (S2.2-5)."))
f(["/boot/fonts"], R("HOLE", "S2.2-1,S2.2-7", "console fonts used by the loader and the kernel vt console",
   FB("vt", 4), "Appearance shared by the loader and all console programs: S2.2-7 exempts one-program settings only, S2.2-1 counts behaviour; appearance is not addressed."))
f(["/boot/images"], R("NOT", "S2.2-7", "logo pictures of the boot loader menu", FB("loader.conf", 5),
   "Theme of the boot menu, in force only inside the loader; S2.2-7 names a program's theme as not needing recording."))
f(["/boot/kernel"], R("MUST", "S2.2-9,S2.2-2", "the booted kernel and its loadable modules", FB("kldload", 8),
   "The kernel and modules run on the computer (S2.2-9); without them the computer does not boot (S2.2-2)."))
f(["/boot/kernel.old"], R("MUST", "S2.2-9,S2.2-16", "previous kernel and modules, selectable in the loader menu",
   FB("freebsd-update", 8), "A program that can be started from the boot menu (S2.2-9); it is a boot choice the system keeps (S2.2-16)."))
f(["/boot/loader.help.bios", "/boot/loader.help.efi", "/boot/loader.help.userboot"], R("NOT", "S2.2-4",
   "help text shown by the loader's help command", FB("loader", 8), "A document; after removal the computer does the same, only the help text is missing (S2.2-4)."))
f(["/etc/aliases"], R("MUST", "S2.2-1", "link to the mail alias table used by the mail delivery agent", FB("aliases", 5),
   "Where local mail, such as root's, is delivered depends on it (S2.2-1)."))
f(["/etc/auto_master"], R("MUST", "S2.2-1", "autofs master map: automounted directories", FB("auto_master", 5),
   "automountd mounts what this map lists; what can be mounted on access depends on it (S2.2-1)."))
f(["/etc/autofs"], R("MUST", "S2.2-10", "executable autofs map scripts (LDAP, NIS, hosts, media)", FB("auto_master", 5),
   "automountd executes these special maps as programs with root rights; S2.2-10 requires such code to be recorded."))
f(["/etc/blacklistd.conf"], R("MUST", "S2.2-15,S2.2-1", "blacklistd rules: when to block remote hosts in the firewall",
   FB("blacklistd.conf", 5), "Rules deciding which hosts the firewall blocks after failed logins (S2.2-15, S2.2-1)."))
f(["/etc/bluetooth"], R("MUST", "S2.2-1,S2.2-13", "Bluetooth link-key/PIN settings, host and protocol names",
   FB("hcsecd.conf", 5), "Read as values (S2.2-13) by Bluetooth daemons and tools; which devices can pair depends on them (S2.2-1)."))
f(["/etc/cron.d", "/etc/crontab"], R("MUST", "S2.2-10", "system cron tables: commands cron runs as root on schedule",
   FB("crontab", 5), "cron executes the listed commands with root rights; S2.2-10 requires such code to be recorded."))
f(["/etc/ddb.conf"], R("MUST", "S2.2-10,S2.2-13", "scripts for the kernel debugger, loaded by ddb(8)", FB("ddb", 8),
   "The kernel debugger executes these scripts as code (S2.2-13) with kernel rights (S2.2-10)."))
f(["/etc/defaults"], R("MUST", "S2.2-10,S2.2-13", "default rc.conf, periodic.conf, devfs rules, Bluetooth device settings",
   FB("rc.conf", 5), "rc and periodic source these files as shell code (S2.2-13, S2.2-10); service defaults and device rules come from them."))
f(["/etc/devd", "/etc/devd.conf"], R("MUST", "S2.2-10,S2.2-13", "devd rules whose actions are shell commands run on device events",
   FB("devd.conf", 5), "devd runs the action commands with root rights, so the file counts as code (S2.2-13) that S2.2-10 requires."))
f(["/etc/devfs.conf"], R("MUST", "S2.2-1", "device node permissions and links applied at boot", FB("devfs.conf", 5),
   "Access rights to devices depend on it (S2.2-1)."))
f(["/etc/dhclient.conf"], R("MUST", "S2.2-1,S2.2-13", "DHCP client settings", FB("dhclient.conf", 5),
   "Read as values (S2.2-13) by the running dhclient; network configuration depends on it (S2.2-1)."))
f(["/etc/disktab"], R("MUST", "S2.2-1,S2.2-2", "disk type geometry table for bsdlabel and newfs", FB("disktab", 5),
   "Read as values by disk tools; after removal labelling disks by type becomes impossible (S2.2-2)."))
f(["/etc/dma"], R("MUST", "S2.2-1,S2.2-13", "DragonFly Mail Agent settings and SMTP authentication", FB("dma", 8),
   "Read as values (S2.2-13) by the mail agent; how and where the computer sends mail depends on it (S2.2-1)."))
f(["/etc/dumpdates"], R("NOT", "S2.2-6", "record of past dump(8) runs and levels", FB("dump", 8),
   "A history of past backups; S2.2-6 says records of the past need not be recorded."))
f(["/etc/fbtab"], R("MUST", "S2.2-1", "devices whose ownership login gives to console users", FB("fbtab", 5),
   "Access rules to devices at console login (S2.2-1)."))
f(["/etc/freebsd-update.conf"], R("MUST", "S2.2-1,S2.2-2", "freebsd-update server, key and components to update",
   FB("freebsd-update.conf", 5), "Without it freebsd-update cannot fetch updates (S2.2-2)."))
f(["/etc/fstab"], R("MUST", "S2.2-1,S2.2-2", "table of file systems mounted at boot", FB("fstab", 5),
   "File system mounts come from it; after removal they are not mounted (S2.2-2)."))
f(["/etc/ftpusers"], R("MUST", "S2.2-15", "accounts refused FTP login", FB("ftpusers", 5),
   "A rule about which accounts may log in over FTP (S2.2-15)."))
f(["/etc/gettytab"], R("MUST", "S2.2-1", "terminal line settings used by the running getty", FB("gettytab", 5),
   "getty sets up console logins from it (S2.2-1)."))
f(["/etc/group", "/etc/master.passwd", "/etc/passwd"], R("MUST", "S2.2-15", "account and group database source files",
   FB("passwd", 5), "They hold the accounts and their password-login state; S2.2-15 says both must be recorded."))
f(["/etc/pwd.db", "/etc/spwd.db"], R("MUST", "S2.2-15,S2.2-2", "account databases built by pwd_mkdb, read by libc for lookups",
   FB("pwd_mkdb", 8), "libc reads accounts from these databases; after removal account lookups and logins fail (S2.2-2, S2.2-15)."))
f(["/etc/gss"], R("MUST", "S2.2-1", "GSS-API mechanism and quality-of-protection tables", FB("mech", 5),
   "Which GSS mechanism libraries programs load depends on it (S2.2-1)."))
f(["/etc/hostid"], R("MUST", "S2.2-1", "host UUID saved by hostid_save and set at boot", FB("rc.conf", 5),
   "The host identity presented to programs depends on it; no sentence exempts it (S2.2-1)."))
f(["/etc/machine-id"], R("MUST", "S2.2-1", "machine identifier derived from the host UUID", FB("rc.conf", 5),
   "Programs identify the machine by it (S2.2-1)."))
f(["/etc/hosts"], R("MUST", "S2.2-1", "static host name to address table", FB("hosts", 5),
   "Name resolution of localhost and the host's own name depends on it (S2.2-1)."))
f(["/etc/hosts.allow"], R("MUST", "S2.2-1", "TCP wrappers access rules for sshd and other wrapped services", FB("hosts_access", 5),
   "Access rules deciding which hosts may use wrapped services (S2.2-1)."))
f(["/etc/hosts.equiv"], R("MUST", "S2.2-15", "trusted hosts allowed to log in without a password", FB("hosts.equiv", 5),
   "A rule allowing login to accounts; S2.2-15 requires login rules to be recorded."))
f(["/etc/hosts.lpd"], R("MUST", "S2.2-1", "hosts allowed to use the line printer daemon", FB("lpd", 8),
   "An access rule for printing (S2.2-1)."))
f(["/etc/inetd.conf"], R("MUST", "S2.2-15,S2.2-1", "services inetd starts on incoming connections", FB("inetd", 8),
   "It decides which ports inetd opens and what it runs; S2.2-15 requires open ports to be recorded."))
f(["/etc/kyua"], R("MUST", "S2.2-10,S2.2-13", "kyua.conf: Lua configuration file executed by the kyua test tool",
   FB("kyua.conf", 5), "kyua executes the file with its Lua interpreter, so it counts as code (S2.2-13) that S2.2-10 requires."))
f(["/etc/libalias.conf"], R("MUST", "S2.2-1", "list of libalias NAT protocol modules to load", FB("libalias", 3),
   "Which modules NAT loads depends on it (S2.2-1)."))
f(["/etc/libmap.conf"], R("MUST", "S2.2-1", "dynamic linker library substitution rules", FB("libmap.conf", 5),
   "Which libraries programs load depends on it (S2.2-1)."))
f(["/etc/locate.rc"], R("MUST", "S2.2-10,S2.2-13", "locate.updatedb settings, sourced as shell code", FB("locate.updatedb", 8),
   "The update script sources it as shell code (S2.2-13) with root rights; S2.2-10 requires such code to be recorded."))
f(["/etc/login.access"], R("MUST", "S2.2-15", "login access control table by user, group and origin", FB("login.access", 5),
   "Rules on who may log in from where; S2.2-15 requires login rules to be recorded."))
f(["/etc/login.conf"], R("MUST", "S2.2-1,S2.2-15", "login classes: environment, resource limits, password policy", FB("login.conf", 5),
   "Every login's limits and environment depend on it (S2.2-1), including password rules (S2.2-15)."))
f(["/etc/login.conf.db"], R("NOT", "S2.2-5", "hashed database built from login.conf by cap_mkdb", FB("cap_mkdb", 1),
   "getcap reads the text file when the database is missing; programs do the same, only more slowly (S2.2-5)."))
f(["/etc/mac.conf"], R("MUST", "S2.2-1,S2.2-13", "default MAC label elements for programs using mac(3)", FB("mac.conf", 5),
   "Read as values (S2.2-13) by libc for all programs, not one; their label handling depends on it (S2.2-1)."))
f(["/etc/mail"], R("MUST", "S2.2-1", "mail aliases, mailer.conf and sendmail configuration files", FB("mailer.conf", 5),
   "mailer.conf decides which program handles sendmail, and aliases where mail goes; mail depends on them (S2.2-1)."))
f(["/etc/mail.rc", "/home/census/.mailrc", "/home/census/.mail_aliases"], R("MUST", "S2.2-10,S2.2-13",
   "start-up command files executed by mail(1)", FB("mail", 1),
   "mail executes these files as its commands, which include shell escapes, so they count as code (S2.2-13) that S2.2-10 requires."))
f(["/etc/motd"], R("NOT", "S2.2-4", "link to the generated message of the day", FB("motd", 5),
   "Text content; after removal the computer does the same, only the message is not shown (S2.2-4)."))
f(["/etc/motd.template"], R("NOT", "S2.2-4", "template text for the message of the day", FB("motd", 5),
   "Text content; after removal only the message text is missing (S2.2-4)."))
f(["/etc/mtree"], R("MUST", "S2.2-1,S2.2-2", "mtree specifications of the base directory hierarchy", FB("mtree", 8),
   "rc and system updates create directories from them; after removal creating the /var hierarchy becomes impossible (S2.2-2)."))
f(["/etc/netconfig"], R("MUST", "S2.2-1", "network transport selection for RPC", FB("netconfig", 5),
   "RPC programs choose transports from it (S2.2-1)."))
RCSH = R("MUST", "S2.2-10", "shell code run by init/rc as root at boot, shutdown, suspend or resume", FB("rc", 8),
         "rc executes or sources it with root rights; S2.2-10 requires code another program executes to be recorded.")
f(["/etc/netstart", "/etc/network.subr", "/etc/pccard_ether", "/etc/rc", "/etc/rc.subr", "/etc/rc.shutdown",
   "/etc/rc.suspend", "/etc/rc.resume", "/etc/rc.initdiskless", "/etc/rc.d"], RCSH)
f(["/etc/rc.bsdextended", "/etc/rc.firewall"], R("MUST", "S2.2-10,S2.2-15", "shell scripts setting ugidfw or ipfw firewall rules",
   FB("rc.firewall", 8), "rc executes them as root (S2.2-10); they set access and firewall rules (S2.2-15)."))
f(["/etc/rc.conf"], R("MUST", "S2.2-10,S2.2-13", "system configuration: enabled services, network, host name", FB("rc.conf", 5),
   "rc sources it as shell code (S2.2-13); which services run and how the network is set depend on it (S2.2-10)."))
f(["/etc/periodic"], R("MUST", "S2.2-10", "daily, weekly, monthly and security maintenance scripts", FB("periodic", 8),
   "periodic runs these scripts as root from cron; S2.2-10 requires such code to be recorded."))
f(["/etc/networks"], R("MUST", "S2.2-1", "network names database", FB("networks", 5),
   "Read as values by the resolver functions; network name lookups depend on it (S2.2-1)."))
f(["/etc/newsyslog.conf", "/etc/newsyslog.conf.d"], R("MUST", "S2.2-1", "log rotation rules applied by newsyslog from cron",
   FB("newsyslog.conf", 5), "Its effect reaches files beyond newsyslog, so S2.2-7 does not fit; which logs are rotated or removed depends on it (S2.2-1)."))
f(["/etc/nscd.conf"], R("MUST", "S2.2-1,S2.2-13", "name service cache daemon settings", FB("nscd.conf", 5),
   "Read as values (S2.2-13); how lookups of all programs are cached depends on it (S2.2-1)."))
f(["/etc/nsmb.conf"], R("MUST", "S2.2-1", "SMB/CIFS client defaults for mount_smbfs", FB("nsmb.conf", 5),
   "How SMB shares are mounted depends on it (S2.2-1)."))
f(["/etc/nsswitch.conf"], R("MUST", "S2.2-1,S2.2-2", "name service switch: sources for users, hosts, groups", FB("nsswitch.conf", 5),
   "Account and host lookups follow it; behaviour of logins and resolution depends on it (S2.2-1)."))
f(["/etc/ntp"], R("NOT", "S2.2-4", "leap-seconds table published for ntpd", FB("ntp.conf", 5),
   "Published data; ntpd is not running and also learns leap seconds from servers; only the data itself is unavailable (S2.2-4)."))
f(["/etc/ntp.conf"], R("MUST", "S2.2-1,S2.2-13", "ntpd settings: time servers and access restrictions", FB("ntp.conf", 5),
   "Read as values (S2.2-13); how the system clock is set when ntpd runs depends on it (S2.2-1)."))
f(["/etc/os-release"], R("NOT", "S2.2-4", "link to the operating system identification generated at boot", FB("os-release", 5),
   "Descriptive identification text; S2.2-4 counts content as not needing recording."))
f(["/etc/pam.d", "/usr/local/etc/pam.d"], R("MUST", "S2.2-1,S2.2-15", "PAM policies for login, sshd, su, cron, sudo and others",
   FB("pam.conf", 5), "They decide how logins authenticate, including whether password login is allowed (S2.2-15, S2.2-1)."))
f(["/etc/pf.os"], R("MUST", "S2.2-1", "operating system fingerprints for pf rules", FB("pf.os", 5),
   "pf matches os rules against it; firewall behaviour depends on it (S2.2-1)."))
f(["/etc/phones", "/etc/remote"], R("NOT", "S2.2-7", "phone numbers and remote line descriptions for tip and cu", FB("remote", 5),
   "Settings in force only inside tip/cu; S2.2-7 says such settings need not be recorded."))
f(["/etc/pkg", "/usr/local/etc/pkg.conf"], R("MUST", "S2.2-1,S2.2-2", "pkg settings and the FreeBSD package repository definition",
   FB("pkg.conf", 5), "Without the repository definition installing packages becomes impossible (S2.2-2)."))
f(["/etc/ppp"], R("MUST", "S2.2-1", "ppp(8) connection profiles", FB("ppp", 8),
   "Which PPP connections can be made depends on it (S2.2-1)."))
f(["/etc/printcap"], R("MUST", "S2.2-1", "printer definitions for lpd", FB("printcap", 5),
   "Which printers can be used depends on it (S2.2-1)."))
f(["/etc/protocols", "/etc/services", "/etc/rpc"], R("MUST", "S2.2-1,S2.2-2", "protocol, service-port and RPC number databases",
   FB("services", 5), "Programs resolve names and ports through it; after removal such lookups fail (S2.2-2)."))
f(["/etc/regdomain.xml"], R("MUST", "S2.2-1,S2.2-13", "wireless regulatory domains and allowed channels", FB("regdomain", 5),
   "Read as values (S2.2-13) by ifconfig; which Wi-Fi channels can be used depends on it (S2.2-1)."))
f(["/etc/resolv.conf"], R("MUST", "S2.2-1,S2.2-2", "DNS resolver configuration written by dhclient/resolvconf", FB("resolv.conf", 5),
   "Without it the resolver queries a local server that does not run; name resolution fails (S2.2-2)."))
f(["/etc/rmt"], R("MUST", "S2.2-2,S2.2-9", "link to the remote tape program at the path remote dump clients call",
   FB("rmt", 8), "Remote dump and restore invoke /etc/rmt; after removal they cannot use this host's tapes (S2.2-2)."))
f(["/etc/security"], R("MUST", "S2.2-1,S2.2-10", "audit configuration: classes, events, users, warning script", FB("audit_control", 5),
   "auditd reads these values and runs audit_warn as root (S2.2-10); what is audited depends on them (S2.2-1)."))
f(["/etc/shells"], R("MUST", "S2.2-1", "list of valid login shells", FB("shells", 5),
   "chsh and services checking it decide which shells accounts may use (S2.2-1)."))
f(["/etc/snmpd.config"], R("MUST", "S2.2-15,S2.2-1", "bsnmpd configuration: listening port, communities, modules", FB("bsnmpd", 1),
   "It decides the port bsnmpd opens and who may query; S2.2-15 requires open ports to be recorded."))
f(["/etc/ssh"], R("MUST", "S2.2-1,S2.2-2", "sshd and ssh configuration and the host keys", "doc:https://man.openbsd.org/sshd.8",
   "sshd reads its configuration and host keys to run; removal stops sshd or changes the host identity (S2.2-1, S2.2-2)."))
f(["/etc/ssl"], R("MUST", "S2.2-1,S2.2-2", "OpenSSL configuration and links to trusted CA certificates", FB("certctl", 8),
   "TLS clients look up trusted CAs here; after removal verifying TLS servers becomes impossible (S2.2-2)."))
f(["/etc/sysctl.conf"], R("MUST", "S2.2-1", "kernel parameters set at boot", FB("sysctl.conf", 5),
   "Applied to the kernel at boot; kernel behaviour depends on it (S2.2-1)."))
f(["/etc/syslog.conf", "/etc/syslog.d"], R("MUST", "S2.2-1,S2.2-2", "syslogd rules routing messages to log files",
   FB("syslog.conf", 5), "Its effect reaches files beyond syslogd, so S2.2-7 does not fit; after removal those logs stop being written (S2.2-2)."))
f(["/etc/termcap"], R("MUST", "S2.2-2", "link to the terminal capability database at the path the library reads",
   "doc:https://lists.freebsd.org/archives/freebsd-current/2024-May/005908.html", "The terminal library falls back to /etc/termcap; after removal full-screen programs cannot find terminal descriptions (S2.2-2)."))
f(["/etc/termcap.small"], R("NOT", "S2.2-2", "small termcap with common terminals, not on the library's search path",
   FB("termcap", 5), "Nothing reads it unless copied or named in TERMCAP; removal changes nothing (S2.2-2)."))
f(["/etc/ttys"], R("MUST", "S2.2-1,S2.2-15", "terminals on which init starts getty, and root-login security flags",
   FB("ttys", 5), "Which consoles offer login, and whether root may log in on them, depend on it (S2.2-1, S2.2-15)."))
f(["/etc/unbound"], R("MUST", "S2.2-2", "link to the local_unbound configuration directory", FB("local-unbound", 8),
   "local_unbound reads its configuration through this path; after removal starting it becomes impossible (S2.2-2)."))
f(["/home/census/.exrc"], R("MUST", "S2.2-10,S2.2-13", "ex commands vi executes at start-up (set number)", FB("vi", 1),
   "vi executes the file as ex commands, an editor configuration in the editor's command language (S2.2-10); S2.2-13 counts it as code."))
f(["/root/.k5login"], R("MUST", "S2.2-15", "Kerberos principals allowed to log in as root", FB("ksu", 1),
   "It names who may log in to the root account; S2.2-15 requires login rights and keys to be recorded."))
f(["/home/census/.login_conf"], R("MUST", "S2.2-1,S2.2-13", "per-user login class overrides: environment, limits",
   FB("login.conf", 5), "Read as values (S2.2-13) by login, sshd and su, not one program; the user's sessions depend on it (S2.2-1)."))
f(["/usr/local/etc/sudo.conf"], R("MUST", "S2.2-1,S2.2-15", "sudo front-end settings: policy and I/O plugins, paths",
   "doc:https://www.sudo.ws/docs/man/sudo.conf.man/", "It selects the policy plugin that grants superuser rights (S2.2-15) and the plugins sudo loads (S2.2-1)."))
f(["/usr/local/etc/sudo_logsrvd.conf"], R("MUST", "S2.2-15,S2.2-1", "sudo log server settings: listening ports, storage",
   "doc:https://www.sudo.ws/docs/man/sudo_logsrvd.conf.man/", "It decides which ports sudo_logsrvd opens and where it writes; S2.2-15 requires open ports to be recorded."))
f(["/usr/local/etc/sudoers", "/usr/local/etc/sudoers.d"], R("MUST", "S2.2-15", "rules granting accounts the right to run commands as superuser",
   "doc:https://www.sudo.ws/docs/man/sudoers.man/", "The file grants the right to become superuser; S2.2-15 says this right must be recorded."))
f(["/usr/local/share"], R("UNKNOWN", "S2.2-4,S3-2", "shared files of local packages; info index and licenses visible",
   "evidence", "Visible members are documents (S2.2-4); most of the 129 members, possibly code or data programs use, are not visible (S3-2)."))
f(["/var/cache/nuageinit"], R("MUST", "S2.2-10,S2.2-2", "user-data script nuageinit copied for the first-boot rc script",
   "doc:https://man.freebsd.org/nuageinit/7", "A script rc runs as root at first boot (S2.2-10); after removal running it is impossible (S2.2-2)."))
f(["/var/crash"], R("MUST", "S2.2-1,S2.2-13", "minfree: free space savecore must leave when saving crash dumps",
   FB("savecore", 8), "Read as a value (S2.2-13) by the enabled savecore; whether crash dumps are written to disk depends on it (S2.2-1)."))
f(["/var/db/dhclient.leases.vtnet0"], R("NOT", "S2.2-4,S2.2-2", "DHCP lease database of interface vtnet0", FB("dhclient.leases", 5),
   "Database contents (S2.2-4); without it dhclient obtains a new lease and the network works the same (S2.2-2)."))
f(["/var/db/etcupdate"], R("HOLE", HOLE_DB + ",S2.2-6", "etcupdate's stock copy of /etc used for three-way merges",
   FB("etcupdate", 8), "Past copies (S2.2-4, S2.2-6, need not), but upgrades merge configuration from them and fail without them (S2.2-2, must); unresolved."))
f(["/var/db/freebsd-update"], R("NOT", "S2.2-5", "freebsd-update downloaded patches, file indexes and install state",
   FB("freebsd-update", 8), "Downloaded data fetched again on the next run; updating works the same, only more slowly (S2.2-5)."))
f(["/var/db/mergemaster.mtree"], R("UNKNOWN", "S2.2-6,S3-2", "mergemaster's checksum tree of stock /etc files",
   "doc:https://lists.freebsd.org/archives/dev-commits-src-all/2024-July/043328.html", "mergemaster was removed from FreeBSD 15; whether it is installed here, so whether anything reads this file, is not established (S3-2)."))
f(["/var/db/pkg"], R("HOLE", HOLE_DB + ",S2.2-5", "pkg database of installed packages and repository catalogues",
   FB("pkg", 8), "Catalogues are cache (S2.2-5); local.sqlite is database contents (S2.2-4, need not), yet without it pkg cannot manage packages (S2.2-2, must)."))
f(["/var/db/services.db"], R("NOT", "S2.2-5", "hashed services database built by services_mkdb", FB("services_mkdb", 8),
   "libc falls back to /etc/services when it is missing; lookups work the same, only more slowly (S2.2-5)."))
f(["/var/log/x1-bootstrap.done"], DONE)
f(["/var/mail"], R("NOT", "S2.2-4", "mailbox of user census", FB("mail", 1), "Mail is content; S2.2-4 says content need not be recorded."))
f(["/var/msgs"], R("NOT", "S2.2-4,S2.2-6", "msgs(1) bounds file of system message numbers", FB("msgs", 1),
   "Bookkeeping of system messages: content and past records (S2.2-4, S2.2-6)."))
f(["/var/run"], R("MUST", "S2.2-2", "runtime files: daemon PID files, dhclient PID, cleanvar marker", FB("rc.subr", 8),
   "rc stops and checks services through their PID files; after removal stopping them through rc becomes impossible (S2.2-2)."))
f(["/var/spool/lock"], R("HOLE", "S2.2-1,S2.2-6", "clean_var marker created by the cleanvar rc script", FB("rc", 8), STAMP_REASON))
f(["/var/yp"], R("MUST", "S2.2-10,S2.2-13", "NIS map Makefile executed by make when building maps", FB("ypinit", 8),
   "make executes the Makefile's commands as root when NIS maps are built, so it counts as code (S2.2-13, S2.2-10)."))


def key(row):
    m = "d" if row["machine"] == "debian-desktop" else "f"
    return f"{m}|{row['kind']}|{row['name'].replace(chr(92) * 2, chr(92))}"


def words(s):
    return len(s.split())


def main(inp, out):
    rows = list(csv.DictReader(open(inp, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE))
    done = set()
    if os.path.exists(out):
        done = {l.split("\t")[0] for l in open(out, encoding="utf-8").read().splitlines()[1:] if l}
    new = not os.path.exists(out)
    f_ = open(out, "a", encoding="utf-8")
    if new:
        f_.write("id\tdecision\tsentences\twhat_it_does\tbasis\treason\n")
    used, missing, tkeys = {}, [], set()
    for row in rows:
        tag, rec = rule(row)
        if rec is None:
            k = key(row)
            rec, tag = T.get(k), "T"
            if rec is not None:
                tkeys.add(k)
        if rec is None:
            missing.append(row["id"] + " " + key(row)); continue
        d_, s, w, b, r = rec
        assert words(w) <= 15, (row["id"], words(w), w)
        assert words(r) <= 30, (row["id"], words(r), r)
        for x in rec:
            assert "\t" not in x and "\n" not in x
        used.setdefault(tag, []).append(row["id"])
        if row["id"] in done:
            continue
        f_.write("\t".join([row["id"], d_, s, w, b, r]) + "\n")
    f_.close()
    for t, ids in sorted(used.items()):
        print(t, len(ids))
    print("unused table keys:", sorted(set(T) - tkeys))
    print("MISSING", len(missing), *missing, sep="\n  ")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--dry":
        sys.argv = [sys.argv[0], "A1/in/part-6.tsv", "/dev/null"]
    main(sys.argv[1], sys.argv[2])

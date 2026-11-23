#!/usr/bin/env python3
"""Classification c2, part 5 of A1: decide every row of A1/in/part-5.tsv.

Rules (stated in A1/c2/part-5.notes.md) are applied to homogeneous kinds;
everything else is decided row by row in TABLE below.
Usage: part5_decide.py <in.tsv> <out.tsv>   (appends only ids missing from out)
"""
import csv, os, re, sys

FD = "https://www.freedesktop.org/software/systemd/man/latest/"
M7 = "https://man7.org/linux/man-pages/"

def R(d, s="", w="", b="", r=""):
    return (d, s, w, b, r)

# ---------- rules for homogeneous kinds ----------
BACKUPS = {"/etc/group-", "/etc/passwd-", "/etc/shadow-", "/etc/gshadow-",
           "/etc/subuid-", "/etc/subgid-"}
STARTUP = (".bashrc", ".bash_profile", ".bash_logout", ".profile")

def rule(row):
    kind, name, ev = row["kind"], row["name"], row["evidence"]
    if kind == "account":
        m = re.search(r"uid=(\d+)", ev)
        return "A", R("MUST", "S2.2-15", f"user account {name}, uid {m.group(1)}, listed in the account database",
                      "evidence", "S2.2-15 states that accounts must be recorded; the object is an existing account.")
    if kind != "stored":
        return None, None
    if name.startswith("/var/log/") and name != "/var/log/README":
        return "L", R("NOT", "S2.2-6", "log or login-history file written by a program or the login system",
                      "evidence", "A log or history file is a record of the past; S2.2-6 says records of the past need not be recorded.")
    if name in BACKUPS:
        return "B", R("NOT", "S2.2-2,S2.2-6", "previous copy of an account file kept by shadow tools; nothing reads it",
                      "doc:" + M7 + "man8/vipw.8.html",
                      "Only a backup of the previous state; removal changes nothing the computer does (S2.2-2), and it is a record of the past (S2.2-6).")
    if name.endswith(STARTUP) or name == "/etc/profile":
        return "S", R("MUST", "S2.2-10", "shell startup file executed by bash/sh at login or shell start",
                      "doc:https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html",
                      "The shell executes this file with the user's rights; S2.2-10 names shell startup files as code that must be recorded.")
    if re.search(r"/(root|home/[^/]+|var/home/[^/]+)/\.ssh$", name) and "authorized_keys" in ev:
        return "K", R("MUST", "S2.2-15", "authorized_keys: public keys allowed to log in to this account over SSH",
                      "doc:https://man.openbsd.org/sshd.8#AUTHORIZED_KEYS_FILE_FORMAT",
                      "These are keys used to log in to an account; S2.2-15 says they must be recorded.")
    if name in ("/etc/sudoers.d", "/etc/doas.d"):
        return "U", R("MUST", "S2.2-15", "rules granting accounts the right to run commands as superuser",
                      "doc:https://www.sudo.ws/docs/man/sudoers.man/" if name == "/etc/sudoers.d" else "doc:https://man.openbsd.org/doas.conf.5",
                      "The file grants the right to become superuser; S2.2-15 says this right must be recorded.")
    if name.startswith("/var/cache/") and name not in ("/var/cache/debconf", "/var/cache/pollinate"):
        return "C", R("NOT", "S2.2-5", "cache of a program: downloaded indexes, packages or compiled data it can rebuild",
                      "evidence", "Regenerated or re-downloaded by its program; after removal the computer does the same, only more slowly (S2.2-5).")
    return None, None

# ---------- row-by-row decisions (key: name, or machine|name) ----------
HOLE_DB = "S2.2-4,S2.2-2"
T = {}
def put(keys, rec):
    for k in keys:
        T[k] = rec

# processes
put(["kernel threads"], R("MUST", "S2.2-1,S2.2-9", "kernel threads executing kernel code (workers, softirq, rcu, kswapd)",
    "evidence", "They are kernel code that runs on the computer; S2.2-9: a program that runs must be recorded, and behaviour depends on them (S2.2-1)."))
put(["ps"], R("MUST", "S2.2-9", "ps from procps, run by the inventory to list processes",
    "evidence", "A program that runs on the computer must be recorded regardless of how it was installed (S2.2-9); whether it is running now does not matter."))
# OpenRC service
put(["cloud-getty"], R("PENDING",))
# systemd units, single
put(["arch|pacman-init.service"], R("MUST", "S2.2-1,S2.2-2", "local unit that initializes and populates the pacman keyring",
    "evidence", "A service the service manager can start; after removal, keyring initialization by this service becomes impossible (S2.2-2)."))
put(["arch|swap-swapfile.swap", "silverblue|dev-disk-by\\x2ddiskseq-13.swap", "silverblue|dev-zram0.swap"],
    R("MUST", "S2.2-1,S2.2-2", "active swap area, generated from fstab or zram-generator",
      "doc:" + FD + "systemd.swap.html",
      "The computer's memory beyond RAM depends on it; without it programs exceeding RAM are killed, so something becomes impossible (S2.2-2)."))
put(["arch|user-unit|swap-swapfile.swap", "silverblue|user-unit|dev-disk-by\\x2ddiskseq-13.swap",
     "silverblue|user-unit|dev-disk-by\\x2dlabel-zram0.swap",
     "silverblue|user-unit|dev-disk-by\\x2duuid-4006196a\\x2d41f8\\x2d478c\\x2d936e\\x2def0fbc89c369.swap",
     "silverblue|user-unit|dev-zram0.swap"],
    R("MUST", "S2.2-1,S2.2-2", "the active system swap area as seen by the user service manager",
      "doc:" + FD + "systemd.swap.html",
      "It is the swap area in force on the computer; memory beyond RAM depends on it (S2.2-1), removal makes large workloads impossible (S2.2-2)."))
put(["silverblue|bootloader-update.service"], R("MUST", "S2.2-1,S2.2-16", "runs bootupd at boot to update the installed bootloader",
    "doc:https://github.com/coreos/bootupd", "A service that changes the bootloader at boot; the computer's boot depends on it (S2.2-1, S2.2-16)."))
put(["silverblue|systemd-zram-setup@zram0.service"], R("MUST", "S2.2-1,S2.2-2", "creates the compressed swap device /dev/zram0 at boot",
    "doc:https://github.com/systemd/zram-generator", "Without it the zram swap is not created and memory beyond RAM is unavailable (S2.2-2)."))
put(["silverblue|user@1000.service"], R("MUST", "S2.2-9,S2.2-1", "user service manager for UID 1000, runs that user's services",
    "doc:" + FD + "user@.service.html", "A program that runs on the computer (S2.2-9); the user's services depend on it."))
put(["ubuntu|netplan-ovs-cleanup.service"], R("MUST", "S2.2-1,S2.2-2", "service generated by netplan to clean Open vSwitch configuration",
    "doc:https://netplan.readthedocs.io/en/stable/netplan-generate/", "A service the service manager can start; after removal starting it becomes impossible (S2.2-2)."))
put(["ubuntu|systemd-networkd-wait-online.service"], R("MUST", "S2.2-1", "delays boot targets until the network is configured; netplan drop-in",
    "doc:" + FD + "systemd-networkd-wait-online.service.html", "An enabled service whose run decides when network-dependent services start (S2.2-1)."))
# unit groups
put(["system-units|unpackaged *.device", "user-units|unpackaged *.device"],
    R("MUST", "S2.2-1,S2.2-2", "systemd device units for present disks, partitions, serial ports, network card",
      "doc:" + FD + "systemd.device.html",
      "They are the devices the computer uses; removing a disk or its unit's device makes mounts, swap or the network impossible (S2.2-2)."))
put(["system-units|unpackaged *.mount", "user-units|unpackaged *.mount"],
    R("MUST", "S2.2-1,S2.2-2", "mounted file systems: root, boot, EFI, runtime and kernel file systems",
      "doc:" + FD + "systemd.mount.html", "The group includes the root file system mount; after its removal the computer can do nothing (S2.2-2)."))
put(["system-units|unpackaged *.automount"], R("MUST", "S2.2-1,S2.2-2", "mounts the EFI partition on first access",
    "doc:" + FD + "systemd.automount.html", "After removal, /efi is not mounted on access, so using the boot partition becomes impossible (S2.2-2)."))
put(["system-units|unpackaged *.not-found", "user-units|unpackaged *.not-found"],
    R("NOT", "S2.2-1,S2.2-2", "names referenced by other units for which no unit file exists",
      "doc:" + FD + "systemctl.html",
      "Nothing is loaded, runs or can be started under these names; behaviour does not depend on them and removal changes nothing (S2.2-1, S2.2-2)."))
put(["system-units|unpackaged *.scope"], R("MUST", "S2.2-9,S2.2-1", "init.scope holds PID 1; session scope holds a login session's processes",
    "doc:" + FD + "systemd.scope.html", "init.scope contains the running service manager, a program that runs (S2.2-9); the whole computer depends on it."))
put(["user-units|unpackaged *.scope"], R("MUST", "S2.2-9", "init.scope of the user manager: the running systemd --user process",
    "doc:" + FD + "systemd.scope.html", "It contains a program that runs on the computer (S2.2-9)."))
put(["system-units|unpackaged *.slice", "user-units|unpackaged *.slice"],
    R("MUST", "S2.2-1,S2.2-2", "cgroup slices in which the service manager places and limits units",
      "doc:" + FD + "systemd.slice.html", "The group includes the root slice; services cannot be placed without it, and resource limits are applied through slices (S2.2-1)."))
put(["system-units|unpackaged *.socket"], R("MUST", "S2.2-15,S2.2-1", "generated listening sockets for SSH over AF_UNIX (and vsock)",
    "doc:" + FD + "systemd-ssh-generator.html", "Listening sockets accept SSH logins; S2.2-15 says open ports must be recorded, and login over them depends on it (S2.2-1)."))
# directory-only remainder
put(["directory-only remainder"], R("UNKNOWN", "S3-2", "empty directories belonging to no package; members not available",
    "none", "The listed directories are not available to this classification, so what they do cannot be established; S3-2 gives ?."))

# ---------- stored objects ----------
BOOTMOD = R("MUST", "S2.2-1,S2.2-9", "SYSLINUX boot loader module executed at boot",
            "doc:https://wiki.syslinux.org/wiki/index.php?title=Library_modules",
            "Boot loader code run at boot or available to boot entries; booting depends on it (S2.2-1), it is code that runs (S2.2-9).")
put(["/boot/ldlinux.c32", "/boot/ldlinux.sys", "/boot/libcom32.c32", "/boot/libutil.c32", "/boot/mboot.c32",
     "/boot/menu.c32", "/boot/vesamenu.c32"], BOOTMOD)
put(["/boot/boot"], R("PENDING",))
put(["/boot/extlinux.conf"], R("MUST", "S2.2-1,S2.2-16", "EXTLINUX boot menu: boot entries, kernel and command line",
    "doc:https://wiki.syslinux.org/wiki/index.php?title=EXTLINUX", "The boot loader reads it to boot; without it the computer does not boot (S2.2-1, S2.2-2); it sets boot entries (S2.2-16)."))
put(["/boot/initramfs-virt", "/boot/initramfs-linux.img", "/boot/initrd.img-6.8.0-147-generic"],
    R("MUST", "S2.2-1,S2.2-9", "initial RAM file system loaded and executed at boot",
      "evidence", "Its init program runs at boot and mounts the root file system; without it the computer does not boot (S2.2-9, S2.2-1)."))
put(["/boot/vmlinuz-linux"], R("MUST", "S2.2-1,S2.2-9", "Linux kernel image booted by the boot loader",
    "evidence", "The kernel runs on the computer; without it the computer does not boot (S2.2-9, S2.2-1)."))
GRUB = R("MUST", "S2.2-1,S2.2-16", "GRUB boot loader: modules, configuration, environment block, fonts",
         "doc:https://www.gnu.org/software/grub/manual/grub/grub.html",
         "The boot loader and its configuration; the computer boots through it and it sets the boot entries (S2.2-1, S2.2-16).")
put(["/boot/grub", "/boot/grub2"], GRUB)
put(["/boot/efi"], R("MUST", "S2.2-1,S2.2-16", "EFI system partition: shim, GRUB EFI binaries, boot entry CSV",
    "doc:https://www.gnu.org/software/grub/manual/grub/grub.html", "Firmware starts these binaries to boot; without them the computer does not boot (S2.2-1, S2.2-16)."))
put(["/boot/bootupd-state.json"], R("PENDING",))
put(["/boot/loader", "/boot/loader.1"], R("MUST", "S2.2-16,S2.2-1", "boot loader entries for the OSTree deployments",
    "doc:https://ostreedev.github.io/ostree/deployment/", "They define which deployments the boot loader offers and in which order (S2.2-16); booting depends on them."))
put(["/boot/ostree"], R("MUST", "S2.2-1,S2.2-9", "kernels and initramfs images of the OSTree deployments",
    "doc:https://ostreedev.github.io/ostree/deployment/", "The kernel and initramfs run at boot; without them no deployment boots (S2.2-9, S2.2-1)."))
put(["/boot/initrd.img", "/boot/initrd.img.old", "/boot/vmlinuz", "/boot/vmlinuz.old"],
    R("NOT", "S2.2-2", "fixed-name symlink to the current kernel or initrd, for boot loaders using fixed names",
      "doc:https://manpages.debian.org/kernel-img.conf.5",
      "GRUB entries generated by grub-mkconfig name the versioned files; after removal of the alias the computer boots and does the same (S2.2-2)."))

put(["/etc/apk"], R("MUST", "S2.2-1,S2.2-2", "apk architecture, package repositories and world (selected packages)",
    "doc:https://wiki.alpinelinux.org/wiki/Alpine_Package_Keeper", "Without the repositories installing packages becomes impossible, and world decides what apk keeps installed (S2.2-2)."))
put(["/etc/conf.d"], R("MUST", "S2.2-10,S2.2-13", "OpenRC settings of the cloud-getty service instances, sourced by the init script",
    "doc:https://github.com/OpenRC/openrc/blob/master/user-guide.md", "openrc-run sources conf.d files as shell code; S2.2-13 counts such a file as code, which S2.2-10 requires to be recorded."))
put(["/etc/init.d"], R("MUST", "S2.2-10,S2.2-9", "OpenRC init script of the cloud-getty service, run as root",
    "doc:https://github.com/OpenRC/openrc/blob/master/user-guide.md", "Shell code executed by openrc-run with root rights (S2.2-10); it starts a service."))
put(["/etc/mkinitfs"], R("MUST", "S2.2-1,S2.2-13", "mkinitfs feature lists of kernel modules for gVNIC and Hyper-V PCI",
    "evidence", "They decide which drivers go into the initramfs, so booting with those devices depends on them (S2.2-1); read as values, a setting (S2.2-13)."))
put(["/etc/profile.d"], R("MUST", "S2.2-10", "shell script sourced by login shells to set the locale",
    "doc:https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html", "Sourced by the login shell with the user's rights: a shell startup file, which S2.2-10 requires to be recorded."))
put(["/etc/resolv.conf"], R("MUST", "S2.2-1,S2.2-2", "DNS resolver configuration (or link to the resolved stub) used by libc",
    "doc:" + M7 + "man5/resolv.conf.5.html", "Without it the resolver queries a server on the local host that is not configured; name resolution becomes impossible (S2.2-2)."))
put(["/etc/runlevels"], R("MUST", "S2.2-1,S2.2-2", "OpenRC runlevel links: which services start at boot",
    "doc:https://github.com/OpenRC/openrc/blob/master/user-guide.md", "They enable services; after removal those services no longer start (S2.2-2)."))
put(["/etc/ssh"], R("MUST", "S2.2-1,S2.2-2", "SSH server host keys (private and public) and other sshd files",
    "doc:https://man.openbsd.org/sshd.8", "sshd reads its host keys to run and prove the host's identity; removal stops sshd or changes the identity clients verify (S2.2-1, S2.2-2)."))
put(["/etc/sudoers.apk-new"], R("NOT", "S2.2-1,S2.2-2", "new packaged sudoers kept by apk beside the modified file; sudo does not read it",
    "doc:https://wiki.alpinelinux.org/wiki/Alpine_Package_Keeper", "sudo reads /etc/sudoers and its include directory, not this copy; removal changes nothing (S2.2-1, S2.2-2)."))
put(["/etc/udev"], R("MUST", "S2.2-1", "udev rules, including persistent network interface naming",
    "doc:https://man7.org/linux/man-pages/man7/udev.7.html", "udev applies these rules to devices; interface names and device handling depend on them (S2.2-1)."))
put(["/home/census/.inputrc"], R("MUST", "S2.2-1,S2.2-7,S2.2-13", "readline init file: key bindings and editing settings of the user",
    "doc:https://tiswww.case.edu/php/chet/readline/rluserman.html", "Read as values (S2.2-13) by every readline program, not one (S2.2-7 does not fit); command-line editing depends on it (S2.2-1)."))
put(["/etc/inputrc"], R("MUST", "S2.2-1,S2.2-7,S2.2-13", "system readline init file: key bindings for all readline programs",
    "doc:https://tiswww.case.edu/php/chet/readline/rluserman.html", "Read as values (S2.2-13) by every readline program, not one (S2.2-7 does not fit); command-line editing depends on it (S2.2-1)."))
put(["/home/census/.nanorc"], R("NOT", "S2.2-7,S2.2-13", "settings of the nano editor",
    "doc:https://www.nano-editor.org/dist/latest/nanorc.5.html", "nano reads it as values (S2.2-13); the settings are in force only inside nano, which S2.2-7 says need not be recorded."))
put(["/lib/apk"], R("MUST", "S2.2-10,S2.2-2", "apk installed-package database, lock, package scripts archive, triggers",
    "doc:https://wiki.alpinelinux.org/wiki/Alpine_Package_Keeper", "scripts.tar.gz holds package scripts apk runs as root (S2.2-10); without the database apk cannot manage packages (S2.2-2)."))
put(["/var/lib/cloud"], R("MUST", "S2.2-1,S2.2-2", "cloud-init instance data, per-instance semaphores and scripts",
    "doc:https://cloudinit.readthedocs.io/en/latest/reference/directory_layout.html", "cloud-init decides from it which modules already ran; removal makes it redo first-boot configuration (S2.2-1)."))
put(["/var/lib/dhcpcd"], R("MUST", "S2.2-1", "dhcpcd DHCP unique identifier, lease and secret for stable addresses",
    "doc:https://man.archlinux.org/man/dhcpcd.8", "The identifier and secret decide which identity and IPv6 addresses the computer uses on the network (S2.2-1); no exemption names them."))

put(["/etc/.pwd.lock"], R("NOT", "S2.2-2", "lock file used by lckpwdf while account files are edited",
    "doc:" + M7 + "man3/getspnam.3.html", "Created again when a tool locks the account files; removal changes nothing the computer does (S2.2-2)."))
STAMP = R("HOLE", "S2.2-1,S2.2-6", "stamp file: its absence makes a program repeat a one-time action",
          "evidence", "Readings: a record of the past (S2.2-6, need not) or something the computer's behaviour depends on (S2.2-1, must); no sentence says which prevails.")
put(["/etc/.updated", "/var/.updated"], R("HOLE", "S2.2-1,S2.2-6,S2.2-2",
    "systemd-update-done stamp; if older than /usr, boot reruns update services",
    "doc:" + FD + "systemd-update-done.service.html",
    "What boot does depends on it (S2.2-1, must), yet it is a record of the past (S2.2-6) and removal stops nothing (S2.2-2); no sentence settles it."))
put(["/etc/ca-certificates"], R("MUST", "S2.2-1,S2.2-2", "extracted trusted CA bundles generated by update-ca-trust",
    "doc:https://man.archlinux.org/man/update-ca-trust.8", "TLS clients read these bundles; after removal verifying TLS servers becomes impossible (S2.2-2)."))
put(["/etc/hostname"], R("MUST", "S2.2-1", "static host name of the computer",
    "doc:" + FD + "hostname.html", "The name the computer uses and announces on the network depends on it (S2.2-1)."))
put(["/etc/ld.so.cache"], R("NOT", "S2.2-5", "dynamic linker cache of library locations built by ldconfig",
    "doc:" + M7 + "man8/ld.so.8.html", "A cache: without it the linker searches the default directories, so programs start, only more slowly (S2.2-5)."))
put(["/etc/locale.conf"], R("MUST", "S2.2-1,S2.2-13", "system locale (LANG and related variables)",
    "doc:" + FD + "locale.conf.html", "Read as values (S2.2-13) by the service manager and login, it sets language and character encoding for all programs (S2.2-1)."))
put(["/etc/localtime"], R("MUST", "S2.2-1", "system time zone link read by libc",
    "doc:" + FD + "localtime.html", "The time zone of every program depends on it (S2.2-1)."))
put(["/etc/machine-id"], R("MUST", "S2.2-1,S2.2-2", "unique machine identifier; its absence makes systemd treat the boot as first boot",
    "doc:" + FD + "machine-id.html", "Removal makes the next boot a first boot (presets, first-boot units) and changes identifiers derived from it (S2.2-1)."))
put(["/etc/mkinitcpio.d"], R("MUST", "S2.2-10,S2.2-13", "mkinitcpio preset for the linux kernel, a bash file sourced by mkinitcpio",
    "doc:https://man.archlinux.org/man/mkinitcpio.8", "mkinitcpio sources the preset as bash code (S2.2-13 counts it as code, S2.2-10 requires it); kernel updates build the initramfs from it."))
put(["/etc/os-release"], R("NOT", "S2.2-2", "link to /usr/lib/os-release, the operating system identification",
    "doc:" + FD + "os-release.html", "Programs fall back to /usr/lib/os-release when /etc/os-release is missing; after removal they read the same data (S2.2-2)."))
put(["/etc/pacman.d"], R("MUST", "S2.2-1,S2.2-2", "pacman keyring (GnuPG home) of trusted packager keys",
    "doc:https://man.archlinux.org/man/pacman-key.8", "pacman verifies package signatures against it; after removal installing signed packages becomes impossible (S2.2-2)."))
put(["/etc/ssl"], R("MUST", "S2.2-1,S2.2-2", "CA certificate directory and bundle used by TLS libraries",
    "doc:" + M7 + "man1/openssl-rehash.1ssl.html", "TLS clients look up trusted CAs here; after removal verifying TLS servers becomes impossible (S2.2-2)."))
put(["/etc/systemd"], R("MUST", "S2.2-1,S2.2-2", "local systemd units, enablement links, network and control drop-ins",
    "doc:" + FD + "systemd.unit.html", "They decide which services are enabled and how; after removal enabled services stop starting (S2.2-2)."))
put(["/etc/vconsole.conf"], R("MUST", "S2.2-1,S2.2-13", "virtual console keymap and font settings (or link to keyboard defaults)",
    "doc:" + FD + "vconsole.conf.html", "Read as values (S2.2-13) by systemd-vconsole-setup; the console keyboard layout of all programs depends on it (S2.2-1)."))
put(["/var/cache/ldconfig"], R("NOT", "S2.2-5", "ldconfig auxiliary cache", "doc:" + M7 + "man8/ldconfig.8.html",
    "A cache of ldconfig; after removal ldconfig does the same, only more slowly (S2.2-5)."))
put(["/var/lib/dbus"], R("NOT", "S2.2-2", "compatibility link from the D-Bus machine-id path to /etc/machine-id",
    "doc:" + FD + "machine-id.html", "D-Bus also reads /etc/machine-id; after removal of the link it gets the same identifier (S2.2-2)."))
put(["/var/lib/lastlog"], R("NOT", "S2.2-6", "lastlog2 database of last logins", "evidence",
    "Records of past logins are history; S2.2-6 says records of the past need not be recorded."))
put(["/var/lib/pacman"], R("HOLE", HOLE_DB + ",S2.2-1", "pacman local database of installed packages and sync databases",
    "doc:https://man.archlinux.org/man/pacman.8",
    "Literally the contents of a database (S2.2-4, need not), but after removal pacman cannot manage installed packages (S2.2-2, must); no sentence says which prevails."))
put(["arch|/var/lib/systemd", "silverblue|/var/lib/systemd"], R("MUST", "S2.2-1,S2.2-2",
    "systemd state: lingering for user census, timer stamps, random seed",
    "doc:" + FD + "loginctl.html", "linger/census makes the user manager start at boot; after removal the user's services stop running without a login (S2.2-2)."))

put(["/etc/.rpm-ostree-shadow-mode-fixed2.stamp"], R("PENDING",))
put(["/etc/NetworkManager"], R("MUST", "S2.2-1,S2.2-2", "saved NetworkManager connection profile for interface ens3",
    "doc:https://networkmanager.dev/docs/api/latest/nm-settings-keyfile.html", "A saved network the computer connects with; after removal that connection is no longer made (S2.2-2, S2.2-14 by kind)."))
put(["/etc/alternatives"], R("MUST", "S2.2-1,S2.2-2", "alternatives links choosing which program runs under a common command name",
    "doc:" + M7 + "man1/update-alternatives.1.html", "Commands such as arptables run through these links; after removal those commands are not found (S2.2-2)."))
put(["/etc/alternatives-admindir"], R("HOLE", HOLE_DB + ",S2.2-1", "alternatives administrative database: registered choices for each name",
    "doc:" + M7 + "man1/update-alternatives.1.html",
    "Contents of a database (S2.2-4, need not), but after removal the alternatives tool cannot switch or repair these names (S2.2-2, must); no sentence says which prevails."))
put(["/etc/dconf"], R("MUST", "S2.2-1,S2.2-7", "compiled system dconf databases: defaults and locks for GNOME and GDM",
    "doc:https://help.gnome.org/admin/system-admin-guide/stable/dconf.html.en", "Settings read by many programs and the login screen, not one (S2.2-7 does not fit); their behaviour depends on them (S2.2-1)."))
put(["/etc/firewalld"], R("MUST", "S2.2-15", "firewalld zone definition FedoraWorkstation and its previous copy",
    "doc:https://firewalld.org/documentation/zone/", "The zone sets firewall rules and open ports; S2.2-15 says firewall rules and open ports must be recorded."))
put(["/etc/grub.d"], R("MUST", "S2.2-10", "grub-mkconfig script executed as root to generate boot entries",
    "doc:https://www.gnu.org/software/grub/manual/grub/grub.html", "A script executed by grub-mkconfig with its rights; S2.2-10 requires such code to be recorded."))
put(["/etc/nvme"], R("MUST", "S2.2-1", "NVMe over Fabrics host identifier and host NQN",
    "doc:https://github.com/linux-nvme/nvme-cli", "The identity nvme-cli presents to NVMe-oF targets depends on them (S2.2-1); no exemption names such identifiers."))
put(["silverblue|/etc/sysconfig"], R("PENDING",))
put(["silverblue|/etc/selinux"], R("MUST", "S2.2-1,S2.2-2", "SELinux targeted policy store: modules, booleans, file contexts",
    "doc:https://github.com/SELinuxProject/selinux-notebook", "The access rules enforced by the kernel come from this policy; after removal the policy cannot load (S2.2-1, S2.2-2)."))
put(["/var/.ostree-selabeled"], R("PENDING",))
put(["/var/home/census/.config/toolbox"], R("HOLE", "S2.2-1,S2.2-6,S2.2-7", "marker that toolbox has shown its welcome message on the host",
    "evidence", "Readings: a record of the past (S2.2-6) or a setting in one program (S2.2-7), need not; or toolbox behaviour depends on it (S2.2-1); unresolved."))
put(["/var/home/census/.local/share/flatpak"], R("UNKNOWN", "S2.2-9,S3-2", "per-user Flatpak installation; repository config seen, other members not available",
    "none", "Installed applications or remotes here would be programs to record (S2.2-9), but its 13 members are not available; what it holds is unknown (S3-2)."))
put(["/var/lib/NetworkManager"], R("MUST", "S2.2-1", "NetworkManager state: networking/radio enabled flags, internal config, leases, seen BSSIDs",
    "doc:https://networkmanager.dev/docs/api/latest/NetworkManager.html", "NetworkManager reads from it whether networking and radios are enabled; the computer's network behaviour depends on it (S2.2-1)."))
put(["/var/lib/authselect"], R("PENDING",))
put(["/var/lib/flatpak"], R("MUST", "S2.2-9", "system Flatpak installation: applications and runtimes",
    "doc:https://docs.flatpak.org/en/latest/flatpak-command-reference.html", "Holds application packages that run on the computer; S2.2-9 says a program must be recorded including a Flatpak."))
put(["/var/lib/nfs"], R("MUST", "S2.2-1,S2.2-2", "rpc_pipefs pipes used by rpc.gssd for Kerberos NFS",
    "doc:https://man7.org/linux/man-pages/man8/rpc.gssd.8.html", "Kernel upcall pipes for NFS security; without them Kerberos NFS mounts become impossible (S2.2-2)."))
put(["/var/lib/rpm"], R("PENDING",))
put(["/var/lib/rpm-ostree"], R("NOT", "S2.2-6", "rpm-ostree history of deployments", "evidence",
    "A history of past deployments; S2.2-6 says records of the past need not be recorded."))
put(["/var/lib/vagrant"], R("PENDING",))
put(["/var/log/README"], R("NOT", "S2.2-4,S2.2-2", "link to a systemd documentation file about logs",
    "evidence", "A document (S2.2-4); after removal the computer does and can do the same (S2.2-2)."))
put(["/var/roothome"], R("UNKNOWN", "S2.2-6,S2.2-10,S3-2", "root's home: kickstart files, Flatpak repo config; 15 other members not available",
    "none", "Seen members are installation records (S2.2-6); unseen members may include shell startup files (S2.2-10); what the group holds is unknown (S3-2)."))
put(["silverblue|/var/spool/mail"], R("NOT", "S2.2-4", "mailbox of user census", "evidence",
    "Mail is content; S2.2-4 says content need not be recorded."))

put(["/etc/.resolv.conf.systemd-resolved.bak"], R("NOT", "S2.2-2,S2.2-6", "backup of resolv.conf made when systemd-resolved was installed",
    "evidence", "Nothing reads the backup; removal changes nothing (S2.2-2); it keeps a past state (S2.2-6)."))
put(["/etc/apparmor.d"], R("MUST", "S2.2-1", "local AppArmor additions included into the shipped profiles",
    "doc:https://manpages.ubuntu.com/manpages/noble/man5/apparmor.d.5.html", "They are parts of the access rules applied to confined programs; what those programs may do depends on them (S2.2-1)."))
put(["/etc/apt"], R("MUST", "S2.2-1,S2.2-2", "APT package sources and unattended-upgrades policy",
    "doc:https://manpages.debian.org/sources.list.5", "Without the sources installing packages becomes impossible, and the policy decides automatic upgrades (S2.2-2, S2.2-1)."))
put(["/etc/ca-certificates.conf"], R("MUST", "S2.2-1", "list of CA certificates update-ca-certificates enables",
    "doc:https://manpages.debian.org/update-ca-certificates.8", "It decides which CAs the generated trust bundle contains, so which TLS servers can be verified (S2.2-1)."))
put(["/etc/ca-certificates.conf.dpkg-old"], R("NOT", "S2.2-2,S2.2-6", "dpkg's copy of the previous ca-certificates.conf",
    "doc:https://manpages.debian.org/dpkg.1", "No program reads the old copy; removal changes nothing (S2.2-2); it keeps a past state (S2.2-6)."))
put(["/etc/cloud"], R("MUST", "S2.2-1,S2.2-13", "cloud-init datasource list setting and image build information",
    "doc:https://cloudinit.readthedocs.io/en/latest/reference/base_config_reference.html", "cloud-init reads 90_dpkg.cfg as values (S2.2-13) to choose datasources; first-boot configuration depends on it (S2.2-1)."))
put(["/etc/console-setup"], R("PENDING",))
put(["/etc/crypttab"], R("MUST", "S2.2-1", "table of encrypted block devices to set up at boot",
    "doc:" + FD + "crypttab.html", "systemd-cryptsetup-generator reads it to unlock devices at boot; what is mounted depends on it (S2.2-1)."))
put(["/etc/default"], R("MUST", "S2.2-10,S2.2-13", "defaults for GRUB (sourced shell), keyboard, console-setup and others",
    "doc:https://www.gnu.org/software/grub/manual/grub/grub.html", "grub-mkconfig sources /etc/default/grub as shell code (S2.2-13, S2.2-10); keyboard settings set the console layout."))
put(["/etc/dpkg"], R("UNKNOWN", "S2.2-1,S3-2", "dpkg vendor origin link naming Ubuntu as the vendor",
    "doc:https://manpages.debian.org/dpkg-vendor.1", "Read by dpkg-vendor; whether any installed program uses it here cannot be established without the package list, so the effect is unknown (S3-2)."))
put(["/etc/ec2_version"], R("NOT", "S2.2-4,S2.2-2", "text naming the cloud image build", "evidence",
    "Descriptive content; nothing the computer does depends on it (S2.2-4, S2.2-2)."))
put(["/etc/environment"], R("MUST", "S2.2-1,S2.2-13", "system environment variables (PATH) set by pam_env for every session",
    "doc:" + M7 + "man8/pam_env.8.html", "Read as values (S2.2-13); which programs are found by name in every session depends on it (S2.2-1)."))
put(["/etc/fstab"], R("MUST", "S2.2-1,S2.2-2", "table of file systems mounted at boot",
    "doc:" + M7 + "man5/fstab.5.html", "Root, boot and EFI mounts come from it; after removal they are not mounted (S2.2-2)."))
put(["/etc/group", "/etc/gshadow", "/etc/passwd", "/etc/shadow"], R("MUST", "S2.2-15",
    "account database: accounts, groups, password-login state",
    "doc:" + M7 + "man5/passwd.5.html", "It holds the accounts and whether password login is allowed; S2.2-15 says both must be recorded."))
put(["/etc/hosts"], R("MUST", "S2.2-1", "static host name to address table", "doc:" + M7 + "man5/hosts.5.html",
    "Name resolution of localhost and the host's own name depends on it (S2.2-1)."))
put(["/etc/hosts.allow", "/etc/hosts.deny"], R("MUST", "S2.2-1", "TCP wrappers access rules for wrapped network services",
    "doc:https://linux.die.net/man/5/hosts.allow", "They are access rules deciding which hosts may use wrapped services (S2.2-1)."))
put(["/etc/initramfs-tools"], R("MUST", "S2.2-1", "list of modules added to the initramfs",
    "doc:https://manpages.debian.org/initramfs-tools.7", "Which drivers the initramfs has at boot depends on it (S2.2-1)."))
put(["/etc/iscsi"], R("MUST", "S2.2-1", "iSCSI initiator name of this host",
    "doc:https://github.com/open-iscsi/open-iscsi", "iscsid presents this name to targets and needs it to run; iSCSI use depends on it (S2.2-1)."))
put(["/etc/locale.gen"], R("PENDING",))
put(["ubuntu|/etc/locale.conf"], R("PENDING",))
put(["/etc/mdadm"], R("MUST", "S2.2-1", "mdadm configuration: arrays to assemble and monitoring",
    "doc:" + M7 + "man5/mdadm.conf.5.html", "Read as values; which RAID arrays are assembled and monitored depends on it (S2.2-1)."))
put(["/etc/modules"], R("MUST", "S2.2-1", "kernel modules loaded at boot", "doc:https://manpages.debian.org/modules.5",
    "Which drivers are loaded at boot depends on it (S2.2-1)."))
put(["/etc/mtab"], R("MUST", "S2.2-2", "link exposing the kernel mount table at the traditional path",
    "doc:" + M7 + "man5/fstab.5.html", "Programs reading /etc/mtab list mounts through it; after removal they cannot (S2.2-2)."))
put(["/etc/multipath"], R("MUST", "S2.2-1,S2.2-13", "multipath bindings of device WWIDs to names",
    "doc:https://manpages.debian.org/multipath.conf.5", "Read as values (S2.2-13) by multipathd; the names of multipath devices depend on it (S2.2-1)."))
put(["/etc/netplan"], R("MUST", "S2.2-1,S2.2-2", "netplan network configuration written by cloud-init",
    "doc:https://netplan.readthedocs.io/en/stable/netplan-yaml/", "The network configuration is generated from it; after removal the interface is not configured (S2.2-2)."))
put(["/etc/networks"], R("MUST", "S2.2-1", "network names database read by getnetbyname",
    "doc:" + M7 + "man5/networks.5.html", "Read as values by the resolver functions; network name lookups depend on it (S2.2-1)."))
put(["/etc/newt"], R("HOLE", "S2.2-1,S2.2-7", "colour palette link for programs using the newt library",
    "doc:" + M7 + "man1/update-alternatives.1.html", "A theme used by several newt programs: S2.2-7 exempts settings of one program only, S2.2-1 counts behaviour; whether appearance is behaviour is not stated."))
put(["/etc/nsswitch.conf"], R("MUST", "S2.2-1,S2.2-2", "name service switch: sources for users, hosts, groups",
    "doc:" + M7 + "man5/nsswitch.conf.5.html", "Account and host lookups follow it; behaviour of logins and resolution depends on it (S2.2-1)."))
put(["/etc/overlayroot.local.conf"], R("MUST", "S2.2-1,S2.2-13", "overlayroot setting: whether root is mounted read-only with an overlay",
    "evidence", "Read by the initramfs at boot; how the root file system is mounted depends on it (S2.2-1)."))
put(["/etc/pam.d"], R("MUST", "S2.2-1,S2.2-15", "PAM common configuration for account, auth, password, session",
    "doc:https://manpages.debian.org/pam-auth-update.8", "They decide how logins authenticate, including whether password login is allowed (S2.2-15, S2.2-1)."))
put(["/etc/python3"], R("UNKNOWN", "S2.2-5,S2.2-10,S3-2", "Debian Python 3 helper configuration; second member not available",
    "evidence", "debian_config only sets byte-compilation options; the other member is not available and may be code run by python; unknown (S3-2)."))
RC = R("MUST", "S2.2-1", "SysV runlevel links: which init scripts start or stop in the runlevel",
       "doc:" + FD + "systemd-sysv-generator.html",
       "systemd-sysv-generator uses these links to enable init scripts without native units; service enablement depends on them (S2.2-1).")
put(["/etc/rc0.d", "/etc/rc1.d", "/etc/rc2.d", "/etc/rc3.d", "/etc/rc4.d", "/etc/rc5.d", "/etc/rc6.d", "/etc/rcS.d"], RC)
put(["/etc/rsyslog.d"], R("MUST", "S2.2-2,S2.2-7", "rsyslog rules routing messages to log files",
    "doc:https://www.rsyslog.com/doc/configuration/index.html", "Its effect reaches beyond rsyslog (files written), so S2.2-7 does not fit; after removal the computer stops writing those logs (S2.2-2)."))
put(["/etc/security"], R("NOT", "S2.2-6,S2.2-15", "opasswd: history of old password hashes for reuse checks",
    "doc:" + M7 + "man8/pam_pwhistory.8.html", "A history of past passwords: records of the past (S2.2-6); account passwords need not be recorded (S2.2-15)."))
CAT = R("MUST", "S2.2-1,S2.2-2", "SGML/XML catalog mapping public identifiers to local DTD files",
        "doc:https://manpages.debian.org/update-xmlcatalog.1", "Programs resolving these identifiers use the local files through it; after removal offline resolution becomes impossible (S2.2-2).")
put(["/etc/sgml", "/etc/xml", "/var/lib/sgml-base", "/var/lib/xml-core"], CAT)
put(["/etc/shells"], R("MUST", "S2.2-1", "list of valid login shells", "doc:" + M7 + "man5/shells.5.html",
    "chsh and services checking it decide which shells accounts may use (S2.2-1)."))
put(["/etc/subgid", "/etc/subuid"], R("MUST", "S2.2-1,S2.2-2", "subordinate ID ranges for user namespaces",
    "doc:" + M7 + "man5/subuid.5.html", "After removal rootless containers of the user become impossible (S2.2-2)."))
put(["/etc/sysctl.d"], R("MUST", "S2.2-1", "kernel parameter setting from the cloud image (IPv6)",
    "doc:" + FD + "sysctl.d.html", "Applied to the kernel at boot; network behaviour depends on it (S2.2-1)."))
put(["/etc/timezone"], R("MUST", "S2.2-1", "Debian time zone name file", "doc:https://wiki.debian.org/TimeZoneChanges",
    "Read as the system time zone name by programs and tzdata configuration (S2.2-1)."))
put(["/etc/tmpfiles.d"], R("MUST", "S2.2-1", "tmpfiles rule for the screen runtime directory",
    "doc:" + FD + "tmpfiles.d.html", "systemd-tmpfiles applies it at boot; the runtime directory screen needs depends on it (S2.2-1)."))
put(["/etc/ufw"], R("MUST", "S2.2-15", "ufw firewall rules and hooks", "doc:https://manpages.ubuntu.com/manpages/noble/man8/ufw.8.html",
    "Firewall rules; S2.2-15 says firewall rules must be recorded."))
put(["/etc/update-motd.d"], R("MUST", "S2.2-10", "link to a script run by pam_motd at login to print system info",
    "doc:https://manpages.ubuntu.com/manpages/noble/man5/update-motd.5.html", "Executed as root at login by run-parts; S2.2-10 requires code another program runs with its rights."))
put(["/etc/vtrgb"], R("HOLE", "S2.2-1,S2.2-7", "virtual console colour map link (alternatives)",
    "doc:" + M7 + "man1/update-alternatives.1.html", "A colour theme of the console used by all console programs: S2.2-7 exempts one-program settings only, S2.2-1 counts behaviour; appearance is not addressed."))
put(["/home/census/.cache/motd.legal-displayed", "/home/census/.sudo_as_admin_successful"], STAMP)
put(["/usr/local/man"], R("NOT", "S2.2-4,S2.2-2", "link to the local manual page directory", "evidence",
    "Manual pages are documents (S2.2-4); after removal of the link the computer does the same (S2.2-2)."))
put(["/var/cache/debconf"], R("HOLE", "S2.2-4,S2.2-5,S2.2-2", "debconf database of package configuration answers and templates",
    "doc:https://manpages.debian.org/debconf.conf.5", "Database contents (S2.2-4) in a cache directory (S2.2-5), need not; but packages reconfigure from these answers (S2.2-2, must); unresolved."))
put(["/var/cache/pollinate"], R("HOLE", "S2.2-1,S2.2-5,S2.2-6", "marker that pollinate already seeded the random generator",
    "evidence", "Its absence makes boot fetch seed data again: behaviour depends on it (S2.2-1), yet it is a past record in a cache directory (S2.2-5, S2.2-6)."))
put(["/var/lib/PackageKit"], R("NOT", "S2.2-6", "PackageKit database of past transactions", "evidence",
    "A history of transactions; S2.2-6 says records of the past need not be recorded."))
put(["/var/lib/app-info", "/var/lib/swcatalog"], R("NOT", "S2.2-5", "AppStream catalog data derived from APT lists",
    "doc:https://www.freedesktop.org/software/appstream/docs/", "Regenerated from package indexes by apt update; after removal software centres do the same, only more slowly (S2.2-5)."))
put(["/var/lib/apt"], R("HOLE", HOLE_DB + ",S2.2-5", "APT package lists (indexes) and extended_states automatic-install marks",
    "doc:https://manpages.debian.org/apt-mark.8", "Lists are cache (S2.2-5); extended_states is database contents (S2.2-4, need not) yet decides what autoremove removes (S2.2-2, must); unresolved."))
put(["/var/lib/command-not-found"], R("HOLE", HOLE_DB + ",S2.2-5", "database mapping commands to the packages providing them",
    "evidence", "Database contents (S2.2-4, need not), yet after removal command suggestions are impossible until regenerated (S2.2-2, must); no sentence says which prevails."))
put(["/var/lib/dpkg"], R("HOLE", HOLE_DB + ",S2.2-1", "dpkg database: alternatives registry and package state",
    "doc:https://manpages.debian.org/dpkg.1", "Contents of a database (S2.2-4, need not), but after removal dpkg and alternatives cannot manage packages (S2.2-2, must); unresolved."))
put(["/var/lib/grub"], R("NOT", "S2.2-6", "ucf copy of the previous /etc/default/grub", "doc:https://manpages.debian.org/ucf.1",
    "A copy of a past state kept for merges; S2.2-6 says records of the past need not be recorded."))
put(["/var/lib/landscape"], R("PENDING",))
put(["/var/lib/man-db"], R("NOT", "S2.2-7,S2.2-5", "flag enabling man-db to update its index after package changes",
    "evidence", "A setting in force only inside man-db that affects only its index cache (S2.2-7, S2.2-5)."))
put(["/var/lib/pam"], R("HOLE", HOLE_DB, "pam-auth-update state of enabled and seen profiles",
    "doc:https://manpages.debian.org/pam-auth-update.8", "Database contents (S2.2-4, need not), but later package updates rewrite PAM configuration from it (S2.2-2, must); no sentence says which prevails."))
put(["/var/lib/python"], R("PENDING",))
put(["/var/lib/shells.state"], R("HOLE", HOLE_DB, "update-shells record of shells registered by packages",
    "doc:https://manpages.debian.org/update-shells.8", "Database contents (S2.2-4, need not), but update-shells derives /etc/shells from it on package changes (S2.2-2, must); unresolved."))
put(["/var/lib/snapd"], R("MUST", "S2.2-1,S2.2-2", "snapd state, assertions, AppArmor snippet for snap-confine",
    "doc:https://snapcraft.io/docs/", "Includes AppArmor rules for snap-confine and snapd's state; after removal snaps cannot be confined or managed (S2.2-2)."))
put(["ubuntu|/var/lib/systemd"], R("HOLE", HOLE_DB + ",S2.2-5", "systemd catalog database and deb-systemd-helper enablement records",
    "doc:https://manpages.debian.org/deb-systemd-helper.1p", "Catalog is rebuildable (S2.2-5); helper records are database contents (S2.2-4) yet decide unit enablement on upgrades (S2.2-2); unresolved."))
put(["/var/lib/ubuntu-advantage"], R("UNKNOWN", "S2.2-5,S3-2", "Ubuntu Pro client: ESM APT cache tree and other state",
    "evidence", "The apt-esm tree is a cache (S2.2-5); 28 members, others not available, so what the group holds is unknown (S3-2)."))
put(["/var/lib/ubuntu-release-upgrader", "/var/lib/update-manager", "/var/lib/update-notifier"],
    R("NOT", "S2.2-5", "cached results of release and update checks shown in the login message",
      "evidence", "Regenerated by the checking scripts; after removal the computer does the same, only more slowly (S2.2-5)."))
put(["/var/lib/ucf"], R("HOLE", HOLE_DB + ",S2.2-6", "ucf registry and pristine copies of configuration files",
    "doc:https://manpages.debian.org/ucf.1", "Past copies and database contents (S2.2-4, S2.2-6, need not), but upgrades decide whether to replace configuration from them (S2.2-2, must)."))
put(["ubuntu|/var/spool/mail"], R("UNKNOWN", "S2.2-2,S3-2", "compatibility link /var/spool/mail -> /var/mail",
    "none", "Whether any installed mail program uses this path cannot be established without the package list; the removal effect is unknown (S3-2)."))

# ---------- rows decided after documentation checks ----------
put(["cloud-getty"], R("MUST", "S2.2-1,S2.2-9", "boot one-shot of the cloud image that sets up gettys on serial/VGA consoles",
    "doc:https://gitlab.alpinelinux.org/alpine/cloud/alpine-cloud-images/-/merge_requests/179",
    "A service started at boot that provides console logins; after removal console login through it becomes impossible (S2.2-1, S2.2-9)."))
put(["/boot/boot"], R("UNKNOWN", "S2.2-2,S3-2", "link /boot/boot -> . so /boot/... paths work on a separate boot partition",
    "doc:https://github.com/ostreedev/ostree/commit/0ced9fde7649271d9458ca424aa8c41908634b02",
    "Whether the boot entries here use the /boot/ prefix needs the boot configuration, which is not available; the removal effect is unknown (S3-2)."))
put(["/boot/bootupd-state.json"], R("HOLE", "S2.2-4,S2.2-6,S2.2-2", "bootupd record of installed bootloader component versions",
    "doc:https://docs.rs/crate/bootupd/latest/source/src/model.rs",
    "A record of state (S2.2-4, S2.2-6, need not); without it bootupctl update may require explicit adoption, stopping automatic updates (S2.2-2, must); unresolved."))
put(["/etc/.rpm-ostree-shadow-mode-fixed2.stamp"], R("HOLE", "S2.2-1,S2.2-6", "stamp; if absent rpm-ostree-fix-shadow-mode.service fixes shadow permissions again",
    "doc:https://github.com/coreos/rpm-ostree/blob/main/src/daemon/rpm-ostree-fix-shadow-mode.service",
    "Readings: a record of the past (S2.2-6, need not) or something boot behaviour depends on (S2.2-1, must); no sentence says which prevails."))
put(["/var/.ostree-selabeled"], R("HOLE", "S2.2-1,S2.2-6", "stamp; if absent ostree relabels /var when creating a deployment",
    "doc:https://github.com/ostreedev/ostree/blob/main/src/libostree/ostree-sysroot-deploy.c",
    "Readings: a record of the past (S2.2-6, need not) or something deployment behaviour depends on (S2.2-1, must); no sentence says which prevails."))
put(["/var/lib/authselect"], R("HOLE", "S2.2-1,S2.2-6", "copy of the profiles checksum; if absent boot re-applies the authselect profile",
    "doc:https://github.com/authselect/authselect/blob/master/src/lib/paths.h",
    "Readings: a record of the past (S2.2-6, need not) or something boot behaviour depends on (S2.2-1, must); no sentence says which prevails."))
put(["ubuntu|/etc/console-setup"], R("UNKNOWN", "S2.2-5,S3-2", "console keymap/font caches from setupcon, plus two uncached font/map files",
    "doc:https://sources.debian.org/src/console-setup/unstable/init/console-setup.sh/",
    "cached_ files are rebuilt by setupcon at boot (S2.2-5); what wrote and reads the two uncached files was not established (S3-2)."))
put(["ubuntu|/etc/locale.conf"], R("MUST", "S2.2-1,S2.2-13", "system locale file read and written by systemd on Ubuntu 24.04",
    "doc:https://github.com/systemd/systemd/blob/v255/src/shared/locale-setup.c",
    "Read as values (S2.2-13) by the service manager; language and encoding of all programs depend on it (S2.2-1)."))
put(["/etc/locale.gen"], R("MUST", "S2.2-1,S2.2-2", "list of locales locale-gen compiles; locale-gen exits if it is missing",
    "doc:https://git.launchpad.net/ubuntu/+source/glibc/tree/debian/local/usr_sbin/locale-gen?h=ubuntu/noble-updates",
    "After removal locale-gen compiles nothing, so generating the configured locales becomes impossible (S2.2-2)."))
put(["/var/lib/vagrant"], R("UNKNOWN", "S2.2-2,S3-2", "rpm-ostree compatibility link /var/lib/vagrant -> /usr/lib/vagrant",
    "doc:https://github.com/coreos/rpm-ostree/blob/main/rust/src/composepost.rs",
    "It matters only if vagrant is installed; the package list is not available, so the removal effect is unknown (S3-2)."))
put(["/var/lib/rpm"], R("UNKNOWN", "S2.2-2,S3-2", "compatibility link to the rpm database in /usr/share/rpm",
    "doc:https://github.com/coreos/rpm-ostree/blob/main/rust/src/composepost.rs",
    "rpm uses /usr/share/rpm directly; the link works around libsolv, and what breaks without it was not established (S3-2)."))
put(["/var/lib/landscape"], R("HOLE", "S2.2-1,S2.2-5,S2.2-6", "sysinfo cache and marker that the package created the landscape account",
    "doc:https://github.com/canonical/landscape-client/blob/main/debian/landscape-common.postrm",
    "Cache (S2.2-5) and a past record (S2.2-6), need not; but purge deletes the landscape account only if the marker exists (S2.2-1, must)."))
put(["/var/lib/python"], R("NOT", "S2.2-6,S2.2-2", "marker written when the python3.12 runtime was first installed",
    "doc:https://git.launchpad.net/ubuntu/+source/python3.12/tree/debian/PVER-minimal.preinst.in?h=ubuntu/noble-updates",
    "A record of a past installation (S2.2-6); no reader of it was found, so removal changes nothing (S2.2-2)."))
put(["silverblue|/etc/sysconfig"], R("UNKNOWN", "S2.2-7,S3-2", "installer record read by gnome-initial-setup, and legacy network file",
    "doc:https://anaconda-installer.readthedocs.io/en/latest/developer/sysconfig-file.html",
    "The anaconda file is read by gnome-initial-setup; whether anything on this release reads /etc/sysconfig/network was not established (S3-2)."))


def lookup(row):
    m, k, n = row["machine"], row["kind"], row["name"].replace("\\\\", "\\")
    if k in ("system-units", "user-units"):
        keys = [f"{k}|{n}"]
    elif k == "user-unit":
        keys = [f"{m}|user-unit|{n}"]
    else:
        keys = [f"{m}|{n}", n]
    for key in keys:
        if key in T:
            return T[key]
    return None


def words(s):
    return len(s.split())


def main(inp, out):
    rows = list(csv.DictReader(open(inp, encoding="utf-8"), delimiter="\t"))
    done = set()
    if os.path.exists(out):
        done = {l.split("\t")[0] for l in open(out, encoding="utf-8").read().splitlines()[1:] if l}
    new = not os.path.exists(out)
    f = open(out, "a", encoding="utf-8")
    if new:
        f.write("id\tdecision\tsentences\twhat_it_does\tbasis\treason\n")
    rules_used, missing, pending = {}, [], []
    for row in rows:
        if row["id"] in done:
            continue
        tag, rec = rule(row)
        if rec is None:
            rec = lookup(row)
            tag = "T"
        if rec is None:
            missing.append(row["id"] + " " + row["name"]); continue
        if rec[0] == "PENDING":
            pending.append(row["id"] + " " + row["name"]); continue
        d, s, w, b, r = rec
        assert words(w) <= 15, (row["id"], w)
        assert words(r) <= 30, (row["id"], words(r), r)
        for x in rec:
            assert "\t" not in x and "\n" not in x
        f.write("\t".join([row["id"], d, s, w, b, r]) + "\n")
        rules_used.setdefault(tag, []).append(row["id"])
    f.close()
    for t, ids in sorted(rules_used.items()):
        print(t, len(ids))
    print("MISSING", len(missing), *missing, sep="\n  ")
    print("PENDING", len(pending), *pending, sep="\n  ")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

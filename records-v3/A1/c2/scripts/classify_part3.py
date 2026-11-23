"""Classification c2, part 3 of A1: decide for every input row whether the object must be recorded.

Rules (stated in A1/c2/part-3.notes.md) are applied per kind; non-homogeneous rows are decided row by row
in the tables below. Appends to the output file; ids already present are kept and skipped.
Usage: classify_part3.py <input part-3.tsv> <output part-3.tsv>
"""
import csv
import os
import re
import sys

NP = "https://github.com/NixOS/nixpkgs/blob/master/"
DOC_XRT = "doc:" + NP + "nixos/" + "lib" + "/systemd-lib.nix"
DOC_SWITCH = "doc:" + NP + "nixos/modules/system/activation/switchable-system.nix"
DOC_UDEV = "doc:" + NP + "nixos/modules/services/hardware/udev.nix"
DOC_STAGE2 = "doc:" + NP + "nixos/modules/system/boot/stage-2.nix"
DOC_DHCPCD = "doc:" + NP + "nixos/modules/services/networking/dhcpcd.nix"
DOC_CONSOLE = "doc:" + NP + "nixos/modules/config/console.nix"
DOC_NET = "doc:" + NP + "nixos/modules/config/networking.nix"
DOC_KERNEL = "doc:" + NP + "nixos/modules/system/boot/kernel.nix"
DOC_SSHD = "doc:" + NP + "nixos/modules/services/networking/ssh/sshd.nix"

# ---- reusable decisions: (decision, sentences, reason) ----
R = {
    "doc": ("NOT", "S2.2-3,S2.2-4",
            "Documents read by people; after removal the computer does and can do the same, only the documentation text is unavailable (S2.2-4)."),
    "prog": ("MUST", "S2.2-2,S2.2-9,S2.2-10",
             "A program, or library code programs execute with their own rights; removal stops the programs that run it or makes them impossible to start."),
    "unitfile": ("MUST", "S2.2-1,S2.2-2",
                 "Removal makes starting the unit impossible and stops what it runs, mounts or orders; its effect is not confined inside one program."),
    "script": ("MUST", "S2.2-10,S2.2-13",
               "Code an interpreter or program executes with its own rights (S2.2-10); a file executed as code counts as code (S2.2-13)."),
    "shellstart": ("MUST", "S2.2-10",
                   "Shell startup code executed by bash with the shell's rights; S2.2-10 names shell startup files explicitly."),
    "xrt": ("NOT", "S2.2-2",
            "No program reads the file at run time; only its path appears in the unit file, so removal stops nothing and makes nothing impossible."),
    "shareddata": ("MUST", "S2.2-1,S2.2-2,S2.2-7,S2.2-13",
                   "Values read by many programs (a setting, S2.2-13), so S2.2-7 does not exempt it; removal changes what those programs do (S2.2-2)."),
    "sharedsetting": ("MUST", "S2.2-1,S2.2-2,S2.2-7,S2.2-13",
                      "Setting read by several programs, so S2.2-7 (one program) does not exempt it; removal changes what the computer does (S2.2-2)."),
    "single": ("HOLE", "S2.2-7,S2.2-2",
               "Read by one program but acts beyond it. S2.2-7 reading 'read only by one program' gives NOT; reading 'effect stays inside that program' with S2.2-2 gives MUST."),
    "ifaceonly": ("NOT", "S2.2-7",
                  "Setting in force only inside one program, affecting only that program's own interface, like the browser examples of S2.2-7."),
    "gruptheme": ("NOT", "S2.2-7",
                  "Theme of the boot loader menu, in force only inside GRUB; S2.2-7 names a program's theme as not needing recording."),
    "appearance": ("HOLE", "S2.2-1,S2.2-7",
                   "Font/theme shared by many programs: S2.2-7 exempts a theme only inside one program; the text does not say whether shared appearance is behaviour under S2.2-1."),
    "login": ("MUST", "S2.2-15,S2.2-2",
              "Authentication rules (incl. whether password login is allowed) or rights to become superuser; S2.2-15 requires them; removal makes the login/su path impossible."),
    "keys": ("MUST", "S2.2-15",
             "Keys used to log in to an account; S2.2-15 requires them to be recorded."),
    "accounts": ("MUST", "S2.2-15",
                 "Defines accounts (names, ids, groups); S2.2-15 requires accounts to be recorded."),
    "boot": ("MUST", "S2.2-16,S2.2-2",
             "Determines the boot menu/boot order the system can change (S2.2-16); removal makes booting the system impossible (S2.2-2)."),
    "firmware": ("MUST", "S2.2-16,S2.2-2",
                 "Device firmware the kernel loads for drivers; S2.2-16 requires device firmware; removal stops devices needing it."),
    "kmod": ("MUST", "S2.2-10,S2.2-2",
             "Code the kernel executes with the kernel's own rights (S2.2-10); unloading it removes the capability it provides (S2.2-2)."),
    "process": ("MUST", "S2.2-9",
                "A program that runs on the computer; S2.2-9 requires it regardless of how it was installed."),
    "cache": ("NOT", "S2.2-5",
              "Cache: regenerated when missing; after removal the computer does the same, only more slowly (S2.2-5)."),
    "logs": ("NOT", "S2.2-6",
             "Records of the past (logs, login history); S2.2-6 says they need not be recorded."),
    "content": ("NOT", "S2.2-4",
                "User document (content); after removal the computer does and can do the same, only the content is unavailable (S2.2-4)."),
    "unknown": ("UNKNOWN", "S3-2",
                "What the object does is not established by the evidence, inventory files or found documentation; S3-2 gives ?."),
}

# ---- system-closure store objects: ordered rules on the name after the hash ----
STORE_EXPLICIT = {
    # data read by many programs
    "tzdata-2026f": ("shareddata", "time zone database read by the C library and programs", "evidence"),
    "iana-etc-20251215": ("shareddata", "/etc/services and /etc/protocols data for all programs", "evidence"),
    "nss-cacert-3.131.1": ("shareddata", "trusted CA certificate bundle used for TLS by many programs", "evidence"),
    "nss-cacert-3.131.1-p11kit": ("shareddata", "CA trust store in p11-kit format used by TLS libraries", "evidence"),
    "publicsuffix-list-0-unstable-2026-05-13": ("shareddata", "public suffix list used by libpsl/curl for cookie domains", "evidence"),
    "dns-root-data-2025-04-14": ("shareddata", "DNS root hints and DNSSEC trust anchor read by resolver libraries", "evidence"),
    "mailcap-2.1.54": ("shareddata", "MIME type to handler mapping read by many programs", "evidence"),
    "glibc-locales-2.42-103": ("shareddata", "compiled locales used by the C library in all programs", "evidence"),
    "shared-mime-info-2.4": ("shareddata", "MIME type database read by many programs", "evidence"),
    "hwdb.bin": ("shareddata", "udev hardware database queried by udev and libudev users", DOC_UDEV),
    "kmod-blacklist-31+20240202-2ubuntu8": ("sharedsetting", "modprobe blacklist of kernel modules, read by kmod tools and udev", "evidence"),
    "kmod-debian-aliases.conf-30+20230601-2": ("sharedsetting", "modprobe aliases for kernel modules, read by kmod tools and udev", "evidence"),
    "50-coredump.conf": ("sharedsetting", "kernel sysctl for core dumps, applied by systemd-sysctl / sysctl --system", "evidence"),
    "55-nixos-aslr-entropy.conf": ("sharedsetting", "kernel sysctl for ASLR entropy, applied at boot", "evidence"),
    # appearance
    "hicolor-icon-theme-0.18": ("appearance", "fallback icon theme for desktop programs", "evidence"),
    "sound-theme-freedesktop-0.8": ("appearance", "event sound theme for desktop programs", "evidence"),
    "dejavu-fonts-minimal-2.37": ("appearance", "font files used by fontconfig programs", "evidence"),
    "fontconfig-conf": ("appearance", "fontconfig configuration for all fontconfig programs", "evidence"),
    "fontconfig-etc": ("appearance", "fontconfig /etc/fonts tree for all fontconfig programs", "evidence"),
    "fc-cache": ("cache", "pre-generated fontconfig font cache", "evidence"),
    "nix-wallpaper-simple-dark-gray_bootloader.png": ("gruptheme", "boot loader background picture", "evidence"),
    "simple-dark-gray-bootloader-2018-08-28": ("gruptheme", "boot loader theme picture package", "evidence"),
    # boot, firmware, devices
    "firmware": ("firmware", "firmware tree whose path is written to firmware_class.path", "raw:activation-script.txt"),
    "grub-config.xml": ("boot", "boot loader configuration read by install-grub to write grub.cfg", "evidence"),
    "udev-rules": ("single", "udev rules directory interpreted by udevd (names, permissions, RUN)", DOC_UDEV),
    "udev-path": ("prog", "symlink tree of programs that udev rules execute", DOC_UDEV),
    "console-env": ("sharedsetting", "console keymaps and fonts used by vconsole setup and kbd tools", DOC_CONSOLE),
    "binfmt_nixos.conf": ("single", "binfmt_misc registrations applied by systemd-binfmt", "evidence"),
    "nixos.conf": ("single", "modules-load.d list of kernel modules loaded by systemd-modules-load", DOC_KERNEL),
    # accounts, login, rights
    "census-authorized_keys": ("keys", "authorized SSH public keys of the user account", "evidence"),
    "sudoers": ("login", "sudo rules: who may become superuser", "evidence"),
    "sshd.conf-final": ("login", "sshd configuration: ports, password login, authentication", DOC_SSHD),
    "users-groups.json": ("accounts", "account and group definitions applied by update-users-groups.pl", "raw:account-definitions.txt"),
    "useradd": ("single", "defaults useradd applies to new accounts", "evidence"),
    "login.defs": ("sharedsetting", "shadow suite settings (id ranges, hashing) read by login, su, useradd", "evidence"),
    # single-reader settings acting beyond the program
    "nix.conf": ("single", "settings of nix and nix-daemon (users, sandbox, substituters)", "evidence"),
    "dhcpcd.conf": ("single", "dhcpcd network configuration", "evidence"),
    "logrotate.conf": ("single", "logrotate rules for rotating logs", "evidence"),
    "switch-inhibitors": ("single", "JSON values that block switching configuration when changed", DOC_SWITCH),
    "empty-inhibitors": ("single", "fallback '{}' inhibitor values read by the pre-switch check", DOC_SWITCH),
    "systemd-generator-environment.json": ("single", "environment values systemd passes to generators", "evidence"),
    "shutdown-ramfs-contents.json": ("single", "list of files make-initrd-ng puts into the shutdown ramfs", "evidence"),
    "dbus-1": ("single", "D-Bus daemon configuration: bus policy and service activation", "evidence"),
    "tmpfiles.d": ("single", "tmpfiles rules applied by systemd-tmpfiles", "evidence"),
    "nixos-tmpfiles.d": ("single", "NixOS tmpfiles rules applied by systemd-tmpfiles", "evidence"),
    "ssh-root-provision.conf": ("single", "tmpfiles rule creating /root and /root/.ssh with modes", DOC_SSHD),
    "locale.conf": ("sharedsetting", "system locale read by systemd, localed and login sessions", "evidence"),
    "vconsole.conf": ("sharedsetting", "console keymap/font settings read by vconsole-setup and localed", "evidence"),
    "inputrc": ("sharedsetting", "readline key bindings for all readline programs", "evidence"),
    "hosts": ("sharedsetting", "host name to address table used by all programs", DOC_NET),
    "issue": ("ifaceonly", "login banner text shown by agetty", "evidence"),
    "lessconfig": ("ifaceonly", "key bindings and options of the pager less", "evidence"),
    # scripts / code
    "local-cmds": ("script", "boot.postBootCommands shell code run at boot", DOC_STAGE2),
    "migrate-dhcpcd": ("script", "shell script run before dhcpcd starts (lease migration)", DOC_DHCPCD),
    "set-environment": ("shellstart", "shell code exporting system environment, sourced by shells", "evidence"),
    "firewall-start": ("script", "script that installs the firewall rules", "evidence"),
    "firewall-stop": ("script", "script that removes the firewall rules", "evidence"),
    "firewall-reload": ("script", "script that reloads the firewall rules", "evidence"),
    "install-grub.pl": ("script", "Perl program installing GRUB and writing grub.cfg", "evidence"),
    "install-grub.sh": ("script", "shell wrapper running install-grub.pl", "evidence"),
    "lib.sh": ("script", "shell library sourced by NixOS scripts", "evidence"),
    "mounts.sh": ("script", "shell script performing mounts", "evidence"),
    "setup-etc.pl": ("script", "Perl script creating /etc symlinks at activation", "evidence"),
    "update-users-groups.pl": ("script", "Perl script creating/updating accounts at activation", "evidence"),
    "pre-switch-checks": ("script", "script run before switching to a new configuration", DOC_SWITCH),
    "system-shutdown": ("script", "directory of executables systemd runs at shutdown", "evidence"),
    "system-generators": ("script", "directory of generator programs systemd runs at boot", "evidence"),
    "user-generators": ("script", "directory of generator programs the user manager runs", "evidence"),
    "bash-completion-2.17.0": ("script", "completion code sourced by interactive bash", "evidence"),
    "nix-bash-completions-0.6.8": ("script", "nix completion code sourced by interactive bash", "evidence"),
    "build-vms.nix": ("script", "Nix code evaluated by nixos-build-vms", "evidence"),
    "nixos-option.nix": ("script", "Nix code evaluated by nixos-option", "evidence"),
    # whole-system trees
    "etc": ("unitfile_tree", "the /etc tree of the system generation", "evidence"),
    "system-path": ("prog", "profile tree of all system programs (PATH)", "evidence"),
    "system-units": ("unitfile", "directory of all system unit files", "evidence"),
    "user-units": ("unitfile", "directory of all user unit files", "evidence"),
    # documentation pointer
    "nixos-manual.desktop": ("doc", "desktop menu entry opening the NixOS manual", "evidence"),
    # not established
    "systemd": ("unknown", "store path named only 'systemd'; content not in inventory", "evidence"),
    "hostname": ("unknown", "store path named only 'hostname'; content not in inventory", "evidence"),
    "getty": ("unknown", "store path named only 'getty'; content not in inventory", "evidence"),
    "multiuser.nix": ("unknown", "Nix file; no user of it established", "evidence"),
    "sandbox.nix": ("unknown", "Nix file; no user of it established", "evidence"),
    "relaxedsandbox.nix": ("unknown", "Nix file; no user of it established", "evidence"),
    "linux-headers-static-6.18.7": ("unknown", "kernel C headers for compiling; run-time user not established", "evidence"),
    "zlib-1.3.2-static": ("unknown", "static zlib library for linking; run-time user not established", "evidence"),
}

ETC_STORE = {
    "etc-bash_logout": ("shellstart", "bash logout script /etc/bash_logout"),
    "etc-bashrc": ("shellstart", "bash startup script /etc/bashrc"),
    "etc-profile": ("shellstart", "login shell startup script /etc/profile"),
    "etc-dhcpcd.exit-hook": ("script", "shell hook dhcpcd runs on network events"),
    "etc-environment.d-50-systemd-path.conf": ("single", "PATH for user services, read by the user manager"),
    "etc-fstab": ("sharedsetting", "file systems to mount, read by mount, fsck and systemd"),
    "etc-fuse.conf": ("single", "fusermount options (user_allow_other)"),
    "etc-gai.conf": ("sharedsetting", "getaddrinfo address preference for all programs"),
    "etc-host.conf": ("sharedsetting", "C library resolver options for all programs"),
    "etc-hostname": ("sharedsetting", "the system host name"),
    "etc-lsb-release": ("sharedsetting", "operating system identification read by programs"),
    "etc-os-release": ("sharedsetting", "operating system identification read by systemd and programs"),
    "etc-lvm-lvm.conf": ("single", "settings of the LVM tools"),
    "etc-man_db.conf": ("ifaceonly", "search paths and options of man"),
    "etc-nanorc": ("ifaceonly", "settings of the nano editor"),
    "etc-netgroup": ("netgroup", "netgroup database, empty by default"),
    "etc-nix-registry.json": ("single", "flake registry of nix (what 'nixpkgs' refers to)"),
    "etc-nscd.conf": ("single", "settings of the name service cache daemon"),
    "etc-nsswitch.conf": ("sharedsetting", "name service sources for users, hosts, groups"),
    "etc-pam-environment": ("sharedsetting", "environment set by pam_env for all login sessions"),
    "etc-resolvconf.conf": ("single", "openresolv settings generating /etc/resolv.conf"),
    "etc-shells": ("sharedsetting", "list of valid login shells used by chsh, login, sshd"),
    "etc-ssh-ssh_config": ("single", "settings of the ssh client"),
    "etc-ssh-ssh_known_hosts": ("single", "host keys the ssh client trusts"),
    "etc-sysctl.d-60-nixos.conf": ("sharedsetting", "kernel sysctl values applied at boot"),
    "etc-systemd-coredump.conf": ("single", "settings of systemd-coredump"),
    "etc-systemd-journald.conf": ("single", "settings of systemd-journald (storage, limits)"),
    "etc-systemd-logind.conf": ("single", "settings of systemd-logind (power keys, sessions)"),
    "etc-systemd-oomd.conf": ("single", "settings of systemd-oomd (killing processes on memory pressure)"),
    "etc-systemd-sleep.conf": ("single", "settings of systemd-sleep (suspend, hibernate)"),
    "etc-systemd-system.conf": ("single", "settings of the systemd system manager (PID 1)"),
    "etc-systemd-system-preset-00-nixos.preset": ("single", "systemctl preset policy for system units"),
    "etc-systemd-timesyncd.conf": ("single", "settings of systemd-timesyncd (time servers)"),
    "etc-systemd-user.conf": ("single", "settings of the systemd user manager"),
    "etc-systemd-user-preset-00-nixos.preset": ("single", "systemctl preset policy for user units"),
}


def store_decide(name):
    """Return (rule_key, what, basis) for a system-closure store object."""
    short = re.sub(r"^/nix/store/[a-z0-9]{32}-", "", name)
    if short in STORE_EXPLICIT:
        return STORE_EXPLICIT[short]
    if short in ETC_STORE:
        key, what = ETC_STORE[short]
        basis = DOC_NET if key == "netgroup" else "evidence"
        return key, what, basis
    if short.startswith("etc-modprobe.d-"):
        return "sharedsetting", "modprobe options/blacklists read by kmod tools and udev", "evidence"
    if short.startswith("fc-") and short.endswith(".conf"):
        return "appearance", "fontconfig rule file for all fontconfig programs", "evidence"
    if short.startswith("X-Restart-Triggers-"):
        return "xrt", "restart-trigger strings; only its path is compared in the unit file", DOC_XRT
    if short.endswith(".pam"):
        return "login", "PAM rules for " + short[:-4] + " (authentication, account, session)", "evidence"
    if short.startswith("unit-script-"):
        return "script", "shell script a systemd unit runs: " + short[len("unit-script-"):], "evidence"
    if short.startswith("unit-"):
        return "unitfile", "systemd unit file " + short[len("unit-"):], "evidence"
    if re.search(r"-(man|doc|info)$", short) or short.startswith("nix-manual-") or short in (
            "nixos-manual-html", "nixos-configuration-reference-manpage"):
        return "doc", "documentation (man/info/HTML pages) of " + re.sub(r"-(man|doc|info)$", "", short), "evidence"
    if short.startswith("nixos-system-"):
        return "prog", "top-level system generation: kernel, init, activation, all programs", "raw:current-system.txt"
    return "prog", "program or library package " + short, "evidence"


def stored_decide(name):
    T = STORED.get(name)
    if T is None:
        raise KeyError(name)
    return T


# stored objects outside the store: (rule key or explicit tuple, what, basis)
STORED = {
    "/boot/background.png": ("gruptheme", "boot loader background picture", "evidence"),
    "/boot/converted-font.pf2": ("gruptheme", "font of the GRUB menu", "evidence"),
    "/boot/grub": ("boot", "GRUB modules, grub.cfg boot menu, fonts, environment block", "raw:files.tsv"),
    "/etc/.clean": (("NOT", "S2.2-2", "List setup-etc uses to delete stale copied /etc files at the next activation; removal stops nothing now and makes nothing impossible."),
                    "list of /etc files copied by the activation script", "evidence"),
    "/etc/.updated": (("NOT", "S2.2-2,S2.2-5", "Timestamp for ConditionNeedsUpdate; removal only makes update units (catalog, hwdb) run again, then the computer does the same."),
                      "stamp checked by units with ConditionNeedsUpdate", "evidence"),
    "/var/.updated": (("NOT", "S2.2-2,S2.2-5", "Timestamp for ConditionNeedsUpdate; removal only makes update units (catalog, hwdb) run again, then the computer does the same."),
                      "stamp checked by units with ConditionNeedsUpdate", "evidence"),
    "/etc/NIXOS": (("MUST", "S2.2-2", "Marker the NixOS switch and boot code check for a NixOS root; removal makes switching configuration impossible."),
                   "marker file identifying a NixOS root file system", "evidence"),
    "/etc/bash_logout": ("shellstart", "bash logout script", "evidence"),
    "/etc/bashrc": ("shellstart", "bash startup script", "evidence"),
    "/etc/profile": ("shellstart", "login shell startup script", "evidence"),
    "/etc/binfmt.d": ("single", "binfmt_misc registrations applied by systemd-binfmt", "evidence"),
    "/etc/dbus-1": ("single", "D-Bus daemon configuration: bus policy and service activation", "evidence"),
    "/etc/default": ("single", "useradd defaults for new accounts", "evidence"),
    "/etc/dhcpcd.exit-hook": ("script", "shell hook dhcpcd runs on network events", "evidence"),
    "/etc/environment.d": ("single", "PATH for user services, read by the user manager", "evidence"),
    "/etc/fonts": ("appearance", "fontconfig configuration for all fontconfig programs", "evidence"),
    "/etc/fstab": ("sharedsetting", "file systems to mount, read by mount, fsck and systemd", "evidence"),
    "/etc/fuse.conf": ("single", "fusermount options (user_allow_other)", "evidence"),
    "/etc/gai.conf": ("sharedsetting", "getaddrinfo address preference for all programs", "evidence"),
    "/etc/group": ("accounts", "group database: groups and members", "evidence"),
    "/etc/passwd": ("accounts", "account database: names, ids, homes, shells", "evidence"),
    "/etc/shadow": (("MUST", "S2.2-15,S2.2-2", "Holds account lock and expiry fields besides hashes (hashes alone need not be, S2.2-15); removal makes password login and su impossible."),
                    "password hashes plus account lock and expiry fields", "evidence"),
    "/etc/subgid": ("sharedsetting", "subordinate group id ranges for user namespaces", "evidence"),
    "/etc/subuid": ("sharedsetting", "subordinate user id ranges for user namespaces", "evidence"),
    "/etc/host.conf": ("sharedsetting", "C library resolver options for all programs", "evidence"),
    "/etc/hostname": ("sharedsetting", "the system host name", "evidence"),
    "/etc/hosts": ("sharedsetting", "host name to address table used by all programs", "evidence"),
    "/etc/inputrc": ("sharedsetting", "readline key bindings for all readline programs", "evidence"),
    "/etc/issue": ("ifaceonly", "login banner text shown by agetty", "evidence"),
    "/etc/kbd": ("sharedsetting", "console keymaps and fonts used by kbd tools and vconsole setup", "evidence"),
    "/etc/locale.conf": ("sharedsetting", "system locale read by systemd, localed and sessions", "evidence"),
    "/etc/login.defs": ("sharedsetting", "shadow suite settings read by login, su, useradd, passwd", "evidence"),
    "/etc/lsb-release": ("sharedsetting", "operating system identification read by programs", "evidence"),
    "/etc/os-release": ("sharedsetting", "operating system identification read by systemd and programs", "raw:os-release"),
    "/etc/lvm": ("single", "settings of the LVM tools", "evidence"),
    "/etc/machine-id": (("NOT", "S2.2-2", "Machine identifier; if removed systemd generates a new one at boot and the computer does the same, so the removal test is negative."),
                        "unique machine identifier used by systemd, journald, D-Bus", "evidence"),
    "/etc/man_db.conf": ("ifaceonly", "search paths and options of man", "evidence"),
    "/etc/modprobe.d": ("sharedsetting", "modprobe options/blacklists read by kmod tools and udev", "evidence"),
    "/etc/modules-load.d": ("single", "kernel modules systemd-modules-load loads at boot", DOC_KERNEL),
    "/etc/mtab": ("unknown", "symlink to /proc/mounts for programs reading the legacy mount table", "evidence"),
    "/etc/nanorc": ("ifaceonly", "settings of the nano editor", "evidence"),
    "/etc/netgroup": ("netgroup", "netgroup database, empty by default", DOC_NET),
    "/etc/nix": ("single", "nix.conf and flake registry read by nix and nix-daemon", "evidence"),
    "/etc/nixos": (("HOLE", "S2.2-2,S2.2-10", "The system's own configuration (Nix code); removal makes rebuilding impossible (S2.2-2), but the text does not say whether the declaration itself must be recorded in it."),
                   "configuration.nix and hardware-configuration.nix, the NixOS configuration", "raw:nixos-configuration/configuration.nix"),
    "/etc/nscd.conf": ("single", "settings of the name service cache daemon", "evidence"),
    "/etc/nsswitch.conf": ("sharedsetting", "name service sources for users, hosts, groups", "evidence"),
    "/etc/pam": ("sharedsetting", "environment pam_env sets for all login sessions", "evidence"),
    "/etc/pam.d": ("login", "PAM rules of login, su, sudo, sshd, passwd and others", "evidence"),
    "/etc/pki": ("shareddata", "CA certificate bundle used for TLS by many programs", "evidence"),
    "/etc/ssl": ("shareddata", "CA certificate bundles used for TLS by many programs", "evidence"),
    "/etc/protocols": ("shareddata", "protocol number database used by all programs", "evidence"),
    "/etc/rpc": ("shareddata", "RPC program number database used by the C library", "evidence"),
    "/etc/services": ("shareddata", "service name to port database used by all programs", "evidence"),
    "/etc/resolv.conf": ("sharedsetting", "DNS servers for all programs, written by resolvconf", "evidence"),
    "/etc/resolv.conf.bak": (("NOT", "S2.2-2", "Backup copy no program reads; removal stops nothing and makes nothing impossible."),
                             "backup copy of resolv.conf", "evidence"),
    "/etc/resolvconf.conf": ("single", "openresolv settings generating /etc/resolv.conf", "evidence"),
    "/etc/set-environment": ("shellstart", "shell code exporting system environment, sourced by shells", "evidence"),
    "/etc/shells": ("sharedsetting", "list of valid login shells used by chsh, login, sshd", "evidence"),
    "/etc/ssh": (("MUST", "S2.2-15,S2.2-2", "Holds the user's login keys and sshd_config (ports, password login), which S2.2-15 requires; removing the directory makes SSH login impossible."),
                 "authorized keys, host keys, sshd_config, ssh_config, known hosts, moduli", "raw:files.tsv"),
    "/etc/static": (("MUST", "S2.2-2", "Every /etc link resolves through it; removal breaks all /etc settings, PAM, units and scripts listed elsewhere."),
                    "symlink to the /etc tree of the current generation", "evidence"),
    "/etc/sudoers": ("login", "sudo rules: who may become superuser", "evidence"),
    "/etc/sysctl.d": ("sharedsetting", "kernel sysctl values applied at boot", "evidence"),
    "/etc/systemd": (("MUST", "S2.2-1,S2.2-2", "Contains the system unit directory and generator programs; removal makes services impossible to start (daemon .conf files inside are a separate HOLE case)."),
                     "system/user unit links, generators, daemon .conf files, presets", "raw:files.tsv"),
    "/etc/terminfo": ("shareddata", "terminal descriptions used by all terminal programs", "evidence"),
    "/etc/tmpfiles.d": ("single", "tmpfiles rules applied by systemd-tmpfiles", "evidence"),
    "/etc/udev": (("MUST", "S2.2-1,S2.2-2", "Contains hwdb.bin, read by udev and libudev users, so removal changes device handling; the rules directory inside alone would be the S2.2-7 HOLE."),
                  "udev hardware database and rules directory", "evidence"),
    "/etc/vconsole.conf": ("sharedsetting", "console keymap/font settings read by vconsole-setup and localed", "evidence"),
    "/etc/zoneinfo": ("shareddata", "time zone database read by the C library and programs", "evidence"),
    "/home/census/.local/state/nix": (("MUST", "S2.2-9,S2.2-2", "The user's Nix profile links that make the installed program (hello) runnable; removal makes it impossible to start from the profile."),
                                      "user Nix profile generation links", "raw:user-profile.txt"),
    "/home/census/.nix-profile": (("MUST", "S2.2-9,S2.2-2", "Link on the user's PATH to the profile with the installed program (hello); removal makes it impossible to start that way."),
                                  "link to the user's Nix profile", "raw:user-profile.txt"),
    "/home/census/.nix-defexpr": ("single", "channel links nix-env of the user evaluates", "evidence"),
    "/root/.nix-defexpr": ("single", "channel links nix-env of root evaluates", "evidence"),
    "/root/.nix-channels": ("single", "channel URLs nix-channel of root downloads", "evidence"),
    "/root/.nix-profile": (("NOT", "S2.2-2", "Points to a root profile that does not exist (root-profile.txt empty); removal stops nothing and makes nothing impossible."),
                           "dangling link to the root user's Nix profile", "raw:root-profile.txt"),
    "/home/census/.vimrc": (("NOT", "S2.2-10,S2.2-2", "Vim configuration code, but no vim is installed (not in system closure or user profile), so no program runs it; removal changes nothing."),
                            "vim editor configuration file of the user", "raw:system-closure.txt"),
    "/home/census/Documents": ("content", "user's documents directory with a markdown note", "evidence"),
    "/nix/var/log/nix": ("logs", "compressed build logs of Nix derivations", "evidence"),
    "/nix/var/nix": (("NOT", "S2.2-2", "Lock file Nix creates on demand for garbage collection; removal stops nothing and makes nothing impossible."),
                     "gc.lock lock file of Nix", "evidence"),
    "/nix/var/nix/daemon-socket": (("MUST", "S2.2-2", "Listening socket of nix-daemon; removal makes Nix operations of non-root users impossible."),
                                   "nix-daemon listening socket", "evidence"),
    "/nix/var/nix/db": (("HOLE", "S2.2-4,S2.2-2", "S2.2-4 exempts database contents, but removing the Nix store database makes package operations impossible (S2.2-2); no sentence says which prevails."),
                        "Nix database of valid store paths and references", "evidence"),
    "/nix/var/nix/gcroots": (("MUST", "S2.2-2", "Garbage-collector roots incl. the user profile and current system; removal lets garbage collection delete programs in use, which then stop."),
                             "Nix garbage-collector roots", "raw:files.tsv"),
    "/nix/var/nix/profiles": (("MUST", "S2.2-2,S2.2-16", "System profile links that boot entries and garbage-collector roots use; removal makes booting the generation and rebuilding impossible."),
                              "system and channel profile generation links", "raw:nix-profiles.tsv"),
    "/nix/var/nix/userpool": (("NOT", "S2.2-2", "Lock file for an automatically allocated build user id, created by Nix on demand; removal stops nothing."),
                              "lock file of Nix build user id allocation", "evidence"),
    "/root/.cache/nix": ("cache", "Nix binary cache metadata cache of root", "evidence"),
    "/var/lib/dhcpcd": (("NOT", "S2.2-2", "DHCP client id and lease; dhcpcd regenerates them and obtains a lease again, so the computer does the same."),
                        "dhcpcd DUID and current lease", "evidence"),
    "/var/lib/lastlog": ("logs", "lastlog2 database of last logins", "evidence"),
    "/var/lib/nixos": (("MUST", "S2.2-15,S2.2-2", "Keeps the uid/gid each declared account received; removal lets the next activation renumber accounts (S2.2-15), breaking ownership of their files."),
                       "uid/gid maps and lists of declared users and groups", "evidence"),
    "/var/lib/systemd": (("NOT", "S2.2-2,S2.2-5", "Program state (seed, clock, timer stamps, catalog, linger flag) regenerated by its programs; after removal the computer does the same."),
                         "systemd state: random seed, clock, timer stamps, catalog, linger", "raw:files.tsv"),
    "/var/lock": ("unknown", "symlink /var/lock -> /run/lock for legacy lock files", "evidence"),
    "/var/run": (("MUST", "S2.2-2", "Legacy path many programs use for sockets and pid files (e.g. D-Bus default system bus address); removal breaks those programs."),
                 "symlink /var/run -> /run", "evidence"),
    "/var/log/btmp": ("logs", "record of failed login attempts", "evidence"),
    "/var/log/wtmp": ("logs", "record of logins and reboots", "evidence"),
    "/var/log/journal": ("logs", "persistent systemd journal files", "evidence"),
    "/var/log/lastlog.migrated": ("logs", "marker that old lastlog records were imported", "evidence"),
}

NETGROUP = ("NOT", "S2.2-2", "Empty by default in NixOS (netgroup.text = \"\"); removing an empty database changes no lookup, so nothing stops.")

OTHER = {
    "nixos-8a2cb02577": (R["accounts"], "32 Nix build accounts nixbld1..32 used by nix-daemon", "raw:nix-builder-accounts.txt"),
    "nixos-bfd49e603a": (("MIXED", "S2.2-9,S2.2-5,S2.2-2",
                          "MUST: user profile programs (hello) and the root channel nixpkgs; NOT: .drv files, sources, build-time outputs, re-fetched or rebuilt on demand (S2.2-5)."),
                         "store paths outside the system closure: derivations, sources, profiles, channel",
                         "raw:store-outside-system-closure.txt"),
    "nixos-d2fde56a38": (R["process"][:2] + ("A program installed in the user's profile (hello, its environment and manifest); S2.2-9 requires a program in the home directory profile.",),
                         "user Nix profile: program hello, user-environment, manifest", "raw:user-closure-outside-system.txt"),
    "nixos-64f62c6553": (("MUST", "S2.2-2",
                          "Includes /var/empty, the privilege separation directory sshd requires; removal makes SSH login impossible. Other members are empty or parent directories."),
                         "26 bare directories (/var/empty, /srv, /var/tmp, parents)", "raw:directory-only-groups.json"),
    "nixos-a3f2270221": (("HOLE", "S2.2-1,S2.2-2",
                          "Device units exist only as systemd's reflection of kernel devices; no object can be removed apart from the hardware, and the text gives no rule for such derived objects."),
                         "systemd device units generated from kernel devices", "evidence"),
    "nixos-88335c6c87": (("HOLE", "S2.2-1,S2.2-2",
                          "Device units exist only as systemd's reflection of kernel devices; no object can be removed apart from the hardware, and the text gives no rule for such derived objects."),
                         "user manager view of device units generated from kernel devices", "evidence"),
    "nixos-18fb2985ed": (("MUST", "S2.2-2",
                          "Mounted file systems (/, /nix/store, /run/keys, user runtime dir); unmounting them stops the system or makes programs impossible to run."),
                         "mount units for /, /nix/store, /run/keys, /run/user/1000", "evidence"),
    "nixos-565df89b5f": (("MUST", "S2.2-2",
                          "Mounted file systems (/, /nix/store, credentials, kernel file systems); unmounting them stops programs or makes things impossible."),
                         "user manager view of system mount units", "evidence"),
    "nixos-9994d7ebc4": (("NOT", "S2.2-2",
                          "Units named in dependencies but with no unit file; there is nothing to remove, and nothing stops or becomes impossible."),
                         "unit names referenced by other units, no unit file exists", "evidence"),
    "nixos-97fdaec6aa": (("NOT", "S2.2-2",
                          "Unit name referenced by dependencies but with no unit file; there is nothing to remove, and nothing stops or becomes impossible."),
                         "unit name referenced by a dependency, no unit file exists", "evidence"),
    "nixos-0ff15b2741": (("MUST", "S2.2-2,S2.2-9",
                          "Scopes holding PID 1 and the running login session; removing them stops the init system or the session's programs."),
                         "init.scope (PID 1) and session-5.scope (login session)", "evidence"),
    "nixos-3bc8c8458c": (("MUST", "S2.2-2,S2.2-9",
                          "Scope holding the running user manager process; removal stops it and the user services."),
                         "init.scope of the user manager", "evidence"),
    "nixos-253d752b01": (("MUST", "S2.2-2",
                          "Slices (cgroups) containing running getty, modprobe and user services; removal stops the programs inside them."),
                         "slices for getty, modprobe and user 1000 services", "evidence"),
    "nixos-b855166ba5": (("MUST", "S2.2-2",
                          "Root slice of the user manager containing all user services; removal stops them."),
                         "root slice of the user manager", "evidence"),
    "nixos-eb57ff0e5c": (("MUST", "S2.2-2,S2.2-15",
                          "Socket systemd's ssh generator creates for local SSH login; removal makes that login path impossible."),
                         "AF_UNIX socket offering local SSH login (systemd-ssh-generator)", "evidence"),
    "nixos-89ce5c5668": (("MUST", "S2.2-9,S2.2-2",
                          "Threads of the running kernel, a program running on the computer (S2.2-9); without them the computer does nothing."),
                         "kernel worker threads of the running Linux kernel", "evidence"),
    "nixos-d8ee8908a9": (("MUST", "S2.2-9",
                          "A program that ran on the computer when observed (ps of procps); S2.2-9 requires a running program regardless of origin."),
                         "ps process running at inventory time", "evidence"),
}


def clip(s, n):
    w = s.split()
    return " ".join(w[:n])


def decide(row):
    rid, kind, name = row["id"], row["kind"], row["name"]
    if rid in OTHER:
        (dec, sen, why), what, basis = OTHER[rid]
        return dec, sen, what, basis, why
    if kind == "system-closure-store-object":
        key, what, basis = store_decide(name)
        if key == "netgroup":
            dec, sen, why = NETGROUP
        elif key == "unitfile_tree":
            dec, sen, why = ("MUST", "S2.2-1,S2.2-2,S2.2-15",
                             "Holds PAM, sudoers, accounts, unit links and shared settings; removal makes login, services and name lookup impossible.")
        else:
            dec, sen, why = R[key]
        return dec, sen, what, basis, why
    if kind == "stored":
        v, what, basis = stored_decide(name)
        if v == "netgroup":
            dec, sen, why = NETGROUP
        elif isinstance(v, tuple):
            dec, sen, why = v
        else:
            dec, sen, why = R[v]
        return dec, sen, what, basis, why
    if kind in ("system-unit", "user-unit"):
        desc = row["evidence"].split(": ", 1)[1].split(";")[0]
        what = "unit " + name + ": " + " ".join(desc.split()[4:])
        dec, sen, why = R["unitfile"]
        return dec, sen, what, "evidence", why
    if kind == "kernel-module":
        dec, sen, why = R["kmod"]
        return dec, sen, "kernel module " + name + " loaded in the running kernel", "raw:modules.txt", why
    if kind == "process":
        dec, sen, why = R["process"]
        prog = name.rsplit("/", 1)[-1]
        return dec, sen, "running process of " + prog, "raw:processes.txt", why
    if kind == "account":
        dec, sen, why = R["accounts"]
        return dec, sen, "account " + name + " (" + row["evidence"].split(": ", 1)[1].split(" home")[0] + ")", "raw:accounts.txt", why
    raise KeyError((rid, kind, name))


def main():
    inp, out = sys.argv[1], sys.argv[2]
    rows = list(csv.DictReader(open(inp, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE))
    done = set()
    if os.path.exists(out):
        for line in open(out, encoding="utf-8").read().splitlines()[1:]:
            if line.strip():
                done.add(line.split("\t", 1)[0])
    new = not os.path.exists(out)
    with open(out, "a", encoding="utf-8") as fh:
        if new:
            fh.write("id\tdecision\tsentences\twhat_it_does\tbasis\treason\n")
        for row in rows:
            if row["id"] in done:
                continue
            dec, sen, what, basis, why = decide(row)
            what = clip(what, 15)
            why = clip(why, 30)
            fields = [row["id"], dec, sen, what, basis, why]
            assert all("\t" not in f and "\n" not in f for f in fields), fields
            fh.write("\t".join(fields) + "\n")
            fh.flush()


if __name__ == "__main__":
    main()

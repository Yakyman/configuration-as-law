# Part 5: stored-object classification notes

Scope: 150 rows selected by machine column ubuntu and kind stored or stored-directory-skeleton. No other classifications were read. Only supplied inventory rows and public documentation were used. No objects were removed.

The input uses members=1 even when evidence reports n>1. The evidence count is treated as an internal group count; partial samples never establish the omitted members. No raw machine files are available for this subset.

## Governing sentences

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- **S3-2** If what the object does remains unknown, the case yields ?.

## Scripted rules and manual checks

Rule U applies S3-1 and S3-2 only when the inventory explicitly reports more stored members than it identifies. It does not infer that a directory is homogeneous from sample names. Unknown member functions prevent a complete group decision, irrespective of familiar sampled files. Public documentation cannot recover this machine-specific membership.

Ten manually checked rows follow. Each has fewer named samples than its stated count.

| ID | Reported count | Named samples |
|---|---:|---:|
| ubuntu-5bf2e2415a | 12 | 4 |
| ubuntu-76634f69cd | 580 | 4 |
| ubuntu-809cb439ce | 110 | 4 |
| ubuntu-384e8d981f | 10 | 4 |
| ubuntu-2a3c514663 | 9 | 4 |
| ubuntu-228a030233 | 7 | 4 |
| ubuntu-966a04ec60 | 2 | 1 |
| ubuntu-4d882498fa | 5 | 4 |
| ubuntu-2dfb100dfa | 2 | 1 |
| ubuntu-5ecd8ad6ee | 8 | 4 |

Rule L applies S2.2-6 to fully enumerated log/history storage. It excludes configuration, control markers and incomplete journal groups. Ten manual checks identify the kind of past activity; all are records, not commands.

| ID | Manual finding |
|---|---|
| ubuntu-5ce874f910 | Alternatives log |
| ubuntu-c4c1593248 | Crash-report log |
| ubuntu-83df02e6eb | Three enumerated package logs |
| ubuntu-3f3dc85096 | Authentication log |
| ubuntu-9c96b64591 | Failed-login history |
| ubuntu-93b020b2d3 | Cloud initialization output log |
| ubuntu-2954505d9d | Cloud initialization log |
| ubuntu-293699acd1 | Kernel message record |
| ubuntu-626ab0ebaf | Previous kernel message record |
| ubuntu-6f5cf081f0 | Package operation log |

All other rows were considered individually; explicit calls in part-5.1.build.py preserve those decisions. Its initial provisional entries were corrected before completion as recorded below. The output TSV is authoritative.

## Functional checks and corrections

The protected account files require their membership and login restrictions to be recorded; password values remain exempt. Declaration representation and secret protection are design matters, so their combined storage is not a HOLE. The manual-database auto-update flag controls whether rebuilding happens: despite being a cached value, it fails the functional cache exemption. The distribution-origin link selects package-build behavior, not only provenance content. These corrections changed rows ubuntu-7740cdd4af, ubuntu-2adfd50853, ubuntu-cfe66bc678, ubuntu-6ead5eb670.

Remaining HOLE rows concern explicit substantive overlaps: historical records also used to control future behavior, and the unspecified scope of settings inside one daemon. They do not concern storage layout, secret protection, or the design treatment of accumulated state.

UNKNOWN singleton cases are not classified from suggestive names. Searches for the image-version file, overlay-root local configuration, legal-display marker and snap section cache did not establish the actual contents and consumers on this machine. Secondary discussion of the legal marker was found, but no version-matched primary package source was established; its effect remains unconfirmed. PackageKit documentation shows proxy persistence as well as transaction history, so its missing database contents matter.

## Documentation excerpts

Short quotations below identify the documented functions. The TSV records the applied functional inference. Source-specific quotations remain below 25 words each.

- [https://manpages.debian.org/unstable/linux-base/linux-update-symlinks.1.en.html](https://manpages.debian.org/unstable/linux-base/linux-update-symlinks.1.en.html): “maintain symlinks to default kernel and initramfs”
- [https://kernel.org/doc/html/next/driver-api/early-userspace/early_userspace_support.html](https://kernel.org/doc/html/next/driver-api/early-userspace/early_userspace_support.html): “Early userspace support”
- [https://man7.org/linux/man-pages/man3/lckpwdf.3.html](https://man7.org/linux/man-pages/man3/lckpwdf.3.html): “The lckpwdf() function is intended to protect against multiple simultaneous accesses of the shadow password database.”
- [https://manpages.ubuntu.com/manpages/noble/man8/systemd-update-done.8.html](https://manpages.ubuntu.com/manpages/noble/man8/systemd-update-done.8.html): “Mark /etc/ and /var/ fully updated”
- [https://manpages.ubuntu.com/manpages/noble/man8/update-ca-certificates.8.html](https://manpages.ubuntu.com/manpages/noble/man8/update-ca-certificates.8.html): “update /etc/ssl/certs and ca-certificates.crt”
- [https://manpages.debian.org/testing/dpkg-dev/deb-origin.5.en.html](https://manpages.debian.org/testing/dpkg-dev/deb-origin.5.en.html): “These files are usually used both to determine the behavior of tools and resulting contents during package builds targeting a specific vendor”
- [https://man7.org/linux/man-pages/man5/crypttab.5.html](https://man7.org/linux/man-pages/man5/crypttab.5.html): “Configuration for encrypted block devices”
- [https://man7.org/linux/man-pages/man5/pam_env.conf.5.html](https://man7.org/linux/man-pages/man5/pam_env.conf.5.html): “pam_env.conf, environment - the environment variables config files”
- [https://man7.org/linux/man-pages/man5/fstab.5.html](https://man7.org/linux/man-pages/man5/fstab.5.html): “The file fstab contains descriptive information about the filesystems the system can mount.”
- [https://man7.org/linux/man-pages/man5/gshadow.5.html](https://man7.org/linux/man-pages/man5/gshadow.5.html): “Administrators can change the password or the members of the group.”
- [https://man7.org/linux/man-pages/man5/hostname.5.html](https://man7.org/linux/man-pages/man5/hostname.5.html): “The /etc/hostname file configures the name of the local system.”
- [https://man7.org/linux/man-pages/man5/hosts.5.html](https://man7.org/linux/man-pages/man5/hosts.5.html): “This file is a simple text file that associates IP addresses with hostnames”
- [https://manpages.ubuntu.com/manpages/noble/man5/hosts_access.5.html](https://manpages.ubuntu.com/manpages/noble/man5/hosts_access.5.html): “format of host access control files”
- [https://manpages.ubuntu.com/manpages/focal/man5/initramfs.conf.5.html](https://manpages.ubuntu.com/manpages/focal/man5/initramfs.conf.5.html): “Modules listed in /etc/initramfs-tools/modules and /usr/share/initramfs-tools/modules.d/* are always included in the initramfs, and are loaded early in the boot process.”
- [https://www.gnu.org/software/bash/manual/html_node/Readline-Init-File.html](https://www.gnu.org/software/bash/manual/html_node/Readline-Init-File.html): “When a program that uses the Readline library starts up, Readline reads the init file and sets any variables and key bindings it contains.”
- [https://github.com/open-iscsi/open-iscsi](https://github.com/open-iscsi/open-iscsi): “read initiatorname from file”
- [https://man7.org/linux/man-pages/man8/ldconfig.8.html](https://man7.org/linux/man-pages/man8/ldconfig.8.html): “The cache is used by the run-time linker, ld.so or ld-linux.so.”
- [https://man7.org/linux/man-pages/man5/locale.conf.5.html](https://man7.org/linux/man-pages/man5/locale.conf.5.html): “The /etc/locale.conf file configures system-wide locale settings.”
- [https://manpages.ubuntu.com/manpages/noble/man5/locale.gen.5.html](https://manpages.ubuntu.com/manpages/noble/man5/locale.gen.5.html): “Configuration file for locale-gen”
- [https://man7.org/linux/man-pages/man5/localtime.5.html](https://man7.org/linux/man-pages/man5/localtime.5.html): “Local timezone configuration file”
- [https://man7.org/linux/man-pages/man5/machine-id.5.html](https://man7.org/linux/man-pages/man5/machine-id.5.html): “Local machine ID configuration file”
- [https://manpages.ubuntu.com/manpages/noble/man5/mdadm.conf.5.html](https://manpages.ubuntu.com/manpages/noble/man5/mdadm.conf.5.html): “configuration for management of Software RAID with mdadm”
- [https://manpages.debian.org/bookworm/kmod/modules.5.en.html](https://manpages.debian.org/bookworm/kmod/modules.5.en.html): “/etc/modules - kernel modules to load at boot time”
- [https://netplan.readthedocs.io/en/stable/netplan-tutorial/](https://netplan.readthedocs.io/en/stable/netplan-tutorial/): “Netplan configuration is stored in YAML-formatted files in the /etc/netplan directory.”
- [https://manpages.ubuntu.com/manpages/jammy/man5/networks.5.html](https://manpages.ubuntu.com/manpages/jammy/man5/networks.5.html): “network name information”
- [https://man7.org/linux/man-pages/man5/nsswitch.conf.5.html](https://man7.org/linux/man-pages/man5/nsswitch.conf.5.html): “used by the GNU C Library and certain other applications to determine the sources from which to obtain name-service information”
- [https://www.gnu.org/software/bash/manual/bash.html](https://www.gnu.org/software/bash/manual/bash.html): “it first reads and executes commands from the file /etc/profile, if that file exists.”
- [https://man7.org/linux/man-pages/man5/resolv.conf.5.html](https://man7.org/linux/man-pages/man5/resolv.conf.5.html): “The resolver is a set of routines in the C library that provide access to the Internet Domain Name System (DNS).”
- [https://manpages.ubuntu.com/manpages/jammy/man8/pam_pwhistory.8.html](https://manpages.ubuntu.com/manpages/jammy/man8/pam_pwhistory.8.html): “This module saves the last passwords for each user in order to force password change history”
- [https://man7.org/linux/man-pages/man5/shadow.5.html](https://man7.org/linux/man-pages/man5/shadow.5.html): “Account expiration prevents the user from logging in”
- [https://man7.org/linux/man-pages/man5/shells.5.html](https://man7.org/linux/man-pages/man5/shells.5.html): “This file is consulted by chsh(1) and available to be queried by other programs.”
- [https://man7.org/linux/man-pages/man5/subgid.5.html](https://man7.org/linux/man-pages/man5/subgid.5.html): “Subgid authorizes a group id to map ranges of group ids from its namespace into child namespaces.”
- [https://man7.org/linux/man-pages/man5/subuid.5.html](https://man7.org/linux/man-pages/man5/subuid.5.html): “Subuid authorizes a user id to map ranges of user ids from its namespace into child namespaces.”
- [https://man7.org/linux/man-pages/man5/sysctl.d.5.html](https://man7.org/linux/man-pages/man5/sysctl.d.5.html): “Configure kernel parameters at boot”
- [https://man7.org/linux/man-pages/man5/tmpfiles.d.5.html](https://man7.org/linux/man-pages/man5/tmpfiles.d.5.html): “Configuration for creation, deletion, and cleaning of files and directories”
- [https://manpages.ubuntu.com/manpages/noble/man8/update-motd.8.html](https://manpages.ubuntu.com/manpages/noble/man8/update-motd.8.html): “immediately update the dynamic MOTD and print it to stdout”
- [https://man7.org/linux/man-pages/man5/vconsole.conf.5.html](https://man7.org/linux/man-pages/man5/vconsole.conf.5.html): “Configuration file for the virtual console”
- [https://manpages.ubuntu.com/manpages/noble/man8/setvtrgb.8.html](https://manpages.ubuntu.com/manpages/noble/man8/setvtrgb.8.html): “set the virtual terminal RGB colors”
- [https://www.nano-editor.org/dist/latest/nanorc.5.html](https://www.nano-editor.org/dist/latest/nanorc.5.html): “The nanorc files contain the default settings for nano, a small and friendly text editor.”
- [https://www.sudo.ws/docs/man/1.9.14/sudoers.man.pdf](https://www.sudo.ws/docs/man/1.9.14/sudoers.man.pdf): “created the first time a user that is a member of the sudo or admin groups runs sudo.”
- [https://manpages.ubuntu.com/manpages/noble/man8/ldconfig.8.html](https://manpages.ubuntu.com/manpages/noble/man8/ldconfig.8.html): “Ignore auxiliary cache file.”
- [https://github.com/PackageKit/PackageKit/issues/392](https://github.com/PackageKit/PackageKit/issues/392): “PackageKit doesn't reset proxy setting when global proxy gets disabled”
- [https://sources.debian.org/src/man-db/2.11.2-2/debian/postinst/](https://sources.debian.org/src/man-db/2.11.2-2/debian/postinst/): “Not building database; man-db/auto-update is not 'true'.”
- [https://manpages.ubuntu.com/manpages/jammy/man8/update-shells.8.html](https://manpages.ubuntu.com/manpages/jammy/man8/update-shells.8.html): “To track changes made by the administrator, it consults a state file in /var/lib/shells.state .”

## Verification

Exactly 150 assigned IDs, one occurrence each, with no extras or omissions. All decisions are valid; word limits and single-line fields pass.

MUST: 54

NOT: 37

HOLE: 5

UNKNOWN: 54

MIXED: 0


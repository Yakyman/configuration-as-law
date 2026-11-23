# Part 1 classification notes

This is the combined c1 record for all 1,222 input rows. Only the designated text, sentence list, this part input/raw inventory and public program documentation were used. No removal test was performed.

The main TSV was appended as decisions completed. Independently completed subsets were merged without dropping earlier rows. The input members field sometimes says 1 where evidence enumerates multiple objects; the explicit raw member list was examined in those cases. Exact heterogeneous partitions are in part-1.root.members.tsv and part-1.owned.members.tsv. The latter uses member ordinals into the raw inventory intersection documented below.


---

# Part 1: account, module, process and stored-object notes

Only COMMON.md, TEXT.md, SENTENCES.md, part-1 input, its raw inventory, and public program documentation were consulted. No objects were removed. Inventory class labels were disregarded.

## Exact controlling sentences

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-3** The following need not be recorded:
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-8** Consequences of this rule that we fix explicitly:
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-11** Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.
- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-14** a saved Wi-Fi network must be recorded; the network password need not be: when it changes, the computer does the same;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S2.2-16** the boot order and device firmware must be recorded where the system is able to change them.
- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- **S3-2** If what the object does remains unknown, the case yields ?.

## Homogeneous rules and manual checks

### account

Every enumerated account is MUST under S2.2-15, irrespective of login shell. UID and GID in each checked row establish an account.

Manually checked rows:

- coreos-688f82dd27: adm; UID/GID and shell inspected.
- coreos-016dfe226d: avahi-autoipd; UID/GID and shell inspected.
- coreos-8d1e409524: bin; UID/GID and shell inspected.
- coreos-96a19ba1e6: census; UID/GID and shell inspected.
- coreos-a2044ac6f8: ceph; UID/GID and shell inspected.
- coreos-f3d59b813f: chrony; UID/GID and shell inspected.
- coreos-83bc7a060a: clevis; UID/GID and shell inspected.
- coreos-bee4a827f4: cockpit-ws; UID/GID and shell inspected.
- coreos-14dc4e5831: core; UID/GID and shell inspected.
- coreos-4900fca16b: daemon; UID/GID and shell inspected.
### kernel-module

Each loaded kernel module executes native code with kernel rights. S2.2-1 and S2.2-10 require it. Module names, loaded status and .ko paths establish this common property, irrespective of individual hardware support.

Manually checked rows:

- coreos-0074a80686: ata_generic; loaded module and native module path inspected.
- coreos-74d56deeff: be2iscsi; loaded module and native module path inspected.
- coreos-fb3db84e61: bnx2i; loaded module and native module path inspected.
- coreos-13fab1e09e: bochs; loaded module and native module path inspected.
- coreos-c65fa10f58: cnic; loaded module and native module path inspected.
- coreos-70a1915470: cxgb3; loaded module and native module path inspected.
- coreos-fc0b6e9d58: cxgb3i; loaded module and native module path inspected.
- coreos-f9596ccf1d: cxgb4; loaded module and native module path inspected.
- coreos-81e82393df: cxgb4i; loaded module and native module path inspected.
- coreos-77228a25f8: dm_multipath; loaded module and native module path inspected.
### process

Each observed userspace executable runs as its own process: MUST under S2.2-9 and S2.2-12. The kernel-thread aggregate is evaluated separately under S2.2-1 and S2.2-9.

Manually checked rows:

- coreos-323120ab12: /usr/bin/NetworkManager; PID list and executable identity inspected.
- coreos-7df9d4d1ad: /usr/bin/agetty; PID list and executable identity inspected.
- coreos-c2dda41768: /usr/bin/auditd; PID list and executable identity inspected.
- coreos-ce95966cbb: /usr/bin/bash; PID list and executable identity inspected.
- coreos-4fe1a69bcb: /usr/bin/chronyd; PID list and executable identity inspected.
- coreos-d5aa6b47fd: /usr/bin/dbus-broker; PID list and executable identity inspected.
- coreos-e0e91241c3: /usr/bin/dbus-broker-launch; PID list and executable identity inspected.
- coreos-5b9f128bb2: /usr/bin/gssproxy; PID list and executable identity inspected.
- coreos-5ff63dc6c3: /usr/bin/irqbalance; PID list and executable identity inspected.
- coreos-58a8ead628: /usr/bin/sshd; PID list and executable identity inspected.

Module documentation: https://docs.kernel.org/admin-guide/module-signing.html — “Modules are loaded with insmod, modprobe, `init_module()` or `finit_module()`”. This corroborates the loaded-module interpretation; raw/coreos/modules.txt supplies machine-specific observations.

The kernel-thread aggregate includes kthreadd, workqueue, networking, memory and filesystem tasks in raw/coreos/processes.txt; these are execution of the operating-system program, not historical records.

## Stored rows

These are assessed individually, including every member listed in raw/coreos/unowned-groups.json. Structural directories are considered with the files they make accessible; directory-only groups are assessed separately. Their inclusion does not turn a known content-only group into executable code.

### Interpretation of explicit exemptions

S2.2-3 introduces exceptions to the general dependence/removal test. A historical record is NOT under S2.2-6 even if consulted later: the sentence does not restrict the exemption to unread logs. Completion stamps and timer timestamps record completed events. Current bootloader component maps, ongoing transactions, operational identities and radio state are assessed by their current roles. No gap is inferred merely because Section 2.5 leaves state-management design open.

### Documentation excerpts for stored objects

Each row gives its principal basis; these sources supplement the inventory. Descriptions following quotations are inferences from the documented role, not observations of undisclosed file contents.

- Bash: https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files — “Bash reads and executes commands from the file”. The page explicitly identifies the three inventoried shell files.
- Boot preparation: URL in boot-edit.source.txt — “it create a .root_uuid stamp file on the bootfs or fails if one exists”. This establishes participation in boot preparation.
- Platform handling: https://github.com/coreos/coreos-installer/blob/main/src/install.rs — “Read the platform specifications from the platforms.json file.” PlatformSpec contains kernel arguments and bootloader commands.
- Provisioning report: https://github.com/coreos/ignition/blob/main/docs/release-notes.md — “Move Ignition report to”. The named destination is the inventoried result JSON.
- Update timestamps: https://www.freedesktop.org/software/systemd/man/latest/systemd-update-done.service.html — “updates the file modification time (mtime)”. The page describes both .updated files and subsequent condition checks.
- Permission-repair marker: URL in shadow-service.source.txt — “ConditionPathExists=!/etc/.rpm-ostree-shadow-mode-fixed2.stamp”. This suppresses repeat repair after completion.
- LVM population: URL in lvmdevices-service.source.txt — “ExecStartPost=touch /var/lib/coreos-populate-lvmdevices.stamp”. A matching absence condition controls execution.
- Shared container signature configuration: https://github.com/containers/image/blob/main/docs/containers-registries.d.5.md — “it can be shared by all users of containers/image.” The distribution file contains a lookaside signature URL; see registry.source.txt.
- LVM devices: https://www.man7.org/linux/man-pages/man8/lvmdevices.8.html — “The LVM devices file is the list of devices that lvm commands will use.”
- Password-quality policy: https://github.com/libpwquality/libpwquality/blob/master/doc/man/pwquality.conf.5.pod — “This file is read by the libpwquality library and utilities that use this library for checking and generating passwords.”
- Account database backup: https://man7.org/linux/man-pages/man5/shadow.5.html — “Backup file for /etc/shadow.” Other trailing-hyphen account database entries are corresponding backups, not active definitions.
- Bootloader state: https://raw.githubusercontent.com/coreos/bootupd/main/src/model.rs — “Maps a component name to its currently installed version”; “Maps a component name to an in progress update”. This is current operational state, not a sequential historical log.
- Account lock: https://man7.org/linux/man-pages/man3/lckpwdf.3.html — “protect against multiple simultaneous accesses of the shadow password database”. The inventory does not report lock holders.
- Desktop authentication: https://github.com/authselect/authselect/blob/master/src/man/authselect-profiles.5.adoc — “This file defines locks on values set in dconf database.” Actual values and resulting authentication effects are not captured.
- SSH public-key copies: https://raw.githubusercontent.com/openssh/openssh-portable/master/sshd.8 — “really used for anything”. The surrounding passage says public copies are provided for users to copy into known-host files. Private keys instead implement server identity.
- Labeling marker: https://raw.githubusercontent.com/ostreedev/ostree/main/src/libostree/ostree-sysroot-deploy.c — “var/.ostree-selabeled”. The surrounding function relabels when absent and then creates the marker.
- Repository cache: https://raw.githubusercontent.com/coreos/rpm-ostree/main/man/rpm-ostree.xml — “option cleans up cached RPM”. The repomd cleanup option discards repository metadata; the inventoried solver indexes are derived from it.
- Network identity: https://www.networkmanager.dev/docs/api/latest/NetworkManager.html — “The identity of the machine is determined by the”. The named file is secret_key; its seed generates stable network identifiers, rather than serving as a login password.
- Network internal settings: https://www.networkmanager.dev/docs/api/latest/NetworkManager.conf.html — “it is read last and can shadow user configuration”. Actual values are unavailable, so this member remains UNKNOWN.
- Network history: https://www.networkmanager.dev/docs/api/latest/nm-settings-nmcli.html — “NetworkManager internally tracks previously seen BSSIDs.”
- Persistent radio state, maintainer explanation: https://blogs.gnome.org/dcbw/2015/02/16/networkmanager-for-administrators-part-1/ — “This file stores persistent user-determined state for Airplane mode”. Timestamps record past connections; radio state governs current connectivity.
- RPC endpoints: https://man7.org/linux/man-pages/man8/rpc.gssd.8.html — “The rpc.gssd daemon uses the rpc_pipefs filesystem to communicate with the kernel.”
- User lingering: https://www.freedesktop.org/software/systemd/man/latest/loginctl.html — “a user manager is spawned for the user at boot and kept around after logouts.”
- Timer history: https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html — “the time when the service unit was last triggered is stored on disk.”
- GRUB translations: https://www.gnu.org/software/grub/manual/grub/grub.html — “Translation files in MO format are read from”. These are message content; native modules and executed commands have a different role.
- SELinux module store: https://raw.githubusercontent.com/SELinuxProject/selinux/master/libsemanage/src/semanage_store.c — “/commit_num”, “/modules_checksum”, “/policy.kern”. Source paths and operations identify policy, transaction serial and synchronization files. Lock state and derived-file reconstruction provenance remain unknown.
- RPM database: https://raw.githubusercontent.com/rpm-software-management/rpm/master/docs/man/rpm.8.scd — “metadata stored in the *rpm* database”. Its conventional path exposes package-management metadata used for verification and transactions.

### Explicit mixed member partitions

Every member is assigned once in part-1.root.members.tsv. Selectors apply only to exact inventoried members, not arbitrary descendants. Structural directories follow the files they expose; unrelated empty directories remain UNKNOWN.

- coreos-809cb439ce (/etc/alternatives): MUST 14, NOT 4. Exact paths in the member table.
- coreos-23a9706caf (/boot/grub2): MUST 294, NOT 44. Exact paths in the member table.
- coreos-f12cddbc22 (/etc/selinux): UNKNOWN 881, MUST 868, NOT 1. Exact paths in the member table.
- coreos-0075a76d48 (/etc/ssh): MUST 4, NOT 3. Exact paths in the member table.
- coreos-23f2259103 (/var/lib/NetworkManager): UNKNOWN 1, MUST 3, NOT 2. Exact paths in the member table.
- coreos-57da4d32dc (/var/lib/systemd): UNKNOWN 3, NOT 5, MUST 1. Exact paths in the member table.
- coreos-2d7adb8ef6 (/var/roothome): UNKNOWN 1, NOT 4, MUST 3. Exact paths in the member table.

### Review corrections

The alternatives summary counted five manual links; corrected to four, matching the exact member table. Package-module function corrections were handled in the package notes.

GRUB index grounding: https://raw.githubusercontent.com/rhboot/grub2/master/grub-core/normal/autofs.c states “Read the file fs.lst for auto-loading.” It installs an autoload hook calling grub_dl_load. fs.lst therefore enables loading filesystem implementations required to locate bootable systems, rather than just changing display content. Native module execution is corroborated by https://github.com/rhboot/grub2/blob/master/grub-core/kern/dl.c. Other index consumers could not be established in the consulted sources, including failed lookups of autocmd.c/autoload.c. Their member decisions were corrected to UNKNOWN, preserving the aggregate MIXED decision.

Updated coreos-23a9706caf member counts: {'MUST': 287, 'NOT': 44, 'UNKNOWN': 7}. This supersedes the earlier member-count summary above.

---

# Package classification notes

Scope: 483 package rows of part 1, classified independently from the supplied text and inventory, plus public package documentation. No removals or machine probes were performed.

## Evidence

The inventory establishes installed package identities and versions. Its package-files listing combines paths without package ownership, so package names alone were not treated as evidence of executable content. The public Fedora metadata service provides per-package function descriptions and, for boundary cases, file lists. Documentation describes the Fedora 44 package family; repository revisions can differ from the inventory version. Classification uses documented purpose rather than claiming byte identity.

The metadata API documents its package and file-list endpoints at https://mdapi.fedoraproject.org/ : “You can retrieve the information about a specific package on a specific branch by querying its package name.”

## Scripted rule: executable implementations

Apply only to packages whose individually inspected descriptions identify executable utilities, daemons, interpreters, native shared libraries, or executable integration modules. A package containing such an implementation is MUST under S2.2-9 or S2.2-10, supported by S2.2-1 and S2.2-2. Shared native libraries execute in their callers’ address spaces and with their callers’ rights; they are not database content or confined web-page code. No name-prefix-only inference establishes function: the per-package description is the evidence. Distribution metadata, data-only packages, settings and directory-only packages were excluded and decided individually in packages-special.tsv. Accompanying manuals do not make a single package row a group row: members=1 throughout this subset.

Exact deciding sentences:

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-9: “a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

Manual checks of the scripted rule are listed below. Each description was read directly, not only matched by a pattern. Thirty checks cover standalone programs, loaded native code and integration scripts/modules; all supply executable implementation.

- coreos-7e581bffc1: The GNU Bourne Again shell. [bash](https://mdapi.fedoraproject.org/f44/pkg/bash).
- coreos-0193da0aff: A set of basic GNU tools commonly used in shell scripts. [coreutils](https://mdapi.fedoraproject.org/f44/pkg/coreutils).
- coreos-aeb3d018e8: A utility for getting files from remote servers (FTP, HTTP, and others). [curl](https://mdapi.fedoraproject.org/f44/pkg/curl).
- coreos-0995783d77: An NTP client/server. [chrony](https://mdapi.fedoraproject.org/f44/pkg/chrony).
- coreos-cfb2399c07: Command-line package manager. [dnf5](https://mdapi.fedoraproject.org/f44/pkg/dnf5).
- coreos-260249db89: Settings tool for Ethernet NICs. [ethtool](https://mdapi.fedoraproject.org/f44/pkg/ethtool).
- coreos-565b5cc910: A small text editor. [nano](https://mdapi.fedoraproject.org/f44/pkg/nano).
- coreos-7a42a4252b: Manage Pods, Containers and Container Images. [podman](https://mdapi.fedoraproject.org/f44/pkg/podman).
- coreos-ffc8d72bcf: Allows restricted root access for specified users. [sudo](https://mdapi.fedoraproject.org/f44/pkg/sudo).
- coreos-50e2bf1471: System and Service Manager. [systemd](https://mdapi.fedoraproject.org/f44/pkg/systemd).
- coreos-f3c1ddad24: Libraries for adding NetworkManager support to applications.. [NetworkManager-libnm](https://mdapi.fedoraproject.org/f44/pkg/NetworkManager-libnm).
- coreos-74c2756231: Dynamic library for libaudit. [audit-libs](https://mdapi.fedoraproject.org/f44/pkg/audit-libs).
- coreos-34bed8330e: Libraries used by the BIND DNS packages. [bind-libs](https://mdapi.fedoraproject.org/f44/pkg/bind-libs).
- coreos-1ef7821ef8: A library that performs asynchronous DNS operations. [c-ares](https://mdapi.fedoraproject.org/f44/pkg/c-ares).
- coreos-ef9986c01f: The GNU libc libraries. [glibc](https://mdapi.fedoraproject.org/f44/pkg/glibc).
- coreos-8263d34f1d: Dynamic library for access control list support. [libacl](https://mdapi.fedoraproject.org/f44/pkg/libacl).
- coreos-821b73ea25: A library for handling streaming archive formats. [libarchive](https://mdapi.fedoraproject.org/f44/pkg/libarchive).
- coreos-9056c714eb: Library for getting and setting POSIX.1e capabilities. [libcap](https://mdapi.fedoraproject.org/f44/pkg/libcap).
- coreos-1be2d8a6c5: Enhanced seccomp library. [libseccomp](https://mdapi.fedoraproject.org/f44/pkg/libseccomp).
- coreos-e81d659198: A general purpose cryptography library with TLS implementation. [openssl-libs](https://mdapi.fedoraproject.org/f44/pkg/openssl-libs).
- coreos-e8ce9e26b5: Programmable completion for Bash. [bash-completion](https://mdapi.fedoraproject.org/f44/pkg/bash-completion).
- coreos-b0ae80e209: Dracut modules for afterburn. [afterburn-dracut](https://mdapi.fedoraproject.org/f44/pkg/afterburn-dracut).
- coreos-0396c2cd0e: Dracut integration for clevis. [clevis-dracut](https://mdapi.fedoraproject.org/f44/pkg/clevis-dracut).
- coreos-8659fdc136: systemd integration for clevis. [clevis-systemd](https://mdapi.fedoraproject.org/f44/pkg/clevis-systemd).
- coreos-cee9463582: A script for growing a partition. [cloud-utils-growpart](https://mdapi.fedoraproject.org/f44/pkg/cloud-utils-growpart).
- coreos-175467aee2: dracut modules to build a dracut initramfs with network support. [dracut-network](https://mdapi.fedoraproject.org/f44/pkg/dracut-network).
- coreos-7ffeb97666: dracut module to build an initramfs with most files in a squashfs image. [dracut-squash](https://mdapi.fedoraproject.org/f44/pkg/dracut-squash).
- coreos-84590fac64: Issue generator scripts showing SSH keys and IP address. [console-login-helper-messages-issuegen](https://mdapi.fedoraproject.org/f44/pkg/console-login-helper-messages-issuegen).
- coreos-ab0dd862b9: Message of the day generator script showing system information. [console-login-helper-messages-motdgen](https://mdapi.fedoraproject.org/f44/pkg/console-login-helper-messages-motdgen).
- coreos-87cc515d65: Profile script showing systemd failed units. [console-login-helper-messages-profile](https://mdapi.fedoraproject.org/f44/pkg/console-login-helper-messages-profile).

## Individually decided boundary cases

All exceptions are explicitly enumerated in packages-special.tsv with their own function and reasoning. File lists show that seemingly informational packages can contain active code or system policy: vim-data contains defaults.vim; bash-color-prompt and nano-default-editor contain shell startup files; grub2-common contains kernel installation hooks; hwdata contains a module blacklist; release identity packages contain service presets; shared-mime-info includes a database updater. These findings prevent classifying them from their names alone.

Directory-only and fileless dependency packages are HOLE, not UNKNOWN: their function is documented, but the removal test lacks an object boundary. Removing package registration or empty directory ownership leaves dependent implementations available; treating the package as including the dependent implementation or populated directory removes capabilities. Section 2.2 does not say which removal the package row denotes. This is a classification-object ambiguity, not a demand to specify system state handling. No claim is made about how a distribution should implement removal.

Ordinary licence and syntax documents and translated messages are NOT under S2.2-4. Firmware packages contain loadable device implementations; they are distinct from documentation describing firmware. System keyboard mappings, trust roots, terminal control descriptions and timezone rules affect operations across programs. The database-content exemption requires unchanged behaviour and therefore does not cover these operational rules.

## Documentation quotations

Each following short exact quotation is from that package’s public metadata summary. The saved evidence also records file-list snippets for boundary cases.

- coreos-63d110eacd — [NetworkManager](https://mdapi.fedoraproject.org/f44/pkg/NetworkManager): “Network connection manager and user applications”.
- coreos-dff0e9e5a9 — [NetworkManager-cloud-setup](https://mdapi.fedoraproject.org/f44/pkg/NetworkManager-cloud-setup): “Automatically configure NetworkManager in cloud”.
- coreos-f3c1ddad24 — [NetworkManager-libnm](https://mdapi.fedoraproject.org/f44/pkg/NetworkManager-libnm): “Libraries for adding NetworkManager support to applications.”.
- coreos-7f3530663e — [NetworkManager-team](https://mdapi.fedoraproject.org/f44/pkg/NetworkManager-team): “Team device plugin for NetworkManager”.
- coreos-a3cfe34149 — [NetworkManager-tui](https://mdapi.fedoraproject.org/f44/pkg/NetworkManager-tui): “NetworkManager curses-based UI”.
- coreos-1c2e270b27 — [WALinuxAgent-udev](https://mdapi.fedoraproject.org/f44/pkg/WALinuxAgent-udev): “Udev rules for Microsoft Azure”.
- coreos-e468c6f8bb — [aardvark-dns](https://mdapi.fedoraproject.org/f44/pkg/aardvark-dns): “Authoritative DNS server for A/AAAA container records”.
- coreos-366d5ef548 — [acl](https://mdapi.fedoraproject.org/f44/pkg/acl): “Access control list utilities”.
- coreos-58e8c8cb13 — [adcli](https://mdapi.fedoraproject.org/f44/pkg/adcli): “Active Directory enrollment”.
- coreos-47dcb4622a — [adcli-selinux](https://mdapi.fedoraproject.org/f44/pkg/adcli-selinux): “The adcli SELinux policy”.
- coreos-b9a6118ba5 — [afterburn](https://mdapi.fedoraproject.org/f44/pkg/afterburn): “Simple cloud provider agent”.
- coreos-b0ae80e209 — [afterburn-dracut](https://mdapi.fedoraproject.org/f44/pkg/afterburn-dracut): “Dracut modules for afterburn”.
- coreos-376faeab5b — [alternatives](https://mdapi.fedoraproject.org/f44/pkg/alternatives): “A tool to maintain symbolic links determining default commands”.
- coreos-8d15baf920 — [amd-gpu-firmware](https://mdapi.fedoraproject.org/f44/pkg/amd-gpu-firmware): “Firmware for AMD GPUs”.
- coreos-8da34fafa6 — [amd-ucode-firmware](https://mdapi.fedoraproject.org/f44/pkg/amd-ucode-firmware): “Microcode updates for AMD CPUs”.
- coreos-e70f129b34 — [attr](https://mdapi.fedoraproject.org/f44/pkg/attr): “Utilities for managing filesystem extended attributes”.
- coreos-0f154c42d9 — [audit](https://mdapi.fedoraproject.org/f44/pkg/audit): “User space tools for kernel auditing”.
- coreos-74c2756231 — [audit-libs](https://mdapi.fedoraproject.org/f44/pkg/audit-libs): “Dynamic library for libaudit”.
- coreos-5384bc590f — [audit-rules](https://mdapi.fedoraproject.org/f44/pkg/audit-rules): “audit rules and utilities”.
- coreos-75d85d00b8 — [authselect](https://mdapi.fedoraproject.org/f44/pkg/authselect): “Configures authentication and identity sources from supported profiles”.
- coreos-2a048e9d56 — [authselect-libs](https://mdapi.fedoraproject.org/f44/pkg/authselect-libs): “Utility library used by the authselect tool”.
- coreos-082f54e226 — [azure-vm-utils](https://mdapi.fedoraproject.org/f44/pkg/azure-vm-utils): “Core utilities and configuration for Linux VMs on Azure”.
- coreos-7e581bffc1 — [bash](https://mdapi.fedoraproject.org/f44/pkg/bash): “The GNU Bourne Again shell”.
- coreos-8a00b8ef09 — [bash-color-prompt](https://mdapi.fedoraproject.org/f44/pkg/bash-color-prompt): “Color prompt for bash shell”.
- coreos-e8ce9e26b5 — [bash-completion](https://mdapi.fedoraproject.org/f44/pkg/bash-completion): “Programmable completion for Bash”.
- coreos-34bed8330e — [bind-libs](https://mdapi.fedoraproject.org/f44/pkg/bind-libs): “Libraries used by the BIND DNS packages”.
- coreos-77d324c60b — [bind-utils](https://mdapi.fedoraproject.org/f44/pkg/bind-utils): “Utilities for querying DNS name servers”.
- coreos-8909dee021 — [bootc](https://mdapi.fedoraproject.org/f44/pkg/bootc): “Bootable container system”.
- coreos-1f8e3c97b1 — [bootupd](https://mdapi.fedoraproject.org/f44/pkg/bootupd): “Bootloader updater”.
- coreos-4dd4696ff5 — [bsdtar](https://mdapi.fedoraproject.org/f44/pkg/bsdtar): “Manipulate tape archives”.
- coreos-1a23568212 — [btrfs-progs](https://mdapi.fedoraproject.org/f44/pkg/btrfs-progs): “Userspace programs for btrfs”.
- coreos-044a20fe18 — [bubblewrap](https://mdapi.fedoraproject.org/f44/pkg/bubblewrap): “Core execution tool for unprivileged containers”.
- coreos-33df359f48 — [bzip2](https://mdapi.fedoraproject.org/f44/pkg/bzip2): “File compression utility”.
- coreos-87d225dda0 — [bzip2-libs](https://mdapi.fedoraproject.org/f44/pkg/bzip2-libs): “Libraries for applications using bzip2”.
- coreos-1ef7821ef8 — [c-ares](https://mdapi.fedoraproject.org/f44/pkg/c-ares): “A library that performs asynchronous DNS operations”.
- coreos-25fe0e46e8 — [ca-certificates](https://mdapi.fedoraproject.org/f44/pkg/ca-certificates): “The Mozilla CA root certificate bundle”.
- coreos-b5785d4138 — [catatonit](https://mdapi.fedoraproject.org/f44/pkg/catatonit): “A signal-forwarding process manager for containers”.
- coreos-0995783d77 — [chrony](https://mdapi.fedoraproject.org/f44/pkg/chrony): “An NTP client/server”.
- coreos-27445df088 — [cifs-utils](https://mdapi.fedoraproject.org/f44/pkg/cifs-utils): “Utilities for mounting and managing CIFS mounts”.
- coreos-7537f58886 — [clevis](https://mdapi.fedoraproject.org/f44/pkg/clevis): “Automated decryption framework”.
- coreos-0396c2cd0e — [clevis-dracut](https://mdapi.fedoraproject.org/f44/pkg/clevis-dracut): “Dracut integration for clevis”.
- coreos-768551d990 — [clevis-luks](https://mdapi.fedoraproject.org/f44/pkg/clevis-luks): “LUKS integration for clevis”.
- coreos-4dfbe04a79 — [clevis-pin-tpm2](https://mdapi.fedoraproject.org/f44/pkg/clevis-pin-tpm2): “Clevis PIN for unlocking with TPM2 supporting Authorized Policies”.
- coreos-8659fdc136 — [clevis-systemd](https://mdapi.fedoraproject.org/f44/pkg/clevis-systemd): “systemd integration for clevis”.
- coreos-cee9463582 — [cloud-utils-growpart](https://mdapi.fedoraproject.org/f44/pkg/cloud-utils-growpart): “A script for growing a partition”.
- coreos-cecad5827b — [composefs](https://mdapi.fedoraproject.org/f44/pkg/composefs): “Tools to handle creating and mounting composefs images”.
- coreos-4edd221aad — [composefs-libs](https://mdapi.fedoraproject.org/f44/pkg/composefs-libs): “Libraries for composefs”.
- coreos-1a16421180 — [conmon](https://mdapi.fedoraproject.org/f44/pkg/conmon): “OCI container runtime monitor”.
- coreos-7f9505c013 — [console-login-helper-messages](https://mdapi.fedoraproject.org/f44/pkg/console-login-helper-messages): “Combines motd, issue, profile features to show system information to”.
- coreos-84590fac64 — [console-login-helper-messages-issuegen](https://mdapi.fedoraproject.org/f44/pkg/console-login-helper-messages-issuegen): “Issue generator scripts showing SSH keys and IP address”.
- coreos-ab0dd862b9 — [console-login-helper-messages-motdgen](https://mdapi.fedoraproject.org/f44/pkg/console-login-helper-messages-motdgen): “Message of the day generator script showing system information”.
- coreos-87cc515d65 — [console-login-helper-messages-profile](https://mdapi.fedoraproject.org/f44/pkg/console-login-helper-messages-profile): “Profile script showing systemd failed units”.
- coreos-e9983ff941 — [container-selinux](https://mdapi.fedoraproject.org/f44/pkg/container-selinux): “SELinux policies for container runtimes”.
- coreos-7fd1231eae — [containerd](https://mdapi.fedoraproject.org/f44/pkg/containerd): “An open and reliable container runtime”.
- coreos-be2c2b37b4 — [containers-common](https://mdapi.fedoraproject.org/f44/pkg/containers-common): “Common configuration and documentation for containers”.
- coreos-d49702b0f3 — [containers-common-extra](https://mdapi.fedoraproject.org/f44/pkg/containers-common-extra): “Extra dependencies for Podman and Buildah”.
- coreos-dc63698fdd — [coreos-installer](https://mdapi.fedoraproject.org/f44/pkg/coreos-installer): “Installer for Fedora CoreOS and RHEL CoreOS”.
- coreos-6d64501b94 — [coreos-installer-bootinfra](https://mdapi.fedoraproject.org/f44/pkg/coreos-installer-bootinfra): “coreos-installer boot-time infrastructure for use on Fedora/RHEL CoreOS”.
- coreos-0193da0aff — [coreutils](https://mdapi.fedoraproject.org/f44/pkg/coreutils): “A set of basic GNU tools commonly used in shell”.
- coreos-3ed34b954a — [coreutils-common](https://mdapi.fedoraproject.org/f44/pkg/coreutils-common): “coreutils common optional components”.
- coreos-dc687dcf52 — [cpio](https://mdapi.fedoraproject.org/f44/pkg/cpio): “A GNU archiving program”.
- coreos-61ca8524d2 — [cracklib](https://mdapi.fedoraproject.org/f44/pkg/cracklib): “A password-checking library”.
- coreos-fb6e0c43dc — [criu](https://mdapi.fedoraproject.org/f44/pkg/criu): “Tool for Checkpoint/Restore in User-space”.
- coreos-c6cef83e00 — [criu-libs](https://mdapi.fedoraproject.org/f44/pkg/criu-libs): “Libraries for criu”.
- coreos-9c9b977afe — [crun](https://mdapi.fedoraproject.org/f44/pkg/crun): “OCI runtime written in C”.
- coreos-eea0c3d435 — [crun-wasm](https://mdapi.fedoraproject.org/f44/pkg/crun-wasm): “crun with wasm support”.
- coreos-5d25b880f9 — [crypto-policies](https://mdapi.fedoraproject.org/f44/pkg/crypto-policies): “System-wide crypto policies”.
- coreos-8c3f980c48 — [cryptsetup](https://mdapi.fedoraproject.org/f44/pkg/cryptsetup): “Utility for setting up encrypted disks”.
- coreos-4cb6eeb8d6 — [cryptsetup-libs](https://mdapi.fedoraproject.org/f44/pkg/cryptsetup-libs): “Cryptsetup shared library”.
- coreos-aeb3d018e8 — [curl](https://mdapi.fedoraproject.org/f44/pkg/curl): “A utility for getting files from remote servers (FTP, HTTP,”.
- coreos-1b77999e98 — [cyrus-sasl-gssapi](https://mdapi.fedoraproject.org/f44/pkg/cyrus-sasl-gssapi): “GSSAPI authentication support for Cyrus SASL”.
- coreos-3d63bcf222 — [cyrus-sasl-lib](https://mdapi.fedoraproject.org/f44/pkg/cyrus-sasl-lib): “Shared libraries needed by applications which use Cyrus SASL”.
- coreos-5ddf73f1ac — [dbus](https://mdapi.fedoraproject.org/f44/pkg/dbus): “D-BUS message bus”.
- coreos-95e624f4d6 — [dbus-broker](https://mdapi.fedoraproject.org/f44/pkg/dbus-broker): “Linux D-Bus Message Broker”.
- coreos-f56ab0f4a8 — [dbus-common](https://mdapi.fedoraproject.org/f44/pkg/dbus-common): “D-BUS message bus configuration”.
- coreos-a1738811a2 — [dbus-libs](https://mdapi.fedoraproject.org/f44/pkg/dbus-libs): “Libraries for accessing D-BUS”.
- coreos-35f10107d2 — [device-mapper](https://mdapi.fedoraproject.org/f44/pkg/device-mapper): “Device mapper utility”.
- coreos-40cd98e117 — [device-mapper-event](https://mdapi.fedoraproject.org/f44/pkg/device-mapper-event): “Device-mapper event daemon”.
- coreos-2db543012f — [device-mapper-event-libs](https://mdapi.fedoraproject.org/f44/pkg/device-mapper-event-libs): “Device-mapper event daemon shared library”.
- coreos-10115d09cb — [device-mapper-libs](https://mdapi.fedoraproject.org/f44/pkg/device-mapper-libs): “Device-mapper shared library”.
- coreos-e27847dd7e — [device-mapper-multipath](https://mdapi.fedoraproject.org/f44/pkg/device-mapper-multipath): “Tools to manage multipath devices using device-mapper”.
- coreos-5f0b8d3b53 — [device-mapper-multipath-libs](https://mdapi.fedoraproject.org/f44/pkg/device-mapper-multipath-libs): “The device-mapper-multipath modules and shared library”.
- coreos-d295ea0fe4 — [device-mapper-persistent-data](https://mdapi.fedoraproject.org/f44/pkg/device-mapper-persistent-data): “Device-mapper Persistent Data Tools”.
- coreos-9dc02150a9 — [diffutils](https://mdapi.fedoraproject.org/f44/pkg/diffutils): “GNU collection of diff utilities”.
- coreos-cfb2399c07 — [dnf5](https://mdapi.fedoraproject.org/f44/pkg/dnf5): “Command-line package manager”.
- coreos-b17e3d0c14 — [dnsmasq](https://mdapi.fedoraproject.org/f44/pkg/dnsmasq): “A lightweight DHCP/caching DNS server”.
- coreos-353798ef36 — [docker-cli](https://mdapi.fedoraproject.org/f44/pkg/docker-cli): “The Docker CLI”.
- coreos-b141cac26b — [dosfstools](https://mdapi.fedoraproject.org/f44/pkg/dosfstools): “Utilities for making and checking MS-DOS FAT filesystems on Linux”.
- coreos-7670bd2540 — [dracut](https://mdapi.fedoraproject.org/f44/pkg/dracut): “Initramfs generator using udev”.
- coreos-175467aee2 — [dracut-network](https://mdapi.fedoraproject.org/f44/pkg/dracut-network): “dracut modules to build a dracut initramfs with network support”.
- coreos-7ffeb97666 — [dracut-squash](https://mdapi.fedoraproject.org/f44/pkg/dracut-squash): “dracut module to build an initramfs with most files in”.
- coreos-81d0a02a95 — [duktape](https://mdapi.fedoraproject.org/f44/pkg/duktape): “Embeddable Javascript engine”.
- coreos-6eda280f77 — [e2fsprogs](https://mdapi.fedoraproject.org/f44/pkg/e2fsprogs): “Utilities for managing ext2, ext3, and ext4 file systems”.
- coreos-c6925b10a0 — [e2fsprogs-libs](https://mdapi.fedoraproject.org/f44/pkg/e2fsprogs-libs): “Ext2/3/4 file system specific shared libraries”.
- coreos-bc2b712980 — [efi-filesystem](https://mdapi.fedoraproject.org/f44/pkg/efi-filesystem): “The basic directory layout for EFI machines”.
- coreos-963b8a3d15 — [efibootmgr](https://mdapi.fedoraproject.org/f44/pkg/efibootmgr): “EFI Boot Manager”.
- coreos-a7aefe035b — [efivar-libs](https://mdapi.fedoraproject.org/f44/pkg/efivar-libs): “Library to manage UEFI variables”.
- coreos-29d771e7fa — [elfutils-default-yama-scope](https://mdapi.fedoraproject.org/f44/pkg/elfutils-default-yama-scope): “Default yama attach scope sysctl setting”.
- coreos-d20265f542 — [elfutils-libelf](https://mdapi.fedoraproject.org/f44/pkg/elfutils-libelf): “Library to read and write ELF files”.
- coreos-11e004dea9 — [elfutils-libs](https://mdapi.fedoraproject.org/f44/pkg/elfutils-libs): “Libraries to handle compiled objects”.
- coreos-260249db89 — [ethtool](https://mdapi.fedoraproject.org/f44/pkg/ethtool): “Settings tool for Ethernet NICs”.
- coreos-85dc57d931 — [expat](https://mdapi.fedoraproject.org/f44/pkg/expat): “An XML parser library”.
- coreos-81c99a9fcb — [fedora-gpg-keys](https://mdapi.fedoraproject.org/f44/pkg/fedora-gpg-keys): “Fedora RPM keys”.
- coreos-8542fa1711 — [fedora-release-common](https://mdapi.fedoraproject.org/f44/pkg/fedora-release-common): “Fedora release files”.
- coreos-d9db8ebd61 — [fedora-release-coreos](https://mdapi.fedoraproject.org/f44/pkg/fedora-release-coreos): “Base package for Fedora CoreOS-specific default configurations”.
- coreos-3e46edf1bb — [fedora-release-identity-coreos](https://mdapi.fedoraproject.org/f44/pkg/fedora-release-identity-coreos): “Package providing the identity for Fedora CoreOS”.
- coreos-b93da1d973 — [fedora-repos](https://mdapi.fedoraproject.org/f44/pkg/fedora-repos): “Fedora package repositories”.
- coreos-6d32cdfc21 — [fedora-repos-archive](https://mdapi.fedoraproject.org/f44/pkg/fedora-repos-archive): “Fedora updates archive package repository”.
- coreos-ae08fbb9b9 — [file](https://mdapi.fedoraproject.org/f44/pkg/file): “Utility for determining file types”.
- coreos-622ec08a5f — [file-libs](https://mdapi.fedoraproject.org/f44/pkg/file-libs): “Libraries for applications using libmagic”.
- coreos-705fd08cd6 — [filesystem](https://mdapi.fedoraproject.org/f44/pkg/filesystem): “The basic directory layout for a Linux system”.
- coreos-55f35bbf11 — [findutils](https://mdapi.fedoraproject.org/f44/pkg/findutils): “The GNU versions of find utilities (find and xargs)”.
- coreos-0afb6efb2e — [flatpak-session-helper](https://mdapi.fedoraproject.org/f44/pkg/flatpak-session-helper): “User D-Bus service used by flatpak and others”.
- coreos-8334624d91 — [fmt](https://mdapi.fedoraproject.org/f44/pkg/fmt): “Small, safe and fast formatting library for C++”.
- coreos-0c06642f40 — [fstrm](https://mdapi.fedoraproject.org/f44/pkg/fstrm): “Frame Streams implementation in C”.
- coreos-4c44b1402c — [fuse-common](https://mdapi.fedoraproject.org/f44/pkg/fuse-common): “Common files for File System in Userspace (FUSE) v2 and”.
- coreos-5b9e69b119 — [fuse-overlayfs](https://mdapi.fedoraproject.org/f44/pkg/fuse-overlayfs): “FUSE overlay+shiftfs implementation for rootless containers”.
- coreos-12c7acb05a — [fuse-sshfs](https://mdapi.fedoraproject.org/f44/pkg/fuse-sshfs): “FUSE-Filesystem to access remote filesystems via SSH”.
- coreos-7d79754cca — [fuse3](https://mdapi.fedoraproject.org/f44/pkg/fuse3): “File System in Userspace (FUSE) v3 utilities”.
- coreos-ddb6c2cb64 — [fuse3-libs](https://mdapi.fedoraproject.org/f44/pkg/fuse3-libs): “File System in Userspace (FUSE) v3 libraries”.
- coreos-7cfd84f60c — [fwupd](https://mdapi.fedoraproject.org/f44/pkg/fwupd): “Firmware update daemon”.
- coreos-162a0e2c7e — [gawk](https://mdapi.fedoraproject.org/f44/pkg/gawk): “The GNU version of the AWK text processing utility”.
- coreos-d1637c42e8 — [gdbm](https://mdapi.fedoraproject.org/f44/pkg/gdbm): “A GNU set of database routines which use extensible hashing”.
- coreos-90ea44adeb — [gdbm-libs](https://mdapi.fedoraproject.org/f44/pkg/gdbm-libs): “Libraries files for gdbm”.
- coreos-9c33950601 — [gdisk](https://mdapi.fedoraproject.org/f44/pkg/gdisk): “An fdisk-like partitioning tool for GPT disks”.
- coreos-c94641e220 — [gettext-envsubst](https://mdapi.fedoraproject.org/f44/pkg/gettext-envsubst): “Substitutes the values of environment variables”.
- coreos-c4bf90c6df — [gettext-libs](https://mdapi.fedoraproject.org/f44/pkg/gettext-libs): “Libraries for gettext”.
- coreos-0f2b75cc18 — [gettext-runtime](https://mdapi.fedoraproject.org/f44/pkg/gettext-runtime): “GNU runtime libraries and programs for producing multi-lingual messages”.
- coreos-4a2c82b764 — [git-core](https://mdapi.fedoraproject.org/f44/pkg/git-core): “Core package of git with minimal functionality”.
- coreos-5039d272e2 — [glib2](https://mdapi.fedoraproject.org/f44/pkg/glib2): “A library of handy utility functions”.
- coreos-ef9986c01f — [glibc](https://mdapi.fedoraproject.org/f44/pkg/glibc): “The GNU libc libraries”.
- coreos-1600002691 — [glibc-common](https://mdapi.fedoraproject.org/f44/pkg/glibc-common): “Common binaries and locale data for glibc”.
- coreos-3258b68544 — [glibc-gconv-extra](https://mdapi.fedoraproject.org/f44/pkg/glibc-gconv-extra): “All iconv converter modules for glibc.”.
- coreos-80c805d99c — [glibc-minimal-langpack](https://mdapi.fedoraproject.org/f44/pkg/glibc-minimal-langpack): “Minimal language packs for glibc.”.
- coreos-f969339b5f — [gmp](https://mdapi.fedoraproject.org/f44/pkg/gmp): “GNU arbitrary precision library”.
- coreos-649434ba30 — [gnulib-l10n](https://mdapi.fedoraproject.org/f44/pkg/gnulib-l10n): “Localizations for Gnulib”.
- coreos-15f061c6d5 — [gnupg2](https://mdapi.fedoraproject.org/f44/pkg/gnupg2): “Utility for secure communication and data storage”.
- coreos-00729a9b5c — [gnupg2-dirmngr](https://mdapi.fedoraproject.org/f44/pkg/gnupg2-dirmngr): “GnuPG network certificate management service”.
- coreos-811a2431bb — [gnupg2-gpg-agent](https://mdapi.fedoraproject.org/f44/pkg/gnupg2-gpg-agent): “GnuPG cryptographic agent”.
- coreos-0d61fe56d4 — [gnupg2-gpgconf](https://mdapi.fedoraproject.org/f44/pkg/gnupg2-gpgconf): “GnuPG core configuration utilities”.
- coreos-1722def71c — [gnupg2-keyboxd](https://mdapi.fedoraproject.org/f44/pkg/gnupg2-keyboxd): “GnuPG public key material service”.
- coreos-363a4747b8 — [gnupg2-verify](https://mdapi.fedoraproject.org/f44/pkg/gnupg2-verify): “GnuPG signature verification tool”.
- coreos-0698e8e13b — [gnutls](https://mdapi.fedoraproject.org/f44/pkg/gnutls): “A TLS protocol implementation”.
- coreos-cb2b49ffa2 — [google-compute-engine-guest-configs-udev](https://mdapi.fedoraproject.org/f44/pkg/google-compute-engine-guest-configs-udev): “udev rules for google-compute-engine-guest-configs”.
- coreos-31e6f0ceca — [gpgme](https://mdapi.fedoraproject.org/f44/pkg/gpgme): “GnuPG Made Easy - high level crypto API”.
- coreos-9573ee576e — [grep](https://mdapi.fedoraproject.org/f44/pkg/grep): “Pattern matching utilities”.
- coreos-e66369e38a — [grub2-common](https://mdapi.fedoraproject.org/f44/pkg/grub2-common): “grub2 common layout”.
- coreos-f650a7ba4a — [grub2-efi-x64](https://mdapi.fedoraproject.org/f44/pkg/grub2-efi-x64): “GRUB for EFI systems.”.
- coreos-c6e0e5b67e — [grub2-pc](https://mdapi.fedoraproject.org/f44/pkg/grub2-pc): “Bootloader with support for Linux, Multiboot, and more”.
- coreos-aae56aa09f — [grub2-pc-modules](https://mdapi.fedoraproject.org/f44/pkg/grub2-pc-modules): “Modules used to build custom grub images”.
- coreos-3646a16b4b — [grub2-tools](https://mdapi.fedoraproject.org/f44/pkg/grub2-tools): “Support tools for GRUB.”.
- coreos-6484b21b83 — [grub2-tools-minimal](https://mdapi.fedoraproject.org/f44/pkg/grub2-tools-minimal): “Support tools for GRUB.”.
- coreos-f4b67c06fa — [gssproxy](https://mdapi.fedoraproject.org/f44/pkg/gssproxy): “GSSAPI Proxy”.
- coreos-e2c6ab9a77 — [gzip](https://mdapi.fedoraproject.org/f44/pkg/gzip): “GNU data compression program”.
- coreos-ba3c150598 — [hostname](https://mdapi.fedoraproject.org/f44/pkg/hostname): “Utility to set/show the host name or domain name”.
- coreos-255276b939 — [hwdata](https://mdapi.fedoraproject.org/f44/pkg/hwdata): “Hardware identification and configuration data”.
- coreos-cfa458bd11 — [ignition](https://mdapi.fedoraproject.org/f44/pkg/ignition): “First boot installer and configuration tool”.
- coreos-83bd886029 — [ignition-grub](https://mdapi.fedoraproject.org/f44/pkg/ignition-grub): “Enablement glue for bootupd's grub2 config”.
- coreos-c806b2dc2f — [inih](https://mdapi.fedoraproject.org/f44/pkg/inih): “Simple INI file parser library”.
- coreos-f5df3bac85 — [intel-gpu-firmware](https://mdapi.fedoraproject.org/f44/pkg/intel-gpu-firmware): “Firmware for Intel GPUs”.
- coreos-87615c4328 — [ipcalc](https://mdapi.fedoraproject.org/f44/pkg/ipcalc): “IP network address calculator”.
- coreos-eac9f712f1 — [iproute](https://mdapi.fedoraproject.org/f44/pkg/iproute): “Advanced IP routing and network device configuration tools”.
- coreos-597c55d43f — [iproute-tc](https://mdapi.fedoraproject.org/f44/pkg/iproute-tc): “Linux Traffic Control utility”.
- coreos-9788ef0867 — [iptables-libs](https://mdapi.fedoraproject.org/f44/pkg/iptables-libs): “libxtables and iptables extensions userspace support”.
- coreos-e4b295c645 — [iptables-nft](https://mdapi.fedoraproject.org/f44/pkg/iptables-nft): “nftables compatibility for iptables, arptables and ebtables”.
- coreos-708f435dde — [iptables-services](https://mdapi.fedoraproject.org/f44/pkg/iptables-services): “iptables and ip6tables services for iptables”.
- coreos-e795bb7c9f — [iptables-utils](https://mdapi.fedoraproject.org/f44/pkg/iptables-utils): “iptables and ip6tables misc utilities”.
- coreos-cdef01aa99 — [iputils](https://mdapi.fedoraproject.org/f44/pkg/iputils): “Network monitoring tools including ping”.
- coreos-339a11db57 — [irqbalance](https://mdapi.fedoraproject.org/f44/pkg/irqbalance): “IRQ balancing daemon”.
- coreos-a4b85c53e7 — [iscsi-initiator-utils](https://mdapi.fedoraproject.org/f44/pkg/iscsi-initiator-utils): “iSCSI daemon and utility programs”.
- coreos-4b1ab8b13d — [iscsi-initiator-utils-iscsiuio](https://mdapi.fedoraproject.org/f44/pkg/iscsi-initiator-utils-iscsiuio): “Userspace configuration daemon required for some iSCSI hardware”.
- coreos-6b9f0c9a1f — [isns-utils-libs](https://mdapi.fedoraproject.org/f44/pkg/isns-utils-libs): “Shared library files for iSNS”.
- coreos-e5ce1280b2 — [jansson](https://mdapi.fedoraproject.org/f44/pkg/jansson): “C library for encoding, decoding and manipulating JSON data”.
- coreos-b8fbe826d7 — [jose](https://mdapi.fedoraproject.org/f44/pkg/jose): “Tools for JSON Object Signing and Encryption (JOSE)”.
- coreos-6fdd3238b7 — [jq](https://mdapi.fedoraproject.org/f44/pkg/jq): “Command-line JSON processor”.
- coreos-8c8a578b79 — [json-c](https://mdapi.fedoraproject.org/f44/pkg/json-c): “JSON implementation in C”.
- coreos-4f2c91d418 — [json-glib](https://mdapi.fedoraproject.org/f44/pkg/json-glib): “Library for JavaScript Object Notation format”.
- coreos-2c5af78459 — [kbd](https://mdapi.fedoraproject.org/f44/pkg/kbd): “Tools for configuring the console (keyboard, virtual terminals, etc.)”.
- coreos-a5bed6ae63 — [kbd-legacy](https://mdapi.fedoraproject.org/f44/pkg/kbd-legacy): “Legacy data for kbd package”.
- coreos-50fb2d29ef — [kbd-misc](https://mdapi.fedoraproject.org/f44/pkg/kbd-misc): “Data for kbd package”.
- coreos-dee40d049d — [kdump-utils](https://mdapi.fedoraproject.org/f44/pkg/kdump-utils): “Kernel crash dump collection utilities”.
- coreos-326325fdeb — [kernel](https://mdapi.fedoraproject.org/f44/pkg/kernel): “The Linux kernel”.
- coreos-38bc5e74c6 — [kernel-core](https://mdapi.fedoraproject.org/f44/pkg/kernel-core): “The Linux kernel”.
- coreos-b6d312d39f — [kernel-modules](https://mdapi.fedoraproject.org/f44/pkg/kernel-modules): “kernel modules to match the core kernel”.
- coreos-88c12220a5 — [kernel-modules-core](https://mdapi.fedoraproject.org/f44/pkg/kernel-modules-core): “Core kernel modules to match the core kernel”.
- coreos-1e6c269b3e — [kexec-tools](https://mdapi.fedoraproject.org/f44/pkg/kexec-tools): “The kexec/kdump userspace component”.
- coreos-e3e024a7cd — [keyutils](https://mdapi.fedoraproject.org/f44/pkg/keyutils): “Linux Key Management Utilities”.
- coreos-d998c35384 — [keyutils-libs](https://mdapi.fedoraproject.org/f44/pkg/keyutils-libs): “Key utilities library”.
- coreos-1683a2267d — [kmod](https://mdapi.fedoraproject.org/f44/pkg/kmod): “Linux kernel module management utilities”.
- coreos-282d72dbe6 — [kmod-libs](https://mdapi.fedoraproject.org/f44/pkg/kmod-libs): “Libraries to handle kernel module loading and unloading”.
- coreos-f1dd45afba — [kmscon](https://mdapi.fedoraproject.org/f44/pkg/kmscon): “Linux KMS/DRM based virtual Console Emulator”.
- coreos-1d36ab3dd1 — [kpartx](https://mdapi.fedoraproject.org/f44/pkg/kpartx): “Partition device manager for device-mapper devices”.
- coreos-8c6ec82169 — [krb5-libs](https://mdapi.fedoraproject.org/f44/pkg/krb5-libs): “The non-admin shared libraries used by Kerberos 5”.
- coreos-c85e9b1c30 — [less](https://mdapi.fedoraproject.org/f44/pkg/less): “A text file browser similar to more, but better”.
- coreos-8263d34f1d — [libacl](https://mdapi.fedoraproject.org/f44/pkg/libacl): “Dynamic library for access control list support”.
- coreos-4ef7703fd1 — [libaio](https://mdapi.fedoraproject.org/f44/pkg/libaio): “Linux-native asynchronous I/O access library”.
- coreos-821b73ea25 — [libarchive](https://mdapi.fedoraproject.org/f44/pkg/libarchive): “A library for handling streaming archive formats”.
- coreos-6d13c759bb — [libassuan](https://mdapi.fedoraproject.org/f44/pkg/libassuan): “GnuPG IPC library”.
- coreos-b7d7832d01 — [libatasmart](https://mdapi.fedoraproject.org/f44/pkg/libatasmart): “ATA S.M.A.R.T. Disk Health Monitoring Library”.
- coreos-917967605f — [libattr](https://mdapi.fedoraproject.org/f44/pkg/libattr): “Dynamic library for extended attribute support”.
- coreos-4959211686 — [libbasicobjects](https://mdapi.fedoraproject.org/f44/pkg/libbasicobjects): “Basic object types for C”.
- coreos-60dc2c2355 — [libblkid](https://mdapi.fedoraproject.org/f44/pkg/libblkid): “Block device ID library”.
- coreos-c1e4e1ff53 — [libblockdev](https://mdapi.fedoraproject.org/f44/pkg/libblockdev): “A library for low-level manipulation with block devices”.
- coreos-41e739c544 — [libblockdev-crypto](https://mdapi.fedoraproject.org/f44/pkg/libblockdev-crypto): “The crypto plugin for the libblockdev library”.
- coreos-333f99c83e — [libblockdev-fs](https://mdapi.fedoraproject.org/f44/pkg/libblockdev-fs): “The FS plugin for the libblockdev library”.
- coreos-8b5913dc95 — [libblockdev-loop](https://mdapi.fedoraproject.org/f44/pkg/libblockdev-loop): “The loop plugin for the libblockdev library”.
- coreos-d576728283 — [libblockdev-mdraid](https://mdapi.fedoraproject.org/f44/pkg/libblockdev-mdraid): “The MD RAID plugin for the libblockdev library”.
- coreos-4ca095c44b — [libblockdev-nvme](https://mdapi.fedoraproject.org/f44/pkg/libblockdev-nvme): “The NVMe plugin for the libblockdev library”.
- coreos-3030ce9cc9 — [libblockdev-part](https://mdapi.fedoraproject.org/f44/pkg/libblockdev-part): “The partitioning plugin for the libblockdev library”.
- coreos-e32ee18a5c — [libblockdev-smart](https://mdapi.fedoraproject.org/f44/pkg/libblockdev-smart): “The smart plugin for the libblockdev library”.
- coreos-5c992ef2e2 — [libblockdev-swap](https://mdapi.fedoraproject.org/f44/pkg/libblockdev-swap): “The swap plugin for the libblockdev library”.
- coreos-0c5d4db3b0 — [libblockdev-utils](https://mdapi.fedoraproject.org/f44/pkg/libblockdev-utils): “A library with utility functions for the libblockdev library”.
- coreos-3cec076745 — [libbpf](https://mdapi.fedoraproject.org/f44/pkg/libbpf): “Libbpf library”.
- coreos-043948a2a4 — [libbsd](https://mdapi.fedoraproject.org/f44/pkg/libbsd): “Library providing BSD-compatible functions for portability”.
- coreos-aea19cfdd0 — [libbytesize](https://mdapi.fedoraproject.org/f44/pkg/libbytesize): “A library for working with sizes in bytes”.
- coreos-9056c714eb — [libcap](https://mdapi.fedoraproject.org/f44/pkg/libcap): “Library for getting and setting POSIX.1e capabilities”.
- coreos-48c5c2c5d3 — [libcap-ng](https://mdapi.fedoraproject.org/f44/pkg/libcap-ng): “Alternate posix capabilities library”.
- coreos-73e20bc8aa — [libcbor](https://mdapi.fedoraproject.org/f44/pkg/libcbor): “A CBOR parsing library”.
- coreos-a2cda6845d — [libcollection](https://mdapi.fedoraproject.org/f44/pkg/libcollection): “Collection data-type for C”.
- coreos-f521326e1b — [libcom_err](https://mdapi.fedoraproject.org/f44/pkg/libcom_err): “Common error description library”.
- coreos-fb1851e122 — [libcurl-minimal](https://mdapi.fedoraproject.org/f44/pkg/libcurl-minimal): “Conservatively configured build of libcurl for minimal installations”.
- coreos-7b6ac84ae2 — [libdaemon](https://mdapi.fedoraproject.org/f44/pkg/libdaemon): “Library for writing UNIX daemons”.
- coreos-e6dff94b57 — [libdhash](https://mdapi.fedoraproject.org/f44/pkg/libdhash): “Dynamic hash table”.
- coreos-926abb8d7c — [libdnf5](https://mdapi.fedoraproject.org/f44/pkg/libdnf5): “Package management library”.
- coreos-a9ba7fad4f — [libdnf5-cli](https://mdapi.fedoraproject.org/f44/pkg/libdnf5-cli): “Library for working with a terminal in a command-line package”.
- coreos-05f802043c — [libdrm](https://mdapi.fedoraproject.org/f44/pkg/libdrm): “Direct Rendering Manager runtime library”.
- coreos-6ac957116a — [libeconf](https://mdapi.fedoraproject.org/f44/pkg/libeconf): “Enhanced config file parser library”.
- coreos-cad673e8c1 — [libedit](https://mdapi.fedoraproject.org/f44/pkg/libedit): “The NetBSD Editline library”.
- coreos-c6dcafbd85 — [libev](https://mdapi.fedoraproject.org/f44/pkg/libev): “High-performance event loop/event model with lots of features”.
- coreos-eedabdc72e — [libevent](https://mdapi.fedoraproject.org/f44/pkg/libevent): “Abstract asynchronous event notification library”.
- coreos-a8cc8521ed — [libfdisk](https://mdapi.fedoraproject.org/f44/pkg/libfdisk): “Partitioning library for fdisk-like programs”.
- coreos-a004699dae — [libffi](https://mdapi.fedoraproject.org/f44/pkg/libffi): “A portable foreign function interface library”.
- coreos-a14066db74 — [libfido2](https://mdapi.fedoraproject.org/f44/pkg/libfido2): “FIDO2 library”.
- coreos-ab16b6d2cb — [libgcc](https://mdapi.fedoraproject.org/f44/pkg/libgcc): “GCC version 16 shared support library”.
- coreos-f95ed6d172 — [libgcrypt](https://mdapi.fedoraproject.org/f44/pkg/libgcrypt): “A general-purpose cryptography library”.
- coreos-346b67e420 — [libgpg-error](https://mdapi.fedoraproject.org/f44/pkg/libgpg-error): “Library for error values used by GnuPG components”.
- coreos-ab4a26ab6b — [libgudev](https://mdapi.fedoraproject.org/f44/pkg/libgudev): “GObject-based wrapper library for libudev”.
- coreos-fa5e763620 — [libibverbs](https://mdapi.fedoraproject.org/f44/pkg/libibverbs): “A library and drivers for direct userspace use of RDMA”.
- coreos-3fa4ccdd46 — [libicu](https://mdapi.fedoraproject.org/f44/pkg/libicu): “International Components for Unicode - libraries”.
- coreos-14fa5e3611 — [libidn2](https://mdapi.fedoraproject.org/f44/pkg/libidn2): “Library to support IDNA2008 internationalized domain names”.
- coreos-4945c218a9 — [libini_config](https://mdapi.fedoraproject.org/f44/pkg/libini_config): “INI file parser for C”.
- coreos-9a880c8735 — [libipa_hbac](https://mdapi.fedoraproject.org/f44/pkg/libipa_hbac): “FreeIPA HBAC Evaluator library”.
- coreos-a28ae2cc05 — [libjose](https://mdapi.fedoraproject.org/f44/pkg/libjose): “Library implementing JSON Object Signing and Encryption”.
- coreos-6af48df928 — [libkcapi](https://mdapi.fedoraproject.org/f44/pkg/libkcapi): “User space interface to the Linux Kernel Crypto API”.
- coreos-b7c7dd5ec4 — [libkcapi-hasher](https://mdapi.fedoraproject.org/f44/pkg/libkcapi-hasher): “Common libkcapi hashing application”.
- coreos-b7401506a2 — [libkcapi-hmaccalc](https://mdapi.fedoraproject.org/f44/pkg/libkcapi-hmaccalc): “Drop-in replacements for hmaccalc provided by the libkcapi package”.
- coreos-055a3b9fef — [libksba](https://mdapi.fedoraproject.org/f44/pkg/libksba): “CMS and X.509 library”.
- coreos-92047da192 — [liblastlog2](https://mdapi.fedoraproject.org/f44/pkg/liblastlog2): “lastlog database library and PAM module”.
- coreos-ef7bf99e7a — [libldb](https://mdapi.fedoraproject.org/f44/pkg/libldb): “A schema-less, ldap like, API and database”.
- coreos-3cb9cf3a3e — [libluksmeta](https://mdapi.fedoraproject.org/f44/pkg/libluksmeta): “Library for storing small metadata in the LUKSv1 header”.
- coreos-b4c62ff53f — [libmaxminddb](https://mdapi.fedoraproject.org/f44/pkg/libmaxminddb): “C library for reading MaxMind DB files”.
- coreos-b28d41df65 — [libmd](https://mdapi.fedoraproject.org/f44/pkg/libmd): “Library that provides message digest functions from BSD systems”.
- coreos-cc14f4c162 — [libmnl](https://mdapi.fedoraproject.org/f44/pkg/libmnl): “Minimalistic Netlink user-space library”.
- coreos-edd6e2ec25 — [libmodulemd](https://mdapi.fedoraproject.org/f44/pkg/libmodulemd): “Module metadata manipulation library”.
- coreos-0d29cd0af1 — [libmount](https://mdapi.fedoraproject.org/f44/pkg/libmount): “Device mounting library”.
- coreos-d95883bdfb — [libndp](https://mdapi.fedoraproject.org/f44/pkg/libndp): “Library for Neighbor Discovery Protocol”.
- coreos-a7c6611cac — [libnet](https://mdapi.fedoraproject.org/f44/pkg/libnet): “C library for portable packet creation and injection”.
- coreos-45652e9293 — [libnetfilter_conntrack](https://mdapi.fedoraproject.org/f44/pkg/libnetfilter_conntrack): “Netfilter conntrack userspace library”.
- coreos-c78a311472 — [libnfnetlink](https://mdapi.fedoraproject.org/f44/pkg/libnfnetlink): “Netfilter netlink userspace library”.
- coreos-281e5393f6 — [libnfsidmap](https://mdapi.fedoraproject.org/f44/pkg/libnfsidmap): “NFSv4 User and Group ID Mapping Library”.
- coreos-d398b5d688 — [libnftnl](https://mdapi.fedoraproject.org/f44/pkg/libnftnl): “Library for low-level interaction with nftables Netlink's API over libmnl”.
- coreos-0b19996182 — [libnghttp2](https://mdapi.fedoraproject.org/f44/pkg/libnghttp2): “A library implementing the HTTP/2 protocol”.
- coreos-58102caf82 — [libnl3](https://mdapi.fedoraproject.org/f44/pkg/libnl3): “Convenience library for kernel netlink sockets”.
- coreos-ab1054621d — [libnl3-cli](https://mdapi.fedoraproject.org/f44/pkg/libnl3-cli): “Command line interface utils for libnl3”.
- coreos-23fe02b945 — [libnsl2](https://mdapi.fedoraproject.org/f44/pkg/libnsl2): “Public client interface library for NIS(YP) and NIS+”.
- coreos-73d8160803 — [libnvme](https://mdapi.fedoraproject.org/f44/pkg/libnvme): “Linux-native nvme device management library”.
- coreos-75efd9fd04 — [libpath_utils](https://mdapi.fedoraproject.org/f44/pkg/libpath_utils): “Filesystem Path Utilities”.
- coreos-e63fd8356d — [libpathrs](https://mdapi.fedoraproject.org/f44/pkg/libpathrs): “C-friendly API to make path resolution safer on Linux”.
- coreos-f809c8bde9 — [libpcap](https://mdapi.fedoraproject.org/f44/pkg/libpcap): “A system-independent interface for user-level packet capture”.
- coreos-f924a87673 — [libpciaccess](https://mdapi.fedoraproject.org/f44/pkg/libpciaccess): “PCI access library”.
- coreos-893e6539c7 — [libpkgconf](https://mdapi.fedoraproject.org/f44/pkg/libpkgconf): “Backend library for pkgconf”.
- coreos-a52a237b76 — [libpsl](https://mdapi.fedoraproject.org/f44/pkg/libpsl): “C library for the Publix Suffix List”.
- coreos-022f5dc625 — [libpwquality](https://mdapi.fedoraproject.org/f44/pkg/libpwquality): “A library for password generation and password quality checking”.
- coreos-de37380759 — [libref_array](https://mdapi.fedoraproject.org/f44/pkg/libref_array): “A refcounted array for C”.
- coreos-84b1e0dd30 — [librepo](https://mdapi.fedoraproject.org/f44/pkg/librepo): “Repodata downloading library”.
- coreos-bd48096336 — [libreport-filesystem](https://mdapi.fedoraproject.org/f44/pkg/libreport-filesystem): “Filesystem layout for libreport”.
- coreos-1be2d8a6c5 — [libseccomp](https://mdapi.fedoraproject.org/f44/pkg/libseccomp): “Enhanced seccomp library”.
- coreos-aab14ef4e9 — [libselinux](https://mdapi.fedoraproject.org/f44/pkg/libselinux): “SELinux library and simple utilities”.
- coreos-04d5503bb0 — [libselinux-utils](https://mdapi.fedoraproject.org/f44/pkg/libselinux-utils): “SELinux libselinux utilities”.
- coreos-8c5b17f010 — [libsemanage](https://mdapi.fedoraproject.org/f44/pkg/libsemanage): “SELinux binary policy manipulation library”.
- coreos-a76fdc3263 — [libsepol](https://mdapi.fedoraproject.org/f44/pkg/libsepol): “SELinux binary policy manipulation library”.
- coreos-1892e5fd2a — [libslirp](https://mdapi.fedoraproject.org/f44/pkg/libslirp): “A general purpose TCP-IP emulator”.
- coreos-676403c216 — [libsmartcols](https://mdapi.fedoraproject.org/f44/pkg/libsmartcols): “Formatting library for ls-like programs”.
- coreos-3bb570feb8 — [libsmbclient](https://mdapi.fedoraproject.org/f44/pkg/libsmbclient): “The SMB client library”.
- coreos-52c3ed2f3d — [libsolv](https://mdapi.fedoraproject.org/f44/pkg/libsolv): “Package dependency solver”.
- coreos-2fb71de7a3 — [libss](https://mdapi.fedoraproject.org/f44/pkg/libss): “Command line interface parsing library”.
- coreos-d0697667f1 — [libsss_certmap](https://mdapi.fedoraproject.org/f44/pkg/libsss_certmap): “SSSD Certificate Mapping Library”.
- coreos-96f08ad18e — [libsss_idmap](https://mdapi.fedoraproject.org/f44/pkg/libsss_idmap): “FreeIPA Idmap library”.
- coreos-0d9dcfc39b — [libsss_nss_idmap](https://mdapi.fedoraproject.org/f44/pkg/libsss_nss_idmap): “Library for SID and certificate based lookups”.
- coreos-6ef76a82e4 — [libsss_sudo](https://mdapi.fedoraproject.org/f44/pkg/libsss_sudo): “A library to allow communication between SUDO and SSSD”.
- coreos-0f5b1231bb — [libstdc++](https://mdapi.fedoraproject.org/f44/pkg/libstdc%2B%2B): “GNU Standard C++ Library”.
- coreos-3b7580acf4 — [libtalloc](https://mdapi.fedoraproject.org/f44/pkg/libtalloc): “The talloc library”.
- coreos-0e95ec4ca3 — [libtasn1](https://mdapi.fedoraproject.org/f44/pkg/libtasn1): “The ASN.1 library used in GNUTLS”.
- coreos-6d2bb63d4b — [libtdb](https://mdapi.fedoraproject.org/f44/pkg/libtdb): “The tdb library”.
- coreos-cb6be70709 — [libteam](https://mdapi.fedoraproject.org/f44/pkg/libteam): “Library for controlling team network device”.
- coreos-c5e7e717db — [libtevent](https://mdapi.fedoraproject.org/f44/pkg/libtevent): “The tevent library”.
- coreos-53ec920a31 — [libtextstyle](https://mdapi.fedoraproject.org/f44/pkg/libtextstyle): “Text styling library”.
- coreos-0b7cc5dc27 — [libtirpc](https://mdapi.fedoraproject.org/f44/pkg/libtirpc): “Transport Independent RPC Library”.
- coreos-c68c8562b0 — [libtool-ltdl](https://mdapi.fedoraproject.org/f44/pkg/libtool-ltdl): “Runtime libraries for GNU Libtool Dynamic Module Loader”.
- coreos-5deb1d5633 — [libtsm](https://mdapi.fedoraproject.org/f44/pkg/libtsm): “DEC-VT terminal emulator state machine”.
- coreos-11fcbb532d — [libudisks2](https://mdapi.fedoraproject.org/f44/pkg/libudisks2): “Dynamic library to access the udisksd daemon”.
- coreos-be9d1800e3 — [libunistring](https://mdapi.fedoraproject.org/f44/pkg/libunistring): “GNU Unicode string library”.
- coreos-848b999f98 — [libusb1](https://mdapi.fedoraproject.org/f44/pkg/libusb1): “Library for accessing USB devices”.
- coreos-e460aa6f3b — [libuuid](https://mdapi.fedoraproject.org/f44/pkg/libuuid): “Universally unique ID library”.
- coreos-be20531a2b — [libuv](https://mdapi.fedoraproject.org/f44/pkg/libuv): “Platform layer for node.js”.
- coreos-01f2ad4d77 — [libverto](https://mdapi.fedoraproject.org/f44/pkg/libverto): “Main loop abstraction library”.
- coreos-b862ca061c — [libverto-libev](https://mdapi.fedoraproject.org/f44/pkg/libverto-libev): “libev module for libverto”.
- coreos-e4df18fb84 — [libwbclient](https://mdapi.fedoraproject.org/f44/pkg/libwbclient): “The winbind client library”.
- coreos-81c4038523 — [libxcrypt](https://mdapi.fedoraproject.org/f44/pkg/libxcrypt): “Extended crypt library for descrypt, md5crypt, bcrypt, and others”.
- coreos-aace2002ff — [libxkbcommon](https://mdapi.fedoraproject.org/f44/pkg/libxkbcommon): “X.Org X11 XKB parsing library”.
- coreos-56797b733c — [libxml2](https://mdapi.fedoraproject.org/f44/pkg/libxml2): “Library providing XML and HTML support”.
- coreos-62ef4089d6 — [libxmlb](https://mdapi.fedoraproject.org/f44/pkg/libxmlb): “Library for querying compressed XML metadata”.
- coreos-0eeca9c8f8 — [libyaml](https://mdapi.fedoraproject.org/f44/pkg/libyaml): “YAML 1.1 parser and emitter written in C”.
- coreos-b45e2d1b15 — [libzstd](https://mdapi.fedoraproject.org/f44/pkg/libzstd): “Zstd shared library”.
- coreos-0c6843c143 — [linux-firmware](https://mdapi.fedoraproject.org/f44/pkg/linux-firmware): “Firmware files used by the Linux kernel”.
- coreos-d431bf68da — [linux-firmware-whence](https://mdapi.fedoraproject.org/f44/pkg/linux-firmware-whence): “WHENCE License file”.
- coreos-1438f778ed — [lld18-libs](https://mdapi.fedoraproject.org/f44/pkg/lld18-libs): “LLD shared libraries”.
- coreos-85b0ab81dd — [llvm18-libs](https://mdapi.fedoraproject.org/f44/pkg/llvm18-libs): “LLVM shared libraries”.
- coreos-f3c264c83c — [lmdb-libs](https://mdapi.fedoraproject.org/f44/pkg/lmdb-libs): “Shared libraries for lmdb”.
- coreos-746d859138 — [logrotate](https://mdapi.fedoraproject.org/f44/pkg/logrotate): “Rotates, compresses, removes and mails system log files”.
- coreos-0753fbb02a — [lsof](https://mdapi.fedoraproject.org/f44/pkg/lsof): “A utility which lists open files on a Linux/UNIX system”.
- coreos-d1d8ff501d — [lua-libs](https://mdapi.fedoraproject.org/f44/pkg/lua-libs): “Libraries for lua”.
- coreos-281cb669f1 — [luksmeta](https://mdapi.fedoraproject.org/f44/pkg/luksmeta): “Utility for storing small metadata in the LUKSv1 header”.
- coreos-c54f1d6858 — [lvm2](https://mdapi.fedoraproject.org/f44/pkg/lvm2): “Userland logical volume management tools”.
- coreos-8fc8823a53 — [lvm2-libs](https://mdapi.fedoraproject.org/f44/pkg/lvm2-libs): “Shared libraries for lvm2”.
- coreos-b6c1634ac1 — [lz4-libs](https://mdapi.fedoraproject.org/f44/pkg/lz4-libs): “Libaries for lz4”.
- coreos-51667a6761 — [lzo](https://mdapi.fedoraproject.org/f44/pkg/lzo): “Data compression library with very fast (de)compression”.
- coreos-190f07f37b — [makedumpfile](https://mdapi.fedoraproject.org/f44/pkg/makedumpfile): “make a small dumpfile of kdump”.
- coreos-04922e12b0 — [mdadm](https://mdapi.fedoraproject.org/f44/pkg/mdadm): “The mdadm program controls Linux md devices (software RAID arrays)”.
- coreos-cb9ae41f08 — [microcode_ctl](https://mdapi.fedoraproject.org/f44/pkg/microcode_ctl): “Tool to transform and deploy CPU microcode update for x86”.
- coreos-8880a5b21d — [moby-engine](https://mdapi.fedoraproject.org/f44/pkg/moby-engine): “The open-source application container engine”.
- coreos-cc816199e8 — [moby-filesystem](https://mdapi.fedoraproject.org/f44/pkg/moby-filesystem): “Filesystem package for the Moby/Docker stack”.
- coreos-3be19d5365 — [mokutil](https://mdapi.fedoraproject.org/f44/pkg/mokutil): “Tool to manage UEFI Secure Boot MoK Keys”.
- coreos-c9e19e83cb — [mpfr](https://mdapi.fedoraproject.org/f44/pkg/mpfr): “C library for multiple-precision floating-point computations”.
- coreos-565b5cc910 — [nano](https://mdapi.fedoraproject.org/f44/pkg/nano): “A small text editor”.
- coreos-5d2ee97627 — [nano-default-editor](https://mdapi.fedoraproject.org/f44/pkg/nano-default-editor): “Sets GNU nano as the default editor”.
- coreos-645a706559 — [ncurses](https://mdapi.fedoraproject.org/f44/pkg/ncurses): “Ncurses support utilities”.
- coreos-9c32a751d6 — [ncurses-base](https://mdapi.fedoraproject.org/f44/pkg/ncurses-base): “Descriptions of common terminals”.
- coreos-a0acaed055 — [ncurses-libs](https://mdapi.fedoraproject.org/f44/pkg/ncurses-libs): “Ncurses libraries”.
- coreos-f250f37b9f — [net-tools](https://mdapi.fedoraproject.org/f44/pkg/net-tools): “Basic networking tools”.
- coreos-2cc57136b5 — [netavark](https://mdapi.fedoraproject.org/f44/pkg/netavark): “OCI network stack”.
- coreos-399852e08d — [nettle](https://mdapi.fedoraproject.org/f44/pkg/nettle): “A low-level cryptographic library”.
- coreos-9763d07ebf — [newt](https://mdapi.fedoraproject.org/f44/pkg/newt): “A library for text mode user interfaces”.
- coreos-56b6b697cc — [nfs-client-utils](https://mdapi.fedoraproject.org/f44/pkg/nfs-client-utils): “NFS client utilities”.
- coreos-38cd844153 — [nfs-common-utils](https://mdapi.fedoraproject.org/f44/pkg/nfs-common-utils): “Common NFS utilities”.
- coreos-b175ff7ae3 — [nfsv3-client-utils](https://mdapi.fedoraproject.org/f44/pkg/nfsv3-client-utils): “NFSv3 client utilities”.
- coreos-f687fcd749 — [nfsv4-client-utils](https://mdapi.fedoraproject.org/f44/pkg/nfsv4-client-utils): “NFSv4 client utilities”.
- coreos-aa9f98d21f — [nftables](https://mdapi.fedoraproject.org/f44/pkg/nftables): “Netfilter Tables userspace utilities”.
- coreos-160df5d64d — [nftables-services](https://mdapi.fedoraproject.org/f44/pkg/nftables-services): “Systemd service for nftables”.
- coreos-d70ab2ad1a — [ngtcp2](https://mdapi.fedoraproject.org/f44/pkg/ngtcp2): “Implementation of RFC 9000 QUIC protocol”.
- coreos-d58a8bc037 — [ngtcp2-crypto-gnutls](https://mdapi.fedoraproject.org/f44/pkg/ngtcp2-crypto-gnutls): “The ngtcp2 GnuTLS crypto provider”.
- coreos-455df95933 — [nmstate](https://mdapi.fedoraproject.org/f44/pkg/nmstate): “Declarative network manager API”.
- coreos-9c8350f428 — [npth](https://mdapi.fedoraproject.org/f44/pkg/npth): “The New GNU Portable Threads library”.
- coreos-19e9ebafb3 — [nspr](https://mdapi.fedoraproject.org/f44/pkg/nspr): “Netscape Portable Runtime”.
- coreos-b20fb812e7 — [nss](https://mdapi.fedoraproject.org/f44/pkg/nss): “Network Security Services”.
- coreos-0cd1d6e7a0 — [nss-altfiles](https://mdapi.fedoraproject.org/f44/pkg/nss-altfiles): “NSS module to look up from files in /usr/lib as”.
- coreos-012c5954c2 — [nss-softokn](https://mdapi.fedoraproject.org/f44/pkg/nss-softokn): “Network Security Services Softoken Module”.
- coreos-4471e3cb6e — [nss-softokn-freebl](https://mdapi.fedoraproject.org/f44/pkg/nss-softokn-freebl): “Freebl library for the Network Security Services”.
- coreos-58f9c8f7a3 — [nss-sysinit](https://mdapi.fedoraproject.org/f44/pkg/nss-sysinit): “System NSS Initialization”.
- coreos-37b93df644 — [nss-util](https://mdapi.fedoraproject.org/f44/pkg/nss-util): “Network Security Services Utilities Library”.
- coreos-4ca1940a79 — [numactl](https://mdapi.fedoraproject.org/f44/pkg/numactl): “Library for tuning for Non Uniform Memory Access machines”.
- coreos-72f6221f7c — [numactl-libs](https://mdapi.fedoraproject.org/f44/pkg/numactl-libs): “libnuma libraries”.
- coreos-aef7954f0c — [numad](https://mdapi.fedoraproject.org/f44/pkg/numad): “NUMA user daemon”.
- coreos-480c7392f9 — [nvidia-gpu-firmware](https://mdapi.fedoraproject.org/f44/pkg/nvidia-gpu-firmware): “Firmware for NVIDIA GPUs”.
- coreos-794a26732a — [nvme-cli](https://mdapi.fedoraproject.org/f44/pkg/nvme-cli): “NVMe management command line interface”.
- coreos-be18a3c4e1 — [oniguruma](https://mdapi.fedoraproject.org/f44/pkg/oniguruma): “Regular expressions library”.
- coreos-b02f7155aa — [openldap](https://mdapi.fedoraproject.org/f44/pkg/openldap): “LDAP support libraries”.
- coreos-31d39416fb — [openssh](https://mdapi.fedoraproject.org/f44/pkg/openssh): “An open source implementation of SSH protocol version 2”.
- coreos-38eb1b89ac — [openssh-clients](https://mdapi.fedoraproject.org/f44/pkg/openssh-clients): “An open source SSH client applications”.
- coreos-dd3aa38850 — [openssh-server](https://mdapi.fedoraproject.org/f44/pkg/openssh-server): “An open source SSH server daemon”.
- coreos-87d2e8ffa5 — [openssl](https://mdapi.fedoraproject.org/f44/pkg/openssl): “Utilities from the general purpose cryptography library with TLS implementation”.
- coreos-e81d659198 — [openssl-libs](https://mdapi.fedoraproject.org/f44/pkg/openssl-libs): “A general purpose cryptography library with TLS implementation”.
- coreos-c12d51b4ea — [os-prober](https://mdapi.fedoraproject.org/f44/pkg/os-prober): “Probes disks on the system for installed operating systems”.
- coreos-077b3e7ce1 — [ostree](https://mdapi.fedoraproject.org/f44/pkg/ostree): “Tool for managing bootable, immutable filesystem trees”.
- coreos-ba42334b3e — [ostree-libs](https://mdapi.fedoraproject.org/f44/pkg/ostree-libs): “C shared libraries ostree”.
- coreos-e6c0eebe08 — [p11-kit](https://mdapi.fedoraproject.org/f44/pkg/p11-kit): “Library for loading and sharing PKCS#11 modules”.
- coreos-92df2ba491 — [p11-kit-trust](https://mdapi.fedoraproject.org/f44/pkg/p11-kit-trust): “System trust module from p11-kit”.
- coreos-a45eaaff04 — [pam](https://mdapi.fedoraproject.org/f44/pkg/pam): “An extensible library which provides authentication for applications”.
- coreos-a2ce607c7a — [pam-libs](https://mdapi.fedoraproject.org/f44/pkg/pam-libs): “Shared libraries of the PAM package”.
- coreos-b4f046d707 — [passim-libs](https://mdapi.fedoraproject.org/f44/pkg/passim-libs): “Local caching server library”.
- coreos-718cd069dd — [passt](https://mdapi.fedoraproject.org/f44/pkg/passt): “User-mode networking daemons for virtual machines and namespaces”.
- coreos-0cfcf786b7 — [passt-selinux](https://mdapi.fedoraproject.org/f44/pkg/passt-selinux): “SELinux support for passt and pasta”.
- coreos-873284e269 — [pciutils](https://mdapi.fedoraproject.org/f44/pkg/pciutils): “PCI bus related utilities”.
- coreos-cf77df5255 — [pciutils-libs](https://mdapi.fedoraproject.org/f44/pkg/pciutils-libs): “Linux PCI library”.
- coreos-a8f332b99f — [pcre2](https://mdapi.fedoraproject.org/f44/pkg/pcre2): “Perl-compatible regular expression library”.
- coreos-303f2a1f13 — [pcre2-syntax](https://mdapi.fedoraproject.org/f44/pkg/pcre2-syntax): “Documentation for PCRE2 regular expressions”.
- coreos-24f2e0d3bb — [pigz](https://mdapi.fedoraproject.org/f44/pkg/pigz): “Parallel implementation of gzip”.
- coreos-b0116c047d — [pkgconf](https://mdapi.fedoraproject.org/f44/pkg/pkgconf): “Package compiler and linker metadata toolkit”.
- coreos-0edb8355bc — [pkgconf-m4](https://mdapi.fedoraproject.org/f44/pkg/pkgconf-m4): “m4 macros for pkgconf”.
- coreos-24df94462d — [pkgconf-pkg-config](https://mdapi.fedoraproject.org/f44/pkg/pkgconf-pkg-config): “pkgconf shim to provide /usr/bin/pkg-config”.
- coreos-7a42a4252b — [podman](https://mdapi.fedoraproject.org/f44/pkg/podman): “Manage Pods, Containers and Container Images”.
- coreos-265963a9c7 — [podman-sequoia](https://mdapi.fedoraproject.org/f44/pkg/podman-sequoia): “Polyfill to use Sequoia as a signing backend for containers”.
- coreos-dcbf463472 — [policycoreutils](https://mdapi.fedoraproject.org/f44/pkg/policycoreutils): “SELinux policy core utilities”.
- coreos-4c386ca1d0 — [polkit](https://mdapi.fedoraproject.org/f44/pkg/polkit): “An authorization framework”.
- coreos-22c603a062 — [polkit-libs](https://mdapi.fedoraproject.org/f44/pkg/polkit-libs): “Libraries for polkit”.
- coreos-7bf15684da — [popt](https://mdapi.fedoraproject.org/f44/pkg/popt): “C library for parsing command line parameters”.
- coreos-5cda2447d6 — [procps-ng](https://mdapi.fedoraproject.org/f44/pkg/procps-ng): “System and process monitoring utilities”.
- coreos-b19485c9b6 — [protobuf-c](https://mdapi.fedoraproject.org/f44/pkg/protobuf-c): “C bindings for Google's Protocol Buffers”.
- coreos-7909659263 — [psmisc](https://mdapi.fedoraproject.org/f44/pkg/psmisc): “Utilities for managing processes on your system”.
- coreos-79d4269657 — [publicsuffix-list-dafsa](https://mdapi.fedoraproject.org/f44/pkg/publicsuffix-list-dafsa): “Cross-vendor public domain suffix database in DAFSA form”.
- coreos-255c97768a — [qed-firmware](https://mdapi.fedoraproject.org/f44/pkg/qed-firmware): “Firmware for Marvell FastLinQ adapters family”.
- coreos-8fa59ebbf6 — [rdma-core-common](https://mdapi.fedoraproject.org/f44/pkg/rdma-core-common): “Common files for all subpackages of rdma-core”.
- coreos-9ab2d1413a — [readline](https://mdapi.fedoraproject.org/f44/pkg/readline): “A library for editing typed command lines”.
- coreos-18f05f8b8b — [rpcbind](https://mdapi.fedoraproject.org/f44/pkg/rpcbind): “Universal Addresses to RPC Program Number Mapper”.
- coreos-95e253402f — [rpm](https://mdapi.fedoraproject.org/f44/pkg/rpm): “The RPM package management system”.
- coreos-fb6c1f8e77 — [rpm-libs](https://mdapi.fedoraproject.org/f44/pkg/rpm-libs): “Libraries for manipulating RPM packages”.
- coreos-1ea6d98ae7 — [rpm-ostree](https://mdapi.fedoraproject.org/f44/pkg/rpm-ostree): “Hybrid image/package system”.
- coreos-d7ea0db557 — [rpm-ostree-libs](https://mdapi.fedoraproject.org/f44/pkg/rpm-ostree-libs): “Shared library for rpm-ostree”.
- coreos-faa5c4805d — [rpm-plugin-selinux](https://mdapi.fedoraproject.org/f44/pkg/rpm-plugin-selinux): “Rpm plugin for SELinux functionality”.
- coreos-cbf670ba8d — [rpm-sequoia](https://mdapi.fedoraproject.org/f44/pkg/rpm-sequoia): “Implementation of the RPM PGP interface using Sequoia”.
- coreos-39c196795b — [rsync](https://mdapi.fedoraproject.org/f44/pkg/rsync): “A program for synchronizing files over a network”.
- coreos-b2ce7a8912 — [runc](https://mdapi.fedoraproject.org/f44/pkg/runc): “CLI tool for spawning and running containers according to the”.
- coreos-38ac7e6cf7 — [samba-client-libs](https://mdapi.fedoraproject.org/f44/pkg/samba-client-libs): “Samba client libraries”.
- coreos-103a7d5e4f — [samba-common](https://mdapi.fedoraproject.org/f44/pkg/samba-common): “Files used by both Samba servers and clients”.
- coreos-805c8a963a — [samba-core-libs](https://mdapi.fedoraproject.org/f44/pkg/samba-core-libs): “Samba core libraries”.
- coreos-401d9dbfe3 — [samba-ndr-libs](https://mdapi.fedoraproject.org/f44/pkg/samba-ndr-libs): “Samba NDR libraries”.
- coreos-b31881df33 — [sdbus-cpp](https://mdapi.fedoraproject.org/f44/pkg/sdbus-cpp): “High-level C++ D-Bus library”.
- coreos-52c44d5b15 — [sed](https://mdapi.fedoraproject.org/f44/pkg/sed): “A GNU stream text editor”.
- coreos-b3c56ff9a3 — [selinux-policy](https://mdapi.fedoraproject.org/f44/pkg/selinux-policy): “SELinux policy configuration”.
- coreos-3284fb8e87 — [selinux-policy-targeted](https://mdapi.fedoraproject.org/f44/pkg/selinux-policy-targeted): “SELinux targeted policy”.
- coreos-34c88d127c — [setup](https://mdapi.fedoraproject.org/f44/pkg/setup): “A set of system configuration and setup files”.
- coreos-1c70d5d11f — [sg3_utils](https://mdapi.fedoraproject.org/f44/pkg/sg3_utils): “Utilities for devices that use SCSI command sets”.
- coreos-e70eab6188 — [sg3_utils-libs](https://mdapi.fedoraproject.org/f44/pkg/sg3_utils-libs): “Shared library for sg3_utils”.
- coreos-1567722810 — [shadow-utils](https://mdapi.fedoraproject.org/f44/pkg/shadow-utils): “Utilities for managing accounts and shadow password files”.
- coreos-304ad867dc — [shadow-utils-subid](https://mdapi.fedoraproject.org/f44/pkg/shadow-utils-subid): “A library to manage subordinate uid and gid ranges”.
- coreos-0e676da806 — [shared-mime-info](https://mdapi.fedoraproject.org/f44/pkg/shared-mime-info): “Shared MIME information database”.
- coreos-63a1b30c11 — [shim-x64](https://mdapi.fedoraproject.org/f44/pkg/shim-x64): “First-stage UEFI bootloader”.
- coreos-560b5a58a8 — [skopeo](https://mdapi.fedoraproject.org/f44/pkg/skopeo): “Inspect container images and repositories on registries”.
- coreos-769ee8dae5 — [slang](https://mdapi.fedoraproject.org/f44/pkg/slang): “Shared library for the S-Lang extension language”.
- coreos-4bc1509a79 — [slirp4netns](https://mdapi.fedoraproject.org/f44/pkg/slirp4netns): “slirp for network namespaces”.
- coreos-ae19774f50 — [snappy](https://mdapi.fedoraproject.org/f44/pkg/snappy): “Fast compression and decompression library”.
- coreos-227ec7b5e5 — [socat](https://mdapi.fedoraproject.org/f44/pkg/socat): “Bidirectional data relay between two data channels ('netcat++')”.
- coreos-b0dcdb9cf0 — [spdlog](https://mdapi.fedoraproject.org/f44/pkg/spdlog): “Super fast C++ logging library”.
- coreos-c24a74c989 — [sqlite-libs](https://mdapi.fedoraproject.org/f44/pkg/sqlite-libs): “Shared library for the sqlite3 embeddable SQL database engine.”.
- coreos-a7f60be368 — [squashfs-tools](https://mdapi.fedoraproject.org/f44/pkg/squashfs-tools): “Utility for the creation of squashfs filesystems”.
- coreos-040648dab5 — [sssd-ad](https://mdapi.fedoraproject.org/f44/pkg/sssd-ad): “The AD back end of the SSSD”.
- coreos-1816e78740 — [sssd-client](https://mdapi.fedoraproject.org/f44/pkg/sssd-client): “SSSD Client libraries for NSS and PAM”.
- coreos-cda95a848b — [sssd-common](https://mdapi.fedoraproject.org/f44/pkg/sssd-common): “Common files for the SSSD”.
- coreos-3cf84ce108 — [sssd-common-pac](https://mdapi.fedoraproject.org/f44/pkg/sssd-common-pac): “Common files needed for supporting PAC processing”.
- coreos-36c59c224a — [sssd-ipa](https://mdapi.fedoraproject.org/f44/pkg/sssd-ipa): “The IPA back end of the SSSD”.
- coreos-be9e46142a — [sssd-krb5](https://mdapi.fedoraproject.org/f44/pkg/sssd-krb5): “The Kerberos authentication back end for the SSSD”.
- coreos-983276acd3 — [sssd-krb5-common](https://mdapi.fedoraproject.org/f44/pkg/sssd-krb5-common): “SSSD helpers needed for Kerberos and GSSAPI authentication”.
- coreos-1bdc71dae5 — [sssd-ldap](https://mdapi.fedoraproject.org/f44/pkg/sssd-ldap): “The LDAP back end of the SSSD”.
- coreos-0a768fb5ab — [sssd-nfs-idmap](https://mdapi.fedoraproject.org/f44/pkg/sssd-nfs-idmap): “SSSD plug-in for NFSv4 rpc.idmapd”.
- coreos-34ed8ccb6e — [stalld](https://mdapi.fedoraproject.org/f44/pkg/stalld): “Daemon that finds starving tasks and gives them a temporary”.
- coreos-ffc8d72bcf — [sudo](https://mdapi.fedoraproject.org/f44/pkg/sudo): “Allows restricted root access for specified users”.
- coreos-50e2bf1471 — [systemd](https://mdapi.fedoraproject.org/f44/pkg/systemd): “System and Service Manager”.
- coreos-cd7ea86f74 — [systemd-container](https://mdapi.fedoraproject.org/f44/pkg/systemd-container): “Tools for containers and VMs”.
- coreos-df09839d3a — [systemd-libs](https://mdapi.fedoraproject.org/f44/pkg/systemd-libs): “systemd libraries”.
- coreos-e515555fca — [systemd-pam](https://mdapi.fedoraproject.org/f44/pkg/systemd-pam): “systemd PAM module”.
- coreos-7aa532688c — [systemd-resolved](https://mdapi.fedoraproject.org/f44/pkg/systemd-resolved): “Network Name Resolution manager”.
- coreos-3bce7fb26f — [systemd-shared](https://mdapi.fedoraproject.org/f44/pkg/systemd-shared): “Internal systemd shared library”.
- coreos-89638e5403 — [systemd-sysusers](https://mdapi.fedoraproject.org/f44/pkg/systemd-sysusers): “systemd-sysusers program”.
- coreos-92a1f8c33e — [systemd-udev](https://mdapi.fedoraproject.org/f44/pkg/systemd-udev): “Rule-based device node and kernel event manager”.
- coreos-b48d271d11 — [tar](https://mdapi.fedoraproject.org/f44/pkg/tar): “GNU file archiving program”.
- coreos-ae1c228ef2 — [teamd](https://mdapi.fedoraproject.org/f44/pkg/teamd): “Team network device control daemon”.
- coreos-2daeff0083 — [tini-static](https://mdapi.fedoraproject.org/f44/pkg/tini-static): “Standalone static build of tini”.
- coreos-b3cec3d0b2 — [toolbox](https://mdapi.fedoraproject.org/f44/pkg/toolbox): “Tool for interactive command line environments on Linux”.
- coreos-63dca81f51 — [tpm2-tools](https://mdapi.fedoraproject.org/f44/pkg/tpm2-tools): “A bunch of TPM testing toolS build upon tpm2-tss”.
- coreos-770425e9bc — [tpm2-tss](https://mdapi.fedoraproject.org/f44/pkg/tpm2-tss): “TPM2.0 Software Stack”.
- coreos-967696c7f6 — [tpm2-tss-fapi](https://mdapi.fedoraproject.org/f44/pkg/tpm2-tss-fapi): “High-level TPM2.0 Software Stack”.
- coreos-a8dbc728a9 — [tree](https://mdapi.fedoraproject.org/f44/pkg/tree): “File system tree viewer”.
- coreos-b26e3ddcb0 — [tzdata](https://mdapi.fedoraproject.org/f44/pkg/tzdata): “Timezone data”.
- coreos-57090322dd — [udisks2](https://mdapi.fedoraproject.org/f44/pkg/udisks2): “Disk Manager”.
- coreos-08ece770c2 — [userspace-rcu](https://mdapi.fedoraproject.org/f44/pkg/userspace-rcu): “RCU (read-copy-update) implementation in user-space”.
- coreos-44726e1d79 — [util-linux](https://mdapi.fedoraproject.org/f44/pkg/util-linux): “Collection of basic system utilities”.
- coreos-cf20788205 — [util-linux-core](https://mdapi.fedoraproject.org/f44/pkg/util-linux-core): “The most essential utilities from the util-linux suite”.
- coreos-10298fadc7 — [vim-data](https://mdapi.fedoraproject.org/f44/pkg/vim-data): “Shared data for Vi and Vim”.
- coreos-7153ad0487 — [vim-minimal](https://mdapi.fedoraproject.org/f44/pkg/vim-minimal): “A minimal version of the VIM editor”.
- coreos-bbd74c7527 — [volume_key-libs](https://mdapi.fedoraproject.org/f44/pkg/volume_key-libs): “A library for manipulating storage encryption keys and passphrases”.
- coreos-17441f27fa — [wasmedge-rt](https://mdapi.fedoraproject.org/f44/pkg/wasmedge-rt): “WasmEdge Runtime”.
- coreos-b8d62d9361 — [which](https://mdapi.fedoraproject.org/f44/pkg/which): “Displays where a particular program in your path is located”.
- coreos-42c3a48310 — [wireguard-tools](https://mdapi.fedoraproject.org/f44/pkg/wireguard-tools): “Fast, modern, secure VPN tunnel”.
- coreos-d72ec67a67 — [xfsprogs](https://mdapi.fedoraproject.org/f44/pkg/xfsprogs): “Utilities for managing the XFS filesystem”.
- coreos-dc6dfe07fc — [xkeyboard-config](https://mdapi.fedoraproject.org/f44/pkg/xkeyboard-config): “X Keyboard Extension configuration data”.
- coreos-7a81f32819 — [xxhash-libs](https://mdapi.fedoraproject.org/f44/pkg/xxhash-libs): “Extremely fast hash algorithm - library”.
- coreos-f6480c2722 — [xz](https://mdapi.fedoraproject.org/f44/pkg/xz): “LZMA compression utilities”.
- coreos-062d79a287 — [xz-libs](https://mdapi.fedoraproject.org/f44/pkg/xz-libs): “Libraries for decoding LZMA compression”.
- coreos-ea8b41bd24 — [zchunk-libs](https://mdapi.fedoraproject.org/f44/pkg/zchunk-libs): “Zchunk library”.
- coreos-35772aafe4 — [zincati](https://mdapi.fedoraproject.org/f44/pkg/zincati): “Update agent for Fedora CoreOS”.
- coreos-569595199e — [zlib-ng-compat](https://mdapi.fedoraproject.org/f44/pkg/zlib-ng-compat): “Zlib implementation provided by zlib-ng”.
- coreos-5e3328d069 — [zram-generator](https://mdapi.fedoraproject.org/f44/pkg/zram-generator): “Systemd unit generator for zram devices”.
- coreos-92d2c46387 — [zstd](https://mdapi.fedoraproject.org/f44/pkg/zstd): “Zstd compression library”.

## Verification corrections

The final file-list pass found that dbus owns no files, despite a generic message-bus description. It was moved from the executable rule to the same individual removal-boundary HOLE as the other dependency metapackages. The numactl file list shows standalone commands, so its sentence and function were corrected from the misleading library summary to S2.2-9.

The same pass also found nfs-client-utils is fileless; it received the individual metapackage HOLE decision. microcode_ctl ships firmware payload rather than standalone control utilities in the inspected package; its MUST decision cites S2.2-16. Native plugin and shared-library packages were checked against their file lists and assigned S2.2-10; standalone utility subpackages cite S2.2-9. The file-list evidence is retained in package-filechecks.jsonl. Network failures for some optional file-list lookups do not invalidate independently retrieved package function descriptions.

---

# c1 part 1: unit rows

Scope: 318 rows of kinds system-unit, user-unit, system-units, and user-units. Only the supplied input, its unit inventory files, the numbered text, and the documentation below were used. No removal or execution experiments were performed. No earlier classification was consulted.

## Sentences used, quoted exactly

- S2.2-1: Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- S2.2-2: The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- S2.2-7: settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- S2.2-13: A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- S2.2-15: accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- S3-1: **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- S3-2: If what the object does remains unknown, the case yields ?.

## Documentation and exact excerpts

- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html — “A unit file is a plain text ini-style file”; masking: “making it impossible to start it even manually.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html — “encodes information about a process controlled and supervised by systemd.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html — “For each socket unit, a matching service unit must exist, describing the service to start on incoming traffic on the socket”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.target.html — “Target units are used to group units and to set synchronization points for ordering dependencies with other unit files.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html — “By default, a service by the same name as the timer (except for the suffix) is activated.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.path.html — “For each path file, a matching unit file must exist, describing the unit to activate when the path changes.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html — “encodes information about a file system mount point controlled and supervised by systemd.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.slice.html — “This management is performed by creating a node in the Linux Control Group (cgroup) tree.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.device.html — “This may be used to define dependencies between devices and other units.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.scope.html — “Scope units manage a set of system processes.”
- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html — “List units that systemd currently has in memory.”

## Homogeneous rule U: loaded stored unit controls

Applied by `part-1.units.build.py` to 306 individual rows: the inventory shows a loaded unit, a nonempty fragment path, and its type. The unit is a control definition for independent process invocation, communication, activation ordering, filesystem mounting, or process-resource management. Removing the definition removes that managed capability or changes its orchestration: MUST under S2.2-1 and S2.2-2. Current inactivity does not establish absence of a capability. A timer that starts a cache refresh is a schedule, not the cache; a service that writes logs is a service definition, not historical logs.

The object classified is the unit control, not its executable payload. S2.2-13 does not make a value file executable code. S2.2-7 does not exempt these controls: their effects reach independent services, kernel filesystem access, IPC endpoints, or kernel process groups. Being parsed by one manager is different from being in force only inside one program. No precedence between conflicting sentences is assumed.

The output function identifies the control's common role. Its individual service purpose remains identified by the input evidence; knowing every executable argument is unnecessary to establish that a loaded service unit controls invocation of another process.

Ten rows checked by hand against their evidence and the corresponding type documentation:

| ID | Evidence inspected and why rule fits |
|---|---|
| coreos-ba67dc14d4 | Loaded running network manager service with a stored fragment; controls a separate network-management process. |
| coreos-956040fa23 | Loaded running security audit service; logging producer is a process control, not a historical log. |
| coreos-e38652edff | Loaded exited linker-cache rebuild service; invocation definition is distinct from its cache output. |
| coreos-c5a27a2455 | Loaded listening container-engine socket; exposes an IPC endpoint and service activation. |
| coreos-77462850bc | Loaded basic target with a stored fragment; groups and orders other unit activation. |
| coreos-f5fee7c08e | Loaded waiting weekly filesystem-discard timer; schedules a service invocation. |
| coreos-d023432e09 | Loaded waiting password-request path watch; triggers another unit upon filesystem conditions. |
| coreos-16081f0750 | Loaded mounted huge-pages filesystem unit; controls a kernel filesystem available to processes. |
| coreos-0325994aec | Loaded waiting executable-format automount; triggers filesystem mounting on access. |
| coreos-eb1055f947 | Loaded active application slice; creates a resource hierarchy for independent application processes. |

## Individually assessed exceptions and group rows

These 12 rows were individually assessed, rather than inferred from the stored-unit rule. Member lists were read from the input; runtime state was checked in `../in/raw/coreos/units.txt` or `../in/raw/coreos/user-list-units.txt`. Although each grouped row's numeric members field says 1, its evidence explicitly lists multiple members. The whole listed group is assessed.

- coreos-ca040c10df: MUST. `../in/raw/coreos/unit-realpaths.tsv` resolves the service fragment to `/dev/null`. This is an operative prohibition on starting the service. S2.2-1 covers restrictions on capabilities; S2.2-2's sufficient removal condition does not say that gaining a capability is exempt.
- coreos-a3f2270221: MUST for every listed device unit. These are live device-availability objects used in unit dependencies, including block-backed mounts. The object is its dependency/activation representation, not a claim that hardware must be reinstalled.
- coreos-88335c6c87: MUST for every listed device unit exposed to the user manager, for the same dependency/activation role. The duplicated device names do not denote programs confined inside an interface.
- coreos-18fb2985ed: MUST for every listed system mount. Root, boot, configuration, runtime-user, system-root and variable-data mounts provide filesystem access. Generated and observed mounts are not treated as content merely because a stored fragment is absent.
- coreos-565df89b5f: MUST for every listed mount visible to the user manager. The list includes kernel API mounts, credentials, runtime-user, root and data mounts. Their mount availability enables access by processes.
- coreos-9994d7ebc4: NOT for every listed absent unit. The raw inventory confirms not-found and inactive for each. The row is a list of unresolved names, not an installed implementation of the named facilities; there is no corresponding functionality to remove.
- coreos-97fdaec6aa: NOT for both listed absent block-device targets. The raw user inventory confirms not-found and inactive for both. These are unresolved references, not implemented target controls.
- coreos-0ff15b2741: MUST for init.scope and session-4.scope. Both are loaded, active and running; their scope controls manage existing independent processes rather than merely recording past activity.
- coreos-3bc8c8458c: MUST for init.scope. The sole listed scope is loaded, active and running and provides process grouping/resource management.
- coreos-253d752b01: MUST for all listed slices. Root, system, per-template, and user slices constitute the process-resource hierarchy. Their lifecycle/resource function extends to processes outside the manager.
- coreos-b855166ba5: MUST for the root slice. It is the root of the process-resource hierarchy, not an isolated user-interface preference.
- coreos-eb57ff0e5c: MUST for both sshd-unix-local.socket and sshd-vsock.socket. Both are loaded and listening in the raw inventory, with explicit local and virtual-machine socket descriptions. Both provide login-service endpoints and activation.

No group received differing member decisions. No rule treats generated state as automatically exempt; state handling is outside the definition under Section 2.5 and is not counted as a textual hole.

---

# Package-owned path classification

Membership is the normalized intersection of `files.tsv` and `package-files.txt`, applying `path-aliases.tsv`. Nested input groups are excluded from ancestor groups. All 237 member counts agree after normalization. Package ownership is never a recording criterion. Filesystem contents were not collected: the raw file table supplies type, path, link target, and size only.

## Directory-only rule

For rows consisting solely of directory entries, the inventory establishes a namespace container but not operational consumers or reconstruction behavior. General directory-purpose documentation does not establish these instances’ actual functional dependence. These are UNKNOWN under S3-2, not a presumption that empty directories are content. No physical removal is performed.

Manual checks: coreos-3cd182c07b, coreos-827c5914e9, coreos-037231a728, coreos-d3d071d2ba, coreos-c0faa16997, coreos-43399114f3, coreos-edd98ae366, coreos-fc1b65b090, coreos-31a0673933, coreos-1ae98d3e98. Each has one member with raw type d and no supplied contents or consumer trace.

General source: https://man7.org/linux/man-pages/man7/hier.7.html — “A typical Linux system has, among others, the following directories:” This describes typical layout, not operational use on this instance.

## Individually consulted sources

- https://man7.org/linux/man-pages/man5/dir_colors.5.html — “The program ls(1) uses the environment variable LS_COLORS”; “configuration file for dircolors(1)”
- https://man7.org/linux/man-pages/man5/adjtime.5.html — “hardware mode clock setting and clock drift factor”
- https://man7.org/linux/man-pages/man5/aliases.5.html — “an alias can refer to other aliases”
- https://man7.org/linux/man-pages/man1/bash.1.html — “executes commands read from the standard input, from a string, or from a file”
- https://man7.org/linux/man-pages/man5/host.conf.5.html — “configuration information specific to the resolver library”
- https://man7.org/linux/man-pages/man5/hosts.5.html — “associates IP addresses with hostnames”
- https://man7.org/linux/man-pages/man5/exports.5.html — “Each file system in this table has a list of options and an access control list.”
- https://man7.org/linux/man-pages/man5/group.5.html — “defines the groups on the system”
- https://man7.org/linux/man-pages/man5/passwd.5.html — “describes user login accounts for the system”
- https://man7.org/linux/man-pages/man5/gshadow.5.html — “contains the shadowed information for group accounts”
- https://man7.org/linux/man-pages/man5/shadow.5.html — “contains the password information for the system's accounts and optional aging information”
- https://man7.org/linux/man-pages/man5/ld.so.conf.5.html — “a list of directories, one per line, in which to search for libraries”
- https://man7.org/linux/man-pages/man5/libaudit.conf.5.html — “configuration information for user space applications that link to libaudit”
- https://man7.org/linux/man-pages/man5/locale.conf.5.html — “configures system-wide locale settings”
- https://man7.org/linux/man-pages/man5/login.defs.5.html — “defines the site-specific configuration for the shadow password suite”
- https://man7.org/linux/man-pages/man8/logrotate.8.html — “allows automatic rotation, compression, removal, and mailing of log files”
- https://man7.org/linux/man-pages/man5/machine-id.5.html — “contains the unique machine ID of the local system”
- https://man7.org/linux/man-pages/man5/mke2fs.conf.5.html — “controls the default parameters used by mke2fs(8)”
- https://man7.org/linux/man-pages/man5/networks.5.html — “describes known DARPA networks and symbolic names for these networks”
- https://man7.org/linux/man-pages/man5/nfs.conf.5.html — “site-specific configuration for various NFS daemons and other processes”
- https://man7.org/linux/man-pages/man5/nfsmount.conf.5.html — “section headers followed by variable assignments associated with that section”
- https://man7.org/linux/man-pages/man5/protocols.5.html — “describing the various DARPA internet protocols”
- https://man7.org/linux/man-pages/man5/request-key.conf.5.html — “determine which program it should run to instantiate a key”
- https://man7.org/linux/man-pages/man5/rpc.5.html — “names that can be used in place of RPC program numbers”
- https://man7.org/linux/man-pages/man5/rsyncd.conf.5.html — “controls authentication, access, logging and available modules”
- https://man7.org/linux/man-pages/man5/sestatus.conf.5.html — “determine what file and process security contexts should be displayed”
- https://man7.org/linux/man-pages/man5/shells.5.html — “full pathnames of valid login shells”
- https://man7.org/linux/man-pages/man5/subgid.5.html — “authorizes a group id to map ranges of group ids”
- https://man7.org/linux/man-pages/man5/subuid.5.html — “authorizes a user id to map ranges of user ids”
- https://man7.org/linux/man-pages/man5/sudo.conf.5.html — “used to configure the sudo front-end”
- https://man7.org/linux/man-pages/man5/sudoers.5.html — “determines a user's sudo privileges”
- https://man7.org/linux/man-pages/man5/sysctl.conf.5.html — “contain Linux kernel configuration parameters”
- https://man7.org/linux/man-pages/man5/vconsole.conf.5.html — “configures the virtual console, i.e. keyboard mapping and console font”
- https://man7.org/linux/man-pages/man5/issue.5.html — “contains a message or system identification to be printed before the login prompt”
- https://man7.org/linux/man-pages/man5/motd.5.html — “displayed by login(1) after a successful login”
- https://man7.org/linux/man-pages/man5/os-release.5.html — “contain operating system identification data”

Each single-file entry above was decided individually; the script only serializes the written decisions.

## Individually inspected grouped objects

The member table `part-1.owned.members.tsv` gives every member’s decision. Ordinals use the order of normalized intersection entries in raw `files.tsv`, excluding nested groups. Paths are intentionally not duplicated. Directory members are UNKNOWN unless they are ancestors necessary to reach a classified MUST member; such ancestors are MUST because removing them removes access to that required object. Unused sibling directories remain UNKNOWN. The table below records the individually selected file classes and exceptions; these selections are not a classifier inferred from package ownership.

Ancestor checks by hand: coreos-9945c88deb (dispatcher script), coreos-0a38e83850 (session shell script), coreos-47cc2958ff (completion scripts), coreos-96885714dc (backend policy links), coreos-ec5f04bd95 (bus configuration), coreos-4f3962b16e (account defaults), coreos-b91b989f2d (generator scripts), coreos-8265490c79 (library path configuration), coreos-cbdd239882 (authentication stacks), coreos-2f70798fb0 (shell startup scripts). In each, direct pathname prefixes identify exactly the needed containing directories; sibling directories do not inherit the child’s decision.

- coreos-1d70ce548d: Provides boot menu code, boot variables, and display font. MUST=3, NOT=1, UNKNOWN=1.
- coreos-9945c88deb: Configures network management and executes network-event hooks. MUST=4, UNKNOWN=7.
- coreos-0a38e83850: Runs session-startup shell integration. MUST=4, UNKNOWN=3.
- coreos-a4c2c16ae9: Sets kernel audit rules and audit-daemon preferences. HOLE=1, MUST=5, UNKNOWN=1.
- coreos-e2885ad43a: Supplies authentication stacks and name-service selection. MUST=7, UNKNOWN=4.
- coreos-47cc2958ff: Executes shell completion functions. MUST=3.
- coreos-8ff1651d76: Selects an identity-mapping plugin through a symbolic link. UNKNOWN=2.
- coreos-3a7a7fb965: Configures container-runtime behavior. HOLE=1, UNKNOWN=1.
- coreos-c2d2685965: Stores container trust, registry, and toolbox configuration. UNKNOWN=15.
- coreos-96885714dc: Distributes cryptographic policy to multiple program backends. MUST=18, UNKNOWN=3.
- coreos-ec5f04bd95: Configures message-bus connectivity and interprocess access policy. MUST=5, UNKNOWN=1.
- coreos-4f3962b16e: Supplies defaults used when creating accounts. MUST=2.
- coreos-05942fe9ff: Stores package-manager configuration and explanatory documentation. HOLE=9, NOT=1, UNKNOWN=10.
- coreos-e9bcb7e1df: Stores firmware-update daemon settings and explanatory documentation. HOLE=5, NOT=1, UNKNOWN=3.
- coreos-b91b989f2d: Executes boot-configuration generator scripts and includes explanatory documentation. MUST=13, NOT=1.
- coreos-35fa9d83db: Configures an authentication mechanism plugin. UNKNOWN=3.
- coreos-89042bc9be: Stores authentication-proxy configuration. UNKNOWN=3.
- coreos-95865da962: Provides explanatory documentation for networking configuration. NOT=1, UNKNOWN=1.
- coreos-d33aabe318: Stores storage-session daemon configuration. UNKNOWN=2.
- coreos-85898eb196: Supplies integrity-verification certificates. MUST=10.
- coreos-5fd4dee5c3: Provides an example terminal configuration. NOT=1.
- coreos-3368ad3458: Includes shared authentication and cryptography configuration. MUST=3.
- coreos-8265490c79: Adds shared-library discovery directories. MUST=2.
- coreos-a17631eb59: Selects block-device library configuration. UNKNOWN=3.
- coreos-66ca6c2372: Stores driver-selection values for userspace RDMA. UNKNOWN=19.
- coreos-ee7f18d46b: Supplies network library identifier tables. UNKNOWN=3.
- coreos-f5454e1609: Stores event-handler configuration. UNKNOWN=6.
- coreos-1af8073cda: Configures log processing, potentially including executed hook code. UNKNOWN=9.
- coreos-a45be4a17a: Stores volume-manager defaults and optional profiles. HOLE=10, UNKNOWN=6.
- coreos-20d5a4dc7b: Stores firewall rule files and operating-system fingerprint data. UNKNOWN=6.
- coreos-34af1b92eb: Provides explanatory network-state documentation. NOT=1, UNKNOWN=1.
- coreos-ae5247403a: Stores storage-discovery configuration. UNKNOWN=2.
- coreos-1ef6a866b0: Supplies defaults shared by LDAP clients. MUST=2, UNKNOWN=1.
- coreos-cbdd239882: Defines authentication and account-access stacks. MUST=22.
- coreos-17a7caf72b: Stores trust anchors, cryptographic configuration, scripts, and explanatory documents. MUST=368, NOT=7, UNKNOWN=563.
- coreos-2f70798fb0: Executes shell initialization scripts. MUST=29.
- coreos-5d89e4193b: Provides explanatory initialization documentation. NOT=1, UNKNOWN=2.
- coreos-d159c2f1cf: Selects helpers for kernel key requests. MUST=4.
- coreos-29ef947721: Stores writable-filesystem setup descriptions. UNKNOWN=4.
- coreos-38d62d7f56: Stores file-sharing configuration and a sample configuration. NOT=1, UNKNOWN=3.
- coreos-aaa1adf124: Controls authentication, account resources, namespaces, and password history. HOLE=1, MUST=13, UNKNOWN=3.
- coreos-c9f542a45c: Stores access-control policy, labels, and compiled label caches. MUST=43, NOT=2, UNKNOWN=2.
- coreos-4c24122c97: Supplies shell startup code copied into new accounts. MUST=4.
- coreos-c366c1919d: Controls login access and SSH client behavior. HOLE=3, MUST=7, UNKNOWN=2.
- coreos-5f604fda76: Exposes shared trust bundles and cryptographic configuration. MUST=6, NOT=1, UNKNOWN=2.
- coreos-cc6acfb8b2: Exposes software-identification metadata. NOT=1, UNKNOWN=2.
- coreos-0fea41ffe5: Stores firewall policy and service-startup options. MUST=5, UNKNOWN=11.
- coreos-2b4fe000fc: Exposes persistent kernel parameter configuration. MUST=2.
- coreos-0c7a1a4d1e: Stores TPM library configuration and cryptographic profiles. UNKNOWN=7.
- coreos-ec7d8d80c0: Supplies compiled hardware properties for device setup. MUST=2, UNKNOWN=2.
- coreos-3da21e28f6: Stores disk-management settings and a sample configuration. NOT=1, UNKNOWN=3.
- coreos-3eb238bafa: Exposes desktop autostart and user-service search locations. UNKNOWN=4.
- coreos-b656843499: Sets software package repository sources. HOLE=5, UNKNOWN=1.
- coreos-e2cc7e7fb6: Stores an auxiliary cache for rebuilding the library index. NOT=1, UNKNOWN=1.
- coreos-e48d7a5dbe: Persists measured clock drift used for future time correction. HOLE=1, UNKNOWN=1.
- coreos-a51d3ac08b: Provides a package-manager locking object. UNKNOWN=2.
- coreos-94db10583a: Exposes an authentication-proxy socket and storage directories. UNKNOWN=4.
- coreos-89229e49e6: Stores message catalog data, boot entropy seed, and service-state directories. MUST=2, NOT=1, UNKNOWN=3.

## Additional primary-source evidence and limits

The following short passages establish functions used in the grouped partitions and remaining individual rows. Inventory paths determine membership; documents determine the programs’ handling of these object formats. A format that permits several materially different uses does not establish the actual contents of an uncollected file. UNKNOWN is used where that distinction matters.

- https://man7.org/linux/man-pages/man7/audit.rules.7.html — “a file containing audit rules that will be loaded by the audit daemon's init script”. Audit rules govern kernel recording, not the historical log output.
- https://man7.org/linux/man-pages/man5/auditd.conf.5.html — “configuration information specific to the audit daemon”. The daemon preferences have the inside/outside ambiguity, unlike kernel audit rules.
- https://www.networkmanager.dev/docs/api/latest/NetworkManager-dispatcher.html — “NetworkManager will wait for script execution to complete”. Dispatcher hooks are executed code. Empty sibling directories have no established operational contents.
- https://dbus.freedesktop.org/doc/dbus-daemon.1.html — “Multiple programs connect to the message bus daemon and can exchange messages with one another.” Bus access policy governs communication between processes.
- https://man7.org/linux/man-pages/man8/useradd.8.html — “creates a new user account using the values specified on the command line plus the default values from the system.” Account defaults control system accounts.
- https://man7.org/linux/man-pages/man5/dnf.conf.5.html — “all *.repo files found under /etc/yum.repos.d”. Repository selection is operational input to package management; its treatment as one program’s values versus external system control is not specified.
- https://man7.org/linux/man-pages/man5/dracut.conf.5.html — “Each line specifies an attribute and a value.” Values affect construction of a later boot environment; one-program scope remains ambiguous.
- https://man7.org/linux/man-pages/man8/pam_env.8.html — “allows the (un)setting of environment variables”. Session values propagate to child applications; this is not a single editor’s presentation preference.
- https://man7.org/linux/man-pages/man5/pam.d.5.html — “These files list the PAMs that will do the authentication tasks required by this service”. The stacks implement login and account checks.
- https://man7.org/linux/man-pages/man5/ldap.conf.5.html — “used to set system-wide defaults to be applied when running ldap clients”. These values are shared across clients.
- https://web.mit.edu/kerberos/krb5-latest/doc/admin/conf_files/krb5_conf.html — “defaults for the current realm and for Kerberos applications”. The same source documents included files; the authentication configuration spans applications.
- https://man7.org/linux/man-pages/man8/selinux.8.html — “an implementation of a flexible mandatory access control architecture in the Linux operating system.” Access-control policy and labeling inputs govern system-wide permissions.
- https://man7.org/linux/man-pages/man8/pam_pwhistory.8.html — “saves the last passwords for each user in order to force password change history”. The saved password history is both a past record and input restricting future passwords: S2.2-6 versus S2.2-1/S2.2-15 has no stated treatment for the dual role.
- https://man7.org/linux/man-pages/man5/sshd_config.5.html — “sshd(8) reads configuration data from /etc/ssh/sshd_config”. Login restrictions are explicitly required. Client configuration remains a scope ambiguity; the uncollected moduli’s operational dependence is left UNKNOWN.
- https://man7.org/linux/man-pages/man7/hwdb.7.html — “used primarily by udev to add the relevant properties to matching devices”. The compiled database supplies device properties affecting other programs; being compiled alone is not the cache exemption.
- https://man7.org/linux/man-pages/man8/systemd-random-seed.service.8.html — “loads an on-disk random seed into the kernel entropy pool during boot and saves it at shutdown”. The seed contributes to future system randomness, not merely display content.
- https://chrony-project.org/doc/latest/chrony.conf.html — “The driftfile directive allows a file to be specified into which chronyd can store the rate information.” Clock configuration controls system time. Stored drift is a past measurement reused for future correction; removing it causes relearning, and the text does not distinguish this from exempt cache or history.
- https://www.thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html — “a lightweight DNS, TFTP, PXE, router advertisement and DHCP server.” Server configuration changes network facilities available to other programs and machines.
- https://www.nano-editor.org/dist/latest/nanorc.5.html — “The nanorc files contain the default settings for nano”. Its documented settings and interface commands fall within the single-program setting exemption.
- https://man7.org/linux/man-pages/man5/services.5.html — “a mapping between human-friendly textual names for internet services, and their underlying assigned port numbers and protocol types.” Lookup data is operational across network clients; entries are not themselves open ports.
- https://man7.org/linux/man-pages/man8/lastlog.8.html — “prints the contents of the last login log”. The corresponding file is historical information.
- https://man7.org/linux/man-pages/man5/proc_pid_mounts.5.html — “This file lists all the filesystems currently mounted in the process's mount namespace”. The mount-table link exposes live state rather than a historical record.
- https://man7.org/linux/man-pages/man8/ld.so.8.html — “find and load the shared objects (shared libraries) needed by a program”. The main loader cache can identify libraries outside fallback directories: without its entries, the speed-only condition is unproved.
- https://man7.org/linux/man-pages/man8/ldconfig.8.html — “creates the necessary links and cache to the most recent shared libraries”. The auxiliary index caches rebuilding work; it differs from the runtime loader’s primary path index.
- https://github.com/Azure/azure-vm-utils/blob/main/ephemeral-disk-setup/azure-ephemeral-disk-setup — “# Ensure key is valid.” The inspected implementation parses allowed configuration assignments and uses them to select disk aggregation, formatting, and mounts. It does not execute unrestricted configuration text.

Attempted primary manual URLs for missing or ambiguous formats included the corresponding man7 pages for csh, tcsh, idmapd.conf, kdump.conf, netconfig, printcap, xattr.conf, crypto-policies, containers-policy.json, gssproxy.conf, and iscsid.conf. Those pages were unavailable. General filesystem documentation establishes only typical purposes, not the missing contents of this inventory. UNKNOWN groups retain unresolved entries even when some other members have known functions.

Some raw paths directly identify interpreter startup files or scripts; these are judged by the explicitly named S2.2-10 examples. No execution rights are inferred from package ownership. README and sample members are explanatory content identified individually in their group partitions. The group directory members do not silently become exempt because their files are content.

## Specific mixed-group reasoning

- coreos-1d70ce548d: boot configuration and boot variables MUST; the display font NOT; font-only directory UNKNOWN. The latter’s operational requirement is unestablished independently of the content.
- coreos-a4c2c16ae9: audit rule files MUST; daemon preference file HOLE between one-program settings and external operation; unused plugin directory UNKNOWN.
- coreos-05942fe9ff, coreos-e9bcb7e1df: documentation NOT; manager configuration HOLE between internal values and external system changes; directory entries UNKNOWN unless needed by a MUST member.
- coreos-b91b989f2d: generator scripts MUST; explanatory README NOT; parent directory MUST because it exposes the scripts.
- coreos-17a7caf72b: identified shared trust bundles MUST because they control authentication across consumers; explanatory README members NOT; unresolved per-tool configuration, key purposes, and empty directories UNKNOWN. Exact partition is the ordinal member table.
- coreos-aaa1adf124: authentication/resource restrictions and namespace initialization MUST; password history HOLE because past records/passwords are exempt but they enforce future restrictions.
- coreos-c9f542a45c: access-control policy and textual labels MUST; corresponding compiled label lookup caches NOT; the checksum’s actual consumer UNKNOWN.
- coreos-c366c1919d: server login policy MUST; client configuration HOLE between single-client preferences and externally visible connectivity; moduli dependence UNKNOWN.
- coreos-5f604fda76: shared trust-bundle aliases MUST; explanatory README NOT; two cryptographic configuration aliases UNKNOWN without established contents/consumers.
- coreos-e48d7a5dbe: drift measurement HOLE between behavior-affecting future clock correction and exempt history/cache; directory requirement UNKNOWN.
- coreos-89229e49e6: entropy seed MUST; message catalog database NOT as explanatory message content; other directory members UNKNOWN.

## Scope and limitations

These are classification outputs, not a removal experiment. No system object was changed or removed. Public documentation supplies format and intended-consumer evidence; unavailable instance contents are not silently replaced with distribution defaults. Directory-only uncertainty is not a claimed defect of the definition. The text’s exclusion of state-management design questions is respected: only whether the object’s established function meets Section 2.2 is considered.

## Exact deciding sentences

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-14** a saved Wi-Fi network must be recorded; the network password need not be: when it changes, the computer does the same;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S3-2** If what the object does remains unknown, the case yields ?.

## Final source checks and clarification

- https://p11-glue.github.io/p11-glue/p11-kit/manual/trust.html — “Extract trust policy from the shared trust policy store.” Extracted trust bundles are operational authentication inputs across libraries, not automatically speed-only caches.
- https://www.mankier.com/8/update-ca-trust — “new applications that read the consolidated configuration files found in the /etc/pki/ca-trust/extracted directory”. This is the program’s manual, reproduced on a manual-page host, and confirms the collected directory’s role.
- https://www.mankier.com/7/crypto-policies — “allow consistently deprecating and disabling algorithms system-wide”. This is the program manual; it supports required shared cryptographic backend policy rather than single-program preferences.
- https://www.mankier.com/8/authselect — “configure system identity and authentication sources and providers by selecting a specific profile”. The generated authentication and name-service files implement account access across processes.
- https://www.mankier.com/5/containers-policy.json — “Signature verification policy files are used to specify policy”. This program manual establishes shared image-verification policy. Final correction for coreos-c2d2685965: policy.json and its containing directory MUST; all other collected members UNKNOWN, producing MIXED. This supersedes the earlier UNKNOWN-only count line.
- https://www.gnu.org/software/grub/manual/grub/html_node/Embedded-configuration.html — “read the real configuration file from $prefix/grub.cfg”. The configuration links target the bootloader’s command configuration.
- https://www.gnu.org/software/grub/manual/grub-dev/html_node/File-Structure.html — “The standard file extension for PFF2 font files is .pf2.” The collected font is display material, classified separately from boot commands.
- https://man7.org/linux/man-pages/man5/file_contexts.5.html — “This optimization is no longer required due to the use of file_contexts.bin files and is deprecated.” The binary files optimize lookup of the corresponding textual mapping members; the text sources remain present in this inventory.
- https://man7.org/linux/man-pages/man8/ldconfig.8.html — “Ignore auxiliary cache file.” The explicit option establishes that the auxiliary cache is dispensable for rebuilding the main index.

The standalone operating-system release identifiers are HOLE because their documented descriptive role does not exclude use as behavioral input. The software-tag group is treated as explanatory metadata; its directory members remain UNKNOWN. Directory UNKNOWN does not assert that every directory has the same runtime role.

## Exception-priority review

The explicit introduction S2.2-3 (“The following need not be recorded:”) makes S2.2-6 a stated exception to the broad dependency rule. Merely consulting history later does not cancel that exception. Final corrections therefore supersede the earlier discussions and count lines: password-history member in coreos-aaa1adf124 is NOT; recorded drift member in coreos-e48d7a5dbe is NOT; migration stamp coreos-845955a7d2 is NOT. Their earlier HOLE/UNKNOWN reasoning overextended the general dependency sentence. Directory decisions are unchanged. The final TSV and ordinal member table contain the corrected decisions.

The remaining single-program-setting HOLE cases concern the undefined scope of “only inside one program”: whether settings whose values a single program reads but whose operation creates external artifacts satisfy that qualifier. They do not assume that the broad rule overrides a known exemption. Password-plus-lock files remain HOLE because distinct required and exempt information occupies the same ungrouped file and no aggregate file rule is provided.

- **S2.2-3** The following need not be recorded:

---

## Final mechanical verification

verify-part-1.py asserts identical input/output ID multisets and counts, uniqueness, exact header, allowed decisions, allowed sentence IDs, field lengths, and agreement with completed subset files. Only after these assertions does it write part-1.done. Review findings and follow-up resolutions are preserved separately in part-1.review.md.

## Final execution-evidence linkage

For coreos-aae56aa09f, package identity and module contents are established by the package metadata and saved file list above. Execution is established by https://github.com/rhboot/grub2/blob/master/grub-core/kern/dl.c, whose loader invokes the module initialization function. The row now cites this execution source directly. The module is loaded native bootloader code under S2.2-10, not a standalone operating-system process.

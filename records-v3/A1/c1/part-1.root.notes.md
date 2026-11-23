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

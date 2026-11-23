# Part 5 classification notes

Only COMMON.md, TEXT.md Sections 2–3, SENTENCES.md, this part input, and public program documentation were consulted. No other classification or earlier inventory source tree was read. The raw folders for the four input machine labels are absent under A1/in/raw. Input ids retain their required literal labels; descriptions do not reproduce personal paths or identities. No removal was performed.

## Account rule R1

Apply to every row with kind=account whose evidence gives uid and gid: MUST under S2.2-15. The rule does not depend on shell availability, privilege level, or whether an account is interactive.

Exact deciding sentence S2.2-15: “accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;”

Ten rows manually checked against their evidence:

- alpine-c6df412fe9: UID 1000, GID 1000, interactive shell; account.
- alpine-8d1e409524: UID 1, GID 1, nologin; still an account.
- alpine-3d437d2b28: UID 7, GID 0, halt shell; still an account.
- alpine-736d2abbd6: UID 10, GID 14, nologin; still an account.
- arch-0eb052c890: UID 970, GID 970, nologin; still an account.
- arch-cbaf0b4232: UID 0, GID 0, shell; privileged account.
- silverblue-688f82dd27: UID 3, GID 4, nologin; still an account.
- silverblue-3d437d2b28: UID 7, GID 0, halt shell; still an account.
- ubuntu-205e945769: UID 42, GID 65534, nologin; still an account.
- ubuntu-8c8f9ffd14: UID 33, GID 33, nologin; still an account.

129 rows appended under R1. All other locally assigned objects are decided individually. Stored-object partitions have separate notes, incorporated below after completion.

## Individually decided processes and units

The 56 explicit assignments are in part-5.local-decisions.py; its mapping names every id rather than inferring decisions from name patterns. A script only validates and appends those manually written assignments. Generic manuals establish unit semantics, while input evidence establishes the listed instance. In particular, a unit name alone does not identify dependency properties. A filesystem or swap unit observed in a user-manager listing without a backing fragment is not assumed to control the corresponding system operation. No claim of a definitional hole is made solely from missing state or inventory detail.

For scope and slice rows, the known type itself establishes external process lifecycle/resource management. Removing that operation changes behavior outside the manager interface. Kernel-thread rows contain only numeric process ids; generic kernel-thread documentation cannot establish their individual functions. The custom init-service body is missing, but the upstream runner establishes its shell-code execution role. S2.2-10 decides that service without requiring the details of every command. Kernel-thread identities remain UNKNOWN, not HOLE.

### Deciding sentences quoted exactly

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-9: “a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;”
- S3-1: “**Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.”
- S3-2: “If what the object does remains unknown, the case yields ?.”

### Primary documentation consulted

Short exact excerpts below support the functions, not the classification rule. The latter comes solely from the cited hypothesis sentences.

- https://www.freedesktop.org/software/systemd/man/latest/systemd.device.html — “This may be used to define dependencies between devices and other units.” Device representations can participate in dependencies; listed names alone do not supply them.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.swap.html — “encodes information about a swap device or file for memory paging controlled and supervised by systemd.” The documentation distinguishes privileged swap support from unprivileged user-manager operation.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.scope.html — “Scope units manage a set of system processes.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.slice.html — “A slice unit is a concept for hierarchically managing resources of a group of processes.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html — “Mount points created at runtime (independently of unit files or /etc/fstab) will be monitored by systemd” (inline formatting omitted). Existence of a mount listing does not alone prove a distinct configuration source.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.automount.html — “Automount units may be used to implement on-demand mounting as well as parallelized mounting of file systems.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html — “for socket-based activation.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html — “encodes information about a process controlled and supervised by systemd.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html — “A unit file is a plain text ini-style file”
- https://www.freedesktop.org/software/systemd/man/254/systemctl.html — “if no unit file was found for this unit” (description of not-found).
- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html — “List units that systemd currently has in memory.” This includes references and failed units, not exclusively installed working services.
- https://github.com/procps-ng/procps/blob/master/man/ps.1 — “report a snapshot of the current processes.”
- https://busybox.net/downloads/BusyBox.html — “Report process status”; this establishes the same process-listing role without assuming an executable provider from a process name alone.
- https://kernel.org/doc/html/v6.11/driver-api/basics.html — “the function to run in the thread” (threadfn parameter). Numeric identifiers in this input do not provide that function.

All classifications concern the supplied object; no files, processes, units, or devices were removed. Current manuals were used for longstanding semantics, not as evidence of an installed version or of unlisted local configuration.

<!-- included-part-2 -->

# Part 5, stored objects on the two assigned distributions

Only COMMON.md, TEXT.md Sections 2 and 3, SENTENCES.md, and the assigned input rows were read locally. The expected raw directories for these distributions do not exist. No objects were removed. Directory groups have `members=1` in the input, but inventory evidence often supplies a larger `n`; that underlying count was respected rather than treating four sample paths as the entire group.

The classifications are row-specific except the two explicitly identified rules below. The build script records each individual assessment. This is a classification, not independent acceptance.

## Exact governing sentences

- S2.2-1: Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- S2.2-2: The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- S2.2-5: cache: after it is removed, the computer does the same, only more slowly;
- S2.2-6: records of the past—logs, history;
- S2.2-7: settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- S2.2-9: a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- S2.2-10: code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- S2.2-13: A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- S2.2-15: accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- S3-2: If what the object does remains unknown, the case yields ?.

## Rule L: standalone historical log files

S2.2-6 directly exempts logs. This rule applies only to individually identified, standalone log files. It does not classify incompletely enumerated log directories. Hand checks of ten input rows:

- alpine-4156dc1632: acpid event log, one file.
- alpine-336e9af6dd: apk operation log, one file.
- alpine-93b020b2d3: cloud initialization output log, one file.
- alpine-2954505d9d: cloud initialization execution log, one file.
- alpine-293699acd1: saved kernel message log, one file.
- alpine-91a21a61f1: system message log, one file.
- alpine-d6ce9987c3: completed login-session history, one file.
- arch-9c96b64591: failed-login history, one file.
- arch-698c23461f: last-login history, one file.
- arch-abc9f2b51d: package transaction history, one file.

The additional row arch-d6ce9987c3 is also a single login-history file. All eleven fit the historical-log exemption.

## Rule U: incomplete stored-directory enumeration

The input supplies only a subset of members and the full raw listing is absent. Documentation can describe a known filename, but cannot recover unnamed members of these particular directories. S3-2 therefore requires UNKNOWN for the complete group; neither homogeneity nor a complete member-by-member MIXED allocation is inferred from samples. Ten hand checks, each comparing the inventory count with the actual displayed sample paths:

- alpine-312e18febb: 24 objects, four service-link samples.
- alpine-0075a76d48: seven objects, four server-key samples.
- alpine-561d6a5935: three objects, one device-rule sample.
- alpine-c3a3dd6c9b: two objects, one login-key sample.
- alpine-351644c1fd: two objects, one login-key sample.
- alpine-995a8560ba: 53 objects, four initialization-state samples.
- arch-76634f69cd: 699 objects, four bootloader samples.
- arch-472ce9551e: 361 objects, four certificate-store samples.
- arch-d938b25615: 19 objects, four package-signing samples.
- arch-0075a76d48: eight objects, four server-key samples.

The remaining Rule U rows were likewise read individually: arch-0306bdd9a9, arch-b86fee9a16, arch-c3a3dd6c9b, arch-2b7dd179b7, arch-b618c77d89, arch-23338df933, arch-cafdef0617, arch-57da4d32dc, arch-e6b33c3854. Each gives fewer sample paths than its inventory count. The two unnamed directory skeletons were separately assessed as UNKNOWN because even their paths are unavailable.

## Documentation and exact supporting excerpts

Short quotations below identify the relevant documentation; deductions are in the TSV reasons. No source substitutes for a missing machine-specific inventory.

- https://wiki.archlinux.org/title/Syslinux — “Stage 3 - Load `/boot/syslinux/ldlinux.c32`”. The indexed documentation describes the bootloader stages, native module libraries, configuration loading, and text menu.
- https://kernel.googlesource.com/pub/scm/boot/syslinux/syslinux/+/master/doc/menu.txt — “com32/menu/vesamenu.c32 (graphical) or com32/menu/menu.c32 (text”. This upstream source establishes both menu module functions.
- https://github.com/alpinelinux/mkinitfs — “Tool to create initramfs images”.
- https://github.com/alpinelinux/mkinitfs/blob/master/mkinitfs.in — `for file in $(feature_files "${kerneldir}/" modules); do`. The surrounding routine gathers module dependencies and copies selected drivers into the image.
- https://github.com/alpinelinux/apk-tools/blob/master/doc/apk.8.scd — “Collection of all package scripts from currently installed packages.” Its FILES section separately documents architecture, repository lists, required packages, installed metadata, trigger rules, transaction lock, and index cache.
- https://github.com/OpenRC/openrc/blob/master/sh/openrc-run.sh.in — `sourcex -e "$_f/conf.d/$_c"` and `sourcex "$RC_SERVICE"`. Both service settings and service scripts are sourced by the runner.
- https://man.archlinux.org/man/doas.conf.5.en — “The target user the running user is allowed to run the command as. The default is all users.”
- https://man.archlinux.org/man/sudoers.5.en — “The sudoers policy plugin determines a user's sudo privileges.”
- https://man7.org/linux/man-pages/man5/passwd.5%40%40shadow-utils.html — “Backup file for /etc/passwd.”
- https://man7.org/linux/man-pages/man5/shadow.5.html — “Backup file for /etc/shadow.”
- https://man.archlinux.org/man/subuid.5.en — “Backup file for /etc/subuid.”
- https://man.archlinux.org/man/dhcpcd.8.en — “Text file that holds the DUID used to identify the host.” The same manual describes lease reuse, a stored secret, and resolver configuration. The secret's mere existence does not establish this installation's operational dependence.
- https://www.man7.org/linux/man-pages/man3/getspnam.3.html — “lock file”. This identifies the password lock, but does not show whether this stored inode currently carries a lock.
- https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files — “This section describes how Bash executes its startup files.” The manual explicitly describes login, interactive, and logout command execution.
- https://ftp.gnu.org/old-gnu/Manuals/bash-2.05a/html_mono/bashref.html — “Any user can customize programs that use Readline by putting commands in an inputrc file”. Shared use creates the reported scope ambiguity, not uncertainty over Readline's basic function.
- https://www.nano-editor.org/dist/latest/nanorc.5.html — “The nanorc files contain the default settings for nano, a small and friendly text editor.”
- https://man.archlinux.org/man/mkinitcpio.8.en — “Creates an initial ramdisk environment for booting the Linux kernel.” This also documents preset-based generation of images.
- https://man7.org/linux/man-pages/man8/ld.so.8.html — “a compiled list of candidate shared objects previously found in the augmented library path.” Cache contents are unavailable, so the fallback search cannot establish equivalent behavior here.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-update-done.service.html — “Mark `/etc/` and `/var/` as fully updated”. The modification times are compared by conditional update services: both historical recording and future behavioral control are documented.
- https://www.freedesktop.org/software/systemd/man/latest/hostname.html — “The `/etc/hostname` file configures the name of the local system.”
- https://www.freedesktop.org/software/systemd/man/latest/locale.conf.html — “The `/etc/locale.conf` file configures system-wide locale settings.”
- https://www.freedesktop.org/software/systemd/man/latest/localtime.html — “If `/etc/localtime` is missing, the default `UTC` timezone is used.” The input explicitly shows a UTC target, so removal retains the documented timezone default.
- https://www.freedesktop.org/software/systemd/man/latest/machine-id.html — “`/etc/machine-id` is used to decide whether a boot is the first one.” The documentation also identifies the D-Bus compatibility link.
- https://www.freedesktop.org/software/systemd/man/latest/vconsole.conf.html — “The `/etc/vconsole.conf` file configures the virtual console, i.e. keyboard mapping and console font.”
- https://www.freedesktop.org/software/systemd/man/latest/os-release.html — “Applications should check for the former, and exclusively use its data if it exists, and only fall back to `/usr/lib/os-release` if that is missing.” Compatibility-only readers are also documented; their presence is not inventoried.

The apk replacement file and the boot-directory alias remain UNKNOWN because their actual readers are not established. The upstream mboot README and mboot documentation URLs were tried but inaccessible, and the inventory supplies no module contents. This is factual insufficiency, not a textual hole.

## Validation

The script verified exactly 87 assigned IDs, identical sets and counts, each once; all decisions allowed; every description and reason meets its word limit. Counts: MUST=31, NOT=23, HOLE=4, UNKNOWN=28, MIXED=1.

<!-- included-part-3 -->

# Part 5, assigned stored-object subset

All 57 rows were assessed individually. The script only serializes explicit assessments and verifies format; no homogeneous automatic classification rule was used. No removal, system modification, or probe was performed.

The input reports `members=1` for every assigned row, while directory evidence often reports `n>1`. The actual evidence describes aggregate contents, so those contents are the objects assessed. No missing entry is assumed to resemble sampled entries. Named members can establish MIXED when their different decisions are already known; otherwise incomplete membership yields UNKNOWN. Documentation describes program conventions but cannot recover the missing inventory entries or local file contents. The assigned machine has no supplied raw directory.

The required input identifiers retain their literal spelling. All other discussion uses object roles and paths outside user directories.

## Exact deciding sentences

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.

- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;

- **S2.2-6** records of the past—logs, history;

- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;

- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;

- **S3-2** If what the object does remains unknown, the case yields ?.

## Documentation consulted and quoted

- Bash startup documentation: https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files — “Bash reads and executes commands from the file `~/.bash_logout`, if it exists.” This identifies logout execution; the same page identifies login profiles and interactive startup files as command files. Applied individually to 0ef3eb01b3 and be57689b36. The 661587021d inventory additionally reports actual execution of the editor-variable assignment.
- System update timestamps: https://www.freedesktop.org/software/systemd/man/261/systemd-update-done.service.html — “Mark `/etc/` and `/var/` as fully updated”. Its Description explains that the timestamps are tested by `ConditionNeedsUpdate=`. Applied individually to 5932b79e41 and 1711d3c8c4. These are HOLE because the completion records are also inputs to future service execution; the text does not delimit “records of the past” to passive logs.
- Permission repair condition: https://raw.githubusercontent.com/coreos/rpm-ostree/main/src/daemon/rpm-ostree-fix-shadow-mode.service — `Description=Update permissions for /etc/shadow` and `ConditionPathExists=!/etc/.rpm-ostree-shadow-mode-fixed2.stamp`. Applied to 3f676c29ae. The completion stamp both records repair and determines whether repair is run.
- Relabel condition: https://raw.githubusercontent.com/ostreedev/ostree/main/src/libostree/ostree-sysroot-deploy.c — `const char selabeled[] = "var/.ostree-selabeled";` and `"Relabeling /var (no stamp file '%s' found)"`. Applied to 5a0b991b97. The surrounding absence check triggers relabeling and later creates the marker. This is the same historical-record/active-condition ambiguity, individually assessed.
- NetworkManager keyfiles: https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/nm-settings-keyfile.html — “NetworkManager is based on the concept of connection profiles that contain network configuration”. Applied to 84bd973295. The only inventoried member is a connection profile; its effects configure a network device rather than remaining inside a program interface.
- Deployment boot entries: https://ostreedev.github.io/ostree/deployment/ — “This configuration file will include a special `ostree=` kernel argument”. The surrounding description identifies `/boot/loader/entries/` as the configuration location. Applied to 91fe7de139: the inventoried selector link supplies access to those deployment entries. Other boot aggregates remain UNKNOWN because entries are missing from their samples.
- Boot updater state: https://github.com/coreos/bootupd/issues/65 — “Today we have a singular (not published: external working record).” This establishes the storage convention for e51a3be8af, but neither the local state nor its operational consequences are supplied. UNKNOWN is retained.
- Password database locking: https://www.kernel.org/pub/linux/docs/man-pages/book/man-pages-6.03.pdf — “Only programs that use `lckpwdf()` will notice the lock.” Applied to fefd90f542. The inventory establishes a path but not an active lock, so no claim that removal disrupts a concurrent operation is made.
- Firewall backup implementation: https://raw.githubusercontent.com/firewalld/firewalld/main/src/firewall/core/io/zone.py — `shutil.copy2(name, "%s.old" % name)` and `"Backup of file '%s' failed: %s"`. Zone format: https://firewalld.org/documentation/man-pages/firewalld.zone.html — “firewalld zone configuration files”. Applied to 3f0965f4b3. Both members are identified: the XML is firewall policy and the `.old` file preserves the previous version.
- Account backup: https://man7.org/linux/man-pages/man5/passwd.5@@shadow-utils.html — “Backup file for /etc/passwd.” Applied to c169edc1ca.
- Protected account backup: https://man7.org/linux/man-pages/man5/shadow.5.html — “Backup file for /etc/shadow.” Applied to 9ed4eb3a99.
- Subordinate group backup: https://man7.org/linux/man-pages/man5/subgid.5.html — “Backup file for /etc/subgid.” Applied to c1ef82d842.
- Subordinate user backup: https://www.man7.org/linux/man-pages/man5/subuid.5.html — “Backup file for /etc/subuid.” Applied to a2bc9043e2.
- Shared account-file backup implementation: https://raw.githubusercontent.com/shadow-maint/shadow/master/lib/commonio.c — `static int create_backup (const char *name, FILE * fp)` and `stprintf_a(target, "%s-", name);`. Applied individually to d3bb1c2fce and 42b0af3cd4. The trailing-hyphen files preserve previous versions, not the current group definitions.
- GRUB shell scripts: https://www.gnu.org/software/grub/manual/grub/grub.html — “shell scripts stored in `/etc/grub.d/`”. Applied to 211f893687; this explicitly identifies code rather than values-only configuration.
- NVMe identities: https://github.com/linux-nvme/nvme-cli/blob/master/Documentation/CONFIGURATION.md — “The default host NQN and host identifier are read from `/etc/nvme/hostnqn` and `/etc/nvme/hostid`.” Applied to c72b0441bf. Both inventoried members are identified. Identity access effects are described in https://github.com/linux-nvme/nvme-cli/blob/master/libnvme/design/CONFIG.md — “The subsystem uses it for access-control lists and to filter the discovery log.” These identities affect access outside the reading program.
- DNS resolver: https://www.freedesktop.org/software/systemd/man/latest/systemd-resolved.service.html — “systemd-resolved is a system service that provides network name resolution to local applications.” Its resolv.conf discussion identifies the inventoried stub link. Applied to cee61291d2.
- SSH keys: https://man.openbsd.org/sshd — “Specifies a file from which a host key is read.” Documentation confirms sampled server-key functions but cannot establish the two unsampled members for 0075a76d48. Likewise it cannot identify the second member of the authorized-key collection b2b64aaca8.
- D-Bus identity: https://dbus.freedesktop.org/doc/dbus-uuidgen.1.html — “This will ensure that /var/lib/dbus/machine-id exists and has the uuid in it.” This confirms convention but does not establish whether the inventoried alias is required by local consumers rather than their direct use of the target; 7c99ede366 remains UNKNOWN.

## Individual evidence-only distinctions

For 809cb439ce, the evidence explicitly identifies two aliases to executables and two aliases to manual pages. Executable aliases supply command invocation; documentation aliases supply content. The remaining 42 entries are unknown. MIXED records the demonstrated difference without inventing their decisions.

For d01c2fc3c7, the sole target is a README document about logs, not executable logging configuration. For 98e3025b9e, the sole mailbox stores message content. For 134469a114, b8fb1ae9b1, d1a2b04577, and 125b64b2d7, each sole member is a named log; the historical-log exemption decides each independently. Larger logging directories are not assumed homogeneous because their member lists are incomplete.

For all UNKNOWN aggregates, the output reason identifies the missing membership or contents. Examples with potentially consequential samples include deployment kernels, SELinux policies, deployed applications, login keys, and resource controls; these samples do not license inferring the roles of all other entries. The directory-only remainder lacks even paths and permissions. Local files such as the sudoers fragment can contain policy, options, or comments; public syntax documentation cannot establish their particular contents.

## Verification

The serialization script verified exact assigned ID multiset equality (57 IDs, each once), allowed decisions, and both word limits. Counts: MUST 8; NOT 12; HOLE 4; UNKNOWN 31; MIXED 2. This records completion of the assigned subset, not independent acceptance.

The current-task OpenRC service assessment was refined after reading the upstream runner: `sourcex "$RC_SERVICE"` establishes execution with the runner privileges. This is sufficient for S2.2-10 even though custom command details are unavailable. No prior-attempt rows existed.

<!-- included-part-1 -->

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


## Completion validation

part-5.verify.py passed: 479 input rows and 479 output rows; identical id multisets; each id occurs once; every decision is permitted; header, sentence ids, field limits, and field structure are valid. part-5.done contains the five decision counts. This is mechanical validation of c1 output, not independent acceptance.

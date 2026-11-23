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

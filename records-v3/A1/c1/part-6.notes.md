# Part 6, classification c1

Only (not published: outside selected checks and direct evidence), Sections 2 and 3 of `../../TEXT.md`, `../../SENTENCES.md`, the supplied input part and this part's own working outputs were consulted locally. No earlier classification was consulted. The expected raw directories for the two input platforms do not exist. References beginning `raw-X1` or `raw-X2` are therefore treated as quoted inventory evidence, not as files inspected. No object was removed and no machine experiment was performed.

The original IDs are preserved verbatim. Prose avoids identifying users or machines. Documentation is used to establish object function; classification follows only Section 2.2 and the first indicator of Section 3. Inventory classification labels are ignored. Missing per-object facts give UNKNOWN rather than a speculative reading of the text. Generated status and persistent state are not declared holes simply because Section 2.5 assigns state handling to system design.

## Scripted homogeneous rules

### A — account entries: 59 rows

Every `kind=account` row supplies a user ID, group ID and login-shell field. It is an account, irrespective of whether interactive login is disabled. S2.2-15 explicitly requires accounts: MUST. No inference from the account name or intended daemon is needed. All rows were checked for the account-record shape. Ten manual checks:

- `debian-desktop-54a0a0356a`: UID 107, GID 118; false login shell still leaves an account.
- `debian-desktop-205e945769`: UID 42, GID 65534; nologin account.
- `debian-desktop-2b866190eb`: UID 104, GID 111; nologin account.
- `debian-desktop-ebda0cbba2`: UID 105, GID 112; nologin account.
- `debian-desktop-3fa3a857d8`: UID 34, GID 34; nologin account.
- `debian-desktop-8d1e409524`: UID 2, GID 2; nologin account.
- `debian-desktop-96a19ba1e6`: UID 1000, GID 1000; bash login account.
- `debian-desktop-c23681be3a`: UID 106, GID 117; nologin account.
- `debian-desktop-4900fca16b`: UID 1, GID 1; nologin account.
- `debian-desktop-8e4a0f0c6a`: UID 5, GID 60; nologin account.

### P — executable processes: 13 rows

The input identifies an executable and observed process IDs. Apply MUST under S2.2-9 and S2.2-12. The two kernel-thread aggregates and the sequencer are excluded from this rule and decided separately. The specific utility's higher-level purpose does not change the explicit running-program requirement. Ten manual checks:

- `debian-desktop-015af60fe8`: application executable, PID 4248.
- `debian-desktop-377e7f2465`: busybox executable, PID 4410.
- `debian-desktop-d8ee8908a9`: ps executable, PID 5455.
- `freebsd-966dfcae87`: shell executable, PID 1126.
- `freebsd-3f55296154`: device daemon executable, PID 527.
- `freebsd-288a960bcc`: DHCP client executable, PIDs 293, 296, 362.
- `freebsd-fdd8b25853`: init executable, PID 1.
- `freebsd-ca230cdfbe`: getty executable, nine observed PIDs.
- `freebsd-ef537795af`: SSH session executable, PIDs 1123, 1125.
- `freebsd-210417177a`: cron executable, PID 836.

### R — enabled rc services: 30 rows

All `kind=rc-service` entries explicitly say `true` and refer to the enabled-service inventory. These are startup/service shell scripts, including one-shot startup actions. Their code executes with system privileges and their execution supplies system actions. Apply MUST under S2.2-1, S2.2-2 and S2.2-10. This rule is about the executing service/script, not the logs, content or settings it may produce. Ten manual checks of enabled entries:

- `freebsd-03fa3830f7`: bgfsck, true.
- `freebsd-3f74f2c9a3`: cleanvar, true.
- `freebsd-dcd1432266`: cron, true.
- `freebsd-7c164f0a1e`: devd, true.
- `freebsd-64d35e706d`: devmatch, true.
- `freebsd-f2075842a4`: dmesg, true.
- `freebsd-c16e56505a`: firstboot_freebsd_update, true.
- `freebsd-2d5294aab2`: gptboot, true.
- `freebsd-ed204757d1`: growfs, true.
- `freebsd-cc5f87b39c`: growfs_fstab, true.

Primary documentation: https://docs.freebsd.org/en/articles/rc-scripting/ describes each basic service as having its own shell script: “script able to start the service, stop it, reload it, check its status.” The service utility manual, https://man.freebsd.org/cgi/man.cgi?format=html&query=service&sektion=8, defines `-e`: “List services that are enabled.”

## Individual non-stored rows

The other 25 non-stored rows are explicit per-ID decisions in `part-6.local.py`, not a blanket classification rule. Unit groups are assessed at the indicated functional level. The entries themselves list their member unit names; no unseen unit content is presumed. Service definitions launch external processes; mounts supply filesystem access; scopes and slices manage other processes; device units carry dependencies for other units. These effects are not settings confined to a single application's own interface. A completed one-shot service remains a service definition when the inventory says loaded/active/exited.

The two `*.not-found` groups identify absent unit definitions rather than installed services. Their display does not establish a service or socket to remove. Dependencies that reference those names are separate objects. Neither absence of a unit file nor the manager's display of absence is treated as installed program code.

The scheduler inventory contains no job entries, and the directory-only aggregates contain no individual directory names. Public program documentation cannot recover those missing facts; all three are UNKNOWN.

Supporting primary documentation and short exact excerpts:

- https://www.freedesktop.org/software/systemd/man/latest/systemd.device.html — “This may be used to define dependencies between devices and other units.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html — “encodes information about a file system mount point controlled and supervised by systemd.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.scope.html — “Scope units manage a set of system processes.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.slice.html — “A slice unit is a concept for hierarchically managing resources of a group of processes.”
- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html — “not-found” means “if no unit file was found for this unit”.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html — “encodes information about a process controlled and supervised by systemd.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.kill.html — “all remaining processes in the control group of this unit will be killed on unit stop”.
- https://docs.kernel.org/driver-api/basics.html — “When woken, the thread will run” `threadfn()` “with data as its argument.”
- https://raw.githubusercontent.com/freebsd/freebsd-src/main/share/man/man9/kproc.9 — “The main function for this kernel process to run.”
- https://raw.githubusercontent.com/freebsd/freebsd-src/stable/14/sys/dev/sound/midi/sequencer.c — `kproc_create` invokes `seq_eventthread`; the source names “Sequencer output /dev/sequencer (FM” and “synthesizer and MIDI output)”.
- https://man.freebsd.org/cgi/man.cgi?manpath=freebsd-release-ports&query=intpm&sektion=4 — “only smbus(4) controller function is implemented.”
- https://raw.githubusercontent.com/freebsd/freebsd-src/main/share/man/man4/smbus.4 — “system for the implementation of drivers to control various SMB devices”.

## Stored-object classifications

The three disjoint stored-object subsets and their row-specific documentation are recorded in `part-6.1.notes.md`, `part-6.2.notes.md`, and `part-6.3.notes.md`. Their notes are incorporated below after completion, so the required single notes file contains every scripted rule and its manual checks.

## Exact sentences used for the non-stored rows

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.

- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;

- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.

- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;

- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.

- **S3-2** If what the object does remains unknown, the case yields ?.


# Incorporated subset 1 notes

# Part 6: stored-object subset notes

The subset contains 183 input rows. Every row was inspected. Input IDs are preserved solely as identifiers. Only the assigned input, the fixed definition and public documentation were consulted. No removal, probe, or machine modification was performed. No earlier classification was consulted.

## Evidence limits

The referenced raw inventory directory is unavailable. The supplied evidence is therefore the available inventory evidence. Many rows have `members=1` while their evidence describes a directory group with `n` greater than one and at most four sampled filenames. These rows were not silently treated as complete file inventories. An UNKNOWN row records the specific missing information. Public program documentation can establish a standard file's role, but cannot supply this installation's unlisted objects, arbitrary script contents, database keys, or lock ownership.

A standard account file, shell startup file, documented executable-hook directory, or clearly identified historical log can establish its role without reproducing every contained value. By contrast, arbitrary scripts, mixed application profiles and unenumerated storage trees do not establish their members' functions. Uncertainty in those cases is factual, under S3-2, not a proposed extension of the definition. No design question from Section 2.5 was classified as a textual hole.

The classifications apply to the inventory objects, not to every possible object a directory could contain. Missing membership is not positive evidence of a mixture. MIXED requires established different decisions, not merely plausible differences. A database containing both password values and account policy is required for its policy role; the password value exemption remains intact.

## Scripted rules and hand checks

The serialization script retains previously written IDs and flushes after each newly written row. Explicit per-row calls encode the heterogeneous decisions. The following two homogeneous selections also use shared serialization:

1. Host command hooks and service transition links: MUST under S2.2-1, S2.2-2, S2.2-10 and S2.2-13. Shell startup/logout files are executed with shell rights; runlevel links select scripts which start or stop host services. This is a rule about documented executable/activation function, not filename suffix alone. Hand-checked ten rows: debian-desktop-5ecd8ad6ee, debian-desktop-2e520cea02, debian-desktop-31b4602da2, debian-desktop-78bcc39697, debian-desktop-8e766b28b8, debian-desktop-f032939066, debian-desktop-b1fb6e4c19, debian-desktop-4311df43fb, debian-desktop-3543b3a205, debian-desktop-2d36998dd6. The first eight contain documented runlevel start/stop links, the ninth is the system profile, and the tenth is an interactive shell startup file. The custom workload files were not included merely because they end in `.sh`.

2. Explicitly identified logs/history: NOT under S2.2-6. This is an enumerated selection of historical records, not a blanket rule for everything under the log directory. Hand-checked ten rows: debian-desktop-5ce874f910 (alternative changes), debian-desktop-83df02e6eb (package history/output), debian-desktop-9c96b64591 (failed login events), debian-desktop-93b020b2d3 (initialization output), debian-desktop-2954505d9d (initialization log), debian-desktop-81374794e5 (printing access log), debian-desktop-6f5cf081f0 (package actions), debian-desktop-1e4870c945 (font processing output), debian-desktop-e6b33c3854 (service journal), debian-desktop-698c23461f (previous login records). The failure-limit database, shell script and completion marker in the same directory were separately inspected and left UNKNOWN.

## Public documentation consulted

Short quotations below establish the standard roles used in the TSV. Documentation was read without applying its terminology as a classification rule.

- https://manpages.debian.org/bookworm/initramfs-tools-core/mkinitramfs.8.en.html — “All finding of the root device happens in this early userspace.”
- https://man7.org/linux/man-pages/man5/passwd.5.html — “The /etc/passwd file is a text file that describes user login accounts for the system.”
- https://man7.org/linux/man-pages/man5/group.5.html — “The /etc/group file is a text file that defines the groups on the system.”
- https://manpages.debian.org/bookworm/passwd/gshadow.5.en.html — “Administrators can change the password or the members of the group.”
- https://manpages.debian.org/bookworm/passwd/shadow.5.en.html — “In case of an account expiration, the user shall not be allowed to login.” Also: “Backup file for /etc/shadow.”
- https://manpages.debian.org/bookworm/passwd/subgid.5.en.html — “Subgid authorizes a group id to map ranges of group ids from its namespace into child namespaces.” Also: “Backup file for /etc/subgid.”
- https://manpages.debian.org/bookworm/passwd/subuid.5.en.html — “Subuid authorizes a user id to map ranges of user ids from its namespace into child namespaces.” Also: “Backup file for /etc/subuid.”
- https://man7.org/linux/man-pages/man8/pam_env.8.html — “Second a file (/etc/environment by default) with simple KEY=VAL pairs on separate lines will be read.”
- https://man7.org/linux/man-pages/man5/fstab.5.html — “The file fstab contains descriptive information about the filesystems the system can mount.”
- https://man7.org/linux/man-pages/man5/hostname.5.html — “The /etc/hostname file configures the name of the local system.”
- https://man7.org/linux/man-pages/man5/hosts.5.html — “This file is a simple text file that associates IP addresses with hostnames, one line per IP address.”
- https://manpages.debian.org/bookworm/libwrap0/hosts_access.5.en.html — “A non-existing access control file is treated as if it were an empty file.” This prevents inferring an active access rule from existence alone.
- https://man7.org/linux/man-pages/man5/networks.5.html — “This file is read by the route(8) and netstat(8) utilities.”
- https://man7.org/linux/man-pages/man5/nsswitch.conf.5.html — “to determine the sources from which to obtain name-service information in a range of categories, and in what order.”
- https://man7.org/linux/man-pages/man5/resolv.conf.5.html — “The resolver configuration file contains information that is read by the resolver routines the first time they are invoked by a process.”
- https://man7.org/linux/man-pages/man5/shells.5.html — “valid login shells. This file is consulted by chsh(1) and available to be queried by other programs.”
- https://man7.org/linux/man-pages/man5/localtime.5.html — “If /etc/localtime is missing, the default "UTC" timezone is used.” The input link points to UTC, so the same timezone survives removal.
- https://man7.org/linux/man-pages/man5/machine-id.5.html — “The /etc/machine-id file contains the unique machine ID of the local system that is set during installation or boot.”
- https://manpages.debian.org/bookworm/mailcap/mailcap.5.en.html — “It will be passed to the shell via the system(3) facility.”
- https://manpages.debian.org/bookworm/libpaper1/papersize.5.en.html — “The papersize file is used to specify the preferred paper size to use by available commands and programs generating documents.”
- https://man7.org/linux/man-pages/man5/motd.5.html — “The contents of /etc/motd are displayed by login(1) after a successful login but just before it executes the login shell.”
- https://manpages.debian.org/bookworm/bash/bash.1.en.html — “The systemwide initialization file, executed for login shells”. Also: “bash reads and executes commands from the file ~/.bash_logout, if it exists.”
- https://www.gnu.org/software/grub/manual/grub/html_node/Simple-configuration.html — “making complex changes to shell scripts stored in /etc/grub.d/.” Direct retrieval timed out; the same primary manual passage was retrieved through search.
- https://manpages.debian.org/bookworm/init-system-helpers/update-rc.d.8.en.html — “These links are run by init when it changes runlevels; they are generally used to start and stop system services such as daemons.”
- https://manpages.debian.org/bookworm/openssh-server/sshd.8.en.html — “Lists the public keys (DSA, ECDSA, Ed25519, RSA) that can be used for logging in as this user.”
- https://man7.org/linux/man-pages/man7/hier.7.html — “Man pages associated with locally installed programs.” The input documentation link targets that manual hierarchy.
- https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html — “Watch font files being scanned to build caches”. Also: “This file is automatically maintained by fontconfig.”
- https://gstreamer.freedesktop.org/documentation/gstreamer/gstregistry.html — “The primary source, at all times, of plugin information is each plugin file itself.” Also: “the plugin is loaded and the cache updated.”
- https://docs.mesa3d.org/envvars.html — “if set to true, disables the on-disk shader cache.”
- https://pip.pypa.io/en/stable/topics/caching/ — “Pip provides an on-by-default caching, designed to reduce the amount of time spent on duplicate downloads and builds.”
- https://man7.org/linux/man-pages/man8/ldconfig.8.html — “Ignore auxiliary cache file.”
- https://manpages.debian.org/bookworm/man-db/mandb.8.en.html — “If a database does not exist, it will create it.”
- https://specifications.freedesktop.org/basedir/latest/ — “user-specific non-essential (cached) data”. This general directory convention alone was not taken to establish every member's function.
- https://manpages.debian.org/bookworm/kmod/modules.5.en.html — “The /etc/modules file contains the names of kernel modules that are to be loaded at boot time, one per line.” Missing actual entries matter.

## Fixed sentences used

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-11** Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.
- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- **S3-2** If what the object does remains unknown, the case yields ?.

## Verification

The script verified 183 unique output IDs exactly equal the assigned input IDs; decisions and field word limits are valid.

MUST: 38; NOT: 39; HOLE: 0; UNKNOWN: 106; MIXED: 0.


# Incorporated subset 2 notes

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


# Incorporated subset 3 notes

# Part 6, c1 subset 3

Scope: 54 stored-object rows from the supplied part, excluding boot and system configuration directories. Only the task input, the fixed text and public primary documentation were consulted. Raw inventory files are unavailable. No object was removed. Directory counts in evidence include entries not enumerated by the sample; large incomplete groups remain UNKNOWN. No inference of file contents from an upstream sample is made.

## Scripted rule: logs

S2.2-6: "records of the past—logs, history;"

A row explicitly identifying an event log or login history is NOT. The completion-marker file is excluded because its control-flow role is unknown. Hand-checked cases: freebsd-3f3dc85096 (authentication log), freebsd-1a6382c15a (scheduler log), freebsd-17935511d8 (daemon log), freebsd-3577a2c8c2 (debug log), freebsd-71ac7977fa (device-event log), freebsd-a3218f48ea (printing error log), freebsd-063e60271f (mail log), freebsd-91a21a61f1 (system messages), freebsd-bf93d84cc6 (initialization log), freebsd-c1a31fd033 (connection log). Each is one named log, not an arbitrary directory. Login histories were separately checked against https://man.freebsd.org/cgi/man.cgi?query=utmpx&format=html: "Log of all entries, sorted by date of addition."

Every remaining row was decided individually; the serialization script only writes those explicit decisions.

## Primary documentation and supporting passages

- https://man.freebsd.org/cgi/man.cgi?query=sh&format=html: "A login shell first reads commands from the files /etc/profile"; "Default shell resources." The manual describes the profile, ENV and shell-resource execution mechanism.
- https://man.freebsd.org/cgi/man.cgi?query=tcsh&format=html: "Non-login shells read only /etc/csh.cshrc and ~/.tcshrc or ~/.cshrc on startup." Login startup also executes the login file.
- https://man.freebsd.org/cgi/man.cgi?query=vi&format=html: "Execute an ex command." The manual identifies the ex startup files; the inventory independently reports the executed `set number` command. S2.2-13 makes this code despite its setting purpose.
- https://man.freebsd.org/cgi/man.cgi?query=mail&format=html: "commands in the user's personal command file ~/.mailrc are executed"; "Executes the shell". The command language is not confined to displaying mail.
- https://raw.githubusercontent.com/freebsd/freebsd-src/main/share/skel/dot.mail_aliases: ".mail_aliases - private mail aliases". This establishes intended purpose only; actual contents and sourcing are unavailable.
- https://raw.githubusercontent.com/freebsd/freebsd-src/main/share/skel/dot.mailrc: "source ~/.mail_aliases". This documents the default sourcing mechanism, not the actual installed contents.
- https://man.freebsd.org/cgi/man.cgi?query=login.conf&format=html: "this file is used by login(1) to set user-defined environment settings". These settings propagate into the login session, beyond one program.
- https://man.freebsd.org/cgi/man.cgi?query=sshd&format=html: "AuthorizedKeysFile specifies the files containing public keys for public key authentication". The inventory identifies authorized-key files.
- https://man.freebsd.org/cgi/man.cgi?query=k5login&format=html: "Anyone with valid tickets for a principal in the file is allowed host access with the UID of the user".
- https://man.freebsd.org/cgi/man.cgi?query=pam.conf&format=html: "The PAM library searches for policies in the following files, in decreasing order of preference". The inventory identifies the privilege tool's PAM policy.
- https://man.freebsd.org/cgi/man.cgi?query=pkg.conf&format=html: "pkg.conf is the system-wide configuration file used by the pkg(8) tools." Its actual directives are not provided.
- https://man.freebsd.org/cgi/man.cgi?query=sudo.conf&format=html: "It is used to configure sudo plugins, plugin-agnostic path names, debug flags, and other settings." Actual enabled directives are unknown.
- https://man.freebsd.org/cgi/man.cgi?query=sudo_logsrvd.conf&format=html: "The sudo_logsrvd.conf file is used to configure the sudo_logsrvd log server." Configuration can involve listening addresses, storage and logging; actual values are unavailable.
- https://man.freebsd.org/cgi/man.cgi?query=sudoers&format=html: "The sudoers policy plugin determines a user's sudo privileges." Applies to the main policy and included policy directory.
- https://man.freebsd.org/cgi/man.cgi?query=pkg-clean&format=html: "Delete all cached packages including those which have not been superseded by newer versions yet and are still in use." Downloaded archive copies are distinct from installed executable programs.
- https://man.freebsd.org/cgi/man.cgi?query=savecore&format=html: "the copies are not attempted." This is the documented consequence of the minimum-free-space threshold. The setting governs only savecore's dump-saving operation.
- https://man.freebsd.org/cgi/man.cgi?query=dhclient&format=html: "if they are determined to be valid, they are used until either they expire or the DHCP server becomes available." Saved leases enable network use without a responding server. Actual lease validity is not supplied.
- https://man.freebsd.org/cgi/man.cgi?query=etcupdate&format=html: "To perform a three-way merge, etcupdate keeps copies of the current and previous versions of files that it manages." The inventory gives only four samples of hundreds of members.
- https://man.freebsd.org/cgi/man.cgi?query=freebsd-update&format=html: "temporary files, downloaded updates, and files required for rollback." This broad directory is not established as homogeneous from its four samples.
- https://man.freebsd.org/cgi/man.cgi?query=mergemaster&format=html: "Location to store the list of mtree values for AUTO_UPGRADE purposes". Historical file fingerprints provide a baseline for detecting local changes.
- https://man.freebsd.org/cgi/man.cgi?query=services&format=html: "If \"db\" is specified as source in the nsswitch.conf(5), /var/db/services.db is searched." Neither the lookup configuration nor fallback behavior on this machine is supplied.
- https://man.freebsd.org/cgi/man.cgi?query=msgs&format=html: "an error will be displayed if /var/msgs/bounds does not exist." This bounds file is functional metadata; the given sample contains it.
- https://raw.githubusercontent.com/freebsd/freebsd-src/main/usr.sbin/ypserv/Makefile.yp: "These are commands which this Makefile needs to properly rebuild the NIS databases." The supplied directory contains the makefile and its symlink; make executes recipes with caller rights.
- https://man.freebsd.org/cgi/man.cgi?query=nuageinit&format=html: "because the user_data provided is a script." The cached user-data file can instead contain configuration values, so its name does not establish its contents.

## Limits of inference

Shell startup files and policy/key files have documented functional roles identified by their standard filenames. Whether a file contains active directives, rather than comments, matters most where the documented format mixes materially different categories; those cases are UNKNOWN here. The private alias file is not established as sourced on this installation. The large shared-data, update, package-database and runtime groups do not have full member listings. The bootstrap completion and cleanup marker names have no supplied producer/consumer code.

## Exact fixed-text sentences cited

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S3-2** If what the object does remains unknown, the case yields ?.


## Cross-subset evidence corrections

Four stored script rows initially had only filename evidence within their assigned subset. The service rows in the same input explicitly identify those files as bash command arguments. Their execution as shell code is established by that corroborating inventory, so S2.2-10 requires MUST without needing the scripts' application-specific contents. The merged output and subset output incorporate these corrections.

- `debian-desktop-fb87e8bdd4`: execution established by service row `debian-desktop-53d095e912`.
- `debian-desktop-09fa2e5ce3`: execution established by service row `debian-desktop-fdb6cb41a8`.
- `debian-desktop-2438267eef`: execution established by service row `debian-desktop-ba3d3e02a2`.
- `debian-desktop-d54b59c426`: execution established by service row `debian-desktop-7218a536a4`.

## Structural verification

`part-6.verify.py` verified all 528 rows against the input: exact ID set and count, each ID once, exact header, allowed decisions, nonempty fields, sentence IDs restricted to Section 2.2 and Section 3, valid basis prefixes, and the 15/30-word limits. `part-6.done` contains the resulting decision counts. This is a structural check, not an experimental test of the hypothesis. The separate bounded review is recorded in `part-6.review.md`.


## Review evidence corrections

The review identified three path-only configuration rows whose initial MUST reasons presumed effective local values. Public documentation establishes their formats and possible effects, but the inventory does not expose those values. The identical evidence limitation applies to the second filesystem-table row. These four decisions are UNKNOWN under S3-1 and S3-2; no missing fact is repaired by assuming default contents.

- `debian-desktop-5deb3892cc`: local contents and effective values are unavailable.
- `debian-desktop-4cce813fe8`: local contents and effective values are unavailable.
- `freebsd-4cce813fe8`: local contents and effective values are unavailable.
- `debian-desktop-868a743843`: local contents and effective values are unavailable.

The alternative-link directory remains UNKNOWN: sampled documentation links are identifiable, but the provided executable-target link does not establish its active generic-name consumer or complete directory membership.

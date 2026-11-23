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

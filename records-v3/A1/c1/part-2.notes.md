# Part 2 classification c1

Decisions use only Section 2.2 and S3-1/S3-2, with functions established from the assigned inventory and cited public documentation. No objects were removed. No other classification was consulted. `raw:` basis paths are relative to `A1/in/raw/`; `evidence` refers to the matching input row.

Completed rows were appended and flushed individually. All existing IDs were retained; documented review corrections replaced affected fields without adding or dropping IDs. Component notes below document homogeneous rules, ten manual checks per rule, and individual exceptions. The separate review is recorded in `part-2.review.md`.

# Accounts, loaded modules, and observed processes

Only `../in/part-2.tsv`, the relevant `A1/in/raw/debian/` inventory files, the fixed text, and the public sources below supplied evidence. No removal was performed. Inventory classification language was disregarded. Decisions concern the object represented by each row, not the text file reporting it.

## Rule A: accounts

All 27 account rows are account definitions confirmed by the seven fields in `accounts.txt`. S2.2-15 explicitly requires accounts, without limiting this to interactive accounts. Apply MUST to each account row. No account passwords are classified by this rule.

Documentation: https://man7.org/linux/man-pages/man5/passwd.5.html — “The /etc/passwd file is a text file that describes user login accounts for the system.”

Ten manual checks against the account records:

- debian-205e945769: UID 42, noninteractive account.
- debian-3fa3a857d8: UID 34, noninteractive account.
- debian-8d1e409524: UID 2, noninteractive account.
- debian-96a19ba1e6: UID 1000, interactive shell.
- debian-4900fca16b: UID 1, noninteractive account.
- debian-8e4a0f0c6a: UID 5, noninteractive account.
- debian-707e10c2e4: UID 39, noninteractive account.
- debian-3413994e24: UID 38, noninteractive account.
- debian-55e4967557: UID 7, noninteractive account.
- debian-cbaf0b4232: UID 0, privileged account.

Each record is an account, so the explicit sentence fits regardless of shell or UID.

## Rule K: loaded kernel modules

All 52 module rows are observed loaded modules in `modules.txt`, with corresponding module file paths in the input. They execute native code in kernel space, with the kernel's privileges, rather than in an interface restricting their capabilities. Apply MUST using S2.2-10. This is a code rule, not an inference that every module's removal prevents boot; redundant implementations do not override the explicit code requirement.

Documentation: https://man7.org/linux/man-pages/man2/init_module.2.html — “init_module() loads an ELF image into kernel space”. The same description states that loading runs the module's initialization function. https://docs.kernel.org/kbuild/modules.html — “after linking, will result in the kernel module <module_name>.ko.”

Ten manual checks against `modules.txt` and the input file paths:

- debian-ddb5a87d9a: aesni_intel, loaded, native crypto module path.
- debian-0074a80686: ata_generic, loaded, ATA driver module path.
- debian-4ef0af6396: ata_piix, loaded, ATA driver module path.
- debian-4fb00be8be: autofs4, loaded, filesystem module path.
- debian-d8aafdbe20: binfmt_misc, loaded, binary-format module path.
- debian-70a3c6eeb0: button, loaded, ACPI driver module path.
- debian-3b459c779e: cdrom, loaded, CD-ROM driver module path.
- debian-37eece24d6: configfs, loaded, filesystem module path.
- debian-3817fdb2ed: crc32_pclmul, loaded, native crypto module path.
- debian-ec81aeacb8: crc32c_intel, loaded, native crypto module path.

Each checked object is loaded kernel code. The inventory usage count is not a permissions boundary or an exemption.

## Rule P: observed executable processes

Apply MUST under S2.2-9 and S2.2-12 to the 14 executable process rows. `processes.txt` directly reports running commands; `process-executables.tsv` resolves executables where available. No assertion that a process is a saved setting is needed. The row for `ps` is observed in the process listing even though the executable-resolution snapshot missed this short-lived process.

Ten manual checks against both process inventories:

- debian-ce95966cbb: PID 805 executes bash.
- debian-670c720118: PID 501 executes the system bus daemon.
- debian-0605c303f7: PID 523 executes Python for the upgrade shutdown helper.
- debian-add864bf46: PID 804 executes sudo.
- debian-aee2bf821c: PID 286 runs device management; executable resolution names udevadm.
- debian-42c14762fe: PIDs 1, 579, 580 resolve to the service manager executable.
- debian-7b2f0c0e4f: PID 260 executes the journal daemon, not the journal records.
- debian-a7da54431d: PID 504 executes the login manager.
- debian-ca73c5eaa2: PID 445 executes the network manager.
- debian-b66da72753: PID 417 executes the resolver daemon.

Every checked row is an observed separate executable process, so the explicit program requirement applies without further assumptions about its individual configuration.

## Individual case: kernel threads

`debian-89ce5c5668` groups observed kernel threads. `processes.txt` identifies kernel task names and `process-executables.tsv` has no userspace executable for them. This is kernel code running with kernel privileges, meeting S2.2-10; the group is homogeneous at that decisive boundary. No claim that each thread is a separate installed userspace program is made.

Documentation: https://docs.kernel.org/driver-api/basics.html — “This helper function creates and names a kernel thread.” The kthread_create_on_node description explains that waking the task runs its supplied function. All listed members have the same MUST decision.

## Application and scope

`part-2.core.py` applies these three rules and the single kernel-thread case, appending only missing IDs to `part-2.tsv` and flushing each row. Raw paths in the basis field are relative to `A1/in/raw/`. Public documentation supplements the inventories; the inventories establish that these specific objects exist or execute.

## Exact deciding text

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;

- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.

- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;

- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.

- **S3-2** If what the object does remains unknown, the case yields ?.



# Unit classifications, part 2

Only the assigned unit kinds in `../in/part-2.tsv` were considered. Inventory class labels were ignored. Sources inspected: `../in/raw/debian/units.txt`, `unit-paths.txt`, `user-list-units.txt`, `user-unit-paths.txt`, and `user-manager-state.txt`. No object was removed.

## Sentences used

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

## Documentation

- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html : “A unit file is a plain text ini-style file that encodes information about a service”. Unit files also describe activation, dependency, mounting, and resource management objects; they are not themselves the processes they configure.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.target.html : “Target units are used to group units and to set synchronization points for ordering dependencies with other unit files.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.device.html : “Many unit types automatically acquire dependencies on device units of devices they require.” Device units dynamically expose kernel device availability; mount and socket dependencies can use them.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html : “Mount points created at runtime (independently of unit files or /etc/fstab) will be monitored by systemd”. These units represent mounts, including mounts created outside the manager.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.scope.html : “Scope units manage a set of system processes.” They group externally created processes for resource management.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.slice.html : “A slice unit is a concept for hierarchically managing resources of a group of processes.” The hierarchy is implemented through kernel control groups, including the root slice.
- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html : “List units that systemd currently has in memory.” Listing includes referenced units; a displayed name does not establish an installed unit file.

## Rule U: configured functional units

Applied by script to the 155 singular system-unit/user-unit rows. Every row reports a loaded unit, a fragment, and its concrete service, activation, synchronization, filesystem, or resource-management function. Removing such a unit removes the corresponding managed action or activation/ordering capability: MUST by S2.2-1 and S2.2-2. S2.2-13 makes value-based unit configuration settings, but S2.2-7 only exempts settings in force *only inside* one program. Starting other processes, ordering their execution, mounting kernel interfaces, and managing their resources have effects outside the manager. Unit configuration is not an internal theme or preference. Neither inactive status nor completed one-shot status changes the available unit function. Logging and cache-maintenance services are actions, not the logs and caches they produce.

Ten manually checked rows, checked against their input descriptions and raw unit listing:

1. debian-29a7d582ee — apparmor.service loads security profiles; removal loses managed profile loading, an external security effect.
2. debian-4a8bc234ee — apt-daily-upgrade.service performs package upgrade/cleanup; inactive status does not remove the configured action.
3. debian-aa6c43f73c — apt-daily-upgrade.timer schedules that external package-maintenance action.
4. debian-77462850bc — basic.target groups/orders basic-system activation; the target mechanism changes process activation dependencies.
5. debian-b2eac0adbc — dbus.service runs the system message bus used between processes.
6. debian-06be1b0d47 — dbus.socket provides the system bus socket activation endpoint.
7. debian-16081f0750 — dev-hugepages.mount exposes a kernel filesystem to processes.
8. debian-46b677ba51 — systemd-ask-password-console.path watches requests to activate an external password-response service.
9. debian-e92ded7963 — user.slice organizes resources for user/session processes through control groups.
10. debian-6d902f1685 — user basic.target orders and groups user-unit activation, not a preference confined to an application interface.

## Individually assessed grouped rows

Despite `members=1` in the input column, the evidence enumerates multiple units. Decisions below cover all enumerated members, not an invented single file.

- debian-a3f2270221 and debian-88335c6c87: every enumerated device unit dynamically exposes a device and supplies its availability to unit dependencies. MUST: removing that availability/dependency object removes its device-dependent activation capability. No assertion that these are stored configuration files or firmware settings is needed.
- debian-18fb2985ed: all members are mounted filesystems: root, EFI, service credential mounts, and user runtime storage. MUST: removing the represented mount removes its filesystem access. The object classified is the mount unit, not a text copy of inventory output.
- debian-565df89b5f: all members are observed mounts, additionally including hugepages, message queues, binary-format registration, FUSE control, configuration, debugging, and tracing filesystems. MUST for the represented mounts and their access to kernel interfaces, even though the user manager discovers them from mountinfo.
- debian-9994d7ebc4: all enumerated units are not-found/inactive/dead. NOT: these are references to unavailable unit definitions, not installed services or mount configurations. Removing an unavailable reference removes no existing unit capability. This does not classify the hypothetical installed programs bearing those names.
- debian-97fdaec6aa: the sole block-device target is not-found/inactive/dead in the user manager. NOT on the same individually verified grounds: no configured target capability exists to remove.
- debian-0ff15b2741: init.scope and session-4.scope manage actual manager/session process groups. MUST: these are active process-management objects, not log records about the processes.
- debian-3bc8c8458c: init.scope manages the active user manager's process group. MUST for the same process-management function, individually checked in the user listing.
- debian-253d752b01: all named slices form the active resource hierarchy for system, template-instance, and user process groups. MUST because the hierarchy manages kernel resources for those processes.
- debian-b855166ba5: the root user slice supplies the root of that resource hierarchy. MUST for its actual process-resource management function.

The grouped assessments are individual decisions supported by the listed members and documentation, not additional bulk rules.


# Package classification notes

Only the supplied package rows and the permitted inventory were used. Package status establishes installation, not function. Official Debian package descriptions establish functions. The release index and English descriptions were read from:

- https://deb.debian.org/debian/dists/bookworm/main/binary-amd64/Packages.xz
- https://deb.debian.org/debian/dists/bookworm/main/i18n/Translation-en.xz

Descriptions were inspected for program, library, data, configuration and dependency-only roles. Package installation alone was never used as a MUST rule. Package rows represent packages, not grouped directory members; a package containing code and ancillary documentation is classified by its executable contribution.

## Rule P: executable programs

S2.2-9: “a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;”

Apply MUST to documented executable utilities, daemons, interpreters and operating-system code. The installation evidence establishes their presence; the documented function supplies the removal reasoning. Pure data, configuration and dependency-only packages were excluded and individually decided.

Ten hand-checked rule P rows:
- debian-7ac0ecf630 (adduser): add and remove users and groups. The described object is an executable program, so rule P fits.
- debian-52a6e89c50 (apt): commandline package manager. The described object is an executable program, so rule P fits.
- debian-7e581bffc1 (bash): GNU Bourne Again SHell. The described object is an executable program, so rule P fits.
- debian-aeb3d018e8 (curl): command line tool for transferring data with URL syntax. The described object is an executable program, so rule P fits.
- debian-e99d8e16f1 (dpkg): Debian package management system. The described object is an executable program, so rule P fits.
- debian-9573ee576e (grep): GNU grep, egrep and fgrep. The described object is an executable program, so rule P fits.
- debian-dd3aa38850 (openssh-server): secure shell (SSH) server, for secure access from remote machines. The described object is an executable program, so rule P fits.
- debian-50e2bf1471 (systemd): system and service manager. The described object is an executable program, so rule P fits.
- debian-b48d271d11 (tar): GNU version of the tar archiving utility. The described object is an executable program, so rule P fits.
- debian-21b48c46af (vim): Vi IMproved - enhanced vi editor. The described object is an executable program, so rule P fits.

## Rule L: directly executed library/module code

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

Apply MUST to runtime shared libraries and Python modules loaded into the consuming program. Their API code executes with the caller’s rights. A library implementing a sandbox remains executable host code; possible confined inputs to that library are different objects. Prefixes only dispatch already-reviewed descriptions; data/common/dependency exceptions are removed first.

Ten hand-checked rule L rows:
- debian-5d52ef819a (libacl1): access control list - shared library. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-66f672bca8 (libc6): GNU C Library: Shared libraries. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-5a7fa751a2 (libcurl4): easy-to-use client-side URL transfer library (OpenSSL flavour). Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-6643bd2a37 (libssl3): Secure Sockets Layer toolkit - shared libraries. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-f72e8ae6ef (libsqlite3-0): SQLite 3 shared library. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-2611cd5289 (libzstd1): fast lossless compression algorithm. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-ebf827c02b (python3-apt): Python 3 interface to libapt-pkg. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-a51a155fba (python3-requests): elegant and simple HTTP library for Python3, built for human beings. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-5f4f0aab5c (python3-yaml): YAML parser and emitter for Python3. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-0fb500bd4c (python3-jinja2): small but fast and easy to use stand-alone template engine. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.

## Individually decided cases

The script special-case table contains the individual reasoning. In addition, libpython3-stdlib was checked by its file list and description: it is a dependency package without runtime library code itself; further dependency-semantics review below establishes MUST. Pure metapackages are not silently treated as the executable packages they depend on. No package removal or other probe was performed.

Selected package file lists are preserved in part-2.packages.filelists.json, each with its URL. They establish, for example, gcc-12-base has only documents, while vim-common also supplies /usr/bin/helpztags.

Additional sources:

- https://manpages.debian.org/bookworm/libaudit-common/libaudit.conf.5.en.html: “The file /etc/libaudit.conf contains configuration information for user space applications that link to libaudit.”
- https://manpages.debian.org/bookworm/libtirpc-common/netconfig.5.en.html: “The netconfig file defines a list of” transport names and descriptions (transport table evidence).
- https://packages.debian.org/bookworm/linux-image-6.1.0-56-cloud-amd64: “Linux 6.1 for x86-64 cloud (signed)”.
- https://packages.debian.org/bookworm/libpython3-stdlib: “This package is a dependency package”.

## Package documentation excerpts

The following short exact title excerpts are from the official package descriptions. The runtime/data distinction also used their full descriptions during classification.
- https://packages.debian.org/bookworm/libacl1: “access control list - shared library”.
- https://packages.debian.org/bookworm/adduser: “add and remove users and groups”.
- https://packages.debian.org/bookworm/apparmor: “user-space parser utility for AppArmor”.
- https://packages.debian.org/bookworm/libapparmor1: “changehat AppArmor library”.
- https://packages.debian.org/bookworm/apt: “commandline package manager”.
- https://packages.debian.org/bookworm/apt-utils: “package management related utility programs”.
- https://packages.debian.org/bookworm/libapt-pkg6.0: “package management runtime library”.
- https://packages.debian.org/bookworm/apt-listchanges: “package change history notification tool”.
- https://packages.debian.org/bookworm/libargon2-1: “memory-hard hashing function - runtime library”.
- https://packages.debian.org/bookworm/libattr1: “extended attribute handling - shared library”.
- https://packages.debian.org/bookworm/libaudit-common: “Dynamic library for security auditing - common files”.
- https://packages.debian.org/bookworm/libaudit1: “Dynamic library for security auditing”.
- https://packages.debian.org/bookworm/base-files: “Debian base system miscellaneous files”.
- https://packages.debian.org/bookworm/base-passwd: “Debian base system master password and group files”.
- https://packages.debian.org/bookworm/bash: “GNU Bourne Again SHell”.
- https://packages.debian.org/bookworm/bash-completion: “programmable completion for the bash shell”.
- https://packages.debian.org/bookworm/bind9-host: “DNS Lookup Utility”.
- https://packages.debian.org/bookworm/bind9-libs: “Shared Libraries used by BIND 9”.
- https://packages.debian.org/bookworm/python3-blinker: “Fast, simple object-to-object and broadcast signaling (Python3)”.
- https://packages.debian.org/bookworm/libbrotli1: “library implementing brotli encoder and decoder (shared libraries)”.
- https://packages.debian.org/bookworm/libbz2-1.0: “high-quality block-sorting file compressor library - runtime”.
- https://packages.debian.org/bookworm/ca-certificates: “Common CA certificates”.
- https://packages.debian.org/bookworm/libdebconfclient0: “Debian Configuration Management System (C-implementation library)”.
- https://packages.debian.org/bookworm/genisoimage: “Creates ISO-9660 CD-ROM filesystem images”.
- https://packages.debian.org/bookworm/python3-chardet: “Universal Character Encoding Detector (Python3)”.
- https://packages.debian.org/bookworm/cloud-init: “initialization system for infrastructure cloud instances”.
- https://packages.debian.org/bookworm/cloud-initramfs-growroot: “automatically resize the root partition on first boot”.
- https://packages.debian.org/bookworm/cloud-guest-utils: “cloud guest utilities”.
- https://packages.debian.org/bookworm/cloud-image-utils: “cloud image management utilities”.
- https://packages.debian.org/bookworm/cloud-utils: “metapackage for installation of upstream cloud-utils source”.
- https://packages.debian.org/bookworm/python3-configobj: “simple but powerful config file reader and writer for Python 3”.
- https://packages.debian.org/bookworm/coreutils: “GNU core utilities”.
- https://packages.debian.org/bookworm/cpio: “GNU cpio -- a program to manage archives of files”.
- https://packages.debian.org/bookworm/libcryptsetup12: “disk encryption support - shared library”.
- https://packages.debian.org/bookworm/curl: “command line tool for transferring data with URL syntax”.
- https://packages.debian.org/bookworm/libcurl3-gnutls: “easy-to-use client-side URL transfer library (GnuTLS flavour)”.
- https://packages.debian.org/bookworm/libcurl4: “easy-to-use client-side URL transfer library (OpenSSL flavour)”.
- https://packages.debian.org/bookworm/libsasl2-2: “Cyrus SASL - authentication abstraction library”.
- https://packages.debian.org/bookworm/libsasl2-modules-db: “Cyrus SASL - pluggable authentication modules (DB)”.
- https://packages.debian.org/bookworm/dash: “POSIX-compliant shell”.
- https://packages.debian.org/bookworm/libdb5.3: “Berkeley v5.3 Database Libraries [runtime]”.
- https://packages.debian.org/bookworm/dbus: “simple interprocess messaging system (system message bus)”.
- https://packages.debian.org/bookworm/dbus-bin: “simple interprocess messaging system (command line utilities)”.
- https://packages.debian.org/bookworm/dbus-daemon: “simple interprocess messaging system (reference message bus)”.
- https://packages.debian.org/bookworm/dbus-session-bus-common: “simple interprocess messaging system (session bus configuration)”.
- https://packages.debian.org/bookworm/dbus-system-bus-common: “simple interprocess messaging system (system bus configuration)”.
- https://packages.debian.org/bookworm/libdbus-1-3: “simple interprocess messaging system (library)”.
- https://packages.debian.org/bookworm/python3-dbus: “simple interprocess messaging system (Python 3 interface)”.
- https://packages.debian.org/bookworm/debconf: “Debian configuration management system”.
- https://packages.debian.org/bookworm/python3-debconf: “interact with debconf from Python 3”.
- https://packages.debian.org/bookworm/debian-archive-keyring: “GnuPG archive keys of the Debian archive”.
- https://packages.debian.org/bookworm/debianutils: “Miscellaneous utilities specific to Debian”.
- https://packages.debian.org/bookworm/runit-helper: “dh-runit implementation detail”.
- https://packages.debian.org/bookworm/diffutils: “File comparison utilities”.
- https://packages.debian.org/bookworm/python3-distro-info: “information about distributions' releases (Python 3 module)”.
- https://packages.debian.org/bookworm/distro-info-data: “information about the distributions' releases (data files)”.
- https://packages.debian.org/bookworm/dpkg: “Debian package management system”.
- https://packages.debian.org/bookworm/libduktape207: “embeddable Javascript engine, library”.
- https://packages.debian.org/bookworm/e2fsprogs: “ext2/ext3/ext4 file system utilities”.
- https://packages.debian.org/bookworm/libcom-err2: “common error description library”.
- https://packages.debian.org/bookworm/libext2fs2: “ext2/ext3/ext4 file system libraries”.
- https://packages.debian.org/bookworm/libss2: “command-line interface parsing library”.
- https://packages.debian.org/bookworm/logsave: “save the output of a command in a log file”.
- https://packages.debian.org/bookworm/libefiboot1: “Library to manage UEFI variables”.
- https://packages.debian.org/bookworm/libefivar1: “Library to manage UEFI variables”.
- https://packages.debian.org/bookworm/libelf1: “library to read and write ELF files”.
- https://packages.debian.org/bookworm/ethtool: “display or change Ethernet device settings”.
- https://packages.debian.org/bookworm/libexpat1: “XML parsing C library - runtime library”.
- https://packages.debian.org/bookworm/file: “Recognize the type of data in a file using "magic" numbers”.
- https://packages.debian.org/bookworm/libmagic-mgc: “File type determination library using "magic" numbers (compiled magic file)”.
- https://packages.debian.org/bookworm/libmagic1: “Recognize the type of data in a file using "magic" numbers - library”.
- https://packages.debian.org/bookworm/findutils: “utilities for finding files--find, xargs”.
- https://packages.debian.org/bookworm/libfreetype6: “FreeType 2 font engine, shared library files”.
- https://packages.debian.org/bookworm/libfstrm0: “Frame Streams (fstrm) library”.
- https://packages.debian.org/bookworm/libfuse2: “Filesystem in Userspace (library)”.
- https://packages.debian.org/bookworm/libfuse3-3: “Filesystem in Userspace (library) (3.x version)”.
- https://packages.debian.org/bookworm/gcc-12-base: “GCC, the GNU Compiler Collection (base package)”.
- https://packages.debian.org/bookworm/libgcc-s1: “GCC support library”.
- https://packages.debian.org/bookworm/libstdc++6: “GNU Standard C++ Library v3”.
- https://packages.debian.org/bookworm/libgdbm6: “GNU dbm database routines (runtime version)”.
- https://packages.debian.org/bookworm/gdisk: “GPT fdisk text-mode partitioning tool”.
- https://packages.debian.org/bookworm/gettext-base: “GNU Internationalization utilities for the base system”.
- https://packages.debian.org/bookworm/libglib2.0-0: “GLib library of C routines”.
- https://packages.debian.org/bookworm/libc-bin: “GNU C Library: Binaries”.
- https://packages.debian.org/bookworm/libc-l10n: “GNU C Library: localization files”.
- https://packages.debian.org/bookworm/libc6: “GNU C Library: Shared libraries”.
- https://packages.debian.org/bookworm/locales: “GNU C Library: National Language (locale) data [support]”.
- https://packages.debian.org/bookworm/libgmp10: “Multiprecision arithmetic library”.
- https://packages.debian.org/bookworm/gpgv: “GNU privacy guard - signature verification tool”.
- https://packages.debian.org/bookworm/libgnutls30: “GNU TLS library - main runtime library”.
- https://packages.debian.org/bookworm/libgpm2: “General Purpose Mouse - shared library”.
- https://packages.debian.org/bookworm/grep: “GNU grep, egrep and fgrep”.
- https://packages.debian.org/bookworm/groff-base: “GNU troff text-formatting system (base system components)”.
- https://packages.debian.org/bookworm/grub-cloud-amd64: “GRand Unified Bootloader (cloud setup)”.
- https://packages.debian.org/bookworm/grub-efi-amd64-signed: “GRand Unified Bootloader, version 2 (amd64 UEFI signed by Debian)”.
- https://packages.debian.org/bookworm/grub-common: “GRand Unified Bootloader (common files)”.
- https://packages.debian.org/bookworm/grub-efi-amd64-bin: “GRand Unified Bootloader, version 2 (EFI-AMD64 modules)”.
- https://packages.debian.org/bookworm/grub-pc-bin: “GRand Unified Bootloader, version 2 (PC/BIOS modules)”.
- https://packages.debian.org/bookworm/grub2-common: “GRand Unified Bootloader (common files for version 2)”.
- https://packages.debian.org/bookworm/gzip: “GNU compression utilities”.
- https://packages.debian.org/bookworm/hostname: “utility to set/show the host name or domain name”.
- https://packages.debian.org/bookworm/libicu72: “International Components for Unicode”.
- https://packages.debian.org/bookworm/init: “metapackage ensuring an init system is installed”.
- https://packages.debian.org/bookworm/init-system-helpers: “helper tools for all init systems”.
- https://packages.debian.org/bookworm/initramfs-tools: “generic modular initramfs generator (automation)”.
- https://packages.debian.org/bookworm/initramfs-tools-core: “generic modular initramfs generator (core tools)”.
- https://packages.debian.org/bookworm/iproute2: “networking and traffic control tools”.
- https://packages.debian.org/bookworm/iptables: “administration tools for packet filtering and NAT”.
- https://packages.debian.org/bookworm/libip4tc2: “netfilter libip4tc library”.
- https://packages.debian.org/bookworm/libip6tc2: “netfilter libip6tc library”.
- https://packages.debian.org/bookworm/libxtables12: “netfilter xtables library”.
- https://packages.debian.org/bookworm/iputils-ping: “Tools to test the reachability of network hosts”.
- https://packages.debian.org/bookworm/isc-dhcp-client: “DHCP client for automatically obtaining an IP address”.
- https://packages.debian.org/bookworm/libjemalloc2: “general-purpose scalable concurrent malloc(3) implementation”.
- https://packages.debian.org/bookworm/python3-jinja2: “small but fast and easy to use stand-alone template engine”.
- https://packages.debian.org/bookworm/jq: “lightweight and flexible command-line JSON processor”.
- https://packages.debian.org/bookworm/libjq1: “lightweight and flexible command-line JSON processor - shared library”.
- https://packages.debian.org/bookworm/libjson-c5: “JSON manipulation library - shared library”.
- https://packages.debian.org/bookworm/libkeyutils1: “Linux Key Management Utilities (library)”.
- https://packages.debian.org/bookworm/klibc-utils: “small utilities built with klibc for early boot”.
- https://packages.debian.org/bookworm/libklibc: “minimal libc subset for use with initramfs”.
- https://packages.debian.org/bookworm/kmod: “tools for managing Linux kernel modules”.
- https://packages.debian.org/bookworm/libkmod2: “libkmod shared library”.
- https://packages.debian.org/bookworm/libgssapi-krb5-2: “MIT Kerberos runtime libraries - krb5 GSS-API Mechanism”.
- https://packages.debian.org/bookworm/libk5crypto3: “MIT Kerberos runtime libraries - Crypto Library”.
- https://packages.debian.org/bookworm/libkrb5-3: “MIT Kerberos runtime libraries”.
- https://packages.debian.org/bookworm/libkrb5support0: “MIT Kerberos runtime libraries - Support library”.
- https://packages.debian.org/bookworm/less: “pager program similar to more”.
- https://packages.debian.org/bookworm/libaio1: “Linux kernel AIO access library - shared library”.
- https://packages.debian.org/bookworm/libbpf1: “eBPF helper library (shared library)”.
- https://packages.debian.org/bookworm/libbsd0: “utility functions from BSD systems - shared library”.
- https://packages.debian.org/bookworm/libcap-ng0: “alternate POSIX capabilities library”.
- https://packages.debian.org/bookworm/libcap2: “POSIX 1003.1e capabilities (library)”.
- https://packages.debian.org/bookworm/libcap2-bin: “POSIX 1003.1e capabilities (utilities)”.
- https://packages.debian.org/bookworm/libcbor0.8: “library for parsing and generating CBOR (RFC 7049)”.
- https://packages.debian.org/bookworm/libedit2: “BSD editline and history libraries”.
- https://packages.debian.org/bookworm/libffi8: “Foreign Function Interface library runtime”.
- https://packages.debian.org/bookworm/libfido2-1: “library for generating and verifying FIDO 2.0 objects”.
- https://packages.debian.org/bookworm/libgcrypt20: “LGPL Crypto library - runtime library”.
- https://packages.debian.org/bookworm/libgpg-error0: “GnuPG development runtime library”.
- https://packages.debian.org/bookworm/libidn2-0: “Internationalized domain names (IDNA2008/TR46) library”.
- https://packages.debian.org/bookworm/libmaxminddb0: “IP geolocation database library”.
- https://packages.debian.org/bookworm/libmd0: “message digest functions from BSD systems - shared library”.
- https://packages.debian.org/bookworm/libmnl0: “minimalistic Netlink communication library”.
- https://packages.debian.org/bookworm/libnetfilter-conntrack3: “Netfilter netlink-conntrack library”.
- https://packages.debian.org/bookworm/libnfnetlink0: “Netfilter netlink library”.
- https://packages.debian.org/bookworm/libnftnl11: “Netfilter nftables userspace API library”.
- https://packages.debian.org/bookworm/libnsl2: “Public client interface for NIS(YP) and NIS+”.
- https://packages.debian.org/bookworm/libonig5: “regular expressions library”.
- https://packages.debian.org/bookworm/libpcap0.8: “system interface for user-level packet capture”.
- https://packages.debian.org/bookworm/libpipeline1: “Unix process pipeline manipulation library”.
- https://packages.debian.org/bookworm/libpng16-16: “PNG library - runtime (version 1.6)”.
- https://packages.debian.org/bookworm/libpsl5: “Library for Public Suffix List (shared libraries)”.
- https://packages.debian.org/bookworm/libseccomp2: “high level interface to Linux seccomp filter”.
- https://packages.debian.org/bookworm/libselinux1: “SELinux runtime shared libraries”.
- https://packages.debian.org/bookworm/libsemanage-common: “Common files for SELinux policy management libraries”.
- https://packages.debian.org/bookworm/libsemanage2: “SELinux policy management library”.
- https://packages.debian.org/bookworm/libsepol2: “SELinux library for manipulating binary security policies”.
- https://packages.debian.org/bookworm/libsodium23: “Network communication, cryptography and signaturing library”.
- https://packages.debian.org/bookworm/libssh2-1: “SSH2 client-side library”.
- https://packages.debian.org/bookworm/libtasn1-6: “Manage ASN.1 structures (runtime)”.
- https://packages.debian.org/bookworm/libtirpc-common: “transport-independent RPC library - common files”.
- https://packages.debian.org/bookworm/libtirpc3: “transport-independent RPC library”.
- https://packages.debian.org/bookworm/libunistring2: “Unicode string library for C”.
- https://packages.debian.org/bookworm/liburing2: “Linux kernel io_uring access library - shared library”.
- https://packages.debian.org/bookworm/libutempter0: “privileged helper for utmp/wtmp updates (runtime)”.
- https://packages.debian.org/bookworm/libuv1: “asynchronous event notification library - runtime library”.
- https://packages.debian.org/bookworm/libcrypt1: “libcrypt shared library”.
- https://packages.debian.org/bookworm/libxml2: “GNOME XML library”.
- https://packages.debian.org/bookworm/libyaml-0-2: “Fast YAML 1.1 parser and emitter library”.
- https://packages.debian.org/bookworm/libzstd1: “fast lossless compression algorithm”.
- https://packages.debian.org/bookworm/zstd: “fast lossless compression algorithm -- CLI tool”.
- https://packages.debian.org/bookworm/linux-base: “Linux image base package”.
- https://packages.debian.org/bookworm/linux-image-cloud-amd64: “Linux for x86-64 cloud (meta-package)”.
- https://packages.debian.org/bookworm/liblmdb0: “Lightning Memory-Mapped Database shared library”.
- https://packages.debian.org/bookworm/lsb-release: “Linux Standard Base version reporting utility (minimal implementation)”.
- https://packages.debian.org/bookworm/dmsetup: “Linux Kernel Device Mapper userspace library”.
- https://packages.debian.org/bookworm/libdevmapper1.02.1: “Linux Kernel Device Mapper userspace library”.
- https://packages.debian.org/bookworm/liblz4-1: “Fast LZ compression algorithm library - runtime”.
- https://packages.debian.org/bookworm/man-db: “tools for reading manual pages”.
- https://packages.debian.org/bookworm/manpages: “Manual pages about using a GNU/Linux system”.
- https://packages.debian.org/bookworm/python3-markdown-it: “Python port of markdown-it and some its associated plugins”.
- https://packages.debian.org/bookworm/python3-markupsafe: “HTML/XHTML/XML string library”.
- https://packages.debian.org/bookworm/mawk: “Pattern scanning and text processing language”.
- https://packages.debian.org/bookworm/python3-mdurl: “Python port of the JavaScript mdurl package”.
- https://packages.debian.org/bookworm/media-types: “List of standard media types and their usual file extension”.
- https://packages.debian.org/bookworm/mokutil: “tools for manipulating machine owner keys”.
- https://packages.debian.org/bookworm/nano: “small, friendly text editor inspired by Pico”.
- https://packages.debian.org/bookworm/libncursesw6: “shared libraries for terminal handling (wide character support)”.
- https://packages.debian.org/bookworm/libtinfo6: “shared low-level terminfo library for terminal handling”.
- https://packages.debian.org/bookworm/ncurses-base: “basic terminal type definitions”.
- https://packages.debian.org/bookworm/ncurses-bin: “terminal-related programs and man pages”.
- https://packages.debian.org/bookworm/netbase: “Basic TCP/IP networking system”.
- https://packages.debian.org/bookworm/python3-netifaces: “portable network interface information - Python 3.x”.
- https://packages.debian.org/bookworm/libnetplan0: “YAML network configuration abstraction runtime library”.
- https://packages.debian.org/bookworm/netplan.io: “YAML network configuration abstraction for various backends”.
- https://packages.debian.org/bookworm/libhogweed6: “low level cryptographic library (public-key cryptos)”.
- https://packages.debian.org/bookworm/libnettle8: “low level cryptographic library (symmetric and one-way cryptos)”.
- https://packages.debian.org/bookworm/libnewt0.52: “text mode windowing with slang”.
- https://packages.debian.org/bookworm/whiptail: “Displays user-friendly dialog boxes from shell scripts”.
- https://packages.debian.org/bookworm/libnghttp2-14: “library implementing HTTP/2 protocol (shared library)”.
- https://packages.debian.org/bookworm/libnuma1: “Libraries for controlling NUMA policy”.
- https://packages.debian.org/bookworm/libldap-2.5-0: “OpenLDAP libraries”.
- https://packages.debian.org/bookworm/openssh-client: “secure shell (SSH) client, for secure access to remote machines”.
- https://packages.debian.org/bookworm/openssh-server: “secure shell (SSH) server, for secure access from remote machines”.
- https://packages.debian.org/bookworm/openssh-sftp-server: “secure shell (SSH) sftp server module, for SFTP access from remote machines”.
- https://packages.debian.org/bookworm/libssl3: “Secure Sockets Layer toolkit - shared libraries”.
- https://packages.debian.org/bookworm/openssl: “Secure Sockets Layer toolkit - cryptographic utility”.
- https://packages.debian.org/bookworm/libp11-kit0: “library for loading and coordinating access to PKCS#11 modules - runtime”.
- https://packages.debian.org/bookworm/libpam-modules: “Pluggable Authentication Modules for PAM”.
- https://packages.debian.org/bookworm/libpam-modules-bin: “Pluggable Authentication Modules for PAM - helper binaries”.
- https://packages.debian.org/bookworm/libpam-runtime: “Runtime support for the PAM library”.
- https://packages.debian.org/bookworm/libpam0g: “Pluggable Authentication Modules library”.
- https://packages.debian.org/bookworm/pci.ids: “PCI ID Repository”.
- https://packages.debian.org/bookworm/libpci3: “PCI utilities (shared library)”.
- https://packages.debian.org/bookworm/pciutils: “PCI utilities”.
- https://packages.debian.org/bookworm/libpcre2-8-0: “New Perl Compatible Regular Expression Library- 8 bit runtime files”.
- https://packages.debian.org/bookworm/perl-base: “minimal Perl system”.
- https://packages.debian.org/bookworm/libpolkit-agent-1-0: “polkit Authentication Agent API”.
- https://packages.debian.org/bookworm/libpolkit-gobject-1-0: “polkit Authorization API”.
- https://packages.debian.org/bookworm/polkitd: “framework for managing administrative policies and privileges”.
- https://packages.debian.org/bookworm/libpopt0: “lib for parsing cmdline parameters”.
- https://packages.debian.org/bookworm/libproc2-0: “library for accessing process information from /proc”.
- https://packages.debian.org/bookworm/procps: “/proc file system utilities”.
- https://packages.debian.org/bookworm/libprotobuf-c1: “Protocol Buffers C shared library (protobuf-c)”.
- https://packages.debian.org/bookworm/psmisc: “utilities that use the proc file system”.
- https://packages.debian.org/bookworm/python3-pycurl: “Python bindings to libcurl (Python 3)”.
- https://packages.debian.org/bookworm/python3-pygments: “syntax highlighting package written in Python 3”.
- https://packages.debian.org/bookworm/python3-jwt: “Python 3 implementation of JSON Web Token”.
- https://packages.debian.org/bookworm/python3-pyparsing: “alternative to creating and executing simple grammars - Python 3.x”.
- https://packages.debian.org/bookworm/python3-pyrsistent: “persistent/functional/immutable data structures for Python”.
- https://packages.debian.org/bookworm/python3-serial: “pyserial - module encapsulating access for the serial port”.
- https://packages.debian.org/bookworm/python3-pysimplesoap: “simple and lightweight SOAP Library (Python 3)”.
- https://packages.debian.org/bookworm/python-apt-common: “Python interface to libapt-pkg (locales)”.
- https://packages.debian.org/bookworm/python3-apt: “Python 3 interface to libapt-pkg”.
- https://packages.debian.org/bookworm/python3-attr: “Attributes without boilerplate (Python 3)”.
- https://packages.debian.org/bookworm/python3-certifi: “root certificates for validating SSL certs and verifying TLS hosts (python3)”.
- https://packages.debian.org/bookworm/python3-cffi-backend: “Foreign Function Interface for Python 3 calling C code - runtime”.
- https://packages.debian.org/bookworm/python3-charset-normalizer: “charset, encoding and language detection (Python 3)”.
- https://packages.debian.org/bookworm/python3-cryptography: “Python library exposing cryptographic recipes and primitives (Python 3)”.
- https://packages.debian.org/bookworm/python3-debian: “Python 3 modules to work with Debian-related data formats”.
- https://packages.debian.org/bookworm/python3-debianbts: “Python interface to Debian's Bug Tracking System”.
- https://packages.debian.org/bookworm/python3-distro: “Linux OS platform information API”.
- https://packages.debian.org/bookworm/python3-httplib2: “comprehensive HTTP client library written for Python3”.
- https://packages.debian.org/bookworm/python3-idna: “Python IDNA2008 (RFC 5891) handling (Python 3)”.
- https://packages.debian.org/bookworm/python3-jsonpatch: “library to apply JSON patches - Python 3.x”.
- https://packages.debian.org/bookworm/python3-json-pointer: “resolve JSON pointers - Python 3.x”.
- https://packages.debian.org/bookworm/python3-jsonschema: “An(other) implementation of JSON Schema (Draft 3, 4, 6, 7)”.
- https://packages.debian.org/bookworm/python3-oauthlib: “generic, spec-compliant implementation of OAuth for Python3”.
- https://packages.debian.org/bookworm/python3-urllib3: “HTTP library with thread-safe connection pooling for Python3”.
- https://packages.debian.org/bookworm/libpython3-stdlib: “interactive high-level object-oriented language (default python3 version)”.
- https://packages.debian.org/bookworm/python3: “interactive high-level object-oriented language (default python3 version)”.
- https://packages.debian.org/bookworm/python3-minimal: “minimal subset of the Python language (default python3 version)”.
- https://packages.debian.org/bookworm/libpython3.11-minimal: “Minimal subset of the Python language (version 3.11)”.
- https://packages.debian.org/bookworm/libpython3.11-stdlib: “Interactive high-level object-oriented language (standard library, version 3.11)”.
- https://packages.debian.org/bookworm/python3.11: “Interactive high-level object-oriented language (version 3.11)”.
- https://packages.debian.org/bookworm/python3.11-minimal: “Minimal subset of the Python language (version 3.11)”.
- https://packages.debian.org/bookworm/python3-yaml: “YAML parser and emitter for Python3”.
- https://packages.debian.org/bookworm/qemu-utils: “QEMU utilities”.
- https://packages.debian.org/bookworm/libreadline8: “GNU readline and history libraries, run-time libraries”.
- https://packages.debian.org/bookworm/readline-common: “GNU readline and history libraries, common files”.
- https://packages.debian.org/bookworm/python3-reportbug: “Python modules for interacting with bug tracking systems”.
- https://packages.debian.org/bookworm/reportbug: “reports bugs in the Debian distribution”.
- https://packages.debian.org/bookworm/python3-requests: “elegant and simple HTTP library for Python3, built for human beings”.
- https://packages.debian.org/bookworm/python3-rich: “render rich text, tables, progress bars, syntax highlighting, markdown and more”.
- https://packages.debian.org/bookworm/librtmp1: “toolkit for RTMP streams (shared library)”.
- https://packages.debian.org/bookworm/screen: “terminal multiplexer with VT100/ANSI terminal emulation”.
- https://packages.debian.org/bookworm/sed: “GNU stream editor for filtering/transforming text”.
- https://packages.debian.org/bookworm/sensible-utils: “Utilities for sensible alternative selection”.
- https://packages.debian.org/bookworm/python3-pkg-resources: “Package Discovery and Resource Access using pkg_resources”.
- https://packages.debian.org/bookworm/sgml-base: “SGML infrastructure and SGML catalog file support”.
- https://packages.debian.org/bookworm/login: “system login tools”.
- https://packages.debian.org/bookworm/passwd: “change and administer password and group data”.
- https://packages.debian.org/bookworm/shim-unsigned: “boot loader to chain-load signed boot loaders under Secure Boot”.
- https://packages.debian.org/bookworm/shim-helpers-amd64-signed: “boot loader to chain-load signed boot loaders (signed by Debian)”.
- https://packages.debian.org/bookworm/shim-signed: “Secure Boot chain-loading bootloader”.
- https://packages.debian.org/bookworm/shim-signed-common: “Secure Boot chain-loading bootloader (common helper scripts)”.
- https://packages.debian.org/bookworm/python3-six: “Python 2 and 3 compatibility library”.
- https://packages.debian.org/bookworm/libslang2: “S-Lang programming library - runtime version”.
- https://packages.debian.org/bookworm/socat: “multipurpose relay for bidirectional data transfer”.
- https://packages.debian.org/bookworm/libsqlite3-0: “SQLite 3 shared library”.
- https://packages.debian.org/bookworm/ssh-import-id: “securely retrieve an SSH public key and install it locally”.
- https://packages.debian.org/bookworm/sudo: “Provide limited super user privileges to specific users”.
- https://packages.debian.org/bookworm/libnss-myhostname: “nss module providing fallback resolution for the current hostname”.
- https://packages.debian.org/bookworm/libpam-systemd: “system and service manager - PAM module”.
- https://packages.debian.org/bookworm/libsystemd-shared: “systemd shared private library”.
- https://packages.debian.org/bookworm/libsystemd0: “systemd utility library”.
- https://packages.debian.org/bookworm/libudev1: “libudev shared library”.
- https://packages.debian.org/bookworm/systemd: “system and service manager”.
- https://packages.debian.org/bookworm/systemd-resolved: “systemd DNS resolver”.
- https://packages.debian.org/bookworm/systemd-sysv: “system and service manager - SysV compatibility symlinks”.
- https://packages.debian.org/bookworm/systemd-timesyncd: “minimalistic service to synchronize local time with NTP servers”.
- https://packages.debian.org/bookworm/udev: “/dev/ and hotplug management daemon”.
- https://packages.debian.org/bookworm/sysvinit-utils: “System-V-like utilities”.
- https://packages.debian.org/bookworm/tar: “GNU version of the tar archiving utility”.
- https://packages.debian.org/bookworm/libwrap0: “TCP wrappers library”.
- https://packages.debian.org/bookworm/tcpdump: “command-line network traffic analyzer”.
- https://packages.debian.org/bookworm/traceroute: “Traces the route taken by packets over an IPv4/IPv6 network”.
- https://packages.debian.org/bookworm/tzdata: “time zone and daylight-saving time data”.
- https://packages.debian.org/bookworm/ucf: “Update Configuration File(s): preserve user changes to config files”.
- https://packages.debian.org/bookworm/libuchardet0: “universal charset detection library - shared library”.
- https://packages.debian.org/bookworm/unattended-upgrades: “automatic installation of security upgrades”.
- https://packages.debian.org/bookworm/usr-is-merged: “Transitional package to assert a merged-/usr system”.
- https://packages.debian.org/bookworm/bsdextrautils: “extra utilities from 4.4BSD-Lite”.
- https://packages.debian.org/bookworm/bsdutils: “basic utilities from 4.4BSD-Lite”.
- https://packages.debian.org/bookworm/eject: “ejects CDs and operates CD-Changers under Linux”.
- https://packages.debian.org/bookworm/fdisk: “collection of partitioning utilities”.
- https://packages.debian.org/bookworm/libblkid1: “block device ID library”.
- https://packages.debian.org/bookworm/libfdisk1: “fdisk partitioning library”.
- https://packages.debian.org/bookworm/libmount1: “device mounting library”.
- https://packages.debian.org/bookworm/libsmartcols1: “smart column output alignment library”.
- https://packages.debian.org/bookworm/libuuid1: “Universally Unique ID library”.
- https://packages.debian.org/bookworm/mount: “tools for mounting and manipulating filesystems”.
- https://packages.debian.org/bookworm/util-linux: “miscellaneous system utilities”.
- https://packages.debian.org/bookworm/util-linux-extra: “interactive login tools”.
- https://packages.debian.org/bookworm/uuid-runtime: “runtime components for the Universally Unique ID library”.
- https://packages.debian.org/bookworm/vim: “Vi IMproved - enhanced vi editor”.
- https://packages.debian.org/bookworm/vim-common: “Vi IMproved - Common files”.
- https://packages.debian.org/bookworm/vim-runtime: “Vi IMproved - Runtime files”.
- https://packages.debian.org/bookworm/vim-tiny: “Vi IMproved - enhanced vi editor - compact version”.
- https://packages.debian.org/bookworm/wget: “retrieves files from the web”.
- https://packages.debian.org/bookworm/xml-core: “XML infrastructure and XML catalog file support”.
- https://packages.debian.org/bookworm/libxxhash0: “shared library for xxhash”.
- https://packages.debian.org/bookworm/liblzma5: “XZ-format compression library”.
- https://packages.debian.org/bookworm/xz-utils: “XZ-format compression utilities”.
- https://packages.debian.org/bookworm/zlib1g: “compression library - runtime”.

GRUB defaults source: https://www.gnu.org/software/grub/manual/grub/html_node/Simple-configuration.html states: “It is sourced by a shell script, and so must be valid POSIX shell input”. This establishes the code classification for grub-cloud-amd64.

## Review corrections

D-Bus configuration (debian-6551aee88e, debian-2102ddaaf0) governs interprogram communication, so its effect is not confined inside one program. Both rows are MUST under S2.2-1 and S2.2-2.

Recognition rules in libmagic-mgc (debian-f1ae2388d8) and media-types (debian-ad283af0ea) change automatic classification capabilities. The unchanged-behaviour condition in S2.2-4 is unmet, so both are MUST under S2.2-1 and S2.2-2.

zlib1g (debian-5ba05539a3) is library code under rule L, with S2.2-10 rather than S2.2-9.

## Dependency and maintainer-script review

The five former dependency-only HOLE cases are resolved from additional documentation; no unresolved ambiguity is attributed to dependency removal.

For cloud-utils (debian-e62af4f5a5), init (debian-95bb80c619), linux-image-cloud-amd64 (debian-d805aa0253), and libpython3-stdlib (debian-ec71209928), the package descriptions identify operational dependency packages. Their installed requirements maintain the corresponding suite, init implementation, kernel series, or standard-library version. Removing the requirement loses that package-maintenance constraint even if already-installed binaries remain at that instant. Therefore S2.2-1 and S2.2-2 yield MUST.

Official semantics: https://www.debian.org/doc/debian-policy/ch-relationships.html states “A package will not be configured unless all of the packages listed in its Depends field have been correctly configured”. This makes dependency metadata operational rather than reference content.

https://manpages.debian.org/bookworm/apt/apt-get.8.en.html states that dist-upgrade “also intelligently handles changing dependencies with new versions of packages”. Dependency-package presence determines continued dependency-driven upgrades; autoremove additionally distinguishes packages still needed by dependencies.

For usr-is-merged (debian-01d10767da), the ordinary file list was insufficient: package maintainer scripts are control-archive files, absent from that payload list. Reading the official source archive https://deb.debian.org/debian/pool/main/u/usrmerge/usrmerge_37~deb12u1.tar.xz established debian/usr-is-merged.preinst defines `fail_if_unmerged` and debian/usr-is-merged.postinst defines `cleanup_biarch_dirs`. Both have shell interpreter headers; the latter contains `cleanup_biarch_dirs` in the configure branch. The scripts check filesystem layout and clean obsolete architecture directories with installer rights. S2.2-10 and S2.2-13 therefore yield MUST. No script was executed and no file was removed.

## Repository templates and shared recognition database

python-apt-common (debian-9e34733f17) is MUST, not a whole-package aggregation HOLE. The official source archive https://deb.debian.org/debian/pool/main/p/python-apt/python-apt_2.6.0.tar.xz contains aptsources/distro.py. Its get_sources method searches matcher templates; when source_template remains absent, it executes `raise NoDistroTemplateException`. The diagnostic is “Error: could not find a distribution template for %s/%s”. Thus template removal breaks distribution-aware source operations; translations accompanying the templates do not cancel the package’s operational role.

The official API https://apt-team.pages.debian.net/python-apt/library/aptsources.sourceslist.html documents matcherPath as `/usr/share/python-apt/templates/` and `save()` as “save the current sources”. https://apt-team.pages.debian.net/python-apt/library/aptsources.distro.html describes get_sources as “Find the corresponding template, main and child sources for the distribution”. These are repository-management operations used by library consumers, not merely displayed reference content.

libmagic-mgc (debian-f1ae2388d8) remains MUST. The shared-library API https://manpages.debian.org/bookworm/libmagic-dev/libmagic.3.en.html specifies that database loading is required before magic queries and allows client programs to load the system database; this capability is not confined to the file command.

Debian’s exact file 5.44 patch archive https://deb.debian.org/debian/pool/main/f/file/file_5.44-3.debian.tar.xz contains debian/patches/local.support-local-definitions-in-etc-magic.patch. Its library-build definition is `AM_CPPFLAGS = -DMAGIC='"/etc/magic:$(MAGIC)"'`. Therefore the local magic path also belongs to the shared-library default search path.

The corresponding upstream source https://deb.debian.org/debian/pool/main/f/file/file_5.44.orig.tar.gz, src/apprentice.c, contains “Compatibility with old code that looked in .mime” followed by a MAGIC_MIME branch checking the corresponding .mime filename. This establishes that local MIME rules can likewise be consumed by shared-library clients. Whether the particular local files contain any effective rules is a separate evidence question; no file contents were inferred from these default search semantics.


# c1 part 2: stored-object classification

Scope: 253 rows of kinds `package-owned-paths`, `stored`, and `stored-directory-skeleton`. No other classification was consulted. No object was removed and no probe was run. File types, sizes, symlink targets, and group membership come from `../in/raw/debian/files.tsv`, `package-files.txt`, `unowned-groups.json`, and `directory-only-groups.json`. Package groups were reconstructed by assigning each owned pathname to its longest matching input group; every reconstructed count equals the input's `members` count. For stored rows, the raw group membership is used even when the input's `members` column is 1: the evidence itself identifies a group containing more objects. No implication is drawn from inventory classification terminology.

The output was appended as cases were settled. Refinement corrected an initially overbroad directory HOLE reading to factual UNKNOWN, and removed database-content HOLE readings where functional dependence is established. These are c1's own intermediate corrections, not consultation of an earlier classification. The final TSV is authoritative; the construction and refinement scripts preserve the process.

## Governing sentences

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”
- S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”
- S2.2-6: “records of the past—logs, history;”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”
- S3-2: “If what the object does remains unknown, the case yields ?.”

An operational database is not exempt merely because it is a database: S2.2-4 requires unchanged capability. Shared library tables and systemwide policy are not confined to one program. Merely storing a file under a cache directory does not establish the conditional cache exemption. In particular the dynamic linker cache is UNKNOWN because library locations and cache entries were not collected; the auxiliary ldconfig cache has a documented optional role.

## Homogeneous rules and ten manual checks

Rule D: directory-only objects receive UNKNOWN (S3-1, S3-2). The observed fact is namespace storage. The inventory does not establish the directory's independent functional dependency or reconstruction after absence. A pathname becoming unavailable is not by itself sufficient: S2.2-4 already distinguishes content unavailability from lost capability. No automatic inference from package ownership, conventional directory name, or nonzero directory size is made. The same uncertainty is explicitly retained for directory members in heterogeneous groups. This is a conservative evidence limitation, not a textual hole.

Ten individually checked cases against `files.tsv` intersected with `package-files.txt`:

| ID | Manual inspection |
| --- | --- |
| debian-c0faa16997 | binfmt.d is only a directory entry, without a collected rule in this group. |
| debian-7642c049c2 | ca-certificates and update.d are both directories; no hook body occurs in the group. |
| debian-ec5f04bd95 | dbus-1, session.d, system.d are directory entries; no policy payload occurs in this group. |
| debian-35fa9d83db | gss and mech.d are directory entries without mechanism definitions. |
| debian-b69b9d321c | modprobe.d has one directory entry; actual unowned policy is a separate row. |
| debian-5c3528c19a | netplan has one directory entry; network YAML is in a separate row. |
| debian-ad79f60794 | polkit-1 and rules.d are directories, with no rule body in this group. |
| debian-1d27c32fa0 | rc0.d here contains only the directory object; service links form a separate stored row. |
| debian-0b197a23e7 | rc1.d here contains only the directory object; service links form a separate stored row. |
| debian-cadf3ec932 | rc2.d here contains only the directory object; service links form a separate stored row. |

Rule L: identified log/history payloads receive NOT under S2.2-6. This rule applies only to payloads whose event-recording role is established, not every path under a log directory. The README is separately content, and the journal group is MIXED because it also contains directories.

Ten manually checked input IDs and raw payload roles:

| ID | Manual inspection |
| --- | --- |
| debian-83df02e6eb | eipp.log.xz, history.log, term.log record package operations. |
| debian-9c96b64591 | btmp records failed login attempts. |
| debian-93b020b2d3 | cloud-init-output.log records provisioning command output. |
| debian-2954505d9d | cloud-init.log records provisioning events. |
| debian-6f5cf081f0 | dpkg.log records package management events. |
| debian-8dc29397cf | faillog records login failures. |
| debian-698c23461f | lastlog records previous account logins. |
| debian-dea214b7e3 | unattended-upgrades-shutdown.log records upgrade shutdown events. |
| debian-d6ce9987c3 | wtmp records login/session history. |
| debian-917d8d1269 | resolver .bak file preserves previous configuration, rather than the active resolver symlink. |

All other cases have individual records in the construction/refinement scripts and final TSV; no ownership-wide rule assigns a decision to heterogeneous groups. Short MIXED reasons enumerate member categories. “Directory dependency: UNKNOWN” means each directory member, not a missing classification of the group.

## Documentation and quoted functional evidence

The inventory establishes which object exists; these primary manuals establish its role. Quotes are deliberately short. URLs are linked here for compact rows whose basis points to inventory membership.

- [Linux pathname resolution](https://manpages.debian.org/bookworm/manpages/path_resolution.7.en.html): “If the component is not found, an ENOENT error is returned”. This establishes namespace mechanics, not whether an application requires an observed directory.
- [Filesystem hierarchy](https://manpages.debian.org/bookworm/manpages/hier.7.en.html): “Contains static files for the boot loader.” The conventional role of a directory alone does not establish every observed inode's independent effect.
- [Bash](https://manpages.debian.org/bookworm/bash/bash.1.en.html): “executes commands read from the standard input or from a file.” Supports shell startup and executable hook cases.
- [Nano configuration](https://manpages.debian.org/bookworm/nano/nanorc.5.en.html): “The nanorc files contain the default settings for nano”. Supports both editor preference rows.
- [Account creation configuration](https://manpages.debian.org/bookworm/adduser/adduser.conf.5.en.html): “contains defaults for the programs”. The named programs include account creation and deletion utilities; the file is not confined to one program.
- [APT configuration](https://manpages.debian.org/bookworm/apt/apt.conf.5.en.html): “shared by all the tools in the APT suite of tools”. Shared repository/installation policy is distinguished from listchanges display preferences.
- [dpkg](https://manpages.debian.org/bookworm/dpkg/dpkg.1.en.html): “dpkg keeps its record of available packages in /var/lib/dpkg/available.” Active records govern package handling; the content exemption is not assumed.
- [Alternatives](https://manpages.debian.org/bookworm/dpkg/update-alternatives.1.en.html): “maintain symbolic links determining default commands”. Raw links to executable paths and links to manual pages are distinguished.
- [Initramfs scripts](https://manpages.debian.org/bookworm/initramfs-tools-core/initramfs-tools.7.en.html): “has one main script and two different sets of subscripts”. Supports early boot code and hook roles.
- [Dynamic loader](https://manpages.debian.org/bookworm/manpages/ld.so.8.en.html): “contains a compiled list of candidate shared objects previously found in the augmented library path.” The cache is not blindly treated as speed-only.
- [ldconfig](https://manpages.debian.org/bookworm/manpages/ldconfig.8.en.html): “Ignore auxiliary cache file.” Supports the auxiliary metadata cache exemption.
- [Manual index](https://manpages.debian.org/bookworm/man-db/mandb.8.en.html): “create or update the manual page index caches”. Cache roles are distinguished from the auto-update enabling marker.
- [Manual package installation script](https://sources.debian.org/src/man-db/2.11.2-2/debian/postinst/): `if [ ! -e /var/lib/man-db/auto-update ]; then`. The branch reports “Not building database”; marker removal skips a real operation.
- [Debconf](https://manpages.debian.org/bookworm/debconf-doc/debconf.7.en.html): “Debconf is a configuration system for Debian packages.” Current answers are operational configuration, templates are question text, old copies are historical.
- [PAM generation](https://manpages.debian.org/bookworm/libpam-runtime/pam-auth-update.8.en.html): “configuring the central authentication policy for the system”. Supports systemwide effects of PAM inputs and generation state.
- [Password history](https://manpages.debian.org/bookworm/libpam-modules/pam_pwhistory.8.en.html): “The last N passwords for each user are saved in /etc/security/opasswd.” Unlike the conditional content exception, the past-record exception is unqualified, motivating the specific operative-history HOLE.
- [Shadow](https://manpages.debian.org/bookworm/passwd/shadow.5.en.html): “contains the password information for the system's accounts and optional aging information.” A single file combines explicitly exempt secrets with access policy; removing the whole file loses that policy, so it is MUST.
- [Group shadow](https://manpages.debian.org/bookworm/passwd/gshadow.5.en.html): “Administrators can change the password or the members of the group.” Membership authority and password fields occupy one object; whole-object removal loses the authority policy, so it is MUST.
- [SSH server configuration](https://manpages.debian.org/bookworm/openssh-server/sshd_config.5.en.html): “OpenSSH daemon configuration file”. Account access and listening-port rules have explicit treatment in S2.2-15.
- [Configuration preservation](https://manpages.debian.org/bookworm/ucf/ucf.1.en.html): “preserve user changes in configuration files”. Active merge baselines change conflict handling; numbered backups are past copies.
- [Python policy](https://www.debian.org/doc/packaging-manuals/python-policy/): “allows configuration how modules should be byte-compiled.” The inventory's Python configuration participates in package module processing, rather than executable application source.
- [Login shell registration](https://manpages.debian.org/bookworm/debianutils/update-shells.8.en.html): “To track changes made by the administrator, it consults a state file”. This establishes the operative past-state boundary rather than assuming a passive database.
- [Cloud first boot](https://docs.cloud-init.io/en/latest/explanation/first_boot.html): “stores a cache of its internal state for use across stages and boots.” The documented role determines whether per-instance configuration runs; this is not a speed-only cache.
- [User lingering](https://manpages.debian.org/bookworm/systemd/loginctl.1.en.html): “a user manager is spawned for the user at boot and kept around after logouts.” Supports the MUST member of the systemd state group.
- [AppArmor parser](https://manpages.debian.org/bookworm/apparmor/apparmor_parser.8.en.html): “specify the default options for the parser”. Compiled policy cache is regenerable; kernel access profiles are operative policy.
- [Groff](https://manpages.debian.org/bookworm/groff-base/groff.1.en.html): “Unsafe mode. Reverts to the (old) unsafe behaviour”. Missing macro contents and execution mode prevent deciding code confinement.
- [Screen](https://manpages.debian.org/bookworm/screen/screen.1.en.html): “creates a single window with a shell in it”. The program has settings and command execution; the collected file contents are insufficient to separate them.

Additional primary manuals for shared mappings and policy:

| Function | Source and quoted identification |
| --- | --- |
| Resolver policy | [host.conf](https://manpages.debian.org/bookworm/manpages/host.conf.5.en.html): “resolver configuration file” |
| Address selection | [gai.conf](https://manpages.debian.org/bookworm/manpages/gai.conf.5.en.html): “getaddrinfo(3) configuration file” |
| Network service names | [services](https://manpages.debian.org/bookworm/manpages/services.5.en.html): “Internet network services list” |
| Protocol names | [protocols](https://manpages.debian.org/bookworm/manpages/protocols.5.en.html): “protocols definition file” |
| RPC transport definitions | [netconfig](https://manpages.debian.org/bookworm/libtirpc-common/netconfig.5.en.html): “network configuration data base” |
| Audit library settings | [libaudit.conf](https://manpages.debian.org/bookworm/libaudit-common/libaudit.conf.5.en.html): “libaudit configuration file” |
| User namespace delegation | [subuid](https://manpages.debian.org/bookworm/passwd/subuid.5.en.html): “configuration for subordinate user ids” |

## Group details and limitations

The bootloader group contains EFI executables and configuration references; the GRUB group includes module binaries, loader images, `.lst` lookup files, configuration, one font, translations, and directories. The font and translation payloads are presentation content; loader/module lookup files support actual boot execution. The alternatives group contains 102 symlinks: executable-target aliases are distinguished from documentation-target aliases.

The package-state group contains maintainer scripts, active status/available information, alternatives/diversions/statoverride/trigger data, old copies, locks, and one directory. Current operational metadata is MUST; `.old`/`-old` copies are NOT; lock lifecycle and cmethopt contents remain UNKNOWN. Mere `.list` or checksum text being database-like is not used to exempt metadata required by removal/verification operations.

The provisioning-state group contains known result/history files, per-instance execution semaphores, identity metadata, saved data of unknown contents, and directories. No assumption is made that every saved user-data file is executable or that a serialized object is benign content. The system-manager state group includes an explicit lingering entry, timestamps and enablement records, a message catalog, a random seed, and directories. The random seed's precise contribution is not inferred from the pathname alone.

For configuration files supporting both internal values and executable actions (screen, logrotate) the absence of contents yields UNKNOWN, not a manufactured textual conflict. The remaining HOLE cases state specific textual boundaries in the TSV; none is based on Section 2.5 design questions.

## Final review corrections

The formatter defaults file is NOT under S2.2-7/13: the defaults are applied inside the formatter; its output filesystem does not continue reading those settings. [mke2fs.conf](https://manpages.debian.org/bookworm/e2fsprogs/mke2fs.conf.5.en.html) states: “Contains relations which influence how mke2fs behaves.”

The shadow and group-shadow objects are MUST because whole-file removal loses required lock/expiry or administration/membership policy, regardless of exempt password fields. The APT mirrors directory uses the same UNKNOWN dependency treatment as other directory members.

The successful-sudo marker is NOT, correcting an unsupported assumption about an advisory consumer. [sudoers](https://manpages.debian.org/bookworm/sudo/sudoers.5.en.html) describes admin_flag as a file “created the first time a user” runs sudo. [Distribution bug 1012276](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1012276) explains that the advice consumer was absent from the distribution shell setup. This historical bug does not prove the inventoried shell contents; it does disprove assuming the advice behavior from the filename alone. The established function is the past-use record. No observed consumer supplies a conflicting active function.

Local magic override correction: debian-3058cb94e3 and debian-4ddca1eeaa are UNKNOWN, replacing the unsupported one-program exemption. [The recognition library manual](https://manpages.debian.org/bookworm/libmagic-dev/libmagic.3.en.html) identifies a “Magic number recognition library”. [The distribution patch archive](https://deb.debian.org/debian/pool/main/f/file/file_5.44-3.debian.tar.xz), patch local.support-local-definitions-in-etc-magic.patch, sets the library default path to include `/etc/magic`. [The upstream source archive](https://deb.debian.org/debian/pool/main/f/file/file_5.44.orig.tar.gz), src/apprentice.c, documents “Compatibility with old code that looked in .mime” and constructs the MIME variant for MAGIC_MIME loading. This establishes shared-library scope. Both observed files are 111 bytes, however, and the inventory captures no contents. The conffile checksums are package database metadata, not independently measured current file hashes. Consequently effective local rules cannot be distinguished from comment-only placeholders. Neither NOT for one-program scope nor MUST for assumed rules is warranted.


# Exact text of all sentences cited in the final table

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


# Final mechanical validation

`part-2.verify.py --complete` verified exact header, UTF-8 TSV fields, all 839 input IDs present exactly once, no extra IDs, permitted decisions, sentence IDs, word limits, basis syntax, and existence of cited raw files. The main table matches the final component fragments. `part-2.done` contains the verified counts. No independent substantive acceptance is inferred from this mechanical check; review findings are recorded separately.

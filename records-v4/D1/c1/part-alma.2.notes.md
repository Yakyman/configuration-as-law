# L1 non-package classification notes

Scope: exactly 3,044 L1 rows other than packages, from `D1/in/part-alma.tsv`. The output is `part-alma.2.tsv`. Classification uses object identity from the retained query, not its collector class label. Package integrity comes from (not published: over 20 MB); runtime filesystem metadata comes from (not published: over 20 MB). Packages remain separate rows assigned elsewhere.

## Deciding sentences

- **S8.2-5** What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.

- **S8.2-6** What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.

- **S8.2-7** Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?

- **S8.2-8** Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.

- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?

- **S8.2-10** Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.

- **S8.2-11** Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?

- **S8.2-12** Then it is a **setting**, however it was entered and whatever file stores it.

- **S8.2-13** Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.

- **S8.2-14** A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.

- **S8.2-15** Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.

- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.

- **S8.2-17** A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.

- **S8.2-22** A program that runs as its own process on the computer, including in a container, is a program.

- **S8.2-23** A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.

## Documentation used to identify objects

- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html — “List units that systemd currently has in memory.” This distinguishes missing-unit references from installed files. Timer listings include live deadlines.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html — “A unit file is a plain text ini-style file”. Unit files supply values; executable content is not inferred from ExecStart values. The documented search order selects local overrides before vendor files.
- https://polkit.pages.freedesktop.org/polkit/polkit.8.html — “Actions are defined by applications.” Each captured action identifier was matched to an actual action element in the retained policy XML; all 299 identifiers matched.
- https://docs.kernel.org/filesystems/sysfs.html — “sysfs is a RAM-based filesystem initially based on ramfs.” The module and driver query scripts enumerate sysfs registrations, not stored module binaries.
- https://firewalld.org/documentation/configuration/runtime-versus-permanent.html — “The runtime configuration will be lost with a firewalld service stop.” The nft query reports live kernel tables, chains and rules, not the persistent files.
- https://docs.podman.io/en/latest/markdown/podman.1.html — “Simple management tool for pods, containers and images”. This description does not by itself establish an installer under S8.1-4.
- https://docs.podman.io/en/latest/markdown/podman-start.1.html — “Start one or more containers using container IDs or names as input.” Exited containers remain startable; they are not merely historical log records.
- https://networkmanager.dev/docs/api/latest/nm-settings-keyfile.html — “NetworkManager is based on the concept of connection profiles that contain network configuration”. Stored connection files provide values, not executable source code.

## Rules applied by the script

`part-alma.2.classify.py` appends missing ids and flushes every row. Corrections discovered during checking were confined to two generated SSH aliases: their explicit runtime filesystem records establish RUNTIME. No sampling substitutes for member or integrity joins.

- **setting-origin:** For account, group or service values, S8.2-13 establishes settings. Neither presence nor a familiar system name establishes whether the current value is a package default or a later choice. S8.2-17 then leaves the recording line factually unknown. The aggregate passwd/group files are changed; this does not prove individual records changed. Existing missing-unit references and the locally enabled authentication service are separate cases.
- **unchanged-package:** If the selected actual file, or XML action's containing file, has an unchanged package-file entry, S8.2-6–8 decide at question one. S8.2-16 covers it through its package. This includes code-like rules and default values; no settings clarification overrides question order. The script checks exact paths, unit search precedence and XML identifiers.
- **unit-origin:** The remaining ten persistent unit aliases lack reliable facts on default creation versus later configuration; S8.2-7 and S8.2-17 require UNKNOWN. A target's unchanged bytes do not prove that a separately created alias was received with a package.
- **runtime-process:** Every process is explicitly covered by S8.2-5, regardless of whether its creator is identified. Where executable integrity is known unchanged, the creator is INSTALLED-PACKAGE. Missing executable identity or integrity leaves the creator UNKNOWN, without changing the process's RUNTIME decision.
- **runtime-kernel:** The captured module names and driver paths are sysfs registrations created by the kernel during execution. S8.2-5 gives RUNTIME. The retained kernel image integrity is unknown; no unchanged-image assumption is made for its creator decision.
- **runtime-firewall:** nft's live tables, chains and rules exist in the running kernel. S8.2-5 gives RUNTIME; the observed owning tables distinguish firewalld from netavark, whose program files are unchanged packaged content. Persistent policy is not identified with these live objects.
- **runtime-manager:** A missing unit loaded only as an in-memory reference, or a unit file positively identified on a runtime filesystem, exists only during execution. S8.2-5 gives RUNTIME. The reasons identify systemd, its autostart generator or the SSH generator and the creator decision; unknown SSH generator provenance remains explicit.

## Manual ten-row checks per rule

For each list below, the retained record and the rule's deciding predicate were examined. Account rows have complete identity records but no individual default provenance. Missing-unit rows explicitly say not-found. Packaged unit rows join unchanged entries. Unit aliases have persistent links without creation provenance. Firewall entries are live table/chain objects. Process records contain a PID and the stated executable or unknown. Kernel entries came from the sysfs enumeration.

### setting-origin

alma-1270901ac803f087770d4a03, alma-18ded40433b6af01a8b11595, alma-09fe3e2ff1af708b3e2f3cc4, alma-3a9032548c4616d565f24feb, alma-b2d0097b60aae99ae9ddedac, alma-2306394bc0f92c33d49a6439, alma-448646fafcede98990f077af, alma-986feb2c79e9e648fbc39e33, alma-013789c485cfe6ad406fb020, alma-adb91fb58b73a818d97424ca

### unchanged-package

alma-b6d46ec30f2a5544c8f034eb, alma-dd2e571f5cdae7a0aea00765, alma-603e2163557a3fa31b3f1153, alma-395e07fd1415587cadf07f46, alma-fc8e6f4b3aebd52ec58570e2, alma-2ba8c538abcd0c153252e88c, alma-c719ee65ca6427a425f4f522, alma-751b49f4326ea93b25b6bb98, alma-3b2e8e00da65dbcf24bc87bd, alma-53fa364e2cf166bce33a9d60

### unit-origin

alma-d33e0438b1ccb4129ae9ab25, alma-e72dbb895ddd9bd0b38bf52a, alma-a4b5dace6048c24e81811995, alma-6a26dbb966bac7d9fb0abda6, alma-4c81a69e31ead4120098f60b, alma-7cca1c6906c99a886e86a692, alma-37c4765f1bc3df9c50c7463a, alma-5404dea0fe8c5190436c31c2, alma-b40629803b933a2b052a5d96, alma-0bd28f6010aed40c90735f95

### runtime-process

alma-9a469fe77b60b9eee6cbc515, alma-75112624ed82d0e836f2ee39, alma-77e5d61dde1f088c197037f2, alma-9df7398e97f9cabd55360708, alma-3e28697c90e169b6c550c7db, alma-777296add37822d2eea78d3e, alma-a1c243a655ffb692916a77b1, alma-bb2694c887ad035a89e32d81, alma-fd6b39a52e45b2be95e932c9, alma-745b2a282c25d73ae65778f6

### runtime-kernel

alma-5af8cb1ac7d4e30d3d553dfd, alma-ca5ea4d08e696ec77a27abca, alma-560aa70d01e89fade6df1603, alma-a9b6c7abd3408634d9f2b559, alma-0b81fc9ad7e1a078a37e337f, alma-9de8441033d886077fa55e16, alma-e2e9fc511c77b1af2b5f829d, alma-c405862ece732c9908e94b15, alma-d3fafbd1cca07dee22d1c425, alma-b0fee5f436b48c4afccef587

### runtime-firewall

alma-29c00ab03689c5595ac65e00, alma-0c695f336bb265c216f7580d, alma-46c44d88c85808a30abe4396, alma-5d2eac647b1caffc0399f7fb, alma-b066134477290f823c90fa58, alma-4490b98ebd1bb292cf7be570, alma-0e03ad75fcfbc172e17db3ed, alma-aebda2823cfbe5da62e9eaec, alma-d0d13c64d97968b31767e4a5, alma-2f69e065457643db27086f00

### runtime-manager

alma-fab6357cc46e0afe3e20300f, alma-1be76eae4b11dbcdae07b4eb, alma-4129e3f409a79b3d38a21046, alma-95ff055b8b66bf4cbca9f279, alma-29a28d1283ab2c445bd3ccaf, alma-c0411eed574d1c9e19fb3d05, alma-7281b2c2ab87affb0fa1d77d, alma-fa682c4e155d67c2da71234d, alma-62edff09e6688088a39f7ac8, alma-dbfa31eb16cc5f0a78cfaf37

Additional cross-kind checks: all access-policy files were joined to the package-file table; only the local sudoers grant lacked an unchanged package match. All 299 policy identifiers matched XML action elements. Generated autostart units had runtime persistence. The two generated SSH aliases also had runtime persistence and were corrected before completion. The entire group record, including membership, was considered; empty named membership is not evidence that a group is inert.

## Individually decided objects

The nine timer entries describe future live deadlines; systemd creates those schedules. The nine socket entries omit owning executables, so creator UNKNOWN is explicit. Four sudo report headings are textual program output and RECORD. Two sudo default-value rows and two broad permission rows match unchanged packaged sudoers; the passwordless local grant is SETTING-OWN, as is its source file. The two stopped-container rows refer to the same retained executable instance from the same image and are PROGRAM-DERIVED. Both image rows identify the same executable image, already used successfully, and are PROGRAM-OWN. This is duplicate inventory representation, not duplicated ids.

NetworkManager's added connection UUIDs in `D1/in/control/alma/actions-logs/network_connection.log` match the two local profile rows and their persistent files: four SETTING-OWN rows. `D1/in/control/alma/actions-logs/user_service.stderr` establishes the locally enabled authentication service: its service and file rows are SETTING-OWN. No local path is reproduced here. Initial ethernet profile origin is unknown; the loopback profile listing does not establish persistent versus automatic creation. The unchanged packaged supplicant file is INSTALLED-PACKAGE.

## Validation

The assigned input ids and output ids have equal sets and counts, each once. Each decision is allowed, every row has six fields, all sentence ids exist, and word limits hold. Counts follow in the completion record. This is mechanical verification, not independent adjudication.

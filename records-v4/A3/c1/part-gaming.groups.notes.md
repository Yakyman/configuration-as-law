# Gaming stored-member groups, c1

Scope: all 1,872 input rows whose inventory kind is `2:stored-ownership-unresolved`. The inventory label is not a classification. (not published: orchestration or scratch), `TEXT.md` Sections 8.1–8.3 and 8.5, `SENTENCES.md`, and `A3/in/FACTS.md` were read first. No other classification was consulted.

The full tables named by these rows contain 35,128 immediate members. Each table was read completely, its count checked against the row metadata, and its traversal-completeness flag checked. Members include directories as well as files, symlinks, sockets, FIFOs and devices. A directory is not silently replaced with its recursive contents. Classification of a separate row for its contents does not settle the directory entry's origin.

(not published: direct evidence at least 2 MB) identifies every member by input group id, one-based member-table row number, and basename. These three fields refer unambiguously to the complete original table. It gives each member's decision and missing fact or deciding reason. Every MIXED row references this exact map. It also records the reasoning for homogeneous rows rather than concealing exceptions in a sampled group.

## Facts used

- (not published: over 20 MB): installed package membership and whole-file integrity. A missing entry was not treated as proof of non-package origin. The inventory explicitly reports incomplete package ownership coverage in `metadata.json`.
- (not published: direct evidence at least 2 MB): installed native package identity and explicit/dependency reasons. The runtime creators used here all have known native package reasons; their decisions are named in the member map and output reasons.
- (not published: direct evidence at least 2 MB): installation provenance is frequently explicitly unknown. Timestamps and script mentions do not prove that a configuration value was created during installation.
- (not published: over 20 MB): persistence, actual types, symlink targets, and device/inode identity. It establishes the aliases `/bin` → `usr/bin`, `/sbin` → `usr/sbin`, `/lib` → `usr/lib`, and `/lib64` → `usr/lib64`. Package joins normalize these observed aliases. Identical device/inode pairs also recover the CUPS backend hardlinks; a matching prefix hash alone never establishes identity or unchanged status.
- All 35,128 members have known persistence: 34,096 persistent and 1,032 runtime. Persistent sockets/FIFOs were not automatically called transient merely because their active endpoints are transient.
- Input action logs for launcher installation, Windows-program execution, and user settings were also examined. They establish executions and installation events, but do not provide full current-versus-installed comparisons for every Steam, Wine, or downloaded payload member.

## Deciding sentences

S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”

S8.2-9: “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”

S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

S8.2-15: “Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.”

S8.2-5: “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.”

## Rules and hand checks

The script `part-gaming.groups.py` applies the following member rules in order and aggregates only after all members are decided. UNKNOWN is a missing-fact result, not a proposed repair to the text. Section 8.5's storage and enforcement design questions are not gaps.

### Package and provenance evidence

An unchanged manifest member, including a verified path alias or identical inode, is INSTALLED-PACKAGE by S8.2-6–8 and S8.2-16. Otherwise a missing first-question fact remains UNKNOWN if its possible answers change the decision. In particular, a Steam asset can be unchanged package content or altered content; its pathname and first 4,096-byte signature cannot establish the former. An executable bit does not establish that an arbitrary log or asset contains executable code. A directory's lack of a manifest entry does not establish who created it.

Hand-checked ten group rows for these fact conditions:

- `gaming-f0a9df95219dd5d754a0f6e9`: GRUB entries; no full package/integrity join for these generated/copied paths.
- `gaming-61483700375520f8155e3df6`: configuration and state; recorded origin uncertainty prevents assuming defaults.
- `gaming-d5aba99d46bf02ccbb790689`: alternatives links; target names do not establish original/default versus later selected link state.
- `gaming-b9fd058e4c13a03c9e02ea66`: one AppArmor tuning file; creation provenance unknown.
- `gaming-d451adfd92919bb0ea885c82`: CUPS configuration and subscriptions; no complete provenance/integrity evidence.
- `gaming-c002466b0636040c062a265e`: five PAM generated configuration candidates; installation origin unknown.
- `gaming-37978ac0c56987eb4914c41e`: certificate links and bundle; selected trust sources and current original equivalence unestablished.
- `gaming-8ac297c67303303673ce1fdc`: service link and directories; creation/default origin unestablished.
- `gaming-365cbfb8a4e3624fbec64364`: four service activation links; default versus person-selected state not established.
- `gaming-c6a6144cf5efeea6c1f882d5`: single persistent directory; no observed origin sufficient to choose installed/record/material.

All six native groups with recovered unchanged members were additionally checked individually: `gaming-fc557f3125938f34d3727148`, `gaming-f14f42f597efb3f8a03d34e3`, `gaming-0b9c75abae9461b0be7b041d`, `gaming-7045b2cfb39b6919d6cbb076`, `gaming-b5b399a1952d145cba092894`, `gaming-4b2f118928192eae89e5ccb0`. The first, fourth, fifth and sixth are MIXED because their remaining links or generated objects lack deciding integrity/provenance facts. The AppArmor group and six CUPS backend members are entirely INSTALLED-PACKAGE. The separate `gaming-5024a5607275cd351095bdf1` directory group has package associations but unknown integrity, hence UNKNOWN.

### Python bytecode

Persistent `cpython-312.pyc` members under the system Python `__pycache__` directories, with corresponding unchanged package-owned `.py` sources, are PROGRAM-DERIVED by S8.2-9–10 and S8.2-16. Each source is joined separately; a directory containing a cache directory is not itself executable bytecode.

[Python FAQ](https://docs.python.org/3/faq/programming.html) states: “creation of a .pyc file is automatic if you’re importing a module”. [Debian Python Policy](https://www.debian.org/doc/packaging-manuals/python-policy/) states: “the byte-compiled modules must not be shipped with the binary package”. This distinguishes generated executable cache files from unchanged files received in the package.

Hand-checked ten complete bytecode group rows, confirming version-tagged filenames, persistent files, and their unchanged source-package joins:

`gaming-4907aa06823bfde8dce6f982`, `gaming-d6be9189d16dc2825d0ebaf3`, `gaming-d7207a900f35c49f1cde2f7e`, `gaming-fbb29da26124e26b433935a0`, `gaming-23382bc4609b7d0a44eba5a4`, `gaming-2be08990cdfb1267e67f6400`, `gaming-92fe7321497a6eb0dba3ac6d`, `gaming-d7cc084b7bc880125dedcef7`, `gaming-d6a1624ce14a9344ec8d659f`, `gaming-83d99db0fb36ece0bc035be7`.

### Program records

Observed diagnostic/history files in the enumerated logging locations and package manager `.list` inventories are RECORD by S8.2-15 and S8.2-2. This is not a generic rule for everything in a cache or data directory: possible code caches, launch values, credentials, package metadata received in archives, and directories retain separate decisions.

[Steamworks uploading documentation](https://partner.steamgames.com/doc/sdk/uploading) describes `content_log.txt`: “Lists all logged SteamPipe operations and errors.” [systemd file hierarchy](https://www.freedesktop.org/software/systemd/man/256/file-hierarchy.html) describes `/var/log` as persistent log storage and `/run` as runtime storage. The input's action-log files are the captured command outputs themselves. The dpkg `.list` files contain installed path inventories; their raw contents are available in the metadata-read outputs.

Hand-checked all ten groups to which this record rule applies:

`gaming-2dac226320b6f354608c3b7b`, `gaming-0528c26cdd0cdd77fcb380b1`, `gaming-2ffd964e585c353313bc520e`, `gaming-63e2acee9dd1c09ce676ad5f`, `gaming-ef0828c6f747894897b5efe1`, `gaming-7dc478f00b1ef77f21328793`, `gaming-2720a9e9ed4064eab6eeaece`, `gaming-fa9b5f9fc3de1f5bc7bdb2de`, `gaming-9c924a29b4d7e177f169f369`, `gaming-3c49d8ede866731e9d36a16a`.

The Lutris cache, top log directory and dpkg information directory are MIXED. Their maps distinguish log/files-list records from directories, metadata or scripts whose required provenance/integrity fact is missing. In particular, maintainer scripts were not mislabeled records merely because dpkg stores them.

### Runtime objects

Members positively marked runtime, whose creating subsystem is identified, are RUNTIME by S8.2-5. Their creator's installed native package and its explicit/dependency reason determine the named inherited decision. The runtime map distinguishes NetworkManager, CUPS, D-Bus, systemd, udev, and session daemons. [udev documentation](https://www.freedesktop.org/software/systemd/man/latest/udev.html) states that matching rules provide information “to be stored in the udev database”. [systemd execution documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html) documents runtime directories and private temporary directories.

Hand-checked ten complete groups for persistence and creator association:

`gaming-70a5f4e6de517cdfe4d6d563`, `gaming-0a11dcbb1aa2221152ddbe04`, `gaming-579e9ff33bed334e9ea093a5`, `gaming-7b7b6ebff6237a7347c1322f`, `gaming-64b489715c2bde942a579bd0`, `gaming-17c9f1235ee1cb98f258b3a5`, `gaming-1733df06abe7085517577d40`, `gaming-3fe08d01e4f4b7617de68a23`, `gaming-3b45f88a79f6db15c8923720`, `gaming-de883a85e06bfe7120ecc147`.

Four heterogeneous groups additionally contain runtime members with unestablished creator association, individually inspected: `gaming-d6e7cd8207d135165f0e39be`, `gaming-8b7138a7e9691ba6cff8e1e3`, `gaming-48246940849ffde2a4c99c53`, `gaming-cca7f34869a6ff1d0fe2858a`. Their member map names the missing runtime creator fact; `/run` is MIXED because several creators are known. A pathname alone was not used to choose a creator for shared lock/session roots.

## Validation

The script appends and flushes each finished group row, preserves pre-existing ids, and verifies exact id multiset equality with this input subset. All 1,872 ids occur exactly once. It checks the 15-word description and 30-word reason limits. All member counts and complete flags pass. The final parent merge must validate the full gaming part's allowed decisions and id coverage.

Counts: UNKNOWN 1,700; RUNTIME 120; PROGRAM-DERIVED 35; MIXED 8; RECORD 7; INSTALLED-PACKAGE 2.

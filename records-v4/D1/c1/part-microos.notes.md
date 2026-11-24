# MicroOS c1 classification notes

Scope: D1/in/part-microos.tsv only. No other classification or earlier-night evidence was consulted. The three parallel subsets share these fixed instructions and only MicroOS inventory evidence. This file records the L1 rules; the complete code and stored-group rules and their hand checks are included below when those subsets finish.

Facts read: D1/in/FACTS.md; D1/in/raw/microos/objects.tsv, package-files.tsv, configuration-origin.tsv, coverage.tsv, and the cited raw outputs and query scripts. Persistence is taken from explicit filesystem records. Snapshot copies are not certified by current-root integrity. These are classifications, not acceptance of the hypothesis or independent review.

## Sentence anchors

- S8.1-6: **Package**—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.
- S8.2-5: What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.
- S8.2-6: What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.
- S8.2-7: Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?
- S8.2-8: Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.
- S8.2-9: Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?
- S8.2-11: Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?
- S8.2-12: Then it is a **setting**, however it was entered and whatever file stores it.
- S8.2-13: Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.
- S8.2-16: What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.
- S8.2-17: A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.

## Public documentation

- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html — "List units that systemd currently has in memory." The list-timers section likewise describes in-memory timers. list-unit-files describes installed unit files and enablement state; it does not establish file origin.
- https://www.kernel.org/doc/Documentation/ABI/stable/sysfs-module — "The name of the module that is in the kernel." Entries include built-in and dynamically loaded modules.
- https://docs.kernel.org/driver-api/driver-model/driver.html — "When a driver is registered, a sysfs directory is created in its bus’s directory."
- https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html — "Actions correspond to operations that clients can request the mechanism to carry out"; their XML action definitions were matched directly to captured unchanged policy files.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-sysusers.html — "systemd-sysusers creates system users and groups". The mechanism does not prove which actor created a particular observed account.
- https://www.kernel.org/doc/html/latest/filesystems/proc.html — "Link to the executable of this process" describes the exe link; unsuccessful lookup alone does not identify the program.

## Homogeneous L1 rules and manual checks

Ten evenly distributed rows per rule were displayed and inspected against their records and relevant joins. The following lists retain exactly those IDs. Scripted application is in part-microos.l1.py; the rule assignment audit is part-microos.l1.rules.json.

### packages (376 rows)

S8.1-6,S8.2-7,S8.2-8,S8.2-16. Installed RPM packages answer question one. Apply the retained reason field, not native_reason: explicit => INSTALLED-OWN; dependency => INSTALLED-DERIVED. This determines the required recording line; no declaration was supplied, so actual compliance is not asserted.

Hand-checked IDs:

- microos-78b5b375771cc1326bf69347: INSTALLED-DERIVED; predicate checked against retained record.
- microos-9fbd182445aa3ea46cfed6ec: INSTALLED-DERIVED; predicate checked against retained record.
- microos-c19707c106f747be0c089cd2: INSTALLED-DERIVED; predicate checked against retained record.
- microos-3243e547471fd4701b061f39: INSTALLED-DERIVED; predicate checked against retained record.
- microos-5249669ea44c45222d389136: INSTALLED-DERIVED; predicate checked against retained record.
- microos-8079c67e8b2a16d0c7b7d72c: INSTALLED-DERIVED; predicate checked against retained record.
- microos-447fd15bf9717c4dbb45d4ce: INSTALLED-DERIVED; predicate checked against retained record.
- microos-cd55fc13d19958ea07d3cd61: INSTALLED-DERIVED; predicate checked against retained record.
- microos-588c1b1bf409be06fa36222b: INSTALLED-DERIVED; predicate checked against retained record.
- microos-49fb45ef8b71d66041277d2b: INSTALLED-OWN; predicate checked against retained record.

### packaged-policy (145 rows)

S8.2-6,S8.2-7,S8.2-8,S8.2-16. For the captured policy files and action definitions explicitly located in their XML contents, exact-path unchanged package integrity answers question one and gives INSTALLED-PACKAGE. Action identifiers are declarations of operations, not commands a person typed. JavaScript policy code is also decided by question one before the code question.

Hand-checked IDs:

- microos-da6b6f0282afd4df50793b1d: INSTALLED-PACKAGE; predicate checked against retained record.
- microos-c867c964daebdd97f383cadb: INSTALLED-PACKAGE; predicate checked against retained record.
- microos-ddbe1f64a39018cca8fc9295: INSTALLED-PACKAGE; predicate checked against retained record.
- microos-a1d287f31ef1b292c4251f88: INSTALLED-PACKAGE; predicate checked against retained record.
- microos-0ac3898fc36aeb9c2223f74d: INSTALLED-PACKAGE; predicate checked against retained record.
- microos-8a498d07ba9062cb311ac5dc: INSTALLED-PACKAGE; predicate checked against retained record.
- microos-60e31232e558ab46746c16f9: INSTALLED-PACKAGE; predicate checked against retained record.
- microos-13bd572af72137bd7e06fff1: INSTALLED-PACKAGE; predicate checked against retained record.
- microos-14beef1a9661518aca98e717: INSTALLED-PACKAGE; predicate checked against retained record.
- microos-85978a69929daf05c51e0994: INSTALLED-PACKAGE; predicate checked against retained record.

### identity-origin (43 rows)

S8.2-11,S8.2-12,S8.2-13,S8.2-17. Account and group identity/access values are settings. Their database records lack creation or later-choice provenance. Installation-default and individually chosen origins yield different required lines, hence UNKNOWN. Empty supplementary member lists do not remove group identity or access significance. Numeric primary groups remain separate account facts.

Hand-checked IDs:

- microos-13cd5b718c5e71a530a2bed1: UNKNOWN; predicate checked against retained record.
- microos-2f586359d0d957df639cb748: UNKNOWN; predicate checked against retained record.
- microos-a531caca62cb2eef2eab36da: UNKNOWN; predicate checked against retained record.
- microos-3ecb9c0894c818e99d0639ee: UNKNOWN; predicate checked against retained record.
- microos-8adfbfceb575897b7a5d0c93: UNKNOWN; predicate checked against retained record.
- microos-79832895029d104f3c3baa8e: UNKNOWN; predicate checked against retained record.
- microos-ab6df478dccd1df3259ac90a: UNKNOWN; predicate checked against retained record.
- microos-0e414890acc44df08e995154: UNKNOWN; predicate checked against retained record.
- microos-5951783e7743030e7a6d05eb: UNKNOWN; predicate checked against retained record.
- microos-eaa0642b203330ac727ca215: UNKNOWN; predicate checked against retained record.

### manager-runtime (165 rows)

S8.2-5,S8.2-7,S8.2-16. The service/timer queries are list-units and list-timers: the observed objects are in-memory unit states and timer relationships. They are RUNTIME, created by the systemd manager whose exact executable is unchanged and INSTALLED-PACKAGE. This does not classify a persistent service definition or an enablement choice as runtime. Not-found references still exist in manager memory; they do not establish installed service files.

Hand-checked IDs:

- microos-5aed4583bf9b0b1395f36fab: RUNTIME; predicate checked against retained record.
- microos-65033770ab810dab4f8330d3: RUNTIME; predicate checked against retained record.
- microos-4bd8518587e592836f9c8e55: RUNTIME; predicate checked against retained record.
- microos-fdcdb2fc1d6dd5514947da43: RUNTIME; predicate checked against retained record.
- microos-df5db76ab27a0fe62205ea8c: RUNTIME; predicate checked against retained record.
- microos-9e5c87643fdc0ddae47ddb4a: RUNTIME; predicate checked against retained record.
- microos-e0caad0a6ae37e22499c091f: RUNTIME; predicate checked against retained record.
- microos-8fd67d375120db591523aa25: RUNTIME; predicate checked against retained record.
- microos-f70503e6d85736a26401f6d8: RUNTIME; predicate checked against retained record.
- microos-3cee21584ca44ac5c5bfa79f: RUNTIME; predicate checked against retained record.

### unit-origin (260 rows)

S8.2-7,S8.2-11,S8.2-13,S8.2-16,S8.2-17. A list-unit-files row supplies a unit name, state and possibly preset, not the selected definition path or enablement origin. Package basenames do not prove the selected file: the live /etc subvolume is opaque in this traversal. Overrides and enablement changes remain possible facts, making UNKNOWN necessary. An enabled state equal to the preset does not prove installation-default provenance.

Hand-checked IDs:

- microos-3f91cb28ce6d2aed43546a0e: UNKNOWN; predicate checked against retained record.
- microos-bac9f51f4146db5ba9934292: UNKNOWN; predicate checked against retained record.
- microos-de59386305160618d511b5bd: UNKNOWN; predicate checked against retained record.
- microos-668ff3f7d90dd5b77c3c34f0: UNKNOWN; predicate checked against retained record.
- microos-212e4ee5c74af242724bff1f: UNKNOWN; predicate checked against retained record.
- microos-2fe14b5bc79f3a65cfec1e5b: UNKNOWN; predicate checked against retained record.
- microos-47d59ea148ac19b8b548d676: UNKNOWN; predicate checked against retained record.
- microos-aa79f7e79cf351507df16c5c: UNKNOWN; predicate checked against retained record.
- microos-ad5122b5aab82bb2a0fdbe96: UNKNOWN; predicate checked against retained record.
- microos-a2308472231b716e9422c66e: UNKNOWN; predicate checked against retained record.

### process-known (26 rows)

S8.2-5,S8.2-7,S8.2-16. A live PID with a captured executable path that joins an unchanged package-file record is RUNTIME; name that executable and its INSTALLED-PACKAGE decision. The observations identify executable programs, not the process parent.

Hand-checked IDs:

- microos-05d2bb8eb5cb733104b98595: RUNTIME; predicate checked against retained record.
- microos-7ae2f67f18a5b6ac2031f190: RUNTIME; predicate checked against retained record.
- microos-04f548044a041a1ee52830a4: RUNTIME; predicate checked against retained record.
- microos-4fc232041a6f9aabb853cf49: RUNTIME; predicate checked against retained record.
- microos-a0ea4cd28ea51fad3f0ae215: RUNTIME; predicate checked against retained record.
- microos-a9d0812f46a46d7ed47d9c9b: RUNTIME; predicate checked against retained record.
- microos-5815274b265c1b9c99a3674f: RUNTIME; predicate checked against retained record.
- microos-c0e5d083ec0c66b0fa302ec8: RUNTIME; predicate checked against retained record.
- microos-3a8f932b3c33c45c039505ca: RUNTIME; predicate checked against retained record.
- microos-499353f1b1407b760f8e3e75: RUNTIME; predicate checked against retained record.

### process-unresolved (106 rows)

S8.2-5. A live PID with failed executable lookup is runtime, but its producer cannot be named. UNKNOWN records that missing fact as required by the task. An inaccessible or vanished process and a kernel thread cannot be distinguished by the retained unknown string.

Hand-checked IDs:

- microos-f2bf2068cf868759128fa09f: UNKNOWN; predicate checked against retained record.
- microos-d9520da1fef81675d6297acd: UNKNOWN; predicate checked against retained record.
- microos-d170b4f1fca0fdaaf3fbd1b9: UNKNOWN; predicate checked against retained record.
- microos-c663c504d436dd9cb9e7a6a6: UNKNOWN; predicate checked against retained record.
- microos-79812699173cfbd6e0e07832: UNKNOWN; predicate checked against retained record.
- microos-729b8d64b28be718c01bd904: UNKNOWN; predicate checked against retained record.
- microos-26f621d72ee3afd6ce351d91: UNKNOWN; predicate checked against retained record.
- microos-1d94d624d43758939e75d026: UNKNOWN; predicate checked against retained record.
- microos-117ac3373f25ac7cc9d136b3: UNKNOWN; predicate checked against retained record.
- microos-07d25ce8385bf219c3f82cce: UNKNOWN; predicate checked against retained record.

### kernel-runtime (306 rows)

S8.2-5,S8.2-7,S8.2-9,S8.2-16. The queries enumerate sysfs module and driver registrations, not stored module files. Linux kernel creates these RUNTIME interfaces. Its executable recording decision is UNKNOWN because the package-file table reports unknown integrity for the kernel image; no unchanged image is inferred from an unchanged boot symlink.

Hand-checked IDs:

- microos-a158587e0842063326e2484d: RUNTIME; predicate checked against retained record.
- microos-d97461155d078b67a33c3c85: RUNTIME; predicate checked against retained record.
- microos-408dbaab2f52c90ab0f116d7: RUNTIME; predicate checked against retained record.
- microos-13706b6821d47810291a4433: RUNTIME; predicate checked against retained record.
- microos-8b4a10a86e010c697e3c1b8a: RUNTIME; predicate checked against retained record.
- microos-bae799b23eb81a6c72ef7734: RUNTIME; predicate checked against retained record.
- microos-c34abe637ca27d719a5152f7: RUNTIME; predicate checked against retained record.
- microos-c8fb1fe9caa90fd884a93cee: RUNTIME; predicate checked against retained record.
- microos-5c18b59cf3277ae56d9dc185: RUNTIME; predicate checked against retained record.
- microos-f5445ce056c88353ae653ff1: RUNTIME; predicate checked against retained record.

## Individually decided L1 exceptions

- microos-3910e36316edcb214ddebea8: RUNTIME. systemd creates this runtime mask; its unchanged packaged executable is INSTALLED-PACKAGE.
- microos-c9038b728dc737c9e37cc9a9: RUNTIME. systemd creates this runtime mask; its unchanged packaged executable is INSTALLED-PACKAGE.
- microos-135bf562f7e471dafc32c00b: RUNTIME. systemd creates this runtime mask; its unchanged packaged executable is INSTALLED-PACKAGE.
- microos-c1c18b8f2aad6b4fd8aab972: UNKNOWN. Socket is runtime-only; missing owning program and its recording decision. A conventional port number does not establish ownership.
- microos-d6e8a40c92c31909b67ab099: UNKNOWN. Socket is runtime-only; missing owning program and its recording decision. A conventional port number does not establish ownership.
- microos-f8e7465f61b925afa9e849c9: UNKNOWN. Socket is runtime-only; missing owning program and its recording decision. A conventional port number does not establish ownership.
- microos-78d4ec5980b48fce38877151: UNKNOWN. Socket is runtime-only; missing owning program and its recording decision. A conventional port number does not establish ownership.
- microos-e346e6a4b38f0e6fb9c4155f: RUNTIME. NetworkManager creates this runtime connection profile; its unchanged packaged executable is INSTALLED-PACKAGE.
- microos-2371b85ca263f1507d4eeb5a: RUNTIME. NetworkManager creates this runtime connection profile; its unchanged packaged executable is INSTALLED-PACKAGE.
- microos-d047f8d3c4b57cba8b295f2f: RUNTIME. NetworkManager creates this runtime connection profile; its unchanged packaged executable is INSTALLED-PACKAGE.
- microos-841d39fd7b56a0c7609af03f: RUNTIME. Inventory probe creates this process; probe decision UNKNOWN because its installation or derivation provenance is not retained.
- microos-7380228a01744e649019aaf4: RECORD. This row is a report heading emitted by sudo, not an access value or executable command.
- microos-8db6691105c8ac421e0e73b7: UNKNOWN. Policy values are established, but installation-default versus later-choice provenance is absent; this determines SETTING-DEFAULT versus SETTING-OWN.
- microos-77aa628b348e4d7bb3c040f1: RECORD. This row is a report heading emitted by sudo, not an access value or executable command.
- microos-faa9663df42f9349b7627ba9: UNKNOWN. Policy values are established, but installation-default versus later-choice provenance is absent; this determines SETTING-DEFAULT versus SETTING-OWN.
- microos-514aeb3931dc5e7630645de5: RECORD. This row is a report heading emitted by sudo, not an access value or executable command.
- microos-c2cb0aae2410f18e15023fe3: UNKNOWN. Policy values are established, but installation-default versus later-choice provenance is absent; this determines SETTING-DEFAULT versus SETTING-OWN.
- microos-ea85a44a147204be0182f10a: UNKNOWN. Policy values are established, but installation-default versus later-choice provenance is absent; this determines SETTING-DEFAULT versus SETTING-OWN.
- microos-bb37078a67d144be5e2cc701: RECORD. This row is a report heading emitted by sudo, not an access value or executable command.
- microos-68691ac08ba5b8bb07517ff3: UNKNOWN. Policy values are established, but installation-default versus later-choice provenance is absent; this determines SETTING-DEFAULT versus SETTING-OWN.
- microos-35c8155b46fe134ff542daa0: RECORD. This row is a report heading emitted by sudo, not an access value or executable command.
- microos-58a5bf771842e6e74625f86c: UNKNOWN. Policy values are established, but installation-default versus later-choice provenance is absent; this determines SETTING-DEFAULT versus SETTING-OWN.
- microos-fa208e794205b3f9734e573c: RECORD. This row is a report heading emitted by sudo, not an access value or executable command.
- microos-14b49eb5b4dbb9b8e9701af7: UNKNOWN. Policy values are established, but installation-default versus later-choice provenance is absent; this determines SETTING-DEFAULT versus SETTING-OWN.
- microos-2651ae8b3936cafe8ab643b8: UNKNOWN. Policy values are established, but installation-default versus later-choice provenance is absent; this determines SETTING-DEFAULT versus SETTING-OWN.

Network profile names join the three explicit /run/NetworkManager/system-connections paths. All three have runtime persistence. Sudo heading rows are report text rather than inferred policy values; policy-bearing rows remain UNKNOWN because creation provenance was not captured. Socket port numbers alone do not identify their owning program. Runtime masks are identified explicitly by masked-runtime.


---

# Code, image, and snapshot slice

Read (not published: orchestration), TEXT.md Sections 8.1–8.3 and 8.5, SENTENCES.md, and the microos fact index. No other classification was consulted. The output contains 1,896 assigned rows. All are explicitly persistent in their retained metadata; none qualifies as RUNTIME merely because a disposable installation was inventoried.

## Homogeneous rule: retained snapshot files

Applied only to the 1,875 individual files below snapshot 1. Decision: UNKNOWN. S8.2-7 asks whether the object "was it obtained as part of such a package and does it remain as received?" S8.2-16 distinguishes the package line from a source line. Snapshot-specific package provenance and installation integrity were not collected. The current-root package-files table cannot be applied to a different snapshot by removing the prefix. Mode bits and shebang flags are not package provenance. A prefix digest does not establish full-file integrity. Equal full-file contents establish equality, not how a copy was obtained. These are missing facts, not a textual gap.

The script checks persistence for every row. Of these snapshot files, 1,873 have a current-root counterpart with unchanged integrity; one counterpart has unknown integrity and one lacks an entry. Exactly 465 also match full-file size and signature against a current-root unchanged counterpart. These stronger matches still do not identify actual snapshot-copy provenance. No independence or source-generation assumption is added.

Ten hand-inspected rows, including scripts, binaries, and shared libraries:

- microos-900b60a922695141d874da92: theme activation script; persistent, 1,748 bytes, no exact snapshot package entry.
- microos-9d3252cb482db18294bcb635: egrep wrapper; persistent, 102 bytes; full equality still lacks snapshot provenance.
- microos-171b4cdc14cf247f11ca2b46: nsenter executable candidate; persistent, 39,440 bytes; only 4,096 hashed.
- microos-31797ce7bc86785e054b07c0: unlink executable candidate; persistent, 39,312 bytes; only prefix retained.
- microos-7cdfdd40f0fcf7b8e2d81b3b: dracut module setup script; persistent, 3,502 bytes; missing snapshot provenance.
- microos-5faf66d2cfde8d08355a62b4: dracut pollcdrom setup script; persistent, 217 bytes; missing snapshot provenance.
- microos-0ff4c854405acc4194570659: modem plugin library; persistent, 26,832 bytes; prefix cannot certify integrity.
- microos-9eca87132c50b87369acf227: transport crypto library; persistent, 59,520 bytes; prefix cannot certify integrity.
- microos-c4f62b944c241e9a017e3b4f: filesystem plugin library; persistent, 18,520 bytes; prefix cannot certify integrity.
- microos-d56723cb64ff372b378c8463: SELinux boolean utility candidate; persistent, 14,520 bytes; prefix cannot certify integrity.

Checks used the exact object JSON in D1/in/part-microos.tsv, D1/in/raw/microos/raw/0004-filesystem.out and exact-path lookup in D1/in/raw/microos/package-files.tsv. The rule stops at the unresolved first question; it does not assume all executable-mode objects actually execute.

## Individually decided rows

The nine live GRUB image files under the packaged share directory each have an exact-path unchanged integrity record. Each is INSTALLED-PACKAGE by S8.2-6–8 and S8.2-16, regardless of executable mode: boot.img, boot_hybrid.img, cdboot.img, diskboot.img, kernel.img, lnxboot.img, lzma_decompress.img and pxeboot.img for the BIOS target, and kernel.img for EFI. These nine records were individually checked, not sampled.

The two opaque subvolume rows have no complete member lists; classifying them as homogeneous package content or material would require missing facts. The collector calls the live configuration directory a snapshot, but its label alone does not establish its semantic class. Both are UNKNOWN.

The ten other individual rows comprise four EFI-directory files, two boot images, a GRUB module information script, a theme script, and two shell startup files. Their identity can be described, but no retained record establishes package delivery or whether system generation from a source rather than independent copying supplied each object. These are UNKNOWN for the recording line. Matching packaged bytes in startup skeleton files or the boot image is not a provenance record. No runtime inference is made from boot-time use.

## Public documentation used for identities and limits

- https://kubic.opensuse.org/documentation/transactional-update-guide/tu-howitworks.html : "In the first step, a new snapshot of the current root file system will be created." Its workflow permits later modification; it cannot certify this snapshot's actual per-file origin or integrity.
- https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files : "it reads and executes commands from" the startup file. This establishes that shell startup files are code under S8.2-9 and S8.2-23, not merely values.
- https://www.gnu.org/software/grub/manual/grub/grub.html : "images for booting from CD-ROM drives are now constructed using" the documented boot images. The manual describes boot image roles and construction, but does not establish the origin of an observed copy.

The direct GNU subsection fetches timed out; the indexed official manual excerpts supplied the quoted material. No machine query or experiment was run.


---

# Stored-object classification notes

Scope: all 3,174 `L2:stored-outside-packages` input rows. Only the permitted task text and this system's raw inventory were consulted. Each exact member TSV was read in full, its count checked against the source JSON, and its completeness flag checked. Filesystem persistence came from the member TSV and the exact per-path filesystem record. Package-file integrity was joined by exact path; raw RPM manifest paths were also inspected for the residual groups. No snapshot-prefix stripping was used to transfer installation integrity. A prefix hash, read-only status, executable permission, and a suggestive inventory label are not installation-integrity evidence.

`part-microos.stored.py` preserves existing output rows and flushes every appended row. Its manually enumerated residual groups are individual decisions, not inferred matches from a generic name classifier.

In every MIXED reason, **member N means data row N of the exact member TSV named in that row's basis**, counting from one and excluding its header. Ranges include both endpoints. Each MIXED reason partitions the complete member list. UNKNOWN members share the stated missing fact; UNKNOWN does not claim two already-established member classes.

## Deciding text

- S8.2-5: “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.”
- S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”
- S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”
- S8.2-9: “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”
- S8.2-15: “Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.”
- S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”
- S8.2-17: “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.”
- S8.2-23: “A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.”

## Rule S: snapshot-member provenance uncertainty

Applies to 2,964 groups rooted at the retained snapshot tree. Every member is persistent, and none has an exact-path package-file integrity entry. These are homogeneous in the decisive missing provenance/integrity fact, not homogeneous in file format. A current-root manifest does not establish that a differently stored snapshot member was obtained with an installed package and remains as received. If that fact is true, question one precedes code, settings, and records; if false, those later questions and source-line provenance matter. Public snapshot documentation cannot establish the missing historical facts of these particular copies. Therefore UNKNOWN, not a text gap, and not a blanket exemption for snapshots. Section 8.5's exclusion of rollback mechanism design does not exempt executable snapshot members from question two.

Primary documentation: https://susedoc.github.io/doc-sle/main/html/opensuse-reference/cha-snapper.html — “Snapshots taken from the root file system (defined by Snapper's root configuration), can be used to do a system rollback.”

Ten hand checks (complete lists inspected):

- microos-e8d4e9636694c6a9239e60d8: one font; persistent; prefix hash only, no snapshot installation record.
- microos-6f2ef8904d971d8fd45b6017: 37 translation files; same missing snapshot provenance despite descriptive suffixes.
- microos-6f297717869bcff1f5915701: two audit plugin configuration files; package defaults versus later copies not established.
- microos-968f58408e01fc92ebbbcbd1: one audit rules file; chosen/default/history origin absent.
- microos-8394dfb686660b222beb8a3c: one policy module directory; directory execute permission does not prove code.
- microos-b1b47346e524f424ba948e3b: three policy compilation files; prefix signatures do not prove package reception.
- microos-86e5186fbb5ecac0fe6e4396: three other policy compilation files; same missing provenance.
- microos-b2124efe0ac2ac768edc2061: three policy compilation files; no exact snapshot manifest coverage.
- microos-3dd84eae292aa0d8e3b96fa4: one compressed kernel module; code character does not bypass unknown question one.
- microos-537cfac91331a77bceee0878: six executable shared libraries; execute permission does not establish own versus package/derived coverage.

## Rule R: verified volatile working objects

Applies only when every member's persistence is `runtime`. These members exist in volatile runtime storage; S8.2-5 supplies RUNTIME before the four-object questions. Each reason names its creating service program and that program's decision. The package-file table establishes unchanged executable files for systemd, systemd-udevd, NetworkManager, chronyd, dbus-broker, fsck, blkid, LVM, mount, polkitd, rebootmgrd, sysextmgrd, wtmpdbd, agetty, auditd, dmeventd, dracut, and systemd-tmpfiles. They are INSTALLED-PACKAGE by S8.2-7 and S8.2-16. The grouped runtime root lists the multiple service creators. Persistent service-private storage was excluded from this rule.

Primary documentation: https://www.freedesktop.org/software/systemd/man/latest/udev.html — “The udev daemon, systemd-udevd.service(8), receives device uevents directly from the kernel”. This identifies the device-state producer; the raw persistence facts establish volatility.

Ten hand checks:

- microos-7b376f05940c758d2a37f25a: NetworkManager temporary configuration; one runtime member.
- microos-d56837a491224b6057bb1911: three runtime NetworkManager device records.
- microos-b9d5df898e3b476d5283db7d: three runtime NetworkManager connection files.
- microos-7ea3796712ff653f4dd19185: two blkid runtime cache files.
- microos-5d2c58c61ea05295e1882e18: chronyd PID and socket; both runtime.
- microos-d77c5bfcfd114e48a21363af: D-Bus container directory and bus socket; both runtime.
- microos-b664fb9fdbf168a622097c76: filesystem-check runtime lock.
- microos-811fd00b5fe4dbf0eae1b7ca: runtime LVM lock directory.
- microos-c3cebce608b5dd1fdb376dd0: three mount runtime bookkeeping files.
- microos-093d7f542f7d7820ae05b230: one udev runtime device-link record.

## Rule C: repository metadata cache

The 19 ZYpp cache groups contain repository metadata, signatures, solver indexes/cookies, and their storage directories. No installed RPM package archive or executable program appears in these lists. S8.2-15 expressly includes caches and working state. The fact that metadata can influence an installer does not make it code or a person's chosen system value. Accordingly RECORD.

Primary documentation: https://manpages.opensuse.org/Tumbleweed/zypper/zypper.8.en.html — “storing it in local cache (typically under /var/cache/zypp/raw/alias directory)”. The documented refresh operation also builds the solver cache.

Ten hand checks:

- microos-0a99fc43b8282959128ea705: one geographic mirror cache entry.
- microos-973779de3806881d2bacaf6b: one repository medium metadata file.
- microos-044b73e102c0cdee25dc3c66: one other repository medium metadata file.
- microos-e2e22c31f0b2d7ea6b4f5823: repository check marker and metadata directories.
- microos-aa22e2a773f9357d2fbbc775: repository check marker and metadata directory.
- microos-7cc2a7c5eef50507eed81020: cookie, solver data, and index.
- microos-117734517486366eda298f3b: cookie, solver data, and index.
- microos-d4e3c6c7eed7627e851bcbe0: cookie, solver data, and index.
- microos-30730ffcfc3d76aac8b29438: cookie, solver data, and index.
- microos-4c2af10b2e15f152df0dff86: cookie, solver data, and index.

## Rule M: generated MIME data

The 14 MIME groups contain generated type-description XML, indexes/cache files, and their generated directories. None of these members is an input package XML file. S8.2-23 distinguishes values from code; these generated descriptions are not a person's chosen setting. S8.2-15 therefore gives RECORD. S8.2-16 governs which line covers what has already qualified as installed; it does not reverse the ordered questions to classify every generated data file as installed.

Primary documentation: https://specifications.freedesktop.org/shared-mime-info/latest-single/ — “It scans all the XML files in the packages subdirectory, combines the information in them, and creates a number of output files.”

Ten hand checks; complete member metadata was checked for file type, persistent storage, XML extension, and absence of exact package membership:

- microos-cfb3363718fdffa8e2decf3b: one chemical type description.
- microos-694303c3e26c4258aea1d9c7: five font type descriptions.
- microos-d57b64903524ac552f704f80: seven inode type descriptions.
- microos-93512b44fa58fc3da7d64afe: seven message type descriptions.
- microos-39fc4d3ee2703d92a368043c: eleven model type descriptions.
- microos-f44edeb7bae64c93251b6196: nine multipart type descriptions.
- microos-d11025d3c1706c2bf1f18c68: 33 video type descriptions.
- microos-4a6d90938dee0cb1148e2714: 19 content type descriptions.
- microos-e0e96d11a6b0449ff18790d9: one application type description.
- microos-819a45f8a130b43da2bc3d8c: 68 audio type descriptions.

## Rule D: directories with unknown creator

For the explicitly enumerated residual persistent directory-only groups, no member appears in the raw RPM file manifest, and no captured creation record identifies the creator. Directory execute bits mean traversal. Program-created working storage and person-created material are different S8.2-15 cases; therefore UNKNOWN. No inference is made from directory names alone. Ten hand checks: microos-9b1fbc813c5876fd618e71f2, microos-7e85ee24d5a79ba81acd55bf, microos-10f3f32ef128ab5c54608484, microos-13a878fb75c30087a0c945f2, microos-f259b60aca1fd13da7a98094, microos-fb60b6412ee79d20c1e490c3, microos-20f675737a015be831213148, microos-c3584b79f29f4bed45c410e1, microos-cbf1329980f813598d30e154, microos-1c25959e8ab1f682fdbeb3a3. Every listed member in these ten groups is a persistent directory; creation provenance is missing.

## Individual residual decisions

GRUB and EFI objects have recognizable functions, but their actual generation/installation lineage is absent. The documented normal installation procedure cannot prove how these particular copies arose. Primary documentation: https://www.gnu.org/software/grub/manual/grub/html_node/Invoking-grub_002dinstall.html — “generates a GRUB core image using grub-mkimage and installs it on your system.”

NetworkManager's persistent configuration/state files were separated from its leases, generated identity seed, and histories. Primary documentation: https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/NetworkManager.conf.html identifies the internal configuration file; the actual user-chosen versus default contents were not captured.

Generated certificate stores were not automatically called installed objects or inert cache. Their role is system trust; whether particular values represent selected policy or installation defaults is unretained. Primary documentation: https://github.com/openSUSE/ca-certificates — “by generating the certificate stores in /var/lib/ca-certificates”. The three exact groups are individually UNKNOWN for that missing origin fact.

Login accounting databases, journal files, timer trigger stamps, package history, and update cookies record events/state. No runtime-only exemption was inferred for their persistent storage. The eight persistent service-private temporary subdirectories and their parent group were each inspected and assigned RECORD as working storage. Authorized login keys are SETTING-OWN by S8.2-13 and S8.2-17.

No result here settles a hypothesis outcome or repairs the definition. Separate review remains external to this classification.


Final mechanical verification: part-microos.verify.py confirms 6,522 rows, exactly the input ID set and count, each once; all decisions belong to the prescribed vocabulary. Field word limits, sentence IDs, and absence of embedded tabs/newlines also pass. This is format verification, not independent acceptance. Counts are in part-microos.done.

CHECK 1: 1 confirmed gaps

Verification D1-H, corrected by FX-D1-H-1 on 2026-11-23 UTC. The outcome is **0 under both readings A and B** in `check-inputs-v4/QUESTIONS.md`. The frozen adjudication satisfies the separate disagreement failure condition; the archive-of-code gap also survives verification. Missing facts remain, and Gentoo supplied no inventory.

The verification used `TEXT.md`, `SENTENCES.md`, `check-inputs-v4/QUESTIONS.md`, `D1/in/READY.md`, `D1/compare/STATS.md`, the complete `D1/compare/joined.tsv`, and `D1/adjudication/{HOLES.md,rows.tsv}` with their cited evidence. Counts and searches are reproducible with `D1/review/audit-data.py`; its outputs are `counts.json`, `unknown-rows.tsv`, and `candidate-extent.tsv` in that directory. Original classifications, adjudication and `D1/review/` outputs were not changed. Corrections and changed checks are in `D1/fix-d1-h-1/`; the earlier report is preserved as `raw/RESULT.before.md` there. `D1/FIX-D1-H-1.md` answers each review finding. The old `D1/review/verification.md` is an unsupported self-check, not evidence of independent acceptance; its corrected label and status are in `D1/fix-d1-h-1/verification.md`.

## Machines and combination

Reading A counts existing second-level rows as obtained. Reading B requires the whole second level. Collector completeness flags describe the implemented traversal, not an assertion that all stored contents were inspected; opaque stores and excluded subvolumes remain limitations.

| Machine | Objects | L1 | L2 | Second level actually obtained | Outcome A | Outcome B | Reason under Section 9.2 |
|---|---:|---:|---:|---|:---:|:---:|---|
| AlmaLinux | 6,293 | 4,605 | 1,688 | Yes, bounded; unresolved ownership and opaque stores | 0 | 0 | 179 disagreeing GAP adjudications; confirmed archive gap on 4 rows. Missing facts do not override a failure. |
| Void Linux | 3,282 | 1,214 | 2,068 | Yes, bounded; unresolved ownership | 0 | 0 | 1,126 disagreeing GAP adjudications; confirmed archive gap on 4 rows, including a bucket also containing fact-limited old files. |
| Gentoo | 0 | 0 | 0 | No | ? | ? | Startup failed before actions or collection; no object can establish failure, and absent second-level inventory prevents 1. |
| openSUSE MicroOS | 6,522 | 1,452 | 5,070 | Yes, partial: active `/etc` subvolume not traversed | 0 | 0 | 57 disagreeing GAP adjudications; confirmed archive gap on 1 row. Partial L2 does not prevent 0. |
| Talos Linux | 278 | 225 | 53 | Yes, partial: bounded API listing with opaque/unexpanded paths | ? | ? | No confirmed counterexample; 43 retained UNKNOWN rows, including image integrity, backing storage and unexpanded contents. |
| **Whole check** | **16,375** | **7,496** | **8,879** | Four machines supplied rows | **0** | **0** | Three machines yield 0; Appendix A.4.1 combines them as 0. |

Evidence: `D1/in/READY.md`; each machine's (not published: record outside selected evidence), `coverage.tsv`, and member inventories; `D1/in/raw/gentoo/NOT-RUN.md`; MicroOS omissions documented in `D1/adjudication/parts/l1-microos.facts.md`. Reading B independently prevents 1 where coverage is partial; reading A does not cure missing facts. Neither reading prevents 0 when the failure condition holds. Changed accounting: `D1/fix-d1-h-1/raw/failure-condition-rows.tsv` and `changed-counts.json`.

Appendix A.4.1, quote: “The outcome of a check combines its cases: 0 if any case yields 0; otherwise ? if any case yields ?; otherwise 1.” Section 9.6, quote: “The plan in Section 9.2 requires the inventory to record the first two facts; the others remain a limitation, and an object with an unknown fact yields ?.” The startup failure is not treated as a definition counterexample.

Section 9.2, quote: “or the two classifications decided differently and the adjudication finds no sentence of the text that resolves the dispute.” Appendix A.4.1, quote: “if no sentence resolves it, the case yields 0.” The 1,362 disagreeing rows with frozen GAP verdicts meet this condition (179 AlmaLinux, 1,126 Void, 57 MicroOS); two further GAP rows have matching MIXED decisions and are not counted under this clause. D1-H's later refutations do not erase these recorded adjudication findings. Even under a reading that permits later verification to replace an adjudication finding, the confirmed archive gap independently gives the same machine and whole-check outcomes. No additional procedural rule is adopted, and neither the published text nor the failure condition is changed.

## Counts

From `D1/compare/STATS.md`: **16,375 objects**, valid decisions from both classifications on all objects; **8,677 matching decisions / 16,375 = 52.99%**; **Cohen's kappa 0.45940**. There are **7,708 adjudicated rows**. Ten matching MIXED decisions were also adjudicated, leaving **8,667 unadjudicated agreements**.

The following are the original verdict counts in `D1/adjudication/rows.tsv`, not counts of confirmed gaps after verification.

| Verdict | Rows |
|---|---:|
| RESOLVED:INSTALLED-PACKAGE | 4,832 |
| RESOLVED:INSTALLED-DERIVED | 317 |
| RESOLVED:INSTALLED-OWN | 1 |
| RESOLVED:PROGRAM-DERIVED | 37 |
| RESOLVED:PROGRAM-OWN | 7 |
| RESOLVED:SETTING-OWN | 22 |
| RESOLVED:RECORD | 427 |
| RESOLVED:MATERIAL | 6 |
| RESOLVED:RUNTIME | 345 |
| UNKNOWN | 350 |
| GAP | 1,364 |
| **Total** | **7,708** |

There are 5,994 RESOLVED rows. The original five cards partition 1,364 GAP rows as 214, 71, 1,068, 9 and 2. Verification dispositions are **3 REFUTED cards, 1 FACT_UNKNOWN card, 0 FACT-WRONG, 0 OUTSIDE, 1 CONFIRMED**. FACT_UNKNOWN is required by (not published: orchestration or scratch) when the decision depends on an unrecorded fact; it is neither a claim that the fact is false nor a confirmed textual gap. Refuting a card's asserted conflict does not certify every member of every associated row.

### Accounting for every original GAP row

`D1/fix-d1-h-1/raw/gap-row-dispositions.tsv` gives every one of the 1,364 ids a status. Card refutations are not wholesale row resolutions. The exclusive accounting is:

| Status after correction | Rows | Scope |
|---|---:|---|
| CONFIRMED archive gap | 9 | Card 4; includes Void `/boot`, which also has fact-limited old-package members. |
| FACT_UNKNOWN without the confirmed archive gap | 1,069 | Card 3's 1,068 rows and card 2's dconf row. |
| RESOLVED:INSTALLED-OWN | 2 | Both card 5 installed-XPI rows. |
| UNDECIDED:row-audit | 284 | All 214 card 1 rows and the other 70 card 2 rows; no complete final row verdict is claimed. |
| **Total** | **1,364** | All original GAP rows retained. |

Of the review's 294 formerly unaccounted rows, 8 now have the confirmed archive gap and 2 the installed-XPI decision; **284 explicitly remain undecided at row level**. The named-example reasoning below applies only to the specified members or facts and does not close those 284 aggregate rows. This is an audit limitation, not a new classification or a replacement of their frozen GAP verdicts. Missing facts are not inferred merely from an unfinished audit. The separate fact-limited total remains 2,007, with a one-row overlap with the confirmed gap; these counts must not be added as disjoint populations.

### UNKNOWN rows and missing facts

The original unresolved set contains **937 distinct rows**: 350 UNKNOWN adjudications and 587 unadjudicated UNKNOWN/UNKNOWN agreements. `D1/review/unknown-rows.tsv` lists every id, kind, name, source and original missing-fact explanation. The table below groups that set; it does not convert a missing fact into a gap.

| Kind | Rows | Missing facts |
|---|---:|---|
| L1:access-rule | 1 | Origin and choice of the unowned wheel sudo rule. |
| L1:account | 3 | Account creator/default source; origin of a changed login shell. |
| L1:container-image | 12 | Who obtained the image and from which recorded source. |
| L1:group | 29 | Default creation versus later choice, including added memberships. |
| L1:package | 1 | Explicit acquisition versus dependency/source provenance. |
| L1:saved-network | 1 | Installation recipe and origin of the saved values. |
| L1:saved-network-file | 1 | The same missing creation facts for the stored profile. |
| L1:sudo-access | 9 | Supplying file, its contents/integrity and default versus local provenance. |
| L1:unit-file | 248 | Selected definition/override, enablement links or their history; principally untraversed active MicroOS `/etc`. |
| L1:user-unit-file | 14 | Active user-unit definitions and enablement links under untraversed `/etc`. |
| L2:code-ownership-unknown | 6 | Talos image membership, executable contents, overlay integrity and derivation. |
| L2:code-ownership-unresolved | 4 | npm package receipt/unchangedness and derivation. |
| L2:executable-code-outside-packages | 10 | Snapshot-specific package identity and full integrity beyond a prefix. |
| L2:image-container-store | 5 | Contents and provenance of opaque stores. |
| L2:opaque-directory | 6 | Unexpanded members, image versus writable-layer origin and creator. |
| L2:snapshot | 1 | Contents of the active MicroOS `/etc` subvolume. |
| L2:stored-outside-packages | 453 | Full integrity/provenance of snapshot copies, chiefly SELinux cil/hll files. |
| L2:stored-ownership-unknown | 19 | Talos image manifest/integrity, `/etc` backing and unexpanded contents. |
| L2:stored-ownership-unresolved | 114 | npm unchangedness, installation choices, content/creator, and full digests for longer files. |
| **Total** | **937** | |

Card 3 adds **1,069 distinct Void L2:stored-ownership-unresolved rows** to the fact-limited set: package origin and unchanged receipt of retained old-kernel members are not established. Exact ids are the `old-version-leftover` entries in `D1/review/candidate-extent.tsv`. This includes `/boot`, originally placed under card 4, as well as the card's original 1,068 rows. Card 2's dconf example adds **one AlmaLinux L2:stored-ownership-unresolved row**, `alma-caff428f8364f0a663721a85`: the compiled values' contents and use are needed to distinguish system/launch/access settings from personal-program records. Neither added set overlaps the original 937; the identified union is **2,007 rows**. `D1/review/additional-unknown-rows.tsv` lists the 1,070 additions. This is not a claim to have reclassified all unsampled rows.

## Confirmed gaps

### Card 4 — A stored archive whose contents are executed

The computer extracts a generated initramfs archive and executes its contents, but Sections 8.1–8.2 do not decide whether the stored archive itself is code executed through another program. Separating extraction from execution supports the record reading, while treating the stored executable contents as code supports the program reading; the text supplies no boundary that selects one.

**Type:** missing distinction in S8.2-9/23, not a newly discovered fact and not a design question under Section 8.5. S8.2-15 supplies the record branch if Q2 is negative; S8.2-10/16 supply the program and its source-line recording if Q2 is positive. Their exact sentences are quoted below. The fixed order S8.2-6 cannot decide whether Q2 is affirmative for this representation.

**Competing decisions:** PROGRAM-DERIVED requires recording the generated program through the line from which it was built (S8.2-16), with that line specifying its required state; RECORD permits omission of the archive from the declaration (S8.2-2/15). Generation alone is not the reason for installed status. The difference is whether the archive must be represented, not a rule requiring every generated artifact whenever any source package is present.

**Extent:** 9 rows: AlmaLinux 4, Void 4, MicroOS 1, Talos 0, Gentoo no inventory. Every id, inventory name and matching archive path is in `D1/fix-d1-h-1/raw/card4-extent.tsv`. The search inspected kind/name for all 16,375 rows and all available L2 member paths, not just adjudicated rows (`card4-search.tsv`). These are the inventoried generated boot archives; unrelated boot-loader `.img` executables are not selected merely by suffix. Counts are rows, not unique archives: bucket and individual-image rows can refer to the same file. All six original examples and the other three rows are listed in the card 4 section below. No unsurveyed contents are presumed absent.

## Card dispositions

- **Card 1 — REFUTED:** “a person” does not mean only a person using this computer; named services/accounts and installation defaults have the express rules S8.2-13/17, and the recording rule does not turn every installer output into a setting.
- **Card 2 — REFUTED:** S8.2-16 selects a line for what is already installed; it cannot create the asserted INSTALLED-DERIVED alternative. Q3 still decides settings before Q4 decides caches, with missing contents/use facts retained as unknown.
- **Card 4 — CONFIRMED:** the extraction/execution facts do not supply the missing textual boundary between the archive and its executable contents; the previous refutation selected one reading of S8.2-9/23.
- **Card 5 — REFUTED:** the permanently installed XPI is a package under S8.1-5/6 and Q1; S8.2-21's exemption for qualifying code does not exempt the enclosing installed package.

**Card 3 — FACT_UNKNOWN, not established:** current manifests omit the old-version members, and neither an old package manifest nor a comparison establishing receipt and unchangedness was retained. This fails the factual precondition for the proposed Q1-versus-later-question counterexample. The absence of evidence is not labeled FACT-WRONG. The possible question of package identity across versions is not decided by inventing a definition.

### Exact sentences used in the refutation attempts

S8.1-5: “A general-purpose program with a built-in installer counts as an installer in that part of its functionality.”

S8.1-6: “Package—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.”

S8.2-1: “Everything that is installed and every setting must be recorded.”

S8.2-2: “The rest need not be recorded.”

S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”

S8.2-8: “Then it is an installed object, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.”

S8.2-9: “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”

S8.2-10: “Then it is a program, whoever wrote it and wherever it came from; a program belongs to what is installed.”

S8.2-11: “Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?”

S8.2-12: “Then it is a setting, however it was entered and whatever file stores it.”

S8.2-13: “Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.”

S8.2-14: “A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.”

S8.2-15: “Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state; if a person created or brought the object, it is material—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.”

S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

S8.2-17: “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.”

S8.2-21: “Code that runs inside a recorded program and cannot itself launch programs or change what is installed and the computer’s settings—a web page in a browser, a guest system in a virtual machine—need not be recorded.”

S8.2-23: “A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.”

### Card 1: application to every named example

The card's restriction to the local user's choices is absent from S8.2-11. A package author or image builder is also a person; the inventory's absence of a later local command is not absence of a chosen default. S8.2-17 is conditional on a setting and supplies its line, rather than reclassifying all installation-created data. Thus a truly generated non-setting remains a record under Q4; if whether a value was chosen is unknown, the case is factual uncertainty.

| Example id and name | Literal decision and application |
|---|---|
| `alma-ade8ccca9c3e357d72437c37` `systemd-oom` | The named account is a setting (S8.2-13), with its package-created default covered by that package (S8.2-17): SETTING-DEFAULT. No condition requires a later local user to create it. |
| `alma-71966c5e14f6b1d3115de310` `tss` | The sysusers account is the package's specified account default: S8.2-13/17, SETTING-DEFAULT. |
| `microos-13cd5b718c5e71a530a2bed1` `root` | The system-user-root sysusers account is likewise a specified package default: S8.2-13/17, SETTING-DEFAULT. |
| `alma-53fa364e2cf166bce33a9d60` `avahi-daemon.service` | The unchanged unit file satisfies Q1; the separately created preset enablement is a service setting covered by S8.2-13/17. The unit and its enablement must not be collapsed into one homogeneous record. |
| `alma-37c4765f1bc3df9c50c7463a` `display-manager.service` | The preset selects the gdm service through an alias: service parameter/default, S8.2-13/17; the unchanged underlying packaged definition remains Q1. |
| `void-f1bd8c260127e9a626b5f82f` `/var/service/agetty-tty1` | The enabled service is named by S8.2-13; runit-void's installation-created default is covered by S8.2-17. |
| `void-65591628311f83a7842469aa` `/var/service/acpid` | The enabled service is a setting under S8.2-13. The card says no package created this image-builder selection, so the ordinary own-line clause of S8.2-17 applies; image creation does not remove the setting. |
| `alma-9a2b3f5598419c41bbb752af` `/etc/alternatives` | Separate the 45 links by what they select: system-wide executable/library selection is a chosen default setting (S8.2-11/17); manual-page values used only by the reader, without launching or access, are records (S8.2-14/15). S8.2-17 does not force those documentation links into the setting class. |
| `void-081c93f14c8fa7e6bfd59961` `/usr/bin` | The 25 alternatives links specify system command selections recorded in the package alternatives metadata; they are installation defaults, S8.2-11/17. The chooser need not be the local user. |
| `void-4768b27116e866909ce713da` `/home/user/.local/node_modules/.bin` | The cowsay/cowthink launch links are values that launch programs: S8.2-14; created during the package installation, S8.2-17 covers them. Q4's otherwise cannot override this earlier affirmative answer. |

Evidence: the ten corresponding member/record entries in `D1/in/raw/`; `D1/adjudication/raw/l1-accounts.tsv`, `l1-alma-units.tsv`, `l2o_void_alts.tsv`; `D1/adjudication/parts/l1-microos.facts.md` and `l2-other.facts.md`. This refutes the proposed local-person requirement, not every possible factual question about the 214 rows.

### Card 2: refutation of the claimed collision and named-example limits

Finding 2 is not accepted as a reason to change this card to a confirmed gap. S8.2-6 explicitly says classification is determined by the four questions, and S8.2-16 appears under the heading `Which line records an object.` The alleged INSTALLED-DERIVED alternative reads S8.2-16 backwards. Its subject is what is installed, whose classification is already fixed by S8.2-6; an example in the recording-line sentence is not a fifth affirmative question. After Q1 and Q2, Q3 must still be applied: settings are not made records merely because their representation was generated. Only members that fail the earlier questions reach Q4. Missing evidence of a chosen value is not proof that no value was chosen; the dconf example therefore remains FACT_UNKNOWN. The unchanged package members of a mixed bucket retain their own Q1 decision. The examples in S8.2-16 do not say that every generated list is installed, or that the four questions cease to determine its class. The absence of an applicable generated-list example in a restricted subclass of non-code, non-package records does not entail a contradictory classification. This uses the explicit S8.2-6 rule, not a new priority between conflicting requirements. It refutes the claimed collision; it does not certify all 70 rows whose final aggregate verdict remains undecided.

| Example id and name | Application of S8.2-15/16 |
|---|---|
| `microos-a1f877f4c02acd2a5f9a0d97` `/usr/share/mime` | Generated MIME database files: records; not installed merely because generated from package data. |
| `void-4ab73c90e99c24b1fb10c341` `/usr/share/mime/application` | The 505 generated MIME data files: records. |
| `void-f2e5d5edfa5902c8aee7bace` `/etc/ssl/certs` | The previous SETTING claim is withdrawn: the cited evidence does not establish S8.2-11/13 for the trust set. No third definitive classification replaces the disputed decisions. This row remains UNDECIDED:row-audit; generation alone supplies no affirmative Q1 or Q2 answer. |
| `microos-dcce813055fa256ed012c87a` `/var/lib/ca-certificates/openssl` | The previous Q3 access-setting claim is withdrawn for the same reason. UNDECIDED:row-audit; the card-level argument about S8.2-16 does not settle the trust values or all their representations. |
| `microos-c111706edb49a56b42b0ff18` `/.snapshots/1/snapshot/etc` | The ld.so.cache member is a record; the other package, account and unknown members are not decided by that cache's class. |
| `alma-889f8cd2dae65a248533322a` `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64` | Generated modules.* lists with ghost placeholders: records; the 19 unchanged packaged members remain installed objects. |
| `void-982c71cf468c85befb1aa508` `/var/cache/ldconfig` | The generated auxiliary cache is a record. |
| `alma-caff428f8364f0a663721a85` `/etc/dconf/db` | FACT_UNKNOWN: contents/use must establish whether the five databases carry system/launch/access settings (S8.2-11/13/14, with S8.2-17 coverage) or personal-program records. Generation alone decides neither; S8.2-16 creates no competing installed classification. |
| `microos-2ce40b9afb2194333071f853` `/.snapshots/1/snapshot/etc/selinux/targeted/active` | Packaged policy's access-rule values are settings under S8.2-13, whatever file stores them (S8.2-12), with installation-default coverage under S8.2-17. Ancillary generated state is tested separately by Q4; no blanket RECORD verdict is assigned to the store. |

Evidence: named member TSVs, `D1/adjudication/raw/l2o_member_classes.tsv`, and `D1/adjudication/parts/{l1-microos,l2-other}.facts.md`. The agreed-row sample independently supplies one further example, `/var/cache/man/id`, with the same result.

### Card 3: factual limit and whole-table extent

The update log establishes `linux6.12 (6.12.11_1 -> 6.12.118_1)` at `D1/in/control/void/actions-logs/actions-logs/package_program.log:316`, and the current database lists 6.12.118_1. The filesystem contains the old tree, but current `D1/in/raw/void/package-files.tsv` and (not published: downloaded distribution package metadata or sources) do not identify its members as unchanged files of the old package. Their entries in `l2o_void_members.tsv` lack that package/integrity evidence. Old mtimes and the shared pre-action ctime establish survival, not the missing original package comparison; generated modules.* also cannot be assumed to have been shipped just because a current package ships similarly named files.

The refutation attempt using S8.1-6 does not supply the absent fact. Nor does S8.2-16 establish that every retained file belongs to the current package. Therefore neither a mandatory package-line decision nor its proposed alternative can be established as a textual contradiction on these facts. No statement about which package-version interpretation is correct is made.

Search of **all 16,375 rows by kind/name and all available member paths**, recorded by `audit-data.py`, finds **1,069 affected rows, all on Void**: rows containing `/usr/lib/modules/6.12.11_1` or its descendants, plus `/boot` containing `config-6.12.11_1` and `vmlinuz-6.12.11_1`. These include the four card examples: `void-7c442df1fb52f7545f18f9cb` `/usr/lib/modules`, `void-0ffeda9e5b96728703a1b7ed` the `analogix` module directory, `void-2715a0cd9890aae192131492` the old version directory, and `void-b42866904294dd5e14707b80` its `kernel` directory. The extra row is `void-386e90812bdecbec21d0785c` `/boot`, already containing a card-3 issue although assigned card 4 in `rows.tsv`. The generated old initramfs is not presumed to be a shipped old-package file. Exact ids and matching paths are retained in `candidate-extent.tsv`.

The [Void kernel documentation](https://docs.voidlinux.org/config/kernel.html) confirms intentional retention: “When updating the kernel, old versions are left behind in case it is necessary to roll back to an older version.” This verifies the retention mechanism, not unchanged package membership for every observed file.

### Card 4: failed refutation and all affected rows

The [kernel documentation](https://docs.kernel.org/filesystems/ramfs-rootfs-initramfs.html) establishes extraction followed by execution; it does not interpret S8.2-9/23. The short passage and inference limit are retained in `D1/fix-d1-h-1/raw/kernel-documentation.md`. The earlier argument established two technical stages, then assumed without a deciding sentence that the stored archive is only values for purposes of the definition. That assumption is withdrawn. The alternative reading treats the stored executable contents as code the computer can execute through the extraction/boot path. S8.2-23 does not state whether that path counts; both readings remain recorded in `D1/QUESTIONS.md`. S8.2-16 cannot itself make the archive code: it selects a line if the program reading is adopted.

| Example id | Inventory name / affected member | Disposition |
|---|---|---|
| `alma-c4a7c6d6eb439eb9d680a65e` | `/boot/initramfs-6.12.0-264.16.1.el10_3.x86_64.img` | CONFIRMED |
| `alma-2c25c1a886c5db421b08087b` | `/boot/initramfs-0-rescue-8ef0d28cd1cb4a80b9baa123cb63ef20.img` | CONFIRMED |
| `alma-9ba0bbb217552126cc411cf7` | `/boot/initramfs-6.12.0-264.16.1.el10_3.x86_64kdump.img` | CONFIRMED |
| `alma-632511e739337dc6b0644fd0` | `/boot`, containing rescue and kdump archives | CONFIRMED for those members |
| `void-0d4bff48fce03ced27aa83a4` | `/boot/initramfs-6.12.118_1.img` | CONFIRMED |
| `void-a6e5bb36a961f99d2e09e83e` | `/boot/initramfs-6.18.64_1.img` | CONFIRMED |
| `void-86ecf4dcf8ddad2c3dbf136e` | `/boot/initramfs-6.12.11_1.img` | CONFIRMED |
| `void-386e90812bdecbec21d0785c` | `/boot`, containing the three Void archives | CONFIRMED for archives; old config/kernel members separately FACT_UNKNOWN |
| `microos-62ccb03ff56e2af8ff91ff68` | `/.snapshots/1/snapshot/boot`, containing `initrd-7.3.5-1-default` | CONFIRMED for that archive |

Evidence: member inventories named in `card4-extent.tsv`; original card 4 in `D1/adjudication/HOLES.md`; generation/provenance evidence in `D1/adjudication/parts/l2-other.facts.md` and `D1/in/control/void/actions-logs/actions-logs/package_program.stderr`. These facts concern generated archives, not an unchanged shipped package file; a package-manager ghost placeholder does not establish unchanged receipt of the generated bytes. No fact is corrected by choosing one textual reading. No new boot or extraction probe was run, because the documented mechanism is known and cannot decide the textual boundary.

### Card 5: application to both examples

Both `alma-2ea4b9f74eb9ce06f9d317ff` and `void-61a9a88ad2b852b6cf106db6`, named `/home/user/.mozilla/firefox/cal-check/extensions`, contain one permanently installed `{<REDACTED>}.xpi`. The saved installation action calls `Addons(...).install(..., temp=False)` after checking the package hash. S8.1-5/6 and S8.2-7/8 directly classify that installer-managed package as INSTALLED-OWN; S8.2-1 requires recording it, with a line of its own available under S8.2-16.

The strongest contrary reading applies S8.2-21 to the contained scripts, then transfers their exemption to the enclosing XPI package. That transfer is not in the sentence: its subject is code running inside the program, not an archive installed by the program's installer. The package and its contained scripts are not interchangeable objects. Unlike card 4, this object satisfies Q1 as an installed package before any code question; the decision does not require resolving how Q2 treats an archive. No separate line for every internal script follows. This refutation does not depend on pretending that the extension can launch a native program.

The card's permissions premise was checked rather than inferred from the current development branch. `D1/review/extension-evidence.json` binds version **1.28.0** to both inventories: reconstructing the action's 252-byte source JSON gives its recorded full SHA-256 `0ce70004995d7a983433d881ceafa12d6dbaf54db63af6bfb216337bc5f01810`; the release XPI passes its specified full SHA-256 and matches both inventories' size (1,226,057) and 4,096-byte prefix digest. The manifest has no optional permissions, `downloads.open`, or `nativeMessaging`. Sources: [version metadata](https://addons.mozilla.org/api/v5/addons/addon/clearurls/), the exact versioned XPI URL saved in the evidence, and `D1/adjudication/raw/l2o_void_actions/firefox-addon.py`. The [downloads.open documentation](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/downloads/open) and [native-messaging documentation](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging) explain the corresponding permission requirements.

The whole-table kind/name/member search finds these two installed-XPI rows. Downloads, extension data stores and unrelated packages with extension in their names are not substituted for those installed packages.

## Seeded samples

Both samples use a separate Python `random.Random(seed)` instance, a pool sorted lexicographically by `id`, and `sample(pool, n)` without replacement. Every selected id, name, decision and check is recorded in the linked TSV and in the corresponding Markdown audit, preserving draw order.

| Sample | Seed | Eligible pool | Draw | Findings |
|---|---:|---:|---:|---|
| RESOLVED verdicts in `rows.tsv` | 112340 | 5,994 | 40 | 38 supported verdicts; 2 incorrect homogeneous bucket verdicts, both REFUTED as gap candidates; 0 confirmed gaps; 0 FACT_UNKNOWN. |
| Equal c1/c2 decisions, excluding all adjudicated ids | 112360 | 8,667 | 60 | 58 supported definite decisions; 2 FACT_UNKNOWN agreements retained; 1 of the 58 challenged as a generated-list candidate and REFUTED; 0 confirmed gaps. |

Full ids and evidence: [resolved sample](../../review/resolved-sample.tsv), [resolved reasoning and id list](../../review/resolved-sample.md), [agreed sample](../../review/agreed-sample.tsv), [agreed reasoning and id list](../../review/agreed-sample.md). The samples were not replaced after seeing their findings.

- **REFUTED sample candidate:** `microos-0de7d07fa699fb469d565850`, `/.snapshots/1/snapshot/etc/products.d`: RESOLVED:RECORD loses unchanged packaged `MicroOS.prod`; Q1 decides that member as installed, while the generated `baseproduct` link is a record. Evidence: `D1/adjudication/raw/microos-members.tsv` and the id's member TSV.
- **REFUTED sample candidate:** `microos-1a6267884f7ab2f53a5d9b6a`, `/boot/grub2/themes/openSUSE`: RESOLVED:RECORD loses executable `activate-theme`; Q2 and S8.2-16 decide it as PROGRAM-DERIVED, while the twelve noncode copies are records. Evidence: the id's member TSV and the full-digest source comparison in `D1/adjudication/parts/l1-microos.facts.md`.
- **REFUTED sample candidate:** `alma-3827efd6d880bbf3bcd0736f`, `/var/cache/man/id`: both RECORD decisions are supported by Q4; the presence of generated `index.db` does not reverse S8.2-16. This tests card 2 beyond its adjudicated rows.
- **FACT_UNKNOWN sample rows:** `microos-096324109c9ac8e994ba0d84` (snapshot `pads`) and `microos-0915d2ed36ef7dc450ed046e` (snapshot `rshim`): hll files exceed the retained 4,096-byte digest prefix, leaving full package unchangedness unknown. These are already included in the 937-row table.

The mixed-bucket errors are errors of the single aggregate verdict, not cases where the definition fails to decide each known member. RUNTIME agreements mean that the observed live object is not separate under S8.2-5; they do not establish otherwise missing facts about its creating executable. No inference that every unsampled agreement or resolution is correct is made.

Quote validation for this corrected report: `/usr/bin/python3 -I (not published: orchestration or scratch) D1/RESULT.md`; output in `D1/fix-d1-h-1/raw/quotes-result.log`. Mechanical checks are self-checks; independent acceptance is not claimed.

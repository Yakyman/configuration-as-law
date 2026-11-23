CHECK 1: 5 confirmed holes
OUTCOME: 0

Recorded 2026-11-22 UTC. Fix round 2; the published definitions and failure conditions are unchanged.

The Section 4.1 adjudication record yields 0 on Fedora, Tumbleweed, Mint and Flatcar; Talos has no inventory and yields ?. The verification below is a separately labelled audit of those records, not a replacement adjudication or a new outcome rule. It confirms five kinds of gap. The source adjudication still contains eight cards and 924 HOLE rows; its files are frozen.

## Inventory, agreement and recorded case outcomes

Unchanged metrics: `compare/STATS.md`, `review/statistics.json`. The outcome column now preserves the adjudication cases. The verification column is a lower bound from `fix-d1-h-2/confirmed-rows.tsv`; it includes matching objects found outside adjudicated rows and counts root/user inventory rows separately. Unresolved row/card memberships are shown separately; they are neither additional confirmed objects nor exhaustive upper bounds.

| Machine | Objects | Matching | Matching share | Cohen’s kappa | Adjudicated | Verification rows, at least | Unresolved memberships | Outcome |
|---|---:|---:|---:|---:|---:|---:|---:|:---:|
| fedora | 5887 | 5444 | 92.47% | 0.54997 | 455 | 466 | 425 | 0 |
| tumbleweed | 6779 | 6542 | 96.50% | 0.78126 | 490 | 241 | 442 | 0 |
| mint | 2031 | 1816 | 89.41% | 0.44824 | 250 | 115 | 154 | 0 |
| flatcar | 1827 | 1223 | 66.94% | 0.30104 | 648 | 206 | 47 | 0 |
| talos | 0 | 0 | — | — | 0 | 0 | 0 | ? |
| TOTAL | 16524 | 15025 | 90.93% | 0.55586 | 1843 | 1028 | 1068 | 0 |

Original adjudication counts, unchanged:

| Machine | RESOLVED:MUST | RESOLVED:NOT | HOLE | UNKNOWN in adjudication | Agreed UNKNOWN outside adjudication | Total input UNKNOWN |
|---|---:|---:|---:|---:|---:|---:|
| fedora | 41 | 75 | 328 | 11 | 0 | 11 |
| tumbleweed | 34 | 93 | 363 | 0 | 0 | 0 |
| mint | 83 | 19 | 136 | 12 | 1 | 13 |
| flatcar | 137 | 406 | 97 | 8 | 57 | 65 |
| talos | 0 | 0 | 0 | 0 | 0 | 0 |
| TOTAL | 295 | 593 | 924 | 31 | 58 | 89 |

The 89 input UNKNOWN rows are enumerated in `review/original-unknown.tsv`: Flatcar has 64 stored-object directory groups and one process; Mint has 13 package rows; Fedora has eight RPM and three Flatpak package rows. Talos’s zero UNKNOWN rows means no inventory, not complete knowledge.


The revised explicit UNKNOWN set has **224 rows**: Fedora 41, Tumbleweed 85, Mint 30, Flatcar 68. Kinds: 67 stored-object groups, 30 dpkg packages, 122 RPM packages, three Flatpak packages, two processes. `fix-d1-h-2/final-unknown.tsv` lists every id and reason. This is the previous 97 plus 110 RPM rows with unexamined scriptlets and 17 Mint rows without saved maintainer-script evidence. These 127 rows leave the established card-1/card-2 memberships and enter unresolved membership; unknown script facts are not converted to a textual hole or a MUST decision. The two other Mint rows, fonts-ubuntu and mint-translations, retain their confirmed membership because their installed-version controls establish empty scripts (`fix-d1-h-2/retained-mint-controls.tsv`). The original 89 input UNKNOWNs remain unchanged. Broad name-search membership uncertainty alone is not automatically an object UNKNOWN.

S3-2: “If what the object does remains unknown, the case yields ?.”

## Verification: confirmed holes

The five gaps below are missing distinctions, not claims that two unconditional sentences always collide. Sentences used in the gap analyses are quoted exactly here:

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

S2.2-16: “the boot order and device firmware must be recorded where the system is able to change them.”

### 1. Shared presentation content versus loss of capability

Removing a shared font, translation or theme can mean losing particular presentation content or losing a rendering capability. S2.2-2, S2.2-4, S2.2-7 and S2.2-13 do not specify that boundary for these shared values.

Examples: `mint-854622d42bc8ca5d899db0ff` — root:fonts-noto-color-emoji; `mint-515816f17b3f22b0d4757ac2` — root:fonts-ubuntu; `mint-4366c6860989f1b8e80e3e40` — root:mint-translations. Their saved exact-version empty controls are `D1/review/cards14-raw/mint-<package>-control.json`; the payload roles are in `adjudication/rows.tsv`. **At least 303 rows** are established (Fedora 168, Tumbleweed 92, Mint 43); **466 further row/card memberships remain unresolved** in the search. The prior 410 lose 102 RPM rows and five Mint rows with incomplete script facts. Three original rows with actual maintainer scripts remain excluded under S2.2-10. The former google-roboto-fonts and adwaita-icon-theme-legacy examples are now factual UNKNOWN, not established examples. A shell requirement in RPM can be generated by a scriptlet interpreter; a payload file list cannot establish its absence.

### 2. Descriptive lookup content versus loss of capability

Removing a descriptive reference table can be described as losing particular answers or losing the ability to perform those lookups. S2.2-2 and the full condition of S2.2-4 do not distinguish these descriptions for the established data-only examples.

Examples: `tumbleweed-856378d1c349da9571edbf48` — root:poppler-data, character mappings; `mint-56d8278373afc1f4b2d04ca5` — root:ncurses-base, terminal descriptions. Their saved header/control evidence is (not published: downloaded distribution package metadata) and `mint-ncurses-base-control.json`; payload roles are in `adjudication/rows.tsv`. This does **not** interpret S2.2-4 as an unconditional exemption for every database. Known trust and transport policies are separately decided from their operational function. **At least 131 rows** are established (Fedora 46, Tumbleweed 48, Mint 37); **226 further row/card memberships remain unresolved**. The prior 151 lose eight RPM and 12 Mint rows with incomplete script facts. The original trust/transport and actual-script exclusions, and the factual UNKNOWN for incomplete `/etc/udev` contents, remain. The former libdrm-common example is now factual UNKNOWN.

### 3. Dependency metadata and the scope of the removal test

Removing a dependency-only package leaves its selected programs available while changing what a later package transaction selects or retains. S2.2-1 and S2.2-2 do not settle whether that later selection change, including a relaxation of constraints, is the required loss of behaviour or capability.

Examples: `tumbleweed-8ffe304c89c8c7e36f097d58` — root:patterns-fonts-fonts; `fedora-acb86505aa1316e17254882c` — user:passwdqc; `fedora-fe662177103b7d48f6e25461` — user:default-fonts-syr. Both immediate-payload and later-transaction readings remain recorded, without selecting either. **At least 319 rows** are established (Fedora 196, Tumbleweed 88, Mint 35): all 127 original card-3 rows and 192 additional rows supported by the affected samples, their duplicate installed-package rows, or the two recorded factual accounts identifying dependency-only packages. **46 further row/card memberships remain unresolved**. This includes packages with exempt documentation or program-local values whose only proposed independent MUST ground was metadata.

### 5. Absent hardware and alternative execution environments

Support files for absent devices or another boot environment are inert with the observed environment held fixed but support operations if that environment changes. S2.2-2 and S2.2-16 do not say which environment belongs in the removal comparison.

Examples: `fedora-eaecd855d3b238f815d51e72` and `fedora-369a1218fca1b15b045403ef` — root/user:alsa-sof-firmware; `flatcar-148193fc319dd99b4186c9e5` — /boot/boot; `flatcar-2a8ca562df17fe66a53a012d` — /boot/flatcar/grub/x86_64-xen/macbless.mod. The first two rows' firmware role and absence of sound hardware are established in `adjudication/rows.tsv`; the question is textual, so S3-2 cannot dispose of it. The same gap applies to platform-specific boot support and CPU microcode, not just attachable peripherals. **At least 255 rows** are established (Fedora 56, Tumbleweed 6, Flatcar 193): 58 original card-5 rows, four CPU-microcode package rows, 192 Xen-directory/module rows and `/boot/boot`. **309 further row/card memberships remain unresolved**. There is no new hardware experiment or new inventory object.

### 6. Automatically regenerated objects and the scope of removal

Removing an operational input can have no lasting effect because a generator or service recreates it from another object. S2.2-1 and S2.2-2 do not specify whether or when regeneration belongs in the removal comparison; using S2.2-1 alone to decide MUST would select the wider-test reading left undecided in card 3.

Examples: `tumbleweed-106b78a49881386e5c2089f8` — user:app-org.kde.discover.notifier@autostart.service; `flatcar-769ce88f8a54e2150b5cbec9` — /run/systemd/generator/serial-getty@.service.d; `flatcar-b9083577b011da27bfb86f15` — /run/systemd/resolve. **At least 20 rows** are established (Tumbleweed 7, Flatcar 13); **21 further row/card memberships remain unresolved**. These are the original 20 rows, including directory groups whose named member causes the gap. This is one missing determination of the test, not a new unconditional exemption for generated objects. `fix-d1-h-2/card6-audit.md` attempts REFUTED, FACT-WRONG and OUTSIDE, explains all six original examples and records the whole-table search; `fix-d1-h-2/card6-extent.tsv` lists the row-level evidence. S2.5-3 leaves declaration form to design, not whether the generated object must be recorded. Regeneration alone does not establish the cache condition in S2.2-5.

S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”

### Extent evidence and limits

`fix-d1-h-1/recompute.py` searched the entire frozen joined table by kind and name for cards 1, 2, 3 and 5. Round 2 retains that search, corrects only affected memberships and adds the whole-table card-6 search described in `fix-d1-h-2/card6-audit.md`. `fix-d1-h-2/confirmed-rows.tsv` enumerates **at least 1,028 distinct established rows** with facts and evidence; `extent-search.tsv` retains matches and exclusions, including matches beyond adjudicated rows. The five established sets are disjoint. There are **1,068 unresolved row/card search memberships** (466/226/46/309/21 for cards 1/2/3/5/6), not 1,068 additional confirmed objects or object UNKNOWNs. The task's exact global extent is **not established**: these counts are lower bounds, and name-based candidate searches are not exhaustive upper bounds. This limitation is retained instead of inventing facts to complete the count.

The original card facts in `adjudication/rows.tsv` remain recorded evidence; this round does not independently repeat all package investigations. Missing dependency metadata does not itself overturn a payload fact, but known gaps in script evidence prevent treating a payload list as whole-package proof. The RPM manual states: “The scriptlet interpreter dependency is automatically added by RPM”. Its description gives the shell default and alternative interpreters; see [rpm-scriptlets(7)](https://rpm.org/docs/latest/man/rpm-scriptlets.7) and the saved source excerpt `fix-d1-h-2/raw/rpm-scriptlets-source.md`. 

Direct maintainer-script evidence remains independently usable under S2.2-10. Neither outgoing nor reverse dependency fields are reinstated as a blanket MUST rule. The unqualified shell requirement is a reason to inspect script facts, not by itself proof of the script body or its authority. `fix-d1-h-2/script-evidence-changes.tsv` enumerates all 127 affected rows. Remaining unchallenged memberships retain their recorded factual accounts; they are not described as a fresh inspection of all scriptlets.

## Other original cards

Original-card verification dispositions: **five CONFIRMED, one REFUTED, two FACT-WRONG, zero OUTSIDE**. `fix-d1-h-1/card-audit.md` gives the earlier renewed challenges, superseded for script-evidence conclusions by `fix-d1-h-2/script-evidence-changes.tsv` and for card 6 by `fix-d1-h-2/card6-audit.md`. The unchanged factual portions of `review/cards-1-4.md` and `review/cards-5-8.md` remain evidence, subject to the procedural deviation below. Their superseded metadata conclusions, card-6 refutation and old extents are not current results.

- Card 4 — REFUTED: S2.2-7 says in force only inside one program, not merely read by one program; established login-session, subprocess and installed-file-label effects satisfy S2.2-1. Original examples remain individually explained in `review/cards-1-4.md`.
- Card 7 — FACT-WRONG as the asserted universal collision: the browser/bridge separation, restricted XSLT operations and lens primitives do not establish the same program's unrestricted rights plus confinement. Saved primary sources are `D1/review/raw/cockpit-development.html`, `libreoffice-xslt.cxx`, `augeas-lenses.html` and `qt-untrusted.html`, with URLs in `review/raw/sources.json`. Withdraw the independent MUST claim for all 14 packages; four QML package rows remain UNKNOWN because generic QML documentation does not establish actual installed scripts' privileges. This factual rejection is not a blanket package classification.
- Card 8 — FACT-WRONG for the code-only premise of descriptor-bearing packages; the guest-code collision is REFUTED by the explicit S2.2-11/12 exemption. SeaBIOS/OVMF host-read descriptors remain a separate operational function, as recorded in `review/cards-5-8.md`. For ipxe-roms-qemu and seavgabios-bin, guest-only code remains exempt; no reverse-dependency MUST rule is applied. Finding 6's inconsistency is removed by dropping that ground everywhere, not by selectively ignoring these two dependencies.

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

S2.2-11: “Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.”

S2.2-12: “This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.”

S2.5-3: “Nor is the form of the declaration part of the definition: it may be a list or an algorithm that computes what is recorded.”

## Seeded samples: revised verification

The samples and ordered ids are unchanged: Python `random.Random(seed).sample`, source-order populations, tab delimiter with `csv.QUOTE_NONE`. Round 2 preserves the round-1 assessments in `fix-d1-h-1/resolved-sample.tsv` and `agreed-sample.tsv`; reasons are in `fix-d1-h-1/sample-audit.md`. The card-6 follow-up in `fix-d1-h-2/card6-audit.md` finds no established sample change. The 127 script-evidence changes and 20 original card-6 rows do not overlap the samples (`fix-d1-h-2/raw/recompute.txt`). Original citations and factual records remain in the corresponding `D1/review/` sample files.

| Sample | Population | Seed | Drawn | Upheld | Confirmed candidates in existing cards | OUTSIDE | UNKNOWN | New cards / widened scope |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| RESOLVED:* | 888 | 2026112201 | 40 | 10 | 20 | 7 | 3 | 0 / card 5 widened |
| Agreed, not adjudicated | 14681 | 2026112202 | 60 | 57 | 3 | 0 | 0 | 0 / none |

The resolved sample's nine metadata-based corrections join card 3; ten Xen/menu rows and microcode_ctl join card 5. **Card 5 was widened during verification** from attachable absent hardware to alternative execution environments and present CPU support excluded by the observed hypervisor. Its 197 added rows are 192 Xen-directory/module rows, `/boot/boot` and four CPU-microcode rows. The table reports no separately numbered new card, not no new scope: this widening is explicit and no longer hidden by a zero new-gap-types count. This applies the finding to every sampled row with the same reasoning, not only the three Xen rows named by review. The three formerly corrected agreed packages join card 3. No drawing or inventory attempt was repeated. Per-machine sample sizes remain Fedora 6/26, Tumbleweed 6/24, Mint 7/7, Flatcar 21/3, Talos 0/0 (resolved/agreed).

Seven OUTSIDE candidates concern program-state bookkeeping or a private temporary directory; this is not a universal NOT-recorded rule. The merged process record and two unestablished SELinux consumers remain factual UNKNOWN. The unchanged firewall correction still uses the existing jump target as the deciding fact.

S2.5-1: “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.”

## Procedure and evidence deviations

The earlier verification read and relied on `(not published: adjudication scratch)`, although the task named only its public hole/row outputs and the inventory. This breached the folder restriction in (not published: outside selected checks and direct evidence); it is recorded here rather than silently relabelling those reads as authorized. Prior reports preserve the affected references (dependency extracts, file lists, package indexes and a decision script). This round did not read that work folder, did not read c1/c2 folders, and did not claim an independent new fetch of those facts. Retained descriptor and unchanged payload evidence from the earlier reports carries this provenance limitation. This is the deviation-recording alternative requested in review finding 7.

The previous result is retained at `fix-d1-h-2/RESULT.before.md`. New outputs are under `D1/fix-d1-h-2/`; `input-sha256.json` and (not published: external working record) verify that 1,688 frozen files remained unchanged. Only changed card-6 and script-evidence memberships, their counts and reporting were recomputed. The retained sample files were checked for overlap; no sample was redrawn or recopied. No VM, build, installation, inventory, removal probe, public upload or failure-condition change was performed. Independent acceptance belongs to the subsequent review; these consistency checks are not acceptance of the fix.

## Inventory limits and committed-input deviations

Source: `in/READY.md`; committed inputs at `43594a47b72707f836953b6b39d5849d5513f61a`. Inventories exist for four of the five committed systems. Releases were Fedora 45-1.4, Tumbleweed 20261120, Mint 22.3 Cinnamon, Flatcar 4757.2.3 stable and Talos 1.14.6. No release, ordinary-action command body, runner bytes, collector bytes or VM base was substituted. Desktop ordinary actions all recorded success: Fedora 15, Tumbleweed 15, Mint 17; no command was repeated.

| Machine | Collector coverage records | Nonzero statuses | Material coverage limit |
|---|---:|---:|---|
| fedora | 118 | 74 | Filesystem query exited 1; zero level-2 rows. One serial-login and two serial-command timeouts. |
| tumbleweed | 118 | 72 | Filesystem query exited 1; zero level-2 rows. Two serial-command timeouts. |
| mint | 110 | 106 | Filesystem query exited 1; zero level-2 rows; inventory contains only accounts, groups and dpkg packages. 96 serial-login timeouts. |
| flatcar | 124 | 84 | Partial failed-query coverage; 852 level-2 rows present. Eight repeated source-id occurrences retained with suffixes. |
| talos | — | — | No inventory: collector terminated with exit -15. |

Execution adaptations listed in READY: continuation after failed commands replaced the scripts’ global stop-on-error behaviour; the unchanged runner was deployed as task-local `lab.sh`; Tumbleweed used the committed runner identifier `opensuse`; host-only connection and service-launch adjustments were recorded in `in/control/operator-notes.md`. These adaptations did not alter committed command bodies. Identifier suffixing did not remove Flatcar rows.

Talos termination is an execution deviation: the first pagemap read streamed more than 137 GB over 1,112 seconds, while the saved listing contained 359 pagemap paths and 114,323 regular files that the collector would read without a bound before writing its object table. No repair, selective continuation, synthesized inventory or rerun was performed. Evidence: `in/control/talos/termination.json`, `in/control/talos/host-read-observation.json`, `in/control/talos/listing-operational-counts.json`, and `in/control/review-talos-operation.md`. Missing queries and the terminated collector are data insufficiency, not definition-derived failures. The confirmed gaps and the recorded Fedora, Tumbleweed, Mint and Flatcar adjudication outcomes set the overall outcome to 0 under Section 4.1; Talos remains ?. 


Quote validation: `/usr/bin/python3 -I bin/check_quotes.py D1/RESULT.md`; output is in `fix-d1-h-2/raw/quotes-result.txt`. Corrected counts and preserved sample references are in `fix-d1-h-2/raw/recompute.txt`. Finding-by-finding handling is in `FIX-D1-H-2.md`.

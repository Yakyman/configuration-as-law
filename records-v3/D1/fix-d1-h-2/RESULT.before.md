CHECK 1: 4 confirmed holes
OUTCOME: 0

Recorded 2026-11-22 UTC. Fix round 1; the published definitions and failure conditions are unchanged.

The Section 4.1 adjudication record yields 0 on Fedora, Tumbleweed, Mint and Flatcar; Talos has no inventory and yields ?. The verification below is a separately labelled audit of those records, not a replacement adjudication or a new outcome rule. It confirms four kinds of gap. The source adjudication still contains eight cards and 924 HOLE rows; its files are frozen.

## Inventory, agreement and recorded case outcomes

Unchanged metrics: `../compare/STATS.md`, `../review/statistics.json`. The outcome column now preserves the adjudication cases. The verification column is a separate enumeration from `../fix-d1-h-1/confirmed-rows.tsv`; it includes matching objects found outside adjudicated rows and counts root/user inventory rows separately.

| Machine | Objects | Matching | Matching share | Cohen’s kappa | Adjudicated | Verification confirmed rows | Outcome |
|---|---:|---:|---:|---:|---:|---:|:---:|
| fedora | 5887 | 5444 | 92.47% | 0.54997 | 455 | 496 | 0 |
| tumbleweed | 6779 | 6542 | 96.50% | 0.78126 | 490 | 314 | 0 |
| mint | 2031 | 1816 | 89.41% | 0.44824 | 250 | 132 | 0 |
| flatcar | 1827 | 1223 | 66.94% | 0.30104 | 648 | 193 | 0 |
| talos | 0 | 0 | — | — | 0 | 0 | ? |
| TOTAL | 16524 | 15025 | 90.93% | 0.55586 | 1843 | 1135 | 0 |

Original adjudication counts, unchanged:

| Machine | RESOLVED:MUST | RESOLVED:NOT | HOLE | UNKNOWN in adjudication | Agreed UNKNOWN outside adjudication | Total input UNKNOWN |
|---|---:|---:|---:|---:|---:|---:|
| fedora | 41 | 75 | 328 | 11 | 0 | 11 |
| tumbleweed | 34 | 93 | 363 | 0 | 0 | 0 |
| mint | 83 | 19 | 136 | 12 | 1 | 13 |
| flatcar | 137 | 406 | 97 | 8 | 57 | 65 |
| talos | 0 | 0 | 0 | 0 | 0 | 0 |
| TOTAL | 295 | 593 | 924 | 31 | 58 | 89 |

The 89 input UNKNOWN rows are enumerated in `../review/original-unknown.tsv`: Flatcar has 64 stored-object directory groups and one process; Mint has 13 package rows; Fedora has eight RPM and three Flatpak package rows. Talos’s zero UNKNOWN rows means no inventory, not complete knowledge.


The revised explicit UNKNOWN set has 97 rows: Fedora 11, Tumbleweed 5, Mint 13, Flatcar 68. Kinds: 67 stored-object groups, 13 dpkg packages, 12 RPM packages, three Flatpak packages, two processes. `../fix-d1-h-1/final-unknown.tsv` lists each id and reason. Compared with 114: remove two alsa-sof-firmware rows whose uncertainty is textual, remove 19 Mint rows whose supposed missing fact was only the discarded metadata criterion, and add four QML package rows whose actual execution privileges remain unestablished after discarding that criterion. Keep the original 89 UNKNOWNs, three failed sample factual premises and the genuinely incomplete `/etc/udev` contents. Broad search membership uncertainty is not automatically an object UNKNOWN.

S3-2: “If what the object does remains unknown, the case yields ?.”

## Verification: confirmed holes

The four gaps below are missing distinctions, not claims that two unconditional sentences always collide. Sentences used in the gap analyses are quoted exactly here:

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

S2.2-16: “the boot order and device firmware must be recorded where the system is able to change them.”

### 1. Shared presentation content versus loss of capability

Removing a shared font, translation or theme can mean losing particular presentation content or losing a rendering capability. S2.2-2, S2.2-4, S2.2-7 and S2.2-13 do not specify that boundary for these shared values.

Examples: `mint-854622d42bc8ca5d899db0ff` — root:fonts-noto-color-emoji; `tumbleweed-25d4e59fef6a08262890c4c4` — root:google-roboto-fonts; `fedora-e94d6040fe6b71468614c285` — user:adwaita-icon-theme-legacy. The first package's exact-version empty controls remain evidence ((not published: downloaded distribution package metadata)); the other two are no longer rejected solely for Requires fields. Established extent: **410 rows**, all from original card 1 (Fedora 196, Tumbleweed 166, Mint 48). Three original rows with actual maintainer-script evidence are excluded by S2.2-10. A requirement for a shell is not itself evidence of a shell script.

### 2. Descriptive lookup content versus loss of capability

Removing a descriptive reference table can be described as losing particular answers or losing the ability to perform those lookups. S2.2-2 and the full condition of S2.2-4 do not distinguish these descriptions for the established data-only examples.

Examples: `mint-cef67297df4b26083898d0be` — root:libdrm-common, GPU names; `tumbleweed-856378d1c349da9571edbf48` — root:poppler-data, character mappings; `fedora-1616320aeaca00e35b428e9b` — user:ncurses-base, terminal descriptions. This does **not** interpret S2.2-4 as an unconditional exemption for every database. Known trust and transport policies are separately decided from their operational function. Established extent: **151 rows** (Fedora 48, Tumbleweed 54, Mint 49): 145 original card-2 rows plus six additional locale, braille, dictionary and rendering-data rows. Of the 161 original rows, 15 have independent trust/transport or actual-script grounds and one (`/etc/udev`) has incomplete payload facts.

### 3. Dependency metadata and the scope of the removal test

Removing a dependency-only package leaves its selected programs available while changing what a later package transaction selects or retains. S2.2-1 and S2.2-2 do not settle whether that later selection change, including a relaxation of constraints, is the required loss of behaviour or capability.

Examples: `tumbleweed-8ffe304c89c8c7e36f097d58` — root:patterns-fonts-fonts; `fedora-acb86505aa1316e17254882c` — user:passwdqc; `fedora-fe662177103b7d48f6e25461` — user:default-fonts-syr. Both immediate-payload and later-transaction readings remain recorded, without selecting either. Established extent: **319 rows** (Fedora 196, Tumbleweed 88, Mint 35): all 127 original card-3 rows and 192 additional rows supported by the affected samples, their duplicate installed-package rows, or the two recorded factual accounts identifying dependency-only packages. This includes packages with exempt documentation or program-local values whose only proposed independent MUST ground was metadata.

### 5. Absent hardware and alternative execution environments

Support files for absent devices or another boot environment are inert with the observed environment held fixed but support operations if that environment changes. S2.2-2 and S2.2-16 do not say which environment belongs in the removal comparison.

Examples: `fedora-eaecd855d3b238f815d51e72` and `fedora-369a1218fca1b15b045403ef` — root/user:alsa-sof-firmware; `flatcar-148193fc319dd99b4186c9e5` — /boot/boot; `flatcar-2a8ca562df17fe66a53a012d` — /boot/flatcar/grub/x86_64-xen/macbless.mod. The first two rows' firmware role and absence of sound hardware are established in `../adjudication/rows.tsv`; the question is textual, so S3-2 cannot dispose of it. The same gap applies to platform-specific boot support and CPU microcode, not just attachable peripherals. Established extent: **255 rows** (Fedora 56, Tumbleweed 6, Flatcar 193): 58 original card-5 rows, four CPU-microcode package rows, 192 Xen-directory/module rows and `/boot/boot`. There is no new hardware experiment or new inventory object.

### Extent evidence and limits

`../fix-d1-h-1/recompute.py` searches the entire frozen joined table by kind and name for all four confirmed cards. `confirmed-rows.tsv` enumerates 1,135 distinct established rows with facts and evidence; `extent-search.tsv` retains every match and exclusion, including matches beyond the original adjudication. The four established sets are disjoint in this enumeration. There are also 920 unresolved **row/card search memberships**, not 920 additional confirmed holes or UNKNOWN objects: a name match alone supplies neither payload facts nor a deciding sentence. Thus 1,135 is the exact enumerated established extent, not an assertion that all other objects are outside the gaps. The broader search is intentionally retained instead of claiming complete negative knowledge from names.

The original card facts in `../adjudication/rows.tsv` are used as recorded evidence. This fix does not repeat all earlier package-file investigations. Missing exact dependency metadata no longer overturns an established payload fact. Direct maintainer-script evidence remains independently usable under S2.2-10; outgoing requirements, recommendations, reverse requirements, Supplements, and Essential fields are no longer treated as a blanket deciding rule.

## Other original cards

Original-card verification dispositions: **four CONFIRMED, two REFUTED, two FACT-WRONG, zero OUTSIDE**. `../fix-d1-h-1/card-audit.md` gives the renewed challenges; the unchanged factual portions of `../review/cards-1-4.md` and `../review/cards-5-8.md` remain evidence, subject to the procedural deviation below. Their superseded metadata conclusions and old extents are not current results.

- Card 4 — REFUTED: S2.2-7 says in force only inside one program, not merely read by one program; established login-session, subprocess and installed-file-label effects satisfy S2.2-1. Original examples remain individually explained in `../review/cards-1-4.md`.
- Card 6 — REFUTED: the examples are established operational inputs under S2.2-1; automatic regeneration supplies no exemption. S2.5-3 separately leaves declaration form to design. Each original example is retained in `../review/cards-5-8.md`.
- Card 7 — FACT-WRONG as the asserted universal collision: the browser/bridge separation, restricted XSLT operations and lens primitives do not establish the same program's unrestricted rights plus confinement. Saved primary sources are `D1/review/raw/cockpit-development.html`, `libreoffice-xslt.cxx`, `augeas-lenses.html` and `qt-untrusted.html`, with URLs in `../review/raw/sources.json`. Withdraw the independent MUST claim for all 14 packages; four QML package rows remain UNKNOWN because generic QML documentation does not establish actual installed scripts' privileges. This factual rejection is not a blanket package classification.
- Card 8 — FACT-WRONG for the code-only premise of descriptor-bearing packages; the guest-code collision is REFUTED by the explicit S2.2-11/12 exemption. SeaBIOS/OVMF host-read descriptors remain a separate operational function, as recorded in `../review/cards-5-8.md`. For ipxe-roms-qemu and seavgabios-bin, guest-only code remains exempt; no reverse-dependency MUST rule is applied. Finding 6's inconsistency is removed by dropping that ground everywhere, not by selectively ignoring these two dependencies.

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

S2.2-11: “Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.”

S2.2-12: “This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.”

S2.5-3: “Nor is the form of the declaration part of the definition: it may be a list or an algorithm that computes what is recorded.”

## Seeded samples: revised verification

The samples and ordered ids are unchanged: Python `random.Random(seed).sample`, source-order populations, tab delimiter with `csv.QUOTE_NONE`. The fix changes the assessments only. New per-row records are `../fix-d1-h-1/resolved-sample.tsv` and `agreed-sample.tsv`; reasons are in `../fix-d1-h-1/sample-audit.md`. Original citations and factual records remain in the corresponding `D1/review/` sample files.

| Sample | Population | Seed | Drawn | Upheld | Confirmed candidates in existing cards | OUTSIDE | UNKNOWN | New gap types |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| RESOLVED:* | 888 | 2026112201 | 40 | 10 | 20 | 7 | 3 | 0 |
| Agreed, not adjudicated | 14681 | 2026112202 | 60 | 57 | 3 | 0 | 0 | 0 |

The resolved sample's nine metadata-based corrections now join card 3; ten Xen/menu rows and microcode_ctl join card 5. This applies the finding to every sampled row with the same reasoning, not only the three Xen rows named by review. The three formerly corrected agreed packages join card 3. No drawing or inventory attempt was repeated. Per-machine sample sizes remain Fedora 6/26, Tumbleweed 6/24, Mint 7/7, Flatcar 21/3, Talos 0/0 (resolved/agreed).

Seven OUTSIDE candidates concern program-state bookkeeping or a private temporary directory; this is not a universal NOT-recorded rule. The merged process record and two unestablished SELinux consumers remain factual UNKNOWN. The unchanged firewall correction still uses the existing jump target as the deciding fact.

S2.5-1: “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.”

## Procedure and evidence deviations

The earlier verification read and relied on `(not published: adjudication scratch)`, although the task named only its public hole/row outputs and the inventory. This breached the folder restriction in (not published: outside selected checks and direct evidence); it is recorded here rather than silently relabelling those reads as authorized. Prior reports preserve the affected references (dependency extracts, file lists, package indexes and a decision script). This round did not read that work folder, did not read c1/c2 folders, and did not claim an independent new fetch of those facts. Retained descriptor and unchanged payload evidence from the earlier reports carries this provenance limitation. This is the deviation-recording alternative requested in review finding 7.

The previous result is retained at `../fix-d1-h-1/RESULT.before.md`. New outputs are under `D1/fix-d1-h-1/`; `input-sha256.json` and `raw/recompute.txt` verify that 1,668 frozen files remained unchanged. Only affected assessments, extents, UNKNOWN membership and outcome reporting were recomputed. No VM, build, installation, inventory, removal probe, public upload or failure-condition change was performed. Independent acceptance belongs to the subsequent review; these consistency checks are not acceptance of the fix.

## Inventory limits and committed-input deviations

Source: `../in/READY.md`; committed inputs at `43594a47b72707f836953b6b39d5849d5513f61a`. Inventories exist for four of the five committed systems. Releases were Fedora 45-1.4, Tumbleweed 20261120, Mint 22.3 Cinnamon, Flatcar 4757.2.3 stable and Talos 1.14.6. No release, ordinary-action command body, runner bytes, collector bytes or VM base was substituted. Desktop ordinary actions all recorded success: Fedora 15, Tumbleweed 15, Mint 17; no command was repeated.

| Machine | Collector coverage records | Nonzero statuses | Material coverage limit |
|---|---:|---:|---|
| fedora | 118 | 74 | Filesystem query exited 1; zero level-2 rows. One serial-login and two serial-command timeouts. |
| tumbleweed | 118 | 72 | Filesystem query exited 1; zero level-2 rows. Two serial-command timeouts. |
| mint | 110 | 106 | Filesystem query exited 1; zero level-2 rows; inventory contains only accounts, groups and dpkg packages. 96 serial-login timeouts. |
| flatcar | 124 | 84 | Partial failed-query coverage; 852 level-2 rows present. Eight repeated source-id occurrences retained with suffixes. |
| talos | — | — | No inventory: collector terminated with exit -15. |

Execution adaptations listed in READY: continuation after failed commands replaced the scripts’ global stop-on-error behaviour; the unchanged runner was deployed as task-local `lab.sh`; Tumbleweed used the committed runner identifier `opensuse`; host-only connection and service-launch adjustments were recorded in `../in/control/operator-notes.md`. These adaptations did not alter committed command bodies. Identifier suffixing did not remove Flatcar rows.

Talos termination is an execution deviation: the first pagemap read streamed more than 137 GB over 1,112 seconds, while the saved listing contained 359 pagemap paths and 114,323 regular files that the collector would read without a bound before writing its object table. No repair, selective continuation, synthesized inventory or rerun was performed. Evidence: `../in/control/talos/termination.json`, `../in/control/talos/host-read-observation.json`, `../in/control/talos/listing-operational-counts.json`, and `../in/control/review-talos-operation.md`. Missing queries and the terminated collector are data insufficiency, not definition-derived failures. The confirmed Mint counterexample independently sets the overall outcome to 0.


Quote validation: `/usr/bin/python3 -I bin/check_quotes.py D1/RESULT.md`; output is in `../fix-d1-h-1/raw/quotes-result.txt`. Corrected counts and unchanged ordered samples are in `raw/recompute.txt`.

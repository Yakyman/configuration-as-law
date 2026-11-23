TRIAL: 2 confirmed holes

# A1 wording-trial review

Review date: 2026-11-22 UTC. This is the first-cycle wording trial specified in Section 5, not a Section 4 check of the hypothesis. The text, classifications and adjudication inputs are unchanged. Confirmed counts below identify established row coverage; factual uncertainty about additional rows is reported separately.

## Numbers

[STATS.md](../../compare/STATS.md): **5,200 objects**, **4,171 matching decisions (80.21%)**, **Cohen’s kappa 0.48385**; **1,084 adjudicated rows**.

| Original adjudication verdict | Rows |
|---|---:|
| RESOLVED:MUST | 279 |
| RESOLVED:NOT | 541 |
| HOLE | 174 |
| UNKNOWN | 90 |

The 90 adjudicated UNKNOWN rows comprise 66 stored groups, 15 package-owned-path groups and 9 system-closure store objects. Adding the 37 non-adjudicated UNKNOWN agreements gives **127 input UNKNOWN rows**: stored groups 87, package-owned paths 17, system-closure store objects 17, directory skeletons 6. IDs and names: [unknown-rows.tsv](../../review/unknown-rows.tsv). Counts and input hashes: [counts.json](../../review/counts.json). These are input counts, not a new classification of all 5,200 rows; factual UNKNOWNs discovered in the samples are reported separately below.

## Confirmed hole 1 — Scope of a setting applied by one program

A setting applied by one program can control other processes, devices or files. The phrase in force only inside one program does not decide whether to follow the applying program or the reach of its effects, so the text does not determine whether the exemption applies.

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

**Type: one missing sentence (scope criterion).** Reading S2.2-7 as an effect boundary would give MUST; reading it as the place where the configuration is applied would give NOT. S2.2-13 identifies a values file as a setting but does not select either reading. The general removal rule cannot determine the scope of its own exception. This is a definition gap rather than a system-design choice. The initial effect-only refutation was therefore withdrawn after independent challenge; [hole-1-notes.md](../../review/hole-1-notes.md) records the attempted refutations and the final boundary.

**Established extent: 721 rows** — 683 standalone definitions and 38 groups with affected constituents. By kind: 486 system-unit definitions, 36 user-unit definitions, 120 system-closure store objects, 45 stored groups, 33 package-owned-path groups and 1 package. A group may also contain independently required code or login rules; its inclusion does not make every member or its overall MUST summary ambiguous. **158 further candidate rows remain factually unestablished**; they are not counted as confirmed.

Examples (full names and exact membership are in the linked TSV):

| ID | Name and effect |
|---|---|
| nixos-009e4f8fbe | `/etc/modules-load.d`: loader settings select kernel modules |
| nixos-195e0d56cd | `…-etc-systemd-logind.conf`: KillUserProcesses controls other processes |
| guix-331ca6e362 | `…-dbus-configuration`: bus policy controls other applications’ communication |
| guix-f8cae21bbc | `…-ntpd.conf`: time sources affect the system clock |
| freebsd-83dfca210b | `/var/crash`, the minfree setting selecting whether dumps are written |
| freebsd-9a8da13e5c | `/etc/newsyslog.conf`: rotation settings affect other programs’ log files |
| nixos-2353155ce2 | `…-unit-systemd-journal-flush.service`: manager values control a separate logging process |
| nixos-6cad6264ed | `…-etc-ssh-ssh_config`: client settings select connection/authentication behaviour |

All confirmed, uncertain and excluded candidate IDs, kinds, names and individual evidence: [hole-1-extent.tsv](../../review/hole-1-extent.tsv). The [whole-table scan](../../review/hole-1-scan.tsv) visits all 5,200 rows by kind and name, including agreements; [build-hole-1-extent.py](../../review/build-hole-1-extent.py) reproduces it. Of the original 97 card-1 rows, 86 remain confirmed, 8 require more facts and 3 fail the single-program premise. The named `nixos-4d1b734b98` sysctl example is among the latter: both systemd-sysctl and installed procps sysctl can apply the file. The original card’s count is not copied as the extent.

Stored native unit files and inventory rows explicitly backed by fragment files are included as configuration definitions: ExecStart names a separate executable and does not itself make the unit file executable code. Sourced shell/Scheme files are instead covered by the code clause. Socket names alone do not establish a network port rather than a Unix socket/FIFO; such unproved cases stay unknown. Shared-reader configurations, known non-operative defaults and runtime-only reflections are separated in the extent record. Evidence is the individual joined-row facts, available inventory, saved configuration/module sources, and unit-format documentation linked in the notes.

## Confirmed hole 2 — Compiled code kept as a cache

Compiled Guile code runs with the executing program’s rights, so S2.2-10 requires it to be recorded. When the same source remains available and is loaded or recompiled automatically after deletion, S2.2-5 also exempts that code as a cache, and the text gives neither sentence priority.

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”

**Type: two sentences collide.** This is original card 4. The own-interface exemption does not cover unrestricted Guile execution; code versus values does not resolve code versus cache. S2.5-1 addresses treatment of state, not this conflict between two express recording clauses. The saved Guile loader actually runs a compiled thunk or, if it is absent, compiles or loads the retained source (`(not published: adjudication scratch)`, lines 1209–1272).

**Established extent: 5 row occurrences** — 4 standalone rows plus 1 aggregate containing confirmed components. **7 further candidate rows are factual UNKNOWN; 7 candidates are FACT-WRONG.**

| Coverage | IDs and names |
|---|---|
| 2 user caches | `guix-084d6fb332` `/home/guest/.cache/guile`; `guix-033f2e4eef` `/root/.cache/guile` |
| 2 imports with captured fallback paths | `guix-eaca1bed67` `ciyca72…-module-import-compiled`; `guix-5e84abb70c` `miwzgjj…-module-import-compiled` |
| 1 aggregate | `guix-25ad6943ae` Guix Home closure outside current system and user-package closures |

The aggregate also contains sources and other required objects: whole-group deletion is not a speed-only operation. Full paths, kinds, all 19 screened IDs and individual certainty: [hole-4-extent.tsv](../../review/hole-4-extent.tsv). The whole-table kind/name search retained [347 relevant candidates](../../review/hole-4-search.tsv), including agreements. Packages/bundles containing both source and compiled files are not wholesale caches; directly named shepherd `.go` files have no established automatic fallback; browser/shader caches have no established execution with all the host program’s rights. Six additional compiled-node outputs found by the whole-table search are FACT-WRONG as hole instances: their files are copied into the final runtime union, so removing the separate build inputs does not trigger source fallback there. The exact-object execution premise is false; their original MUST agreements are not themselves being reclassified here.

Six unmatched import outputs remain unverified: `guix-4693999f1c`, `guix-a36c632a1b`, `guix-9b6df1084f`, `guix-1823ef372b`, `guix-b54e286053`, `guix-060983918a`. The seventh unknown is `guix-da5f01a3ef`, whose exact outside-store member list excludes the confirmed Home objects and contains 18 other unmapped compiled-import outputs. It is not counted twice through the Home group. Exact membership analysis: [final-boundaries.md](../../review/final-boundaries.md).

Evidence: the two cache entries in `../../in/raw/guix/unowned-groups.json` and retained configuration sources; paired paths in `system-boot.scm` and `configuration/run/current-system/activate`; `../../in/raw/guix/home-closure-outside-system-and-user.txt`; and `(not published: adjudication scratch)` (source/compiled nodes, bundle links, copying into the final union and runtime paths), which excludes the six separate build inputs. The exact-hash metadata attempt and hash-verified empty-directory exclusion are saved in [extent-evidence-limit.md](../../review/extent-evidence-limit.md). Missing source/loader mappings prevent an unconditional extent count beyond the established rows.

## Cards and instances not confirmed

Per-example refutations with exact quotations are in [cards.md](../../review/cards.md); its withdrawn card-1 discussion is explicitly marked as superseded.

- **Card 2 — REFUTED:** S2.2-4 requires unchanged capabilities apart from unavailable content; the alleged lost lookup/program functions instead satisfy S2.2-2.
- **Card 3 — REFUTED:** S2.2-5 requires unchanged operation apart from speed; the alleged failures satisfy S2.2-2 despite eventual regenerability.
- **Card 5 — OUTSIDE:** treatment and independent deletion of manager/kernel runtime reflections falls under S2.5-1.
- **Card 6 — REFUTED:** S2.2-1 covers the established later account-creation change; neither it nor S2.2-2 adds a now-only restriction.
- **Card 7 — REFUTED:** S2.2-6 exempts past records, not the directory switch selecting future persistent logging; S2.2-2 decides its relevant existence.
- **Card 4 instance `guix-2b6eee2e59` — FACT-WRONG:** its exact substitute artifact is an empty directory, not compiled code; the 96-byte NAR hash matches its narinfo.
- **Six whole-table H4 candidates — FACT-WRONG:** `guix-ba6bc2924d` (guix-system-tests), `guix-8fd6717fba` (guix-system), `guix-9e2b09e306` (guix-packages-base), `guix-d6f4da0567` (guix-extra), `guix-9849b393fe` (guix-cli-core), and `guix-0c0c8b4f78` (guix-cli) are copied build inputs, not the exact runtime code objects claimed by the candidate; see the saved source trace in [final-boundaries.md](../../review/final-boundaries.md).

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”

S2.2-6: “records of the past—logs, history;”

S2.5-1: “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.”

## Seeded samples

Sampling: `random.Random(seed).sample(sorted(pool, key=id), n)`, without replacement. All IDs in selection order are saved in [resolved-sample.tsv](../../review/resolved-sample.tsv) and [agreed-sample.tsv](../../review/agreed-sample.tsv). [build_records.py](../../review/build_records.py) checks that order and renders the resolved audit and code/cache extent records; the agreed audit contains individual review judgments.

**Resolved — seed 112221, 40 of 820 eligible rows** (17 input MUST, 23 input NOT): **14 quoted resolutions supported; 26 challenged**. Candidate dispositions: **15 REFUTED, 3 FACT-WRONG, 6 OUTSIDE, 2 CONFIRMED as hole 1**. Of the 15 refuted wording candidates, 13 have a decision from the full applicable sentence set and 2 yield factual UNKNOWN under S3-2. No new hole type was found. All rows, original quotes, corrective IDs and reasoning: [resolved-audit.tsv](../../review/resolved-audit.tsv).

- **CONFIRMED:H1:** `nixos-6cad6264ed` (ssh_config) and `coreos-4d2a7c7537` (systemd enablement settings). The sampled `/etc/ssh` group `debian-c366c1919d` additionally contains an H1 client-setting component, but its overall MUST still follows from the explicit server-login rule.
- **FACT-WRONG:** `debian-9e34733f17` python-apt-common (available interpreter/library can use its templates); `guix-68f88fa3ed` xorgproto (GCC preprocessing/compilation-to-assembly needs no binutils); `ubuntu-b20e807939` APT indexes (missing indexes lose selection/lookup capability until a separate refresh). All three are MUST under S2.2-2.
- **REFUTED, factual UNKNOWN:** `guix-0abb5d3f0a` ALSA topology (exact compiler availability unestablished); `debian-4a04681652` package-owned `/var/log/apt` directory (not itself past logs; automatic recreation verified for 2.6.1, not the recorded 2.6.2).
- **Other REFUTED candidates:** no-contribution NOT cases require S2.2-1’s scope, not the converse of S2.2-2 alone; Thunderbird needs content/history as well as settings exemptions; the APT-cache group needs S2.5-1 for its lock; a profile link tree needs the removal rule rather than calling it a program.
- **OUTSIDE:** four program-state groups and two kernel-thread runtime groups under S2.5-1; this does not exempt kernel code or create a blanket state-recording exemption.

Primary-source and version details: [resolved-fact-challenges.md](../../review/resolved-fact-challenges.md). The differing treatment of configurations, runtime instances and aggregate members is checked in [final-boundaries.md](../../review/final-boundaries.md).

**Agreed — seed 112222, 60 of 4,116 eligible rows**, requiring `same=yes` and absence from adjudication: **48 supported decisions (46 MUST, 1 NOT, 1 UNKNOWN); 12 challenged**. **10 candidates are CONFIRMED as hole 1**, including eight file-backed unit definitions, the stored journal-flush unit and newsyslog.conf. **2 candidates are refuted as wording holes by S3-2 but remain factually UNKNOWN**: `arch-18fb2985ed` (grouped mounts without member-to-fragment mapping) and `coreos-160df5d64d` (nftables-services, insufficient evidence for the alleged decisive rule contents). No additional hole type was found. All 60 IDs, exact sentence sets, reasons and evidence: [agreed-audit.tsv](../../review/agreed-audit.tsv); details: [agreed-notes.md](../../review/agreed-notes.md).

S3-2: “If what the object does remains unknown, the case yields ?.”

No removal experiment was run. Older raw-X1/raw-X2/raw-E6 inventories are absent under `A1/in/raw/`; their saved evidence fields were used where relevant. The unknown candidate extents above are evidence limitations, not additional wording holes or assertions that those rows are outside the confirmed kinds.

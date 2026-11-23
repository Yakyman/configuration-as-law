LIVED-IN: 3 confirmed holes

Review date: 2026-11-22 UTC; corrected through fix round 2. This additional lived-in-machine review is beyond the published plan and carries **no published-check outcome**. Three overlaps in the recording rules survive attempted refutation. No change to the text or failure conditions is proposed or assumed. [Round-1 correction record](FIX-A3R-H-1.md); [round-2 correction record](FIX-A3R-H-2.md).

## Numbers and evidence

From `compare/STATS.md`: **5,212 objects**, **3,854 matching decisions (73.94%)**, **Cohen's kappa 0.55445**; **2,010 rows adjudicated**. Agreement includes matching HOLE and MIXED decisions and is not itself a correctness measure.

The original adjudication verdicts, counted from `adjudication/rows.tsv`, are:

| Verdict | Rows |
|---|---:|
| RESOLVED:MUST | 681 |
| RESOLVED:NOT | 226 |
| RESOLVED:MIXED | 441 |
| HOLE | 621 |
| UNKNOWN | 41 |
| Total | 2,010 |

`RESOLVED:MIXED` is an emitted label outside the verdict set specified by (not published: orchestration and working notes); these 441 rows are reported as received, not as valid adjudications. In **9 of the 12 sampled MIXED rows**, the quoted sentence decides only the code members, not the exempt members; see [all 12 sampled MIXED IDs](fix-a3r-h-1/mixed-sample.tsv) and the [corrected sample audit](fix-a3r-h-1/sample_audit.tsv). The review's denominator of 11 was a counting error.

The 41 adjudicated UNKNOWN rows comprise **22 processes**, **18 package-environment-evidence objects**, and **1 stored subtree** (the NSS certificate/key store). Their missing facts concern executable identification, manifest contents and populated key-store contents. Another **5 unadjudicated rows have UNKNOWN from both classifications**, all stored-outside-packages: **46 pre-review UNKNOWN rows** in the combined adjudicated/agreed result. These are evidence limitations under S3-2, not confirmed holes. This review does not claim to reclassify all 5,212 rows.

Of the **8 original cards**, **2 are CONFIRMED**, **5 REFUTED**, **1 is ? under S3-2 (facts not established)**, **0 FACT-WRONG**, and **0 OUTSIDE**. Card 6 is not refuted: S3-2 does not decide whether its examples must be recorded or disprove the hypothetical redundancy question. Rechecking the resolved sample adds **one confirmed card**, numbered 9 to preserve the original card IDs.

The corrected membership ledger is [fix-a3r-h-2/code_extent.tsv](fix-a3r-h-2/code_extent.tsv): **115 rows for card 1**, **4 for card 7**, **3 overlapping**, hence **116 distinct rows** for those two cards; card 9 adds **26 rows**, for **142 distinct rows** overall. Rows are represented directory groups/subtrees, not individual files. Every witness is matched to actual members or a represented subtree; a broad pathname alone does not add all descendants. The [round-2 correction script](fix-a3r-h-2/recount.py) searches all 5,212 rows for card 9's system- and user-instance markers and preserves cards 1 and 7 from the round-1 ledger without reclassifying them. [Computed counts](fix-a3r-h-2/counts.json).

S2.5-1 is not used as a recording exemption anywhere in this corrected review. S3-1 directs coverage decisions to Section 2.2; treatment of program state remains a design question. The proposed broader reading that would exempt state itself, and its consequences for these cases, are recorded without adopting it in [the author question](fix-a3r-h-1/QUESTIONS.md). A known-function conflict is retained as a hole, not recoded as missing data. [Per-row analysis](fix-a3r-h-1/scope-review.md).

## Confirmed hole 1 — Executable caches with source fallback

Regenerable editor and interpreter caches execute with the consuming program's rights, while removing the cache leaves the source-backed operation available and changes its speed. The cache exemption and the code requirement give opposite recording decisions for that same cache, with no sentence selecting between them.

- S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

**Two sentences collide: S2.2-5 and S2.2-10.** S2.2-13 resolves code versus settings, but does not withdraw the cache exemption. S2.5-1 concerns the design of state handling; the disputed question here is the simultaneous recording requirements for identified executable cache objects.

Examples:

| ID | Name | Qualifying member/function |
|---|---|---|
| dd743d5660f8360b1a7dd17e | /home/user/.emacs.d/elpa/embark-consult-20260503.118 | Lisp source and its byte-compiled .elc copy |
| lived-tcf3018d0d8 | /home/user/.emacs.d/eln-cache/30.1-c7a97098 | Regenerated native editor trampolines |
| 8116f43e8ff91b41a1de6d2b | /home/user/.cache/nvim/luac | Lua bytecode with source fallback |
| 00be4be3f78767b555ebdc00 | /home/user/.local/state | Generated lazy.nvim Lua package cache |
| lived-t59f3c9499d | /var/lib/flatpak/runtime/org.gnome.Platform | Interpreter-library bytecode with its corresponding source |

**Extent: 115 rows**: 69 stored-outside-packages, 45 stored-outside-packages:subtree, and 1 executable-code-outside-packages:subtree. The ledger identifies each ID, name and exact source/consumer witness. It contains **113 of the original card's 132 rows**, plus `4977b521c631e8b76eb7538b` `/home/user/Projects` and `lived-t59f3c9499d` above. The runtime witnesses use standard-library (not published: external working record) and its compiled cache, not shipped source/license-tree bytecode.

The original Go download-cache script, Cargo binary fixture and hashed Flatpak repository examples do not establish that removal of their represented paths merely slows the same operation. Other withheld memberships lack demonstrated fallback or execution rights. [review/code_unknown.tsv](review/code_unknown.tsv) records **19 original memberships and 1 additional source/license-tree candidate** as uncertain; they are not counted as confirmed. Merely being compiled, regenerable in principle, or named cache is insufficient. Details, including attempts to refute every original example, are in [review/code_cards.md](review/code_cards.md).

## Confirmed hole 2 — History stored as executable editor code

Saved editor history is exempt as a record of the past. Restoring the same history by executing it with the editor's rights also makes recording mandatory, and the text does not settle that overlap.

- S2.2-6: “records of the past—logs, history;”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

**Two sentences collide: S2.2-6 and S2.2-10.** The settings clarification in S2.2-13 does not withdraw the history exemption. Excluding a design question about how to preserve state does not decide these two opposite recording obligations.

Examples: `99b8709d5a3af244262c5442` `/home/user/.emacs.d/savefile`, containing recentf and savehist loaded as Lisp, and the represented ancestors `/home`, `/home/user`, and `/home/user/.emacs.d`. The saved Neovim session is not established to be history and is excluded from this card.

**Extent: 4 rows**: `/home`, `/home/user`, `/home/user/.emacs.d`, and `/home/user/.emacs.d/savefile`. All four IDs and history witnesses are in `fix-a3r-h-2/code_extent.tsv`, card 7. Three overlap card 1; the savefile row does not. The [three removed session memberships](fix-a3r-h-1/removed-history-memberships.tsv) remain in card 1 through separate executable-cache witnesses. The earlier card-7 extent and session rationale in `review/code_cards.md` are superseded by this correction; its recentf/savehist evidence is retained.

## Confirmed hole 3 — Past enablement records govern future service links

The service helper stores markers recording that enablement was previously performed, which are exempt as records of the past. It also consults those same markers before creating service links, so the computer's behaviour depends on them, and the text does not settle the two recording obligations.

- S2.2-6: “records of the past—logs, history;”
- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

**Two sentences collide: S2.2-6 and S2.2-1.** The installed helper version is `1.69~deb13u1` (`in/raw/lived/raw/003-packages-root-dpkg-query.out`, line 227). Its [primary source](https://sources.debian.org/data/main/i/init-system-helpers/1.69~deb13u1/script/deb-systemd-helper), preserved as [numbered excerpts](fix-a3r-h-2/raw/helper-source.txt), defines both system and user marker directories (source lines 100–110), selects the user directory for user units (576–580), and maps active-link paths to these marker paths and checks marker existence before link creation in the same branch for both instances (354–375). The comment states that the marker records the earlier enable action. This is not an inference from a state-directory name, and does not require the unverified assertion that the next upgrade necessarily re-enables a disabled service.

Examples: `e6c7b500df6175d8c883f1e4` `/var/lib/systemd/deb-systemd-helper-enabled/multi-user.target.wants`; `ca410235ff67492d407759ef` `/var/lib/systemd/deb-systemd-helper-enabled/timers.target.wants`; `42940ad70e4f8bb281976b38` `/var/lib/systemd/deb-systemd-helper-enabled/sockets.target.wants`. Their represented members are the helper's regular-file markers, not active service symlinks.

**Extent: 26 stored-outside-packages rows**, ledger card 9: 19 system marker-directory groups, 4 user marker-directory groups, both helper-state parent groups and `/var/lib/systemd`. [67 inventoried marker witnesses](fix-a3r-h-2/helper-witnesses.tsv) (56 system, 11 user) and the [whole-table membership search](fix-a3r-h-2/helper-search.tsv) establish the represented extent, including ancestors only where their member lists include the witness-bearing directory. The [five added memberships](fix-a3r-h-2/added-memberships.tsv) are the user-helper parent and its `default.target.wants`, `graphical-session-pre.target.wants`, `graphical-session.target.wants` and `sockets.target.wants` groups. For example, `60af4555f895a621f8fdd8b5` `/var/lib/systemd/deb-systemd-user-helper-enabled/default.target.wants` contains the regular-file `pulseaudio.service` marker. No overlap with cards 1 or 7. Refutation attempts and the distinction from a state-handling design question remain in [scope-review.md](fix-a3r-h-1/scope-review.md); the earlier system-only extent is superseded by this correction.

## Cards that did not survive

The following exact Section 2.2 and Section 3 sentences support the refutations and the sample dispositions; the linked reviews apply them individually to every example. S2.5-1 is quoted only to explain why these cards are not OUTSIDE; it supplies neither a recording exemption nor a refutation.

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.5-1: “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.”
- S3-1: “Whether an object must be recorded. The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.”
- S3-2: “If what the object does remains unknown, the case yields ?.”

- **Card 2, Compiler and build input — REFUTED:** the specified lost build/type-checking operations meet S2.2-2; S2.2-13 never claims an exhaustive taxonomy, and S2.2-4's unchanged-capability condition is not met. [Per-example review](review/settings_cards.md).
- **Card 3, In force only inside one program — REFUTED:** one reader does not establish force confined to that reader; the specified account, network, printing, device, process and firmware effects meet S2.2-1/2. [Per-example review](review/settings_cards.md).
- **Card 4, Command strings in value files — REFUTED:** S2.2-10 applies to the executed command strings without requiring the enclosing file to be executed whole; S2.2-7 does not exempt their independent process effects. [Per-example review](review/settings_cards.md).
- **Card 5, Named cache or database that is not dispensable — REFUTED:** on its stated disabling-removal facts, S2.2-2 applies and the behavioural qualifications in S2.2-4/5 fail; a class name alone is no exemption. [Per-example review](review/cache_redundancy.md).
- **Card 6, Redundant copies — ? under S3-2 (facts not established):** filenames, symlinks and an absent second hash link do not establish identical certificates or unchanged effective trust; no certificate bytes/fingerprints or rehash transcript were saved. This decides neither MUST nor NOT and is not a refutation. [Evidence and all five IDs](review/redundancy_unknown.tsv). The REFUTED label in `review/cache_redundancy.md` is superseded; its evidential limitations remain valid.
- **Card 8, Documents that carry macros — REFUTED:** S2.2-10 requires the stated macro; losing its font-sample-building behaviour fails S2.2-4's content-only condition, while ordinary document members remain exempt. [Example review](review/code_cards.md).

## Seeded sample findings

Both samples use `random.Random(seed).sample` without replacement from populations sorted lexically by ID. The [correction script](fix-a3r-h-1/recount.py) verifies the unchanged selections. The [corrected sample audit](fix-a3r-h-1/sample_audit.tsv) records **every selected ID and name**, seed, order, original-quotation check, review decision, candidate disposition, reason and exact sentences. The original selected records remain untouched in `review/resolved_sample.json` and `review/agreed_sample.json`.

**Resolved sample:** seed **2026112201**, **40 of 1,348** RESOLVED rows. **22 decisions have support** and **18 rows became candidates**: **9 REFUTED** MIXED plugin candidates require additional content/settings sentences to decide their exempt members; **7 remain ? under S3-2** (three METADATA copies, the Netdata package-manifest group, journal stream metadata, the staged os-release copy and the container-runtime subtree); **1 is FACT-WRONG**, the Ghostscript values-only rationale; **1 is CONFIRMED**, the enablement-history collision now card 9. The seven unknowns are not counted as refuted candidates. The four formerly accepted S2.5-1 NOT rows are reassessed individually in [scope-review.md](fix-a3r-h-1/scope-review.md); none retains NOT merely because it is program state. These counts do not endorse the original verdicts on the factual problem rows.

Separately, **15 of the 40 original quote cells are not full exact sentences**: nine shortened code quotations, three missing terminal punctuation, two ellipsized scope quotations and one truncated code/settings quotation. The audit supplies full exact sentences; the original adjudication files were not changed. Eight sampled project manifests do satisfy their quoted removal rule through loss of their saved script-dispatch operations, without relying on the adjudication's overly broad implication that every manifest removal breaks runtime import. Saved fields and source checks are in [review/settings_cards.md](review/settings_cards.md) and [review/sample_sources.md](review/sample_sources.md).

**Agreed sample:** seed **2026112202**, **60 of 3,202** matching, unadjudicated rows. **60 shared decisions have support** in their cited Section 2.2 rules, on the recorded functional facts. The udev link-arbitration row `e2107a3dd8d91a0eef56dac4` is MUST by its recorded device-naming effect; the earlier OUTSIDE verdict is withdrawn. S2.5-1 is not a literal recording exemption; the proposed broader reading remains the [author question](fix-a3r-h-1/QUESTIONS.md), not an adopted rule. The six Go-cache and three shader-cache rows retain their earlier assessment: full execution rights are not established, so compiled bytes alone do not create another confirmed collision. **No new confirmed hole from this sample** results.

The samples expose incomplete quotations, unsupported factual inferences and one scope error; agreement and an adjudication label do not substitute for the cited sentence deciding the represented object. Their findings are sample counts, not estimates of unreviewed errors throughout the table.

The earlier independent reviews in `review/independent_review.md` and [fix-a3r-h-1/independent-review.md](fix-a3r-h-1/independent-review.md) predate round 2. The round-2 findings and corrections are recorded in [FIX-A3R-H-2.md](FIX-A3R-H-2.md). The [independent round-2 review](fix-a3r-h-2/independent-review.md) accepts both corrections and independently verifies the full-table extent, preserved cards, frozen-file digests and quotations. The required quote check passes: **14 quotations checked, 0 missing from TEXT.md**, [saved output](fix-a3r-h-2/raw/quote-check.txt). Cards 1 and 7 and the sample audit remain unchanged; round 2 reruns only card 9's extent and derived counts, plus output validation. Frozen inputs and prior review outputs remain unchanged.

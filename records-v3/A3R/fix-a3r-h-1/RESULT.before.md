LIVED-IN: 2 confirmed holes

Review date: 2026-11-22 UTC. This is the additional lived-in-machine review beyond the published plan, not a replacement for its prescribed clean-machine check. Its outcome is **0**: two overlaps in the recording rules survive attempted refutation. No change to the text is proposed or assumed.

## Numbers and evidence

From `../compare/STATS.md`: **5,212 objects**, **3,854 matching decisions (73.94%)**, **Cohen's kappa 0.55445**; **2,010 rows adjudicated**. Agreement includes matching HOLE and MIXED decisions and is not itself a correctness measure.

The original adjudication verdicts, counted from `../adjudication/rows.tsv`, are:

| Verdict | Rows |
|---|---:|
| RESOLVED:MUST | 681 |
| RESOLVED:NOT | 226 |
| RESOLVED:MIXED | 441 |
| HOLE | 621 |
| UNKNOWN | 41 |
| Total | 2,010 |

The 41 adjudicated UNKNOWN rows comprise **22 processes**, **18 package-environment-evidence objects**, and **1 stored subtree** (the NSS certificate/key store). Their missing facts concern executable identification, manifest contents and populated key-store contents. Another **5 unadjudicated rows have UNKNOWN from both classifications**, all stored-outside-packages: **46 pre-review UNKNOWN rows** in the combined adjudicated/agreed result. These are evidence limitations under S3-2, not confirmed holes. This review does not claim to reclassify all 5,212 rows.

Of the **8 original cards**, **2 are CONFIRMED**, **6 REFUTED**, **0 FACT-WRONG**, and **0 OUTSIDE**. Refutation of card 6 is procedural: S3-2 gives ? for its unverified factual premise; it does not establish NOT or disprove the hypothetical redundancy question. Some individual claims and sample decisions have separate factual or scope defects below.

The complete confirmed membership ledger is [review/code_extent.tsv](../review/code_extent.tsv): **115 rows for card 1**, **7 for card 7**, **6 overlapping**, hence **116 distinct rows**. Rows are counted as represented directory groups/subtrees, not individual files. Every qualifying witness is matched to the row's actual members or subtree; a broad pathname alone does not add all descendants. Searches include all kinds and names in (not published: outside selected checks and direct evidence), irrespective of agreement or adjudication. The reproducible scan and its source/fallback checks are in [review/code_extent_build.py](../review/code_extent_build.py).

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

The original Go download-cache script, Cargo binary fixture and hashed Flatpak repository examples do not establish that removal of their represented paths merely slows the same operation. Other withheld memberships lack demonstrated fallback or execution rights. [review/code_unknown.tsv](../review/code_unknown.tsv) records **19 original memberships and 1 additional source/license-tree candidate** as uncertain; they are not counted as confirmed. Merely being compiled, regenerable in principle, or named cache is insufficient. Details, including attempts to refute every original example, are in [review/code_cards.md](../review/code_cards.md).

## Confirmed hole 2 — History stored as executable editor code

Saved editor history is exempt as a record of the past. Restoring the same history by executing it with the editor's rights also makes recording mandatory, and the text does not settle that overlap.

- S2.2-6: “records of the past—logs, history;”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

**Two sentences collide: S2.2-6 and S2.2-10.** The settings clarification in S2.2-13 does not withdraw the history exemption. Excluding a design question about how to preserve state does not decide these two opposite recording obligations.

Examples: `99b8709d5a3af244262c5442` `/home/user/.emacs.d/savefile`, containing recentf and savehist loaded as Lisp; `00be4be3f78767b555ebdc00` `/home/user/.local/state` and `lived-tbba8c81784` `/home/user/.local/state/nvim`, representing the sourced saved session.

**Extent: 7 rows**: `/home`, `/home/user`, `/home/user/.emacs.d`, `/home/user/.emacs.d/savefile`, `/home/user/.local`, `/home/user/.local/state`, and `/home/user/.local/state/nvim`. All seven IDs and their represented history witnesses are in `../review/code_extent.tsv`, card 7. Six overlap card 1; the savefile row does not. The original exclusive assignment of only one row to card 7 understated its full-table extent. Raw file presence and recorded consumer evidence are distinguished in `../review/code_cards.md`.

## Cards that did not survive

The following exact sentences support the refutations and the sample dispositions; the linked reviews apply them individually to every example.

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.5-1: “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.”
- S3-2: “If what the object does remains unknown, the case yields ?.”

- **Card 2, Compiler and build input — REFUTED:** the specified lost build/type-checking operations meet S2.2-2; S2.2-13 never claims an exhaustive taxonomy, and S2.2-4's unchanged-capability condition is not met. [Per-example review](../review/settings_cards.md).
- **Card 3, In force only inside one program — REFUTED:** one reader does not establish force confined to that reader; the specified account, network, printing, device, process and firmware effects meet S2.2-1/2. [Per-example review](../review/settings_cards.md).
- **Card 4, Command strings in value files — REFUTED:** S2.2-10 applies to the executed command strings without requiring the enclosing file to be executed whole; S2.2-7 does not exempt their independent process effects. [Per-example review](../review/settings_cards.md).
- **Card 5, Named cache or database that is not dispensable — REFUTED:** on its stated disabling-removal facts, S2.2-2 applies and the behavioural qualifications in S2.2-4/5 fail; a class name alone is no exemption. [Per-example review](../review/cache_redundancy.md).
- **Card 6, Redundant copies — REFUTED as a demonstrated hole:** S3-2 decides all five examples as ? because filenames, symlinks and an absent second hash link do not establish identical certificates or unchanged effective trust; no certificate bytes/fingerprints or rehash transcript were saved. [Evidence and all five IDs](../review/redundancy_unknown.tsv), [review](../review/cache_redundancy.md).
- **Card 8, Documents that carry macros — REFUTED:** S2.2-10 requires the stated macro; losing its font-sample-building behaviour fails S2.2-4's content-only condition, while ordinary document members remain exempt. [Example review](../review/code_cards.md).

## Seeded sample findings

Both samples use `random.Random(seed).sample` without replacement from populations sorted lexically by ID. [review/audit_samples.py](../review/audit_samples.py) reproduces and verifies the selections. [review/sample_audit.tsv](../review/sample_audit.tsv) records **every selected ID and name**, seed, order, original-quotation check, review decision, candidate verdict, reason and exact resolving sentences. The untouched selected records are also saved as `../review/resolved_sample.json` and `../review/agreed_sample.json`.

**Resolved sample:** seed **2026112201**, **40 of 1,348** RESOLVED rows. **26 decisions have support**, including four design-scope exclusions coded NOT by the adjudication. **14 rows became candidates**: nine MIXED plugin rows whose quoted code rule does not decide their exempt members are REFUTED by the additional literal content/settings sentences; four rows with insufficient functional facts (three METADATA copies and the Netdata package-manifest group) are REFUTED as demonstrated holes by S3-2, leaving their reviewed coverage UNKNOWN; one Ghostscript font-map rationale is FACT-WRONG because the resource-map loader executes cidfmap rather than only reading both maps as values. **No new confirmed hole** results. These findings do not endorse the original verdict on the five factual problem rows.

Separately, **15 of the 40 original quote cells are not full exact sentences**: nine shortened code quotations, three missing terminal punctuation, two ellipsized scope quotations and one truncated code/settings quotation. The audit supplies full exact sentences; the original adjudication files were not changed. Eight sampled project manifests do satisfy their quoted removal rule through loss of their saved script-dispatch operations, without relying on the adjudication's overly broad implication that every manifest removal breaks runtime import. Saved fields and source checks are in [review/settings_cards.md](../review/settings_cards.md) and [review/sample_sources.md](../review/sample_sources.md).

**Agreed sample:** seed **2026112202**, **60 of 3,202** matching, unadjudicated rows. **59 shared decisions have support** in their cited rules; **1 candidate is OUTSIDE**, the transient udev link-arbitration record `e2107a3dd8d91a0eef56dac4`, under S2.5-1's program-state scope exclusion. The six Go-cache and three shader-cache rows were specifically checked for the card-1 overlap: the evidence does not establish execution with the host program's full rights, so compiled bytes alone do not create another confirmed collision. **No new confirmed hole** results.

The samples expose incomplete quotations, unsupported factual inferences and one scope error; agreement and an adjudication label do not substitute for the cited sentence deciding the represented object. Their findings are sample counts, not estimates of unreviewed errors throughout the table.

Independent verification: [review/independent_review.md](../review/independent_review.md). The required command `/usr/bin/python3 -I bin/check_quotes.py A3R/RESULT.md` passes: **11 quotations checked, 0 missing from TEXT.md**; output is saved in [review/quote_check.txt](../review/quote_check.txt).

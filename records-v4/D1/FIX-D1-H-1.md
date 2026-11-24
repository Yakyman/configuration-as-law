# FX-D1-H-1 — response to the D1-H review

Recorded 2026-11-23 UTC. Corrected result: `CHECK 1: 1 confirmed gaps`; outcome **0** under both second-level readings A and B. Confirmed title: **A stored archive whose contents are executed** (card 4; 9 rows).

The corrected report is `D1/RESULT.md`. New output location: `D1/fix-d1-h-1/`; every `raw/` reference below is relative to that directory. The previous result is preserved in `raw/RESULT.before.md`. No classification, adjudication, inventory, published text, original sample, or previous verification output was overwritten. The pre-fix source hashes are in `raw/frozen-input-hashes.json`.

## Finding 1 — FIXED: apply the published failure condition

The former whole-check outcome `?` did not account for the separate disagreement/adjudication clause. The new accounting joins the frozen GAP verdicts to the original decisions: 1,362 disagreements, distributed as AlmaLinux 179, Void 1,126, MicroOS 57. Two matching MIXED/GAP rows are excluded from this particular clause. Exact ids and decisions: `raw/failure-condition-rows.tsv`; counts: `raw/changed-counts.json`.

Section 9.2, quote: “or the two classifications decided differently and the adjudication finds no sentence of the text that resolves the dispute.” Appendix A.4.1, quote: “if no sentence resolves it, the case yields 0.” These give 0 for those three machines, ? for Talos and Gentoo, and 0 for the whole check. Reading B's completeness restriction cannot turn an established 0 into ?. D1-H refutations are no longer used to erase the frozen adjudication findings. No replacement-adjudication procedure is introduced. Even if later verification could replace them, card 4 now independently gives the same outcomes; the result states that conditional comparison without adopting a new rule.

## Finding 2 — NOT FIXED AS REQUESTED: the proposed reversal is not supported

Card 2 remains REFUTED as the asserted S8.2-15/16 collision; its unfinished row-level coverage is explicitly counted under finding 5. The report now gives the textual reason more precisely.

S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

The published heading above S8.2-16 is `Which line records an object.` Its subject is what is installed and its predicate specifies recording lines. Reading the examples as an independent sufficient condition for installed status reverses that dependency and contradicts S8.2-6's express statement that the four questions determine the object. The sentence does not say that every generated list is installed. An example need not cover every subclass of lists; its not applying to non-code, non-package records does not itself create a contradictory requirement. This refutation uses an existing classification rule and the actual sentence's subject, not a new rule ranking conflicting requirements. The two readings were considered; disagreement alone does not establish that both are licensed by the text.

Evidence beyond the original adjudicated examples remains the frozen agreed sample's `alma-3827efd6d880bbf3bcd0736f` (`/var/cache/man/id`): `D1/review/agreed-sample.md` and `.tsv`. No sample was redrawn, and the certificate claim is not used to support this reasoning.

## Finding 3 — FIXED: withdraw the unsupported certificate decision

The two certificate rows, `void-f2e5d5edfa5902c8aee7bace` and `microos-dcce813055fa256ed012c87a`, no longer receive a definitive SETTING decision in the result. Their entries say `UNDECIDED:row-audit`; the cited facts do not establish the necessary Q3 premise. Neither S8.2-13's list nor the word trust proves that the whole computer obeys these values or that they grant the stated access. This correction does not claim that a certificate can never satisfy Q3 with adequate facts. No third classification or additional definition is supplied.

## Finding 4 — FIXED: card 4 remains a gap

The earlier refutation supplied an unstated boundary: extraction was treated as reading only values, and execution of the extracted contents was excluded from execution of the stored archive for Q2. Documentation establishes the mechanism, not that definitional boundary. Card 4 is now CONFIRMED, with the competing RECORD and PROGRAM-DERIVED readings, the different declaration obligations, exact quotes, and all example ids in the result. `D1/QUESTIONS.md` records the readings without selecting or repairing them.

The changed whole-table search covers every kind/name and available L2 member path: `raw/card4-search.tsv` (16,375 rows) and `raw/card4-extent.tsv` (9 affected rows: AlmaLinux 4, Void 4, MicroOS 1). This matches the previous archive extent; the interpretation, not the inventory, changed. The Void `/boot` bucket also has unrelated fact-limited old-kernel members. No claim that all members of a mixed bucket have the gap is made. The evidence and quoted documentation passage are in `raw/kernel-documentation.md`; no machine probe was necessary.

The review's additional reference to a compiled copy in S8.2-16 does not independently classify the archive; the confirmed gap is whether Q2 applies, not a reversal of the line-selection sentence. This preserves the fixed order of questions.

## Finding 5 — FIXED: expose the unfinished row dispositions

`raw/gap-row-dispositions.tsv` accounts for all 1,364 original GAP rows. Exclusive totals are 9 confirmed archive-gap rows, 1,069 FACT_UNKNOWN-only rows, 2 resolved installed-XPI rows, and **284 explicitly undecided rows** (card 1: 214; card 2: 70). These 284 are an unfinished row audit; they are not silently counted as resolved or relabeled FACT_UNKNOWN. Their original GAP verdicts remain in the failure-condition accounting. The named-example reasoning is not a complete class assignment for every member of those rows.

Of the review's 294 formerly unaccounted rows, 8 are now confirmed gap rows and 2 have the installed-XPI disposition; 284 remain undecided, using the review's explicit option to state that count. The ninth confirmed row, Void `/boot`, was already in the 1,070 additional fact-limited rows. Therefore the unchanged identified fact-limited union of 2,007 overlaps the confirmed gap extent by one row; it must not be added to the gap extent as a disjoint count. The result states this overlap.

## Finding 6 — FIXED: correct the role and acceptance claim

The result now calls the work verification D1-H. The old `D1/review/verification.md` does not establish an independent check and its assurance is withdrawn. To preserve the frozen prior output, it remains byte-for-byte unchanged; the corrected record is `D1/fix-d1-h-1/verification.md`, titled as a self-check, and the result explicitly points to that correction. Mechanical checks do not constitute independent acceptance. The old output directory name is retained only as an evidence path.

## Finding 7 — NOT CHANGED: this is a positive finding

The original object totals, matching share, kappa, verdict counts, 937 original unknown rows, 1,070 additional fact-limited rows, and both sample selections are retained. The review found no discrepancy; none of those calculations or selections changed. Only the new outcome accounting, card 4 extent check, and row-disposition accounting were executed. The corrected result's quotes are validated again because its text changed.

## Finding 8 — FIXED FOR THE UNSUPPORTED CLAIM; supported claims retained

Claim (h), the certificate-setting assertion, is removed as described in finding 3. Claims (a)–(g) retain the saved evidence identified by the review: the kernel update log, current manifest, XPI inventory/hash evidence and installation action, dracut generation log, and the two mixed sample buckets. No new observations or downloads of extension packages were made. The kernel documentation was consulted solely to delimit what it establishes for finding 4.

## Finding 9 — NOT CHANGED: this is a positive scope finding

The fix reads the named task inputs and saved evidence. It runs no VM, installation, experiment, resampling, classification from scratch, or weighting. All new files are under `D1/`; only the explicitly requested `D1/RESULT.md` is updated in place. Neither the published failure condition nor any classification rule is amended.

## Validation and remaining limit

Commands and outputs are recorded in `D1/fix-d1-h-1/verification.md`. The changed audit and quote validation are mechanical self-checks. The 284 undecided row audits are disclosed, not presented as completed classifications, and no independent acceptance of this fix is claimed.

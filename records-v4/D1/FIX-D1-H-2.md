# FX-D1-H-2 — response to review round 2

Recorded 2026-11-23 UTC. **CHECK 1: 3 confirmed gaps; outcome 0 under both inventory readings.**

Changed files: `D1/RESULT.md` and `D1/QUESTIONS.md`. New evidence and scripts: `D1/fix-d1-h-2/`. The preceding result and questions are preserved in `raw/RESULT.before.md` and `raw/QUESTIONS.before.md`. Frozen classifications, adjudication, inventories, samples and earlier fix outputs were not edited. No new observation, probe, download, machine run, resampling, weighting or hypothesis amendment was performed.

## 1. Card 2 refutation — FIXED

Withdrawn. The former argument chose the reading in which S8.2-16 only supplies a line after classification. Its generated-list example also supports the installed-object reading, which conflicts with Q4's optional program-record branch. S8.2-6 does not explicitly rank the separate recording-line paragraph against Q4. Both readings are recorded in `D1/QUESTIONS.md`; neither is adopted as a new rule.

Card 2 is CONFIRMED as a collision between S8.2-15 and S8.2-16, producing opposite recording obligations through S8.2-2 and S8.2-1. Exact sentence quotations remain in RESULT. This does not mean every original aggregate row is confirmed: generation alone does not resolve missing facts or classify every member.

Whole-table search and evidence review establish **100 rows (AlmaLinux 38, Void 28, MicroOS 34)**: 63 original card-2 rows and 37 additional rows. The additions include 30 manual-page index buckets, 3 GRUB list buckets, a loader cache, active RPM and XBPS databases, and Void `/etc`'s loader-cache member. Exact ids, members and evidence: `raw/card2-extent.tsv`. All 71 original rows: `raw/card2-original-rows.tsv`; dconf remains FACT_UNKNOWN and seven certificate/policy aggregate rows remain undecided. Five further extent candidates retain named source/content uncertainties in `generated/assessment.md` and `generated/dispositions.tsv`. These limits prevent an unsupported claim of exhaustive extent beyond the established rows.

The existing agreement sample's `/var/cache/man/id` check changes from refuted to CONFIRMED. The inactive MicroOS RPM database in the resolved sample changes from supported RECORD to FACT_UNKNOWN: its full content/source package set is not established. Corrected sample TSVs retain every original id and its draw order. Result: agreement sample 57 supported / 1 confirmed / 2 FACT_UNKNOWN; resolved sample 37 supported / 2 refuted candidates / 1 FACT_UNKNOWN. No draw was repeated.

## 2. Card 5 refutation — FIXED

Withdrawn. Q1 establishes the installed package, but does not settle whether S8.2-21 exempts the same object under the other archive/content reading. The previous refutation depended on the boundary left open for card 4. Card 5 is CONFIRMED as the S8.2-1/21 recording conflict, dependent on that boundary; both readings are in QUESTIONS.

The two installed-XPI rows are now `CONFIRMED:installed-contained-code`, not `RESOLVED:INSTALLED-OWN`. Evidence: `raw/card5-extent.tsv`, `raw/xpi-search.tsv`, `archive/assessment.md`, unchanged `D1/review/extension-evidence.json`, and the saved permanent-installation action. Downloaded copies are considered explicitly: material and qualifying contained-code readings both permit omission, so they do not add the installed-package recording conflict.

## 3. Card 4 extent method — FIXED

The new `scan.py` scans all 16,375 kinds/names and available member paths. Its boot-pattern result is written without an equality-to-adjudicated-ids assertion and can differ from the old set. It returns the same nine boot rows; RESULT now explicitly limits that pattern to boot archive names rather than claiming an exhaustive archive search.

A broader search retains **265 archive-family candidates**, covering XPI/other archive names, image kinds, containers and opaque stores. `archive/assessment.md` distinguishes the nine confirmed boot rows, the two installed-XPI conflicts, downloaded copies, boot-loader components and unresolved representation/content facts. The shared card-4/card-5 boundary is explicit. The criticism is accepted; equality of the observed boot subset does not prove completeness.

## 4. Failure condition — NOT CHANGED; review finding accepted

The reviewer reports this as correct, and no repair is needed. The 1,362 disagreeing frozen GAP rows and the Section 9.2 / Appendix A.4.1 reasoning remain as reported in round 1. Machine outcomes remain AlmaLinux 0, Void 0, Gentoo ?, MicroOS 0, Talos ?; whole 0 under readings A and B. The new confirmed kinds do not change the failure condition or its combination procedure.

## 5. Earlier corrections and row ledger — FIXED where findings 1–2 change it

The certificate-setting withdrawal, confirmed card 4, complete original-GAP ledger and self-check labels are preserved. New ledger counts are **64 generated-list / 9 boot-archive / 2 installed-contained-code / 1,069 FACT_UNKNOWN / 220 undecided = 1,364**, each id once. One card-1 row is included because its loader-cache member has card 2's conflict. Thirty-six confirmed rows outside the original GAP population bring the whole confirmed-row union to 111. Evidence: `raw/gap-row-dispositions.tsv` and `raw/changed-counts.json`.

The seven undecided certificate/policy rows are not silently made confirmed merely because their former card-level refutation was withdrawn. The dconf and old-package missing facts remain missing facts.

## 6. Numeric checks — NOT CHANGED for frozen statistics; changed conclusions updated

The review found no discrepancy in object counts, agreement, kappa, original verdicts, unknown sets or nine boot rows. Those statistics are retained rather than rerun as new observations. The card dispositions, corrected extents, ledger and two affected sample checks are recomputed in the new location. The historical 2,007-row fact-limited set is distinguished from newly documented extent uncertainties. Quote-check and mechanical-validation outputs are in `raw/quotes-result-final.log`, `raw/quotes-fix.log`, and `raw/verification.json`.

## 7. Eight supported claims — NOT CHANGED; review finding accepted

The review supports the factual claims, including account provenance, boot members, ten depmod lists plus 19 unchanged package members, and frozen-input hashes. The depmod decision drawn from those facts changes under finding 1; the facts do not. The generated-list sample interpretation changes as described above. Hash validation checks the previous 23-file manifest and this round's scanned inputs; exact counts and differences are in `raw/verification.json`.

## 8. Scope — NOT CHANGED; review finding accepted

Work stayed within this correction: saved-input searches, changed reasoning, ledger/sample accounting, report and author-question updates. No other task's classifications or previous-night records were read. Analytical parts supplied the archive and database/cache evidence notes under the new output directory; they do not constitute independent acceptance. Mechanical checks are self-checks. Independent acceptance of this corrected report remains with review.

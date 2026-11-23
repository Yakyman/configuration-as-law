# FX-D1-H-1 — response to review

Recorded 2026-11-22 UTC. Result: **CHECK 1: 4 confirmed holes; OUTCOME: 0**. Execution and consistency checks are complete; subsequent independent review performs acceptance.

| Finding | Disposition | Correction or evidence |
|---|---|---|
| 1 — adjudication outcomes | FIXED | The result now reports Fedora/Tumbleweed/Mint/Flatcar 0 and Talos ?. The eight-card/924-row original adjudication is preserved and the four-card verification is separately labelled. No new override stage or failure condition is asserted. |
| 2 — metadata decides MUST | FIXED | Removed the blanket ground everywhere, including cards 1/2/5/7 and both samples. A dependency field does not establish the actual removal loss or executable script. Recomputed all four confirmed-card extents, retaining direct script/trust evidence separately. `confirmed-rows.tsv`, `extent-search.tsv`, `fix-d1-h-1/card-audit.md`. The review's universal assertion that dependency removal stops nothing is not adopted as a NOT rule either; the text's scope remains unresolved. |
| 3 — card 3 refutation | FIXED | Card 3 CONFIRMED: S2.2-1/S2.2-2 do not decide between runtime removal and later transaction selection. 319 established rows, including all 127 original rows. No immediate-only or later-run rule is added. |
| 4 — hardware ambiguity called UNKNOWN | FIXED | Card 5 CONFIRMED. Both alsa-sof-firmware rows leave UNKNOWN, as their roles and device absence are in the allowed adjudication notes. Applying the same correction to metadata-only UNKNOWNs and QML facts gives 97, not merely 112: 114 − 2 − 19 + 4. `final-unknown.tsv` identifies every retained/additional case. |
| 5 — Xen sample | FIXED | All ten Xen/menu sample rows plus microcode_ctl are CONFIRMED card-5 candidates. Resolved sample now 10 upheld, 20 confirmed candidates, 7 outside, 3 UNKNOWN. Seeds and ordered ids unchanged. `fix-d1-h-1/sample-audit.md`, `resolved-sample.tsv`. |
| 6 — guest-ROM dependency inconsistency | FIXED via the offered alternative | Drop metadata MUST everywhere. Do not add card 8 as a confirmed collision merely from those reverse dependencies: S2.2-11 and S2.2-12 explicitly call guest-confined code an exemption. Host-read descriptors remain a distinct package fact. The finding correctly identifies inconsistency; its first suggested remedy is unnecessary after its second remedy is applied. `fix-d1-h-1/card-audit.md` and RESULT's Card 8 discussion. |
| 7 — out-of-scope folder reads | FIXED disclosure; historical deviation cannot be undone | RESULT explicitly records the earlier reads of the adjudication work folder and the provenance limitation of retained evidence. No such folder was read this round, and no replacement public fetch is claimed. This uses the review's requested deviation-recording alternative. |
| 8 — headline count | FIXED | Four confirmed cards: 1, 2, 3, 5; two refuted: 4, 6; two fact-wrong: 7, 8. 1,135 established rows enumerated; broad unresolved search memberships kept separate. Overall outcome remains 0. |
| 9 — verified figures and claims | NOT CHANGED where unaffected | Inventory/decision metrics, ordinary-action counts, missing Talos data, emoji package version, process merge and saved factual evidence remain as verified. Old 114-row UNKNOWN and old sample disposition totals described the previous files correctly but are superseded by the corrections above. `RESULT.before.md` preserves that version. |

All paths in this table without a prefix resolve under `D1/fix-d1-h-1/`. The full revised result is `RESULT.md`.

## What was rerun

Only the changed verification derivations: `recompute.py` generates revised sample decisions, whole-table extent searches, established membership, UNKNOWN ids and summaries into this new directory. The same ordered draws are checked, never replaced. Original metrics are retained from the already verified statistics; no VM or removal/inventory probe was run.

`input-sha256.json` covers 1,668 frozen input/evidence files. (not published: external working record) records the counts and successful unchanged-hash check. Exact quote validation of the updated result and this response is saved in (not published: external working record) and (not published: external working record).

## Limits retained rather than repaired

The established extent is an enumerated set, not a claim that all broad kind/name matches are proved negative. `extent-search.tsv` has 920 unresolved row/card search memberships; these are neither extra confirmed rows nor automatically UNKNOWN objects. Existing factual accounts, rather than new package investigations, supply the unaffected payload evidence. The text alone must decide the four remaining gaps; no wording or rule has been added to it.

The prior verification's procedural breach remains in the record. The correction records it and does not certify the old evidence as newly obtained within scope. Independent acceptance remains with the next review.

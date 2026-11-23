# Independent review of FX-A3R-H-2

**VERDICT: ACCEPT**

Review date: 2026-11-22 UTC. Reviewed (not published: outside selected checks and direct evidence), (not published: orchestration and working notes), (not published: orchestration and working notes), `../REVIEW-A3R-H-2.md`, the corrected `../RESULT.md`, `../FIX-A3R-H-2.md`, and the round-2 source, inventory-search, ledger, count and validation artifacts. The correction writer was not run during this review.

## Finding 1 — fixed

An independent parse of (not published: over 20 MB: raw trace, snapshot, index or operational log) finds 67 regular enablement markers after excluding the `.dsh-also` lists: 56 under the system-instance root and 11 under the user-instance root. These paths match `helper-witnesses.tsv` exactly.

The exact-version source in `raw/helper-source.txt` defines the user-instance enabled-state root at lines 100–102, selects it for user units at lines 576–579, and passes both instance roots through the same marker branch at lines 354–375. That branch checks marker existence before link creation and describes each marker as the stored fact that enablement ran. The user-instance markers therefore have the same simultaneous S2.2-6 and S2.2-1 functions as the previously counted system-instance markers.

An independent whole-table search of all 5,212 `joined.tsv` rows produces 26 card-9 memberships. The previous 21 are retained and exactly these five rows are added:

| ID | Name |
|---|---|
| `44ecaacc91e376e873a2b925` | `/var/lib/systemd/deb-systemd-user-helper-enabled` |
| `60af4555f895a621f8fdd8b5` | `/var/lib/systemd/deb-systemd-user-helper-enabled/default.target.wants` |
| `296089dc9d4776765bdfe6b3` | `/var/lib/systemd/deb-systemd-user-helper-enabled/graphical-session-pre.target.wants` |
| `4c799fa72ea8014675516c7b` | `/var/lib/systemd/deb-systemd-user-helper-enabled/graphical-session.target.wants` |
| `3dbad18363c3236ada19e5bb` | `/var/lib/systemd/deb-systemd-user-helper-enabled/sockets.target.wants` |

The four `.wants` groups contain 1, 1, 1 and 8 regular marker files respectively; the parent group represents those marker-bearing directories. `helper-search.tsv` has one record for every `joined.tsv` row and its ID, kind and name columns match the source table in order. Its 26 confirmed IDs match the independently selected IDs and card 9 of `code_extent.tsv`.

Cards 1 and 7 in the new ledger match their round-1 rows field for field. Their 116-row union has no overlap with card 9, so the corrected total is 142 distinct rows. The reported 26-row card-9 extent and 142-row total are correct.

## Finding 2 — fixed

The introduction to “Cards that did not survive” now limits the support claim to the listed Section 2.2 and Section 3 sentences and states that S2.5-1 is quoted only to explain why the cards are not OUTSIDE. It explicitly says S2.5-1 supplies neither a recording exemption nor a refutation. This removes the contradictory wording without changing a disposition or adding a rule.

## Validation

All 1,066 frozen-file digests in `frozen-inputs.sha256.json` match. The corrected result retains the required first line, reports no published-check outcome, and keeps the undecided conflict as a hole. The quote check independently reports 14 quotations checked and none missing from `../../TEXT.md`. The round-2 diff is limited to the two reviewed findings and their derived links and totals; no sample, text, failure condition or prior disposition changed.

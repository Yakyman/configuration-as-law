# Part (b): findings 7–12 for fix round 1

Recorded 2026-11-23 13:27:55 UTC. Supporting correction analysis, not independent acceptance. Read (not published: orchestration or scratch) first, then the assigned task, fixed text, sentence inventory, supplement, argument, questions, original part (b) and review. No probes, machines, external search or additional cases. Proposed part (b) outcome remains **?**.

## Finding 7: retain, with the existing scope qualification

B0 and B1 have a determined declaration, and the snapshot/current-source readings agree on {account-A}. This does not establish complete source-only semantics. B2 remains reading-dependent under the committed rule in `SUP1/step-3.md`. The source states and last received list are stipulated in `S3/ARGUMENT.md`, part (b), and `S3/raw/part-b.md`, “Fixed facts and what is not a fact”; neither a missing observation nor an additional refresh is needed to distinguish the requirements.

S8.1-12: “The required state of a recorded object is stated by its line.”

S8.2-18: “A line may take a list from outside the declaration, for example accounts from an organisation’s server; in that case, what counts as recorded is the source named in the line.”

These sentences leave the recorded reading question: does the permitted source-only line already supply a complete requirement, or must its defined meaning supply further semantics? Neither source naming nor the Section 8.4 consequence supplies an explicit temporal selection. Adding a provenance reading does not settle the competing current-source reading. No universal contradiction follows.

## Finding 8: fix the omission; qualify the proposed example

The omission is real. `S3/ARGUMENT.md`, refutation 3, and `S3/QUESTIONS.md`, question 2, already identify provenance as a candidate reading, while the B2 alternative-state table has only two rows. Add the third row without adopting it as the rule:

| Reading of L at the same B2 moment | Required contributed account state | Does the stipulated retained {account-A} meet that list requirement? | Difference for the person using the computer |
|---|---|---|---|
| Any list obtained from R, without a freshness requirement | Any list actually obtained from R; the retained {account-A} qualifies | Yes | account-A may remain; this reading does not require replacing it with account-B. |

Suggested adjacent clarification: “The provenance reading permits a list because it was obtained from R, rather than because it is current. In the fixed history only {account-A} is stipulated to have been received. {account-B} would satisfy that provenance condition if obtained from R; no such receipt or local availability is asserted at B2. The table compares candidate requirements for the same retained state and does not add a refresh or require a unique permitted list.”

The review's wording “{account-A} or {account-B} both acceptable; the person may see either account” is too strong if read as an assertion about actual provenance or local availability in this history. The fixed premises explicitly say that the last received list and actual local accounts remain {account-A}. The mere fact that R currently contains {account-B} does not prove that this list was obtained by the computer. The proposed qualification corrects the omission without changing those premises. Both states can be named as abstract alternatives under a condition on provenance; they must not both be represented as established local possibilities.

Suggested refutation-3 replacement for its final sentence: “If the source-only line itself means mere provenance, the retained list qualifies because it was obtained from R; a later list qualifies on that reading if it too is obtained from R. This is another reading requiring author resolution, not a policy adopted here.”

Suggested B2 disposition addition: “The provenance reading accepts the retained {account-A} without a freshness requirement.” The source-only validity question and **?** remain.

## Finding 9: retain the outcomes; update their stated basis

The first line remains `STEP 3: (a) ?; (b) ?`. For part (b), current-source semantics reject the retained list, while snapshot and provenance semantics accept it; a choice between readings remains, irrespective of whether some readings allow multiple lists. `SUP1/step-3.md` explicitly assigns ? to that situation. This analysis neither certifies an unconditional gap nor silently selects provenance to produce 1. Findings 1–4 require separate changes to the part (a) explanation.

## Finding 10: historical verification, not a current count

The review reports six input hashes, 38 checked quotations, 18 distinct ID–quote pairs, 16 moment rows and 3909 words for its reviewed version. This supporting analysis has not independently rerun those checks. A changed argument will have new counts and must have a fresh verification record in the new output location. Preserve the old record; do not present its word or quote count as a check of the corrected document. Adding an alternative-state row does not itself add a moment row or a case.

## Finding 11: retain the part (b) support; preserve the qualification

The cited account classification and force definitions support the distinction between account existence and successful login. S8.1-11: “A service is in force if it is enabled; an account, if it exists.” S8.2-13 explicitly includes accounts, rights, access rules and permitted login means as settings. The two quoted Section 8.4 statements are in `TEXT.md`; they address source identification and excluded reproducibility, not a freshness condition. The report-separation qualification belongs to the part (a) correction and must not be erased by this finding's verified sample.

## Finding 12: preserve original scope; distinguish this correction

The review's scope statement concerns the original work. This part adds textual reasoning only and writes only this file in the new output location. No empirical rerun is warranted because no system-behavior premise changed. Do not infer that a new independent review has accepted the corrected argument from the original scope verification.

## Integration checklist

- Add the provenance row and qualification; align refutation 3, B2 and question 2 to avoid asserting receipt of {account-B}.
- Keep the fixed history, source facts, events, published sentences and failure conditions unchanged.
- Keep both outcomes ?, while updating the part (a) reasons separately.
- Recheck the changed argument and record fresh results separately from the frozen records.

# FBQ1 — review round 1 dispositions, 2026-11-19

Read-only source audit: one separate step of the same executor, as required by the shared rules of the checks. This is not the independent review. Outputs: this record, corrected Q-RESULTS/Q-STAND/Q-CLASSIFICATION, STAND navigation pointer, and new evidence under `B/raw/q-fix-1/`.

**Outcomes: Check 2 ?, Check 3 ?, Check 4 ?, Check 5 ?.** The earlier Check 4 `1` is withdrawn. PAPER and PROTOCOL/failure conditions are unchanged. No classification rule is added; undecided cases remain holes.

| Q-REVIEW-1 finding | Disposition | Correction / reason and evidence |
|---|---|---|
| 1 — caller assigns HOME; Check 4 pass unsupported | **Fixed adjudication/wording; runtime defect not fixed.** | Accept the reviewer's minimal correction. Check 4 returns to **?**: `check-real-lifecycle.py:26–27` supplies browser HOME/XDG/profile and Vim HOME/history; `check-day.py:16–18` does likewise. `cal-login.c` enters AppArmor/Bash, and final policy permits original application paths without enforcing these homes. Package-group removal is real, but ordinary-launch tracking is not shown repaired. Keep the 94 raw passing assertions as fixture evidence, not acceptance. [Reanalysis](raw/q-fix-1/run-2/lifecycle-adjudication.jsonl), [historical survivors](../../check-2-law/stand/raw/fb1/check-browser-lifecycle.jsonl). No new VM run or repaired launcher is claimed. |
| 2 — outside-state scan covers only home | **Fixed claim; comprehensive scan not implemented.** | The original labels at `lifecycle-v3.jsonl:31,113` are too broad. Correct interpretation: no added/changed regular-file or symlink entries under `/home/alice` except the document, with relative `version` excluded. The source compares only after entries, so it also misses deletions, directories/metadata and transient state. `/tmp`, `/var/tmp`, `/dev/shm` are writable in the final policy and not inventoried here. We do not infer `/run/user/1000` access from an example in the review. [Scope/source audit](raw/q-fix-1/run-2/audit.json). Frozen labels are retained; current reports explicitly supersede them. |
| 3 — missing Q-FIX record | **Fixed.** | This file records all eight dispositions. Q-STAND and Q-RESULTS link here. |
| 4 — STAND stale/no pointer | **Fixed.** | Added a historical/supersession pointer at the top of STAND; its prior body is unchanged. BQ1 mechanisms/results are reached through Q-STAND/Q-RESULTS and this correction. Prior report bytes are in before/. |
| 5 — Check 2 ? consistent | **Not changed; finding accepted.** | O5 remains unresolved, virtual radio results do not cover real hardware, O4 and coverage limits remain. Audit reconfirms radio delivery and interpreter markers without changing their classes. [Audit](raw/q-fix-1/run-2/audit.json). Workday wording now also discloses caller-supplied state paths. |
| 6 — Check 3 ? and counts consistent | **Not changed; finding accepted.** | Audit reconfirms counts and 324 inherited + 777 additional package records per machine. Kernel tasks remain 68/69; no new normalization or component-identity rule. [Audit](raw/q-fix-1/run-2/audit.json), [original summary](../../check-3-reproducibility/stand-pair/raw/q/repro/summary.json). |
| 7 — Check 5 ?; conditional P7 consequence | **Fixed wording; outcome unchanged.** | Q-RESULTS question 2 now states both conditional consequences: an undeclared-execution right would conflict with P1/P4 and yield 0 under §9.1; a right exercised through declaration does not fire this clause in this case. Neither scope is selected. The personal ELF path succeeds; the sole listed failure remains `no-lists-unix-execute-own-file`. [Authority evidence](../../check-5-authority/stand/raw/q/authority/final-owner-authority.jsonl), PAPER lines 140/143/146/171/214/243. |
| 8 — five cited claims confirmed | **Not changed; finding accepted with scope correction.** | Original counts remain 94/94 real lifecycle and 102/102 shared; authority retains 54 command rows and its one listed failure. Radio delivery, actual update and O5 markers are reconfirmed. Those observations do not repair finding 1. No change is needed for the separate Python import wording. [Audit](raw/q-fix-1/run-2/audit.json). |

## What was rerun and what remains

Only adjudication, claim scope and documentation changed. Reanalysis reruns the frozen-log counts, home-change interpretation, source-scope extraction, cited markers, links and integrity checks. It does **not** execute applications, simulate a new VM lifecycle run or infer unobserved filesystem contents. Command from the working directory:

```sh
python3 B/raw/q-fix-1/audit.py B/raw/q-fix-1/run-2
```

New results: [audit.json](raw/q-fix-1/run-2/audit.json) and [lifecycle-adjudication.jsonl](raw/q-fix-1/run-2/lifecycle-adjudication.jsonl). The script requires a previously nonexistent destination. All **529 frozen files** in the input manifest are checked unchanged, including PAPER, PROTOCOL, source procedures and previous raw outputs. Pre-correction report copies preserve the withdrawn claims. The historical `raw/q/verify.py` was not rerun: it would write frozen `verification.json` and still assert Check 4 = 1.

The first audit attempt stopped at an audit-only formatting mistake: it expected a space in serialized package-version output, while decoded stdout uses a tab. Its failure record, partial reanalysis and exact script are preserved. The corrected script parses JSON stdout; the successful attempt uses the new `run-2` directory. This failure does not change any VM observation or hypothesis outcome.

Ordinary-launch placement and an adequate outside-state census remain **a**, not textual questions. They are not repaired by narrowing the report. O1/O2/O4/O5/O7/O9 and P7 scope remain undecided where the definitions leave them open. A future stand repair needs evidence from launches without caller-supplied placement, both archive settings, rollback and shared-owner handling; no present result assumes that work succeeded. This is a coverage requirement for that proposed repair, not a change to §9.5.

No VM, server job or disposable disk was created; no system change or installation occurred. The source audit confirms findings 1/2/7 but was run by the same executor.

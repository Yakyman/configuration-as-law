# Final saved-evidence review

Recorded 2026-11-23 UTC, after the main summary at 16:56:44 UTC. Internal engineering
review only, not external case execution or acceptance. No guest probes, evidence
rewrites, sealed-input changes or audit expectation changes were made. The reviewer
authored the audit tools; this report independently recounts selected raw records
but does not claim independent acceptance of those tools.

## Result and scope

The full audit is structurally consistent but incomplete: `regression-audit.json`
reports no errors and one missing entry containing 60 original code/lifecycle
assertions. Its CLI status maps to exit 2. The original raw traceback shows
`os.mkfifo` at line 176 failing with errno 30 after 73 passing observations.
The separate continuation supplies 59 further passing observations, with four
successful setup operations excluded and SEALED-FIFO explicitly NOT-TESTED.
Raw ID recount gives 132 distinct observed assertions, all passing. The original
run still lacks its entire 60-observation suffix and remains failed/incomplete.
Across the disclosed split execution, the unavailable case is FIFO alone.

| Evidence under `B2/raw/round-3/` | Confirmed observation |
|---|---|
| `regression-audit.json` and five referenced component logs in `final-1-validation/` | 19 false records: objects 3, shell 6, native-account old reader 1, direct supplement 5, extra supplement 4; exact ID/file sets agree with raw records |
| Same audit and raw records | Seven UNTESTED records: INTERNAL-CODE-CAPABILITIES, EDITOR-PLUGIN-MODELINE, GIT-HOOK, GIT-LOCAL-ALIAS-FILTER, MAKE-SAVED-RECIPE, FOREIGN-INTERPRETER, BROWSER-EXTENSION |
| `final-1-validation/summary.json`, `whole-suite-ledger.json` | Main exit 1; components 0, round3 1, round4 0; no remaining VM or peer |
| `final-1-validation/carried-suite/regressions/round2.jsonl` | 73/73 observed assertions pass, then FIFO setup traceback; no completed suite summary |
| `final-1-continuation/suffix.jsonl`, exported observations, `continuation-audit.json` | 59/59 planned suffix assertions; setup 4/4 separately marked; one NOT-TESTED FIFO; no earlier test-ID repetition |
| `final-1-continuation/summary.json` | Continuation controller exit 0; owned guest absent |
| `final-1-validation/carried-suite/regressions/powercuts.jsonl` | Nine expected, nine cut and nine result records; all nine results pass |
| `final-1-validation/combined/events.jsonl`, `combined/summary.json`, four verify logs | 24/24 assertion events; both snapshots complete; 584 original-reader rows on both sides before/after reboot; combined exit 0 and no owned guests |
| `final-1-validation/cases.jsonl` | Exactly 17 case-result records, all pass; fixture/setup Boolean records are not counted as additional cases |
| `final-1-validation/cases-filesystem-verify.jsonl` | 1,379 paths checked, no reported failures |

Other carried counts in the saved audit: language 79/79, applications 131/131,
system 32/32, ordinary 59/59, transaction 35/35, authority/frontend 166/166.
Objects contain 37 pure rule observations plus 52 machine observations, with
three machine false results; the aggregate is 86/89. Gate is 9/9; shell 22/28;
tools 85/86; direct supplement 12/17; extra supplement 12/16. These historical
false records are preserved without reclassification. The primary seven UNTESTED
records are separate from the continuation's one unavailable FIFO record.

The inherited independent-peer and combined comparisons concern original machine
declarations and original reader rows. They do not compare the five added
filesystem declarations or the eight-file complete declaration bundle. Neither
these finite passes nor the 17 builder case results constitute external acceptance
or a universal P1/P2/P4 finding. The required full original regression did not
complete; the separate continuation mitigates the missing evidence without
rewriting that fact.

## Reviewed audit identities

- `regression-audit.json`: SHA-256 `cce56087433e623a0e13bb38f6a03c4062d0e73d468324a74250f73b3e0099f1`.
- `continuation-audit.json`: SHA-256 `20ca37311fb99e3a1e3d509fa0395d91e9a186bef12e00cb887cd46cf9c619c3`.
- `final-cases-audit.json`: SHA-256 `e6df88b2a3b9b55382d467c891dc17dfd060bd9501c88d79f8188ee146f0adb9`.

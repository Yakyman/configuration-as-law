STEP 7: the way of sorting 0; part 1: 8 of 10 same, 6 of 10 known; part 2: 2 of 10 known answers accepted, 10 of 10 opposite answers rejected

This step runs under the first of the two readings recorded in [SUP1/step-7.md](../SUP1/step-7.md): the weighting of Section 2 of [PROTOCOL.md](../PROTOCOL.md), rather than the procedure of Section 3. Its outcome holds only for that reading. The known answers and the comparison rule are fixed in `SUP1/step-7.md`, using the table of Section 8.6 of [TEXT.md](../TEXT.md). Sections 8 and 9.2 of `TEXT.md` and Sections 2–4 of `PROTOCOL.md` are the stated context; no new decision about what the definition should mean is made here.

## Part 1: the two parties' answers

Sources: cases 1–10 of [S7/CASES.md](CASES.md); the corresponding `case` rows of [S7/m1/answers.tsv](m1/answers.tsv) (c1) and [S7/m2/answers.tsv](m2/answers.tsv) (c2). Q1 reproduces `by_meaning`; Q2 reproduces `without_forbidding`. A Q2 answer of `yes` means the requirement can be met without forbidding a listed ordinary action. The comparison uses the stated answers, including the covering lines they name; conditional alternatives in the `reason` fields do not replace those answers.

| Case | c1 Q1 | c2 Q1 | Same Q1? | c1 equals known? | c2 equals known? | c1 Q2 | c2 Q2 |
|---|---|---|---|---|---|---|---|
| 1 | yes: covered by the line of the package that supplied it | yes: covered by the line of the package it came with | Yes | No | No | yes | yes |
| 2 | yes: covered by the line of the package that supplied it | yes: covered by the line of the package it came with | Yes | No | No | yes | yes |
| 3 | yes: own line | yes: own line | Yes | Yes | Yes | yes | yes |
| 4 | yes: covered by the line of the package that supplied it | yes: covered by the line of the package it came with | Yes | Yes | Yes | yes | yes |
| 5 | no | yes: covered by the line of the object it is rebuilt from | No | Yes | Yes | yes | yes |
| 6 | yes: own line | yes: own line | Yes | Yes | Yes | yes | yes |
| 7 | yes: covered by the line specifying its source or build | yes: covered by the line of the program whose code it compiles | No | No | No | yes | yes |
| 8 | yes: own line | yes: own line | Yes | Yes | Yes | yes | yes |
| 9 | no | no | Yes | Yes | Yes | yes | yes |
| 10 | yes: own line | yes: own line | Yes | Yes | Yes | yes | yes |

Application of the rule in `SUP1/step-7.md`:

- Cases 1 and 2: the two phrasings name the same supplying-package coverage. The known answer permits a line of the object's own or coverage as a dependency of a recorded package. Neither party's stated answer names either of those alternatives: coverage by the supplying package does not state that the object is a dependency of a recorded package. Both therefore fail the specified known-answer comparison. This does not adjudicate either party's interpretation of Sections 8.1–8.5.
- Cases 3, 4, 6 and 10: the comparison rule explicitly allows any `yes`, so both parties equal the known answer.
- Case 5: `no` and `yes: covered by the line of the object it is rebuilt from` are different answers to Q1. Both nevertheless equal the known answer under the special rule for this case: neither requires a line of the object's own. Equality to the known answer does not make these two Q1 answers the same.
- Case 7: c1 names a line specifying the copy's source or build; c2 names the line of the program whose code it compiles. These are different named-line answers: the first permits a source or build line without identifying it as the second party's program line. Neither names the line of the original package specified by the known answer. No identification of these lines with one another or with an original package line is added.
- Case 8: both require a line of its own, as the known answer does. Case 9: both answer `no`, as the known answer does.

The parties give the same Q1 answer in **8 of 10** cases: 1, 2, 3, 4, 6, 8, 9 and 10. In **6 of 10** cases that shared answer equals the known answer: 3, 4, 6, 8, 9 and 10. The first-line count of known answers is this shared-answer count, as in the expected-result sentence of `SUP1/step-7.md`. Separately, each party equals the known answer in **7 of 10** cases: 3, 4, 5, 6, 8, 9 and 10. Both parties answered both questions for every case; none is counted as a disagreement because of a missing answer. All twenty Q2 answers are `yes`.

## Part 2: the third party's verdicts

Sources: join by `pair` of [S7/PAIRS.tsv](PAIRS.tsv), [SUP1/step-7-key/key/KEY.tsv](../SUP1/step-7-key/key/KEY.tsv) and [S7/j/verdicts.tsv](j/verdicts.tsv). Every pair's case number agrees across the three files. Each case has one `known` pair and one `opposite` pair. Labels and verdicts below are reproduced unchanged; a `reject` remains a rejection even when its reason names an unknown fact.

| Pair | Case | KEY label | Third-party verdict | Known answer rejected? | Opposite answer accepted? |
|---|---|---|---|---|---|
| 1 | 4 | opposite | reject | No | No |
| 2 | 6 | opposite | reject | No | No |
| 3 | 3 | known | accept | No | No |
| 4 | 5 | opposite | reject | No | No |
| 5 | 6 | known | accept | No | No |
| 6 | 9 | known | reject | Yes | No |
| 7 | 2 | opposite | reject | No | No |
| 8 | 8 | known | reject | Yes | No |
| 9 | 1 | opposite | reject | No | No |
| 10 | 1 | known | reject | Yes | No |
| 11 | 10 | opposite | reject | No | No |
| 12 | 7 | known | reject | Yes | No |
| 13 | 4 | known | reject | Yes | No |
| 14 | 7 | opposite | reject | No | No |
| 15 | 5 | known | reject | Yes | No |
| 16 | 2 | known | reject | Yes | No |
| 17 | 9 | opposite | reject | No | No |
| 18 | 3 | opposite | reject | No | No |
| 19 | 8 | opposite | reject | No | No |
| 20 | 10 | known | reject | Yes | No |

Known answers accepted: **2 of 10**, pairs 3 and 5 (cases 3 and 6). Known answers rejected: **8 of 10**, pairs 6, 8, 10, 12, 13, 15, 16 and 20 (cases 9, 8, 1, 7, 4, 5, 2 and 10). Opposite answers rejected: **10 of 10**, pairs 1, 2, 4, 7, 9, 11, 14, 17, 18 and 19. Opposite answers accepted: **0 of 10**.

These numbers are reported as they are. Under the rule in `SUP1/step-7.md`, nothing in part 2 counts for or against the way: this part has one party judging supplied answers and is not the way of Section 2 of `PROTOCOL.md`.

## What counts against the way, and the outcome

The following applies only the two conditions under “What counts against the way” in `SUP1/step-7.md` to the part 1 rows above.

| Case | Counts against the way? | Application of the rule |
|---|---|---|
| 1 | Yes | The same Q1 answer is not the known answer: supplying-package coverage instead of either permitted line. |
| 2 | Yes | The same Q1 answer is not the known answer: supplying-package coverage instead of either permitted line. |
| 3 | No | The same Q1 answer equals the known answer. |
| 4 | No | The same Q1 answer equals the known answer under the any-yes rule. |
| 5 | Yes | Different Q1 answers, although both equal the known answer under the special no-own-line rule. Neither answer is missing. |
| 6 | No | The same Q1 answer equals the known answer. |
| 7 | Yes | Different named-line Q1 answers; neither equals the known original-package answer. Neither answer is missing. |
| 8 | No | The same Q1 answer equals the known answer. |
| 9 | No | The same Q1 answer equals the known answer. |
| 10 | No | The same Q1 answer equals the known answer. |

**Outcome: 0 for the way of sorting**, because cases **1, 2, 5 and 7** count against it in part 1. This follows from the outcome rule in `SUP1/step-7.md`: any such case gives 0. All cases have answers, so there are no unanswered cases to report. No gap is placed in a list of gaps in the wording or gaps in the idea in this step.

## Comparison with the expected result

Each expectation below is unchanged from “Expected result, written before the work” in `SUP1/step-7.md`. The shared-known count uses “this answer” from that sentence, not the separate counts for each party.

| Expected result | Observed result | Met? |
|---|---|---|
| In part 1, the two parties give the same answer in at least eight cases of ten. | 8 of 10: cases 1, 2, 3, 4, 6, 8, 9 and 10. | Met |
| In at least seven cases, this shared answer is the known one. | 6 of 10: cases 3, 4, 6, 8, 9 and 10. | Not met |
| In part 2, the third party accepts at least eight of the ten known answers. | 2 of 10: pairs 3 and 5. | Not met |
| In part 2, the third party rejects at least eight of the ten opposite answers. | 10 of 10: pairs 1, 2, 4, 7, 9, 11, 14, 17, 18 and 19. | Met |

These expectations decide no outcome and are not thresholds. They have not been adjusted to the observations.

The half of step 7 about cases known to be wrong **was not attempted**, as specified in `SUP1/step-7.md`, which records that the published text names no such cases for this way. This outcome concerns only the way of sorting under the first reading; it is not an outcome for the hypothesis or for any check or other step, and changes no outcome of a check or of another step. The designated independent review of this result is RV-S7-R.

# Classification summary

All three input tables are complete. The fixed PAGE.md was not changed.

## Status

| status | D1 | A1 | A3R | Total |
|---|---:|---:|---:|---:|
| DECIDED | 847 | 398 | 1272 | 2517 |
| NOT_DECIDED | 20 | 38 | 0 | 58 |
| TWO_WAYS | 271 | 194 | 77 | 542 |
| FACT_UNKNOWN | 352 | 389 | 174 | 915 |
| MIXED | 353 | 65 | 487 | 905 |
| Total | 1843 | 1084 | 2010 | 4937 |

## Kind

| kind | D1 | A1 | A3R | Total |
|---|---:|---:|---:|---:|
| PROGRAM | 106 | 28 | 82 | 216 |
| SETTING | 225 | 27 | 115 | 367 |
| PROGRAM_RECORD | 15 | 0 | 12 | 27 |
| MATERIAL | 491 | 16 | 5 | 512 |
| PACKAGE_PART | 0 | 61 | 948 | 1009 |
| BUILT | 13 | 266 | 110 | 389 |
| ACTION | 0 | 0 | 0 | 0 |
| NONE | 993 | 686 | 738 | 2417 |
| Total | 1843 | 1084 | 2010 | 4937 |

## Recording

| record | D1 | A1 | A3R | Total |
|---|---:|---:|---:|---:|
| YES | 326 | 55 | 197 | 578 |
| COVERED | 13 | 327 | 1058 | 1398 |
| NO | 709 | 118 | 78 | 905 |
| NA | 795 | 584 | 677 | 2056 |
| Total | 1843 | 1084 | 2010 | 4937 |

Number of homogeneous script rules: **41** (D1: 16; A1: 10; A3R: 15). Each has ten manually checked examples in RULES.md.

CASES-ANSWERS.md covers all fifteen numbered cases and separates their distinct situations. HOLES.md groups all NOT_DECIDED and TWO_WAYS table rows; holes-members.tsv gives their complete membership.

FACT_UNKNOWN is not a textual defect: it includes missing payload/selected-member contents, unestablished provenance, executable compatibility and sandbox capabilities. A raw listing of all descendants was not assumed to equal an omitted selected-member list. Files referenced outside the permitted roots were not opened.

Validation checks exact headers, one output for each input ID, identical counts and ID sets, uniqueness, allowed kind/record/status values, PAGE sentence IDs, basis syntax and the 15/30-word limits. It also checks ten valid sample IDs per script rule, the gap-index partition, and all fifteen case numbers. The check results and output hashes are in validation.json.

This is a draft classification with mechanical validation and recorded manual checks; no independent substantive acceptance by another reviewer is claimed.

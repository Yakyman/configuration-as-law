# Classification summary

The actual inputs contain D1 1840, A1 1084 and A3R 2010 rows: 4934 total. The D1 count stated in the task (1843) differs from its supplied table; no missing rows or IDs were invented.

## Status counts

| Table | Total | DECIDED | NOT_DECIDED | TWO_WAYS | FACT_UNKNOWN | MIXED |
|---|---:|---:|---:|---:|---:|---:|
| D1 | 1840 | 759 | 0 | 0 | 1074 | 7 |
| A1 | 1084 | 549 | 0 | 0 | 495 | 40 |
| A3R | 2010 | 255 | 0 | 0 | 1751 | 4 |

## Counts by kind

| kind | D1 | A1 | A3R | Total |
|---|---:|---:|---:|---:|
| INSTALLED | 1408 | 432 | 48 | 1888 |
| PROGRAM | 0 | 26 | 5 | 31 |
| SETTING | 72 | 147 | 40 | 259 |
| PROGRAM_RECORD | 14 | 150 | 121 | 285 |
| MATERIAL | 0 | 1 | 0 | 1 |
| RUNTIME | 338 | 48 | 68 | 454 |
| ACTION | 0 | 0 | 0 | 0 |
| NONE | 8 | 280 | 1728 | 2016 |

## Counts by record

| record | D1 | A1 | A3R | Total |
|---|---:|---:|---:|---:|
| YES | 3 | 26 | 0 | 29 |
| COVERED | 405 | 322 | 53 | 780 |
| NO | 352 | 204 | 202 | 758 |
| NA | 1080 | 532 | 1755 | 3367 |

## Script rules and validation

26 script rules: D1 5; A1 8; A3R 13. Each rule has ten manually checked IDs in RULES.md. Other decisions are individually entered. Classification scripts append missing IDs; documented corrections replace dispositions from this same run.

(not published: trial helper scripts) checks exact input/output ID sets, counts, uniqueness, the exact eight-column header, allowed kind/record/status words, sentence IDs, field word limits, and required reports before writing DONE.

## Independent review and read-boundary incident

The classifier did not accept its own work: an independent reviewer inspected rules, samples and cases; accepted corrections were applied. REVIEW.md records findings and any bounded disagreements.

The reviewer mistakenly opened A1 raw nixos/system-closure.txt, which was not referenced by any evidence column. This violated the requested read boundary; the incident is explicitly retained in REVIEW.md. That unreferenced content was excluded from all classification support, and all 122 affected Nix coverage claims were changed to FACT_UNKNOWN. Thus the run cannot claim flawless clean-room execution even though final Nix decisions do not rely on that file.

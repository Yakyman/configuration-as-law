CHANNELS: 53 decided, 0 not decided, 8 two ways, 27 fact unknown

FX-B1-1 revision. The current classification, gaps and primary excerpts are in [fix-b1-1/](fix-b1-1); the original CHANNELS-V4.tsv, GAPS.md, SOURCES.md, raw outputs and reviews are preserved. The original result is [fix-b1-1/inputs/RESULT-before.md](fix-b1-1/inputs/RESULT-before.md). Finding-by-finding disposition: [FIX-B1-1.md](FIX-B1-1.md).

All 88 identifiers and names remain in their original order: 76 C rows and 12 M rows. This remains the separate, unweighted investigation under PROTOCOL.md Section 5. No planned-check outcome, system-feasibility verdict, or gap weight is assigned.

Counts are nonexclusive row counts for described objects and explicitly classified branches, including both textual readings and factual alternatives. Generic hypothetical rules, unidentified additional outputs, and the twelve M rows' generic kind rules are excluded. Exact membership and the one kind-membership correction are in [counts.json](fix-b1-1/raw/counts.json) and [kind-count-method.md](fix-b1-1/raw/kind-count-method.md).

## Counts per route

| Route | Rows |
|---|---:|
| Installer | 22 |
| Other built-in tool | 25 |
| General-purpose program without superuser rights | 53 |
| Privileged change past the declaration outside built-in tools | 7 |
| Acting route not established | 16 |

Installer is separate from other built-in functionality. The five C5 rows count both route readings. C3.5 counts the established mount route and an unknown updater route; C4.3 no longer asserts a built-in updater. Root use of a built-in tool is not itself breaking (S8.1-15).

## Counts per kind

| Kind | Rows |
|---|---:|
| Installed object | 37 |
| Program | 54 |
| Setting | 29 |
| Program record | 20 |
| Material | 7 |
| Exists only while the computer runs | 51 |

The runtime category follows S8.2-5 and is not an additional separate-object class. C7.07 is counted only as Program and runtime; its hypothetical installed-package alternative is excluded. History contributes both textual readings. C7.19 remains code at Q2, with the S8.2-21 recording exemption.

## Kinds of gap

- **Home-page navigation and launching something** — C8.08: setting with its own line versus program record requiring none.
- **Compiler and build-tool purpose versus general-purpose work** — C5.1, C5.2, C5.3, C5.4, C5.5: built-in versus general-purpose route; output recording is required under both readings, but the tool-specific recording duty differs.
- **Saved history: values read versus executable statements** — C7.06, C7.17: program record requiring no line versus program requiring a line.

All eight gap rows are TWO_WAYS; none is NOT_DECIDED. [GAPS.md](fix-b1-1/GAPS.md) gives exact quotations and the declaration/system-behaviour consequences without choosing a reading or proposing a text change.

Evidence: [CHANNELS-V4.tsv](fix-b1-1/CHANNELS-V4.tsv), [SOURCES.md](fix-b1-1/SOURCES.md), [cell changes](fix-b1-1/raw/changes.json), [validation](fix-b1-1/raw/validation.txt), and [quotation checks](fix-b1-1/raw/check-quotes.txt). Only affected rows and dependent aggregates were regenerated; no runtime experiment was repeated. Original inputs and artifacts are hash-checked in validation. Independent acceptance of this revision is pending; the preserved reviews concern the earlier result.

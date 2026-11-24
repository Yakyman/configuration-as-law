CHANNELS: 59 decided, 0 not decided, 1 two ways, 28 fact unknown

All 88 identifiers and names are preserved in original order: 76 C rows and 12 M rows. This is the separate, unweighted investigation under PROTOCOL.md Section 5; it makes no system-feasibility verdict and adds no weighted failure to the planned checks.

Counts below are nonexclusive row counts: a composite variant may contain several routes and kinds. Explicit alternatives are included; therefore columns need not sum to 88. The twelve M rows identify cross-channel obligations without an actual tool or artifact inventory; their generic classification rules are not counted as established object kinds. Unknown extra outputs in other rows are likewise excluded. Exact row membership is saved in raw/counts.json.

## Counts per route

| Route | Rows |
|---|---:|
| Installer | 22 |
| Other built-in tool | 26 |
| General-purpose program without superuser rights | 53 |
| Privileged change past the declaration outside built-in tools | 7 |
| Acting route not established | 14 |

Installer is counted separately from other built-in functionality, although S8.1-7 includes installers among built-in tools. Breaking is counted only for the explicitly described privileged, outside-tool, past-declaration branch; root use of a built-in tool is not breaking.

## Counts per kind

| Kind | Rows |
|---|---:|
| Installed object | 38 |
| Program | 54 |
| Setting | 29 |
| Program record | 20 |
| Material | 7 |
| Exists only while the computer runs | 51 |

The runtime category follows S8.2-5 and is not an additional separate-object class. The kind counts include known parts and expressly classified alternatives of FACT_UNKNOWN rows, as well as both readings of C8.08; they are not counts of observed installations.

## Kinds of gap

- **Home-page navigation and launching something** — C8.08 (TWO_WAYS): the saved home-page URL is either a setting requiring a line or a program record requiring none, depending on the meaning of launching something in S8.2-14. See GAPS.md for the two declaration and system-behaviour consequences and exact quotations.

No NOT_DECIDED rows. The other incomplete rows identify missing tool/artifact facts in their status and reason cells; no missing implementation mechanism from Section 8.5 is counted as a gap.

Evidence: CHANNELS-V4.tsv contains each row's facts, ordered decisions, required coverage, route and exact law quotations; SOURCES.md supplies short primary excerpts. The quotation check output is raw/check-quotes.txt; the independent review is review.md.

# Validation of FX-A1-H-1

Date: 2026-11-22 UTC. Validation command: `/usr/bin/python3 -I A1/fix-a1-h-1/validate.py`. Detailed results: `raw/validation.json`; quote-check output: `raw/quote-check.log`.

- All 531 frozen input/review files match the before-fix SHA-256 manifest in `raw/frozen-input-sha256.json`.
- The 40 resolved and 60 agreed audit IDs and their order are unchanged; no sample was redrawn.
- The changed extent and audits were recomputed by `recompute.py`, with arithmetic assertions; `raw/recompute.log` records 114 established H1 occurrences, 243 factual unknowns and 522 reading-dependent inventory units.
- All 598 affected unit rows have a record. State lookups respect system/user manager scope; 21 conditional file readings establish a second applier. The other 577 do not establish presence or absence of a second applier.
- Result/fix local Markdown links resolve. The required `bin/check_quotes.py A1/RESULT.md` check reports 10 quotes checked, 0 not found.

Only the changed analysis was recomputed. H2 membership, the sample selection, input agreement statistics and the already accepted card dispositions were not rerun. Source identity was checked against pinned primary sources in `provenance.md`. Independent verification and the cross-scope correction are in `verification.md` and `unit-boundaries.md`. No unresolved reading is accepted on the operator's authority.

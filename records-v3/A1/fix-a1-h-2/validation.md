# Validation of FX-A1-H-2

Date: 2026-11-22 UTC. Command: `/usr/bin/python3 -I A1/fix-a1-h-2/validate.py`. Machine-readable results: [raw/validation.json](raw/validation.json); quote output: [raw/quote-check.log](raw/quote-check.log).

- All 569 files in the before-fix manifest retain their recorded hashes. This includes the original 531 frozen inputs, the round-1 output directory and prior fix record.
- Exactly the same 21 IDs change in the extent, reader checks and whole-table index. Row order and all other rows are unchanged. The new extent contains 914 unique IDs; the scan contains 5,200.
- H1 remains 114 established occurrences and 243 factual unknowns. Reading-dependent rows are 501; exclusions total 56, comprising 21 under both readings and 35 unchanged prior exclusions.
- Neither sample contains any of the 21 affected IDs. Both frozen audits and sample selections remain unchanged; no sampling or audit procedure was rerun.
- The required quote check on RESULT reports 10 checked, 0 missing. The two boundary-note quotes also match. Local result/fix/boundary links resolve.

Only changed H1 records were recomputed, with exact disabled-state evidence checked against the saved inventory lines. H2, source provenance, other card dispositions and input statistics were retained. No removal experiment, machine, source download or new case was needed. [Independent verification](verification.md) checks the correction separately.

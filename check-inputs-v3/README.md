# Inputs of the checks of version 3

Concrete inputs of checks 1 and 4 of the third paper (`preregistration-v3/prereg-en.md`). Section 4.1 of
that paper: “Before the first observation of a check, its concrete inputs—the release numbers, the test
declaration, the program chosen for each channel, and the ordinary actions with their exact commands—are
committed to the repository of check records.” This folder was committed before the first observation of
checks 1 and 4; the inputs of checks 2 and 3 are committed separately before their first observation.

- `fix-c1-2/inputs-check-1.md` — check 1: releases, clean installations, ordinary actions with their exact
  commands, the inventory collector, and what became known before the first observation.
- `fix-c1-2/inputs-check-4.md` — check 4: releases, clean installations, the facts to be established for
  each property.
- `fix-c1-2/input-files.sha256.tsv` and `fix-c1-2/selected-inputs.json` — the exact files these inputs name,
  with their checksums. The preparation had a first pass and correction rounds after reviews: files no
  correction changed stay in `install/` and `actions/`; files a correction round changed or added are in
  `fix-c1-<n>/`; the final manifests are in `fix-c1-2`.
- The manifests also refer to records that are not inputs (the `raw/` folders, status and validation
  files, the internal task label `TASK-C1` under which the preparation ran). These records are published
  together with the outcomes of the checks.
- Named in the checksum list but not published here: `install/talos/controlplane.yaml` (holds generated key material of a disposable test machine; the checksum commits to it); `fix-c1-1/lab.sh` (operator tool with host-specific paths).

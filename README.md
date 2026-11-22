# Configuration as Law: evidence for the first test cycle

This repository holds the evidence records behind the second paper on the *Configuration as Law*
hypothesis, «Testing the “Configuration as Law” Hypothesis: Results of the First Cycle and a Second
Version». The second paper is published at <https://yakyman.com/configuration-as-law-v2.pdf> (page
<https://yakyman.com/research-v2>). The first paper, which stated version 1 of the hypothesis and fixed
five checks and their failure conditions before any check was run, is published at
<https://yakyman.com/configuration-as-law-v1.pdf>.

## Version 3: fixed before its checks

The folder `preregistration-v3/` holds the third paper, «Testing the “Configuration as Law”
Hypothesis, Version 3: Hypothesis, Checks, and Failure Conditions Fixed Before the Checks»
(21 November 2026): version 3 of the hypothesis, its four checks and their failure conditions,
published before any of these checks is run. `prereg-en.md` is the text; `configuration-as-law-v3.pdf`
is the same text as published at <https://yakyman.com/configuration-as-law-v3.pdf> (page
<https://yakyman.com/research>).

The folder `check-inputs-v3/` holds the concrete inputs of the checks of version 3, committed before the
first observation of each check, as Section 4.1 of the third paper requires.

The records were produced on 19 November 2026 (UTC). The experiments ran on disposable virtual
machines: clean installations of existing systems and a disposable Linux prototype (the *stand*, called
the *testbed* in the paper) built only to test the properties. The records in `definitions-analysis/`
analyse documentation and the written definitions without running machines.

## Outcome of the first cycle

Outcomes are reported strictly under the failure conditions fixed in the first paper
(1 = the hypothesis withstood the check, 0 = it did not, ? = the data are insufficient).

| Check | Property tested | Outcome |
|---|---|---|
| 1. Census | P1, P3 | **0** |
| 2. Law | P4 | **?** |
| 3. Reproducibility | consequence | **?** |
| 4. Derivative lifecycle | P6 | **?** |
| 5. Authority | P7 | **?** |

Outcome vector: **0 / ? / ? / ? / ?**. The 0 of check 1 rests on the clean virtual machines in
`check-1-census/` (Guix System: one object belongs to two classes with different consequences;
Debian, Fedora CoreOS and NixOS: disagreements of the two classifications that the text of the
definitions does not resolve).

## Layout

| Folder | Contents | Paper sections |
|---|---|---|
| `first-paper/` | `PAPER.html`, the English text of the first paper as fixed before the checks and used during them. It is byte-identical to the HTML source of the published first paper (SHA-256 `e69787144830c2706952b1c29bd2a4297b0d03d8e302402826513d10865d93a1`). | §2, §3 |
| `check-1-census/` | Census of clean virtual machines: `debian-fedora-coreos-nixos/`, `guix/`, three further samples in `samples/`, the check of the summary report (`report-check/`) and the observation of file-creating processes (`provenance/`). | §4.1 |
| `check-2-law/` | The stand and its law checks (`stand/`), 64 installation and launch channels on the stand and on NixOS (`channels/`), the second stand implementation (`second-implementation/`), signals of manual root action (`root-signals/`). | §4.2 |
| `check-3-reproducibility/` | Two independent stand installations (`stand-pair/`), three pairs of clean installations (`clean-install-pairs/`), alternating hardware profiles (`hardware-profiles/`), transfer of application state (`state-transfer/`). | §4.3 |
| `check-4-lifecycle/` | Revision of the stand's lifecycle result (`stand/`), random generation sequences (`random-generations/`), ordinary work, shared access and storage faults on both stand implementations (`stands/`), rollback of application versions (`rollback/`). | §4.4 |
| `check-5-authority/` | Final authority run on the stand (`stand/`), Unix permissions, competing application and restoration on both implementations (`stands/`). | §4.5 |
| `definitions-analysis/` | Analysis of the written definitions on documented object types (`documented-objects/`), the finite formal analysis and the comparison with documented rules of existing systems (`formal-and-literature/`). | §4.1, §5.2, §9 |
| `open-problems/` | Records cited for open problem O14 (`apply-crash/`). | §9 |
| `preregistration-v3/` | The third paper: version 3 of the hypothesis with its checks and failure conditions, published before the checks (`prereg-en.md`, `configuration-as-law-v3.pdf`). | |
| `MANIFEST.md` | Evidence key → files → claim of the paper, and the SHA-256 of every file. | |

Each record keeps its original file name. Raw files keep their original paths relative to the record
(for example `raw/…`, `raw-P7-3/…`), so the links inside a record resolve. Letters in record names
(B, D, E, L, P, V, W, X) are the original series labels of the experiments; `BQ` and `X3` name the two
implementations of the stand. In census tables `c1` and `c2` denote the first and the second of the two
independent classifications of every object, and `A`/`C` in hole lists mean classification 1 and
classification 2.

## How to verify a number

1. Find the section of the second paper and its evidence key, e.g. §4.1 `[@ev-v-census]`.
2. Look the key up in `MANIFEST.md`: it lists the records and the raw files that carry the number.
3. Open the record; the numbers are stated there with links to the raw files.

The numbers of the census can be recomputed with the scripts that produced them (Python 3 standard
library only):

```sh
(cd check-1-census/debian-fedora-coreos-nixos && python3 compare.py --output raw/recheck)  # 398 rows, 63.32 %, κ = 0.45480
(cd check-1-census/debian-fedora-coreos-nixos && python3 preclass.py)  # rebuilds preclassified.tsv and residual.tsv from raw/<machine>/
(cd check-1-census/guix && python3 compare.py)                         # 178 rows, 80.34 %, κ = 0.63346
(cd check-1-census/samples/ubuntu-alpine && python3 E6C-compare.py)    # 262 rows, 29.77 % (literal labels 6.11 %)
(cd check-1-census/samples/arch-silverblue-freebsd/raw-X1C && python3 compare.py)  # 510 rows, 12.94 %
(cd check-1-census/samples/debian-desktop/raw-X2C && python3 compare.py)           # 235 rows, 7.23 %
```

Except for the first, these commands rewrite their outputs in place. Each of them was run on the
published copy and reproduced the published files: the output tables byte for byte, the statistics
identically (in `metrics.json` only the time stamp and the list of input hashes differ). The same
holds for `preclass.py` in `check-1-census/guix`.
The remaining numbers (checks 2–5, provenance, open problems) are counts read directly from the summary
and result files listed in `MANIFEST.md`; scripts that computed them are included where they are small,
for documentation.

## What is not included and what was changed

Nothing in the measurements was changed. No number, count, outcome or result was altered by the
preparation of this repository; the census tables were recomputed from the published files, and the
numbers cited in the paper were recounted from the published raw files, with identical results.

* **Personal machines.** The census of the author's two personal machines is not published. The paper
  reports it only as aggregate numbers; the open evidence for the outcome 0 of check 1 is the census of
  clean virtual machines.
* **Selection.** Included are the records cited by the paper and the raw files needed to check the
  numbers it cites: result and summary tables, the classification tables and comparison outputs, the
  census inventories, and the scripts that ran the probes or computed the numbers. Not included are the
  operational files of the test run (scheduling, run logs, task statements, plans and working notes),
  very large raw traces, journals, disk images and archives, copies of third-party documentation (the
  sources are cited with their URLs in the records), and earlier superseded rounds. The list of all
  package files of the NixOS machine (`raw/nixos/package-files.txt`, 12.7 MB) is omitted: `preclass.py`
  produces identical tables without it. File names that appear in the records without a link refer to
  such working files; links to them were removed and their text kept.
* **Placeholders.** The name of the host machine is replaced by `<HOST>`, paths of the working
  directories of the test run on the host machines (which showed their folder layout) by `<WORKDIR>`,
  keeping the part of the path below the working directory, account names on the host by `<USER>`,
  network addresses outside the virtual machines by `<IP>`, Wi-Fi network names by `<SSID>`, MAC
  addresses by `<MAC-n>`, and machine identifiers, host-key fingerprints, public keys, key identifiers,
  test passwords and e-mail addresses by `<REDACTED-n>`.
  The same number denotes the same original value throughout the repository, so comparisons between
  machines remain checkable; the original values are not listed anywhere. Addresses internal to the
  virtual machines (QEMU user networking `10.0.2.x`, the isolated test network `10.44.0.x`, loopback and
  the documentation range `192.0.2.x`) and the test accounts inside the virtual machines (`alice`, `bob`,
  `census`, `guest`, `subject`, …) are unchanged.
* **Time.** Local times of the host were converted to UTC. The virtual machines ran in UTC.
* **Wording.** Internal labels of the tooling used to run and review the experiments (names of the
  executors and of their separate steps) were removed from the text of the records. Where a record named
  the party that executed or reviewed a step, the text now says *executor*, *independent review*,
  *classification 1* / *classification 2* or *separate step*, keeping what the method says about who did
  what and which steps were independent (for example, that an audit was a separate step of the same
  executor, or that the producer of classification 1 also adjudicated its own labels). Addressing of the
  author by name was replaced by *the author*.
* **Operational notes.** Remarks about how the test run was organised were removed from the records and
  from notes in the raw files: computing budgets, time allowances, deadlines and cut-offs of the run,
  scheduling, the history of shared virtual-machine slots and locks, references to other processes and
  runs on the host machine, quoted task statements and task assignments, and statements that an
  independent review was still pending or assigned (the completed reviews are included next to the
  records). References to the shared rules file of the run now read *the shared rules of the checks*. In
  one raw file (`check-3-reproducibility/hardware-profiles/raw-P6-3/analysis-final/control-summary.json`)
  the scheduling slot numbers were removed, and in one JSON note
  (`check-5-authority/stands/raw-P8-1/timing.json`) the time-allowance comment was shortened. Measured
  times and durations, methods, cleanup facts and the results of the completed reviews are kept. Two
  things of this kind remain on purpose: the probe cutoff in one experiment script (see *Scripts*), and
  the names of unpublished input files of the run (two task statements and the shared rules file) as
  keys in raw lists of frozen inputs and input hashes
  (`check-2-law/second-implementation/raw-P3-1/analysis/verification.json`,
  `check-2-law/second-implementation/raw-FX-P3-1-1/analysis/verification.json`,
  `check-1-census/debian-fedora-coreos-nixos/raw/fv1-comparison/metrics.json`); those lists record
  what was checked, so the names were not changed.
* **Scripts.** Identifiers and file names in the scripts were renamed in the same way as in their inputs
  and outputs; the comparison scripts of the census were adapted to this folder layout (input paths and a
  check against the original working tree); a few comments and one sentence of the text template in
  `E6C-compare.py` were reworded under the rules above. The code is otherwise as it ran. The experiment
  script `open-problems/apply-crash/raw-P4-2/src/run.py` contains a probe cutoff of its method: a fixed
  UTC time after which the script refuses to start a new probe row, measured command or recovery
  diagnostic. It is kept exactly as in the original code that produced the data; it stopped none of the
  28 recorded rows (all 28 are `complete`, with a valid recovery acknowledgement, in
  `open-problems/apply-crash/raw-P4-2/matrix.csv`). Hash lists inside records and outputs refer to the
  original working files, so they need not match the cleaned copies; the SHA-256 of every published file
  is in `MANIFEST.md`.

## License

© 2026 Arthur Yakymenko.

* Code written for the checks — files with the extensions `.py`, `.sh`, `.c`, `.S`, `.nix` and `.scm` — is licensed
  under the MIT License; see `LICENSE-CODE`.
* All other files — texts, records, tables and data — are licensed under the Creative Commons Attribution 4.0
  International License (CC BY 4.0); see `LICENSE` and <https://creativecommons.org/licenses/by/4.0/>.
* Files copied from the systems under study that were not written for these checks (for example, system files,
  distribution defaults, package lists and generated scripts in `raw/` folders) keep the licenses of their original
  authors.

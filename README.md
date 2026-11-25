# Configuration as Law: evidence for the test cycles

This repository holds the evidence records behind the papers on the *Configuration as Law* hypothesis.
The records of the first cycle stand behind the second paper, «Testing the “Configuration as Law”
Hypothesis: Results of the First Cycle and a Second Version», published at
<https://yakyman.com/configuration-as-law-v2.pdf> (page <https://yakyman.com/research-v2>). The first
paper, which stated version 1 of the hypothesis and fixed five checks and their failure conditions
before any check was run, is published at <https://yakyman.com/configuration-as-law-v1.pdf>. The records
of the second cycle stand behind the fourth paper and are described in the section «Version 3: results
of its checks, and version 4» below.

The records of the first cycle were produced on 19 November 2026 (UTC). The experiments ran on
disposable virtual machines: clean installations of existing systems and a disposable Linux prototype
(the *stand*, called the *testbed* in the paper) built only to test the properties. The records in
`definitions-analysis/` analyse documentation and the written definitions without running machines.

## Version 3: fixed before its checks

The folder `preregistration-v3/` holds the third paper, «Testing the “Configuration as Law”
Hypothesis, Version 3: Hypothesis, Checks, and Failure Conditions Fixed Before the Checks»
(21 November 2026): version 3 of the hypothesis, its four checks and their failure conditions,
published before any of these checks is run. `prereg-en.md` is the text; `configuration-as-law-v3.pdf`
is the same text as published at <https://yakyman.com/configuration-as-law-v3.pdf> (page
<https://yakyman.com/research-v3>).

The folder `check-inputs-v3/` holds the concrete inputs of the checks of version 3, committed before the
first observation of each check, as Section 4.1 of the third paper requires.

## Version 3: results of its checks, and version 4

The folder `fourth-paper/` holds the fourth paper, «The “Configuration as Law” Hypothesis: Results of
the Checks of Version 3, and Version 4» (22 November 2026). Part I reports the outcomes of the checks of
version 3 strictly under the conditions fixed in the third paper; Part II, formulated after the results,
fixes version 4 of the hypothesis and the failure conditions of its checks before these checks begin.
`paper4-en.md` is the text; `configuration-as-law-v4.pdf` is the same text as published at
<https://yakyman.com/configuration-as-law-v4.pdf> (page <https://yakyman.com/research>).

The folder `records-v3/` holds the dated records of the second cycle: the trial of the wording of
version 3 on objects from the first cycle, the checks conducted under its fixed plan, and the further
investigations reported in the fourth paper. The folder `trial-v4/` holds both rounds of the trial of the
wording of version 4, including the instructions, inputs, decisions, rules, gaps, unknown facts and
reviews. The records are dated 22 November 2026 (UTC). Earlier decisions, corrections and completed
reviews are retained together with their outcomes.

Check 1 yielded **0** and check 4 yielded **1**. Checks 2 and 3 were **not conducted**. In the order of
the four checks, the outcome vector is **0 / not conducted / not conducted / 1**. An unperformed check
is not an observation with outcome ?. Check 4 succeeded in assessing the existing systems; this does not
mean that either system has the properties. The trials of the wording are not checks on new objects.

| Folder | Contents | Fourth-paper sections |
|---|---|---|
| `records-v3/TEXT.md`, `records-v3/SENTENCES.md` | Version 3 and the sentence numbering used in the checks. | §2, §3 |
| `check-inputs-v3/` | Inputs committed before the first observation. | §3, §4.1, §4.4 |
| `records-v3/A1/` | First-cycle objects: inventories, two classifications with notes, comparison, adjudication, verification, corrections and reviews. | §3 |
| `records-v3/D1/` | Check 1: the same evidence chain, collection coverage and the termination of the Talos collection. | §4.1 |
| `records-v3/D4/` | Check 4: two independent assessments, the raw experiments and documentary evidence, and review. | §4.4 |
| `records-v3/A2/`, `records-v3/A3R/`, `records-v3/A3/BUILD.md`, `records-v3/B1/` | Further analysis of the wording, the lived-in disposable machine, and 88 installation/configuration channels. | §4.5 |
| `records-v3/B2/` | Partial testbed, four construction rounds, acceptance records and the small direct evidence they cite. | §4.2 |
| `trial-v4/round-1/`, `trial-v4/round-2/` | Both wording trials, including intermediate decision tables and corrections retained alongside final tables. | §9.6 |
| `MANIFEST.md`, section 5 | Evidence keys, records, claims and hashes of the records of the second cycle. | |

To verify a number, find the fourth-paper section in section 5 of `MANIFEST.md`, open its result and
review, and follow the corresponding comparison, adjudication or correction table. In `A1/` and `D1/`,
`in/` contains the inventories as collected; `c1/` and `c2/` contain the two independent
classifications; `compare/` joins them; `adjudication/` records the disputes. `RESULT.md` and the final
numbered review identify which correction round supplies the current count. Earlier rounds are
historical evidence, not additional observations to add to the final count. For the version-4 trials,
count the `status` column in each final `out/rows-<set>.tsv` and compare its identifiers with
`in/rows-<set>.tsv`. Other `rows-*.tsv` files record intermediate decisions and must not be added to the
final population.

The second trial has 4,934 final rows against 4,937 inputs. Its three missing rows and the 3,320
decisions dependent on unknown facts are retained as reported, not repaired during preparation. Source
hashes inside historical verification records describe the original inputs at the time of that
verification; section 5 of `MANIFEST.md` gives hashes of the cleaned public copies.

Nothing in the measurements was changed. No number, count, outcome or decision was changed in preparing
these folders. Tables retain their source row counts, including intermediate tables. The three console
images show disposable virtual machines and are retained unchanged.

Operational scheduling, task briefs of the second cycle, logs of the trial execution, plans, budgets,
temporary working directories and adjudication scratch are omitted. The two version-4 `TASK.md` files
are retained as the trial instructions. Trial helper scripts and intermediate fact-finding downloads are
omitted. Copies of distribution package metadata downloaded for fact-finding—package file lists,
repository indexes, package control/header records and package API responses—are omitted; these are
available from the distributions. Inventories actually collected on the test machines are retained. Some
citations in the first-cycle input tables point to older raw records that are not part of these folders;
these are marked “(not published: first-cycle raw record)”. For investigations beyond the plan and the
testbed, direct evidence is included only where the individual file is under 2 MB; no individual file
over 20 MB is included. This limits reconstruction of the larger testbed snapshots and some
lived-in-machine aggregates. An unavailable local reference is marked “(not published: category)”.

Privacy substitutions cover host names, host home paths and account names, network addresses outside the
virtual-machine networks, hardware addresses, wireless network names, machine identifiers, host-key
fingerprints, access keys, tokens and e-mail addresses. Virtual-machine names, test users and guest
filesystem paths remain. Internal labels of those carrying out the classification and review are
rewritten neutrally; the independence and scope of reviews are preserved. Names of third-party programs
found in an inventory remain part of the observation. Host local timestamps, where present, are
expressed in UTC; UTC guest records and names of timezone data files remain as collected.

## Version 4: order of its checks

The folder `check-inputs-v4/` holds `PROTOCOL.md`, published before the first observation of any check of
version 4. It restates that the outcome of each check is determined only by the failure conditions of
Section 9 of the fourth paper, sets out how the gaps that are found are weighted, lists the cases whose
decision is known in advance, and names the investigations carried out beyond the plan. The concrete inputs of
the checks are committed to the same folder before the first observation of each check, as Section 9.1 of the
fourth paper requires.

`check-inputs-v4/SUPPLEMENT-1.md`, published on 23 November 2026 after the first night of checks, lists the
claims of the hypothesis that none of the four checks tests and the steps by which they are examined. It changes
neither `PROTOCOL.md` nor the outcomes of the four checks. The inputs and the expected result of each step are
committed to `check-inputs-v4/supplement-1/` before the work on that step begins.

## Version 4: results of its checks, and the plan of a reference implementation

The fifth paper, «The “Configuration as Law” Hypothesis: Results of the Checks of Version 4, and a New Plan for Checking It», is published at <https://yakyman.com/configuration-as-law-v5.pdf> (page <https://yakyman.com/research>). The folder `records-v4/` holds the dated records of the third cycle and Supplement 1. The folder `analysis/` holds the two computations reported in Section 7.3. The records are dated 23 November 2026 (UTC). Earlier classifications, unsuccessful attempts, corrections and reviews remain beside the final results.

Check 1 yielded **0** and check 4 yielded **1**. Checks 2 and 3 were **not conducted**. The outcome vector is **0 / not conducted / not conducted / 1**. An unperformed check is not an observation with outcome ?. Check 4 succeeded in assessing the existing systems; neither system was found to have the three properties.

The outcomes of the eight steps of Supplement 1 are those of Table 4 of the fifth paper:

| Step | Outcome |
|---|---|
| 1 | Understanding 0; Reproducibility ?; Removal ?. |
| 2 | Six families 0; nine ?. In the sample of 600 agreements, 582 were established, 16 were undetermined, and two did not follow from the text. |
| 3 | ? and ?. |
| 4 | AlmaLinux ?; Void Linux 0; Gentoo 0; MicroOS ?; Talos Linux 0. |
| 5 | One case 1; sixteen ?. |
| 6 | Four cases 1; one ?. |
| 7 | 0 for the procedure of weighting. |
| 8 | ? in all four histories. |

| Folder | Contents |
|---|---|
| `records-v4/TEXT.md`, `SENTENCES.md`, `PROTOCOL.md` | The fixed text, sentence numbering and order used for the checks. |
| `records-v4/D1/`, `D1.stopped-before-observation/` | Check 1: inventories, two independent classifications and notes, comparison, adjudication, verification, corrections, questions and reviews; the earlier stopped attempt. |
| `records-v4/D4/` | Check 4: two assessments, the raw experiments and their review. |
| `records-v4/B2/` | Testbed description, construction rounds, review and retained small direct evidence. |
| `records-v4/A2/`, `B1/`, `A3/`, `W0/`, `W1/`, `W2/` | Work beyond the plan, its results, corrections, questions and reviews; the comparison and adjudication of the lived-in machines. |
| `records-v4/SUP1/`, `OP/` | Supplement 1, step texts including versions before review, nine reviews, and the independent assessment cited by the supplement. |
| `records-v4/S1/` … `S8/`, `D1b/` | Arguments and cases of the eight steps, expectations recorded before observations, questions, corrections and reviews; step 4's original and delivered inventories, classifications, comparison, adjudication and handoff verification. |
| `analysis/` | Two read-only Python 3 programs that compute the figures of Section 7.3. |

To verify a number, start with the corresponding entry of section 6 of `MANIFEST.md` and the result and final review of that check or step. Follow their comparison, adjudication and correction tables. In `D1/` and `D1b/`, `in/` holds the input inventories, `c1/` and `c2/` the independent classifications, `compare/` their comparison, and `adjudication/` the decisions on disputes. In `D1b/`, `raw/` retains original observations and `handoff/` the delivered copies; these are not extra populations to add to the totals. `RESULT.md` and the last review distinguish original adjudication findings from the later verification of gaps. Earlier rounds are historical records, not additional observations.

From the repository root, the computations of Section 7.3 require Python 3 and its standard library only:

```sh
python3 analysis/agreement_breakdown.py records-v4/D1/compare/joined.tsv
python3 analysis/disagreement_adjudication.py records-v4/D1
python3 analysis/agreement_breakdown.py records-v4/A3/compare/joined.tsv
python3 analysis/disagreement_adjudication.py records-v4/A3
python3 analysis/agreement_breakdown.py records-v4/D1b/compare/joined.tsv
python3 analysis/disagreement_adjudication.py records-v4/D1b
```

Both programs only read their inputs. On these public copies, all six outputs equal the outputs on the source tables. To inspect retained compressed text records, use `zstd -dc FILE.zst`; the gzip-compressed action-evidence archive retains its original filename. Historical checksums inside records describe the original files at the time of the check. The file `records-v4/SHA256SUMS` gives the SHA-256 of every cleaned file in `records-v4/` and `analysis/`; section 6 of `MANIFEST.md` maps the entries of the paper’s records section to their files.

The inputs committed before observations remain in the already-public `check-inputs-v4/`, including `supplement-1/`, its step instruments, cases, fixtures and sealed declarations. They are not copied into this results folder. Citations point to those existing paths. The fixed text, complete supplement history and step-4 handoff records explicitly required for this collection remain here even where an identical text was also committed as an input.

Working records of how the checks were organised—task texts, schedules and execution logs—working directories, caches and adjudication scratch are omitted. Disk images and access credentials are omitted. Copies of distribution package metadata downloaded for fact-finding—repository indexes, package file lists and package manifests—and downloaded working source archives are omitted; the original distributions provide these materials. Inventories and membership tables actually collected on the test machines are retained within the size limits.

For work beyond the plan, the testbed and steps of the supplement, cited raw evidence is retained where each file is below 2,000,000 bytes. The explicitly required comparison and adjudication tables are retained separately. For check 1 and the step-4 inventory, the general file ceiling is 20,000,000 bytes. The two larger `A3/compare/joined.tsv` and `D1b/compare/joined.tsv` tables are retained because the paper names them and Section 7.3 reads them. Large omitted snapshots, traces and indexes limit full reconstruction of those experiments. An unavailable local reference is marked “(not published: category)”.

Privacy substitutions cover host identity and host home paths, the author's account identity, network addresses outside isolated test networks, hardware addresses, wireless names, machine and connection identifiers, access keys, tokens, fingerprints (including digests of identifier and access-key files) and email addresses. Performer labels are neutralized while preserving which classifications and reviews were independent. Third-party program and package names found on test machines remain observations. Local clocks are expressed in UTC; guest timestamps already in UTC and timezone-data filenames remain unchanged. Compressed observations remain byte-identical where no cleaning was necessary; those containing access credentials were cleaned and recompressed without changing their observation rows.

No measurement, count, outcome or decision was changed. Every included table retains its source row count. The records retain the reported limitations, unknown facts and disagreements of reviews.

## The reference implementation: inputs committed before its check

The fifth paper (Section 9) fixes a check on a reference implementation, ConfOS, built with the text of version 4 as
its specification. Section 9.5 requires that the exact commands of the cases, the declarations, the checking programs,
the program chosen for each channel and the releases of the components be committed before the first complete run.
Two folders hold them:

* `confos/` — the implementation as it stood before the complete run named in `confos/RELEASE.md`: every text file of
  its source archive, and the path, size and SHA-256 of every other file of the archive (`confos/BINARIES.tsv`).
* `confos-check/` — the cases (`CASES.md`); the programs that take the inventory of a machine, compare it with the
  declaration and derive the state from the declaration alone (`inventory`, `compare`, `derive`); the runner (`run`);
  the rules by which objects are decided (`decide.tsv`); the program chosen for each channel (`PROGRAMS.md`); the
  record of the repairs of these programs (`CORRECTIONS.md`); and their self-tests.

Both folders are replaced whole before each later complete run. The history of the repository keeps every earlier
state, and section 7 of `MANIFEST.md` lists the SHA-256 of each state. Runs made while the implementation was being
built are not observations of the check; their records are published with the outcomes. The programs in the two
folders are code under the MIT License (`LICENSE-CODE`), whatever their file extension.

From the third complete run on, a third folder, `confos-check-extra/`, holds cases beyond the plan and the
programs that perform them (`CASES-EXTRA.md`, `run-extra`, `casedefs_extra.py`, `derive-radio`). They exercise the
sentence of Section 8.3 of the fourth paper on tools that record a change in the declaration, and a saved Wi-Fi
network and a Bluetooth pairing on simulated radios. They are not cases of Table 9 and not part of a complete run:
they are committed with its inputs and performed on the same release right after it, and their outcomes are reported
apart from the outcomes of the check.

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
| `check-inputs-v3/` | Inputs of the checks of version 3, committed before the first observation of each check. | third paper §4.1 |
| `fourth-paper/`, `records-v3/`, `trial-v4/` | The fourth paper and the records of the second cycle; see «Version 3: results of its checks, and version 4» above. | fourth paper |
| `check-inputs-v4/` | The order of the checks of version 4 (`PROTOCOL.md`) and the inputs of these checks, committed before the first observation of each check. | fourth paper §9 |
| `fifth-paper/`, `records-v4/`, `analysis/` | The fifth paper and the records of the third cycle; see «Version 4: results of its checks, and the plan of a reference implementation» above. | fifth paper |
| `confos/`, `confos-check/` | The reference implementation and the inputs of its check, committed before each complete run; see «The reference implementation: inputs committed before its check» above. | fifth paper §9 |
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

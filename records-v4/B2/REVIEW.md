# Independent carry and planning review

Recorded 2026-11-23T08:17:45Z by the review role.

**Disposition: ACCEPTED for the bounded carry, rebuild, unchanged Round 0 self-test and version 4 planning task.** This is not a version 4 testbed acceptance and is not a hypothesis outcome of `1`. The testbed remains `STAND: partial`; the overall hypothesis outcome remains `?`.

## Scope and method

The review read the required parts of `TEXT.md` with `SENTENCES.md`, the named historical records and recipe, the carried controller and plan, the current result documents, and the saved Round 0 evidence. It did not inspect unlisted historical evidence, add a probe, rerun a test, or mutate the remote testbed. The review checked the records against the saved evidence rather than accepting builder summaries alone.

The carried recipe has 56 files. Its membership and bytes match the named historical recipe except for the documented VM lock-directory relocation in `build/lab.py`; no installed mechanism, assertion, fixture or expected result changed. [Recipe provenance](raw/round-0/recipe-provenance.json) and the [provenance notes](raw/round-0/PROVENANCE.md) distinguish original, pre-relocation and deployed inventories. [round0.py](tools/round0.py) rebuilds twice, invokes the complete unchanged regression and combined sequence, and performs cleanup. It contains no version 4 mechanism.

## Evidence assessment

Both independent recipe runs and every controller stage exited 0. The four channel suites contain 79, 131, 32 and 59 passing result assertions, respectively; the regression evidence contains 35 Round 3, 166 BC1 and 133 BC2 passing assertions. All nine success-triggered add/change/remove cuts pass. The boot gate records 176 pre-ready ordinary attempts, zero successes and no premature operator session. The independent inventory deliberately remains `complete:false`, with P1 `?`. These observations agree with [SELFTEST.md](SELFTEST.md) and the [stage summaries](raw/round-0/summary.json).

The original D10 comparison has 556 equal actual rows. The comparison across the two full builds also has 556 equal actual rows and equal declaration bytes. The combined test has 24 passing controller assertions, 571 successful per-line checks before and after reboot on each build, equal exact declaration bytes after both reboots, eleven successful channel launches plus the scheduled command on each build, and 571 equal actual rows. The retained declaration hash is `33f293b063fbab1ea6af5cab16f8a7c5ee813dd04a55edab26b32769e09bab17`. Evidence is in the [baseline](raw/round-0/round-4/baseline), [combined run](raw/round-0/round-4/combined) and (not published: over 20 MB).

The two new factories agree at 552 rows, 434 package rows and 31,247 base-file entries. The named previous review reports 553 rows and a different factory hash while reporting the same base-manifest and initramfs hashes. The missing historical row/value is correctly recorded as `FACT_UNKNOWN`; neither the evidence nor this review supports a cause or exact old-factory reproduction claim.

Cleanup records show no owned VM directory, VM entry or emulator process, removal of the temporary peer, and preservation of the sole retained image at mode 0444 and its rebuilt hash. The publication manifest lists 199 files; this review recomputed every listed size and SHA-256 digest successfully. It reports no changed published file and no declaration-byte change. No symbolic link or private access key is present in the published evidence or examples. See [cleanup](raw/round-0/cleanup.json), [host cleanup](raw/round-0/host-cleanup.json) and the [publication manifest](raw/round-0/publication.json).

## Difference record and future rounds

[V4-DIFF.md](V4-DIFF.md), [STAND.md](STAND.md) and [v4-variant-map.json](v4-variant-map.json) agree on all 88 IDs, names, historical dispositions, criterion-change decisions, implications and owning rounds. The historical count is exactly 78 CLOSED and 10 NOT CLOSED. Every row is separately marked NOT VALIDATED for version 4. All 47 quotations from Sections 8.1–8.3 match `SENTENCES.md` exactly. The kept, must-change and removed mechanism decisions identify their sentence or section basis and do not claim that unchanged refusal evidence establishes the required command shell.

During review, C7.15, C7.16 and C7.22 were corrected from no criterion change to **Yes**. The resulting text follows S8.2-5: runtime-only memory state follows its creating program or setting and does not require a separate line for transient memory bytes. Saved source or payload objects and access settings still require their own ordered assessment, and the unsaved-execution/reboot case applies where relevant. The correction is consistent in the difference record, map, stand and Round 1 self-tests.

The declaration description was also clarified against the saved exports. The 552-row factory uses `machine.jsonl` with a checked `base-files.json` sidecar. The complete 571-row combined example consists of one `machine.jsonl` and embeds all 31,247 base-file requirements inline. Both forms are represented accurately in [STAND.md](STAND.md), [HOWTO.md](HOWTO.md) and [example provenance](example/provenance.json).

[ROUNDS.md](ROUNDS.md) has four future, single-scope rounds. Round 1 requires a real ordinary command shell, recorded personal-script use, positive declaration-writing built-in tools under ordinary and actual superuser invocation, and the unsaved execution/reboot case. Rounds 2 and 3 own object coverage and lifecycle/removal work; Round 4 cross-checks all 88 with integrated ordinary work and independent installations. The owning distribution is 65, 9 and 14 rows for Rounds 1–3, with all rows checked again in Round 4. No historical open row is deferred without an owner.

No remaining review finding blocks this bounded deliverable. Historical closure remains historical, all 88 version 4 variants remain NOT VALIDATED, no new mechanism has been accepted, and the overall outcome remains `?`.

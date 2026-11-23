# Rehearsal records

`fx-run.py` is the active repair harness; it accepts one of the ten fixed systems and repair round1–4. Numeric keys11–14 distinguish these rounds from the original pass. `run.py` and `finalize-records.py` are retained historical first-pass sources and are not the final acceptance procedure.

After every worker stops, synchronize status/count files and permitted diagnostics. Run `fx-query-limitations.py`, then `fx-finalize.py`; the latter refuses finalization unless every system is ready or has four FX rounds. Run `fx-fix-report.py`, `build-publication.py` and `make-inputs.py`. Obtain independent review before the final `publish-manifest.py`; a read-only checksum validation follows that last write.

Final acceptance uses only numerical records and documented stderr/coverage limitations. No object table, raw query stdout, member list or package-file content is opened by these scripts. The collector itself emits aggregate counts from memory. `query-limitations.tsv` names every accepted exception and its retained diagnostic. `DISCLOSURES.md` includes diagnostic reads, failed/replaced actions and known preparation content.

Historical reason counts from unsupported inference are preserved but not accepted. The finalizer subtracts every known historical Python/npm reason when the corrected source-category counters are absent; Gentoo FX1 also has invalid historical graph-derived reasons and cannot establish readiness. The final source never infers an individual package reason from a selected group or a native parent.

The publication allowlist includes all cited acceptance diagnostics, all action stderr, coverage, and nonempty retained diagnostics. Uncited empty transport/query stderr remains in the local rehearsal tree; it contains no additional evidence. No inventory stdout, objects or members are published.

Check-4 transport sequences stop after the first failed call because twenty consecutive successes are then impossible. The failed status is retained, the clone is destroyed, and the next permitted round uses a fresh clone after repair. Readiness still requires exactly twenty distinct zero calls. The already-started Guix FX1, if interrupted after failure, records explicit unit/clone cleanup and no fabricated whole-run success.

The publication builder takes source-location arguments instead of embedding the host home layout: `python3 rehearsal/build-publication.py --source-home-relative RELATIVE_DIRECTORY --previous-lab-name PREVIOUS_DIRECTORY_NAME`. These identify the existing installation sources for placeholder conversion; materialization uses separately supplied absolute laboratory roots.

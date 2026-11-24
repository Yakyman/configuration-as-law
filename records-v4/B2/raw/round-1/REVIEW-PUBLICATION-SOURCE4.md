# Independent publication-source review, revision 4

Review time: 2026-11-23T10:51:37Z

Scope: final bounded read-only audit of current `export-round1.py` and `adopt-round1.py`. The summarizer remains a separate pending review. No publication or adoption was executed, and this note makes no experiment-closure decision.

## Final corrections verified

The exporter now requires the outer frozen-supplement source manifest at its exact publication path and requires its key set to be exactly `v4-direct-selftest.py` and `v4-extra-selftest.py`. It compares that manifest exactly with the executed supplement input manifest, requires the frozen payload directory to contain exactly those two filenames, and checks each payload SHA-256 against the manifest.

The normalization guard covers the frozen supplement directory, input manifests, and source-hash records. A host-prefix replacement in any of those protected files stops export instead of changing the bytes. The frozen inputs and both identity records then enter the ordinary publication inventory and archive digest verification.

Archive creation clears numeric owner and group IDs to zero, clears owner and group names, and sets mode 0644 for every member. `verify_pair()` now asserts those fields during initial verification and prepared-marker recovery. Adoption independently asserts the same fields while checking the acceptance-bound archive SHA-256, member count, exact member set, and content hashes.

Both scripts parse successfully as current Python syntax. The previously reviewed locking, staged-source identity checks, export recovery, adoption journaling, rollback, durable commit, and delayed cleanup paths remain intact in the current source.

## Verdict

No material source defect remains in `export-round1.py` or `adopt-round1.py` for the stated host-only publication and adoption guarantees. These two scripts are acceptable for use after the strict summarizer and final evidence review pass and after the external acceptance artifacts they require have been produced. This verdict does not authorize early adoption and does not evaluate the still-pending summarizer. Current overall outcome remains `?`.

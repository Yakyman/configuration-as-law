# Independent strict-summarizer correction review

Review time: 2026-11-23T11:00:05Z

Scope: bounded re-review of the current `summarize-round1.py` and its pinned controller, adapter, application-suite, and baseline inputs. Checks were read-only; no guest was started or changed, and no metrics or closure decision was produced.

## Earlier findings

All three material findings in `REVIEW-SUMMARIZER.md` are corrected.

The main controller is now tied to the reviewed `round1.py` SHA-256 and an exact 22-step success-path contract. The validator requires the exact summary schema, zero controller exit, an empty remaining-machine list, no remaining peer tree, and the neutral `?` outcome. It requires `summary.json` and `steps.json` to contain equal step arrays, and checks every step's exact argument vector, log name, legacy flag, timestamps, expected exit, actual exit, and output-file presence. Direct comparison with the pinned controller source confirms the build, three component lifecycles, peer build, carried regression, example assembly, and combined replay sequence.

Carried and combined evidence now use exact recursive inventories of 123 and 50 unique regular files. The root must be a real directory; every descendant must be a real directory or regular file; symlinks, special entries, missing files, and extra files are rejected. Unknown evidence can no longer remain outside aggregation under either tree.

Shell routing markers are now derived from the SHA-pinned baseline expected commands using the exact transformation implemented by the SHA-pinned adapter. The application holder exception is derived from the pinned application suite and its corresponding baseline command. Marker schema, timestamp, placement immediately after the associated expected row, expected ID, complete argument-vector payload, order, and count are compared. Independent calculation gives 55 language, 59 application, 16 system, and 45 ordinary markers. Metrics retain the complete ordered marker records, their count, their ordered SHA-256, the adapter source SHA-256, and a provenance statement.

## Additional checks

The current source parses successfully, and all controller, adapter, and application source hashes match their embedded pins. The six new-suite contracts still distinguish result-row count from Boolean assertion count. In particular, the extra supplement contract requires 21 result rows consisting of 16 Boolean assertions and five explicit null-verdict runtime observations; these observations cannot be silently converted into passes.

A local `--check-only` invocation rejected the incomplete local evidence tree at the absent carried-suite root before aggregation. This is the expected behavior for the current partial copy and does not validate the complete final tree. Reported malformed-copy tests are consistent with the strict parsing, exact schema, exact inventory, and exact transport checks visible in source; this review does not substitute those synthetic copies for the final evidence.

## Verdict

No material source defect remains in the three corrected paths. The current summarizer is acceptable as a strict host-side validator for final metrics, conditional on a successful `--check-only` run over the complete frozen final evidence and reconciliation of the resulting metrics with the publication manifests and independent evidence review.

This is source acceptance only. It neither accepts final evidence nor closes any variant, and the overall outcome remains `?`.

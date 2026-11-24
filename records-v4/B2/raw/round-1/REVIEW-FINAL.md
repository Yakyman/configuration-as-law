# Independent Round 1 final review

Review time: 2026-11-23T12:27:01Z

Scope: independent source, mechanism, complete final-2 evidence, strict-parser, combined-replay, example, and draft-report review for Round 1. The review used saved files only. No guest, build, probe, or remote mutation was started. This review decides bounded variant disposition; it does not decide the hypothesis.

## Evidence acceptance

The strict validator at SHA-256 `df131f96cae4dc61cf4c10b6ddf196472051fdedd51cc10478fd353efbdcc9a4` passes the complete exported final-2 tree in read-only mode. Its last correction is acceptable: it pins `round4-driver.py` and maps exactly the four source-defined `CLEANUP-bc4-baseline-*` expected identities to their `final-2` forms. It preserves record count, order, schemas, result identities, and all other payload checks. A different phase identity, an omitted cleanup expectation, and a duplicate expectation are rejected.

The validated main controller contains 22 successful steps, an empty remaining-machine list, and no remaining peer tree. The primary and peer images came from separate builds of the frozen recipe. The carried suite has exact 123-file and combined suite exact 50-file inventories. All carried controller stages exited zero, all 301 channel assertions passed, all 166 authority and 133 code/lifecycle assertions passed, all 35 transaction assertions passed, and all nine power-cut assertions passed. The independent carried comparison has identical declaration bytes and 557 equal actual rows. All 205 ordinary login attempts made before observed readiness failed.

The combined controller completed with 24 passing assertions. Both images accepted the same 572-row declaration. Eleven recorded channel launches and the scheduled command passed on each image. All 572 rows read back successfully before and after both reboots, the declaration SHA-256 remained `7a5c9116f501dc280e1681970d1489c97b009509cc14e0c4048a82123d3b7284`, and the final 572-row actual-value comparison is equal. The exported Round 1 example hashes match the assembly log and combined evidence.

The new and supplemental suites contain 157 Boolean assertions: 141 pass and 16 fail. The validator retains all 16 failures: six shell saved-input failures, five direct saved-input failures, four extra saved-input failures, and one native-root account-tool bypass. Five additional runtime observations with null verdicts remain observations rather than passes. The earlier FFI label error remains corrected: its mapping was denied and no exact output marker executed.

The Bash adapter evidence is interpreted narrowly. Broker commands entered ordinary Bash. Retained application launches still invoked the sealed compatibility runner from Bash. Their success establishes compatibility, not a general saved-input boundary. This distinction is present in the draft reports and agrees with the raw marker evidence.

## Variant decisions

### C5.4 — CLOSED

The concrete mechanism protects exactly declared native files as root-owned objects with recorded bytes, mode, owner, and group. Ordinary shell descendants inherit the write and native-execution policy; authorized replacement occurs through declaration application. This protection is based on the recorded path and file state, so it applies equally to a recorded executable or native library rather than depending on the tested program's behavior.

The required adversarial observation is present. `recorded-native-overwrite` attempted to replace the installed worker in place from ordinary Bash. The write was denied, while the exact SHA-256, mode 0755, UID/GID 0, complete covering row, and last successful application identity stayed unchanged. The carried mutable-output overwrite and language immutable-write cases are consistent with the same mechanism. Positive install, launch, removal, complete readback, independent replay, and reboot evidence show that the protection does not make recorded native files unusable.

This closes C5.4 for the supplied recorded-file mechanism. It does not close saved interpreted input, compiler plugins, package-manager bypasses, removal races, or deliberate privileged breaking; those have separate variants and remain open where applicable.

### C10.4 — CLOSED

The supplied editor is a real general document program: it reads, writes, and appends arbitrary document bytes with the caller's identity. Its documented package-install and package-remove operations delegate to the common package broker, whose exact artifact validation changes the primary declaration and applies it before returning success. The same path is exercised through ordinary Bash and actual root execution.

Both identities successfully performed document write, append, and read, then exact package install, installed-program launch, and removal. A bad-hash package was refused without a declaration or report change, followed by 553 clean readback rows. The nested editor caller completed after application with its original cgroup restored and no freezer journal or child group left. Direct privileged document editing also succeeded and was explicitly classified as breaking, as required by the separation between general root editing and the editor's installer functionality.

This closes C10.4 for the supplied editor and its documented installer. It does not claim that arbitrary foreign editor plugins or undisclosed installer interfaces are covered. The native root account-tool bypass keeps C10.1 open and does not undermine the editor-specific positive path.

## Remaining disposition

Exactly two of 88 variants are closed in version 4: C5.4 and C10.4. The other 86 remain NOT CLOSED. The 16 concrete failures, unavailable routes, finite unsupported syntax, saved-code gaps, native privileged-tool bypass, cgroup numeric-PID race limit, and later-round lifecycle/coverage work are not erased by carried or combined success. The overall hypothesis outcome remains `?`.

## Draft report review

The five Round 1 drafts accurately describe the mechanisms, raw evidence, failed attempts, Bash-versus-sealed distinction, combined replay, and known limits. Before promotion, they require the following disposition edits:

- `BUILD-1-DRAFT.md`: replace both pending counts with two closures in this round and two of 88 overall; replace conditional-review language with the two accepted bounded decisions and retain the `?` outcome.
- `STAND-ROUND1-DRAFT.md`: set C5.4 and C10.4 to `CLOSED`, leave every other current row `NOT CLOSED`, state 2 CLOSED / 86 NOT CLOSED, and replace the pending-final-review introduction with the accepted partial result.
- `SELFTEST-ROUND1-DRAFT.md`: replace the pending independent-review language with the two decisions, and replace the statement that all 88 are unvalidated with 2 CLOSED / 86 NOT CLOSED. Its explicitly historical Round 0 counts and 571/556-row figures should remain labeled historical rather than being rewritten as current evidence.
- `ROUND1-COVERAGE-DRAFT.md`: change only C5.4 and C10.4 from conditional candidates to the bounded closures above, update the header and candidate paragraphs, and retain every route-specific limitation and all failed/unavailable observations.
- `HOWTO-ROUND1-DRAFT.md`: its operational and evidence-reading text is acceptable; final links must point to the promoted reports and this review.

No other closure is supported by the current evidence.

## Publication and adoption condition

The earlier 483-member publication verified every member hash and performed zero normalizations, but it binds the superseded parser and must remain unaccepted. Regenerate the raw-evidence/example archive with the accepted parser in the candidate tool inventory and update its manifests. Under the reviewed adoption design, `metrics.json`, this review, and `acceptance.json` must remain outside that archive so the archive collision guard can require their absence. The adopter then verifies each external artifact against the hashes fixed by the acceptance record, adds them to the staged raw tree, rechecks the staged image, source inventories, publication, metrics, and review, and only then performs the journaled durable commit. That hash-linked staged construction satisfies this review's packaging condition. This is host-only packaging work and requires no guest rerun.

Subject to that exact repackaging and the draft disposition edits above, the Round 1 evidence and the two bounded closures are accepted. The testbed remains partial and the hypothesis remains `?`.

VERDICT: AGREE

# Final independent review of the C1 rehearsal repair

Reviewed 2026-11-23T10:58:25Z. The repair and rehearsal record satisfies the binding rule that each assigned system must either meet every readiness criterion or complete four fresh repair rounds. This review used source files, generated documents, numeric status and count tables, limitation records, hashes, and the final cleanup certificate. It did not open guest inventories, rehearsal objects, raw query output, member lists, or the exposure-review document. The disclosure document was checked only by path, size, digest, and its reviewed generator.

## Final readiness record

The headline and all ten rows in `READY.md` match `rehearsal/final-summary.json` and a fresh preview from `rehearsal/fx-finalize.py`. Three systems are ready:

- MicroOS has collector exit 0, 5,070 second-level rows, 376/376 known package reasons, 18,246/18,575 known packaged-file integrity results, twenty successful transport calls, a 76.210-second whole run, and successful clone destruction.
- NixOS has its assigned twenty successful transport calls, a 28.814-second whole run, and successful clone destruction. Actions and collection are correctly not assigned for this check-4 system.
- The lived-in server has all thirteen actions successful, collector exit 0, 1,249 second-level rows, 359/392 known package reasons, 23,314/25,166 known packaged-file integrity results, twenty successful transport calls, a 147.739-second whole run, and successful clone destruction.

The other seven systems are correctly not ready, and each has four completed repair rounds with successful destruction or the documented destruction fallback:

| System | Final retained blocker |
|---|---|
| AlmaLinux | Conservative package-reason lower bound is 999/1,561. |
| Void | Conservative package-reason lower bound is 342/546. |
| Gentoo | The browser-extension action failed and only 12/440 package reasons are known. |
| Talos | Packaged-file integrity is known for 0/95 files. |
| Guix | The fourth transport sequence failed before any successful fixed call and has no qualifying whole-run result. |
| Fedora | Package reasons are known for 1,679/2,248 packages. |
| Mint | Packaged-file integrity is known for 283,328/449,205 files. |

Every ready collector has exit 0, one completed numerical reduction, nonzero second-level coverage, strictly more than 90 percent known package reasons, strictly more than 90 percent known non-directory packaged-file integrity, and no unexplained query failure. Every ready transport has exactly twenty distinct successful calls. Every assigned ready action set is complete and successful. Every ready whole run is below 1,800 seconds. The finalizer fails zero denominators, incomplete reductions, missing cleanup, duplicate or incomplete transport sequences, unexplained query errors, and percentages equal to or below the threshold.

The latest status and count tables independently reproduce these decisions. The query-limitation records explain every retained nonzero query in the latest rounds; unsupported or inaccessible facts remain unavailable rather than being inferred. Directory entries remain outside the file denominator, while symlinks and unresolved object types remain conservatively included.

## Repair-round and source integrity

All seven not-ready systems have rounds 11 through 14 and a qualifying zero-status cleanup record in every round. Merely starting a round cannot satisfy exhaustion. Mint FX4 used the final repaired action and collector sources and retained all nine successful actions, collector exit 0, twenty successful transport calls, a 695.253-second whole run, and successful destruction. No fifth repair round is present or implied.

Later source corrections that were not replayed are described without changing retained results. AlmaLinux and Void remain not ready under the conservative lower bound that removes every historically known Python and npm reason when the older counters cannot separate native-parent inference. Talos remains not ready from its measured 0/95 integrity result; the later conservative symlink handling does not improve it. Gentoo remains not ready after its fourth-round browser failure; the final extension helper is identified as source-reviewed but unrehearsed. No source-only amendment promotes an exhausted system to ready.

The source review records all twenty-six identified instrument findings as resolved. The final collector keeps native package ownership as provenance without transferring the native install reason to language packages, expands Portage reasons only from uniquely resolved selected-set evidence, leaves unsupported Talos integrity unknown, retains symlinks in file accounting, and records unsupported Homebrew discovery as a limitation without creating package facts. The runner requires fresh clones, retains allowed stderr separately, terminates timed-out sessions with certified process absence, and counts a repair round only after cleanup evidence. The final cleanup guard invalidates old certificates before checking, rechecks active preparation units, fails explicitly on any remainder, and publishes its certificate atomically.

## Cleanup

`rehearsal/cleanup-final.tsv` has one UTC timestamp and five zero remainders: rehearsal clone directories, transient unread directories, active preparation units, the temporary probe-build directory, and the uncompressed probe output. The cleanup certificate was generated after the final rehearsal. No retained readiness row depends on a clone or preparation process that remained active afterward.

## Original review and publication records

`FIX-C1-REH-1.md` gives a disposition for all nine original review findings. Findings 1–7 and 9 are repaired in the final documents and sources. Finding 8 remains explicitly identified as absent from the immutable contemporaneous choice record: the exact selected Talos and MicroOS artifacts are fixed, but no later rationale is presented as an original choice. This is an honest disclosed limitation and does not create a new selection.

The protected `TEXT.md`, `PROTOCOL.md`, and `CHOICES.md` digests still match `rehearsal/FX-SCOPE.md`. The regenerated Section 2 inputs retain all prescribed systems, exact release and recipe records, ordinary actions, collector sources, check-4 facts and six cases, and the three lived-in systems outside the four checks. Their 123, 34, and 22 embedded hashes all match the current named files. The input documents assign no hypothesis outcome and keep the conservative rule for incomplete second-level inventories.

The publication generator uses an explicit allowlist, bounded file sizes, path containment, credential and personal-location checks, typed diagnostic admission, and byte-identical probe-chunk reconstruction. Its pre-review check found 1,346 bounded files and only this required final review missing. The final publication list and checksum manifest must now be generated once, after this file exists and all writers have stopped. That mechanical final step must include this review and must not alter the reviewed sources, generated inputs, readiness record, repair report, disclosure record, or cleanup certificate.

The rehearsal records establish instrument readiness only. They do not assign an outcome to any hypothesis or property.

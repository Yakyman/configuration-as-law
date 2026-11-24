# Independent publication-source review, revision 2

Review time: 2026-11-23T10:45:56Z

Scope: second read-only audit of the rewritten `export-round1.py` and `adopt-round1.py`. The summarizer was outside this review. No publication or adoption was executed, and no closure decision is made.

## Corrected first-pass defects

The exporter now uses unconditional checked errors, requires the three publication roots, preflights the merged namespace for collisions, writes normalized copies into a separate tree, preserves pre- and post-normalization hashes, refuses normalization of identified frozen inputs and declarations, verifies every archive member against the staged inventory, and leaves authoritative raw inputs untouched.

The adopter now uses unconditional checked errors, requires completion and external acceptance artifacts, verifies the candidate image hash and mode 0444, compares recursive typed key inventories exactly, validates the expected `example` symlink, verifies the publication tree against its manifest, stages recursive exact copies, journals all swaps, retains previous targets until commit, rolls back an interrupted prepared transaction, and deletes the candidate/publication duplicates only after a committed record exists. These changes resolve the destructive ordering, one-way key comparison, top-level-only recipe copy, and assertion-removal defects from the first review.

## Remaining release blockers

### 1. Retained operational source is not fully hash-linked to acceptance

The accepted input manifest is compared only with the immediate files in candidate `build/`. The adoption sources also include candidate `tools/` and a standalone `lab.py`, but neither tree is compared with an accepted hash inventory. The build input manifest contains the build copy of `lab.py`; it does not prove that the separately adopted controller has the same bytes. The accepted publication manifest covers evidence and examples, not these retained operational source trees.

As written, candidate `tools/` or standalone `lab.py` can change after review and still be copied into the retained root. This contradicts the intended hash linkage between acceptance and retained source.

Required correction: include exact recursive typed inventories for `build/`, `tools/`, and standalone retained files in the accepted source manifest. Bind that manifest's hash in the acceptance record, compare each source before staging, and compare the staged copies again before writing the prepared journal. If only a subset of `tools/` is meant to be retained, enumerate that subset explicitly.

### 2. Staging is vulnerable to time-of-check/time-of-use changes

Image, publication, build, acceptance, metrics, review, and other source checks occur before staging. `copy_exact()` proves only that a staged copy equals its source at copy completion. It does not prove that those bytes still equal the hash accepted earlier. A concurrent or accidental change between the initial check and copy can therefore be adopted. The image has the same gap: its accepted SHA-256 and mode are checked before copying, but the staged image is not rechecked against them.

Required correction: treat accepted hashes/inventories as the authority, then validate every staged object against those fixed values. Recheck staged image SHA-256 and mode, staged publication contents against the accepted manifest, staged build/tools/controller inventories against the accepted source manifest, and staged acceptance/metrics/review hashes against the acceptance record immediately before journaling. Also recheck that source inventories did not gain or lose entries, or hold an exclusive host-side publication/adoption lock across preflight and staging.

### 3. Export commit marker has no recovery path

The exporter creates a prepared marker and performs two renames, but it never handles an existing marker. On the next invocation, the destination-existence checks fail before any recovery logic. Interruption after the first rename leaves a published tree with no archive; interruption after both renames but before marker removal leaves complete outputs that are still permanently treated as incomplete. A marker that exists before staging is checked only after the new stage and archive have been built; the exception handler then preserves those new temporary objects because it sees the old marker.

Required correction: inspect the marker before all destination checks and staging. Validate its schema and exact names, then deterministically finish or roll back each possible state by verifying the staged/published tree and temporary/final archive against the manifest. Reject unexplained combinations. Sync all affected directories, remove the marker only after a verified complete pair, and make repeated recovery idempotent.

### 4. Export completeness list omits raw evidence consumed later

The required evidence list does not include combined events or the supplement reboot, before/after verification, reports, input-hash, controller-step, and cleanup records. Their containing directories are copied if present, but absence does not stop export. Aggregate summaries alone do not preserve the row-level evidence needed to audit those claims.

Required correction: derive the required publication file set from the strict summarizer schema and acceptance review inputs. Require every raw file used for metrics or final findings, including combined events and all supplement identity/readback/reboot/controller records, before building the merged inventory.

### 5. The public archive itself is not bound into adoption acceptance

Export verifies the archive when created, but adoption verifies only the published tree and the publication-manifest hash. It neither hashes nor reopens `round1-publication.tar.gz`. The archive can therefore be changed after export while adoption succeeds and retains an unverified public artifact.

Required correction: record the final archive SHA-256 and member count after verification, bind that digest in the independent acceptance record, and have adoption recheck the archive digest and its exact member inventory against the accepted publication tree before staging.

## Durability and concurrency hardening

The exporter fsyncs each staged file but does not fsync the staged directory hierarchy before renaming the tree. Sync every staged directory from leaves to root before writing the prepared marker. The adopter's swap path syncs both directory sides, but rollback syncs only the restored target parent after some cross-directory renames; sync both changed parents during rollback as well.

Neither script prevents another packaging process from modifying inputs or starting a second run between checks. A root-owned exclusive lock covering export inputs through commit, and covering acceptance inputs through adoption commit, would make the staged revalidation guarantees easier to reason about. A lock does not replace final staged hash checks.

## Disposition

The rewritten scripts are substantially safer and address the first review's central architecture defects. They are not yet ready for actual export or adoption because accepted operational source is incomplete, staged bytes are not revalidated against accepted identities, export interruption cannot recover, required raw evidence is incomplete, and the public archive is not acceptance-bound. These are host-only packaging defects and require no guest rerun. Correct the scripts and perform another bounded source review before execution. Current outcome remains `?`.

# Independent publication-source review

Review time: 2026-11-23T10:39:35Z

Scope: read-only audit of `export-round1.py`, `summarize-round1.py`, and `adopt-round1.py`. No publication or adoption was executed. This review makes no closure decision.

## Release-blocking findings

### 1. Malformed evidence can disappear from the summary

`summarize-round1.py:6-12` decodes with replacement and silently continues after every JSON parse error. It also silently drops valid JSON values that are not objects. A truncated or corrupted failed assertion can therefore vanish while the remaining rows produce a clean count. The output records neither malformed-line count nor line numbers.

`assertions()` then accepts every object with an ID and Boolean `passed`, regardless of phase, expected inventory, duplicate ID, or suite summary. It does not require a fixed count or fixed ID set for any log. A missing tail, missing assertion, duplicate passing row, or omitted suite row can reduce or distort the count without making publication fail.

Required correction: parse each evidence file under an explicit schema; reject unexpected malformed/non-record lines; require the exact preregistered result ID set and phase for each suite; reject duplicate IDs; reconcile result counts and failure IDs with the suite summary. If a log intentionally contains JSON strings or other transport lines, count and validate those separately rather than discarding them.

### 2. Verification parsing can hide bad or missing rows

`verify()` has two incompatible permissive modes. If it finds any JSON object with Boolean `ok`, it ignores every text `FAIL` line in the same file. If it finds none, it counts only recognized `OK` or `FAIL` forms and ignores every other line. Empty, truncated, malformed, mixed-format, or unexpected-status verification files can therefore appear as a smaller clean set, including zero rows.

Required correction: select one declared format per file, reject mixed or unknown lines, require the exact expected row count and unique identity set, and require `ok == rows` with no failure. For the current final readbacks, 553 is an observed consistency check, but the authoritative expected inventory should come from the declaration/readback contract rather than a hard-coded historical number alone.

### 3. Required carried logs are optional

`summarize-round1.py:38-40` silently omits any missing carried-suite log. Loading the aggregate carried summaries later does not prove that each named raw log was present or counted. The boundary-failure aggregate is also built only from `new`; carried and combined failures are not included, while its label does not explain that limitation.

Required correction: require every expected carried and combined evidence file; reconcile each exact ID/count with its aggregate summary; either aggregate all false observations or name each partial aggregate precisely. Missing evidence must stop summary generation.

### 4. Adoption mutates the retained state before all failure checks complete

`adopt-round1.py` copies recipe files and replaces the retained base image before checking raw-evidence destination collisions and the example destination. Any later assertion, move, write, or removal failure leaves a partially adopted tree and has already destroyed the preceding retained image. The candidate is deleted before the adoption record is durably written.

Required correction: perform a complete preflight first, including every source, destination, collision, symlink target, hash, mode, key set, and retained inventory. Stage and verify the full replacement tree without overwriting the retained tree. Commit through a recoverable journal or atomic directory swaps, keep the old retained image until all dependent moves succeed, write and sync the adoption record, and delete the duplicate candidate last. Recovery behavior must be explicit.

### 5. The retained recipe is incomplete and may contain stale files

`adopt-round1.py:22-24` copies only immediate regular files from candidate `build/` and `tools/`. Nested files, directories, and symlinks are omitted. Existing main-root files absent from the candidate remain in place. The resulting `build/` and `tools/` trees are therefore not necessarily the reviewed candidate recipe, despite the adoption record claiming `retained_recipe: build/`.

Required correction: compare a recursive typed inventory, stage an exact recursive copy with hashes and modes, reject unsafe symlinks, and replace the retained recipe tree as a unit. Preserve only explicitly listed main-root material outside that reviewed tree.

### 6. Key equality is checked in only one direction

The adoption loop verifies each immediate candidate key file against a same-named main key, but does not require the two key name/type sets to be equal. Extra main keys, nested entries, directories, and symlinks are not covered. Python optimization would also remove this and every other `assert` safety condition.

Required correction: require exact recursive key inventories with equal relative names, types, hashes, modes, and intended ownership. Express all safety conditions as unconditional checked errors, not `assert` statements.

## Export-specific findings

The exporter requires only the existence of the two completion summary paths; it does not validate their controller exits, ownership cleanup fields, peer completion, or required final evidence inventory. The main raw tree, candidate raw tree, and candidate example are treated as optional, even though all three are required publication inputs.

Both raw trees publish into the same archive namespace, which is appropriate only if their relative names are disjoint. Collision detection occurs during archive construction, after earlier source files may already have been normalized in place. A collision or later tar failure leaves a partial archive that blocks retry and may leave partially rewritten source evidence.

Normalization records pre- and published hashes for changed files, which is the right provenance shape. However, it rewrites the authoritative source files directly while streaming the archive. This can make existing source-hash manifests disagree with the now-normalized files and makes failure recovery ambiguous. The note also claims complete declarations retain exact bytes without enforcing a declaration-file exclusion or verifying that claim.

Required correction: validate completion fields and the exact three input roots first; compute the merged relative-name inventory and reject collisions before writing; stage normalized bytes without changing authoritative raw evidence; emit pre/post hashes and the applied replacement class; verify that protected declarations and frozen inputs remain exact; write a temporary archive, fully verify its inventory, then atomically rename it. If normalized server-side copies are required, place them in a distinct published tree and commit them only after the archive succeeds.

## Adoption preconditions that are correctly present but incomplete

The script does check final and supplement controller exits, reported remaining virtual machines, peer remaining state, candidate peer-directory absence, candidate image SHA-256 against `image.json`, image mode 0444, and post-replacement image SHA-256. It also requires the expected `example/round-1` child to be absent, which is compatible with an existing `example` channel symlink.

Before use, it must additionally verify that the `example` parent is exactly the intended symlink and resolves within the retained root, that all peer artifacts required as evidence are complete while no disposable peer remains, and that the final/combined/carried/independent-review acceptance inputs exist and agree. Operator intent to wait for review is not an executable precondition.

## Disposition

The three scripts are not safe to use for final publication or adoption in their current form. The summarizer can undercount or hide malformed/missing failures; the exporter is non-transactional and mutates evidence during streaming; the adopter can leave a partial retained state and does not preserve an exact reviewed recipe or exact key inventory. Fixes require a second source review before any publication archive or adoption is executed. Current outcome remains `?`.

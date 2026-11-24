# Independent publication-source review, revision 3

Review time: 2026-11-23T10:50:02Z

Scope: third bounded read-only audit of current `export-round1.py` and `adopt-round1.py`. The summarizer remains outside this review. No publication or adoption was executed, and no closure decision is made.

## Revision 2 findings now addressed

The current exporter and adopter bind the retained `build/`, `tools/`, and standalone controller to recursive typed inventories stored in the publication manifest. Adoption checks those inventories at source, checks the staged copies, and checks the source inventories again immediately before journaling.

The staged image is rechecked for exact SHA-256 and mode 0444. Staged publication files and external acceptance, metrics, and review copies are rechecked against fixed accepted hashes. The accepted archive SHA-256, member count, member names, safety properties, and member contents are all checked before adoption.

Exporter recovery now handles every normal prepared state: neither rename completed, only the tree rename completed, or both renames completed. It validates the exact tree/archive pair before completing remaining renames and removes the prepared marker only after syncing the final pair. The staged directory hierarchy is synced before the marker is made durable.

The explicit required list now includes combined events and the supplement's reboot, before/after readbacks and reports, input manifest, image identity, controller steps, and lifecycle logs. Adoption rollback syncs both sides of its cross-directory renames. Committed cleanup retains acceptance, metrics, review, publication manifest, and adoption proof inside the adopted raw tree before removing duplicate external artifacts.

No material fault was found in the stated export recovery state machine or adoption swap/rollback state machine during source analysis. Both files also parse successfully as current Python syntax.

## Remaining material finding

The exporter requires `final-2/supplement/input-sha256.json`, but it does not require the separately frozen supplemental payload directory and its outer source-hash record, nor compare those frozen payload bytes with the supplement input manifest. Those payloads are expected to enter through the merged main raw tree if present, but the required-file preflight does not make their presence or identity mandatory.

Publication can therefore succeed with direct and extra result logs plus an input-hash JSON while omitting the exact payload files those hashes are meant to identify. That weakens independent replay and makes the input identity claim depend on an unchecked optional directory.

Required correction: require the frozen final-2 supplemental input directory and source-hash record at their designated raw paths; require the exact expected file-name set; compare every frozen file SHA-256 with both the outer source-hash record and `final-2/supplement/input-sha256.json`; protect these files from normalization; and include them in the publication inventory. This is a host-only evidence check and needs no guest rerun.

## Archive metadata check

Archive creation explicitly clears numeric owner/group IDs, owner/group names, and sets a public file mode. The verification paths currently validate file type, names, and contents but do not assert those sanitized header fields. This is not a creation-path failure because the filter sets them directly, but checking `uid == 0`, `gid == 0`, empty names, and the intended mode during export recovery and adoption would make the stated privacy property self-verifying.

## Disposition

The architecture and transaction safety findings from revision 2 are resolved. Export and adoption remain blocked on the missing mandatory verification of frozen supplemental payloads, and independently on completion of the strict summarizer review. After adding that bounded input check, the export/adoption sources need only a focused confirmation; no guest rerun or broad packaging redesign is indicated. Current outcome remains `?`.

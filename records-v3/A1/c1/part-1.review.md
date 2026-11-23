# Review of c1 part 1

Scope: methodological and factual review of the currently available `part-1` c1 records. This review did not change any classification and does not decide unresolved alternative readings.

## Findings

1. **Mixed membership is not explicit in the allowed root records.** Several `MIXED` rows say that the full or exact partition is in `part-1.root.notes.md`, but that file currently ends after a general statement about stored rows and contains no member partitions. This affects at least `coreos-23a9706caf`, `coreos-809cb439ce`, `coreos-f12cddbc22`, `coreos-0075a76d48`, `coreos-23f2259103`, `coreos-57da4d32dc`, and `coreos-2d7adb8ef6`. Category summaries such as “MUST: policy and labeling inputs” do not identify which members received each decision.

2. **The `/etc/alternatives` mixed summary contains a factual count error.** `coreos-809cb439ce` says there are five `*-man` links. `../in/raw/coreos/unowned-groups.json` lists four: `arptables-man`, `arptables-restore-man`, `arptables-save-man`, and `ebtables-man`. This row also needs the promised exact member partition.

3. **The `/boot/grub2` treatment is not grounded for its module-index members.** `coreos-23a9706caf` classifies “module indexes” as MUST using only `../in/raw/coreos/unowned-groups.json`. The raw record establishes names and file metadata, not whether the `.lst` files are executed as code, read as values, or consumed outside one program. Because S2.2-7 and S2.2-13 distinguish program-internal settings and value files from executed code, S3-1 requires documentation, observation, or removal evidence before assigning those members. This is an evidence defect; the review does not choose their decisions.

4. **`grub2-pc-modules` has an incorrect function claim and sentence basis.** Package row `coreos-aae56aa09f` cites S2.2-9 and says it “supplies an executable program,” while its cited description says “Modules used to build custom grub images.” That source does not establish a standalone program. The row needs evidence of how the modules execute and, if supported, the corresponding code rule; its current reason is factually unsupported. This does not by itself establish that the final decision must change.

5. **Grouped package-owned decisions lack member-level behavioral evidence in the allowed records.** Mixed rows point to `part-1.owned.members.tsv`, while `part-1.owned.notes.md` supplies only aggregate counts and broad labels for those groups. For example, `coreos-17a7caf72b` assigns 938 `/etc/pki` members among MUST, NOT, and UNKNOWN, but its basis is `../in/raw/coreos/files.tsv`, which records only type, path, link target, and size; the notes provide no member reasons or documentation. The statement that “reasons and documented functions are in notes” is therefore false for the current notes. The same defect applies to other grouped rows serialized from path metadata. Exact member decisions and the documentation, observation, or removal evidence establishing each non-UNKNOWN function are required by S3-1.

## Checks that passed

- All current result rows use only S2.2 and S3-1/S3-2 sentence IDs.
- All current `what_it_does` fields are at most 15 words and all `reason` fields are at most 30 words.
- The account, kernel-module, process, loaded-unit, and directory-only homogeneous rules each record at least ten named handchecks. The package rule records thirty named checks and does not classify packages from package presence alone.
- No prohibited personal or machine paths, or system-attribution language, were found in the reviewed result and notes files.

## Follow-up review

The explicit root and owned member tables, expanded notes, and corrected result rows resolve findings 1, 2, 3, and 5 above at the member-decision level. The alternatives count is now four. Seven unverified GRUB `.lst` files are UNKNOWN, while `fs.lst` has a primary source showing that GRUB reads it to autoload executable filesystem modules. The owned records now provide deterministic ordinal partitions and documented function classes. Password history, saved clock drift, and the migration stamp are now NOT under the explicit S2.2-3/S2.2-6 exception, consistently with the root treatment of completion stamps and timer history.

Two remaining record defects were found:

1. **The aggregate GRUB row contradicts its corrected member table.** `coreos-23a9706caf` still says “MUST: boot code, commands and module indexes,” although `command.lst`, `crypto.lst`, `moddep.lst`, `partmap.lst`, `parttool.lst`, `terminal.lst`, and `video.lst` are now UNKNOWN. Its sentence list also omits S3-2. The aggregate reason and sentences must describe the final partition; the member decisions themselves are now supported.

2. **The `grub2-pc-modules` correction is not yet linked to evidence establishing execution.** `coreos-aae56aa09f` now correctly uses S2.2-10 and calls the files executable bootloader modules, but its basis still points only to the metadata summary “Modules used to build custom grub images.” `part-1.packages.notes.md` contains no package-specific execution source or correction note. The GRUB loader source already cited in `part-1.root.notes.md` can establish that native modules are loaded as code, but the package row or its package notes must point to that evidence. Thus prior finding 4 is semantically corrected but not fully resolved under the evidence-first rule.

The earlier owned-note summaries still display the superseded HOLE counts for password history and drift before a final correction paragraph. Because that paragraph explicitly supersedes them and the TSV/member table agree, this is not a classification inconsistency; updating the stale summaries would make the published record easier to audit.

## Final resolution check

The merged 1,222-row `part-1.tsv` resolves the aggregate GRUB contradiction: `coreos-23a9706caf` now includes S3-2 and explicitly separates `fs.lst` from the seven UNKNOWN indexes. Its member table and source notes agree. The explicit-exception corrections for password history and clock drift also agree between the merged TSV and owned member table. Automated structural verification is reported as passing; an independent scan found no function or reason over the fixed word limits.

The only residual review point is evidence linkage for `coreos-aae56aa09f`. The combined notes contain a primary GRUB loader source establishing native module execution, so the factual claim is now supportable. The row's own `basis`, however, links only to package metadata saying the files are modules used to build images, and the package section does not direct this row to the loader source. This is a traceability defect rather than an unresolved classification or semantic error. All other findings from this review are resolved in the final merged records.

## Evidence-linkage correction

The remaining traceability point was corrected: coreos-aae56aa09f now cites the primary GRUB loader source directly in both the merged and package TSVs. Package notes and combined notes explicitly connect the package file list to native module execution. Its decision is unchanged.

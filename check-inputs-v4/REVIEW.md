VERDICT: DISAGREE

# Review of the check 1 and check 4 inputs, the inputs beyond the plan and the laboratory kit

Reviewed 2026-11-23, 08:00–08:20 UTC, against TEXT.md Sections 9.1, 9.2, 9.5 and Appendix A.4.1, A.4.5. The review took
no part in the work. It read the documents named in its brief, the retained `status.tsv`/`counts.tsv` tables, the
rehearsal notes and eight release or collector evidence files. It read no guest output and no raw inventory.
On the laboratory server it listed running processes and unit names only. Paths are relative to `C1/`.

## Findings

1. **The final input manifest no longer matches the files.** Where: `input-files.sha256.tsv`, `PUBLISH.list`.
   Evidence: checking all 223 rows of the manifest gives 5 mismatches (`CHOICES.md`, `KIT2-READY.md`,
   `rehearsal/fedora/status.tsv`, `rehearsal/fedora/counts.tsv`, `rehearsal/mint/NOTES.md`) and 1 missing file
   (`rehearsal/REVIEW-FINAL.md`, also listed in `PUBLISH.list`). The manifest was written at 07:59 UTC; these files
   changed at 08:02 UTC. Also, `CHOICES.md` now ends with the sentence that makes attempt 6 the active MicroOS recipe,
   and the copy of `CHOICES.md` inside `DISCLOSURES.md` does not have it. Minimal fix: once all writers have stopped,
   regenerate `DISCLOSURES.md`, `input-files.sha256.tsv` and `PUBLISH.list`, and add or remove
   `rehearsal/REVIEW-FINAL.md`.

2. **Rehearsals still run after the inputs were declared final, and the records already disagree.** Where: the
   laboratory server, `READY.md`, `DISCLOSURES.md`. Evidence: at 08:06 UTC, after the task ended at 08:03:47 UTC, these
   were still running: `c1-reh-gentoo-1` (VM up about 43 min), `c1-reh-guix-3` (VM started at about 07:58 UTC) and a VM
   `reh-alma-3` started at about 08:02 UTC. Fedora round 2 was appended at 08:02 UTC: actions exit 1
   (`developer_second_package_manager` 56), collector exit 0 in 225.013 s, 6055 L2 rows, 1679/2248 known reasons.
   `READY.md` and the `DISCLOSURES.md` table report Fedora round 1 only. `rehearsal/mint/NOTES.md` reports a round 4
   (7 of 9 actions zero, 350.301 s). `status.tsv` has no round 4, and `READY.md` reports round 3. The task wanted the
   inputs "exactly as they will be committed". Minimal fix: stop or finish these runs and destroy their clones, then
   rebuild `READY.md` and the `DISCLOSURES.md` tables from the final status files. Use the latest round of each
   system, or say which round is reported and why.

3. **The MicroOS release and checksum in the inputs are for an image that is not used.** Where: `releases.tsv`,
   `inputs-check-1.md` table. Evidence: both list `Snapshot20261121 x86_64 DVD` with SHA256 `512654d3…2e58`. The
   active base is the vendor image `openSUSE-MicroOS.x86_64-16.0.0-kvm-and-xen-Snapshot20261121.qcow2` (`CHOICES.md`,
   KIT2 section; `KIT2-READY.md`). The checksum of that image appears in no input document. Its publication before the
   cutoff is shown by `raw/microos-kit2/appliances.html` (22-Nov-2026 03:08). A.4.1 requires the release numbers to be
   fixed in advance, and the task requires releases with checksums. Minimal fix: add a row for the qcow2 image with its
   published SHA256, its signature reference and the listing date. Mark the DVD row as a superseded attempt.

4. **MicroOS was not rehearsed, and READY.md gives a reason that the records contradict.** Where: `READY.md` microos
   row, `rehearsal/`. Evidence: `KIT2-READY.md` reports MicroOS ready at 07:58:08 UTC with a registered base.
   TASK-C1-REH says that every system KIT2 reports ready gets its rehearsals. There is no `rehearsal/microos/`
   directory. `READY.md` says "no usable base/rehearsal completed by finalization" and cites
   `rehearsal/microos/status.tsv` and `counts.tsv`, which do not exist. Minimal fix: rehearse MicroOS (actions do not
   apply; run the collector and 20 transport calls). Otherwise state in `READY.md` and `inputs-check-1.md` that it was
   not rehearsed, with the real reason, and remove the citation of files that do not exist.

5. **The Gentoo row does not match its notes, and its evidence files are missing.** Where: `READY.md` gentoo row,
   `rehearsal/gentoo/`. Evidence: `READY.md` says "0/9 zero … no usable base" and cites `rehearsal/gentoo/status.tsv`
   and `counts.tsv`. The folder holds only `NOTES.md`. The notes say that the twenty transport calls returned zero,
   that the first action returned 0, that `application_package` returned 1, and that the batch was still active. The
   base exists (`KIT-READY.md`: Gentoo ready). The same kind of missing citation exists for `rehearsal/nixos/counts.tsv`
   and `rehearsal/guix/counts.tsv`. Guix rounds 2 and 3, which `rehearsal/guix/NOTES.md` describes, have no rows in
   `rehearsal/guix/status.tsv`. Minimal fix: keep the numeric status tables of every round actually run, and make the
   rows and citations in `READY.md` match them ("transport 20/20 zero; actions 1 zero, 1 nonzero, 7 incomplete").

6. **Three releases have no saved evidence that they were the latest stable release at the cutoff.** Where:
   `releases.tsv`. Evidence from the sample: `raw/talos/release.json` is the page of the v1.14.6 tag, not a list of
   releases. `raw/nixos/channel-headers.txt` shows a redirect to 26.05.14979 but does not show the requested URL or that
   no newer stable branch exists. For Void, the claim "official current listing agrees" has no saved listing (`raw/void/`
   holds only checksum, signature, key and timeline files). The selections themselves are right; the review checked
   them by reading the public sources. The GitHub releases list of Talos shows v1.14.6 (2026-11-11) as the newest
   non-prerelease, with only v1.15.0 alpha and beta before it. `channels.nixos.org/nixos-26.11` returns 404. In
   `repo-default.voidlinux.org/live/`, `current` dates from 02-Feb-2025, and the later `20250401` directory holds only
   "enterprise" images. Alma, Gentoo, MicroOS and Guix do have such evidence (`raw/alma/sources.txt`,
   `raw/gentoo/latest-stage3.txt`, `raw/microos/releases.html`, `raw/guix/release-index.html`). Minimal fix: save the
   three listings, dated, under `raw/` and cite them in `releases.tsv`.

7. **Files to be published contain home paths of our laboratory host.** Where: 48 files under `install/recipes/` (for
   example `install/recipes/alma/install.sh.in:3` `base="LAB_ROOT"`,
   `install/recipes/void/console-bootstrap.py.in:7` `LAB_ROOT/void/serial.sock`,
   `install/recipes/debian/validate.py.in:5,16,17`). Paths into the previous night's laboratory also appear
   (`install/recipes/guix/kit2-reuse.sh.in:4` `../cal-1122/C1/base/guix.qcow2`,
   `install/recipes/fedora/attempt1-driver.py.in:7`). COMMON.md forbids home paths of our machines in published records.
   No other forbidden name (person, host) was found in the 223 published files. Minimal fix: replace them with a
   `LAB_ROOT`-relative placeholder, which `install/materialize.py` already supports, and regenerate the checksums.

8. **Two image-variant choices without a default are not stated.** Where: `CHOICES.md`. Evidence: the Talos release
   publishes several images, and `metal-amd64.iso` is used (`releases.tsv`). The Talos section of `CHOICES.md` states
   only the node and endpoint choices, and `parts/talos-choices.md` does not mention the image. For MicroOS, the
   appliance index offers plain, `grub-bls` and `sdboot` KVM/XEN images of Snapshot20261121
   (`raw/microos-kit2/appliances.html`). `CHOICES.md` justifies plain against Container Host only. Minimal fix: state
   both as choices of this check, each with its documentation passage.

9. **The review file of the kit is overwritten by this review.** Where: `REVIEW.md`. Evidence: the earlier file "Initial
   independent review of C1-KIT" (SHA256 `dfc78244…58b6`) is linked from `KIT-READY.md` and listed in `KIT-SHA256SUMS`
   and `build-manifest.py`. A.4.1 says that records are never deleted. Before writing, this review copied that file
   byte for byte to `REVIEW-KIT.md`. Minimal fix: point the link in `KIT-READY.md` and the entry in `KIT-SHA256SUMS` to
   `REVIEW-KIT.md`.

## Checked without a finding

- Text (1): `inputs-check-1.md` quotes the five lines of Section 9.2 exactly. It reports a machine without a second
  level by the rule of Section 9.2, adds no agreement threshold or decision rule, and keeps the case list of five
  systems. `inputs-check-4.md` names the six cases and the A.4.5 facts for P1, P2 and P4 of Section 8.3. No property is
  assessed. `inputs-beyond-plan.md` places the three lived-in machines outside the four checks.
- Collector: `COLLECT.md` records a reason (explicit, dependency or unknown) and per-file integrity for each supported
  manager, and names the unsupported cases. The rehearsals show that neither fact is complete on any check system
  (for example Alma 1006/1561 reasons known and 102/1561 packages with every file known; Talos 0/1). `READY.md` reports
  this as not ready and does not relabel unknowns. The Section 9.2 requirement is therefore not yet met, and the
  records say so.
- Numbers (2): every row of `READY.md` and of the `DISCLOSURES.md` table matches its `status.tsv`/`counts.tsv` for the
  round it names (Alma round 2, Void round 4, Talos, Mint round 3, debian-server, NixOS, Guix round 1). The mismatches
  in findings 2 and 5 are rounds that are missing or out of date.
- Observation (4): the retained tables hold only statuses, durations, byte sizes and counts per kind. Exposure of
  account identifiers in query labels on Alma is disclosed (`rehearsal/EXPOSURES.md`, included in `DISCLOSURES.md`).
  The review found no other content of a check machine. No published file is larger than 300 kB.

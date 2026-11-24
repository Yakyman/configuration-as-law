# Void preparation

UTC 2026-11-23. Rehearsals only; no object decisions.

## Prior sources and expected results

Before the first probe: the [Void kernel manual](https://docs.voidlinux.org/config/kernel.html)
says “When updating the kernel, old versions are left behind in case it is necessary to roll back to an older version.” This explains retention but does not establish receipt equality.
The [npm lock documentation](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/)
specifies integrity as the archive's integrity value. The
[cacache implementation](https://github.com/npm/cacache/blob/main/lib/content/path.js)
maps digest bytes to its content-v2 hierarchy. The collector will verify archive integrity before comparing each member; presence alone proves nothing.

Expected rehearsal result: current npm cache archives and lock entries will permit complete member hashes;
old kernel files may lack their original receipt after the installed package manifest is replaced.
Three distinct evidence routes for old files are the surviving installed manifests, residual metadata,
and package-cache archive manifests. These are read-only queries, not another installation.
Historical human choice or creator is not recoverable from an unaudited current state alone.

## Counts from the two named tables

The original Void set has 75 rows: 52 npm stored groups and 2 npm executable rows;
12 account/group/access rows; 3 opaque stores; 6 other stored groups.
The additional table contains 1,069 retained old-version groups, including the boot group.
The other stored groups are default settings (1), module settings (1), sudo rules (1),
store parent (1), mount directory creator (1), trust-key selection (1).
Counts describe dependencies, not decisions.

## Module interface and files

`check-inputs-v4/supplement-1/step-4-instruments/S4/collector/extra_void.py` exports `collect_npm(ctx)` and `collect(ctx)`; call after
ordinary object reduction. Neither changes the two levels or existing membership.

- `npm-archive-sources.tsv`: `lock, package_root, resolved, integrity, cache, status, evidence`.
  Resolves each installed package root to its local lock receipt and cached archive;
  cache bytes must match the recorded SRI digest. No network fetch is performed.
- `npm-member-integrity.tsv`: `object_ids, package_root, path, algorithm, expected, actual, status, evidence`.
  JSON `object_ids` lists the direct object and immediate containing L2 group, where present.
  Equal means full current bytes equal the archive's member bytes; directories are distinct;
  unlisted installed extras are explicitly `not-compared-to-archive`.
- `old-package-receipt-sources.tsv`: `source, status, evidence`.
  Records the readability of installed/residual Linux package metadata and cached archive manifests.
- `old-package-member-integrity.tsv`: `object_ids, path, source, type, expected, actual, status, evidence`.
  Paths without a surviving receipt stay `no-surviving-receipt`; a kernel-looking filename is not proof
  of package origin. Receipt equality does not identify who chose installation.
- `void-configuration-facts.tsv`: `object_ids, path, status, content_base64, historical_creator, evidence`.
  Contains bounded current default/module/sudo/key file contents; historical creator remains explicitly unknown.

All listed columns are tab-separated. Join `object_ids` to new `objects.tsv:id`.
For a grouped object, its existing `members/<id>.tsv:path` leads to the exact fact row.
The baseline collector identity, levels, group names and members remain unchanged.

Synthetic module checks: `parts/void-module-check.py` verifies accepted archive integrity and rejection
of a tampered cache; two cases passed. These synthetic fixtures are deleted automatically.

## Operator command

After the exact ordinary actions from `check-inputs-v4/actions/void.sh`, from the laboratory root:

```sh
LAB_ROOT=LAB C1_INPUTS_COMMIT=INPUT_COMMIT check-inputs-v4/supplement-1/step-4-instruments/S4/collect.sh --observe TARGET OUTPUT
```

`LAB` is the prepared runner directory, `TARGET` a fresh registered Void clone and `OUTPUT`
a nonexistent output directory. `INPUT_COMMIT` is the commit containing the published S4 inputs.
The operator substitutes these values; the collector cannot target the host.

XBPS archive layout is fixed by [xbps-create source](https://raw.githubusercontent.com/void-linux/xbps/master/bin/xbps-create/main.c): the writer appends `./files.plist` before package data. The collector reads that exact member without extracting files.

## Rehearsal 1 and planned repair

Boot 0 / 16.227 seconds; ordinary actions 0 / 284.993 seconds (all nine activities and three language substeps zero);
collector 0 / 90.381 seconds; destroy 0 / 4.179 seconds. Numeric evidence:
`rehearsal/void/status.tsv`, `actions.tsv`, `fact-summary.json`.
Rehearsal inventory deleted; the clone destroyed. Only diagnostics and numeric reductions copied.
Allowed diagnostic reads: collector stderr, coverage, cached-manifest stderr and numeric summary.
One completion-monitor transport returned 255 and recovered; no ordinary action was rerun.

npm: 41 archives verified; 459 full member comparisons equal; 23 directory records.
Full-digest common adapter: 11,317 requested and recorded. Three stores traversed completely.
Old package cache route failed because GNU tar attempted absent `zstd`; nine query failures are retained.
This is an instrument defect, not evidence that receipts are absent.

Before repair rehearsal: [libarchive read API](https://raw.githubusercontent.com/libarchive/libarchive/master/libarchive/archive_read.3)
describes archive reading with filter and format support. The existing XBPS runtime uses libarchive;
reading the exact `./files.plist` member through that library should avoid dependence on a missing
external decompressor. Expected: cached manifests become readable; retained old files lacking any
original cached receipt still remain unsupported. The repair neither installs a package nor executes archive contents.

The reusable npm adapter now has three distinct reference routes: a project/hidden lock,
installed `package.json` `_integrity`, and checksum-validated cacache index entries pointing
to an exact package name/version archive. The latter additionally checks the archive's
internal `package.json` identity. Its explicit status is
`verified-archive:cache-identity-reference-not-install-receipt`: equality to a same-release
cached artifact is a physical comparison, not proof that this was the installed receipt.
This distinction is also retained as an aggregate counter. An installed metadata digest
is labeled `installed-metadata-reference`; lock evidence is labeled `lock-receipt-reference`.
Two additional synthetic checks for unlocked references passed.

Rehearsal 2 uses a fresh clone and the identical ordinary actions. Planned repair facts:
archive extraction should succeed through the existing libarchive; unsupported old receipt
paths must remain explicit. Output inventories will again be deleted unread.

## Rehearsal 2 result and final source validation

`rehearsal/void/round2/status.tsv`: boot 0 / 23.253 seconds; actions 0 / 345.786 seconds;
collector 0 / 78.376 seconds; destroy 0 / 3.842 seconds. All nine cache manifest queries
succeeded through libarchive (coverage entries 135–143). npm retained 41 verified lock
archives and 459 equal complete member hashes. Full hashes: 11,308 of 11,308.
Three store traversals completed. Both clone and unread inventory were verified absent.

All 22,282 successful kernel receipt comparisons refer to already owned paths;
no unowned retained file gained an original receipt. 6,859 kernel/boot entries have
no surviving receipt. The three distinct routes—current installed manifests,
residual old metadata, and cached package archives—do not establish the original
receipt of the 1,069 first-night old-version groups. They are not obtainable from
these surviving records. Historical creator/chooser facts likewise remain unknown
without an actual creation event or an installation record that identifies the choice.

Final validation uses a fresh third clone after the common adapter's directory-index
implementation was made linear without changing its output. No historical query is
repeated with a changed meaning. The final run records all source hashes before
startup and again before cleanup. Its inventory will be deleted unread.

The [official downgrade documentation](https://docs.voidlinux.org/xbps/advanced-usage.html)
explains that an unavailable old version must be obtained elsewhere if its cached archive is absent.
No independently authenticated archive reference for the retained original version was supplied by
these three routes. This is a limitation of the available records, not a claim that no archive could
exist anywhere. The collector does not rebuild a package and treat the new build as its old receipt.

## Final validation result

`rehearsal/void/round3/status.tsv`: boot 0 / 23.250 seconds; ordinary actions 0 / 284.942 seconds;
collector 0 / 60.162 seconds; destroy 0 / 3.933 seconds. `actions.tsv` has zero for all
nine main activities and three language substeps. The three attempts all destroyed their clones;
final absence of the clone directory and unread inventory directory was verified.

Final numeric facts (`round3/fact-summary.json`): 41 verified lock-reference archives,
459 complete npm member comparisons equal, 23 npm directory rows; full hashes 11,310 of
11,310 requested; three store listings complete, 72,162 members, zero inner opaque boundaries.
Listing completion does not by itself establish store image provenance or receipt integrity.
Old-package routes still provide no receipt for 6,859 kernel/boot entries, and zero retained
unowned members have a receipt. The old-version fact for the 1,069 first-night groups remains
unavailable from the surviving records. Historical creator/chooser facts remain unavailable.

`round3/input-sha256.tsv` and `input-sha256-after.tsv` establish stable bytes for
`check-inputs-v4/supplement-1/step-4-instruments/S4/collect.sh`, `check-inputs-v4/supplement-1/step-4-instruments/S4/collector/main.py`, `check-inputs-v4/supplement-1/step-4-instruments/S4/collector/extended.py`, `packages.py`, `check-inputs-v4/supplement-1/step-4-instruments/S4/collector/extra_void.py`, and the
static helper; each also matches the corresponding local final file. Only the unrelated
Talos adapter changed during the run; it is not imported for Void.
The final run uses the optimized common adapter; rounds 1 and 2 use its earlier implementation.
This is a successful instrument rehearsal with stated factual limitations, not independent acceptance.
Independent acceptance belongs to RV-S4-P.

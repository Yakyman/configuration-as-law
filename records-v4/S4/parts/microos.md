# MicroOS extended collector rehearsal

Prepared 2026-11-23 UTC. Instrument preparation only; no object decisions. Independent acceptance belongs to RV-S4-P. Primary sources, expectations written before each attempt, and output schemas are in `microos-plan.md`.

## Result

Ready for collection of the obtainable current facts. Final fresh-copy source-validation run 3: boot 0 in 23.605 s; collector 0 in 87.505 s; destroy 0 in 0.957 s. No ordinary action is assigned to this system. Evidence: `S4/rehearsal/microos/round-3/status.tsv`. All new s4-prefixed queries returned 0 (`round-3/coverage.tsv`).

Numeric diagnostic evidence (`round-3/counts.tsv`):

| Fact mechanism | Recorded count |
|---|---:|
| Active /etc descendants traversed | 2219 |
| Unit and user-unit source selections | 263/263 |
| Snapshot-specific RPM manifests | 2 |
| Snapshot package manifest file/directory rows | 20400 |
| Snapshot complete package digest/target comparisons | 15837 |
| Snapshot/current complete SHA256 comparisons | 16177/16177 |
| Current unit/policy/sysusers source files read | 1318 |
| SELinux policy stores listed with checksums | 2 |
| @System solv cache decoded | 1 |
| Solver cache files with content/digest evidence | 3 |
| Common extension full digests | 18401/18405 |

These are mechanism counters, not claims that every historically unknown object has a deciding fact. The common digest mechanism retains four unknown full hashes. The original package-file mechanism still reports 294 unknown file/target records. No unknown is inferred from a numerical total to be a specific missing row.

## Attempts and diagnostics

Attempt 1 boot 23.614 s, collector 0 in 119.146 s, destroy 0 in 1.263 s. Its active/etc and snapshot mechanisms succeeded; unit selection 9/263 and cache decode 0 disclosed two instrument defects. `systemctl show` rejected uninstantiated template names and stopped each batch. Installed guest dumpsolv was absent, status 127. The second attempt uses documented `systemctl cat` for templates and batched show for ordinary units; all 263 selections now have evidence. It reads bounded cache bytes safely and uses the already installed host dumpsolv on stdin; guest state is unchanged. The host child is limited to 60 s and 64 MiB output; input read limit 16 MiB. Final source is `check-inputs-v4/supplement-1/step-4-instruments/S4/collector/extra_microos.py`.

An initial durable-service launch rejected percent expansion in WorkingDirectory before any machine command. Shell expansion fixed that launcher; this was no additional machine attempt. Evidence: `launch-status.tsv`.

Only diagnostics, aggregate counters and source code were inspected. All three rehearsal inventories were deleted unread. The final cleanup check found zero VM directories and zero transient inventories (`round-3/cleanup.tsv`). The first attempt evidence is directly in `S4/rehearsal/microos/`; the second is under `round-2/`.

## Missing-fact counts and remaining limits

The 754 original table rows group as 22 account/group creation-history rows,8 sudo-source rows,253 current unit/user-unit definition/link rows,7 unit definition/enablement-history rows,10 executable snapshot receipt/integrity rows,452 stored snapshot receipt/integrity rows,1 active/etc row and 1 grubenv content/creation row. D1 RESULT additionally names the inactive RPM database and @System solver cache; corresponding database and decoder evidence is added without counting them in 754.

Recorded current facts: active/etc membership and source contents; actual selected unit fragments/drop-ins and current enablement links; snapshot-root RPM identities and recorded expected hashes/targets; complete actual hashes; current-vs-snapshot equality; grubenv bytes; SELinux module identities/format/checksums; inactive RPM database package records; original solver-cache contents/cookie/checksum.

Not established by these queries: historical human choice versus installation defaults for accounts/groups or enablement; who created a sudo/boot value; original package receipt for generated or unowned snapshot files absent a matching snapshot installation record; historical cache creation cause merely from present identity equality. Current source/scriptlet equality and timestamp equality are not substitutes. No query can reconstruct an unretained historical event solely from identical final states. The collector supplies retained sources for later independent decision without deciding that they prove a cause.

## Operator commands

Run from the laboratory root with `S4_INPUTS` set to the absolute directory containing the committed S4 inputs and `COMMIT` to that inputs commit:

```sh
command -v dumpsolv
./lab.sh new d1b-microos microos
C1_INPUTS_COMMIT="$COMMIT" LAB_ROOT="$PWD" "$S4_INPUTS/collect.sh" --observe d1b-microos D1b/raw/microos
./lab.sh destroy d1b-microos
```

No ordinary-action command belongs between boot and collection. These commands are for the separately authorized observation, not performed in this task. The operator retains failure status and does not repair/retry observation commands.

## Final assembled-source validation

Run 3 validates the common extension's equivalent parent-map index optimization on another fresh throwaway copy. Query methods and the MicroOS module remain unchanged. It is the selected final run: collector0 in87.505s. New fact mechanism counters equal run2; the general scan contains two more transient entries and one more unknown full hash, with no object-level inference made. All s4-prefixed queries return0. Exact before/after hashes are identical and match the local final source for main.py, extended.py, packages.py, extra_microos.py, probe.go and probe-linux-amd64.gz. Evidence: round-3/{before,after}.sha256.tsv; round-3/status.tsv; round-3/counts.tsv; round-3/coverage.tsv; round-3/cleanup.tsv. The inventory and copy were deleted; cleanup counters are both0.

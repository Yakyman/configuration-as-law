D1b INVENTORY: 4 of 5 machines; 34708 objects to decide; 74 first-night objects without a match

2026-11-23 UTC. Operator inventory handoff; independent step review remains responsible for acceptance.

The headline counts delivered inventories. All five original observations were obtained and preserved; four handoff copies succeeded. AlmaLinux is not delivered and gives **?** under the committed handoff-failure rule. No object decision is supplied by this record.

Inputs: gate (not published: orchestration or scratch), commit `c62afbb5861fb038aa7da0aa00c0730ad140ec7c`. The required `/usr/bin/python3 -I S4/verify-inputs.py` passed before the first machine; every staged copy also passed. All 49 hash-covered files match; the manifest excludes itself. Release references: `check-inputs-v4/KIT-READY.md`, and for the final MicroOS installation `check-inputs-v4/KIT2-READY.md`, both referenced by `check-inputs-v4/LAB.md`.

One operator per machine, no nested work. Gentoo started first with ten free slots observed and four held by its VM; its successful startup preceded the other starts. Every machine was created once and destroyed after its one collector invocation. Native destruction succeeded on all five; no cleanup fallback was needed.

| Machine | Original rows (L1 / L2) | Delivered all | Objects to decide | First-night unmatched | Handoff exit |
|---|---:|---:|---:|---:|---:|
| alma | 5711 (4026 / 1685) | 0 | 0 | 66 | 1 |
| void | 3279 (1211 / 2068) | 3279 | 1143 | 1 | 0 |
| gentoo | 32775 (1210 / 31565) | 32775 | 32775 | 0 | 0 |
| microos | 6567 (1464 / 5103) | 6567 | 747 | 7 | 0 |
| talos | 278 (225 / 53) | 278 | 43 | 0 | 0 |

All five copier exit statuses, exact commands and durations: `operator/handoff-status.tsv`. Successful complete audits: `D1b/handoff-audit/{void,gentoo,microos,talos}.json`. AlmaLinux produced no audit or deliverable tree: its exact terminal diagnostic is `_csv.Error: field larger than field limit (131072)` in `operator/handoff-alma.stderr`. The copier was not changed or rerun. All 5,711 original AlmaLinux IDs are listed in `not-delivered-alma.tsv`; its all/part tables contain only the required header.

The unchanged matcher ran once per machine with both fixed old tables; all five exits were 0 (`operator/match-status.tsv`). Complete outputs remain in `match/MACHINE/`; machine-specific lists are `match/matched-MACHINE.tsv` and `match/unmatched-MACHINE.tsv`. New IDs in those outputs are unchanged raw IDs; `object-id-map.tsv` maps them to the required prefixed table IDs. Of 2,007 fixed first-night IDs, 1,933 match delivered rows and 74 remain unmatched: 66 AlmaLinux IDs with no delivered inventory, one Void ambiguous-new-key ID, and seven MicroOS ambiguous-first-night-key IDs. All are listed by ID and receive no decision here. No extra first-night input or matching rule was added.

Every delivered collector row is preserved in `all-MACHINE.tsv`, in source order. The four non-Gentoo part tables contain exactly matched delivered rows; Gentoo contains all 32,775 rows. Names, machine, members and evidence cells are unchanged. The only table transformations are the required ID prefix, part column and level prefix on kind. Full schemas, fact paths, ID joins, membership and persistence fields are in `FACTS.md`; `MISSING-RECORDED.tsv` records all 45 requested fact groups and their explicit limits.

## alma

Committed release: **AlmaLinux 10.3**. new 0 / 16.425 s; collector 0 / 124.580 s; destroy 0 / 2.850 s.

Raw level two was obtained in part: filesystem_complete=true, package_ownership_complete=false, with atomic images/stores and unresolved ownership. No level-two rows were delivered because the handoff failed.

Lifecycle, complete separate command outputs and diagnostics: `operator/alma/`; machine record: (not published: orchestration or scratch). Collector coverage and all failed query streams remain under `D1b/raw/alma/coverage.tsv` and its referenced `raw/` files. Nonzero optional queries were retained, never repaired or repeated.

Ordinary actions (`operator/alma/action-evidence/actions-status.tsv`):

| Action | Exit | Seconds |
|---|---:|---:|
| package_program | 0 | 12 |
| application_package | 0 | 38 |
| language_program | 0 | 14 |
| browser_extension | 0 | 19 |
| personal_setting | 0 | 4 |
| user_service | 0 | 4 |
| network_connection | 0 | 1 |
| home_script | 0 | 0 |
| container_run | 0 | 4 |

Facts requested in `S4/MISSING.tsv` (the detailed evidence paths are in `MISSING-RECORDED.tsv`):

| Fact | Recorded fields and limits |
|---|---|
| A01 | source references only: 41 verified npm archives; no per-object acquisition-event field. **Not delivered.** |
| A02 | current sources recorded: 19 installer-directive rows and current values, including nine nonsecret network-profile rows. **Not delivered.** |
| A03 | source/history extracts only: Directives, 19 retained-event evidence rows and 19 scriptlet rows; no complete choice/change-event table. **Not delivered.** |
| A04 | current policy only: Two current unit-policy rows; no original disablement-event record. **Not delivered.** |
| A05 | inner metadata recorded: 72,148 members in three completed implemented store traversals; zero inner opaque rows. **Not delivered.** |
| A06 | metadata only: Inner member metadata is present; complete payload receipts and per-member creator events are not emitted. **Not delivered.** |
| A07 | import fields recorded; reason absent: One event row with measured import context; no PID/transaction correlation or acquisition-reason field. **Not delivered.** |
| A08 | current bytes recorded: Two /etc/alsa current-content rows retained, each with saved read evidence. **Not delivered.** |
| A09 | creator event absent: Current contents and bounded extracts do not provide a per-value creator record. **Not delivered.** |
| A10 | current values recorded: One native persistent-SELinux-value row retained. **Not delivered.** |
| A11 | chooser event absent: Values, script source and bounded extracts retained; no per-value chooser event. **Not delivered.** |
| A12 | decoded values recorded: Five compiled-values rows retained. **Not delivered.** |
| A13 | current schema/readers only: Five schema-evidence and five current-reader-snapshot rows; no complete consumer history. **Not delivered.** |
| A14 | source decoding recorded: 24 of 24 requested cache decodes; font-source/package joins retained. **Not delivered.** |
| A15 | reference comparisons recorded: 459 equal npm member comparisons and 52 directory entries against verified references. **Not delivered.** |

Objects in `all-alma.tsv`: 0; to decide: 0.

No delivered kinds; all is header-only. Original count by kind remains in (not published: orchestration or scratch) and unchanged `D1b/raw/alma/objects.tsv`.

Deviations from committed machine/action/collector/handoff instruments: none.

## void

Committed release: **Void Linux 20250202, x86-64 glibc, runit**. new 0 / 16.224 s; collector 0 / 78.865 s; destroy 0 / 3.840 s.

Level two obtained in part: filesystem_complete=true describes the implemented traversal; package_ownership_complete=false. Fifteen image rows remain atomic. Three store traversals recorded 72,162 inner members with zero inner opaque rows, without complete payload receipts or creator events.

Lifecycle, complete separate command outputs and diagnostics: `operator/void/`; machine record: (not published: orchestration or scratch). Collector coverage and all failed query streams remain under `D1b/handoff/void/coverage.tsv` and its referenced `raw/` files. Nonzero optional queries were retained, never repaired or repeated.

Ordinary actions (`operator/void/actions/actions-status.tsv`):

| Action | Exit | Seconds |
|---|---:|---:|
| package_program | 0 | 136 |
| application_package | 0 | 52 |
| language_install_node | 0 | 17 |
| language_npm_install | 0 | 2 |
| language_cowsay | 0 | 0 |
| language_program | 0 | 19 |
| browser_extension | 0 | 59 |
| personal_setting | 0 | 8 |
| user_service | 0 | 3 |
| network_connection | 0 | 24 |
| home_script | 0 | 0 |
| container_run | 0 | 13 |

Facts requested in `S4/MISSING.tsv` (the detailed evidence paths are in `MISSING-RECORDED.tsv`):

| Fact | Recorded fields and limits |
|---|---|
| V01 | reference comparisons recorded: 41 verified lock-reference archives; 459 equal member comparisons and 23 directory entries. |
| V02 | reference search/comparisons partial: 17 read sources; 22,282 equal comparisons, 4,294 directory entries and 6,859 no-reference-found rows. Missing references remain missing. |
| V03 | current sources only: Account/group/sudo rows and package sources retained; no per-object choice/creation events. |
| V04 | inner metadata recorded: Three completed implemented store traversals; 72,162 members. |
| V05 | metadata only: Bounded inner metadata present; complete payload receipt and per-member creator events absent. |
| V06 | current bytes/hashes recorded: 11 selected configuration-content rows ok; 11,306 of 11,306 eligible complete digests known. |
| V07 | creator event absent: historical_creator retains an unknown marker; current records supply no creation event. |
| V08 | source decoding recorded: One requested font cache decoded; 47 font-source/package rows. |
| V09 | choice/use events absent: No per-value choice-event or complete consumer/use table emitted; current metadata and eligible digests remain. |

Objects in `all-void.tsv`: 3279; to decide: 1143.

| Kind | Objects in all |
|---|---:|
| L1:access-rule | 38 |
| L1:account | 10 |
| L1:docker-container | 1 |
| L1:docker-image | 1 |
| L1:driver | 89 |
| L1:firewall-ipv4 | 40 |
| L1:firewall-ipv6 | 29 |
| L1:group | 39 |
| L1:module-name | 220 |
| L1:package | 546 |
| L1:polkit-action | 33 |
| L1:port | 4 |
| L1:process | 124 |
| L1:runit-service | 15 |
| L1:saved-network | 6 |
| L1:saved-network-file | 3 |
| L1:sudo-access | 13 |
| L2:code-ownership-unresolved | 21 |
| L2:image | 15 |
| L2:image-container-store | 3 |
| L2:stored-ownership-unresolved | 2029 |

Deviations from committed machine/action/collector/handoff instruments: none.

## gentoo

Committed release: **Gentoo 20261122T164601Z**. new 0 / 16 s; collector 0 / 100.624 s; destroy 0 / 2.644 s.

Level two obtained in part: filesystem_complete=true but package_ownership_complete=false. npm per-file provenance is unresolved; a discovered Go manager has no complete adapter. Eleven image rows remain atomic. Two store traversals recorded 530 members with zero inner opaque rows.

Lifecycle, complete separate command outputs and diagnostics: `operator/gentoo/`; machine record: (not published: orchestration or scratch). Collector coverage and all failed query streams remain under `D1b/handoff/gentoo/coverage.tsv` and its referenced `raw/` files. Nonzero optional queries were retained, never repaired or repeated.

Ordinary actions (`operator/gentoo/actions/actions-status.tsv`):

| Action | Exit | Seconds |
|---|---:|---:|
| package_program | 0 | 5 |
| application_package | 0 | 3 |
| language_program | 0 | 181 |
| browser_extension | 1 | 10 |
| personal_setting | 0 | 96 |
| user_service | 0 | 0 |
| network_connection | 0 | 0 |
| home_script | 0 | 0 |
| container_run | 0 | 286 |

`browser_extension` failed once with `UnsupportedOperationException: System access is required` and the emitted `MOZ_REMOTE_ALLOW_SYSTEM_ACCESS=1` diagnostic. Exact full output: `operator/gentoo/actions/actions-logs/browser_extension.stderr` and `.log`. No change or retry; the remaining fixed actions continued. All other eight actions exited 0.

Facts requested in `S4/MISSING.tsv` (the detailed evidence paths are in `MISSING-RECORDED.tsv`):

| Fact | Recorded fields and limits |
|---|---|
| G01 | both levels obtained; partial coverage: 32,775 rows (1,210 level one; 31,565 level two). Eight actions passed and browser_extension failed once. 109,059/109,382 package-file comparisons and 152,215/152,216 full digests known. |

Objects in `all-gentoo.tsv`: 32775; to decide: 32775.

| Kind | Objects in all |
|---|---:|
| L1:access-rule | 28 |
| L1:account | 19 |
| L1:docker-container | 1 |
| L1:docker-image | 1 |
| L1:driver | 127 |
| L1:firewall-ipv4 | 40 |
| L1:firewall-ipv6 | 29 |
| L1:group | 39 |
| L1:module-name | 203 |
| L1:openrc-runlevel | 60 |
| L1:openrc-service | 47 |
| L1:package | 440 |
| L1:port | 4 |
| L1:process | 159 |
| L1:sudo-access | 13 |
| L2:code-ownership-unresolved | 1620 |
| L2:image | 11 |
| L2:image-container-store | 2 |
| L2:stored-ownership-unresolved | 29932 |

Deviations from committed machine/action/collector/handoff instruments: none.

## microos

Committed release: **openSUSE MicroOS Snapshot20261121**. new 0 / 24 s; collector 0 / 84 s; destroy 0 / 1 s.

Level two obtained in part despite filesystem_complete=true and package_ownership_complete=true: 20 image rows and /.snapshots/2/snapshot retain expanded=false. /etc has expanded=true and 2,219 recorded descendants. Inner store tables are header-only.

Lifecycle, complete separate command outputs and diagnostics: `operator/microos/`; machine record: (not published: orchestration or scratch). Collector coverage and all failed query streams remain under `D1b/handoff/microos/coverage.tsv` and its referenced `raw/` files. Nonzero optional queries were retained, never repaired or repeated.

No ordinary actions assigned.

Facts requested in `S4/MISSING.tsv` (the detailed evidence paths are in `MISSING-RECORDED.tsv`):

| Fact | Recorded fields and limits |
|---|---|
| M01 | source text only: Current sysusers sources and RPM scriptlet query retained; no per-account/group creation-event table. |
| M02 | current sources/links recorded: 263 selected unit rows, all selection fields known; 1,318 source-file reads and current link table. |
| M03 | actor/default history absent: Current links and script source retained; no per-link enablement-event table. |
| M04 | current sources/comparisons recorded: Supplying sudo source bytes and package-file comparisons retained; unknown comparisons stay unknown. |
| M05 | choice events absent: Current source bytes and comparisons retained; no per-rule choice-event table. |
| M06 | active subtree recorded: /etc remains expanded=true with 2,219 descendants in the implemented traversal. |
| M07 | manifest/comparisons partial: Two snapshot manifest roots; 20,400 rows: 15,817 equal, 20 different, 33 unknown and 4,530 directory-membership-only. |
| M08 | complete pairs recorded: 16,177 snapshot/current full-SHA256 comparisons, all comparison fields known. |
| M09 | current sources/comparisons only: Two native SELinux stores listed and snapshot/current comparisons retained; no per-copy original receipt or derivation-event field. |
| M10 | current bytes recorded: grubenv source read status ok, with saved complete bounded bytes. |
| M11 | creator/chooser event absent: Current grubenv bytes retained; no per-value creation/choice event. |
| M12 | snapshot source records retained: Snapshot-root RPM source and package membership plus complete path comparisons retained, with per-row unknowns unchanged. |
| M13 | solver source/decoding recorded: Three solver-cache files; one decoded; content/digest statuses and source evidence retained. |
| M14 | choice/use events absent: No per-value choice-event or complete consumer/use table emitted; current metadata and eligible digests retained. |

Objects in `all-microos.tsv`: 6567; to decide: 747.

| Kind | Objects in all |
|---|---:|
| L1:access-rule | 32 |
| L1:account | 11 |
| L1:driver | 109 |
| L1:group | 32 |
| L1:module-name | 197 |
| L1:package | 376 |
| L1:polkit-action | 123 |
| L1:port | 4 |
| L1:process | 134 |
| L1:saved-network | 3 |
| L1:saved-network-file | 1 |
| L1:service | 147 |
| L1:sudo-access | 14 |
| L1:timer | 12 |
| L1:unit-file | 249 |
| L1:user-service | 5 |
| L1:user-timer | 1 |
| L1:user-unit-file | 14 |
| L2:executable-code-outside-packages | 1874 |
| L2:image | 20 |
| L2:snapshot | 2 |
| L2:stored-outside-packages | 3207 |

Deviations from committed machine/action/collector/handoff instruments: none.

## talos

Committed release: **Talos Linux 1.14.6**. new 0 / 8 s; collector 0 / 203 s; destroy 0 / 47 s.

Level two obtained in part: filesystem_complete=false, original depth/count bounds and 18 extended workload-or-pseudo boundaries remain. The literal package_ownership_complete=true field does not override the explicit metadata limit on complete ownership/level-two coverage. Extended listings contain 8,503 members across 1,219 directories; 5,932 of 5,963 bounded content reads succeeded, with 31 not-found results.

Lifecycle, complete separate command outputs and diagnostics: `operator/talos/`; machine record: `operator/talos/report.md`. Collector coverage and all failed query streams remain under `D1b/handoff/talos/coverage.tsv` and its referenced `raw/` files. Nonzero optional queries were retained, never repaired or repeated.

No ordinary actions assigned.

Facts requested in `S4/MISSING.tsv` (the detailed evidence paths are in `MISSING-RECORDED.tsv`):

| Fact | Recorded fields and limits |
|---|---|
| T01 | current sources only: Three current image-source rows; no historical acquisition actor. |
| T02 | expanded listings partial: 8,503 members, 1,219 directory listings, zero listing failures and 18 retained boundaries. |
| T03 | original reference absent: Current listings/hashes/mounts retained; no original installed-image manifest or receipt comparison. |
| T04 | current namespace recorded; history absent: 29 API-daemon mount rows, query exit0; historical overlay origin and other workload namespaces remain unrecorded. |
| T05 | creator/derivation events absent: Current listings/hashes retained; no per-member creation/derivation-event record. |
| T06 | bounded hashes/signatures partial: 5,932/5,963 content hashes ok; 31 not-found. Initial Read failures, 34 Copy archive-error attempts, and final refresh results retained. |

Objects in `all-talos.tsv`: 278; to decide: 43.

| Kind | Objects in all |
|---|---:|
| L1:block-device | 4 |
| L1:container | 2 |
| L1:container-image | 12 |
| L1:kernel-module | 10 |
| L1:mount | 13 |
| L1:mount-resource | 18 |
| L1:network-configuration | 11 |
| L1:network-state | 44 |
| L1:package | 1 |
| L1:process | 34 |
| L1:service | 12 |
| L1:socket | 64 |
| L2:code-ownership-unknown | 7 |
| L2:opaque-directory | 11 |
| L2:stored-ownership-unknown | 35 |

Deviations from committed machine/action/collector/handoff instruments: none.

## Execution disclosures and verification

No committed instrument was changed, repaired, substituted or repeated. The Gentoo browser failure and AlmaLinux copier failure were processed exactly by the committed failure rules.

Host transport selected the existing user SSH configuration explicitly after the default system configuration ownership error; no configuration changed. Void had one host service submission rejected before process startup because its working-directory syntax was unexpanded; its subsequent submission launched the sole execution. Void monitoring had one transport exit 255 during the network action and continued monitoring the same detached session. An optional adjacent rehearsal diagnostics filename was absent during raw transport; all actual raw files were preserved and verified, and no observation was repeated. Reporting readers increased only their own CSV field-size limit after read-only counting failures; the committed copier was never adjusted. These orchestration/reporting details are recorded in the machine reports and `operator/PROCEDURE.md`.

Mechanical preservation checks: `operator/deliverable-verification.json`; handoff copy hashes: `operator/handoff-local-verification.json` and the four copier audits. The final preservation check covers both local originals and handoffs, including complete file sets, all/part selection, raw-ID mapping and member counts. This is operator verification, not independent acceptance.

Cleanup evidence: `operator/server-cleanup.json`. All five VM directories were absent before temporary server staging was removed. Original observations, handoffs, audits and operator evidence remain in the task directories; ten shared VM slots are free. In the published AlmaLinux failure traceback, absolute task-root paths are displayed as task-relative paths; the diagnostic and stack line numbers are unchanged (`D1b/handoff-audit/alma-failure.json`).

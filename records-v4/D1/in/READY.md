INVENTORY: 4 of 5 machines

Recorded UTC: 2026-11-23T11:26:06.393199+00:00.

Input commit: `b3c3c141c612b8d287c8058733141cb56d1c2431`, supplied by (not published: orchestration or scratch). All 1020 manifest entries matched before observation; all 44 staged runtime files matched after transfer. The laboratory runner also matched. Evidence: `control/input-verification.json`, `control/input-verification.tsv`, `control/deployed-input-verification.json`, `control/OPERATOR-NOTES.md`. The manifest has no self-checksum. This workspace is not a Git worktree; commit-tree identity was not independently verified.

## Machine records

Counts mean rows emitted by the committed collector, without selection, merging or deduplication. The second-level column reports the requested rows-above-zero condition. It does not resolve whether bounded or partial coverage satisfies Section 9.2, and assigns no hypothesis outcome. Known reasons mean explicit/dependency; known integrity means unchanged/changed/missing. Packaged-file shares use all collector package/file records, not unique paths.

| Machine | Committed release | Objects | L1 | L2 | Second-level rows obtained | Known package reasons | Known packaged-file integrity |
|---|---|---:|---:|---:|---|---|---|
| alma | 10.3 | 6293 | 4605 | 1688 | Yes | 1006/1561 (64.45%) | 120520/121931 (98.84%) |
| void | 20250202 (rolling-release installation image) | 3282 | 1214 | 2068 | Yes | 384/546 (70.33%) | 37652/37931 (99.26%) |
| gentoo | stage3-amd64-openrc-20261122T164601Z | 0 | 0 | 0 | No | N/A (no inventory) | N/A (no inventory) |
| microos | Snapshot20261121 plain x86_64 KVM/XEN image | 6522 | 1452 | 5070 | Yes | 376/376 (100.00%) | 18246/18575 (98.23%) |
| talos | 1.14.6 | 278 | 225 | 53 | Yes | 1/1 (100.00%) | 0/287 (0.00%) |

Gentoo: no inventory. The sole fresh-machine command returned 1 with `lab: VM failed to start`; destruction returned 0. Actions and collection were not attempted. The host lifecycle log confirms process exit 1 but provides no specific cause; slot shortage is not inferred. Evidence: `raw/gentoo/NOT-RUN.md`, `control/gentoo/new.err`, `control/gentoo/status.json`, `control/gentoo/host-lifecycle.txt`. The part table is header-only.

## Objects by kind

All values below are observed row counts; zero does not establish absence outside the collector scope.

| Kind | alma | void | gentoo | microos | talos |
|---|---:|---:|---:|---:|---:|
| L1:access-rule | 95 | 38 | 0 | 22 | 0 |
| L1:account | 37 | 10 | 0 | 11 | 0 |
| L1:block-device | 0 | 0 | 0 | 0 | 4 |
| L1:container | 2 | 0 | 0 | 0 | 2 |
| L1:container-image | 2 | 0 | 0 | 0 | 12 |
| L1:docker-container | 0 | 1 | 0 | 0 | 0 |
| L1:docker-image | 0 | 1 | 0 | 0 | 0 |
| L1:driver | 105 | 89 | 0 | 109 | 0 |
| L1:firewall-chain | 127 | 0 | 0 | 0 | 0 |
| L1:firewall-ipv4 | 0 | 40 | 0 | 0 | 0 |
| L1:firewall-ipv6 | 0 | 29 | 0 | 0 | 0 |
| L1:firewall-rule | 206 | 0 | 0 | 0 | 0 |
| L1:firewall-table | 2 | 0 | 0 | 0 | 0 |
| L1:group | 59 | 39 | 0 | 32 | 0 |
| L1:kernel-module | 0 | 0 | 0 | 0 | 10 |
| L1:module-name | 193 | 220 | 0 | 197 | 0 |
| L1:mount | 0 | 0 | 0 | 0 | 13 |
| L1:mount-resource | 0 | 0 | 0 | 0 | 18 |
| L1:network-configuration | 0 | 0 | 0 | 0 | 11 |
| L1:network-state | 0 | 0 | 0 | 0 | 42 |
| L1:package | 1561 | 546 | 0 | 376 | 1 |
| L1:polkit-action | 299 | 33 | 0 | 123 | 0 |
| L1:port | 9 | 4 | 0 | 4 | 0 |
| L1:process | 1280 | 127 | 0 | 133 | 34 |
| L1:runit-service | 0 | 15 | 0 | 0 | 0 |
| L1:saved-network | 4 | 6 | 0 | 3 | 0 |
| L1:saved-network-file | 4 | 3 | 0 | 0 | 0 |
| L1:service | 172 | 0 | 0 | 147 | 12 |
| L1:socket | 0 | 0 | 0 | 0 | 66 |
| L1:sudo-access | 9 | 13 | 0 | 14 | 0 |
| L1:timer | 7 | 0 | 0 | 12 | 0 |
| L1:unit-file | 310 | 0 | 0 | 249 | 0 |
| L1:user-service | 13 | 0 | 0 | 5 | 0 |
| L1:user-timer | 2 | 0 | 0 | 1 | 0 |
| L1:user-unit-file | 107 | 0 | 0 | 14 | 0 |
| L2:code-ownership-unknown | 0 | 0 | 0 | 0 | 7 |
| L2:code-ownership-unresolved | 25 | 21 | 0 | 0 | 0 |
| L2:executable-code-outside-packages | 0 | 0 | 0 | 1874 | 0 |
| L2:image | 13 | 15 | 0 | 20 | 0 |
| L2:image-container-store | 3 | 3 | 0 | 0 | 0 |
| L2:opaque-directory | 0 | 0 | 0 | 0 | 11 |
| L2:snapshot | 0 | 0 | 0 | 2 | 0 |
| L2:stored-outside-packages | 0 | 0 | 0 | 3174 | 0 |
| L2:stored-ownership-unknown | 0 | 0 | 0 | 0 | 35 |
| L2:stored-ownership-unresolved | 1647 | 2029 | 0 | 0 | 0 |

## Ordinary actions

AlmaLinux and Void each execute their committed entry script once. The script continues its fixed list after an action failure; no action is repaired or replaced. Gentoo could not reach the action stage. No ordinary actions are prescribed for MicroOS or Talos.

| Machine | Action/status label | Exit status | Elapsed seconds | Exact stdout | Exact stderr |
|---|---|---:|---:|---|---|
| alma | package_program | 0 | 4 | `control/alma/actions-logs/package_program.log` | `control/alma/actions-logs/package_program.stderr` |
| alma | application_package | 0 | 37 | `control/alma/actions-logs/application_package.log` | `control/alma/actions-logs/application_package.stderr` |
| alma | language_program | 0 | 6 | `control/alma/actions-logs/language_program.log` | `control/alma/actions-logs/language_program.stderr` |
| alma | browser_extension | 0 | 15 | `control/alma/actions-logs/browser_extension.log` | `control/alma/actions-logs/browser_extension.stderr` |
| alma | personal_setting | 0 | 1 | `control/alma/actions-logs/personal_setting.log` | `control/alma/actions-logs/personal_setting.stderr` |
| alma | user_service | 0 | 3 | `control/alma/actions-logs/user_service.log` | `control/alma/actions-logs/user_service.stderr` |
| alma | network_connection | 0 | 0 | `control/alma/actions-logs/network_connection.log` | `control/alma/actions-logs/network_connection.stderr` |
| alma | home_script | 0 | 0 | `control/alma/actions-logs/home_script.log` | `control/alma/actions-logs/home_script.stderr` |
| alma | container_run | 0 | 5 | `control/alma/actions-logs/container_run.log` | `control/alma/actions-logs/container_run.stderr` |
| void | package_program | 0 | 121 | `control/void/actions-logs/actions-logs/package_program.log` | `control/void/actions-logs/actions-logs/package_program.stderr` |
| void | application_package | 0 | 45 | `control/void/actions-logs/actions-logs/application_package.log` | `control/void/actions-logs/actions-logs/application_package.stderr` |
| void | language_install_node | 0 | 4 | `control/void/actions-logs/actions-logs/language_program.log` | `control/void/actions-logs/actions-logs/language_program.stderr` |
| void | language_npm_install | 0 | 2 | `control/void/actions-logs/actions-logs/language_program.log` | `control/void/actions-logs/actions-logs/language_program.stderr` |
| void | language_cowsay | 0 | 1 | `control/void/actions-logs/actions-logs/language_program.log` | `control/void/actions-logs/actions-logs/language_program.stderr` |
| void | language_program | 0 | 7 | `control/void/actions-logs/actions-logs/language_program.log` | `control/void/actions-logs/actions-logs/language_program.stderr` |
| void | browser_extension | 0 | 46 | `control/void/actions-logs/actions-logs/browser_extension.log` | `control/void/actions-logs/actions-logs/browser_extension.stderr` |
| void | personal_setting | 0 | 8 | `control/void/actions-logs/actions-logs/personal_setting.log` | `control/void/actions-logs/actions-logs/personal_setting.stderr` |
| void | user_service | 0 | 4 | `control/void/actions-logs/actions-logs/user_service.log` | `control/void/actions-logs/actions-logs/user_service.stderr` |
| void | network_connection | 0 | 8 | `control/void/actions-logs/actions-logs/network_connection.log` | `control/void/actions-logs/actions-logs/network_connection.stderr` |
| void | home_script | 0 | 0 | `control/void/actions-logs/actions-logs/home_script.log` | `control/void/actions-logs/actions-logs/home_script.stderr` |
| void | container_run | 0 | 14 | `control/void/actions-logs/actions-logs/container_run.log` | `control/void/actions-logs/actions-logs/container_run.stderr` |

Void labels beginning `language_` other than `language_program` are internal substep statuses emitted by the fixed script; they are not added cases. A nonzero exit is retained as failure. Lifecycle/action transport records are in `control/alma/status.tsv` and `control/void/lifecycle.tsv`.

## Collector coverage and cleanup

- alma: 228 queries, 79 nonzero exits; collector `filesystem_complete=true`, `package_ownership_complete=false`. Every query, stdout/stderr and gap remains in `raw/alma/coverage.tsv`, `raw/alma/raw/` and `raw/alma/metadata.json`.
- void: 90 queries, 36 nonzero exits; collector `filesystem_complete=true`, `package_ownership_complete=false`. Every query, stdout/stderr and gap remains in `raw/void/coverage.tsv`, `raw/void/raw/` and `raw/void/metadata.json`.
- microos: 52 queries, 17 nonzero exits; collector `filesystem_complete=true`, `package_ownership_complete=true`. Every query, stdout/stderr and gap remains in `raw/microos/coverage.tsv`, `raw/microos/raw/` and `raw/microos/metadata.json`.
- talos: 85 queries, 0 nonzero exits; collector `filesystem_complete=false`, `package_ownership_complete=true`. Every query, stdout/stderr and gap remains in `raw/talos/coverage.tsv`, `raw/talos/raw/` and `raw/talos/metadata.json`.

Talos has second-level rows but explicitly lacks complete non-package inventory: bounded API traversal, unknown persistence and file integrity, and parser/ownership limitations remain. For other machines, a completeness flag describes the implemented collector scope only. No failed query is repaired or repeated. All facts and unavailable facts are indexed by `FACTS.md`.

Every created disposable machine was destroyed. All temporary server task staging and duplicate outputs were removed after verified transfer; the 44 runtime inputs still matched before removal. See per-machine lifecycle records and `control/final-cleanup.json`. Raw transfer checksums and `control/table-verification.json` document byte preservation and exact one-to-one object-table transformation; these are mechanical checks, not independent acceptance of the experiment.

## Deviations and earlier stop

- Earlier pre-observation stop: `D1.stopped-before-observation/in/READY.md` records a mismatch in the publication-list checksum, with no machine, action, collector or observation. The corrected manifest was committed in `b3c3c14` before this run. The earlier record is preserved; only its READY file was read.
- SSH transport initially rejected a system configuration file because of its ownership/permissions. Explicit selection of the existing user SSH configuration restored transport without system edits or changes to committed inputs.
- MicroOS operator launch preparation failed twice before its sole machine command: the first launcher exited without retained diagnostics and was renamed from `operator.py` to avoid a possible standard-library name collision; the next service command rejected an unexpanded output path. The corrected launch invoked `lab.sh new` once. Exact available evidence and the missing first-launch diagnostic are disclosed in `control/OPERATOR-NOTES.md`.
- Void had one failed completion-monitor transport call (exit 255) while its detached entry script continued. Later monitoring reconnected; no action was retried. The exit status is retained in `control/void/lifecycle.tsv`; `control/void/action-completion.stderr` is empty, so the cause remains unknown.
- Gentoo startup failure prevented its prescribed actions and inventory; cause remains unknown. The failed case was not retried.
- AlmaLinux and Void collector invocation differed from the documented direct command: the operator used `bash D1/inputs/collect.sh --observe ...`, overriding the committed wrapper shebang (`/bin/sh`). This was an operator harness choice without a documented requirement or observed compatibility failure. The wrapper bytes and Python collector were unchanged; both invocations completed once and were not rerun. Evidence: `control/alma/operator.sh`, `control/void/operator.sh`.
- No committed collector, action command or installation recipe was modified or substituted. No objects were selected, filtered, merged or discarded. Remaining operational details are in the machine summaries and retained logs.

No hypothesis outcome is assigned. This operator record is submitted for independent acceptance; it is not self-accepted.

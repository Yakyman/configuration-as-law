INVENTORY: 3 of 3 machines

# A3-I operator record

This investigation is beyond the published plan, reported separately under PROTOCOL.md Section 5. It is not an outcome of any of the four checks. Inventory count denotes collected lived/base pairs and completed derived tables, not universal fact coverage or a hypothesis result.

Inputs: gate commit `3e0207b104f9718793c5b2678810936c7c3c14d2`. Required action/helper/collector checksums passed before execution; see [INPUTS.md](INPUTS.md) and [input-verification.tsv](input-verification.tsv). The PUBLISH.list self-checksum differs from its recorded checksum; the actual named executable inputs match. Outer SSH used the existing user configuration explicitly after the system configuration was rejected; no host configuration was changed.

Method: [REDUCTION.md](REDUCTION.md), [reduce.py](reduce.py). Fact locations and uncertainty: [FACTS.md](FACTS.md). Synthetic reduction checks: [reduction-test.txt](reduction-test.txt). Independent review: [REVIEW.md](REVIEW.md). All raw collector files are retained unchanged, including nonzero query outputs and incomplete/unknown facts. No failed action is repaired, replaced or repeated.

## developer

Objects: **11852 before → 6409 after**; 5443 base-equal rows removed. Untouched base: 5966 objects. Table: (not published: direct evidence at least 2 MB); row-level comparison: [reduction-developer.tsv](reduction-developer.tsv).

Actions: 13/13 succeeded. Exact statuses: [operator/developer/actions-status.tsv/actions-status.tsv](operator/developer/actions-status.tsv/actions-status.tsv). Separate stdout/stderr and lifecycle/restart/destruction records: (not published: orchestration or scratch).

| Action | Exit status | Seconds |
|---|---:|---:|
| developer_prerequisites | 0 | 22 |
| developer_julia | 0 | 7 |
| developer_bun | 0 | 2 |
| developer_version_manager | 0 | 4 |
| developer_global_tools | 0 | 6 |
| developer_editor_plugins | 0 | 1 |
| developer_public_project | 0 | 36 |
| developer_git_hooks | 0 | 1 |
| developer_container | 0 | 23 |
| developer_second_package_manager | 0 | 17 |
| developer_user_service_timer | 0 | 0 |
| developer_shell_startup | 0 | 0 |
| developer_ssh | 0 | 0 |

| Inventory | Filesystem complete | Ownership complete | Recorded gaps | Nonzero queries |
|---|---|---|---:|---:|
| [developer](raw/developer/metadata.json) | true | false | 304 | 114 |
| [developer-base](raw/developer-base/metadata.json) | true | false | 220 | 116 |

The collector metadata retains `ready_for_observation=false`; the operator does not override it. Coverage includes missing or unavailable interfaces; precise status, stderr and gap references remain in each raw inventory. A zero collector exit is not a claim that every fact was collected.

| Level:kind | Before | After |
|---|---:|---:|
| 1:access-rule | 126 | 0 |
| 1:account | 54 | 0 |
| 1:docker-container | 1 | 1 |
| 1:docker-image | 1 | 1 |
| 1:driver | 127 | 0 |
| 1:firewall-chain | 185 | 185 |
| 1:firewall-ct helper | 1 | 1 |
| 1:firewall-ipv4 | 44 | 44 |
| 1:firewall-ipv6 | 29 | 29 |
| 1:firewall-rule | 266 | 266 |
| 1:firewall-table | 6 | 6 |
| 1:group | 84 | 1 |
| 1:module-name | 237 | 12 |
| 1:package | 2248 | 202 |
| 1:polkit-action | 542 | 0 |
| 1:port | 15 | 15 |
| 1:process | 152 | 74 |
| 1:saved-network | 4 | 2 |
| 1:saved-network-file | 2 | 0 |
| 1:service | 221 | 3 |
| 1:sudo-access | 9 | 0 |
| 1:timer | 7 | 5 |
| 1:unit-file | 476 | 2 |
| 1:user-service | 13 | 1 |
| 1:user-timer | 3 | 3 |
| 1:user-unit-file | 125 | 2 |
| 2:code-ownership-unresolved | 634 | 619 |
| 2:image | 22 | 0 |
| 2:image-container-store | 4 | 2 |
| 2:stored-ownership-unresolved | 6214 | 4933 |

Execution details and every machine-specific deviation are recorded in (not published: orchestration or scratch). The following operator record is reproduced to keep this report self-contained; paths within that record are relative to operator/developer/:


Beyond-plan TASK A3-I; base Fedora. All times in retained lifecycle status are UTC.

All 13 committed actions ran exactly once and exited 0. Exact name/status/duration: `actions-status.tsv/actions-status.tsv`; complete command output: `actions-logs/actions-logs/`. Both collection calls exited 0, and both disposable machines were destroyed successfully (`status.json`). Boot identifiers differ (`boot-before.out`, `boot-after.out`), after one stop/start cycle.

| Inventory | Objects | Filesystem complete | Ownership complete | Metadata gaps |
|---|---:|---|---|---:|
| developer | 11852 | True | False | 304 |
| developer-base | 5966 | True | False | 220 |

Complete raw output is in (not published: record outside this collection) and (not published: record outside this collection). `transfer-verification.json` and the two raw `.remote.sha256` manifests certify copied file hashes. `operator.remote.sha256` certifies copied operator output; `inputs.sha256` certifies published staged inputs. Exact collector completeness flags, complete gaps and counts by kind are in `summary.json`; original metadata is retained in each raw directory. No claim of complete package coverage follows from collector exit 0.

Execution details and deviations:
- No committed action edits, substitutions, retries, repairs, or omissions.
- Existing user bus environment supplied through XDG_RUNTIME_DIR and DBUS_SESSION_BUS_ADDRESS, as action documentation requires.
- Operator staged exact scripts under /tmp/a3-developer-inputs then removed this instrument-only directory before restart; action logs and all action-created state remained.
- Restart implemented by one successful lab.sh stop/start cycle.
- Two supplemental status reads collided with restart and failed; original action-status copy succeeded. See monitoring-failures.tsv.
- Host paths and host name replaced in lifecycle stdout/stderr by LAB_ROOT, HOST_HOME, the-host; collector output remains byte-for-byte unchanged.
- PUBLISH.list checksum inconsistency is disclosed in parent inventory records; every staged input individually matches committed checksum table.

No quota interface was available in the task tools; no private authentication files were inspected. No object classification or acceptance performed.

## gaming

Objects: **24243 before → 16515 after**; 7728 base-equal rows removed. Untouched base: 8312 objects. Table: (not published: direct evidence at least 2 MB); row-level comparison: (not published: direct evidence at least 2 MB).

Actions: 8/9 succeeded. Exact statuses: [operator/gaming/actions-status.tsv/actions-status.tsv](operator/gaming/actions-status.tsv/actions-status.tsv). Separate stdout/stderr and lifecycle/restart/destruction records: (not published: orchestration or scratch).

| Action | Exit status | Seconds |
|---|---:|---:|
| gaming_prerequisites | 0 | 146 |
| gaming_store_runtime | 0 | 133 |
| gaming_anonymous_download | 8 | 39 |
| gaming_flatpak_game | 0 | 29 |
| gaming_launcher_tool | 0 | 7 |
| gaming_windows_program | 0 | 12 |
| gaming_overlay | 0 | 0 |
| gaming_user_settings | 0 | 2 |
| gaming_autostart | 0 | 0 |

| Inventory | Filesystem complete | Ownership complete | Recorded gaps | Nonzero queries |
|---|---|---|---:|---:|
| [gaming](raw/gaming/metadata.json) | true | false | 196 | 109 |
| [gaming-base](raw/gaming-base/metadata.json) | true | false | 200 | 111 |

The collector metadata retains `ready_for_observation=false`; the operator does not override it. Coverage includes missing or unavailable interfaces; precise status, stderr and gap references remain in each raw inventory. A zero collector exit is not a claim that every fact was collected.

| Level:kind | Before | After |
|---|---:|---:|
| 1:access-rule | 103 | 0 |
| 1:account | 49 | 0 |
| 1:driver | 170 | 0 |
| 1:group | 78 | 0 |
| 1:module-name | 210 | 0 |
| 1:package | 2303 | 490 |
| 1:polkit-action | 315 | 0 |
| 1:port | 13 | 3 |
| 1:process | 150 | 75 |
| 1:saved-network | 3 | 1 |
| 1:saved-network-file | 3 | 0 |
| 1:service | 169 | 4 |
| 1:sudo-access | 17 | 0 |
| 1:timer | 12 | 12 |
| 1:unit-file | 278 | 0 |
| 1:user-service | 18 | 1 |
| 1:user-timer | 1 | 1 |
| 1:user-unit-file | 112 | 2 |
| 2:code-ownership-unresolved | 15412 | 14053 |
| 2:gvfs-alias | 1 | 0 |
| 2:image | 14 | 0 |
| 2:image-container-store | 2 | 1 |
| 2:stored-ownership-unresolved | 4810 | 1872 |

Execution details and every machine-specific deviation are recorded in (not published: orchestration or scratch). The following operator record is reproduced to keep this report self-contained; paths within that record are relative to operator/gaming/:


All file references in this report are relative to `A3/in/operator/gaming/` unless stated otherwise. Beyond-plan TASK A3-I. Base: mint. Committed input marker: `3e0207b104f9718793c5b2678810936c7c3c14d2`.

All staged input bytes matched the published checksums locally and after server transfer (`input-sha256.tsv`, `deployed-hashes.json`, `deployed-verification.txt`). The collector used the published compressed probe chunks.

The lived script ran exactly once as the ordinary guest account through the documented session environment. Its four required input files were staged under `/run/user/1000/a3-inputs`; this runtime instrumentation disappeared on the one stop/start restart. No failed action was repaired or substituted. Action output is retained under `actions-logs/actions-logs/`; statuses are in `actions-status.tsv/actions-status.tsv`. Host lifecycle output replaces the actual host home and hostname with placeholders; guest action output and collector output are unchanged.

| Action | Exit | Seconds |
|---|---:|---:|
| gaming_prerequisites | 0 | 146 |
| gaming_store_runtime | 0 | 133 |
| gaming_anonymous_download | 8 | 39 |
| gaming_flatpak_game | 0 | 29 |
| gaming_launcher_tool | 0 | 7 |
| gaming_windows_program | 0 | 12 |
| gaming_overlay | 0 | 0 |
| gaming_user_settings | 0 | 2 |
| gaming_autostart | 0 | 0 |

The failed anonymous download reports `ERROR! Failed to install app '1110390' (Missing configuration)` in `actions-logs/actions-logs/gaming_anonymous_download.log`, after successful anonymous connection and user-info retrieval. Its stderr is retained alongside. No repair or retry was performed.

Lifecycle exit statuses and UTC times: `lifecycle.json`; distinct boot identifiers: `boot-before.out`, `boot-after.out`. Both disposable clones were destroyed (`lived-destroy.out`, `base-destroy.out`, lifecycle statuses).

| Inventory | Objects | Collector exit | Filesystem complete | Ownership complete |
|---|---:|---:|---|---|
| gaming | 24243 | 0 | True | False |
| gaming-base | 8312 | 0 | True | False |

Whole collector output: (not published: record outside this collection) and (not published: record outside this collection). Every transferred file matched its remote SHA-256 manifest. Counts by level/kind and all collector gaps are retained in `status.json`; raw `metadata.json` and `coverage.tsv` are authoritative.

Deviations from committed action/collector inputs: none. The published-list checksum discrepancy is recorded by the coordinating operator, separately from the matching executable inputs. No independent acceptance is asserted here.

## server

Objects: **3287 before → 1325 after**; 1962 base-equal rows removed. Untouched base: 2247 objects. Table: [part-server.tsv](part-server.tsv); row-level comparison: [reduction-server.tsv](reduction-server.tsv).

Actions: 13/13 succeeded. Exact statuses: [operator/server/actions-status.tsv](operator/server/actions-status.tsv). Separate stdout/stderr and lifecycle/restart/destruction records: (not published: orchestration or scratch).

| Action | Exit status | Seconds |
|---|---:|---:|
| server_prerequisites | 0 | 48 |
| server_compose | 0 | 18 |
| server_orchestrator | 0 | 19 |
| server_reverse_proxy | 0 | 0 |
| server_database | 0 | 1 |
| server_binary_service | 0 | 2 |
| server_scheduled_jobs | 0 | 1 |
| server_firewall | 0 | 0 |
| server_account | 0 | 0 |
| server_kernel_parameters | 0 | 0 |
| server_swap | 0 | 2 |
| server_automatic_updates | 0 | 0 |
| server_log_rotation | 0 | 0 |

| Inventory | Filesystem complete | Ownership complete | Recorded gaps | Nonzero queries |
|---|---|---|---:|---:|
| [server](raw/server/metadata.json) | true | true | 6 | 17 |
| [server-base](raw/server-base/metadata.json) | true | true | 3 | 15 |

The collector metadata retains `ready_for_observation=false`; the operator does not override it. Coverage includes missing or unavailable interfaces; precise status, stderr and gap references remain in each raw inventory. A zero collector exit is not a claim that every fact was collected.

| Level:kind | Before | After |
|---|---:|---:|
| 1:access-rule | 39 | 3 |
| 1:account | 30 | 2 |
| 1:docker-container | 3 | 3 |
| 1:docker-image | 3 | 3 |
| 1:driver | 100 | 0 |
| 1:firewall-chain | 86 | 86 |
| 1:firewall-ipv4 | 244 | 244 |
| 1:firewall-ipv6 | 77 | 77 |
| 1:firewall-rule | 203 | 203 |
| 1:firewall-table | 8 | 8 |
| 1:group | 57 | 5 |
| 1:module-name | 211 | 41 |
| 1:package | 392 | 42 |
| 1:polkit-action | 92 | 0 |
| 1:port | 26 | 26 |
| 1:process | 162 | 81 |
| 1:service | 129 | 18 |
| 1:sudo-access | 13 | 3 |
| 1:timer | 11 | 11 |
| 1:unit-file | 176 | 14 |
| 1:user-service | 3 | 3 |
| 1:user-unit-file | 6 | 1 |
| 2:executable-code-outside-packages | 444 | 80 |
| 2:image | 14 | 0 |
| 2:image-container-store | 5 | 5 |
| 2:stored-outside-packages | 753 | 366 |

Execution details and every machine-specific deviation are recorded in (not published: orchestration or scratch). The following operator record is reproduced to keep this report self-contained; paths within that record are relative to operator/server/:


This is the authorized beyond-plan A3-I operation. Committed inputs were taken from C1 files named in PUBLISH.list and checked against input-files.sha256.tsv; see verified-inputs.tsv. The parent records the PUBLISH.list self-checksum discrepancy separately.

All 13 actions ran exactly once as ordinary guest user and returned 0. Exact action statuses are in actions-status.tsv and stdout/stderr in actions-logs/. No failed action was repaired or substituted. Input transport staged the unchanged script and library in /tmp/a3-actions. One graceful stop/start restart succeeded; boot-before.out and boot-after.out prove different boots. Lifecycle exits/times are in lifecycle.json.

Both collectors returned 0. Lived inventory: 3287 objects, filesystem_complete=true, package_ownership_complete=true, six gaps (root and calops user service/timer/unit-file queries). Untouched base inventory: 2247 objects, both completeness flags true, three gaps (root user service/timer/unit-file queries). Both metadata records retain ready_for_observation=false. Collector exit 0 is not a claim of complete fact coverage. Detailed counts and gap references are in status.json and raw metadata.

Whole collector outputs are in ../../raw/server/ and ../../raw/server-base/. raw-sha256.txt and copy-verification.json verify every copied raw file without alteration. No private key was copied; the publication scan found no private-key body or known host identifiers. Both clones were destroyed successfully. No deviation from committed action or collector inputs occurred. Host orchestration logs replace host home paths with <host-home>; collector and guest action output remain unchanged.

The operator checks transport integrity and execution evidence only; independent review remains required. Reduction is performed by the parent using ../../reduce.py.

Recorded in UTC: 2026-11-23T11:26:50.873145+00:00

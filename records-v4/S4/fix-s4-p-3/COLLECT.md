# Extended collector for Supplement 1 step 4

This is a copy of the check-1 collector with additional fact files. It makes no hypothesis decision. The published text, ordinary action commands and original C1 files are unchanged. `S4/MISSING.tsv` is the fact list; `check-inputs-v4/supplement-1/step-4-instruments/S4/fix-s4-p-3/tables/missing-row-map.tsv` gives every dependent first-night ID. One row can depend on several facts, so `objects` counts must not be summed. The two fixed tables cover 2,007 distinct IDs; five source/content candidates and two trust-value candidates explicitly named in D1/RESULT.md add seven IDs, outside the fixed matching inputs. Gentoo has zero first-night IDs and a machine-level missing inventory fact.

All paths below are relative to a collector output directory. TSV uses UTF-8, tabs and CSV quoting. A JSON cell is explicitly identified. `evidence` fields name exact saved query outputs under `raw/`; semicolon-separated references identify multiple sources. Never replace an unknown or a failed query with an inference from a name, timestamp, prefix digest, read-only mount or current dependency graph.

## Invocation and prerequisites

Run on the laboratory host, never on the workstation. Python 3, the existing laboratory runner, SSH/Talos credentials and the registered unchanged bases are prerequisites. MicroOS solver-cache decoding uses the host's existing `dumpsolv`; absence is explicitly not collected. The legacy `talos.fixture_check()` tests only the original adapter and must be isolated from the extra adapter by the separate fixture runner; it is not an extended-collector test. The static helper is supplied as both one gzip file and deterministic chunks; the complete gzip takes precedence, otherwise all numbered chunks are joined. `probe-build.json` records source/runtime/binary hashes. Building is server-only through `build_probe.py`, with two compiler threads and a task-local cache; the toolchain is not modified.

```sh
LAB_ROOT="$TASK_LAB" check-inputs-v4/supplement-1/step-4-instruments/S4/fix-s4-p-3/collect.sh --rehearsal reh-s4-SYSTEM-N NEW_OUTPUT
C1_INPUTS_COMMIT="$INPUTS_COMMIT" LAB_ROOT="$TASK_LAB" \
  check-inputs-v4/supplement-1/step-4-instruments/S4/fix-s4-p-3/collect.sh --observe d1b-SYSTEM NEW_OUTPUT
```

Replace SYSTEM with the registered system identifier; the exact five commands are in `COMMANDS.md`. An observation requires the input commit variable and separate operator authorization. The preparation only used rehearsal mode. Rehearsal guards require a `reh-` name, a disposable overlay and its registered read-only backing image. No host inventory mode exists.

## Original tables and levels

`objects.tsv`, `level-1.tsv`, `level-2.tsv` retain exactly `id, machine, level, kind, name, members, evidence`. IDs retain the check-1 generation algorithm. Level one is objects in force; level two is stored objects outside established package ownership, with separate code rows. The collection of extra facts does not reclassify objects or transfer decisions. Original ownership flags and their limitations remain.

`members/ID.tsv` retains `path, type, mode, owner, size, mtime, executable, signature, persistence`; `owner` is numeric UID:GID. `signature` is still explicitly the 4096-byte prefix, for schema compatibility. `package-files.tsv` retains `package, path, integrity, evidence, rule`; `package` joins to the package object ID. `configuration-origin.tsv` retains the original timestamp/script-mention evidence and unknown causal origin.

`coverage.tsv` retains `query, exit_status, duration, rows, bytes, stdout, stderr, status, object_rows`. `metadata.json` records UTC time, system, duration, implemented traversal/ownership completeness and gaps. A zero collector exit does not imply every optional query or every historical fact succeeded. `raw/` retains bounded command text, stdout and separate stderr. The host MicroOS decoder additionally uses `raw/s4-solv-host-N.out/.err`, with its input referenced by the source sidecar.

The active `/etc` snapshot/subvolume now remains an atomic snapshot row with `expanded=true` while its children are traversed. Other snapshot boundaries remain as in C1. Nested immutable snapshots are not silently treated as the current root.

## Common added tables

| File | Exact columns | Object-to-fact join and meaning |
|---|---|---|
| `full-digests.tsv` | `path, algorithm, digest, bytes, status, reason, evidence` | A code/object name or stored member path joins to `path`. Complete SHA256 of scanned unowned regular files; unknown on cap, unsafe open or unstable read. Reference comparisons, when available, are in separate tables. |
| `object-fact-index.tsv` | `object_id, path, fact_file, join_column` | Direct object ID to candidate path in `full-digests.tsv`; missing digest rows are not evidence of absence. Stored groups link their immediate unowned members. |
| `store-members.tsv` | `object_ids, store, path, type, mode, uid, gid, size, target, prefix_signature, persistence, opaque_kind, evidence` | JSON `object_ids` links the original opaque store; group parents can join their child store path. Inner metadata is separate from original objects. This table stores metadata and prefix signatures, without a reference-image comparison column. |
| `store-coverage.tsv` | `object_ids, store, query_exit, traversal_complete, members, inner_opaque, evidence` | Per-store traversal status and explicit remaining nested boundaries. Completion covers the implemented traversal only. |
| `font-cache-sources.tsv` | `path, query_exit, evidence` | Parent group name identifies cache members; raw `fc-cat -v` output names cached directories/fonts. |
| `font-source-packages.tsv` | `path, package_ids` | Exact font source path to JSON package ID list, then `objects.tsv` and `package-files.tsv`. A cache filename alone supplies no source relationship. |

For the SSH/static-helper systems, native package full-hash comparison now permits a regular file up to 1 GiB instead of 16 MiB. The static helper requires a complete read and stable size, mtime, ctime and descriptor/path inode identity before reporting a digest. These checks detect ordinary concurrent modification; they are not an atomic filesystem snapshot. Symlinks retain native literal-target comparison. No content read follows a symlink component or opens a FIFO, socket, device or excluded pseudo path. Metadata reads remain capped at 16 MiB.

Store traversal uses the same static scanner with an explicit root-only expansion. It records inner members but does not extract image archives, execute payloads or establish who acquired them. Nested atomic image/snapshot boundaries remain explicit. The table stores metadata without per-member receipt or acquisition-event records.

## AlmaLinux

`alma-facts.tsv`: `object_id, path, fact, value, status, evidence`. Join directly by object ID, then distinguish the named fact. It records selected current configuration, installer directives with credential fields excluded, native persistent SELinux values, RPM key metadata/history, current unit policy, restricted retained operation history and selected package scriptlets. The scriptlets and installer directives are stored as source text; the adapter emits no complete per-object execution history.

Compiled dconf databases are read with a temporary profile selecting one existing database; no update or settings write is run. The profile is removed. `compiled-values` holds decoded values; schema references and profile files explain keys. `current-reader-snapshot` records only selected DCONF_PROFILE values and mapped database names from bounded process metadata, with at most 1 MiB per process source. It does not dump general environment/command lines and cannot establish absence of other past or possible consumers.

`alma-key-events.tsv`: `object_id, key_id, fingerprint, key_source, import_timestamp, success_timestamp, preceding_command, source_file, log_segment, command_line, event_line, success_line, status, evidence`. The package row joins directly by `object_id`; `key_id` must match the literal key component of its RPM name. `alma-key-event-coverage.tsv`: `source, status, lines, bytes, query_exit_status, evidence` records each queried DNF log, a query-level status row, and any read/size limit. The raw query saves the structured event fields and their exact source/line references. `fields-recorded` means those fields were parsed; unknown fields retain their `unknown:` prefix.

The preceding DNF command is the last permitted install command in the same log-initialization segment. Neither a process identifier nor a transaction identifier linking that command to the import is recorded by this parser. Segment adjacency is retained as context; it is not a causal link or an acquisition-reason field. The original key acquisition reason can therefore remain unknown even with all measured fields present. Only DNF install arguments matching the adapter's safe grammar are emitted; excluded commands remain explicitly unknown. Each binary log read is capped at 32 MiB before text decoding; gzip logs are decoded as data. Nonzero query status marks any retained event rows `unknown:query-failed`. No command extracted from a log is executed.

The npm tables below are used on AlmaLinux as well as Void. Historical key acquisition, disablement, creation/choice and complete dconf use remain limited by missing causal records, even when current evidence queries succeed.

## Void Linux and npm

| File | Exact columns | Join |
|---|---|---|
| `npm-archive-sources.tsv` | `lock, package_root, resolved, integrity, cache, status, evidence` | Package root or member path prefix selects the source record. The record identifies its reference source (lock, installed metadata or cache index). |
| `npm-member-integrity.tsv` | `object_ids, package_root, path, algorithm, expected, actual, status, evidence` | JSON object IDs or exact member path. Complete member bytes or targets are compared with that reference; members absent from it carry not-compared-to-archive. |
| `old-package-receipt-sources.tsv` | `source, status, evidence` | Source identifies surviving installed/residual XBPS metadata or a cached kernel package archive. |
| `old-package-member-integrity.tsv` | `object_ids, path, source, type, expected, actual, status, evidence` | JSON IDs or exact member path; source joins the prior table. Missing comparison references carry no-reference-found in the handoff copy. Only entries in the queried manifests have reference fields. |
| `void-configuration-facts.tsv` | `object_ids, path, status, content_base64, historical_creator, evidence` | Current selected default/module/sudo/trust-key file bytes; creator remains separate and unknown absent causal evidence. |

Archives are parsed as data, never extracted over a filesystem or executed. npm cached content must match a cryptographic reference before a per-file comparison. The table contains a reference comparison, with no per-file installation-event field. The Void package-cache reader uses the existing guest libarchive through Python ctypes to read only files.plist (100,000 archive headers, 16 MiB metadata, 90 seconds); no package is installed or extracted. Installed/residual manifests and cached archives stay separate sources. npm first uses lock-integrity references, then installed package integrity or a verified cache-index identity reference when no lock exists. The handoff status names the cache-identity reference source. Reference archives must pass cryptographic integrity and exact package name/version checks; complete installed member hashes/targets are compared, and members absent from the reference are labeled not-compared-to-archive. The three routes are installed manifests, residual metadata and cached archive manifests.

## openSUSE MicroOS

| File | Exact columns | Join |
|---|---|---|
| `s4-microos-snapshot-files.tsv` | `snapshot_root, path, package_path, package, algorithm, expected, observed, comparison, manifest_evidence, digest_evidence, manifest_exit` | Stored member `path`; `package` is the identity from that snapshot root's RPM database, not transferred from the current root. |
| `s4-microos-snapshot-current.tsv` | `snapshot_path, current_path, snapshot_sha256, current_sha256, comparison, snapshot_evidence, current_evidence` | Exact snapshot member path and corresponding live path, complete SHA256 comparison of the two named paths. |
| `s4-microos-sources.tsv` | `path, status, content_base64, evidence` | Unit/sudo/sysusers/grubenv/SELinux source paths; a group joins its immediate members, unit rows use selected properties. |
| `s4-microos-unit-links.tsv` | `path, target, error` | Literal enablement/alias link paths from the active namespace. |
| `s4-microos-unit-selected.tsv` | `object_id, user, unit, properties_json, query_exit, evidence` | Direct unit ID; selected FragmentPath, drop-ins and source paths. Template definitions use `systemctl cat`; ordinary units use `show`. |
| `s4-microos-scriptlet-query.tsv` | `query_exit, evidence` | RPM installation script text, supporting source evidence without an execution assertion. |
| `s4-microos-selinux-stores.tsv` | `store_root, policy, query_exit, evidence` | Policy directory prefix to read-only native module format/checksum listing. |
| `s4-microos-solver-cache.tsv` | `path, content_status, query_exit, content_evidence, digest_status, sha256, digest_evidence` | Solver cache member path; complete bytes read safely, then decoded with bounded host `dumpsolv`. |

SELinux CIL/HLL copies have separate manifest and snapshot/current comparison tables. Current sysusers/default files and enablement links are retained as sources; no per-object chooser-event table is emitted. No classification follows from these tables.

## Talos Linux

The original documented API collector remains, with its original object columns and levels. The additional adapter records expanded bounded directory listings, current target-file hashes and the API daemon mount namespace in separate files. The added tables emit no original image-member manifest, pull-event history or per-object historical layer record. Talos queries never launch a shell in the guest.

| File | Exact columns | Join |
|---|---|---|
| `talos-image-sources.tsv` | `resource_id, image, evidence` | Exact image reference in current workload configuration; join image object name. No pull-actor field is emitted. |
| `talos-expanded-members.tsv` | `object_ids, path, type, mode, owner, size, link_target, evidence` | Direct IDs where supplied; for an old opaque directory, all descendants have its exact name plus `/` as prefix. Ordinary groups join immediate parent. |
| `talos-listing-coverage.tsv` | `directory, query_exit, status, members, evidence` | Exact directory path and status; each level's listing is separately bounded. |
| `talos-listing-boundaries.tsv` | `path, reason` | Explicit unexpanded boundaries/caps, never complete absence. |
| `talos-content.tsv` | `object_ids, path, status, bytes, sha256, prefix_hex, signature, query_exit, evidence, method, error_category, diagnostic` | Exact file/member path. Full bounded content hash, ELF/shebang signature, last-method result, no original-image comparison field. |
| `talos-content-attempts.tsv` | `object_ids, path, status, bytes, sha256, prefix_hex, signature, query_exit, evidence, method, error_category, diagnostic` | Same joins as content; retains each Read/Copy/refresh-read attempt separately so initial failures remain visible. |
| `talos-mountinfo.tsv` | `mount_id, parent_id, device, root, mountpoint, mount_options, optional_fields, filesystem, source, super_options, evidence` | Object/member path selects component-delimited covering mount candidates. Preserve stacked candidates and parent IDs; the daemon namespace need not equal every workload namespace. |
| `talos-mountinfo-coverage.tsv` | `query_exit, status, mounts, namespace, evidence` | Complete bounded parse status for the exact mountinfo source. |
| `talos-fact-index.tsv` | `object_id, name, members_file, members_join, content_file, content_join, backing, image_integrity` | Direct ID; subtree join above takes precedence for opaque directories. The existing backing and image_integrity fields retain their source references or explicit unknown markers. |

The extended BFS starts at `/etc`, `/opt`, `/var/system`, `/var/lib/containerd`, `/var/lib/kubelet` and `/var/log/containers`; bounds are 8,192 directories, 250,000 members and depth 48. Directory components named `proc`, `sys` and `dev` remain explicit conservative boundaries, including aliases inside workload trees. A component name is not proof that its contents are pseudo data. Listing queries have a 15-second transport bound and a remaining-member line bound. Symlink directories and special files are not followed.

All listed regular files within those six targets are eligible for streaming SHA256 and sixteen-byte ELF/shebang signatures. Each file is capped at 1 GiB and 30 seconds; four client reads can run concurrently, in batches of 64. No whole-file buffer or raw payload output is retained. The byte count must match the listed size; Talos provides no atomic no-follow descriptor or snapshot guarantee. Failed, changing and capped reads have an explicit status and no accepted digest. `content_status_counts` and `content_by_root` in diagnostics distinguish those failures. Unsuccessful eligible Read paths are selected inside the collector for the distinct Copy API: two concurrent clients, four paths per batch, 30 seconds per file, 1 GiB payload and 1 GiB plus 1 MiB compressed stream. The tar.gz stream must contain exactly one regular member with the expected basename and listed size; it is hashed without extraction or retention. Original attempts are preserved. Copy can truncate a growing file to its header size, so it has no atomic snapshot guarantee. The third and final method for remaining eligible failures takes fresh immediate-parent metadata, reads against that fresh size, and takes another metadata sample. Each metadata query is capped at 15 seconds / 1 MiB; Read remains 30 seconds / 1 GiB, with two workers, four paths per batch and a 160-second batch cap. Full Read and matching pre/post type, mode, owner, size and displayed timestamp are required. Raw JSON evidence retains `before`, `after` and `original_listing_size`; a refreshed value is never asserted equal to the original listing. Missing or nonregular paths and unstable/failed reads retain no digest. Same-size writes and lossy timestamps can evade this check; it is not an atomic snapshot. No fourth content method is used. Sanitized diagnostics replace the requested path, home prefix and numeric node address. Batch/listing exits and per-file content statuses are separate fields; no original-image comparison is performed.

The exact `/proc/self/mountinfo` query is a bounded exception to generic pseudo traversal: 1 MiB, 15 seconds, no traversal of `/proc`. Decode Linux path escapes `\040`, `\011`, `\012` and `\134` before comparing paths. Mountpoint equality or a component-delimited ancestor gives a candidate; apply the mountinfo visibility/stacking rules and preserve parent IDs instead of assuming that longest prefix resolves hidden mounts. The table contains current mount options/source and no historical writer or lower-layer comparison fields. Format reference: https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html .

## Diagnostics, readiness and retention

`fact-summary.json` contains only numerical/boolean reductions from collector memory: original row totals, successful query/fact counts, caps and unresolved adapter counts. In rehearsal the same diagnostic is also written beside the transient output as `OUTPUT.diagnostics.json`. This permits verification after the complete rehearsal inventory has been deleted unread. Rehearsal records retain status/duration, these reductions, query coverage and sanitized stderr; empty diagnostic files may be represented by a filename/size index. All nonempty diagnostics remain available; inventories, member tables and raw query stdout are deleted.

Rehearsal reports and diagnostics are records only, excluded from the instrument and classification handoff lists. The deciding parties receive no rehearsal output, readiness report, fact-status summary or part report. Independent acceptance remains separate from preparation.

## Revision scope and observation handoff

The active documentation and fact list are `S4/COLLECT.md`, `S4/MATCH.md`, `S4/MISSING.tsv`, `check-inputs-v4/supplement-1/step-4-instruments/S4/COMMANDS.md` and `S4/HANDOFF.md`. The dependency map is `check-inputs-v4/supplement-1/step-4-instruments/S4/fix-s4-p-3/tables/missing-row-map.tsv`. Core runtime code and the matching script remain in `check-inputs-v4/supplement-1/step-4-instruments/S4/collector`. The active entry point is `check-inputs-v4/supplement-1/step-4-instruments/S4/fix-s4-p-3/collect.sh`: its wrapper invokes that unchanged runtime and appends the Alma DNF event adapter only on AlmaLinux. `check-inputs-v4/supplement-1/step-4-instruments/S4/PUBLISH.list` is the instrument set; `S4/CLASSIFICATION-INPUTS.list` is the document subset for deciding parties, supplied alongside the new observation and matching output. `S4/fix-s4-p-3/RECORDS.list` is a separate publication set, not a classification input.

The operator runs the committed handoff copier before giving an observation to deciding parties. It changes only the 21 explicitly enumerated status-cell and diagnostic-counter labels. Both mapped unknown fields retain the `unknown:` prefix. Positive archive and directory labels name a lock reference or a directory entry; counter values stay unchanged. All object IDs, levels, kinds, names, membership, content, digests, evidence references, query exits and raw evidence are preserved. The original collector output remains a separate frozen record. HANDOFF.md describes the neutral field meanings and exact delivery procedure. The mapping and operator audit remain outside the deciding parties' document set.

V09/M14 list the choice events and consumer/use records missing for the two trust-value groups named by D1/RESULT.md. The current collector emits no per-value choice history or complete consumer/use table. File metadata, prefix signatures and eligible whole-file digests retain their usual path joins; they are not relabeled as those missing records. No additional machine, action, case, or matching input is introduced. Whether the text decides these objects remains for the deciding parties within the authorized scope.

`objects` in MISSING.tsv remains an integer count of dependent first-night IDs, as required by the original task. Matching limits appear in `how_recorded_now` and `check-inputs-v4/supplement-1/step-4-instruments/S4/fix-s4-p-3/checks/match-scope.tsv`: RESULT-only IDs have zero fixed-input matching routes; M04/M05 each have at most one structurally eligible ID. Eligibility does not promise a match in a new inventory.

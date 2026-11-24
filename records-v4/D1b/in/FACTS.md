# Handoff fact locations

2026-11-23 UTC. All facts below come from the delivered handoff copies.

An inventory ID is `d1b-MACHINE-RAW_ID`. Remove that exact machine prefix to obtain the unchanged collector ID, or use `D1b/in/object-id-map.tsv` (`id`, `machine`, `raw_id`). The handoff object, member, package and fact tables and the fixed matcher all use the unchanged raw ID. No content hash matching is implied.

`members` cells and fields explicitly described as JSON must be JSON-decoded; a few inherited rows contain a JSON string holding another JSON value. Evidence paths are relative to the corresponding (not published: record outside selected evidence) directory. Semicolon-separated evidence references retain each named output. For a raw query, `.sh` records its exact command, `.out` its output, and `.err` its error output; `coverage.tsv` records its exit/status and bound.

Package installation reason is the `reason` field in the package object's decoded `members`, with the recorded source/native fields and evidence. `explicit`, `dependency`, and `unknown` are collector values. File comparisons are the `package-files.tsv` rows keyed by that raw package ID and exact path. Omitted file rows, unknown comparisons, and missing reason fields remain unrecorded facts.

For every member group, decode `members.file` and read that exact `members/RAW_ID.tsv` file completely. Its columns are `path`, `type`, `mode`, `owner`, `size`, `mtime`, `executable`, `signature`, `persistence`. `members.count`, `members.complete`, metadata coverage and the underlying query qualify the list. The signature in this inherited table covers only a 4096-byte prefix. A group without an expanded table has only the bounded facts named in its row and the additional store/listing tables; it has no invented full member list.

For stored paths on the SSH systems, the member row's `persistence` (or the individual object's decoded metadata) is the collector's recorded filesystem fact; inspect its saved scan evidence. Inner store members have a separate `persistence`. For Talos, use the recorded `backing` field and covering candidates in `talos-mountinfo.tsv`, with its namespace/status table and explicit unknown values. A current path, read-only flag or digest alone is not a persistence or historical-creator record.

Every root TSV below is listed with its actual columns and row count. `fact-table-status.json` records numerical distributions of returned status fields, without filling missing values. `metadata.json`, `fact-summary.json` and `coverage.tsv` retain traversal bounds, query failures and numeric reductions. The handoff bytes remain the evidence.

## alma

(not published: record outside selected evidence).

No delivered object inventory; no facts asserted for this machine.

## void

`D1b/handoff/void/`.

| Exact file | Rows | Columns | ID/path lookup and recorded fields |
|---|---:|---|---|
| `D1b/handoff/void/configuration-origin.tsv` | 845 | `path`, `created`, `rule_uncertainty`, `mtime`, `ctime`, `package_script_mentions`, `installation_time_evidence`, `evidence` | Join an exact object/member path to `path`. The created field and causal limitations are explicit; modification times and script mentions do not supply a creation event. |
| `D1b/handoff/void/coverage.tsv` | 158 | `query`, `exit_status`, `duration`, `rows`, `bytes`, `stdout`, `stderr`, `status`, `object_rows` | Match an evidence filename to `stdout`; retain query exit_status, duration, status and stderr. Exit zero alone does not assert a known value in every returned field. |
| `D1b/handoff/void/font-cache-sources.tsv` | 1 | `path`, `query_exit`, `evidence` | Exact cache member path joins `path`; evidence names saved fc-cat output identifying its source directories/fonts. |
| `D1b/handoff/void/font-source-packages.tsv` | 47 | `path`, `package_ids` | Exact source font path joins `path`; JSON package_ids joins raw package IDs and package-files.tsv. |
| `D1b/handoff/void/full-digests.tsv` | 11306 | `path`, `algorithm`, `digest`, `bytes`, `status`, `reason`, `evidence` | Exact object/member path joins `path`; algorithm, digest, bytes, status and reason describe the complete bounded read, with no accepted digest for a failed read. |
| `D1b/handoff/void/level-1.tsv` | 1211 | `id`, `machine`, `level`, `kind`, `name`, `members`, `evidence` | Same IDs and cells as the corresponding level-1 rows of objects.tsv. |
| `D1b/handoff/void/level-2.tsv` | 2068 | `id`, `machine`, `level`, `kind`, `name`, `members`, `evidence` | Same IDs and cells as the corresponding level-2 rows of objects.tsv. |
| `D1b/handoff/void/npm-archive-sources.tsv` | 41 | `lock`, `package_root`, `resolved`, `integrity`, `cache`, `status`, `evidence` | Exact package_root, or a component-delimited member beneath it, locates the archive source. lock/resolved/integrity/cache/status/evidence identify the reference and verification. |
| `D1b/handoff/void/npm-member-integrity.tsv` | 482 | `object_ids`, `package_root`, `path`, `algorithm`, `expected`, `actual`, `status`, `evidence` | JSON object_ids contains raw IDs, or join exact member path. package_root joins npm-archive-sources.tsv. expected/actual/status retain the complete byte or target comparison. |
| `D1b/handoff/void/object-fact-index.tsv` | 15751 | `object_id`, `path`, `fact_file`, `join_column` | Raw ID joins `object_id`; `path`, `fact_file` and `join_column` identify the next lookup exactly. |
| `D1b/handoff/void/objects.tsv` | 3279 | `id`, `machine`, `level`, `kind`, `name`, `members`, `evidence` | Find the unchanged raw ID in `id`. `members` is JSON; package rows carry `reason`, `manager`, and available reason-source/native-record fields. Unknown values remain unknown. A `members.file` entry names the separate member table. |
| `D1b/handoff/void/old-package-member-integrity.tsv` | 33435 | `object_ids`, `path`, `source`, `type`, `expected`, `actual`, `status`, `evidence` | JSON object_ids contains raw IDs, or use exact path. source links the manifest source. type/expected/actual/status/evidence retain comparisons; no-reference-found does not provide an original reference. |
| `D1b/handoff/void/old-package-receipt-sources.tsv` | 17 | `source`, `status`, `evidence` | source joins the source field of old-package-member-integrity.tsv; status and evidence distinguish the recorded manifest sources. |
| `D1b/handoff/void/package-files.tsv` | 37904 | `package`, `path`, `integrity`, `evidence`, `rule` | `package` is the raw package object ID; `path` is the supplied file. `integrity` records unchanged, changed, missing or unknown, with its `rule` and saved query evidence. This is the recorded reference comparison; no inference is made for omitted or unknown rows. |
| `D1b/handoff/void/store-coverage.tsv` | 3 | `object_ids`, `store`, `query_exit`, `traversal_complete`, `members`, `inner_opaque`, `evidence` | JSON `object_ids` or exact `store` joins the row. query_exit, traversal_complete, members and inner_opaque bound what was read. |
| (not published: over 20 MB) | 72162 | `object_ids`, `store`, `path`, `type`, `mode`, `uid`, `gid`, `size`, `target`, `prefix_signature`, `persistence`, `opaque_kind`, `evidence` | JSON `object_ids` contains raw IDs. `store` is the root; a parent member can join its child store path. Inner path metadata, target, prefix signature and persistence are retained independently. |
| `D1b/handoff/void/void-configuration-facts.tsv` | 11 | `object_ids`, `path`, `status`, `content_base64`, `historical_creator`, `evidence` | JSON object_ids contains raw IDs, or use exact path. content_base64 holds selected current bytes; historical_creator is separate and can remain unknown. |

Exact member files: (not published: record outside selected evidence), reached through the object row's `members.file`. All files and every member row are retained. For groups whose collector row gives no member file, use its explicit inline members and the joins above; absent expansion stays absent.

`D1b/handoff/void/metadata.json` fields `utc`, `machine`, `system`, `duration`, `filesystem_complete`, `package_ownership_complete`, `gaps`, `ready_for_observation` are retained exactly. `ready_for_observation` is an inherited collector field, not a substituted operator outcome.

`D1b/handoff/void/fact-summary.json` retains the original numeric/boolean reductions and adapter status counters. The source query files under `D1b/handoff/void/raw/` retain the actual output, stderr and exact commands referenced by each evidence cell.

## gentoo

`D1b/handoff/gentoo/`.

| Exact file | Rows | Columns | ID/path lookup and recorded fields |
|---|---:|---|---|
| `D1b/handoff/gentoo/configuration-origin.tsv` | 273 | `path`, `created`, `rule_uncertainty`, `mtime`, `ctime`, `package_script_mentions`, `installation_time_evidence`, `evidence` | Join an exact object/member path to `path`. The created field and causal limitations are explicit; modification times and script mentions do not supply a creation event. |
| `D1b/handoff/gentoo/coverage.tsv` | 233 | `query`, `exit_status`, `duration`, `rows`, `bytes`, `stdout`, `stderr`, `status`, `object_rows` | Match an evidence filename to `stdout`; retain query exit_status, duration, status and stderr. Exit zero alone does not assert a known value in every returned field. |
| `D1b/handoff/gentoo/font-cache-sources.tsv` | 0 | `path`, `query_exit`, `evidence` | Exact cache member path joins `path`; evidence names saved fc-cat output identifying its source directories/fonts. |
| `D1b/handoff/gentoo/font-source-packages.tsv` | 161 | `path`, `package_ids` | Exact source font path joins `path`; JSON package_ids joins raw package IDs and package-files.tsv. |
| (not published: over 20 MB) | 152216 | `path`, `algorithm`, `digest`, `bytes`, `status`, `reason`, `evidence` | Exact object/member path joins `path`; algorithm, digest, bytes, status and reason describe the complete bounded read, with no accepted digest for a failed read. |
| `D1b/handoff/gentoo/level-1.tsv` | 1210 | `id`, `machine`, `level`, `kind`, `name`, `members`, `evidence` | Same IDs and cells as the corresponding level-1 rows of objects.tsv. |
| `D1b/handoff/gentoo/level-2.tsv` | 31565 | `id`, `machine`, `level`, `kind`, `name`, `members`, `evidence` | Same IDs and cells as the corresponding level-2 rows of objects.tsv. |
| (not published: over 20 MB) | 214095 | `object_id`, `path`, `fact_file`, `join_column` | Raw ID joins `object_id`; `path`, `fact_file` and `join_column` identify the next lookup exactly. |
| `D1b/handoff/gentoo/objects.tsv` | 32775 | `id`, `machine`, `level`, `kind`, `name`, `members`, `evidence` | Find the unchanged raw ID in `id`. `members` is JSON; package rows carry `reason`, `manager`, and available reason-source/native-record fields. Unknown values remain unknown. A `members.file` entry names the separate member table. |
| (not published: over 20 MB) | 109382 | `package`, `path`, `integrity`, `evidence`, `rule` | `package` is the raw package object ID; `path` is the supplied file. `integrity` records unchanged, changed, missing or unknown, with its `rule` and saved query evidence. This is the recorded reference comparison; no inference is made for omitted or unknown rows. |
| `D1b/handoff/gentoo/store-coverage.tsv` | 2 | `object_ids`, `store`, `query_exit`, `traversal_complete`, `members`, `inner_opaque`, `evidence` | JSON `object_ids` or exact `store` joins the row. query_exit, traversal_complete, members and inner_opaque bound what was read. |
| `D1b/handoff/gentoo/store-members.tsv` | 530 | `object_ids`, `store`, `path`, `type`, `mode`, `uid`, `gid`, `size`, `target`, `prefix_signature`, `persistence`, `opaque_kind`, `evidence` | JSON `object_ids` contains raw IDs. `store` is the root; a parent member can join its child store path. Inner path metadata, target, prefix signature and persistence are retained independently. |

Exact member files: (not published: record outside selected evidence), reached through the object row's `members.file`. All files and every member row are retained. For groups whose collector row gives no member file, use its explicit inline members and the joins above; absent expansion stays absent.

`D1b/handoff/gentoo/metadata.json` fields `utc`, `machine`, `system`, `duration`, `filesystem_complete`, `package_ownership_complete`, `gaps`, `ready_for_observation` are retained exactly. `ready_for_observation` is an inherited collector field, not a substituted operator outcome.

`D1b/handoff/gentoo/fact-summary.json` retains the original numeric/boolean reductions and adapter status counters. The source query files under `D1b/handoff/gentoo/raw/` retain the actual output, stderr and exact commands referenced by each evidence cell.

## microos

`D1b/handoff/microos/`.

| Exact file | Rows | Columns | ID/path lookup and recorded fields |
|---|---:|---|---|
| `D1b/handoff/microos/configuration-origin.tsv` | 61 | `path`, `created`, `rule_uncertainty`, `mtime`, `ctime`, `package_script_mentions`, `installation_time_evidence`, `evidence` | Join an exact object/member path to `path`. The created field and causal limitations are explicit; modification times and script mentions do not supply a creation event. |
| `D1b/handoff/microos/coverage.tsv` | 166 | `query`, `exit_status`, `duration`, `rows`, `bytes`, `stdout`, `stderr`, `status`, `object_rows` | Match an evidence filename to `stdout`; retain query exit_status, duration, status and stderr. Exit zero alone does not assert a known value in every returned field. |
| `D1b/handoff/microos/font-cache-sources.tsv` | 0 | `path`, `query_exit`, `evidence` | Exact cache member path joins `path`; evidence names saved fc-cat output identifying its source directories/fonts. |
| `D1b/handoff/microos/font-source-packages.tsv` | 18 | `path`, `package_ids` | Exact source font path joins `path`; JSON package_ids joins raw package IDs and package-files.tsv. |
| `D1b/handoff/microos/full-digests.tsv` | 18404 | `path`, `algorithm`, `digest`, `bytes`, `status`, `reason`, `evidence` | Exact object/member path joins `path`; algorithm, digest, bytes, status and reason describe the complete bounded read, with no accepted digest for a failed read. |
| `D1b/handoff/microos/level-1.tsv` | 1464 | `id`, `machine`, `level`, `kind`, `name`, `members`, `evidence` | Same IDs and cells as the corresponding level-1 rows of objects.tsv. |
| `D1b/handoff/microos/level-2.tsv` | 5103 | `id`, `machine`, `level`, `kind`, `name`, `members`, `evidence` | Same IDs and cells as the corresponding level-2 rows of objects.tsv. |
| `D1b/handoff/microos/object-fact-index.tsv` | 30018 | `object_id`, `path`, `fact_file`, `join_column` | Raw ID joins `object_id`; `path`, `fact_file` and `join_column` identify the next lookup exactly. |
| `D1b/handoff/microos/objects.tsv` | 6567 | `id`, `machine`, `level`, `kind`, `name`, `members`, `evidence` | Find the unchanged raw ID in `id`. `members` is JSON; package rows carry `reason`, `manager`, and available reason-source/native-record fields. Unknown values remain unknown. A `members.file` entry names the separate member table. |
| `D1b/handoff/microos/package-files.tsv` | 18575 | `package`, `path`, `integrity`, `evidence`, `rule` | `package` is the raw package object ID; `path` is the supplied file. `integrity` records unchanged, changed, missing or unknown, with its `rule` and saved query evidence. This is the recorded reference comparison; no inference is made for omitted or unknown rows. |
| `D1b/handoff/microos/s4-microos-scriptlet-query.tsv` | 1 | `query_exit`, `evidence` | evidence points to the RPM installation script source output; query_exit is retained. Source text is not an execution event. |
| `D1b/handoff/microos/s4-microos-selinux-stores.tsv` | 2 | `store_root`, `policy`, `query_exit`, `evidence` | Use the component-delimited store_root/policy directory containing the member. evidence names the native module format/checksum listing; query_exit retains failure. |
| `D1b/handoff/microos/s4-microos-snapshot-current.tsv` | 16177 | `snapshot_path`, `current_path`, `snapshot_sha256`, `current_sha256`, `comparison`, `snapshot_evidence`, `current_evidence` | Exact snapshot member joins snapshot_path; current_path names the separately read live file. Both complete SHA256 values, comparison and evidence are retained. |
| `D1b/handoff/microos/s4-microos-snapshot-files.tsv` | 20400 | `snapshot_root`, `path`, `package_path`, `package`, `algorithm`, `expected`, `observed`, `comparison`, `manifest_evidence`, `digest_evidence`, `manifest_exit` | Exact stored member path joins path. snapshot_root identifies that RPM database; package_path/package are its recorded names. algorithm/expected/observed/comparison and manifest/digest evidence retain that comparison. |
| `D1b/handoff/microos/s4-microos-solver-cache.tsv` | 3 | `path`, `content_status`, `query_exit`, `content_evidence`, `digest_status`, `sha256`, `digest_evidence` | Exact cache path joins path. content_status/query_exit/content_evidence describe the safe byte read and host decoder; digest_status/sha256/digest_evidence describe the complete digest. |
| `D1b/handoff/microos/s4-microos-sources.tsv` | 1318 | `path`, `status`, `content_base64`, `evidence` | Join exact object/member path, or a source path selected by the unit table, to path. status/content_base64/evidence retain the bounded current source bytes. |
| `D1b/handoff/microos/s4-microos-unit-links.tsv` | 188 | `path`, `target`, `error` | Exact member/link path joins path. target and error are current link observations. |
| `D1b/handoff/microos/s4-microos-unit-selected.tsv` | 263 | `object_id`, `user`, `unit`, `properties_json`, `query_exit`, `evidence` | Raw ID joins object_id. user/unit and properties_json identify current FragmentPath, drop-ins and source paths; query_exit/evidence retain the query result. |
| `D1b/handoff/microos/store-coverage.tsv` | 0 | `object_ids`, `store`, `query_exit`, `traversal_complete`, `members`, `inner_opaque`, `evidence` | JSON `object_ids` or exact `store` joins the row. query_exit, traversal_complete, members and inner_opaque bound what was read. |
| `D1b/handoff/microos/store-members.tsv` | 0 | `object_ids`, `store`, `path`, `type`, `mode`, `uid`, `gid`, `size`, `target`, `prefix_signature`, `persistence`, `opaque_kind`, `evidence` | JSON `object_ids` contains raw IDs. `store` is the root; a parent member can join its child store path. Inner path metadata, target, prefix signature and persistence are retained independently. |

Exact member files: (not published: record outside selected evidence), reached through the object row's `members.file`. All files and every member row are retained. For groups whose collector row gives no member file, use its explicit inline members and the joins above; absent expansion stays absent.

`D1b/handoff/microos/metadata.json` fields `utc`, `machine`, `system`, `duration`, `filesystem_complete`, `package_ownership_complete`, `gaps`, `ready_for_observation` are retained exactly. `ready_for_observation` is an inherited collector field, not a substituted operator outcome.

`D1b/handoff/microos/fact-summary.json` retains the original numeric/boolean reductions and adapter status counters. The source query files under `D1b/handoff/microos/raw/` retain the actual output, stderr and exact commands referenced by each evidence cell.

## talos

`D1b/handoff/talos/`.

| Exact file | Rows | Columns | ID/path lookup and recorded fields |
|---|---:|---|---|
| `D1b/handoff/talos/coverage.tsv` | 1418 | `query`, `exit_status`, `duration`, `rows`, `bytes`, `stdout`, `stderr`, `status`, `object_rows` | Match an evidence filename to `stdout`; retain query exit_status, duration, status and stderr. Exit zero alone does not assert a known value in every returned field. |
| `D1b/handoff/talos/level-1.tsv` | 225 | `id`, `machine`, `level`, `kind`, `name`, `members`, `evidence` | Same IDs and cells as the corresponding level-1 rows of objects.tsv. |
| `D1b/handoff/talos/level-2.tsv` | 53 | `id`, `machine`, `level`, `kind`, `name`, `members`, `evidence` | Same IDs and cells as the corresponding level-2 rows of objects.tsv. |
| `D1b/handoff/talos/objects.tsv` | 278 | `id`, `machine`, `level`, `kind`, `name`, `members`, `evidence` | Find the unchanged raw ID in `id`. `members` is JSON; package rows carry `reason`, `manager`, and available reason-source/native-record fields. Unknown values remain unknown. A `members.file` entry names the separate member table. |
| `D1b/handoff/talos/package-files.tsv` | 287 | `package`, `path`, `integrity`, `evidence`, `rule` | `package` is the raw package object ID; `path` is the supplied file. `integrity` records unchanged, changed, missing or unknown, with its `rule` and saved query evidence. This is the recorded reference comparison; no inference is made for omitted or unknown rows. |
| `D1b/handoff/talos/talos-content-attempts.tsv` | 6031 | `object_ids`, `path`, `status`, `bytes`, `sha256`, `prefix_hex`, `signature`, `query_exit`, `evidence`, `method`, `error_category`, `diagnostic` | Same joins as talos-content.tsv; each implemented Read, Copy or refreshed-metadata Read attempt remains separately recorded. |
| `D1b/handoff/talos/talos-content.tsv` | 5963 | `object_ids`, `path`, `status`, `bytes`, `sha256`, `prefix_hex`, `signature`, `query_exit`, `evidence`, `method`, `error_category`, `diagnostic` | JSON object_ids or exact member path joins the row. status/bytes/sha256/prefix_hex/signature/query_exit/evidence/method/error_category/diagnostic describe the last accepted or failed bounded content method. No installed-image comparison field is present. |
| `D1b/handoff/talos/talos-expanded-members.tsv` | 8503 | `object_ids`, `path`, `type`, `mode`, `owner`, `size`, `link_target`, `evidence` | JSON object_ids links raw IDs where supplied. For a directory row, exact name plus slash selects descendants; for an ordinary member group, use immediate parent equality. path/type/mode/owner/size/link_target/evidence describe listed members. |
| `D1b/handoff/talos/talos-fact-index.tsv` | 53 | `object_id`, `name`, `members_file`, `members_join`, `content_file`, `content_join`, `backing`, `image_integrity` | Raw ID joins object_id; members_file/members_join/content_file/content_join specify further lookups. backing/image_integrity retain references or explicit unknown fields. |
| `D1b/handoff/talos/talos-image-sources.tsv` | 3 | `resource_id`, `image`, `evidence` | Exact image name joins image; resource_id and evidence identify the current workload configuration source. There is no historical pull-actor field. |
| `D1b/handoff/talos/talos-listing-boundaries.tsv` | 18 | `path`, `reason` | Exact path names an unexpanded boundary and reason. It does not assert an empty directory. |
| `D1b/handoff/talos/talos-listing-coverage.tsv` | 1219 | `directory`, `query_exit`, `status`, `members`, `evidence` | Directory name joins directory; query_exit/status/members/evidence describe each separately bounded listing. |
| `D1b/handoff/talos/talos-mountinfo-coverage.tsv` | 1 | `query_exit`, `status`, `mounts`, `namespace`, `evidence` | query_exit/status/mounts/namespace/evidence qualify the exact API-daemon mountinfo parse; other workload namespaces are not supplied by this row. |
| `D1b/handoff/talos/talos-mountinfo.tsv` | 29 | `mount_id`, `parent_id`, `device`, `root`, `mountpoint`, `mount_options`, `optional_fields`, `filesystem`, `source`, `super_options`, `evidence` | Decode Linux path escapes, then find mountpoints equal to or component-delimited ancestors of the object/member path. Preserve stacked candidates, parent IDs and namespace limits; do not infer the covering mount from longest prefix alone. |

Exact member files: (not published: record outside selected evidence), reached through the object row's `members.file`. All files and every member row are retained. For groups whose collector row gives no member file, use its explicit inline members and the joins above; absent expansion stays absent.

`D1b/handoff/talos/metadata.json` fields `utc`, `machine`, `system`, `duration`, `filesystem_complete`, `package_ownership_complete`, `gaps`, `ready_for_observation` are retained exactly. `ready_for_observation` is an inherited collector field, not a substituted operator outcome.

`D1b/handoff/talos/fact-summary.json` retains the original numeric/boolean reductions and adapter status counters. The source query files under `D1b/handoff/talos/raw/` retain the actual output, stderr and exact commands referenced by each evidence cell.

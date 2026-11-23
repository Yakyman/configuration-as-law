COLLECTOR: not ready

Historical collector-development snapshot. Current portability repairs, conservative fact handling and machine acceptance are documented in `COLLECT.md`, `FIX-C1-REH-1.md` and `READY.md`; original validation results below are retained as history.

2026-11-23 UTC. The second collector is implemented and the authorized tests below
passed. This is preparation evidence, not a hypothesis observation or a claim of
complete coverage on the check systems. Instructions and exact query sources:
`COLLECT.md`, `collector/PACKAGES.md`, `TALOS-COLLECT.md`.

| Requirement | Tested target and result | Evidence |
|---|---|---|
| A: levels, stored groups, executable code, schema | Disposable Debian cloud guest: 2,164 objects, 609 groups, 6,846 members. Rocky Linux 9 disposable container: 604 objects, 17 groups, 47 members. Both traversals and implemented ownership queries completed. No group sampling; a planted group has all 1,201 members, including a tab/newline name. | `raw/debian-validation.json`, `raw/rpm-validation.json`, `raw/debian-final/objects.tsv`, `raw/debian-final/members/`, `raw/rpm-final/objects.tsv` |
| A: in-force categories and failure coverage | Debian and Rocky queried system/user services, timers, processes/executables, accounts/groups, rules, module/driver names, sockets, networks and engines. Missing tools/stopped user managers remain not collected. Container and firewall JSON normalization passed separate guest fixtures. Complete real engine/network/firewall coverage was not exercised. | `raw/debian-final/coverage.tsv`, `raw/rpm-final/coverage.tsv`, `raw/parser-tests-final.log` |
| B: package reasons | Native dpkg/APT and RPM/DNF records exercised. Every emitted package has explicit/dependency/unknown. Seeded Debian package is explicit. Native-owned Python metadata is reconciled to native manifests. Other-manager adapters remain unverified or incomplete. | `raw/debian-final/objects.tsv`, `raw/rpm-final/objects.tsv`, `raw/seed-fixture.log`, `raw/debian-validation.json` |
| B: package-file integrity | Debian: 26,571 manifest rows, including 17,040 unchanged, 4 changed, 1 missing, 9,526 unknown. Seeded unchanged/changed/missing file and changed conffile assertions passed. RPM: 28,797 rows; unchanged/changed/missing/unknown all retained. Omitted container documentation files are not assumed present. | `raw/debian-final/package-files.tsv`, `raw/rpm-final/package-files.tsv`, `raw/debian-validation.json`, `raw/rpm-validation.json` |
| B: configuration creation facts | Debian generated configuration linked to exact post-install script mention and observed mtime/ctime. Creation remains unknown; birth time, installation interval and actual script-branch execution are not established. | `raw/debian-final/configuration-origin.tsv`, `raw/seed-fixture.log`, `raw/debian-validation.json` |
| B: complete member facts | Required member columns, counts, uniqueness and immediate-parent relation validated. 4096-byte prefix signature and all implemented full-digest algorithms checked in Debian fixture. Runtime/persistent/unknown and readonly flags use statfs. | `raw/guest-tests-v2.log`, `raw/debian-final/members/`, `raw/debian-validation.json` |
| C: bounded reads and failure continuation | Debian fixture: pseudo roots and symlink aliases refused for content reads; FIFO nonblocking; no helper pseudo-file opens in syscall trace; one-second timeout kills process group. Controller tests enforce timeout/output cap and then successfully run the next query. | `raw/guest-tests-v2.log`, `raw/probe-trace.log`, `raw/transport-tests.log`, `raw/transport-controls/coverage.tsv` |
| C: GNU, BusyBox, toybox; snapshots; readonly | Same static walker passed with all three PATH toolsets on disposable Debian; actual Btrfs snapshot remained one opaque object and its child was absent; a live subvolume remained walked under readonly mount. Whole-root readonly Rocky container completed in 6.585 seconds; DNF reason query failed there and is recorded. | `raw/guest-tests-v2.log`, `raw/rpm-readonly.log`, `raw/rpm-readonly/metadata.json`, `raw/rpm-readonly/coverage.tsv` |
| C: full-run duration | Final Debian run 25.208 s; Rocky 8.112 s; readonly Rocky 6.585 s. Fresh Debian before fixture additions completed in 21.3 s. These times do not establish completeness on larger or different installations. | `raw/debian-validation.json`, `raw/rpm-validation.json`, `raw/rpm-readonly.log`, `raw/earlier-run-summary.json` |
| D: Talos documented API | Documentation review and Debian-hosted mocks only. Bounded depth/count, no read/copy calls, complete decoded immediate lists, escaping/spacing, JSON stream parsing, failure continuation tested. Unavailable facts are explicitly listed. No Talos/check machine was contacted. | `TALOS-COLLECT.md`, `raw/guest-tests-v2.log` |
| E: permitted machines and cleanup | Only the disposable Debian cloud guest and Rocky-family containers were inventoried. Previous lab copied; previous bases unchanged. VM, task containers, images, copied disk, keys, build caches and server staging removed; shared slots preserved. | `raw/cleanup.json`, `raw/plan.md` |
| F: readiness record and independent checking | This file reports each requirement. Independent source review and subsequent evidence review are separate from implementation; neither asserts complete acceptance. | `raw/independent-review.md`, `raw/review.md` |

Not ready:

1. Exhaustive package coverage is missing for Flatpak/Snap/Ruby ownership and
   several user language managers. Pacman/XBPS verification and Portage selected
   sets are incomplete; the non-Debian/RPM adapters were not validated here.
2. Configuration creation timing is still unknown, and a read-only system image
   is not yet linked to every constituent file for image-based integrity.
3. Arbitrary relocated container stores, mounted images and snapshot mechanisms
   beyond the implemented cases can be traversed or omitted incorrectly. Full
   service/network/firewall coverage on other init systems remains untested.
4. Talos facts unavailable from the chosen bounded APIs remain not collected;
   see the explicit list in `TALOS-COLLECT.md`. It supplies exposed-object evidence,
   not a complete equivalent filesystem inventory. Live validation belongs to a
   separately authorized rehearsal.
5. Only Linux x86-64 is supported, and staging requires an executable writable
   location. Component no-follow protects content reads; concurrent namespace
   races and all internal filesystem reads of third-party query tools were not
   exhaustively verified.

Procedural record: an early adapter syntax/in-memory mock test ran on the
controller, outside the strict guest-only testing rule; it performed no machine
inventory. Acceptance claims above use the subsequently saved authorized guest
and container tests. No check system, NixOS or Guix was inventoried.

The earliest Debian run failed because `/run` was noexec; its failed queries
were retained in `raw/debian-full/`. Later corrections and expected results are
recorded before their checks in `raw/plan.md`. Narrow parser/member-reference
changes after the final full runs were checked in guest fixtures; their full
inventory counts are not represented as a later rerun.

# Talos operator record

2026-11-23 UTC. Release: Talos 1.14.6, committed in C1/KIT-READY.md.
Input commit: c62afbb5861fb038aa7da0aa00c0730ad140ec7c.
The records-host verifier passed 49 hashes before staging; the staged verifier also passed 49.
Runner SHA256: 3402697b02c88449fd6ba41e7137c404185c43a2bcd45fa211623d0d7e349733.
Task-local base, install, keys and client references used the registered existing resources unchanged.
Five shared slots were free before creation; the runner acquired one slot.

Only one creation and one collector invocation occurred. No ordinary actions are assigned to Talos.
Status/durations: new 0/8 seconds; collector 0/203 seconds; destroy 0/47 seconds.
Exact UTC starts and exits are in status.tsv; separate phase stdout/stderr are retained.
Native destroy completed; the disposable machine directory is absent. No cleanup fallback was needed.
Whole raw output is retained under D1b/raw/talos; transfer.json and raw-sha256.json establish exact transfer.
The remote runtime and original raw output remain for the coordinating operator's handoff.

Inventory: 278 objects, level 1 = 225, level 2 = 53. Level 2 was obtained partially.
The collector metadata reports filesystem_complete=false and retains listing count/depth boundaries.
Its package_ownership_complete=true counter is retained literally; its Talos gap states that complete
package ownership and the complete non-package second level were not collected.
The extra listings recorded 8,503 members across 1,219 directories with zero listing failures,
but retained 18 workload-or-pseudo boundaries (talos-listing-boundaries.tsv).
The original extension parser reports missing object identity (metadata.json).
No object decisions were made.

Facts against S4/MISSING.tsv: T01 has 3 current image-source rows but no historical actor;
T02 has the expanded listings above with explicit remaining boundaries;
T03 has current hashes/listing/mounts but no original image manifest or receipt comparison;
T04 has 29 API-daemon mount records, query exit 0, without complete historical overlay origin;
T05 has no per-member creation/derivation-event record;
T06 has 5,932 successful complete hashes out of 5,963 requested files, with 31 not-found results.
The first Read returned 5,929 ok, 31 read-error and 3 size-changed; Copy retained 34 archive-error
attempts; the final fresh-metadata Read returned 3 ok and 31 not-found. Every attempt is retained.
The 287 package-files rows have zero known integrity comparisons.
See fact-summary.json, talos-content.tsv, talos-content-attempts.tsv, talos-mountinfo-coverage.tsv,
talos-listing-coverage.tsv and metadata.json under the raw observation.

Deviations from committed instruments: none.

| Kind | Objects |
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

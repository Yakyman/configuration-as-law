# MicroOS instrument preparation

Prepared 2026-11-23 UTC. No object is decided. Rehearsal inventories are deleted unread.

## Primary sources and expected result before rehearsal

- https://rpm.org/docs/latest/manual/tags : “File cryptographic digest (aka hash) using algorithm specified in Filedigestalgo.” Snapshot membership must use that snapshot's RPM database.
- https://ftp.rpm.org/max-rpm/s1-rpm-query-parts.html documents --root as selecting the query root directory.
- https://www.freedesktop.org/software/systemd/man/256/org.freedesktop.systemd1.html : “UnitFileState encodes the install state of the unit file of FragmentPath.” Current state does not provide link creation history.
- https://www.freedesktop.org/software/systemd/man/latest/systemctl documents show properties and backing definition/drop-in files.
- C1/collector/probe.go stops recursion at directories identified as snapshots; the extension keeps the /etc object while traversing active members.
- check-inputs-v4/actions/README.md specifies no MicroOS actions. No action is invented.

Expected: a fresh committed copy boots, collector exits zero, active /etc descendants are counted, snapshot-specific RPM records and current unit sources are recorded. Full digests establish byte equality, not missing historical creators or absent original receipts.

## Frozen table groups

The 754 original rows partition: 22 account/group history; 8 sudo sources; 253 unit/user-unit definition and links; 7 unit selection/history; 10 executable snapshot receipt/integrity; 452 stored snapshot receipt/integrity; one active /etc; one grubenv contents/creation. Available evidence is not certification of history.

## Extra output contract

extra_microos.collect(ctx) executes after base object creation. Existing object columns and levels stay intact.

- s4-microos-snapshot-files.tsv: snapshot_root, path, package_path, package, algorithm, expected, observed, comparison, manifest_evidence, digest_evidence, manifest_exit. Stored objects join via member paths; executables via name. Snapshot-root RPM supplies package identity and expected digest/target. Equal means complete bytes/size or target agree, not creator provenance. Directory membership is separate.
- s4-microos-sources.tsv: path, status, content_base64, evidence. Selected fragments/drop-ins and symlinks lead to source paths. Account/group names can be searched in sysusers sources; sudo rows use all policy sources; /boot/grub2 uses grubenv. Historical cause remains unknown when absent.
- s4-microos-unit-links.tsv: path, target, error. Current enablement and alias links join unit names/fragments; this is not history.
- s4-microos-unit-selected.tsv: object_id, user, unit, properties_json, query_exit, evidence. Exact ID join; Id, Names, FragmentPath, SourcePath, DropInPaths, UnitFileState, UnitFilePreset, LoadState retained. Multiple matches explicit.
- s4-microos-scriptlet-query.tsv: query_exit, evidence. Raw current scriptlet source does not prove execution.
- Raw s4-microos-mounts and s4-microos-subvolume coverage records identify mounts/subvolumes.

Only diagnostics and aggregate counters may be read in rehearsal; source/package/member/object output is deleted unread.

`s4-microos-snapshot-current.tsv` columns: snapshot_path, current_path, snapshot_sha256, current_sha256, comparison, snapshot_evidence, current_evidence. Exact name/member-path join. Two full SHA256 values are compared; equality does not imply historical package receipt. Both digest statuses must be ok. The active-etc-descendants and active-etc-traversed counters certify that the former boundary was crossed; total/known counters distinguish partial digest availability.

A synthetic context check on 2026-11-23T14:05 UTC passed manifest-to-digest comparison, snapshot/current full comparison, and exact unit selection joins. This is parser validation, not machine readiness. Temporary fixture files were removed.

SELinux primary source: https://github.com/SELinuxProject/selinux/wiki/High-Level-Language-Infrastructure documents stored HLL, cached CIL and lang_ext, and conversion of HLL to CIL. https://raw.githubusercontent.com/SELinuxProject/selinux/master/policycoreutils/semodule/semodule.8 documents -S, -lfull and -m as policy-store root, full listing and SHA256 checksums. Before rehearsal, expected: read-only store listing and lang_ext content provide module identity/format evidence; absent package receipt/creator history is not inferred. s4-microos-selinux-stores.tsv columns store_root, policy, query_exit, evidence point to raw lists. A snapshot group joins by its path prefix under store_root and module name; current source equality remains separate from receipt.

Additional result-only extent facts: inactive RPM database and @System solver cache are included. Snapshot-root RPM manifests query the inactive database. https://raw.githubusercontent.com/openSUSE/libsolv/master/doc/dumpsolv.txt documents dumpsolv FILE as reading a solv file and writing its contents. Expected before rehearsal: if the installed reader exists, cache package contents decode; otherwise an explicit nonzero query records unavailability. Full cache digests and stored cookie/source bytes are retained. Current package identities from base package inventory and decoded solver identities can be compared; matching identities do not prove historical generation. s4-microos-solver-cache.tsv columns path, content_status, query_exit, content_evidence, digest_status, sha256, digest_evidence; object/group member paths join directly. No package is installed to obtain a reader.

## Attempt 2 expectation before run

Attempt 1 collector exited zero, but systemctl show aborted its batch at uninstantiated template units; stderr identifies the template-name rejection. The documented systemctl cat template syntax selects backing files without instantiation. Attempt 2 separately cats templates and batch-shows ordinary units; expected all 263 unit rows obtain source evidence without changing units.

Attempt 1 guest dumpsolv was absent. A read-only host prerequisite check found dumpsolv and libsolv available. Attempt 2 reads the complete bounded solv bytes via the safe helper and decodes with host dumpsolv, stdin only, no guest package install. The child has a 60-second timeout and 64MiB output-file limit; the input read is limited to16MiB. Expected: one original cache is decoded, with cookie bytes/full digest retained and current RPM package identities available for comparison. This is a second different method, not a repeated absent command. Raw host decoder evidence and stderr use raw/s4-solv-host-N.{out,err}; coverage includes s4-solv-host-decode.

## Final source validation expectation before run

The common extension replaces its quadratic object-index loop with an equivalent parent map; `S4/raw/index-equivalence.txt` records the synthetic equivalence check. A fresh third copy validates this final assembled source with unchanged MicroOS query methods and no ordinary actions. Expected: collector exits0 and reproduces the successful mechanism coverage of attempt2; timing may improve. This validates the changed instrument, not a new hypothesis or additional retry of a failed fact. Exact main, extended, packages, extra_microos and probe hashes are recorded before and after.

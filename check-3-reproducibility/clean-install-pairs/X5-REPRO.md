# X5 — independent installation reproducibility

**All six independently installed targets booted and were measured. Stand-level
Check 3 is `?` for each baseline; the hypothesis implication is also `?`.**
Package/closure content reproduces within every pair. Generated identities and
kernel-worker differences remain definition holes under the paper's criterion.

The fixed protocol was written and hashed
before execution. The criterion remains §9.4: **“The running components differ,
and the difference is not explained by differences in hardware.”** Equal package
content alone is insufficient to settle this criterion. Every raw difference is
retained; no open problem is decided here.

| Baseline | Exact input | Installation evidence | Stand / hypothesis (§9.1) |
|---|---|---|---|
| NixOS | nixpkgs `ac62194c3917d5f474c1a844b6fd6da2db95077d`; one configuration | Two empty disks, independent `nixos-install`, successful first boots | `?` / `?` |
| Guix System | channel commit `230aa373f315f247852ee07dff34146e9b480aec`; one `config.scm` and pinned `channels.scm` | Two empty disks, independent pinned `guix system init`, successful first boots | `?` / `?` |
| Debian | bookworm, snapshot `20250101T000000Z`; minbase plus one 12-package list and fixed recipe | Two empty disks, independent debootstrap/apt, successful first boots | `?` / `?` |

Full per-system reports, input hashes, exact commands and cleanup receipts:
NixOS, Guix, Debian.
Both partners of each pair use the same virtual hardware and input bytes.
Installer media and binary substitutes/packages can be shared; populated target
roots/stores are never cloned. This measures installation reproduction using
upstream binaries. It does not measure independent compilation.

## What the pairs reproduce

| Observation | NixOS | Guix System | Debian |
|---|---|---|---|
| Package/closure content | 580 reachable store objects: equal independently computed NAR hashes, all match registered hashes; 129 equal profile references | 353 reachable store objects: equal independently computed NAR hashes, all match registered hashes; 46 equal package/name/version/output/path rows | 168 equal package/version/architecture/status records, dependency rows and downloaded `.deb` hashes; all package-owned regular-file hashes equal |
| `/etc` | 150 paths each; 7 projected differing paths | 43 paths each; 8 projected differing paths | 622 paths each; 8 projected differing paths |
| Accounts/groups | 44 / 35 identical; shadow contains equal records in different order | 13 / 20 identical in account files; 13 shadow rows identical; NSS query gap below | 21 / 46 identical; shadow/gshadow bytes identical |
| Services/processes | Service/timer definitions/states and 14 userspace process records equal; total process counts 88 / 89 | Shepherd status/graph and 16 userspace process records equal; total process counts 98 / 98, with different kernel-worker names | Service/timer definitions/states and 15 userspace process records equal; total process counts 87 / 82 |
| Kernel/modules | Kernel/initrd hashes equal; 7,046 module-tree file hashes and 114 loaded module names equal | Kernel/initrd store content equal within the hashed closure; 6,573 module-tree file hashes and 60 loaded module names equal | Kernel and 4,037 module-tree file hashes equal; 69 loaded module names equal. Initrd archive differs, unpacked content/modes/symlinks equal |
| Persistent files outside store | 1,047 paths each; 46 projected differing union paths | 449 paths each; 21 projected differing union paths, plus separately inventoried persistent `/run`: 335 paths each, 72 differences | 16,634 paths each; 27 projected differing union paths. Corrected package-unowned subset: 2,147 paths each, 21 differences |

Counts include directories and reflect different filesystem layouts; each
comparison is within a baseline. “Projected” removes only inode, device, mtime
and ctime from the file manifest. All raw records and differences remain: NixOS
has 150 `/etc` and 1,063 outside-store raw differing union paths; Guix has 43,
450 and another 339 under `/run`; Debian has 622 and 16,636 respectively.
Processes and module observations retain full raw data
alongside explicitly described projections.

Evidence behind these counts: NixOS [native summary](raw-X5/nixos/analysis-summary.json)
and [manifest comparison](raw-X5/nixos/generic-comparison/summary.json);
Guix [closure comparison](raw-X5/guix/attempt-4/comparison-native/summary.json),
[manifest comparison](raw-X5/guix/attempt-4/comparison/summary.json) and
[`/run`/native supplement](raw-X5/guix/attempt-4/comparison-extra/summary.json);
Debian [manifest comparison](raw-X5/debian/comparison/summary.json),
[package supplement](raw-X5/debian/comparison/supplement-summary.json) and
[process/service projection](raw-X5/debian/comparison/projections-summary.json).
Root's mechanical cross-checks are saved for [NixOS](raw-X5/root-audit-nixos.json)
and [Guix](raw-X5/root-audit-guix.json) and [Debian](raw-X5/root-audit-debian.json);
these are not independent acceptance.

## Differences and the unchanged failure condition

| Baseline | Retained differences | What §9.4 allows / leaves undecided |
|---|---|---|
| NixOS | machine-id, SSH host keys, `.updated`, shadow ordering; store registration times; GRUB/UUID/device aliases; database, DHCP, seed, journal and temporary-directory state; kernel-worker labels/multiplicity | No hardware explanation demonstrated. Equal unique shadow rows and equal NAR hashes support the stated account/content equality. Generated identities and kernel-worker granularity remain holes (O1/O8/O9), not granted exceptions |
| Guix System | Six SSH key files and two Guix signing-key files; store registration metadata; DHCP/cache/database/seed/log state; temporary-file names; persistent `/run/udev` data, watch targets and UUID aliases; kernel-worker names | No hardware explanation demonstrated. Local signing/SSH identities and kernel-worker granularity remain holes (O1/O8/O9). Equal device/driver inventories do not erase differing udev state |
| Debian | machine-id and six SSH key files; directory sizes; initrd archive metadata; caches, random seed, logs/journal paths; filesystem UUID/device alias; kernel-worker labels/multiplicity | No hardware explanation demonstrated. Unpacked initrd equality does not erase its archive difference. Generated identities and kernel-worker granularity remain holes (O1/O8/O9), not granted exceptions |

**No observed running-component difference has been shown to qualify for the
hardware allowance.** Logs and caches are explicit derivative examples in §5.1;
§5.3 does not require transfer of unrecorded derivatives. That does not supply a
general exception for every generated identity, mutable configuration or state
file. The text does not settle whether the differing kernel-worker instances
are distinct recorded components, the same unresolved boundary identified in
[B Check 3](../../check-2-law/stand/RESULTS.md). Hence a full stand `1` is unsupported; an established
stand `0` is also not demonstrated. Baseline differences do not by themselves
establish property-inherent failure under §9.1.

## Coverage and repairs

NixOS's conventional `nix-env` system-profile query returns `{}` despite exit 0;
its profile lacks a package manifest. The 129 profile references and 580 closure
objects are reported as such, not as package counts or a fabricated architecture
inventory. Debian has no native Nix/Guix closure; its package/dependency/download
and installed-file sets are the explicit analogue used here.

Guix's 46 package rows contain name, version, output and store path, without a
separate per-package architecture field. Its generic `getent passwd/group`
commands were unavailable in PATH; the original errors remain. Account-file
contents and rule/configuration content were collected, but successful NSS
resolution is not claimed. The installer build channel, requested release
channel and packaged `guix describe` provenance are distinguished in the Guix
report; actual initialization used `time-machine -C channels.scm` at the stated
release commit.

Guix `/run` is on the persistent root. A supplement inventories it explicitly;
the observer uses a dedicated tmpfs at `/run/x5-observer`, recorded in the mount
inventory and excluded from the file traversal. No whole-directory volatility assumption is
used for Guix; `/run/systemd` and `/run/user` are absent on both targets.
All three pairs' persistent manifests show no read errors or
detected read races. They are sequential observations, not atomic snapshots;
filesystem extended attributes and future runtime states are not covered.

Guix's read-only post-shutdown supplement recovered 273 files per target, all
hash-matched to the live measurements. The two differently named `/tmp/tmp.*`
files contain the same DNS resolver line; their producer was not established.
The 60 changed common udev data files differ in initialization/watch fields and,
for the target disk, filesystem/partition UUIDs. The other `/run` differences
are UUID-link paths and watch targets; no changed device/model field was found.
See verified contents and
[exact line differences](raw-X5/guix/attempt-4/offline-content-line-differences.json).
These observations explain representation/state differences without granting
an additional exception to §9.4.

The generic Debian ownership query `dpkg-query -L '*'` failed. Its original
output and invalid partitions are retained and not used. Read-only recovery
verified all 831 dpkg database files per target against the original manifest;
corrected membership resolves guest parent-directory aliases while preserving
leaf symlinks. See repair and evidence.
This repaired measurement coverage without changing the protocol or predicate.

Per-system reports retain failed setup attempts and coverage repairs. The
measurement/failure protocol and source text checksums remained unchanged.
All owned VM units, temporary server directories/disks/caches and disposable
observer private keys were removed. A final server check
found all three working directories absent and no matching units loaded.
The raw evidence and final reports have a SHA-256 index at
`raw-X5/evidence-sha256.txt`.

The executor does not accept its own work.

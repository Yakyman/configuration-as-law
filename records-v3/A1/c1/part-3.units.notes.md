# Unit classification notes

Scope: 150 rows of kinds system-unit, system-units, user-unit, user-units from `../in/part-3.tsv`. No other classification was consulted. No objects were removed and no probes were run.

## Deciding sentences

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”
- S3-2: “If what the object does remains unknown, the case yields ?.”

## Homogeneous rule U

A loaded unit definition that controls process execution, service activation, filesystem mounting, cross-process dependencies or process resource grouping is MUST under S2.2-1 and S2.2-2. Removing its contribution removes the named management, activation, scheduling, mounting or ordering capability. Units are read as values; this does not make them code under S2.2-13, nor does it make their effects internal to one program under S2.2-7. Their effects reach independently executing processes, shared filesystem interfaces or system resources. A unit need not be currently active to provide a capability. A service that writes logs or maintains caches is not itself a log or cache.

This one rule covers the 139 singular loaded-unit rows; descriptions are taken from the inventory, with explicit documentation for three custom hooks below. The script formats each type's operational description and reasoning; it does not classify from an inventory label. Ten manually checked rows spanning its mechanisms:

| ID | Observed object | Check |
|---|---|---|
| nixos-002aa91047 | Root slice | Active resource hierarchy; slice documentation establishes cross-process resource management. |
| nixos-77462850bc | Basic system target | Loaded boot synchronization and grouping unit; target documentation establishes dependent-unit ordering. |
| nixos-0384997ab4 | System message-bus service | Active running separate bus process; service management has external IPC effects. |
| nixos-06be1b0d47 | Message-bus socket | Active running socket; socket documentation establishes IPC and process activation. |
| nixos-16081f0750 | Huge-pages mount | Active mounted kernel filesystem; removing mounting capability affects filesystem access. |
| nixos-f5fee7c08e | Filesystem trim timer | Active waiting scheduled discard service; timer documentation establishes timed activation. |
| nixos-46b677ba51 | Console password path watcher | Active waiting path unit; path documentation establishes event-triggered activation. |
| nixos-feed84b43d | Emergency shell service | Inactive but loaded shell-launch definition; availability is a capability, independent of current execution. |
| nixos-05069d5c04 | Boot/shutdown accounting service | Unit executes accounting writer; it is not the historical records that writer produces. |
| nixos-f5943b1625 | User temporary-file cleanup timer | Active user timer schedules another process; user scope does not confine effects to a program interface. |

The observed state and description for each checked row are in `../in/raw/nixos/units.txt` or `../in/raw/nixos/user-list-units.txt`. Fragment and drop-in paths are corroborated by `../in/raw/nixos/unit-paths.txt`, `../in/raw/nixos/user-unit-paths.txt`, and `../in/raw/nixos/unit-realpaths.tsv`.

## Documentation supporting unit semantics

Short exact excerpts, each from the linked primary documentation:

- [Service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html): “encodes information about a process controlled and supervised by systemd.”
- [Socket](https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html): “Socket units may be used to implement on-demand starting of services, as well as parallelized starting of services.”
- [Mount](https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html): “encodes information about a file system mount point controlled and supervised by systemd.” Runtime mounts are also monitored and listed as mount units.
- [Target](https://www.freedesktop.org/software/systemd/man/latest/systemd.target.html): “Target units are used to group units and to set synchronization points for ordering dependencies with other unit files.”
- [Slice](https://www.freedesktop.org/software/systemd/man/latest/systemd.slice.html): “A slice unit is a concept for hierarchically managing resources of a group of processes.”
- [Timer](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html): “By default, a service by the same name as the timer (except for the suffix) is activated.”
- [Path](https://www.freedesktop.org/software/systemd/man/latest/systemd.path.html): “For each path file, a matching unit file must exist, describing the unit to activate when the path changes.”
- [Scope](https://www.freedesktop.org/software/systemd/man/latest/systemd.scope.html): “Scope units manage a set of system processes.” They manage externally created processes and resource organization.
- [Device](https://www.freedesktop.org/software/systemd/man/latest/systemd.device.html): “This may be used to define dependencies between devices and other units.” These units are dynamically generated; mounts and sockets acquire dependencies on relevant devices.
- [Unit listing](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html): “List units that systemd currently has in memory.” Such references need not be installed definitions; the LOAD column distinguishes loaded and not-found.

## Custom definitions checked separately

- `nixos-afcf4a91ee`: [user configuration source](https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/config/users-groups.nix), exact identifiers `systemd.services.linger-users`, `disable-linger`, `enable-linger`. The service changes persistent user-manager execution. MUST under rule U.
- `nixos-189b4753ff`: [network configuration source](https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/tasks/network-interfaces.nix), “Run any user-specified commands.” The source links `network-local-commands` to network initialization and DNS configuration. MUST under rule U.
- `nixos-9f30203d50`: [power management source](https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/config/power-management.nix), “Service executed after boot, and stopped during shutdown”. This is the boot/shutdown command-hook service. MUST under rule U; no claim that particular optional power commands are configured.

## Group rows decided individually

The members field says 1 for these inventory group rows, but the evidence explicitly enumerates multiple names. Decisions below apply to every named member, not merely one sample.

- `nixos-a3f2270221`: all listed device units expose kernel devices as dependency/activation units. MUST: device-dependent activation is behavior. This decision concerns the logical units, not a requirement to change hardware.
- `nixos-88335c6c87`: same mechanism for every listed user-visible device unit. MUST: device-dependent activation is behavior.
- `nixos-18fb2985ed`: root, store, key and runtime-directory mounts. All MUST because removing mounts removes the corresponding filesystem access capability.
- `nixos-565df89b5f`: every listed root, shared kernel-interface, store, credential, key, runtime and wrapper mount supplies filesystem access. All MUST.
- `nixos-0ff15b2741`: both listed scopes manage existing system or session processes. All MUST for lifecycle/resource-management behavior.
- `nixos-3bc8c8458c`: the initial-process scope manages an existing process group. MUST for lifecycle/resource-management behavior.
- `nixos-253d752b01`: all four slices group service instances or user processes for resource management. All MUST.
- `nixos-b855166ba5`: root slice provides the resource hierarchy. MUST.
- `nixos-eb57ff0e5c`: local SSH socket is loaded, active and listening according to the raw listing. MUST because removal removes that connection/activation path.
- `nixos-9994d7ebc4`: every member is explicitly not-found and inactive in the raw listing, with no loaded definition. UNKNOWN under S3-2: the inventory contains retained unit references, and absence of a definition does not establish their operational dependency effects. Neither stored unit-path metadata nor public documentation establishes which dependency relationships retain these particular references.
- `nixos-97fdaec6aa`: the sole block-device target reference is not-found and inactive. UNKNOWN under S3-2: its reference relationships and effects are not recorded. The missing definition alone cannot establish that the observed in-memory object does nothing.

These two decisions were corrected after review of the object boundary. [Unit listing documentation](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) expressly includes references in the in-memory listing; its definition of not-found establishes only that the unit file does not exist. [Dependency documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html) distinguishes weak Wants dependencies from stronger Requires dependencies: “this unit will not be started” can follow failure of an ordered requirement. The raw inventories omit those dependency relationships. The uncertainty is factual, not a proposed change to the hypothesis.

## Verification

`part-3.units.build.py` preserves existing output rows and appends each missing row with a flush. It verifies exactly 150 distinct input IDs equal exactly 150 distinct output IDs and checks the decision vocabulary. Results: MUST 148, NOT 0, HOLE 0, UNKNOWN 2, MIXED 0.

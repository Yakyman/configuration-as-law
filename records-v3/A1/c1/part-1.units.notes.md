# c1 part 1: unit rows

Scope: 318 rows of kinds system-unit, user-unit, system-units, and user-units. Only the supplied input, its unit inventory files, the numbered text, and the documentation below were used. No removal or execution experiments were performed. No earlier classification was consulted.

## Sentences used, quoted exactly

- S2.2-1: Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- S2.2-2: The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- S2.2-7: settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- S2.2-13: A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- S2.2-15: accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- S3-1: **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- S3-2: If what the object does remains unknown, the case yields ?.

## Documentation and exact excerpts

- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html — “A unit file is a plain text ini-style file”; masking: “making it impossible to start it even manually.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html — “encodes information about a process controlled and supervised by systemd.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html — “For each socket unit, a matching service unit must exist, describing the service to start on incoming traffic on the socket”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.target.html — “Target units are used to group units and to set synchronization points for ordering dependencies with other unit files.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html — “By default, a service by the same name as the timer (except for the suffix) is activated.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.path.html — “For each path file, a matching unit file must exist, describing the unit to activate when the path changes.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html — “encodes information about a file system mount point controlled and supervised by systemd.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.slice.html — “This management is performed by creating a node in the Linux Control Group (cgroup) tree.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.device.html — “This may be used to define dependencies between devices and other units.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.scope.html — “Scope units manage a set of system processes.”
- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html — “List units that systemd currently has in memory.”

## Homogeneous rule U: loaded stored unit controls

Applied by `part-1.units.build.py` to 306 individual rows: the inventory shows a loaded unit, a nonempty fragment path, and its type. The unit is a control definition for independent process invocation, communication, activation ordering, filesystem mounting, or process-resource management. Removing the definition removes that managed capability or changes its orchestration: MUST under S2.2-1 and S2.2-2. Current inactivity does not establish absence of a capability. A timer that starts a cache refresh is a schedule, not the cache; a service that writes logs is a service definition, not historical logs.

The object classified is the unit control, not its executable payload. S2.2-13 does not make a value file executable code. S2.2-7 does not exempt these controls: their effects reach independent services, kernel filesystem access, IPC endpoints, or kernel process groups. Being parsed by one manager is different from being in force only inside one program. No precedence between conflicting sentences is assumed.

The output function identifies the control's common role. Its individual service purpose remains identified by the input evidence; knowing every executable argument is unnecessary to establish that a loaded service unit controls invocation of another process.

Ten rows checked by hand against their evidence and the corresponding type documentation:

| ID | Evidence inspected and why rule fits |
|---|---|
| coreos-ba67dc14d4 | Loaded running network manager service with a stored fragment; controls a separate network-management process. |
| coreos-956040fa23 | Loaded running security audit service; logging producer is a process control, not a historical log. |
| coreos-e38652edff | Loaded exited linker-cache rebuild service; invocation definition is distinct from its cache output. |
| coreos-c5a27a2455 | Loaded listening container-engine socket; exposes an IPC endpoint and service activation. |
| coreos-77462850bc | Loaded basic target with a stored fragment; groups and orders other unit activation. |
| coreos-f5fee7c08e | Loaded waiting weekly filesystem-discard timer; schedules a service invocation. |
| coreos-d023432e09 | Loaded waiting password-request path watch; triggers another unit upon filesystem conditions. |
| coreos-16081f0750 | Loaded mounted huge-pages filesystem unit; controls a kernel filesystem available to processes. |
| coreos-0325994aec | Loaded waiting executable-format automount; triggers filesystem mounting on access. |
| coreos-eb1055f947 | Loaded active application slice; creates a resource hierarchy for independent application processes. |

## Individually assessed exceptions and group rows

These 12 rows were individually assessed, rather than inferred from the stored-unit rule. Member lists were read from the input; runtime state was checked in `../in/raw/coreos/units.txt` or `../in/raw/coreos/user-list-units.txt`. Although each grouped row's numeric members field says 1, its evidence explicitly lists multiple members. The whole listed group is assessed.

- coreos-ca040c10df: MUST. `../in/raw/coreos/unit-realpaths.tsv` resolves the service fragment to `/dev/null`. This is an operative prohibition on starting the service. S2.2-1 covers restrictions on capabilities; S2.2-2's sufficient removal condition does not say that gaining a capability is exempt.
- coreos-a3f2270221: MUST for every listed device unit. These are live device-availability objects used in unit dependencies, including block-backed mounts. The object is its dependency/activation representation, not a claim that hardware must be reinstalled.
- coreos-88335c6c87: MUST for every listed device unit exposed to the user manager, for the same dependency/activation role. The duplicated device names do not denote programs confined inside an interface.
- coreos-18fb2985ed: MUST for every listed system mount. Root, boot, configuration, runtime-user, system-root and variable-data mounts provide filesystem access. Generated and observed mounts are not treated as content merely because a stored fragment is absent.
- coreos-565df89b5f: MUST for every listed mount visible to the user manager. The list includes kernel API mounts, credentials, runtime-user, root and data mounts. Their mount availability enables access by processes.
- coreos-9994d7ebc4: NOT for every listed absent unit. The raw inventory confirms not-found and inactive for each. The row is a list of unresolved names, not an installed implementation of the named facilities; there is no corresponding functionality to remove.
- coreos-97fdaec6aa: NOT for both listed absent block-device targets. The raw user inventory confirms not-found and inactive for both. These are unresolved references, not implemented target controls.
- coreos-0ff15b2741: MUST for init.scope and session-4.scope. Both are loaded, active and running; their scope controls manage existing independent processes rather than merely recording past activity.
- coreos-3bc8c8458c: MUST for init.scope. The sole listed scope is loaded, active and running and provides process grouping/resource management.
- coreos-253d752b01: MUST for all listed slices. Root, system, per-template, and user slices constitute the process-resource hierarchy. Their lifecycle/resource function extends to processes outside the manager.
- coreos-b855166ba5: MUST for the root slice. It is the root of the process-resource hierarchy, not an isolated user-interface preference.
- coreos-eb57ff0e5c: MUST for both sshd-unix-local.socket and sshd-vsock.socket. Both are loaded and listening in the raw inventory, with explicit local and virtual-machine socket descriptions. Both provide login-service endpoints and activation.

No group received differing member decisions. No rule treats generated state as automatically exempt; state handling is outside the definition under Section 2.5 and is not counted as a textual hole.

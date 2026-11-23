# Unit classifications, part 2

Only the assigned unit kinds in `../in/part-2.tsv` were considered. Inventory class labels were ignored. Sources inspected: `../in/raw/debian/units.txt`, `unit-paths.txt`, `user-list-units.txt`, `user-unit-paths.txt`, and `user-manager-state.txt`. No object was removed.

## Sentences used

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

## Documentation

- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html : “A unit file is a plain text ini-style file that encodes information about a service”. Unit files also describe activation, dependency, mounting, and resource management objects; they are not themselves the processes they configure.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.target.html : “Target units are used to group units and to set synchronization points for ordering dependencies with other unit files.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.device.html : “Many unit types automatically acquire dependencies on device units of devices they require.” Device units dynamically expose kernel device availability; mount and socket dependencies can use them.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html : “Mount points created at runtime (independently of unit files or /etc/fstab) will be monitored by systemd”. These units represent mounts, including mounts created outside the manager.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.scope.html : “Scope units manage a set of system processes.” They group externally created processes for resource management.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.slice.html : “A slice unit is a concept for hierarchically managing resources of a group of processes.” The hierarchy is implemented through kernel control groups, including the root slice.
- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html : “List units that systemd currently has in memory.” Listing includes referenced units; a displayed name does not establish an installed unit file.

## Rule U: configured functional units

Applied by script to the 155 singular system-unit/user-unit rows. Every row reports a loaded unit, a fragment, and its concrete service, activation, synchronization, filesystem, or resource-management function. Removing such a unit removes the corresponding managed action or activation/ordering capability: MUST by S2.2-1 and S2.2-2. S2.2-13 makes value-based unit configuration settings, but S2.2-7 only exempts settings in force *only inside* one program. Starting other processes, ordering their execution, mounting kernel interfaces, and managing their resources have effects outside the manager. Unit configuration is not an internal theme or preference. Neither inactive status nor completed one-shot status changes the available unit function. Logging and cache-maintenance services are actions, not the logs and caches they produce.

Ten manually checked rows, checked against their input descriptions and raw unit listing:

1. debian-29a7d582ee — apparmor.service loads security profiles; removal loses managed profile loading, an external security effect.
2. debian-4a8bc234ee — apt-daily-upgrade.service performs package upgrade/cleanup; inactive status does not remove the configured action.
3. debian-aa6c43f73c — apt-daily-upgrade.timer schedules that external package-maintenance action.
4. debian-77462850bc — basic.target groups/orders basic-system activation; the target mechanism changes process activation dependencies.
5. debian-b2eac0adbc — dbus.service runs the system message bus used between processes.
6. debian-06be1b0d47 — dbus.socket provides the system bus socket activation endpoint.
7. debian-16081f0750 — dev-hugepages.mount exposes a kernel filesystem to processes.
8. debian-46b677ba51 — systemd-ask-password-console.path watches requests to activate an external password-response service.
9. debian-e92ded7963 — user.slice organizes resources for user/session processes through control groups.
10. debian-6d902f1685 — user basic.target orders and groups user-unit activation, not a preference confined to an application interface.

## Individually assessed grouped rows

Despite `members=1` in the input column, the evidence enumerates multiple units. Decisions below cover all enumerated members, not an invented single file.

- debian-a3f2270221 and debian-88335c6c87: every enumerated device unit dynamically exposes a device and supplies its availability to unit dependencies. MUST: removing that availability/dependency object removes its device-dependent activation capability. No assertion that these are stored configuration files or firmware settings is needed.
- debian-18fb2985ed: all members are mounted filesystems: root, EFI, service credential mounts, and user runtime storage. MUST: removing the represented mount removes its filesystem access. The object classified is the mount unit, not a text copy of inventory output.
- debian-565df89b5f: all members are observed mounts, additionally including hugepages, message queues, binary-format registration, FUSE control, configuration, debugging, and tracing filesystems. MUST for the represented mounts and their access to kernel interfaces, even though the user manager discovers them from mountinfo.
- debian-9994d7ebc4: all enumerated units are not-found/inactive/dead. NOT: these are references to unavailable unit definitions, not installed services or mount configurations. Removing an unavailable reference removes no existing unit capability. This does not classify the hypothetical installed programs bearing those names.
- debian-97fdaec6aa: the sole block-device target is not-found/inactive/dead in the user manager. NOT on the same individually verified grounds: no configured target capability exists to remove.
- debian-0ff15b2741: init.scope and session-4.scope manage actual manager/session process groups. MUST: these are active process-management objects, not log records about the processes.
- debian-3bc8c8458c: init.scope manages the active user manager's process group. MUST for the same process-management function, individually checked in the user listing.
- debian-253d752b01: all named slices form the active resource hierarchy for system, template-instance, and user process groups. MUST because the hierarchy manages kernel resources for those processes.
- debian-b855166ba5: the root user slice supplies the root of that resource hierarchy. MUST for its actual process-resource management function.

The grouped assessments are individual decisions supported by the listed members and documentation, not additional bulk rules.

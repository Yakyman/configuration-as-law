# Service and timer classification

Scope: 459 rows of kinds L1:user-service, L1:user-timer, L1:user-unit-file, L1:service, L1:timer and L1:unit-file. Only the assigned input, its raw inventory, COMMON.md, TEXT.md, SENTENCES.md and primary public documentation were consulted. No removal was performed. Inventory conclusions were ignored.

## Exact decisive text

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”
- S3-2: “If what the object does remains unknown, the case yields ?.”

## Primary documentation

- https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html: “A unit configuration file whose name ends in ".service" encodes information about a process controlled and supervised by systemd.” Service units configure supervision of processes; they are not themselves executable programs.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html: “A unit configuration file whose name ends in ".timer" encodes information about a timer controlled and supervised by systemd, for timer-based activation.” The matching unit, normally a service, is activated when the timer elapses.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html: “Units can be aliased (have an alternative name), by creating a symlink from the new name to the existing name”. Such names supply activation entry points. Templates provide definitions for instances.
- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html: “List units that systemd currently has in memory.” The list can contain references lacking definitions; list-unit-files instead lists installed definitions. Inactive is an activation state, not evidence that an installed definition is absent.

## Homogeneous rule R1

Apply MUST to an installed service/timer definition, loaded service, or timer activation entry. Each configures, names or schedules managed activation of a separate service process. Removal removes that managed activation capability, named entry point or schedule (S2.2-1, S2.2-2). Inactive, disabled and template entries still supply capabilities; the task asks whether objects must be recorded, not whether currently active.

These files are settings under S2.2-13, not code merely because an ExecStart value names code. S2.2-7 requires settings to be in force **only inside** one program. Supervision, process activation and the schedule of a separately executing service extend outside the manager. Therefore R1 does not invoke that exemption. Reading values in one parser alone does not establish that their force is only inside it. No precedence between sentences has been invented. A logging or cache-building service is neither its logs nor its cache.

The rule covers service definitions, aliases and timers as one homogeneous kind: controls of external service activation. The script varies the factual description for the documented mechanism without changing the decision rule. The raw inventory scripts confirm list-units, list-timers and list-unit-files as the source commands.

Ten hand checks against the actual cited raw lines and documented unit semantics:

| ID | Checked property |
| --- | --- |
| flatcar-36902b7d91efb89edf0757e2 | Loaded inactive user message-bus service; managed process remains available. |
| flatcar-905e902eefa63160a0ddd48c | Active exited user file-creation service; service activation has filesystem effects. |
| flatcar-2db3435e61f3b7410b61dfcc | User import-service alias; alternative service activation name. |
| flatcar-194640cbe88827831ab4807e | Disabled user p11-kit service definition; disabled is not absence. |
| flatcar-e2392fe58e7be6849e1a44d1 | Static password-request service template; defines parameterized activation. |
| flatcar-19a0e1d4f8287374c6f606d3 | Disabled user cleanup timer definition; supplies scheduling capability. |
| flatcar-c1b32845646e0963306d2ee5 | Running container runtime service; supervised external process. |
| flatcar-ed19a98eeeca14c92573cd16 | Exited linker-cache rebuild service; service is distinct from cache content. |
| flatcar-081049d311fe2c1986619bff | System virtual-terminal service alias template; named activation capability. |
| flatcar-35f9e9b83152b2aff0bca0de | Disabled filesystem-scrubbing timer definition; scheduling rather than file content. |

## Individual unresolved references

The following five service rows each report `not-found inactive dead`. Unlike installed definitions, these are unresolved manager references. No definition or dependency graph is supplied. The generic purpose of a similarly named upstream unit cannot establish what this absent local definition or live reference contributes. Public manager documentation establishes the reference status, but not the individual dependency effects. Each is UNKNOWN under S3-2, not a claim that absent services run or that absence is a textual hole.

- flatcar-f79b464b166dee8a6edf7235: missing plymouth-quit-wait definition; raw/flatcar/raw/073-service.out:46.
- flatcar-db3479ac6a4a75602d47f30f: missing plymouth-start definition; raw/flatcar/raw/073-service.out:47.
- flatcar-4ebcb6edd91450f4eb5aa735: missing syslog definition; raw/flatcar/raw/073-service.out:57.
- flatcar-88464f8a7422c36c077c2907: missing systemd-quotacheck definition; raw/flatcar/raw/073-service.out:93.
- flatcar-ee9d2efa3352fec63a32b097: missing systemd-tpm2-setup-early definition; raw/flatcar/raw/073-service.out:111.

## Validation

The append-only build script preserves prior completed rows and flushes each new row. It verifies exact assigned ID set and count, unique IDs, allowed decisions and field word limits. Result: 454 MUST, 5 UNKNOWN; total 459. No group rows occur in this subset; the members field contains one inventory line per object.

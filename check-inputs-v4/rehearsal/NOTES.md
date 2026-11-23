# Rehearsal preparation record

2026-11-23 UTC. This task retains only exit statuses, elapsed durations, byte
sizes and counts. The disposable output directories are automatically deleted
before each clone is destroyed. No object rows or guest command text are read
by the operator. Rehearsal results are not hypothesis outcomes.

The initial reducer used Python's default CSV field limit. The first Alma
reduction exited unsuccessfully without counts; its output was deleted unread.
The limit was raised to 256 MiB, matching the collector's largest bounded
query. The precise initial failure is unknown; no traceback was read.

Dynamic query labels can contain package or account identifiers. The reducer
records only anonymized query categories. Initial Void and Alma status files
were sanitized automatically before any collector query rows were read. Only
fixed action labels had been read. The collector now anonymizes labels in
rehearsal mode before writing any coverage output. This does not alter queries.

Talos expectation was expressed in the task's acceptance conditions; no separate
system-specific expectation file was written before its first launch. This is
a preparation-record lapse. All queries and transports returned zero; the
existing documented reason/integrity limitations remain material blockers.

Mint round 1 used SSH without exporting the graphical-session variables required
by its source script. Prerequisites returned 1, and dependent actions failed.
Source inspection identifies the missing transport environment as a defect;
no guest error text was read. Round 2 exports DISPLAY=:0, the user's default
Xauthority, runtime directory and session-bus address. A virtual HDA output
is added to the Mint VM using a null host audio backend, providing virtual
sound hardware without physical GPU/audio access. This changes instrument
access, not any of the nine listed activities. Expected before round 2:
prerequisites and the session-dependent actions can now execute unattended;
all actions, collector and transport must still be tested on a fresh clone.

Sources: https://www.x.org/releases/current/doc/man/man7/X.7.xhtml ;
https://dbus.freedesktop.org/doc/dbus-specification.html#transports-unix-domain-sockets ;
https://www.qemu.org/docs/master/system/qemu-manpage.html (`-audiodev none`) ;
https://github.com/qemu/qemu/blob/master/docs/qdev-device-use.txt (HDA devices).

The prescribed existing source-build action deadlines are retained for Gentoo.
No binary-package substitution or additional observation is authorized.

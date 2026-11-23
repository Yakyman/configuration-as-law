# Mint rehearsal record

2026-11-23 UTC. Round 2 began at 07:33:11 UTC on a fresh disposable
clone. Its twenty consecutive transport calls returned zero.

A separate attempt to read only the action-status table through `lab.sh run`
while the action script held the per-machine run lock reached its 30-second
limit (exit 124); no guest content was returned. This diagnostic was outside
the consecutive transport sequence. The transport source (`lab.sh`, run
branch) and `LAB.md` document that the limit includes lock acquisition. No
further concurrent transport query was attempted.

Round 2 completed and its clone was destroyed successfully. Prerequisites,
Flatpak game, Windows program, user settings and autostart returned zero.
Steam client returned 1 after 13 seconds, anonymous download returned 8 after
32 seconds, launcher returned 1 after 6 seconds, and overlay returned 127.
The collector returned 1 after 0.064 seconds; no usable inventory counts were
produced. Only the status/count tables were read.

Before round 3, the overlay's wrapper check changes from `mangohud --version`
to `mangohud /usr/bin/true`. The upstream v0.6.9 wrapper does not implement a
version option and ends with `exec env MANGOHUD=1 LD_PRELOAD="${LD_PRELOAD}" "$@"`:
https://github.com/flightlessmango/MangoHud/blob/v0.6.9/bin/mangohud.in .
Thus the earlier check could attempt to execute an option as a program. The
configuration and chosen activity remain unchanged; this is a version-compatible
instrument check, not a replacement action. Expected: the overlay action
returns zero with the installed distribution wrapper.

GUI checks now expose distinct numeric exit statuses without exposing content:
81/85 for Steam/Lutris premature exit, 82/86 for their completion deadlines,
83 for an unsupported accessibility interface, and 84 for an uncaught GLib
accessibility error. Existing completion checks and deadlines are unchanged.
Expected: any repeated GUI failure identifies one of these instrument branches;
no cause is inferred solely from the prior generic status 1. The anonymous
download's status 8 has no verified cause; its documented commands are retained.

The collection maintainer identified round 2's pre-collection provenance-guard
failure in host-authored code: `qemu-img info` lacked `-U` when inspecting a
live, locked disposable overlay. The deployed guard now uses `-U`. No guest
collection content was used for this diagnosis. Round 3 is expected to pass
this guard and run the normal collector; its measured result remains required.

Before round 4, the two GUI drivers gain isolated, automatically cleaned-up
Xvfb displays and D-Bus sessions: `xvfb-run -a dbus-run-session -- python3`.
Prerequisites add `xvfb`, `xauth` and `dbus-daemon`; existing action limits
remain in force. This provides explicit graphical transport for the same
Steam first launch and Lutris installation, without replacing their activities
or weakening their completion checks. It does not establish that missing
session access caused the earlier failures.

Sources: https://manpages.debian.org/bookworm/xvfb/xvfb-run.1.en.html says the
wrapper runs commands “within a virtual X server environment” and cleans up
the server and temporary authorization file on command exit.
https://dbus.freedesktop.org/doc/dbus-run-session.1.html says the daemon runs
“for as long as the program does, after which it will terminate.” Expected:
the existing GUI actions can reach their real interfaces independently of
whether the copied desktop has a logged-in graphical session. A zero status
still requires the original application-specific completion tests.

Round 3 returned zero for six actions, including the repaired overlay. Steam
returned 81 (its initial process exited before the existing completion test),
Lutris returned 85 (the corresponding launcher-process branch), and SteamCMD
returned 1. For round 4, the final expected-download-file test receives distinct
status 87; the SteamCMD command's own unsuccessful status remains unchanged.
No download command or application is replaced, and no guest error text is read.

Round 3 collector returned 2 after 253.015 seconds. Its filesystem query
returned 75 after 71.082 seconds, with 500000 entry rows and one error row.
The 21164 second-level rows are partial: `collector:reduction-complete` and
`collector:filesystem-complete` are both zero. Of 2302 package rows, 2201
have known reasons and 2199 have at least one known integrity result; none
has every emitted file-integrity result known. These partial counts do not
establish readiness. Clone destruction returned zero.

Round 4 starts on a new clone with an explicit laboratory root environment.
It is the final allowed round for this system.

Before round 4 collection, the shared traversal bound increases from 500000
to 1000000 entries, and its query-output cap increases to 512 MiB. The basis
is round 3's exact 500000-entry count and unsuccessful filesystem status.
The 600-second scan limit and 30-minute collector limit remain in force.
Expected: the previous entry ceiling no longer truncates the same traversal;
completion and all coverage thresholds still require measured confirmation.
The one filesystem error row's content was not read, so its cause remains
unknown rather than being equated with the ceiling.

Final round 4 actions finished in 350.301 seconds: seven of nine returned
zero, including Lutris with its new isolated graphical transport. Steam
still returned 81 after 8 seconds: its launched process exited before the
unchanged completion condition was met. The cause remains unknown. The
anonymous-download action returned 87 after 112 seconds: SteamCMD itself
returned zero, but its expected `steamapps/common/U3DS/ServerHelper.sh` check
failed. Neither the download's actual location nor its content was inspected.
No claim of network failure or absence of all downloaded files follows.
The fourth-round limit is exhausted; no fifth action rehearsal is run.

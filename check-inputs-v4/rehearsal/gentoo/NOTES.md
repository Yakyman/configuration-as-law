# Gentoo original rehearsal notes

Historical first-pass record, superseded by `FX-LOG.md`, `FIX-FX.md`, and the retained numeric tables. The old active run described below was interrupted and its clone destroyed during FX-C1-REH-1. The later diagnostics permission and action repairs are disclosed in `DISCLOSURES-FX.md`.

2026-11-23 UTC. Round 1 uses the existing action limits: 10,800 seconds per
package action, 21,600 seconds for the browser action, and 172,800 seconds
for the whole batch. The original run remains active. Source builds are
not replaced by binary packages.

The prescribed twenty consecutive transport calls returned zero. A separate
numeric-progress request made through the laboratory runner while the action
batch held its exclusive run lock returned 124 after sixty seconds. It did
not execute a guest command. Subsequent progress reductions use separate SSH,
retain only fixed action labels with numeric status/duration fields, and do
not inspect command output.

The first completed action returned zero in eight seconds; application_package
returned one in one second. The latter's precise cause is unknown: its output
was not read. The official package entry confirms that the script's
sys-apps/flatpak atom exists:
https://packages.gentoo.org/packages/sys-apps/flatpak . No source correction
is justified by the currently retained numeric evidence.

No guest content has been seen. These are preparation results, not observations
or hypothesis outcomes.

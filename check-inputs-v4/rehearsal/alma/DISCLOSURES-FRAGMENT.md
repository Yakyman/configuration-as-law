# Alma FX-C1-REH-1 disclosures

2026-11-23 UTC. Fresh repair rounds use round identifiers 11–14 (FX1–FX4),
distinct from historical rehearsal identifiers. Actions retain the originally
selected programs; no Alma action is replaced.

No `objects.tsv`, raw query stdout, package-file inventory or member list was
read. Machine content is reduced mechanically to allowed numerical counts and
then deleted. Diagnostic files read are listed below as the work proceeds.
The original diagnostic files remain under `diagnostics/`.

- `diagnostics/fx1/coverage-live.tsv`: the collector was progressing through successful bounded package-digest batches; this exposed query counts/status/timing only. Successful action stderr remains retained without inspection.
- `diagnostics/fx1/coverage.tsv`: filesystem returned 75; two Flatpak user queries and three user-service queries returned 1; four OpenRC/Docker queries returned 127. Other queries returned zero.
- `diagnostics/fx1/collector.stderr`: empty; no machine facts exposed.
- `diagnostics/fx1/0004-filesystem.err`: empty; traversal failure cause remains unavailable from stderr.
- `diagnostics/fx1/0036-packages-flatpak-user-app.err`: permission denied opening the root account's local Flatpak repository; this identifies the failed scope, not installed applications.
- `diagnostics/fx1/0037-packages-flatpak-user-runtime.err`: the same root-scope repository permission denial.
- `diagnostics/fx1/0431-openrc-service.err`: rc-status was unavailable on this machine.
- `diagnostics/fx1/0432-openrc-runlevel.err`: rc-update was unavailable on this machine.
- `diagnostics/fx1/0441-docker-container.err`: docker was unavailable on this machine.
- `diagnostics/fx1/0442-docker-image.err`: docker was unavailable on this machine.
- `diagnostics/fx1/0446-user-service.err`: the queried user scope lacked a configured session bus/runtime directory.
- `diagnostics/fx1/0447-user-timer.err`: the queried user scope lacked a configured session bus/runtime directory.
- `diagnostics/fx1/0448-user-unit-file.err`: the queried user scope lacked a configured session bus/runtime directory.

Round 11 numerical reductions exposed reason-category counts: 261 RPM packages
carry a group reason and one carries unknown; 17 Python and 41 npm package
objects have unknown reason. These are machine facts limited to counts, without
package identities. They explain why 1241/1561 known reasons fails the readiness
threshold even though 120520/121931 packaged-file integrity facts are known.
- `diagnostics/fx2/filesystem-live.stderr`: filesystem traversal failed on `/run/user/1000/doc` with permission denied. The diagnostic exposes this runtime portal path and access restriction, without enumerating its contents.
- `diagnostics/fx3/coverage.tsv`: filesystem and selected-group provenance queries returned zero. Two Flatpak user queries and three user-service queries returned 1; four OpenRC/Docker queries returned 127. No raw query stdout was read.

FX3 finished with collector status 0, nine actions status 0, twenty transport
calls status 0, whole-run duration 202.641 seconds and clone destruction status
0. Its package/L2 numerical counters were not retained during the concurrent
migration from file-based reduction to in-memory collector reduction. The raw
artifacts had already been deleted unread, so those counters are unavailable;
no earlier round's counts are represented as FX3 counts. The next fresh round
will exercise the synchronized counter path.
- `diagnostics/fx4/coverage.tsv`: filesystem and selected-group queries returned zero; the final run retained nine nonzero queries listed below. Query-status/count/timing information only was exposed.
- `diagnostics/fx4/0040-packages-flatpak-user-app.err`: permission denied opening a root-home Flatpak repository in the queried scope; application contents were not listed.
- `diagnostics/fx4/0041-packages-flatpak-user-runtime.err`: the same repository permission denial for runtimes.
- `diagnostics/fx4/0199-openrc-service.err`: rc-status unavailable.
- `diagnostics/fx4/0200-openrc-runlevel.err`: rc-update unavailable.
- `diagnostics/fx4/0209-docker-container.err`: docker unavailable.
- `diagnostics/fx4/0210-docker-image.err`: docker unavailable.
- `diagnostics/fx4/0214-user-service.err`: user session bus/runtime environment unavailable for that query.
- `diagnostics/fx4/0215-user-timer.err`: user session bus/runtime environment unavailable for that query.
- `diagnostics/fx4/0216-user-unit-file.err`: user session bus/runtime environment unavailable for that query.

The final numerical reduction shows 1238/1561 known package reasons and
120520/121931 known packaged-file integrity facts, 1692 L2 rows, collector
status 0 in 76.862 seconds, whole run 180.137 seconds, all nine actions zero
and twenty transports zero. Native GROUP accounts for 261 unknown reasons;
one other RPM, 41 npm and 20 Python package reasons are unknown. No package
identity was exposed by these counts. All four clones and transient raw
folders were removed (`CLEANUP.tsv`).

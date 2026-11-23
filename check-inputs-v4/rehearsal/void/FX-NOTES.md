# Void instrument continuation

2026-11-23 08:15 UTC. This continuation permits four new fresh-clone rounds,
identified separately from the preceding four rounds. No collected object,
query stdout or member-list content is read.

Before the first continued round, reviewed the current action script, collector
XBPS adapter and the primary sources:
- https://raw.githubusercontent.com/void-linux/void-packages/master/srcpkgs/nodejs/template
  describes the Node.js package and its shared-library build inputs.
- https://docs.voidlinux.org/config/network/networkmanager.html requires disabling
  competing network managers, enabling D-Bus, then enabling NetworkManager.
- https://raw.githubusercontent.com/void-linux/xbps/master/bin/xbps-create/main.c
  records `file`, `target`, `sha256` and `size` by entry type; directories and
  symlinks do not carry regular-file content hashes.

Expected before continued round 1: the corrected host launch and separate
standard-error capture reveal any remaining action/collector startup defects.
The unchanged language/network actions may still fail; diagnostic messages will
be used to repair those precise failures. Collector acceptance requires positive
second-level count, more than 90 percent known package reasons and packaged-file
integrity, within 1800 seconds, with all required queries successful or named
limitations. All twenty transport calls must return zero. Outputs are reduced
and deleted unread; permitted diagnostics are retained in `diagnostics/`.

Before launch, the XBPS adapter was repaired to compare an installed symlink's
literal target with the `target` field in its package manifest. A different
captured target or file type is changed; equal target is unchanged; absent
capture remains unknown. No link is followed. Source: saved
`sources/xbps-manifest-excerpt.c`, `process_xentry`, which writes the manifest's `target`.
This makes a previously unused installation fact available without guessing.

At 08:16 UTC, continued round 1 started as a durable host service. The first
service-launch command was rejected before starting any process because its
working-directory property did not expand the path specifier. Supplying the
shell-expanded laboratory path corrected that host-only launch error.

Continued round 1 completed all actions in 175.780 seconds: eight of nine
returned zero. The language program failed before npm could run; permitted
stderr identifies an incompatible installed C++ runtime. The network action
returned zero without a new repair; its preceding failure is not retrospectively
explained. The exact diagnostic disclosures are in `FX-DISCLOSURES.md`.

Repair before continued round 2: name `libstdc++` together with `nodejs` in
`xbps-install -Sy`. The manual says named installed packages are updated to the
matching repository version; the upstream GCC template installs libstdc++.so
in the `libstdc++` subpackage. Sources: https://man.voidlinux.org/xbps-install.1
and https://raw.githubusercontent.com/void-linux/void-packages/master/srcpkgs/gcc/template .
This repairs the runtime dependency of the same npm/cowsay action; it does not
replace the action or install a collector dependency.

Continued round 1 collector passed: status 0, 712 second-level rows,
485/501 known package reasons, 29979/30258 known packaged-file integrity facts,
complete filesystem traversal and complete reduction. All nonzero queries were
127 for unavailable tool interfaces, the documented COLLECT.md limitation.
Whole run 264.623 seconds; clone destruction returned zero.

Expected before continued round 2: explicitly updating the C++ runtime removes
the observed ABI loader failure and permits the same npm/cowsay action. All nine
actions, twenty transport calls and collector should then pass; known reason
and file integrity must each remain over 90 percent. A new clone is required;
no action is retried on the prior destroyed clone.

Continued round 2: eight of nine actions returned zero; the language program
now failed on undefined SQLite session symbol `sqlite3session_attach`. Collector
status 0 in 32.427 seconds; second level 712 rows; reasons 485/501; packaged-file
integrity 29981/30260; whole run 231.866 seconds; twenty transport calls and clone
destruction zero. The C++ dependency repair exposed the next startup dependency.

Before continued round 3, the Node package source shows `--shared-sqlite` and
the current SQLite recipe enables `--enable-session`. Source:
https://raw.githubusercontent.com/void-linux/void-packages/master/srcpkgs/sqlite/template .
Add `sqlite` to the explicitly updated runtime packages in the same language
installation action. Expected: Node and npm start with both diagnosed runtime
requirements met, all nine actions pass, and collector/transport thresholds
remain satisfied on another fresh clone. No replacement of the action is made.

Continued round 3: eight of nine actions zero; XBPS rejected the language
runtime transaction because current liblastlog2 conflicts with the older
installed util-linux. Collector0 in 25.827 seconds; L2 712; reasons 336/352;
file integrity 27981/28259; whole 224.723 seconds; transport 20/20; destroy 0.

Before final continued round 4, the Void handbook recommends a system update
for old installed shared-library dependencies:
https://docs.voidlinux.org/xbps/troubleshooting/common-issues.html (`shlib errors`).
The xbps-install manual defines `-u` as updating installed packages to repository
versions. Run that documented update after the mandatory XBPS self-update and
before installing tree, so later actions use a consistent repository generation.
The same nine action programs remain selected. Expected: the consistent update
removes both runtime ABI failures and the rejected dependency transaction;
all actions and collector thresholds pass within 1800 seconds. This is the fourth
and final new fresh clone, regardless of result.

Before round 4, the lead also directs the same cowsay installation to use npm's
local-prefix form rather than global-prefix form. The executable moves from
`.local/bin/cowsay` to `.local/node_modules/.bin/cowsay`; project package-lock
records retain requested/dependency facts. Source: npm install and package-lock
reference already listed in `actions/ordinary.md` and `collector/PACKAGES.md`.
Expected: direct cowsay and dependency reasons can be read from manager records;
no installed package or file contents will be read by the operator.

Historical pre-review assessment, subsequently invalidated below: continued round 4 passed: nine actions 0; twenty transport calls 0;
collector 0 in 27.682 seconds; second-level 2068 rows; known reasons 530/546 (97.07%);
known packaged-file integrity 37652/37931 (99.26%); whole 365.953 seconds.
All nonzero queries were documented unavailable interfaces (127). Traversal and
reduction complete. Clone destruction 0; disposable clone and unread collection
folder both verified absent. All four continued rounds are exhausted; a fifth is not permitted.

Independent review later invalidated native-parent reason inheritance for
separate Python/npm package objects. The shared collector removed that logic.
The historical 530/546 reason count cannot certify readiness. Conservatively
subtracting all 188 known Python/npm reasons gives 342/546 (62.64%) using retained
counts only; exact corrected coverage is unknown without another run. Final
Void status: NOT READY, reason threshold uncertified, four rounds exhausted.
The original statuses and counts are preserved unmodified; other measured gates
remain passed. No raw collection output was read for this correction.

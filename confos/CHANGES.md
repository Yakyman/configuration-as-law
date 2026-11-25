# Changes

## 0.55 — development, 2026-11-25 UTC

- The superuser reads which file every process of the machine executes. Up to
  0.54 `sudo -n readlink /proc/PID/exe` printed nothing for a process of a recorded
  Flatpak application and for the radio supervisor of the system: the session
  policy allowed reading towards two of the labels of the machine only
  (evidence/queries-0.54-control.log). It now allows reading, not tracing, towards
  every label; the kernel still requires the same account or the superuser's
  capability. For a process in a sandbox the kernel prints the path in the
  application's own mount namespace (`/app/bin/mpv`); through the root of the
  process (`/proc/PID/root/app/bin/mpv`) it is the stored file of the recorded
  application, with the same checksum (evidence/queries-0.55.log).
- Not changed: after `timeout -s KILL 40 flatpak run io.mpv.Mpv --idle=yes
  --vo=null --ao=null` the application keeps running without its front process,
  as with the native tool; the superuser now reads its executable as well
  (the same log). The native option `--die-with-parent` was tried in the launch
  entry and did not end the application here; it is not part of this release.
- `flatpak list` answers with its native options `--app`, `--runtime`, `--all`,
  `-a`, `--system`, `--user`, `-d`, `--show-details` and `--columns=NAMES`, for the
  ordinary account and for root. Up to 0.54 only the plain form answered and
  `flatpak list --app --columns=application` was refused.
- For an account without recorded container images, root included,
  `podman images`, `podman image ls`, `podman ps`, `podman ps -a` and
  `podman ps --all` followed by `--format json` print `[]` with status 0, also
  between a recorded `podman pull` and its application. Up to 0.54 they ended
  with status 1. An account with recorded images has the plain forms as before.
- Gates: test-queries-055.sh starts the recorded application as the cases
  P4-S-135, P4-S-136 and P4-S-167 start it and makes every check of
  process-exe-probe.sh
  (evidence/queries-0.55.log); the recorder tests of Podman and Flatpak make the
  new queries (evidence/podman-recording-0.55.log,
  evidence/flatpak-recording-0.55.log); the probe of saved Basic libraries
  (evidence/basic-macros-0.55-u9.log), the game case
  (evidence/game-sequence-0.55.log), smoke, both updates and the 0.50 tools test.
- The source archive has 504 files.
- No declaration syntax change. Reader payloads identical to 0.54 (the component
  is repackaged with its version only). Pinned components unchanged.

## 0.54 — development, 2026-11-25 UTC

- Saved Basic macro libraries of the office suite are no longer executed. In
  0.46–0.53 a command such as `libreoffice -env:UserInstallation=file:///tmp/p
  --headless macro:///Standard.Module1.Main` ran a library that a person had saved
  in the home folder or in /tmp and started an external program from it
  (IMPOSSIBLE.md; on 0.52 every one of six such routes of the ordinary account,
  evidence/basic-macros-0.52-control.log).
- How: the suite executes compiled Basic in one function, SbiRuntime::Step(), which
  one loop calls (basic/source/classes/sbxmod.cxx, RunInitGuard::run, used by
  SbModule::Run and SbModule::RunInit). In the guarded core library
  (/usr/lib/libreoffice/program/libmergedlo.so of libreoffice-core) that function
  answers "do not go on" at once and executes nothing: three bytes replaced, at
  the address taken from the debug package of the same build
  (evidence/locate-basic-step.log: two call sites in each release, as the source
  says). No Basic instruction runs, whatever names the code: a macro address, a
  script address, an event, a document, a library of the suite itself. An
  unrecorded library cannot be told from a recorded one at that place, so the
  execution of Basic is refused altogether (CHOICES.md, Revision 54).
- The guard is one more record of the reader-override manifest in the reader
  component. Its payload is the complete guarded library of libreoffice-core
  4:25.2.3-2+deb13u9, the release that a `package libreoffice-writer` line of the
  archive state 20261123T000000Z resolves to, so that the file follows from the
  component by checksum. For the two other pinned releases (deb13u6 in the states
  20260801T000000Z and 20261001T000000Z, deb13u12 in the security state) the record
  lists the same replacement and the assembly makes it in the release's own file.
  A release that the record does not list is refused with a message that names
  the guarded releases.
- Gates: basic-macro-probe.py makes twelve attempts — the default profile and a
  profile given by an option of the command, the library below the home folder
  and below /tmp, a library linked from the profile's index, the macro address
  and the script address, the ordinary account and root; before each attempt the
  same profile converts a document and reads it back. With deb13u9 and with
  deb13u12 no attempt executed the library and every conversion passed
  (evidence/basic-macros-0.54-u9.log, evidence/basic-macros-0.54-u12.log).
  test-basic-guard-unit.py checks the assembly rule for the three releases and for
  an unlisted one (evidence/basic-guard-unit-0.54.log).
- Every installation carries the payload (a compressed copy of the 86 MB library)
  in the reader component, also without the suite.
- The source archive has 491 files.
- No declaration syntax change. Other reader payloads identical to 0.53. Pinned
  components unchanged. The game case passes as in 0.53
  (evidence/game-sequence-0.54.log).

## 0.53 — development, 2026-11-25 UTC

- An application no longer runs out of space in the plan's game case (complete run
  2 on 0.49, OW-8: `No space left on device: '/state/staging/initramfs'` while the
  launcher line 26.6.0 was applied). What took the space, measured by replaying the
  case on the clean installation of that run (evidence/game-sequence-0.49.log): the
  data partition of the 12 GiB disk has 5,834 MiB; at the lowest point of the
  second application it held the person's input files (783 MiB), their frozen
  copies in the staging (530), the downloaded archives and indexes (559), the
  unpacked root (2,677) and its image (998 of 1,244 written). The first
  application already reached 0 MiB free and ended only on the blocks reserved for
  root. Nothing more is kept than in 0.32 (during an application: the generation in
  force and the new one on the system partition, one staging on the data
  partition; after readiness one generation and no staging); the root of the case
  grew from 2,421 MB (0.32) to 2,533 MB (0.49), its image from 1,183 to 1,251 MiB,
  and the case leaves both launcher bundles (2 x 253 MiB) among the input files.
- Repair, both ways: the build command makes a 20 GiB disk (was 12 GiB; the system
  partition keeps its 6 GiB, the data partition grows from 5.9 to 13.9 GiB), and an
  application deletes the downloaded archives from its staging as soon as they are
  unpacked. Gate: test-game-sequence.sh performs the case's own sequence of
  declarations to its end on a disk made by the build command and prints the free
  space before and after every application and the lowest value during each
  (evidence/game-sequence-0.53.log).
- The source archive is reduced to the implementation and what is needed to build
  and test it: the programs, the patches, the example and fixture declarations,
  the documents, the built component packages of this release, the lists of pinned
  inputs with their checksums (pinned-inputs.tsv and the *-source.sha256 files) and
  one folder `evidence/` with the records that the documents cite. Unpacked
  third-party trees, packed third-party inputs, component packages of earlier
  releases and working files of the build are no longer members. The members are
  listed in archive-members.txt: 472 files (the archive of 0.52 held 13,442).
  Before the archive is sealed it is unpacked and scanned with the scan of the
  public repository: no hit of a blocking category in any text file. The built
  component packages stay members, because a build from the archive needs them;
  they are compressed binary files, and in their byte strings the scan reports
  chance matches of its two-letter pattern (23 in 0.53; the whole output is
  releases/scan-0.53.txt beside the archive). That is a departure from "no hit"
  as a count and is stated here for that reason.
- No declaration syntax change. Reader payloads identical to 0.52. Pinned
  components unchanged.

## 0.52 — development, 2026-11-25 UTC

- A declaration whose archive state has another release of a package than the one
  its guarded file was built from is built again (0.42–0.51 refused it: `reader
  override original checksum mismatch`; complete run 2 on 0.49, OW-2 and OW-3:
  curl in the archive states 20260801 and 20261001, libperl5.40 in 20260801).
  The guarded file is installed for whatever release the line names.
- No declaration syntax change. Reader payloads identical to 0.51.

## 0.51 — development, 2026-11-24 UTC

- A recorded container image without `/etc/mtab`, `/proc` and `/sys` runs (case
  X-REC-PODMAN on 0.43: `creating /etc/mtab symlink: read-only file system`; then
  `crun: cannot mkdir proc`).
- `podman images`/`ps` of an account without recorded images print the empty list
  with status 0; `podman image exists NAME` and `npm ls -g` answer.
- No declaration syntax change. Reader payloads identical to 0.50.

## 0.50 — development, 2026-11-24 UTC

- New kind of line `group NAME GID`; `groupadd` and `groupdel` record it.
- New setting `setting module:NAME loaded`; `modprobe NAME` and `modprobe -r NAME`
  record it; declared modules are loaded at every start.
- Queries: `timedatectl show -p Timezone` no longer fails without a timezone line
  and accepts `--value`; `systemctl is-enabled`/`is-active` answer for a `service`
  line instead of `not-found`.
- Reader payloads identical to 0.49. Pinned components unchanged.

## 0.49 — development, 2026-11-24 UTC

- Package files keep their paths and bytes. Releases 0.34–0.48 moved the package
  executables of the recording tools to `/usr/lib/confos/native` and linked their
  paths to the recording entries; an outside comparison with the packages then
  found 10 package files missing and one link changed in every installation
  (development run dev-14b of the case party on 0.43). The recording entries are
  now reached by name through `/usr/local/bin`; the package executables called by
  full path are refused by the session confinement.
- A declaration naming another export of a pinned Flatpak commit builds (the clean
  build of the case party's test declaration failed on 0.43 with `Flatpak reader
  bundle checksum mismatch`).
- No declaration syntax change. Reader payloads are byte, mode and link identical
  to 0.48. Pinned components unchanged (kernel 6.12.118-1, the latest of the
  security archive on the day of the inputs, since 0.43).

## 0.48 — development, 2026-11-24 UTC

- Retry unsuccessful native dependency resolution using all available versions,
  while enforcing every explicit package version and retaining pinned archives.
  This addresses the old Writeru9 request after the archive added u12.
- Preserve reader payloads; declaration syntax and recording protocol unchanged.
  Actual canonical install/document/removal and release gates are in STATE.md.

## 0.47 — development, 2026-11-24 UTC

- Extend native saved-file checks to the exact optional libperl5.40 shared library.
  Preserve all46 reader entries. Unknown original library bytes refuse assembly.
- Require canonical two-boot controls/removal, smoke, updates, source equality
  and inventory before handoff; observed results are in STATE.md.

## 0.46 — development, 2026-11-24 UTC

- Guard the optional exact Debian libpython3.13 shared library's file readers.
  Existing45 readers are preserved; unknown original library bytes refuse.
- Require canonical saved-file/positive controls on two boots, optional package
  removal, extended smoke, updates, fresh-source equality and outside inventory.
  Actual gate results and release status are in STATE.md.

## 0.45 — development, 2026-11-24 UTC

- Add the tested finite nmcli request recorder for existing network rows;
  durable requested text precedes separate application. No radio grammar change.
- Preserve44 native reader payloads byte-for-byte, including modes and links.
- Canonical six-cut radio matrix, smoke, updates and fresh-source/inventory gates
  are required before handoff; exact results are recorded in STATE.md.

## 0.44 — 2026-11-24 UTC

Record supported native visudo snippet edits and explicit removals as file rows,
preserving editor confinement and separate application. Guard exact native SSH
saved config readers while retaining typed options, recorded configs and ordinary
connections. Canonical reader/root controls, nine immediate post-APPLIED cuts,
optional SSH removal, extended smoke and both updates passed. The recorded
editor stays confined; refused include requests leave effective sudoers and
declaration unchanged, but native visudo can edit writable include material
before refusal. Fresh-source/inventory and exact release identities are in STATE.md.

## 0.43 — 2026-11-24 UTC

Record supported nft rule add/handle deletion requests as durable declaration
edits; retain native query forms and direct mutation refusal. Add exact Debian
ed command-input guard while preserving the native red launcher and document
editing. Canonical user/root reader controls, document editing, original red
restrictions and package removal passed. Rule addition, change and removal each
survived three immediate post-APPLIED cuts with native ruleset checks. Extended
smoke and two whole-system updates passed, ending on kernel6.12.118. Fresh-source
and outside-inventory evidence is recorded separately in STATE.md.

## 0.42 — 2026-11-24 UTC

Add exact original-identity-guarded native pdb/gyp/curl saved-input readers.
Preserve all inherited reader files/modes/links and native curl libraries.
Protect native apt/dpkg/cron configuration stores, retaining read queries and
supported declaration recorders. Two guest boots passed17 pdb/gyp and32 curl
controls each; four native root store mutations were refused with unchanged
queries/stores/declaration before and after supported ed recording/apply.
Optional package removal and extended smoke passed. Fresh-source and outside
inventory results are recorded separately in STATE; acceptance is not claimed.

## 0.41 — 2026-11-24 UTC

Add exact native mpv/libmpv/LuaJIT app overrides and preserve original object bytes
with execution/mapping denials. Guard initial Lua/JS and nested file/module reads;
retain explicit data and ordinary media paths. Inherited reader bytes are checked
against sealed40. Permit root read of radio readiness JSON while preserving write
denial, repairing40's external-inventory visibility defect. Two guest boots passed
saved-input/discovery/libmpv/descriptor controls, actual media decoding and EOF,
original-object direct/loader/PROT_EXEC mapping refusals, inherited Bash/Python
controls and app/last-runtime removal. Extended smoke passed. Fixture-copy,
media-event timing and traceback-marker observation failures remain in evidence;
the candidate reader binaries did not change. Source/inventory results are in STATE.

## 0.40 — 2026-11-24 UTC

Add explicit simulated-radio, saved Wi-Fi and native Bluetooth bond input rows.
Restore exact inputs before native association/authenticated traffic and readiness.
Confine controls in a private supervisor namespace, with normal and systemd
lifecycle monitoring. Provide fixed native inspection for independent checks.
Normal/systemd native boots,18 post-APPLIED cuts, independent clean replay,
change/removal/restoration, native/Flatpak control boundaries and both supervisor
death checks passed. Repair normal-PID1 revocation of all readiness/PID files;
preserve before-fix evidence and rerun all canonical gates. Extended smoke and
independent radio payload equality passed. Fresh-source/inventory evidence is
recorded separately in STATE; independent acceptance is not claimed.

## 0.39 — 2026-11-24 UTC

Integrate three exact Flatpak Bash/Python/libpython payloads through the named
reader component. Preserve original repository inodes and deny their execution
and mapping in both profiles. Unknown runtimes and native mpv Lua remain open.
Canonical two-boot reader/alias/namespace and application/runtime removal checks
passed; extended smoke, runtime-source equality and exact inherited component
payload checks passed. Fresh-source/inventory evidence is recorded in STATE.

## 0.38 — 2026-11-24 UTC

Record explicit settings, declared service/user-unit states and account requests
through the existing durable text transaction. Preserve the authorization boundary
before read-only query escalation. New-account defaults are deterministic and
written as complete fields. Separate apply remains required; remaining adapters
are listed in CHOICES. Guest add/change/removal, repeat, pre-apply nonchange,
authorization/query controls and pending/post-APPLIED cuts passed. Source and
inventory verification are recorded separately in STATE.

## 0.37 — 2026-11-24 UTC

Podman pull/rmi record container lines and original native OCI archive inputs for
an explicit or sudo-origin declared account. Private native preparation runs no
image and is removed before reporting success. Repeats retain their recorded pin.
Native helper relocation preserves rootless preparation/run. Actual guest add,
repeat, removal, pre-apply nonchange and pending/post-APPLIED power cuts passed.
Container compatibility and extended smoke passed. Source sealing requires exact
runtime-source/package equality, including a tested stale-module rejection.
Source extraction and outside inventory are recorded separately in STATE.

## 0.36 — 2026-11-24 UTC

Add native Flatpak bundle request recording and dependency-aware removal using
existing flatpak lines and durable bundle inputs. Native metadata inspection uses
isolated scratch; no installed-state inventory. Separate apply remains required.
Remote-add and named-remote install have no current line form and remain refused.
Actual guest add/repeat/removal, pre-apply nonchange, pending-record and
post-APPLIED power cuts and extended smoke passed. Fresh-source payload/disk-input
equality passed. Outside inventory13,632 stored/299 force/zero errors; UNDERIVED63
root differences61 volatile objects. Current/previous pristine images36/35 retained.

## 0.35 — 2026-11-24 UTC

Add pip/npm request recording using their existing line kinds and durable wheel/
native-lock inputs. Explicit/root/module aliases share the recorder; original
native installer helpers remain inaccessible to confined sessions. Separate apply,
exact resolution, repeat/removal behavior and refusals are in INTERFACE/CHOICES.
Native preparation and actual guest recording/add/repeat/removal, pre-apply
nonchange and pending/applied power-cut regressions passed. Native language
compatibility and extended smoke passed. Fresh-source payload/disk-input equality
passed. Outside inventory:13,631 stored objects,299 force rows,zero errors;
63 root deviations and61 volatile objects documented. Current/previous images35/34
retained. Original Flatpak readers remain open; independent acceptance is pending.

## 0.34 — 2026-11-24 UTC

Implement the first S8.3-7 recorder: explicit APT install/remove/purge requests
write durable pinned package lines before separate application. Exact syntax and
refusals are in INTERFACE/CHOICES. Three APT add/removal cycles, pending-record and
post-APPLIED power cuts, authorization, invalid requests and repeated requests pass.
Extended smoke, native reader/vi checks and both whole-system updates pass;
fresh-source payload/disk-input equality passed. Outside inventory:13,630 stored
objects,299 force rows,zero errors;63 root deviations and61 volatile objects
documented. Pin security kernel
6.12.118-1 from security snapshot20261124T000000Z for T2, with the existing main
snapshot; all other native base pins are unchanged. Includes unpublished33
BusyBox vi startup checks and Flatpak app confinement. Original Flatpak readers
remain open; no general P4 or acceptance claim.

## 0.33 — development, continued in34, 2026-11-24 UTC

BusyBox vi .exrc descriptors now follow the immutable-code policy. Native readers
and vi/restart/removal controls passed; original startup shell-command SIGSEGV
was reproduced in both native upstream and patched binaries, so positive vi
controls use native option values. Saved executable-startup negative probes
remain. Extended smoke passed. Flatpak app confinement is enforced, but all nine
original shell/Python/mpv-Lua direct saved-code routes remain open.

## 0.32 — 2026-11-24 UTC

Add checksum-bound Neovim0.10.4 AppImage overrides: native Vimscript/Lua/key-file/
stdin readers, Lua loader cache handling and fixed runtime entry. Native45-route
checks passed through the launcher and internal binary and after restart, with
recorded/typed/data/document controls. Shared and final-owner removal and extended
smoke passed. Source equality passed; outside inventory:13,616 stored objects,
299 force rows,zero errors;58 root deviations and61 volatile objects documented.
Includes Git31 below, with exact component inheritance;31 was not separately
handed over. Earlier30/31 tests keep their original identities. Flatpak remains
open; confinement and BusyBox vi repairs are separate prototypes. Native vi's
saved .exrc reader is open in32. No general P4 or acceptance claim.

## 0.31 — development only, combined into32, 2026-11-24 UTC

Add conditional Git reader payloads for13 native executable paths, preserving
the original package's symlink aliases. Native configuration checks refuse saved
code-valued settings and built-in writes past the declaration. Main/helper routes,
recorded aliases/hooks, repository operations, restart, removal and extended smoke
passed. Source equality passed; its waiting inventory was superseded by32's
combined verification. Component inheritance proves all
previous30 reader bytes unchanged; prior30 language/ordinary/game/update evidence
keeps its original identity. Neovim/Flatpak diagnostics are separate from this release.

## 0.30 — 2026-11-24 UTC

Add conditional native Node20 and libnode115 payloads. Their actual-descriptor
checks cover script/import/preload/stdin/REPL readers, package resolver metadata,
startup snapshot sources/configuration/blobs, environment and policy files.
Native79-route suites passed via node/nodejs and after restart, with removal and
recorded/typed/data controls. Expanded24 snapshot/environment/policy refusals and
recorded snapshot loading after restart passed. Initial snapshot bypasses remain
in the evidence. Extended smoke, two updates, language packages, ordinary work and
game checks passed. Fresh-source payload/disk-input equality passed; outside
inventory reports13,546 stored objects,299 force rows and zero errors. UNDERIVED
lists58 root deviations and61 volatile objects. Git/Neovim prototypes
are not included; no general P4 or acceptance claim.

## 0.29 — 2026-11-24 UTC

Add native dash, mawk, gawk, GNU sed and make as conditional payloads in the
original reader component. Its static manifest supplies target bytes, modes and
activating package names; removal follows ownership. Native suites passed69
shell/awk/sed and30 make refusal routes before/after restart, recorded/typed/data
controls, gawk exact arithmetic/native-extension checks and optional removal.
Extended smoke, two snapshot updates, pip/npm, browser/document/compiler and game
regressions passed. Fresh-source payload/disk-input byte/mode equality passed.
Outside inventory:13,537 stored objects,299 force rows,zero errors;58 root
deviations and61 volatile objects enumerated. Node and Git are separate prototypes,
not included; no general P4 or acceptance claim.

## 0.28 — 2026-11-24 UTC

Extend the original native reader component to BusyBox ash/sh, awk and sed,
using authenticated Debian sources and the static package configuration. Native
path/alias/restart tests, extended smoke, T0/T1/T2 updates, pip/npm and ordinary
browser/document/compiler and game regressions passed. Fresh-source root/disk
byte/mode equality passed. Outside inventory returned13,519 stored objects,299
force rows,zero errors;58 root deviations and61 volatile objects are enumerated.
The inventory waited for shared slots before completing. GNU readers and Node
are separate prototypes, not part of this release.

## 0.27 — 2026-11-24 UTC

Add a genuine confos-code-readers component built from pinned Debian Bash/Python/
Perl sources. Check opened code descriptors, parser refills and Python source/bytecode
imports. Typed commands, pipes and material data reads remain usable. Prototypes
passed32/38/33 refusal routes; native-path/alias/restart checks, extended smoke,
snapshot updates, pip/npm install/remove/re-add, browser/document/compiler and
game install/update/run/removal passed on the final candidate. Fixed omitted Python
extensions, private kernel-context staging and its missing util-linux dependency.
The first ordinary wrapper rejected an expected apply SSH disconnect; its corrected
check requires REBOOTING, subsequent APPLIED and the successful program launch.
Fresh source extraction reproduced root and disk-input bytes/modes. The outside
collector reports13,516 stored objects,299 force rows,zero errors; UNDERIVED lists
58 root deviations and61 volatile objects. BusyBox
and other readers remain open in this release; no general P4/acceptance claim.

## 0.26 — 2026-11-24 UTC

Package the initramfs and module indexes from original pinned Debian archives
and authored early-init, using each snapshot's native depmod/cpio. Clean/apply
copy exact package bytes; retain all three archives for updates. All three
packages matched across independent umask022/077 builds. Extended smoke and
T0/T1/T2 boot/update checks passed, including packaged-vs-boot archive hashes.
Fresh source under umask077 with host GRUB/depmod/cpio disabled produced equal
root and EFI/system/data inputs. Outside inventory:12,462 stored objects,291
force rows,zero errors;59 root deviations and61 volatile objects enumerated.
The initial smoke harness used an absent cmp; initial inventory named a directory.
Both corrected harness runs passed without changing the runtime/source archive.
General saved-code P4 and complete derivation remain unresolved.

## 0.25 — 2026-11-24 UTC

Reject base account/group-name collisions, duplicate/reserved UIDs and malformed
native passwd fields before commitment. Verify native account lookup at boot.
The _apt collision in24 is reproduced in account-p2-probe.log. Account rejection,
add/change/removal, native fields and SSH login passed. Extended smoke and fresh
source equality passed. Outside inventory:12,449 stored objects,zero errors.
All9 post-success power cuts and network interruption/recovery passed. General
saved-code P4 and complete derivation remain unresolved.

## 0.24 — 2026-11-24 UTC

Release23 reported APPLIED for an option-like hostname, an overlong hostname and
conflicting hostname/sysctl lines despite a different running value. Validate
names and aliases before assembly, derive hosts from either spelling, and check
native hostname initialization before readiness. Invalid-candidate rollback,
64-character names, aliases and removal passed; extended smoke, fresh-source
equality and outside inventory passed (12,449 stored objects, zero errors).
A separate account-name collision remains, evidenced in account-p2-probe.log.

## 0.23 — 2026-11-24 UTC

The named confos-boot package supplies exact EFI bytes built from pinned original
GRUB archives and authored configuration; clean builds no longer invoke host GRUB.
Independent package builds, actual packaged-EFI boot, root/ESP/package equality and
two system updates passed. Optional broker links now appear only with their native
package, repairing absent-tool discovery; those conditional links are generated
objects with a remaining D3 obligation. Final smoke, pip/npm, fresh-source equality
with host GRUB disabled and baseline inventory passed (12,449 stored objects,0 errors).
Mixed optional-channel launches passed. Its88,432-object inventory retains2 errors
from querying Flatpak Python outside its namespace; the identical interpreter bytes
return the unchanged metadata query inside Flatpak (evidence/flatpak-python-context.log).
The first candidate's5 discovery errors and source archive remain as evidence.

## 0.22 — 2026-11-24 UTC

Query/run brokers and /usr/local/bin links are genuine runtime-package payloads;
native Debian command files retain their original paths/bytes. Session, sudo and
service PATH select the brokers. Direct native mutations remain refused. The
Python pip module override is an explicit runtime-package replacement. Native
package equality, pip/npm, Flatpak, containers, user units, declared broker-name
replacement/removal and final extended smoke passed. Fresh source extraction
produced equal root and disk-input bytes/modes. Outside inventory: 12,447 stored
objects, zero errors;70 root differences and61 volatile objects. This partially
repairs changed native package files; general saved-code P4 and derivation remain open.

## 0.21 — 2026-11-24 UTC

File lines optionally state numeric UID:GID. The legacy form remains 0:0;
sudo-rule ownership must be 0:0. Native owner/mode enforcement, changes, legacy
syntax, invalid UID rollback and removal passed. Both full Debian updates passed
with the genuine runtime package. Extended smoke, fresh source extraction and
root/disk-input byte/mode equality passed. Outside inventory: 12,426 stored
objects, zero errors; 74 root differences and 61 volatile objects remain.
This supplies explicit file-owner fields, not the other D1–D7 requirements.

## 0.20 — 2026-11-24 UTC

Fixed runtime/default files are shipped in the genuine confos-runtime Debian data
package, named by every component lock and included in the source release. Its
archive is retained read-only for apply. File metadata and retained input modes
are fixed; the unused packages.json ledger is removed. Only the current APT solver
result is unpacked, so a stale cached package no longer appears in a clean rebuild.
The cache regression, final smoke, fresh source-archive extraction with umask077,
equal immutable/disk-input bytes and modes, and outside collection passed. Inventory:
12,426 stored objects, zero errors; 74 root differences from original package data
(109 before runtime packaging), plus 61 volatile objects. This is a partial repair
of derivation inputs, not independent acceptance of Understanding or P4.

## 0.19 — 2026-11-24 UTC

Read-only systemctl arguments are canonicalized with property/type filters, escaped
unit names and `--`; missing declared user managers produce an explicit error.
Native user-unit inspection/mutation/removal and smoke regressions passed. Build
and boot queue at the shared VM limit. A verified inherited slot descriptor supports
guest/appliance reservations across restarts. Outside collections later completed
with zero errors, including all saved-code and unsaved-download/restart probes.
Saved interpreters still executed. Fresh-source permission and stale-cache defects
were reproduced in this release and repaired in 0.20.

## 0.18 — 2026-11-24 UTC

Native LinuxGSM/game bundle installation and launcher update run in staging from
pinned upstream inputs. Code is immutable and account-owned; logs/locks/scratch
are volatile. Clean install, start/stop, update, removal while running and two
independent equal root/initramfs/EFI payloads passed. Root can read private records
without DAC write override; native user-manager mutation regressions still refuse.
Extended smoke passed. Outside game inventories before/after a native updater
attempt have 15,255 stored objects and zero errors; its exit-zero message did not
correspond to changed launcher/module bytes. Baseline inventory has 12,424 stored
objects and zero errors. General saved-code P4 and full derivation remain unresolved.
Additional immutable-payload reproducibility passed for two independent mixed
Flatpak/AppImage/pip/npm/container/user-unit installations (channel-repro-0.18.log).

## 0.17 — 2026-11-24 UTC

Native root /proc/PID/exe inspection across account IDs works through the inspection
capability plus AppArmor read/readby. No trace/tracedby permission is granted.
Cross-UID inspection passed while debugger attachment and process-memory access
were refused (evidence/process-inspection-0.17.log). Extended smoke and outside
inventory passed; no change to the unresolved saved-interpreter-code result.

## 0.16 — 2026-11-24 UTC

Exact file lines below /etc/sudoers.d are supported with restricted names/mode and
no further includes. Native visudo validates before commitment. Failed applications
discard staging/unselected partial generations and restore the read-only system
mount. Native rule effect/removal, direct visudo refusal and invalid-candidate
rollback passed (evidence/sudo-rule-0.16.log). Extended smoke and independent equal
root.sqfs/initramfs/EFI payloads passed (smoke-0.16.log, repro-0.16.log).

## 0.15 — 2026-11-24 UTC

Native pip/npm installation remains in apply; direct entries expose fixed native
inspection in isolated environments. Session access to private installer modules,
pip bootstrap wheels and venv is refused. Clean declared install/run/remove/re-add
and nine direct mutation probes passed (evidence/language-0.15.log); no target
installation directories remained. Extended smoke passed. Arbitrary saved
interpreter input remains an observed P4 failure.

## 0.14 — 2026-11-24 UTC

Unchanged Debian payloads retain archive UID/GID in squashfs; generated objects
retain the documented defaults. libc6-i386 receives its fixed loader compatibility
links. Clean 32-bit execution, package ownership, combined native containers/user
timers, mutation refusals and removal passed (evidence/integrated-0.14.log).
Extended smoke passed. Outside inventory collected 12,421 objects with zero errors;
ownership is now included in the archive comparison. Native LinuxGSM staging start,
update and stop passed, but the ConfOS launcher workspace remains unresolved.

## 0.13 — 2026-11-24 UTC

C.UTF-8 login/service locale with pinned libc-bin in all three snapshot closures;
fixed SSH environment forwarding, standard fd/stdio links, /run and /var mode 0755,
base awk/which links, and native nft rules without generated comments. Tmux, process
substitution, exact rule text, directory modes, extended smoke and native user-unit
regression passed. LinuxGSM still fails on its immutable recorded workspace and the
mutable-copy alternative's noexec script checks; no game-work pass is claimed.

## 0.12 — 2026-11-24 UTC

Native user service/timer declarations with exact unit inputs, deterministic enable
links, confined service children and optional minimal systemd PID 1. Readiness waits
for native managers and enabled units. A fixed read-only native query entry replaces
direct systemctl mutation access; mode-000 manager sockets and removal of session
DAC override/search stop tested ordinary/root transient-service attempts. Native
timer/profile, mutation-refusal and removal regression passed (user-units-0.12.log).

## 0.11 — 2026-11-24 UTC

Account-specific pinned OCI archives with native rootless Podman preparation and
read-only launch. Preserve image ownership with deterministic subordinate-ID ranges;
prepare native mount targets and retire the loader namespace before readiness.
Fixed native configuration and protected runtime metadata. Container regression
passed native launch/ownership, tested mutation refusals and removal through apply.
Extended smoke passed; outside inventory returned zero collector errors.

## 0.10 — 2026-11-24 UTC

AppImage lines pin source bytes, extract the immutable payload at assembly time,
and create declared launchers. Neovim v0.10.4 launched and edited a document in the
VM. Two owners shared the extracted payload; it remained with one owner and vanished
with the last (evidence/appimage-0.10.log). Supported format and xattr restrictions
are documented. No runtime FUSE or extraction is required; general P4 remains open.
Final extended smoke passed (evidence/smoke-0.10.log).

## 0.9 — 2026-11-24 UTC

Native Flatpak bundle lines pin the app/runtime ref, OSTree commit and bundle
checksum. The system store is immutable. The Flatpak command exposes inspection
and ordinary-account launch for declared IDs; direct mutation entries are refused.
Private assembly namespaces provide proc/dev required by the native installer.
One immutable-store AppArmor rule replaces the oversized per-file policy that
failed the first boot. The regression passed mpv installation/launch, tested remote
mutation refusals, and app removal with runtime retention (evidence/flatpak-0.9.log).
General saved-code P4 and full Flatpak reproducibility remain open.

## 0.8 — 2026-11-24 UTC

Read-only native nft inspection through the normal sudo command, with mutations
still refused. A compile line builds pinned C source with declared GCC; clean
compilation, three edits/rebuilds and removal passed. Privileged installers use a
temporary executable view of frozen staging during apply; this repairs the noexec
failure found by the compile regression. Sessions cannot access that view, write
staging or chroot. Extended smoke passed. General saved-code defects remain.
Additional ordinary-work probe fetched the plan's exact hello.c in the VM and
passed three original/edit/rebuild cycles (six outputs): evidence/compile-work-0.8.log.

## 0.7 — 2026-11-24 UTC

Protect home-file ancestors with immutable top-level subtrees; freeze automatic
shell/SSH startup and git defaults, replaceable by exact file lines. Explicit 022
build umask removes host permission dependence. Extended smoke passed rename/startup
refusals. Declared startup changes/removal and shared libjq ownership/removal passed.
Opposite package order produced 12,357 identical root objects, excluding declaration
text/identity. Saved arbitrary interpreter input and direct installer defects remain.

## 0.6 — 2026-11-24 UTC

Pinned wheel/npm-lock lines installed with native pip/npm in the staged root;
recorded programs start and disappear on removal. Deterministic CA bundle and
LibreOffice registry-default copy enable HTTPS, browser screenshot, document
editing/conversion and fetched C compilation/recorded execution in builder probes.
Read-only kernel-log query added. Extended smoke passed. Direct user pip installation
and Node execution of an undeclared npm package still violate P4; evidence and exact
commands are in evidence/language-0.6.log and IMPOSSIBLE.md.

## 0.5 — 2026-11-24 UTC

Complete pinned base closures for T0/T1/T2; application now switches the kernel,
initramfs and root together through a durable boot.cfg selector. Clean T0 followed
by T1 and T2 passed running-kernel/libc checks, sudo and the recorded script.
Extended smoke passed. Two independent clean builds produced identical root.sqfs,
initramfs and EFI executables. Evidence: evidence/updates-0.5.log, smoke-0.5.log and
repro-0.5.log. The subsequent regression passed all nine post-success power cuts
and installation after network loss/restoration (evidence/durability-0.5.log).

## 0.4 — 2026-11-24 UTC

Repairs case request 8: complete PAM sudo/sudo-i/fallback policies work when cron's
dependencies add PAM configuration; hosts follows the declared hostname. Timezone
accepts Etc/UTC. Fresh extended smoke passed, including both sudo modes with cron,
package add/change/removal and service/rule removal. Saved interpreted code remains
an open defect. Evidence: evidence/smoke-0.4.log and evidence/diagnose-sudo-0.3.log.

## 0.3 — 2026-11-24 UTC

Kernel confinement for SSH sessions and declared service children, preserved across
sudo. A fixed immutable application entry may leave that domain; its interpreter,
environment and command lookup are isolated. The generated execution policy names
installed paths. `sudo confos rules` provides a native read-only ruleset query.
File targets cannot replace the trusted application machinery. Extended smoke passed,
including refusal of root hostname, mount and nft mutations while application and
removal still worked. Saved interpreted input is not solved.

## 0.2 — 2026-11-24 UTC

Declared sysctl values, minimal services with immutable JSON descriptors, nftables
input rules. Extended clean smoke passed, including observed service/rule/sysctl state
and removal of the former service process and effective rule. Source release must
match the base line. Systemd user timers and installer-channel kinds remain open.

## 0.1 — 2026-11-24 UTC

Initial empty-root package assembler, immutable squashfs, disk-based EFI boot,
person-written declaration parser, account/key materialization, staged apply and
reboot. Fresh build and extended smoke passed: SSH/sudo, recorded home script,
package addition, change from tree to ed, removal, staging cleanup, native saved-code
refusal. Saved interpreted code still executes (probe-01.log); services, rules,
external installer channels and whole-system snapshot updates remain unfinished.
Development handoff only; no acceptance outcome claimed.

# Inventory collector, version 2

Status: **not ready for observation**. Initial development used disposable Debian
and Rocky Linux 9 only. Authorized throwaway-clone rehearsals are now recorded
in `rehearsal/`; their contents are deleted unread and only numerical reductions
are retained. See `READY.md` for current acceptance and `COL-READY.md` for the
historical development record. NixOS and Guix receive transport tests only.

## Invocation and artifacts

Run the controller on the laboratory server. It reads only the named target:

```sh
LAB_ROOT=TASK_LAB C1/collect.sh --instrument-test col-debian NEW_OUTPUT
LAB_ROOT=TASK_LAB C1/collect.sh --instrument-test col-rpm NEW_OUTPUT \
  --container c1-col-rocky --family rpm
```

`TASK_LAB` contains a copied `lab.sh`, a disposable Debian entry under
`C1/vms/`, or an explicitly declared throwaway container manifest under
`containers/`. Container storage is task-local. Observation mode requires `C1_INPUTS_COMMIT` naming the committed inputs.
There is no local-machine inventory mode. Authorized C1-REH uses
`LAB_ROOT=LAB_ROOT C1/collect.sh --rehearsal reh-SYSTEM-ROUND OUTPUT`; the target
must be a disposable qcow2 overlay backed by its registered read-only base.
The controller uses the same queries and normalization in rehearsal and
observation modes. Rehearsal labels are anonymized and output is reduced then
deleted unread. Talos is selected by registered system metadata; its API
contract is in `TALOS-COLLECT.md`.

The included `collector/probe-linux-amd64.gz` is a static Linux x86-64 helper.
`collector/build_probe.py` rebuilds it on the server; the build requires a Go
runtime matching its checked source-overlay patterns and refuses other layouts.
It does not modify the installed toolchain. Build evidence:
`raw/collector/probe-build.json`. Other architectures are not supported.
The helper is staged exclusively under an executable `/tmp/c1-collector`,
`/var/tmp/c1-collector` or `/run/c1-collector`; those exact directories are excluded
and removed afterwards. No writable executable staging location means explicit
bootstrap failure. The first test discovered `/run` was noexec; see
`raw/debian-full/coverage.tsv`.

Output files:

- `objects.tsv`, `level-1.tsv`, `level-2.tsv`: exactly
  `id, machine, level, kind, name, members, evidence` (tab-separated, CSV quoting).
- `raw/NNNN-query.sh`, `.out`, `.err`: exact query and bounded transport output.
  The previous lab SSH transport merges guest stderr into stdout; the controller
  retains transport stderr separately. This is documented, not discarded.
- `coverage.tsv`: query, exit_status, duration in seconds, raw output rows, bytes,
  stdout/stderr references, status, normalized object_rows. Exit 124 is timeout,
  75 is output/traversal cap, 125 is exhausted overall budget; other failures
  retain their actual status. Exit 127 does not prove the kind is absent.
- `members/<id>.tsv`: complete observed immediate children for each group, never
  a sample. Columns: path, type, mode, owner (numeric uid:gid), size, UTC mtime,
  executable bit, content signature, persistence. Group `members` points to the
  file and records its count and traversal completeness. Filenames with tabs and
  newlines survive TSV quoting. Partial traversal is marked incomplete.
- `package-files.tsv`: package object ID, path, integrity, evidence, rule.
- `configuration-origin.tsv`: every unowned regular file under `/etc` and home
  directories is conservatively included as a configuration candidate; paths,
  mtime, ctime, installation-log metadata references and exact script-path
  mentions are retained. No candidate is silently treated as nonconfiguration.
- `metadata.json`: UTC time, elapsed time, traversal/ownership status and gaps.

The row kind `stored-outside-packages` is used only when supported ownership
queries are complete; otherwise it is `stored-ownership-unresolved`. The same
qualification applies to executable code. This flag concerns the implemented
adapters and is not proof that an arbitrary unknown manager does not exist.

## Levels, facts and uncertainty

Level 1 includes native/application/language package records, system and user
units/timers, runit/OpenRC service evidence, PID-to-executable links, accounts,
groups, sudo/doas/polkit/PAM rule files, kernel module/driver names, TCP/UDP
listening sockets, firewall rules, saved-network identities/files, and container
and image identities. User services are queried without starting a user manager.
A stopped or inaccessible manager is explicitly not collected. Sysfs module
names may include built-ins; module load provenance is not inferred. Process
command lines/comm files are not read. Ports use `ss -H -lntu`, without `-p`.
Nftables JSON rules and engine JSON container/image records are normalized
individually; parse failure is a gap. Network-file contents that may contain
credentials are not dumped; identities and metadata remain available.

Level 2 walks the stored namespace, including homes and mounted filesystems,
and groups non-owned entries by immediate parent. It independently lists files
with executable bits, `#!`, or known shell startup paths. File signatures are
SHA-256 of at most the first 4096 bytes, explicitly **not whole-file integrity**.
Images receive only a raw prefix signature, never an expanded filesystem or
archive. Known engine/Flatpak/Snap stores are opaque objects. Btrfs snapshot
subvolumes are detected using GET_SUBVOL_INFO parent UUID and pruned; ZFS
snapshot children are opaque by their exposed snapshot path. Other image mounts,
custom storage roots and unrecognized snapshot mechanisms remain a coverage gap.
An ioctl failure conservatively prunes a candidate Btrfs subvolume; its exact
snapshot identity then needs further evidence.

Persistence comes from statfs: tmpfs/ramfs are runtime, normal stored filesystem
types are persistent, overlay or failed detection is unknown. Read-only flags
are preserved per entry. This describes the mounted filesystem, not a promise
that a container or temporary disk will be retained by the operator.

Package facts use only manager records. `reason` is always explicit, dependency
or unknown; it is never guessed from a package name:

| Manager | Own-record reason query or record |
|---|---|
| dpkg/APT | `dpkg-query -W`; `apt-mark showmanual`, `apt-mark showauto` |
| RPM/DNF | `rpm -qa`; `dnf -C repoquery --installed --qf` with full package identity and `%{reason}`; user is explicit, dependency/weak dependency are dependency, group/external/unavailable remain unknown |
| RPM/zypp | `/var/lib/zypp/AutoInstalled` |
| pacman | `pacman -Qqe`, `pacman -Qqd` |
| apk | `/etc/apk/world` plus installed database |
| XBPS | `/var/db/xbps/pkgdb-0.38.plist` automatic-install flag; absent flag is the manager manual-install default |
| Portage | direct atoms in `/var/lib/portage/world`; unexpanded set members unknown |
| Flatpak | `flatpak list --app` versus `--runtime`, system and user |
| Python | `.dist-info/REQUESTED` and METADATA/RECORD; native-owned metadata links its native package provenance |
| npm | top-level lockfile entries; transitive entries dependency; unlocked records unknown |
| Cargo | `.crates2.json` installed-binary records |
| Snap/Ruby/other unsupported cases | unknown, with the unavailable fact/adapter named |

`collector/PACKAGES.md` contains the detailed adapter coverage and primary source
references. Native file manifests establish ownership; full hashes are compared
only with installation digests (dpkg conffiles/md5sums, RPM file digests, APK
checksums, XBPS SHA256 file manifests, Portage CONTENTS, Python RECORD). One file is hashed only if regular
and no larger than 16 MiB; unsupported hashes, inaccessible paths, symlinks or
missing verification records remain unknown. Size disagreement is changed.
Successful missing-file verification is missing. Canonicalization uses captured
symlink metadata, never the controller's filesystem. npm directory containment
is deliberately not ownership evidence, because it would hide locally added files.

For configuration creation time, mtime is last modification and ctime is inode
change, neither proves creation. An exact path in an installed maintainer script
does not prove that branch ran. Therefore `created=unknown` unless reliable
creation/installation evidence is available; this implementation does not collect
birth times or establish an installation interval. It retains the timestamps and
script mentions instead of asserting “later” from a newer mtime. The fixture's
post-install-generated configuration is linked to its script and remains unknown.
This factual limitation is material to downstream decisions.

A read-only image must have a package-like identity plus actual read-only/verified
mount evidence before its files can be called unchanged by the image rule. The
current generic adapter preserves mount flags but does **not** implement that
image-to-file mapping. Talos image integrity therefore remains unknown, as
explicitly documented in `TALOS-COLLECT.md`.

## Bounds and portability

The walk uses static syscalls/standard-library directory APIs, not GNU-specific
`find -printf` or `stat` syntax. Tests used GNU, BusyBox and toybox PATHs. It
never follows symlink directories or opens FIFO/socket/device contents. Safe
content opens use component-by-component openat/O_NOFOLLOW plus filesystem-type
checks. `/proc`, `/sys`, `/dev` are excluded from stored traversal and content
reads, including symlink aliases. Only process/module/driver names and executable
symlink targets are requested there. The helper runtime's own startup sysfs,
auxv and random-device fallbacks are disabled by the build overlay; the fixture
traces helper opens. System tools still implement their documented APIs; their
internal reads were not comprehensively traced.

Bounds: 600 seconds and 1,000,000 entries for the walk; 4096-byte signatures;
16-MiB metadata reads and whole-file digests; 64-MiB query output (512 MiB for
filesystem NDJSON); explicit time limits per query; query budget 1740 seconds;
controller alarm at 1760 seconds plus up to 10 seconds for cleanup. Caps are
failures/incomplete coverage, never successful absence. Results are checkpointed
after each query and failures do not stop later queries. Large/busy installations
can hit these bounds; no universal 30-minute completeness claim is made.

## Validation and remaining work

`COL-READY.md` is the requirement-by-requirement result. The tested final full
collections passed automatic membership, schema, reason and integrity checks.
Subsequent narrow JSON normalization and member-reference changes were tested
with guest fixtures (`raw/parser-tests-final.log`); a new full collection was not
needed to validate those isolated branches. No hypothesis classification was made.

Remaining blockers include exhaustive manager coverage (particularly Flatpak,
Snap, Ruby and unsupported user language environments), pacman integrity
adapter, Portage selected-set expansion, reliable configuration-creation facts,
read-only system-image mapping, arbitrary mounted image/container roots, and
untested full service/network/firewall coverage on other init systems. Talos API
limits are explicit rather than replaced by unsafe filesystem reads.

## Rehearsal acceptance limitations

A filesystem query returning 75 is incomplete traversal (entry/time cap or
traversal errors), not an empty inventory. Numerical row counts do not identify
the affected paths. Query exit 127 is the documented missing-tool limitation;
nonzero user-manager/engine queries can reflect unavailable managers or APIs,
but their precise cause is not inferred from status alone. Such unexplained
nonzero queries remain unresolved. Collector exit 1 or 2 is not successful
collection even when partial level rows exist. The package-known counters
retain every package object, including separate language-manager metadata;
unknown reasons are never filled from absence or from a package name.

The overlay provenance check uses read-only `qemu-img info -U` because the guest
already holds the disk lock. An initial guard version omitted `-U` and refused
active disks before bootstrap; the affected numerical failures remain disclosed.
The shared static helper is published in 250000-byte compressed chunks. The
controller joins those chunks when the unchunked compressed file is absent.

## FX repair limitations and file accounting

SSH and Talos transports preserve stderr separately from query stdout. Guix serial transport retains its legacy combined framing and is used only for the twenty fixed exit-status calls; no inventory is authorized there. Optional
commands unavailable with status 127 remain not collected, without an absence
claim. A user service/timer/unit-file query whose diagnostic says the session
bus is unavailable is not collected; the collector does not create a user manager
to change the machine. MicroOS FX1 records this precise limitation in
`rehearsal/microos/FX-DISCLOSURES.md`. Missing DNF on a zypp system is harmless
to the reason fact when the native AutoInstalled record succeeds.

Package directories remain in the ownership map, but are not entries in the
packaged-file integrity denominator. Symlinks remain entries and are compared
against native recorded link targets when supplied. Regular files use full
installation hashes; unknown facts remain unknown. Exact native ownership of
Python/npm metadata records parent-package provenance only. A distinct language
package requires its own manager request or lock evidence for its reason; no
native-parent reason is transferred. No package name or mere absence of a
language-manager request flag supplies an install reason.

The documented `/run/user/UID/doc` document-portal boundary is represented as
one opaque virtual alias namespace, without traversing its FUSE contents. Its
metadata is unknown when unavailable; the ordinary stored namespace remains
walked independently. This avoids counting the same exported files through
a user-specific virtual view that root cannot access. Source: the official
[Documents and FUSE documentation](https://flatpak.github.io/xdg-desktop-portal/docs/documents-and-fuse.html).
Alma FX2 diagnosed permission denial at that boundary; the stderr is retained.

Optional user Flatpak scopes that explicitly report inaccessible or absent scope
are not collected. An optional container engine whose diagnostic identifies an
unavailable socket/service is not collected. Gentoo's installed nft binary can
report `JSON support not compiled-in`; its JSON rules interface is then not
collected. These limitations require retained stderr for the exact query, an
explicit class and a reference to this section in `query-limitations.tsv`.
Timeouts, output caps, filesystem traversal errors and unexplained failures are
never accepted as optional-interface limitations. Repeated queries sharing a
name/status are accepted only when every corresponding diagnostic is explained.

K3s's documented default embedded runtime stores at
`/var/lib/rancher/k3s/agent/containerd` and `.../cri-dockerd` are opaque image/container
stores. The corresponding `/run/k3s/containerd` and `/run/k3s/cri-dockerd` runtime trees are also opaque, preventing traversal into live container root filesystems. The [Linux runtime configuration](https://raw.githubusercontent.com/k3s-io/k3s/master/pkg/agent/config/config_linux.go) fixes those state paths. This covers the fixed server script's default data directory; arbitrary
custom data directories remain a stated scope limitation. Primary source:
[agent configuration](https://raw.githubusercontent.com/k3s-io/k3s/master/pkg/agent/config/config.go).

Homebrew discovery checks `brew` with `command -v` in the system and login-user
scopes, including the documented Linux prefix `/home/linuxbrew/.linuxbrew/bin`,
user `.linuxbrew/bin`, and parent directories of scanned paths ending in
`/bin/brew`. It never executes Homebrew or formula code. Discovery records an
explicit unsupported-adapter gap and marks ownership coverage incomplete:
Homebrew package identities, per-file manifests, install reasons and integrity
are not inferred. Custom prefixes outside the bounded filesystem scan and all
searched PATHs can remain undiscovered; non-discovery is not proof of absence.
The fixed Fedora action uses the documented default prefix. Source:
[Homebrew Installation](https://docs.brew.sh/Installation).

Mint FX1 also exposed the documented GVFS FUSE alias boundary at
`/run/user/UID/gvfs`. The probe represents this exact numeric-UID namespace as
an opaque `gvfs-alias` before lstat, with unknown metadata; contents are not
collected and ordinary stored namespaces are still walked. The GNOME
[GVFS documentation](https://wiki.gnome.org/Projects/gvfs/doc) identifies the
“default mount point” as `/run/user/<UID>/gvfs`; custom and legacy GVFS mount
locations are not generalized into this boundary.

User Flatpak listing now checks the documented default
`$HOME/.local/share/flatpak` directory before invoking Flatpak, and pins
`FLATPAK_USER_DIR` to that exact scope. An absent or inaccessible default scope
returns125 with an explicit stderr limitation, without creating directories
for system accounts. Custom per-user installation locations are not collected.
The [Flatpak filesystem documentation](https://github.com/flatpak/flatpak/wiki/Filesystem)
places per-user applications in `$HOME/.local/share/flatpak/app/`.
Earlier Flatpak assertion failures remain failures; they are not reclassified
as scope absence.

The optional DNF4 selected-group query explicitly tests readability of
`/var/lib/dnf/history.sqlite` before invoking its Python helper. Status127 with
empty stderr from that exact guarded query is an unavailable-manager-record
limitation, not proof that a command or interpreter is missing. No reason fact
is inferred from the missing record.

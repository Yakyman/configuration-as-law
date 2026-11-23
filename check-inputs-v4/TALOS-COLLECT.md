# Talos API collector, repaired rehearsal version

Implementation: `collector/talos.py`. Initial development was documentation-based.
The separately authorized C1-REH throwaway-clone run is recorded by numerical
statuses and counts under `rehearsal/talos/`. Inventory output was deleted unread. Authorized instrument stderr and coverage are retained under `rehearsal/talos/diagnostics/`.
Successful API calls do not remove the unavailable facts listed below.

The previous attempt read an unbounded process pagemap stream. Its termination
record reports more than 137 GB in 1112 seconds and no inventory file. Evidence:
`../../night-1122/D1/in/control/talos/termination.json`. This implementation
never calls `read`, `copy`, support-bundle retrieval, a remote shell, or recursive
listing. It never requests contents of `/proc`, `/sys`, or `/dev`.

## Queries and limits

All requests use documented `talosctl` API commands. `collect(ctx)` passes argv
arrays to `ctx.query(label, argv, timeout=15, max_lines=N)`; the image-config query uses host Python to redact the API result before retaining raw output. The controller owns
credentials, transport, raw files, exit status, duration, and emitted-row
coverage. It must terminate a command on byte/line/time bounds and record a
nonzero exit. No failure is interpreted as absence.

| Kind | API command | Boundary |
|---|---|---|
| Installed image | `version`; redacted `get machineconfig v1alpha1 -o json`; `get MountStatuses.block.talos.dev -o json`; `get Disks.block.talos.dev -o json` | One package-like object; explicit reason only when active configuration names the install image; readonly mount/backing evidence retained separately; image and file integrity remain unknown because complete covering mounts and verification are unavailable |
| Services | `service` without arguments | One row per service |
| Processes | `processes` | One row per PID and displayed command; no process memory or executable-link reads |
| Modules | `get loadedkernelmodules -o json` | One row per exposed resource |
| Mounts | `mounts`; `get mounts -o json` | Raw mount evidence; no inferred read-only state |
| Extensions | `get extensions -o json` | Reason unknown; not separate conventional packages |
| Network configuration | `get LinkSpec`, `AddressSpec`, `RouteSpec`, `ResolverSpec`, `TimeServerSpec`, each `-o json` | Desired configuration from all sources; not proof of manual/saved origin |
| Network state | `get links`, `addresses`, `routes`, each `-o json` | Observed state kept separate from desired configuration |
| Sockets | `netstat --all` | Host namespace only |
| Containers/images | `containers`; `image list` | Default runtime namespace; opaque objects |
| Files | `list --depth 1 --long <directory>` | Immediate directory only; never `--recurse` |

There are at most 64 directory requests, maximum traversal depth 4, at most
4096 accepted members globally, and 20000 parsed rows per other query. Each
directory request also sets a client output-line limit to the remaining member
budget plus its header. The API has no documented count-limit parameter:
the client terminates the stream when its bound is crossed; this does not prove
a server-side count bound. The controller additionally caps bytes. All 21
non-list requests and 64 list requests at their 15-second timeouts sum to
1275 seconds before bounded parsing/output overhead. This is a design bound,
not evidence of a live run completing within 30 minutes.

The walk does not follow symlinks. Stored image/container artifacts, pseudo roots, container
storage directories, and snapshot directories are opaque objects. The API-exposed installed `/usr` namespace is listed for per-file facts of the single image package; this does not extract a stored image artifact. The complete
exclusion set is `OPAQUE` in the source. Unknown storage layouts remain a stated
gap: this adapter cannot prove that every unfamiliar directory is outside an
image, container, or snapshot. It therefore cannot certify full filesystem
coverage. Reaching any depth/count bound emits an explicit gap.

Only successfully decoded, untruncated immediate-child listings create group
rows. Every such row has its full decoded member list in `members/<id>.tsv`;
partial failed groups are not emitted as complete groups. Mode, UID:GID and size
come from the listing. Exact mtime is unknown: CLI display loses either the year
or seconds, with the original display retained separately where supported.
Signatures and persistence are unknown. Outside the installed `/usr` image namespace, file ownership is unknown, so groups
are `stored-ownership-unknown`, never asserted to be unowned. Executable regular
files and known shell startup filenames outside that namespace have separate `code-ownership-unknown`
rows. Installed `/usr` regular files and symlinks are recorded as image-file candidates, while their integrity stays unknown. Symlinks are never followed or omitted from the final file-fact table.

## Facts not collected

- The active machine configuration supplies the installed-image reason when it names the installation image. A host-only standard-library Python filter emits only image references; credentials are never retained in the raw output. Extension reasons remain `unknown`; no manager ownership manifest is available.
- No image signature verification is performed. The block mount resource exposes `readOnly`, `filesystem` and `target`; the disk resource exposes a readonly block-device flag. These are retained as mount/backing evidence, not equated with integrity of every file visible through the root namespace. The available APIs cannot certify the complete covering-mount map: the mounts CLI omits zero-sized/file mount rows and the legacy runtime projection omits options. Therefore the final collector always leaves both image integrity and packaged-file integrity `unknown`, including symlinks. No file is called unchanged merely because its backing device is readonly or Talos is described as immutable.
- The installed `/usr` namespace is enumerated within bounds, but the complete image manifest is not available. The image remains one package-like object; stored image artifacts are not extracted.
- Bounded file-content reads are not used. Content signatures, shebang-only
  scripts, package installation scripts, and configuration creation at
  installation versus later are not collected. Modification timestamps alone
  would not establish creation provenance in any event.
- Complete unowned-file groups, process executable links, accounts and groups,
  sudo/doas/polkit rules, system/user timers, complete firewall state, persistence
  per file, and saved/manual network provenance are not collected.
- Workload interiors, non-default runtime namespaces, hidden/inaccessible API
  paths, unknown snapshot layouts, and ambiguous filenames containing newlines
  remain uncollected. Parser failures are gaps, not successful empty inventories.

These limitations are also appended to the runtime gap list. A successful API
response does not close them. This adapter lists only what the documented
interface exposes; whether that counts as the second-level inventory of
Section 9.2 is not decided here (see `QUESTIONS.md`).

## Primary sources checked before implementation

- [CLI reference](https://docs.siderolabs.com/talos/v1.14/reference/cli):
  `list` is described as “Retrieve a directory listing”; the documented depth
  flag is “maximum recursion depth”. Commands above are read-only forms.
- [Listing implementation](https://raw.githubusercontent.com/siderolabs/talos/v1.14.0/cmd/talosctl/cmd/talos/list.go):
  depth defaults to 1; recursion becomes unlimited only with recurse. Long
  output supplies NODE, MODE, UID, GID, SIZE(B), LASTMOD, LABEL and NAME.
  Symlinks append their target. Timestamps use two lossy display formats.
- [Mount implementation](https://raw.githubusercontent.com/siderolabs/talos/v1.14.0/cmd/talosctl/cmd/talos/mounts.go):
  mount table reports filesystem usage and mountpoint, without read-only flags.
- [Linux administration reference](https://docs.siderolabs.com/talos/v1.14/learn-more/talos-for-linux-admins):
  listing “Lists exposed filesystem paths only”; documents loadedkernelmodules,
  mount resources, and absence of a conventional package manager.
- [Networking resources](https://docs.siderolabs.com/talos/v1.14/learn-more/networking-resources):
  “Spec” defines desired configuration; “Status” describes current state.
  Configuration may originate from machine configuration, metadata, or DHCP.
- CLI source files [service](https://raw.githubusercontent.com/siderolabs/talos/v1.14.0/cmd/talosctl/cmd/talos/service.go),
  [processes](https://raw.githubusercontent.com/siderolabs/talos/v1.14.0/cmd/talosctl/cmd/talos/processes.go),
  [containers](https://raw.githubusercontent.com/siderolabs/talos/v1.14.0/cmd/talosctl/cmd/talos/containers.go)
  establish the table headers used by the parser. Version-specific output or
  unsupported resource aliases fail closed with explicit gaps.

## Authorized fixture validation

Run only on the disposable Debian development guest, with the source copied
there, from its collector directory:

```sh
python3 -B -c 'import json, talos; print(json.dumps(talos.fixture_check(), sort_keys=True))'
```

The fixture uses a fake context and makes no API calls. It checks JSON streams,
metadata parsing, complete immediate membership, spaces in names, path escape
rejection, failure continuation, exclusion of pseudo/image/snapshot paths and
symlink traversal, no content requests, and supplied query time/count limits.
The main task records the actual guest command and output evidence. This
document does not claim that a fixture or live Talos run passed before that
evidence exists. Transport timeout/byte/line enforcement must be tested by the
controller's separate fixture; parser mocks do not verify process termination.

## Repair evidence and reporting

The package record now uses structured facts rather than a semicolon string.
A zero-row packaged-file denominator is not treated as a passing percentage,
and the opaque image is never fabricated as a packaged file. Complete image
file enumeration remains unavailable. Section 9.2 says: “A machine on which
the second-level inventory has not been obtained cannot yield 1: its outcome
is 0 if an object meeting the failure condition below is found on it, and ?
otherwise.” Whether the rows this adapter obtains count as that inventory is
recorded as a question for the author in `QUESTIONS.md`.

New primary sources: [active configuration resource](https://raw.githubusercontent.com/siderolabs/talos/v1.14.0/pkg/machinery/resources/config/machine_config.go),
[JSON serialization](https://raw.githubusercontent.com/siderolabs/talos/v1.14.0/cmd/talosctl/cmd/talos/output/json.go),
[block mount status](https://raw.githubusercontent.com/siderolabs/talos/v1.14.0/pkg/machinery/resources/block/mount_status.go),
and [legacy mount projection](https://raw.githubusercontent.com/siderolabs/talos/v1.14.0/internal/app/machined/pkg/controllers/runtime/mount_status.go).
The first exposes the active configuration as YAML text; the second retains
that text in JSON; the block resource exposes actual readonly state whereas
the legacy projection omits options.

Actual readonly-backing evidence uses the [disk resource schema](https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/pkg/machinery/resources/block/disk.go)
and [disk controller](https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/internal/app/machined/pkg/controllers/block/disks.go).
The [mount API](https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/internal/app/machined/internal/server/v1alpha1/v1alpha1_server.go)
returns mounted sources and targets but not flags; its CLI suppresses zero-sized
and file mount rows. Therefore complete mount masking is not certified.
The version-specific readonly boot design is documented by
[init](https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/internal/app/init/main.go)
and [mount constructors](https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/internal/pkg/mount/v3/helpers.go),
but is not substituted for actual API readonly evidence in the facts.

## Final source versus rehearsed source

Round 14 is the fourth and last fresh-clone rehearsal: it counted 95 regular
packaged files, all integrity unknown. After that round, conservative source
review added symlinks to the file-fact table with unknown integrity and disabled
readonly attribution without a certified complete covering-mount map. It also
removed the image-level integrity implication from readonly backing evidence.
These final source restrictions were not represented as a fifth rehearsal or
as a new measured file count. The recorded 0/95 is the round-14 result only.

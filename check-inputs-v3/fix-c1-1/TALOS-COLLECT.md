# Talos inventory instrument: documentation-only draft

This instrument has not been run against any Talos machine. It intentionally exits 2 and marks its output incomplete. It captures documented API evidence but is not yet a complete equivalent of the general collector. It must not be used for the first observation until the missing normalization and ownership steps are completed and committed.

Source: https://docs.siderolabs.com/talos/v1.14/reference/cli . The reference documents `get`, `service`, `processes`, `containers`, `image list`, `netstat`, `read`, `list`, and `copy`. The `list` command has `--recurse`, `--depth`, and `--long`; `read` retrieves an exact path. No diagnostic/debug container is launched: doing so would add code and processes before inventory.

| Required category | Planned API evidence | Remaining work |
|---|---|---|
| Packages and application/language managers | image lists in system, cri, inmem and taloscontainers namespaces; release SBOM | Match actual installed filesystem objects against release SBOM; enumerate any additional managers without assuming absence |
| Services and timers, system and user | service list; machine config; whole filesystem | Expand rows and distinguish absence from unsupported API |
| Processes and executables | processes; `/proc/<pid>/exe` via API where readable | Process-to-executable relation and namespace coverage |
| Accounts, groups, sudo, polkit | passwd, group; config; whole filesystem | Derive all access rules from actual objects; no documentation-based assumption of absence |
| Kernel modules/drivers | `/proc/modules`, `/proc/devices`; sysfs API listing | Driver binding expansion |
| Ports | netstat host and later namespace-specific calls | Include each relevant namespace |
| Firewall and saved networks | resource definitions and config; links, addresses, routes | Configuration describes intended ingress policy; effective nftables dump remains unresolved |
| Unowned stored objects grouped by parent directory | recursive API listing; SBOM ownership | Package ownership not currently available from a documented installed-package database; unresolved |
| Executable code outside packages | permissions and targeted `read` for shebang/startup files | Complete path iteration and ownership relation unresolved |

`objects.tsv` currently holds source-bundle pointers labelled `source` and `UNEXPANDED`, never pretends they are classified inventory objects. Failed API reads are recorded with exit codes and cannot establish absence. This draft does not satisfy all Section 4.2 inventory requirements.

The lab's Talos `run` transport executes the supplied shell script on the host with a per-clone `talosctl`, `TALOSCONFIG`, `TALOS_ENDPOINT`, and `TALOS_NODE`. It is not an in-machine shell. Only installation and authentication smoke commands may use it during preparation.

Additional primary sources resolve several draft commands: https://docs.siderolabs.com/talos/v1.14/advanced-guides/SBOM documents `get sbom` and the core/extension SBOM directories. https://docs.siderolabs.com/talos/v1.14/learn-more/talos-for-linux-admins documents `get loadedkernelmodules`, `get pcidevices`, link statuses, and states that `list` exposes filesystem paths only through its API. It also states there is no native package manager or systemd. This is documentation evidence about the instrument, not an observation of a check machine. It does not establish absence of every possible workload package manager.

A complete filesystem result cannot currently be promised from these documented interfaces: the Linux-admin guide describes the listing as “Lists exposed filesystem paths only”. The CLI `copy <path> -` streams an archive with ownership/permissions, but neither source establishes exhaustive access to all stored paths or provides a complete package-file ownership map. Exporting an incomplete tree and labelling its complement “unowned” would be invalid. The ingress-firewall guide https://docs.siderolabs.com/talos/v1.14/networking/ingress-firewall describes generated nftables rules and possible additional CNI filtering; machine config alone does not establish all effective rules. These specific coverage limitations block a claim that the draft is a complete equivalent. No on-machine workaround has been attempted.

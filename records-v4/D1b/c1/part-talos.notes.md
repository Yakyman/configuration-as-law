# Part talos: c1 notes

2026-11-23 UTC. Scope: the 43 input rows in `D1b/in/part-talos.tsv`.
This classification did not participate in supplement step 4 parts 1–3 and did not consult another classification, a rehearsal, an adjudication, or an earlier decision. Inventory reads used only the delivered Talos handoff. No machine probes were run.

## Order and evidence limits

S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”

S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

All 287 entries in `D1b/handoff/talos/package-files.tsv` have `integrity=unknown`; all concern `/usr` paths. No comparison for the selected `/etc`, `/opt`, `/boot`, or store objects is supplied. The selected entries of `talos-fact-index.tsv` explicitly retain `unknown:image-reference-field-empty`. Current SHA256 digests and ELF signatures in `talos-content.tsv` identify present content, not its original installation contents or acquisition history. No default origin is inferred from a filename, a comment prefix, or a read-only view.

S8.2-5: “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.”

`talos-mountinfo-coverage.tsv` identifies the API daemon namespace. The saved query is `raw/0086-s4-talos-mountinfo.sh`; its output and parsed table provide 29 mounts. Parent IDs were considered: root mount 40; `/etc` overlay 46; `/etc/cni` and `/etc/kubernetes` tmpfs children 50 and 51; `/run`, `/system`, `/tmp` mounts 37, 41, 42. `/dev`, `/proc`, `/sys` are pseudo-filesystem roots. These specific volatile members are RUNTIME. Their creating Talos filesystem setup has UNKNOWN coverage because the installed-image/reference and configuration-origin facts are absent. This is a named unresolved creator decision, not an assumption that every runtime object requires its own line.

The `/etc/extensions.yaml` mount (36, parent 40) does not establish that the later `/etc` overlay (46) exposes it. `/var` is XFS mount 79 on a block device: its ordinary stored contents are persistent. `/opt` mount 95 combines an unresolved lower layer with a persistent upper and work area under `/var/system/overlays`. Neither its mount flag nor the path alone identifies the layer containing each file. Overlay lower paths are namespace-relative, so no longest-prefix-only resolution was used. Workload namespaces are not represented by the API daemon's table. In particular, a failed later read is not evidence that an earlier listed file was runtime-only.

Public filesystem references:

- [Kernel tmpfs documentation](https://docs.kernel.org/filesystems/tmpfs.html): “If you unmount a tmpfs instance, everything stored therein is lost.” This supports the volatile members, not the unresolved overlays.
- [Kernel overlayfs documentation](https://docs.kernel.org/filesystems/overlayfs.html): “An overlay filesystem combines two filesystems - an ‘upper’ filesystem and a ‘lower’ filesystem.” A merged path alone does not supply its historical source.

## Scripted rule I: container image acquisition unknown

The only classification rule applied to multiple input rows is the first twelve rows in `part-talos.write.py`. Each is a stored CRI image reference observed in `raw/0021-talos-images.out`. Such images are managed as whole units by the runtime's image installation/removal tools, satisfying S8.1-4 and S8.1-6, then S8.2-7–8. For each, no installation reason or historical pull actor is supplied. S8.2-16 therefore leaves an evidential distinction between an explicitly obtained package requiring its own line and system acquisition from a recorded source allowing derived coverage. Result: UNKNOWN, not a textual gap.

[The official CLI reference](https://docs.siderolabs.com/talos/v1.13/reference/cli) describes the relevant operations: “Pull an image into the machine’s container runtime” and “Remove an image from the machine’s container runtime”. This establishes available operations, not which one caused these particular entries.

`talos-image-sources.tsv` and `raw/0087-s4-talos-source-images.out` identify three current control-plane image references. These are not pull histories. `io.cri-containerd.image=managed` and `pinned` are runtime labels, not explicit/dependency installation reasons. The three aliases of each image retain separate input IDs; no deduplication was performed.

Ten rows checked by hand against the actual image listing and current-source table:

| ID | Check |
|---|---|
| d1b-talos-a17c1f63854bee1c87899ea5 | API server tag; current source exists, pull actor absent. |
| d1b-talos-a3943a08f9a984711a8f2f6c | API server digest reference; same manifest, no actor. |
| d1b-talos-a50f0524d2017d10970b75e0 | Controller-manager tag; current source exists, actor absent. |
| d1b-talos-fb4c72097532b2a6e5ee7f0d | Controller-manager digest reference; same manifest, no actor. |
| d1b-talos-e634add8a1918968c654058e | Scheduler tag; current source exists, actor absent. |
| d1b-talos-368fc0eb6b7bf8eeefa09780 | Scheduler digest reference; same manifest, no actor. |
| d1b-talos-1de301bc31af36a197dad392 | Pause tag; pinned label does not establish acquisition reason. |
| d1b-talos-bf9ff0c5e4f144ed63716c37 | Pause digest reference; same missing reason. |
| d1b-talos-765c2ea628f6919041741da8 | Bare identifier resolves to controller-manager manifest; no actor. |
| d1b-talos-b2e3362f68a9561179bc10f4 | Bare identifier resolves to scheduler manifest; no actor. |

## Individual and group decisions

The remaining 31 rows were decided individually and are explicit append calls in the writing script. Their similar UNKNOWN outcomes are not a filename-classification rule. Every referenced `members/<raw-id>.tsv` was read completely and its row count checked. For ordinary groups these are immediate members; an unclassified directory is not silently replaced by its descendants. For the six formerly opaque directories, all available descendants in `talos-expanded-members.tsv` were read, along with content and coverage tables. The available descendant counts are 1 (`/etc/containerd`), 2 (`/opt/containerd`), 4 (`/var/system`), 8350 (`/var/lib/containerd`), 74 (`/var/lib/kubelet`), and 3 (`/var/log/containers`). Eighteen explicit container snapshot boundaries remain unexpanded, as recorded in `talos-listing-boundaries.tsv`; no empty contents were inferred there.

The output's MIXED groups partition their members exhaustively:

- Root: six specified volatile roots are RUNTIME; all twelve remaining immediate members are UNKNOWN.
- `/etc`: its two specified tmpfs roots are RUNTIME; all nineteen remaining immediate members are UNKNOWN. This does not classify every `/etc` file as volatile.
- `/var/lib/containerd`: the two exact metadata databases and introspection UUID named in the reason are RECORD; the other 8347 expanded members are UNKNOWN. The record decisions concern runtime metadata, not executable snapshot contents. The changing Bolt database was successfully refreshed in `raw/1410-s4-talos-content-refresh.out`. Opaque boundaries and absent image-to-member comparisons prevent claiming that every snapshot member remains as installed.
- `/var/lib/kubelet`: six top-level files ending `_state` and three files directly under `image_manager/pulled` are RECORD; the remaining 65 expanded members are UNKNOWN. Certificate/key origin, missing content, and workload mount exposure remain factual limitations. Stored socket inodes are not assumed to disappear with their processes.

S8.2-15: “Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.”

Documentation and source supporting the identified records:

- [Containerd content flow](https://raw.githubusercontent.com/containerd/containerd/main/docs/content-flow.md): “A final mutable mountable filesystem, an "active snapshot", must be created on top of the final layer of content for the image.” Its store structure distinguishes image content, unpacked layers, and mutable snapshots; a blanket cache decision would skip questions one and two.
- [Kubelet files reference](https://kubernetes.io/docs/reference/node/kubelet-files/): “All resource managers keep the mapping of Pods to allocated resources in state files.” It names CPU, memory, DRA, allocated and actuated resource checkpoints.
- [Kubelet image pull records source](https://raw.githubusercontent.com/kubernetes/kubernetes/master/pkg/kubelet/images/pullmanager/fs_pullrecords.go) implements the persisted image pull record accessor.
- [Kubelet shutdown manager source](https://raw.githubusercontent.com/kubernetes/kubernetes/master/pkg/kubelet/nodeshutdown/nodeshutdown_manager_linux.go) persists shutdown state for later restoration.
- [Kubelet container startup source](https://raw.githubusercontent.com/kubernetes/kubernetes/master/pkg/kubelet/kuberuntime/kuberuntime_container.go): “Symlink container logs to the legacy container log location for cluster logging support.” The three links in `raw/0093-s4-talos-list.out` point to per-pod logs. They are persistent logging records, not shell commands or startup settings. All three were inspected individually.

The six CNI binaries have successful content reads and ELF signatures. That establishes present executable content, but does not answer the earlier unchanged-package question or identify a system derivation source. The eight LVM profiles were likewise all read successfully; their names or template comment prefixes do not establish unchanged installation contents.

No UNKNOWN row is promoted to a textual gap merely because an origin or historical comparison is missing. No Section 8.5 design question is treated as a gap.

## Completion

The verification script confirmed 43 matching input/output IDs, each once, fifteen permitted decision labels, valid sentence IDs, six fields, word limits, and existing raw evidence references. Counts are in `part-talos.done`. After verification, only Section 2 of `PROTOCOL.md` was read. No row has GAP-NONE or GAP-TWO, so `meaning-talos.tsv` contains only its required header. The classification table was not changed after verification. Frozen SHA256: `52547b7ef62adeb2ab62d0d25e0dbb9815bea27cdca3c5c112026b21d1622767`.

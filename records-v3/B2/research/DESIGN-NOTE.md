# Builder research input

Recorded 2026-11-22 UTC. No probe, VM, build, or implementation acceptance was performed in this research subtask. The fixed text and numbered sentences, current channel/design reports, every top-level review and both fixes were read. `variants.json` preserves all 88 rows and separates the published verdict from unsettled review obligations. All paths in source references are relative to the night record.

## Decision needed in implementation, not in the text

The published B1 inventory is 8 CLOSABLE, 77 UNKNOWN and 3 TEXT-OPEN, with neither removal-only nor not-closable variants. REVIEW-B1-3 remains unsettled. Its finding 3 challenges the scope of all eight mechanics requirements; findings 1–2 additionally challenge interpreted-code revocation and broker-dependent service reactivation. Consequently none of these eight labels authorizes a whole-channel closure claim. This note applies the stricter review without editing B1 or inventing a textual rule.

## Exact eight published CLOSABLE controls

The source identifiers M1–M14 below are positional labels for the bullets in `../../B1/raw/mechanics-sources.md`, which lacks explicit labels. They are not experimental evidence.

| Variant | Named control to implement | Evidence and precise limitation |
|---|---|---|
| M1.01 | Keep preparation inaccessible; never report preparation as completed application | M3 [atomic deployments](https://ostreedev.github.io/ostree/atomic-upgrades/) and M4 [deployment](https://ostreedev.github.io/ostree/deployment/). Preparing a tree does not activate live rules/accounts. |
| M2.01 | Immutable exact generation; checked file and directory fsync; durable boot selector before success | M1 [fsync](https://man7.org/linux/man-pages/man2/fsync.2.html), M2 [rename](https://man7.org/linux/man-pages/man2/rename.2.html), M3–M4 above. Old-or-new crash consistency is weaker than booting the exact reported generation. |
| M3.01 | Failed or cancelled inert preparation leaves old generation and authorities unchanged | M3–M4 above. Only failures before live activation are covered. |
| M4.01 | Terminate descendants and mapped/open holders, revoke launch authority; wait for absence or reboot | M5 [cgroup v2](https://docs.kernel.org/6.12/admin-guide/cgroup-v2.html), M6 [systemd.kill](https://www.freedesktop.org/software/systemd/man/257/systemd.kill.html), M7 [unlink](https://man7.org/linux/man-pages/man2/unlink.2.html), M8 [mmap](https://man7.org/linux/man-pages/man2/mmap.2.html). REVIEW-B1-3: killing is not interpreted-code restart denial. |
| M4.02 | Authorize only current declaration membership, never merely a surviving name, cache or old signature | `../../B1/raw/install-sources.md` E3/E10/E18 and M7–M8. REVIEW-B1-3: executable aliases can be gated with N; retained script bytes remain unsafe through uncontrolled interpreter reads. |
| M4.03 | Remove uncovered activation edges, effective rules and tasks | `../../B1/raw/install-sources.md` E15–17/E20; M9 [systemctl](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html), M11 [nft](https://www.netfilter.org/projects/nftables/manpage.html). REVIEW-B1-3: withdrawal of a fixed graph only; preventing recreation still needs the broker. |
| M4.04 | Compute residual dependency coverage; remove only uncovered contributions | S2.4-4 and `../../B1/MECHANICS-research.md`. Coverage must include actual files, processes, activators and rules, not package names alone. |
| M5.01 | Finite typed-line validators compare actual content, permissions, state and defaults; separately inventory extras | M9 above, M10 [nmcli](https://networkmanager.dev/docs/api/latest/nmcli.html), M11 above; `../../B1/raw/install-sources.md` E15/E20. Full P1/P2 is not established by validating a finite subset. |

Other positional labels: M12 capabilities(7), M13 release notes, M14 editor package installation. REVIEW-B1-3 finding 5 explains why these positional references must be stated explicitly. Its publication-hygiene finding concerns a B1 file; do not copy that validation script into the new recipe.

## Smallest credible implementation direction

Use a fresh minimal Linux VM with pinned artifacts, a small explicit schema, one broker, and a limited admitted program set. No source reuse from another testbed is needed. Existing immutable image/generation machinery and system tools should perform storage and effective-state operations; new code should translate finite declaration lines, serialize operations and compare actual state. Unsupported manager operations can refuse. A refusal is not evidence that the six required ordinary actions work: installation, system update, Wi-Fi, Bluetooth, browser and document editing each need an implemented path.

A root-owned directory should contain the complete declaration, including exact source digest/version for all executable closure and explicit defaults for every non-file field. A base-system line may cover a pinned manifest, but that manifest must enumerate its installed files, permissions, code, built-in managers and relevant state. It cannot silently exempt a shell, startup script, account, timer, open port or guest-access key. Saved networks and pairings need real backend-readable representations; without radios, report not tested on hardware.

A restricted command dispatcher can offer recorded program invocations and broker operations without exposing an unrestricted interpreter. It is a design choice, not proof that command input is exempt code. Arbitrary host interpreters require complete code-input mediation; if that is not built, mark their variants NOT CLOSED. Removing or refusing an unsupported optional route is an implementation choice, not a B1 finding that removal is universally necessary. Do not replace required ordinary work with refusal.

### Native execution gate

[Kernel IPE documentation](https://docs.kernel.org/admin-guide/LSM/ipe.html), consulted for this task, documents automatic native execution/mapping checks and immutable dm-verity/fs-verity content. Select only the active generation's digest in policy, not every signed generation. Verify actual kernel configuration and enabled LSM before claiming it exists. IPE states: “IPE cannot verify the integrity of anonymous executable memory”. Its interpreter-file limitation is separate. Thus noexec alone, writable-path filtering, an allowed loader executable, or a package database is insufficient.

Anonymous execution, executable memfd, writable/executable aliases, foreign syscall ABIs, ptrace/process memory access, namespace/mount changes and inherited descriptors need additional controls. A mandatory launcher must cover every ordinary user entry and child path. A control attached only to the documented run command is bypassable by a second session or executable path unless those are also constrained. Root general-purpose breaking need not be prevented, but root built-in tools retain the mediation obligation.

### Mandatory interpreter code input

[Executability-check documentation](https://docs.kernel.org/userspace-api/check_exec.html), consulted for this task, recommends interpreter integration; its flags do not independently enforce an unmodified evaluator. Exact source quote: “All files that contain executable code, from the point of view of the interpreter, should be checked.” File admission must bind the checked immutable descriptor to consumed bytes. Argument code, stdin, heredocs, environment functions, imports, editor macros and embedded interpreters each remain inputs.

[Landlock documentation](https://docs.kernel.org/userspace-api/landlock.html), consulted for this task: “Landlock empowers any process, including unprivileged ones, to securely restrict themselves.” It is a conditional self/inherited-domain primitive, not an automatically imposed selective interpreter policy. Blanket inherited read-denial also blocks document editing. Files opened before restriction and non-file inputs do not become safe merely because subsequent opens are denied.

C7.24 is decisive for an honest limit: a recorded arbitrary own-rights script can interpret instructions through its own loops without eval/import hooks. Instructions may arrive through stdin, argv, environment, inherited FDs or IPC. If unrestricted input plus arbitrary dispatch remains, record NOT CLOSED and the exact entry path. This is a testbed limitation unless the separate definition-only conditional argument applies; it is not a universal impossibility result.

### Built-in management, including root

The actual package/account/service/network/firewall/container backends and their APIs must translate through the broker or refuse. A PATH wrapper does not constrain direct absolute paths, alternate roots, libraries, D-Bus, transient units or root options. Either eliminate unsupported backend entry points from the admitted closure or impose mandatory domain transitions and mutation permissions. The broker alone receives authority to change the finite required state. An installable backend hidden under another name remains a backend; root invoking it is not automatically breaking.

Runtime ports need separate enforcement even for admitted binaries. [Seccomp documentation](https://docs.kernel.org/userspace-api/seccomp_filter.html), consulted for this task: “System call filtering isn’t a sandbox.” A default deny of listening operations in ordinary workloads, with narrowly declared service exceptions, is simpler to examine than dynamically accepting arbitrary ports. It must cover implicit listen binding, inherited listening FDs, alternate ABIs and IPC delegation. A firewall dropping packets does not by itself prove absence of an open listening port.

### Durability and failure

The transaction state machine should distinguish staging, activation, verified current state and reported success. Flush payload files and their directories; durably bind selected declaration to the boot/recovery selector. [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html): “an explicit fsync() on a file descriptor for the directory is also needed.” Check flush errors. Immediate power loss after success must boot the selected exact declaration and reconstruct rules, accounts, services and other runtime state before exposing ordinary sessions.

[Atomic deployment documentation](https://ostreedev.github.io/ostree/atomic-upgrades/) promises “either the old system, or the new one.” That is insufficient after success, when only the new reported state satisfies S3-5. Reporting failure after some live changes also requires restoration of the prior declaration. A durable commit immediately before printing has a no-report crash window; record the report protocol and how recovery chooses a declaration rather than pretending rename solves this observation problem. A failed restoration or unsupported radio replay is a known gap, not a successful apply.

For removal, discard all active executable authorities, stop all holders and activators, then read back. Kernel cgroup documentation states: “Killing a cgroup tree will deal with concurrent forks appropriately and is protected against migrations.” This terminates a controlled subtree; it does not stop a process that escaped before membership was enforced, or prevent later script re-execution. Keep closure claims bounded to measured coverage.

## Conservative implementations of TEXT-OPEN cases

- C7.18: require generated own-rights executable cache bytes to be declared before execution, or suppress that executable cache path. State which is implemented; do not settle exemption priority.
- C7.21: record partially confined modules and their granted host directories/rights before running them. Do not call all restricted APIs equivalent to the expressly exempt browser/VM examples.
- C10.4: treat the editor's package installer as mediated even under root, or refuse that installer while preserving document editing. Do not use the breaking exclusion to excuse a root installation bypass.
- Q2 is outside the 88 rows. An explicit finite declaration avoids dependence on mutable external expansion without deciding whether the text permits every other form.

## Evidence to collect in the development self-test

Use development inputs only. Before each unanswered implementation probe, record expectation and source-based reason for the probe. Each CLOSED row needs a concrete mechanism and evidence path; an unavailable variant is a refusal/removal observation, not a successful workflow. Full-R rows also inherit activation, removal, runtime-port and failure obligations. Verify actual machine state, not the just-written declaration. Compare checksums and permissions of every contributed file, service enabled state and unit checksum, complete account tuple, and effective rule text across two clean installations. Hardware-only exceptions cannot excuse random IDs, host keys or timestamps in declaration-required fields.

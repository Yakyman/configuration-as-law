# Implementation choices

Source32 adds static exact-AppImage overrides in the original reader component.
Matching archive digest and original target checksum are required. The package
provides replacement bytes/modes for the Neovim0.10.4 binary, Lua loader and entry.
The entry fixes VIMRUNTIME to this archive's original runtime. The optional Lua
disk bytecode cache is disabled; discovery and in-process caching remain usable.
File/code readers enforce the same opened-descriptor policy as native readers.
No arbitrary AppImage is silently patched. Last-owner removal deletes the entire
extracted tree. Additional requirement: saved Neovim Vimscript/Lua/key/Ex inputs
must be recorded; typed/pipe/data controls remain distinct under REVIEW.md R1.

Source31 extends the static native reader manifest to13 original Git ELF targets.
The source-built Git configuration parser checks opened descriptors for aliases,
credential/filter/tool sections and the executable keys enumerated in the original
component's git-code-policy.h. Broad sections include ancillary values: their
whole configuration must be recorded. Built-in writes of these keys are refused
in confined sessions. Typed -c/environment settings and repository data remain
available. This is an additional declaration constraint, not a claim that all
other Git setting keys are classified. Original symlinks and removal ownership
remain unchanged. Component30's prior executable bytes are retained exactly.

Source26 supplies one confos-initramfs data package per supported snapshot, with
version VERSION+TIMESTAMP. It builds in an empty root from the original archives
selected by that snapshot's committed component lock, using its native depmod
and cpio. Authored early-init is the only non-Debian code input. Directories use
0755, module metadata 0644, ownership 0:0 and fixed timestamps. All three archives
remain on the disk for update availability; only the active one is unpacked.
This is additional base component content and a fixed placement convention, not
an installed-system snapshot or a recording tool. The running kernel must match
the packaged initramfs release. Dynamic declaration forms, disk identities and
general Understanding remain separate obligations.

Source25 reserves base account/group names root, _apt, wheel and nogroup; it
requires unique UIDs other than0/42. Numeric IDs are ASCII in0..4294967294, and
native account fields cannot contain colon/control separators. Shell paths must
be absolute without ..; homes remain immediate /home children. These are additional
declaration restrictions to prevent duplicate native identities and malformed
passwd entries. Boot checks native account lookup before readiness. The duplicate
_apt failure is in records/account-p2-probe.log; the repair regression passed in
records/accounts-0.25.log, including native lookup, key login and removal.

Source24 restricts both hostname forms to1..64 ASCII letters/digits/dots/hyphens,
starting with a letter or digit. It rejects disagreement between hostname and its
kernel.hostname sysctl alias; either supplies the hosts entry and hostname file,
with base default confos on removal of both. These are additional declaration
constraints. Release23's unchecked native hostname command reported readiness
after failed assignments; boot preparation now checks execution and actual value.
Evidence: records/hostname-p2-probe.log. The repair regression passed rejection,
64-character names, aliases and removal (records/hostname-0.24.log).

Source23 adds the genuine confos-boot data package. Its pinned GRUB input closure
comes from snapshot20261123T000000Z and is unpacked into an empty build root;
native grub-mkstandalone runs under rootless chroot with fixed time/configuration.
This boot release remains fixed across the three Debian update snapshots. Clean
builds copy the packaged EFI program; they do not use the host's GRUB. The worker's
2.12-9+deb13u2 was absent from the selected snapshot; the locked snapshot provides
2.12-9+deb13u4 (records/boot-package-first.log, boot-package-prototype.log).
It also stops advertising optional Flatpak/Podman/pip/npm commands without their
native packages: the private broker programs are packaged, and their public links
are generated only with the native executable present. These link bindings remain
a D3 obligation. An updated outside collector exposed five errors from absent
backends in the first23 candidate; its evidence is retained separately.

Source22 packages query/run brokers under /usr/lib/confos/commands, with fixed
/usr/local/bin links. Native Debian executables are not copied or overwritten.
Session/sudo command lookup selects the brokers; direct native entries are denied.
Only the immutable private broker paths receive the privilege transition, so a
declared replacement of a /usr/local/bin link does not inherit broker privileges.
The Python pip module entry remains an explicit confos-runtime package replacement.
This changes absolute command paths as documented in INTERFACE.md; it is an extra
interface restriction and a partial D3 repair, not a general saved-code solution.

| Date UTC | Choice | Reason / requirement beyond the text |
|---|---|---|
| 2026-11-24 | Debian 13 package payloads; no installed distribution used as a base | Start with empty root; add only declared packages and dependency closure |
| 2026-11-24 | Pinned snapshot; exact versions; no maintainer scripts | Deterministic package bytes and avoid generated installation state |
| 2026-11-24 | Read-only squashfs root, separate noexec material | Section 8.5 mechanism choice; insufficient by itself for interpreted saved code |
| 2026-11-24 | Apply ends with reboot | Eliminate former processes on removal; report success only on new boot |
| 2026-11-24 | Numeric account IDs, explicit shell, groups and home | Additional declaration requirements for Understanding and Reproducibility |
| 2026-11-24 | UEFI boot from disk | No external kernel or initramfs in boot command |
| 2026-11-24 | Person edits text; no command writes lines | Required by task; S8.3-7 compatibility question tracked separately |
| 2026-11-24 | Minimal root service supervisor; immutable JSON descriptors | Service argv and enabled state are declared; restart policy is a base default. Native systemd user timers are available from 0.12. |
| 2026-11-24 | Firewall rule lines restricted to one input-chain rule | Reject includes and multiple statements; order by name; accepting chain is a base default |
| 2026-11-24 | File source paths relative below declaration directory | Carry source bytes into the data partition for subsequent apply; checksum verified |
| 2026-11-24 | AppArmor domain for SSH and services; explicit trusted apply transition | Kernel mechanism under Section 8.5; root built-in mutations must not gain administration authority |
| 2026-11-24 | File targets limited to home, local programs and user configuration subtree | Protect application runtime/libraries; additional declaration restriction |
| 2026-11-24 | Fixed helper PATH, isolated interpreter, cleared environment | Do not let ordinary environment variables change the privileged apply program |
| 2026-11-24 | From 0.14, unchanged Debian payloads preserve archive numeric UID/GID; generated objects default to 0:0 | Replaces the earlier all-root normalization, which contradicted package metadata. Account home ownership is set to its declared UID/GID at boot. |
| 2026-11-24 | libc6-i386 loader links materialized from its shipped postinst's fixed usr-merge targets | Allows the recorded 32-bit package to execute without arbitrary maintainer scripts. |
| 2026-11-24 | Complete explicit PAM sudo/sudo-i and deny fallback policies | Maintainer scripts are not run; package fallback includes must not depend on absent generated files. Wheel remains the sudo authorization rule. |
| 2026-11-24 | 0.16 exact declared sudoers.d files, restricted names/mode, no further includes, native validation | Enables native sudo-rule removal checks; restrictions prevent silently ignored filenames or indirect mutable policy inputs. Failed candidate staging is discarded. |
| 2026-11-24 | 0.17 root process inspection capability plus AppArmor read/readby, without trace/tracedby | Allows native cross-account process-file inspection while retaining denial of debugger attachment and process-memory access. |
| 2026-11-24 | Full pinned base closures for three committed snapshot states | Enables T0/T1/T2 with deterministic component versions; other snapshots require a new published lock. Explicit package lines cannot conflict with the base lock. |
| 2026-11-24 | Generation-local kernel and initramfs; atomic boot.cfg selection | One durable selection must choose matching kernel, modules, initramfs and root. No success is reported before that generation boots. |
| 2026-11-24 | Deterministic CA bundle and LibreOffice registry-default copy | Perform explicit byte-derived installation steps needed for ordinary work, without running arbitrary maintainer scripts. |
| 2026-11-24 | Wheel-only pip, no implicit pip dependencies or bytecode; integrity-locked npm ci, lifecycle scripts disabled | Additional input restrictions; native installers assemble immutable payloads in a chroot. Other language-package workflows are not implemented. |
| 2026-11-24 | npm commands prefixed npm- | Avoid collisions when Python and npm packages expose the same command name. |
| 2026-11-24 | 0.15 native pip/npm installation only in apply; fixed direct inspection, no npx/venv or session access to private installer modules | Prevent the tested built-in installer mutations, including root calls and direct private-module entry. This does not mediate arbitrary downloaded or copied interpreter implementations. |
| 2026-11-24 | Random devices allow entropy writes as well as reads | Dropbear mixes entropy into the random device; repeated denied writes obscured useful audit diagnostics. |
| 2026-11-24 | Immutable home subtrees, not just their leaf files | Fix observed ordinary-user rename of a declared file's ancestor. Material in such subtrees is hidden while managed, not removed; use separate source/material directories. |
| 2026-11-24 | Empty immutable shell/SSH startup and git defaults | Prevent unrecorded automatic startup changes; exact file lines can replace defaults. This does not solve arbitrary saved interpreter input. |
| 2026-11-24 | Account home immediately below /home; explicit build umask 022 | Additional pathname restriction simplifies stable home mounts; permission defaults must not depend on the build host. |
| 2026-11-24 | Read-only nft privilege broker; fixed sudo secure_path | Allow independent native ruleset inspection without granting native mutation authority. |
| 2026-11-24 | Single-file C compile line, restricted GCC options, fixed source path/time | Additional declaration form for repeated source edits; compiler packages must be declared. No compiler writes declaration text. |
| 2026-11-24 | Temporary privileged executable staging bind | Native installers need executable staged tools during apply; sessions cannot access this bind, write staging or use chroot. Mutable home/state retain noexec. |
| 2026-11-24 | Flatpak bundle bytes plus exact ref/OSTree commit; explicit runtime lines | Development 0.9: reproducible input selection without following a changing remote head. Native bundle export is an existing tool; no recorder generates declaration lines. |
| 2026-11-24 | Read/run Flatpak entry and immutable system store | Development 0.9: installation occurs only in staged apply; native Flatpak remains the installer and launcher. Complete P4 mediation and reproducibility are not claimed. |
| 2026-11-24 | Ordinary-account Flatpak launch, fixed empty user store and one immutable-store execution rule | Avoid granting root launches an unconfined entry; exclude user overrides; per-file policy exceeded AppArmor's DFA state limit on the full runtime. |
| 2026-11-24 | Assembly-time AppImage extraction and immutable launcher | Development 0.10: content hash names the exact release, payload shared by hash; no runtime FUSE/extraction. Supports type-2 ELF64 little-endian images with squashfs at the section-table end; xattrs omitted. |
| 2026-11-24 | OCI archive and image configuration digests; account-specific rootless Podman | Development 0.11: native boot-time loading preserves namespace UID/GID mappings without build-host IDs. Stores are volatile and rebuilt before APPLIED. UID range 1..60000, 65536 subordinate IDs per account. |
| 2026-11-24 | Read-only container roots and a restricted native command entry | Development 0.11: no network, extra mounts, capabilities, cgroups or root launch. Image entrypoint/environment/user remain effective. These are additional implementation restrictions, not deductions from the hypothesis. |
| 2026-11-24 | Optional native systemd PID 1 and user managers with fixed unit paths | Development 0.12: exact person-authored service/timer inputs, deterministic enable links and AppArmor service drop-ins. No distribution generators or unit search paths; machine-id fixed by the base recipe. |
| 2026-11-24 | Mode-000 manager sockets and privileged read-only native query entry | Development 0.12: a real systemd-run transient creation bypassed pathname confinement. Remove DAC override/search from sessions including sudo; delay SSH until sockets are protected. This limits root access to other users' private files. |
| 2026-11-24 | C.UTF-8 sessions with pinned libc-bin; explicit runtime modes and fd links | Development 0.13: repair native tmux and process substitution without a locale-generation script. Dropbear -e passes only a fixed server environment. |
| 2026-11-24 | No generated nft rule comments | Development 0.13: native effective rule text must match the person's text; line identity remains in the declaration. |
| 2026-11-24 | 0.18 native LinuxGSM installation/update from checksum-pinned source/game/configuration bundles | Additional linuxgsm line names account, workspace and release. Native installers run in staging without privileges; no installed-file recorder creates inputs or declaration lines. Only the two documented launcher releases and ET 2.60b are implemented. |
| 2026-11-24 | Game code is immutable but owned by its declared account; logs, locks and scratch records are volatile | Native ownership checks require caller ownership. Exact native templates and a read-only launcher-cache bind avoid startup code downloads. Native direct updater may exit zero despite read-only errors; observed code checksums, not its message, establish whether it changed code. |
| 2026-11-24 | 0.18 root DAC read/search capability, without DAC write override | Allows the outside collector to read private game records. Native user-manager mutation and private-file write probes still fail; directory traversal does not grant socket write access. Replaces the earlier restriction on root reading private records. |
| 2026-11-24 | 0.19 canonical read-only systemctl arguments and explicit absent-user-manager error | Native inspection accepts property/type filters, escaped unit names and separators without exposing mutation commands. Fixes the outside collector's units_show error. |
| 2026-11-24 | Queue clean disk assembly and boot at the shared six-slot limit | A temporary full pool no longer aborts a completed payload build. Waiting does not acquire extra VM capacity. |
| 2026-11-24 | 0.20 genuine confos-runtime Debian data package, built from authored source/defaults with fixed permissions and no maintainer scripts | Lets a declaration-only reader inspect fixed runtime/default package bytes. Avoids copying source-extraction modes into the installed programs. Component locks name it; its archive remains on the immutable system partition for apply. |
| 2026-11-24 | Unpack only the current APT solver result, with confos-runtime last | A reused download cache otherwise retained a removed package in a clean build. The runtime package's Replaces metadata and final position specify which fixed defaults override Debian payloads. |
| 2026-11-24 | Fixed mode0644 for disk-side declaration/input copies; no unused installed packages.json ledger | Source checkout permissions must not alter installed code or the retained apply inputs. Native dpkg status remains available; the removed JSON ledger was not read by the runtime. |
| 2026-11-24 | 0.21 optional explicit UID:GID on file lines, old form retaining 0:0 | Supplies directly stated file metadata for D5 without recording installed objects. Values are unsigned numeric IDs except the reserved all-ones value; sudo-rule files require 0:0. |

Build documentation consulted: [mmdebstrap manual](https://manpages.debian.org/trixie/mmdebstrap/mmdebstrap.1.en.html)
and [Debian snapshot usage](https://snapshot.debian.org/). Snapshot indices fix the
dependency source; payload extraction avoids running Debian maintainer scripts.
Confinement syntax: [AppArmor profile manual](https://manpages.debian.org/trixie/apparmor/apparmor.d.5.en.html).
Boot selection: [GRUB embedded configuration](https://www.gnu.org/software/grub/manual/grub/html_node/Embedded-configuration.html).
Installation behavior: [CA certificate bundle](https://manpages.debian.org/trixie/ca-certificates/update-ca-certificates.8.en.html),
[pip install](https://pip.pypa.io/en/stable/cli/pip_install/),
[npm ci](https://docs.npmjs.com/cli/v9/commands/npm-ci/).
Compilation environment: [GCC environment variables](https://gcc.gnu.org/onlinedocs/gcc/Environment-Variables.html).
Flatpak bundle/install behavior: [native command reference](https://docs.flatpak.org/en/latest/flatpak-command-reference.html).
Exact commit fetch: [OSTree pull](https://ostreedev.github.io/ostree/man/ostree-pull.html).
AppImage format/extraction: [running AppImages](https://docs.appimage.org/user-guide/run-appimages.html).
Containers: [Podman save](https://docs.podman.io/en/stable/markdown/podman-save.1.html),
[Podman run](https://docs.podman.io/en/latest/markdown/podman-run.1.html),
[version 5.4.2 troubleshooting](https://github.com/containers/podman/blob/v5.4.2/troubleshooting.md).
User managers: [native v257 startup checks](https://github.com/systemd/systemd/blob/v257/src/core/main.c),
[unit search paths](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html),
[manager environment](https://www.freedesktop.org/software/systemd/man/latest/systemd.html),
[setpriv capabilities](https://manpages.debian.org/trixie/util-linux/setpriv.1.en.html).
SSH environment: [Dropbear -e](https://manpages.debian.org/trixie/dropbear-bin/dropbear.8.en.html).
Native process inspection: [proc_pid_exe](https://man7.org/linux/man-pages/man5/proc_pid_exe.5.html)
and [AppArmor ptrace rules](https://apparmor.dev/man/apparmor.d/).
# Saved-code development choice, 2026-11-24

Introduced in27 (not released0.26): source-level checks distinguish code-file readers
from data readers. In confined sessions, an opened regular code file must be on a
read-only executable mount; its mode need not contain an execute bit. Check the
descriptor, not a pathname, and recheck parser refills where input can be rebound.
Pipes and typed commands remain allowed. Only the kernel-reported unconfined
boot/apply context bypasses this policy. No declaration lines are written by it.
See CODE-READERS.md and records/*-code-routes*.log for coverage and open routes.
This is an S8.5 mechanism choice, not a new definition or an impossibility claim.
Native Bash/Python/Perl are source-built from pinned Debian source archives and
supplied in the original confos-code-readers package, including matching Python
extensions. Private installer namespaces supply proc/dev so the reader can inspect
kernel confinement state. util-linux is consequently a named base component.
Release28 applies the same checks to BusyBox ash/sh, awk and sed program inputs,
using its Debian static configuration. All existing aliases use the new executable.
Release29's original reader package carries optional binaries as gzip data and
a manifest naming activating package, target, mode and raw hash. Assembly applies
an entry only if that package is selected. This is a documented deterministic
package-composition rule, not an inventory of an installed root. The base owns
mawk already; removal of an added mawk line leaves that owner's contribution.
Removal of GNU sed restores the separately base-owned BusyBox sed alias. GNU make
uses sealed anonymous memory for checked stdin and does not unlink --temp-stdin
paths. Typed/pipe inputs and explicit data routes are reported separately under R1.

Release30 extends the conditional manifest to nodejs and libnode115. Code readers
check the opened descriptor; package.json resolver configuration also requires
immutable recorded bytes. This additional requirement is separate from ordinary
JSON data imports and fs reads. Native enforcement binding properties are read-only.
The library replacement covers its native loaders when used by another executable;
arbitrary embedding data-to-code APIs are not claimed closed. Debian's shared build
uses pinned private library dependencies and external builtin JS inputs mounted
read-only in a private build namespace. No build modifies the worker system.
Additional Node startup readers obey the same rule: snapshot builders/configs/blobs,
native environment files and policy manifests. A generated snapshot must acquire
its own recorded file line before loading it. Explicit material data reads stay
separate. The first native30 snapshot probe exposed omitted readers; its failures
are retained, and30 is not handed over before the expanded tests pass.

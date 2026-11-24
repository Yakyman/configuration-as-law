# Implementation choices

S8.3-7 recording choice (from34): built-in tools edit only the primary
requested text, never the declaration in force. They do not apply automatically.
Root authority is required, as for existing direct edits. Recording and application
share a lock; manual concurrent editors must serialize their own edits. Recording
preserves unrelated lines/comments, atomically replaces and fsyncs the text and
directory, and reports RECORDED; only later APPLIED reports running-state success.
APT metadata/simulation uses a private temporary directory, an empty status,
the pinned archive map and the declaration's roots. No installed inventory is
read. Up to 0.48 the original native executables were moved to fixed helper
paths and the ordinary paths entered the recorder; from 0.49 every package file
keeps its path and bytes and the recorder is reached by name (Revision 49 below).
Native APT's simulation does not write declaration syntax, so the adapter writes
the line. This is implementation-written recording under the plan's9.3 rule.

| Tool | Request | Line written | Result | Regression log |
|---|---|---|---|---|
| apt, apt-get | install NAME[=VERSION] | package NAME VERSION | records | records/recording-apt-0.34.log |
| apt, apt-get | remove/purge NAME | remove package NAME line | records unless another line/base still requires it | records/recording-apt-0.34.log |
| apt, apt-get | arbitrary -o/-c, local debs, patterns, foreign arch, target suites, dependency/base removals, other mutation verbs | no supported request mapping | refuses | records/recording-apt-0.34.log (representative invalid/base/native tests) |
| pip | install NAME[==VERSION]... or local wheels | pip NAME VERSION SHA256 SOURCE for each resolved wheel | records from35 | records/language-recording-0.35.log; local-wheel preparation language-recording-bare.log |
| pip | uninstall [-y|--yes] NAME... | remove named pip lines | records unless still required by another pip line | records/language-recording-0.35.log |
| npm | install -g NAME[@VERSION]; uninstall -g NAME | npm NAME VERSION SHA256 LOCK; remove that line | records from35 | records/language-recording-0.35.log |
| pip, npm | ranges/tags, editable/source builds, requirements files, VCS/URL roots, alternate index/registry, user/target/prefix overrides, arbitrary flags; npm scoped names/per-project installs/multiple roots | unsupported current grammar or resolution policy | refuses | language-recording-prep.log; records/language-recording-0.35.log (representative guest requests) |
| Flatpak | install --bundle LOCALFILE; uninstall ID or REF | flatpak REF COMMIT SHA256 SOURCE; remove line | records from36; runtime dependency guard | flatpak-recording-native-final.log; records/flatpak-recording-0.36.log |
| Flatpak | remote-add, named-remote install, user installation, other flags/verbs | no current request mapping | refuses | records/flatpak-recording-0.36.log (remote/native-helper controls) |
| Podman | [--account USER] pull/rmi REGISTRY/NAME[:TAG] | container USER NAME CONFIG_SHA ARCHIVE_SHA SOURCE; remove line | records from37 | records/podman-recording-0.37.log |
| Podman | short names, digest/transport forms, multiple images, tag refresh, private authentication, other flags/verbs | unsupported request resolution | refuses | records/podman-recording-0.37.log |
| hostnamectl, timedatectl, sysctl | set-hostname VALUE; set-timezone UTC/Etc/UTC; -w KEY=VALUE... | setting NAME VALUE | records | records/configuration-recording-0.38.log |
| systemctl | [--user] enable/disable existing declared NAME... | change service/user-unit STATE | records; authorized root required before query escalation | records/configuration-recording-0.38.log |
| useradd, usermod, userdel | supported field requests, deterministic new-account defaults, append groups; delete unreferenced account | complete account line, field edits, removal | records | records/configuration-recording-0.38.log |
| nft | add rule inet confos input tcp dport PORT accept/drop; delete rule inet confos input handle HANDLE | deterministic named rule; remove uniquely mapped rule | records from43; nine immediate post-APPLIED cuts passed | NFT-RECORDING-DRAFT.md; records/nft-ed-0.43.log |
| nft | other expressions/tables/chains, command files, unknown handles, ambiguous ownership, noncanonical applied text | unsupported mapping | refuses | exact restrictions in NFT-RECORDING-DRAFT.md |
| visudo | [-f /etc/sudoers.d/NAME]; --remove [-f /etc/sudoers.d/NAME] | file PATH 0440 0:0 SHA SOURCE; remove that row | records from44; canonical gates passed | records/tools-0.44.log; records/visudo-editor-0.44.log; VISUDO-RECORDING-DRAFT.md |
| visudo | generated /etc/sudoers, includes, other edit flags/targets | no supported request mapping | refuses; native check/version/help stay confined | records/tools-0.44.log |
| configuration tools | unsupported flags/timezones, unknown units, account rename/password/home moves, userdel -r | some representable requests still have no adapter | refuses; S8.3-7 incomplete | CONFIGURATION-RECORDING-DRAFT.md; representative refusals in records/configuration-recording-0.38.log |
| nmcli | connection add explicit static Wi-Fi properties; connection modify id NAME ssid/PSK/address; connection delete id NAME | network NAME SHA recorded-inputs/network-SHA.json; remove row | records from45; separate apply | records/radio-recording-0.45.log |
| nmcli | device wifi connect, DHCP, passphrases, other radios/properties | no supported mapping | refuses with exact representability reason | RADIO-RECORDING-DRAFT.md |
| groupadd; at, loginctl enable-linger, localectl, modprobe, mount, ip, systemctl set-property, systemd-run, dpkg -i, chpasswd | mutation | no current request mapping; group has no standalone kind | refusal paths; unsupported recording | previous channel logs; S8.3-7 unfinished; not a claim about every option |
| crontab -u; apt-mark hold/auto/manual; dpkg selections | native store mutation | no line form or recorder | write denial; canonical42 verification in STATE | private proof: NATIVE-CONFIG-RESULTS.md; integrated evidence: records/readers-0.42.log; original39 failure retained |
| curl automatic .curlrc | automatic saved setting | file row required for native saved config input | guarded from42; transfer may continue without refused config | records/readers-0.42.log; curl-config-draft.md records exact-version scope |

Development35 language requests use native binary-only pip download or native npm
lock-only install with exact root saving and lifecycle scripts disabled. Public
PyPI/HTTPS npm registry are fixed resolver choices. ConfOS line syntax is written
by the adapter; npm's lock bytes are written by npm and never rewritten. Existing
pins constrain resolution; repeated bare requests retain their exact input bytes.
Every existing wheel/lock checksum and identity is validated before a new request;
offline native pip resolution verifies existing wheel dependencies. Pip dependencies
become explicit independent lines, not a hidden owner journal; removing a root
does not remove those lines automatically. Version conflicts fail before commit.
Content-addressed source inputs are fsynced before declaration text. Removal keeps
them as source material, not installed payload. Caught failures remove only newly
created, inode-matched inputs when text was not committed. Abrupt failure before
commit can leave unreferenced source material; it cannot put it in force. No
installation or application success is reported by RECORDED.

No arbitrary hooks/configuration options are forwarded to privileged APT.
Only native/all package names and optional exact versions are accepted. Removal does
not add negative package lines; a dependency/base owner must first be removed by
an explicit edit if the declaration syntax permits it. Remove and purge have the
same immutable-generation effect. Bare names resolve within the selected fixed
archives; an existing explicit version remains pinned until explicitly changed.
From34 T2 additionally names security snapshot20261124T000000Z through original
component archive-sources.json; linux-image-amd64 and its image are6.12.118-1.
The native109-package closure was verified before the clean build, with only
those two kernel pins changed (kernel-security-probe.log).
Native resolution uses the documented [APT simulation mode](https://manpages.debian.org/trixie/apt/apt-get.8.en.html),
which reports planned package operations without carrying them out. Simulation
reads a private empty status plus explicit roots, not the running package state.

Source33 development requires a Flatpak runtime with /usr/bin/sh for its fixed
post-sandbox AppArmor entry. The original component contains the separate app
policy template; only declared non-runtime executable paths are inserted. Its
immutable /usr and /app namespaces are executable, mutable storage is not. Native
reader checks are separately required and are not supplied merely by this profile.
BusyBox vi's automatic .exrc commands require recorded immutable inputs; original
ownership/mode conditions still apply. Typed EXINIT/-c remain permitted.

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

Configuration38 account defaults are derived solely from declaration text; the
complete resulting fields are written. Home material is not removed. Native
queries read applied values. nft recording was added in43 and visudo snippet
recording in44; their later entries state the supported requests and limits.

Reader39 choices: exact ref/commit/bundle/original-file identity gates three
Flatpak runtime overrides; their named component manifest fixes new bytes/modes.
Native repository objects remain intact with exact execution/mapping denials.
Unknown runtime versions are not guarded. Different SDK/compiler configuration
from the original is disclosed; matching original feature/ABI controls are tested
without claiming byte-identical rebuilding of the original binaries.

Radio40 choices: explicit fixture/client/native-bond input rows, fixed virtual
identities, one AP/client, two reciprocal saved keys for mutual authentication.
No automatic pairing or key generation occurs at boot. Exact schema restrictions
and native package versions are validated by radio_declaration/radio_integration.
Read-only native inspection is a fixed root broker. Control isolation includes
both session and Flatpak profiles and private mount storage. Simulated fixture
support does not claim hardware radio support. Network/pairing recorders refuse;
manual edits are the supported route. Canonical logs: records/radio-0.40.log and
records/radio-flatpak-0.40.log; do not infer success before their passing markers.

## Native Flatpak mpv input policy — release41

- Exact app ref/commit/bundle and original-file checks gate three replacements;
  unknown app versions retain their original payloads and are unclaimed.
- Confined regular code input must be on a read-only executable filesystem.
  Record scripts/modules through file rows before native loading; the file's
  descriptor decides, including aliases. Typed pipes and explicit data stay open.
- The original dependency libraries/features/export sets are retained. Historical
  upstream toolchain identity is not established; libmujs DT_NEEDED now names its
  same fixed /app/lib object by absolute path. See MPV-041-DOCUMENTATION.md.
- Source archive contains the guarded prebuilt component and source recipes.
  Recompiling mpv also requires the separately pinned SDK deployment identified
  by its full checksum manifest. This is distinct from a clean ConfOS installation,
  which consumes the shipped named component package.

## Native configuration input policy — release42

- Exact original pdb.py from libpython3.13-stdlib3.13.5-2+deb13u5, gyp input.py
  from gyp0.16.2-2 and curl executable8.14.1-2+deb13u7 gate these new replacements.
  Unknown original bytes fail assembly; no silent replacement/version claim.
- Record pdb .pdbrc, gyp .gyp/.gypi and curl config files with file rows before
  using them as saved program/settings inputs. This applies even to a gyp input
  with no expansion. Missing pdb rc stays harmless; denied/unreadable rc fails.
- Curl automatic config errors are printed but native curl may continue its
  transfer with defaults. The tests require the rejected configuration's actual
  HTTP effect to be absent, not merely a diagnostic. Explicit/nested/stdin config
  routes fail. Explicit data reads and upload/header data remain supported (R4).
- Curl uses the original libcurl and selected dependency packages, not a private
  replacement library. The native build's Kerberos revision differs from the
  guest's security revision; exact guest libraries/archive provenance and feature
  comparison are retained in curl-config-guest-draft-evidence.
- Native store writes through apt-mark, dpkg selections and crontab are refused
  by confinement. Holds, auto/manual flags and crontab requests have no current
  line form; no S8.3-7 recorder claim is made for them. Read queries remain native.
- Unknown gyp/node-gyp copies, Flatpak pdb and other runtimes/readers are outside
  these exact-source changes. Private39 evidence precedes integration; only
  canonical42 logs establish the integrated result. Source archives retain
  exact inputs/licences and component recipes; normal clean installs consume
  the named prebuilt component. Regenerating its composition also needs sealed41
  provenance; source recompilation is a separate operation.

## Revision43 native request and reader choices

- Nft supports decimal TCP destination ports1..65535 and accept/drop only in
  inet confos input. Deterministic line name is nft- plus24 SHA256 digits of
  canonical native text. Repeated equivalent add is unchanged. Handle deletion
  cross-checks native JSON, immutable applied text and unique current ownership;
  repeated deletion before apply is unchanged. A handle absent after apply is
  unknown. No native mutation privilege is given to caller sessions.
- Ed command stdin is executable input even when commands only edit text.
  An existing file row records a saved command stream. Document filename/read/
  write operations remain data; explicit producer pipes follow REVIEW R4.
  Native red retains its original regular launcher and restricted behavior.
  ed-reader-draft.md/metadata retain exact inputs, ABI comparison and native
  build libc u4 versus guest u5 limits; other versions/copies are unclaimed.

## Revision44 request and reader choices

- Visudo invokes the native editor/validator in confos-session. Captured bytes
  are validated through native stdin, before durable declaration commit; no
  editor or editor-selected saved code gains unconfined execution. Complete
  composed policy validation is deferred to apply; an individually valid snippet
  may still conflict with another pending snippet, causing apply to refuse.
- A refused include may have been visited by native visudo and its chosen
  editor first: writable /tmp include material can change within confos-session.
  It is never applied policy; the effective immutable sudoers and declaration
  remain unchanged. The supplementary probe records this behavior explicitly
  (records/visudo-editor-0.44.log); no claim of zero editor-material writes is made.
- Native empty edits preserve content. Explicit --remove states deletion,
  including repeated deletion of an absent row. Inputs already recorded under
  recorded-inputs remain source material after removal; no watcher records them.
- SSH policy checks actual configuration file descriptors, including nested
  Include. The exact original package and replacement payload are pinned in the
  reader manifest. Regular stdin and fd0 aliases are saved input; pipes and typed
  options follow REVIEW R4. Unknown originals fail assembly. The automatic user
  config fixture hits the protected .ssh mount; that is a mount-level refusal,
  not a separate observation of the native automatic reader branch.

## Revision45 Wi-Fi request choices

- A finite nmcli adapter records only the person's explicit request. It neither
  inspects saved radio state nor invokes NetworkManager. The native radio runtime
  continues to use hostapd, wpa_supplicant and BlueZ after declaration application.
- Add syntax: `nmcli connection add type wifi ifname wlan1 autoconnect yes con-name
  NAME ssid SSID wifi-sec.key-mgmt wpa-psk wifi-sec.proto rsn wifi-sec.pairwise ccmp
  wifi-sec.group ccmp wifi-sec.psk RAW64HEX ipv4.method manual ipv4.addresses CIDR`.
  Quote the SSID when necessary. All properties are required, in any order.
- Modify syntax: `nmcli connection modify id NAME ipv4.addresses CIDR`; ssid and
  wifi-sec.psk are also accepted. Delete: `nmcli connection delete id NAME`.
  Repeated equivalent requests preserve declaration bytes. A differing duplicate
  add refuses; use modify. Removing an already absent name preserves the text.
- Existing fixture identity supplies the JSON fixture field; requested SSID/key
  must match that declared fixture. Client address is explicit and distinct from
  the AP. No implicit package installation, DHCP, DNS, gateway, general radios,
  ASCII-external SSID or passphrase conversion is supported. Native device wifi
  connect has no explicit address in this form and is refused. Unknown options,
  unavailable fixture and missing pinned prerequisites refuse before commit.
- Generated JSON inputs are written and synced before the declaration commit.
  RECORDED is pending durable text; separate confos apply is required. Unreferenced
  generated inputs remain material after removal, as for the other recorders.
- Private evidence contains a preserved initial transport failure, then a full
  rerun with bounded retries only for read-only SSH transport failures. Mutating
  requests are never automatically retried. Canonical45 repeats the six-cut
  matrix: three cuts at RECORDED and three at APPLIED, with native radio state,
  exact JSON, repeated requests, ordinary/root authority and unchanged bonds.
  Independent acceptance is still the case party's work.

## Revision46 optional shared-library reader

- Replace only libpython3.13's exact shared-library payload when that package is
  selected. Its original checksum must match; unknown originals fail assembly.
  Remove the package and the optional target disappears. The rest of the reader
  component is unchanged in bytes/modes/links, except its version metadata and
  the one appended override record/payload.
- Use the existing CPython descriptor checks with Debian's builtin module
  selection from debian/rules __post_configure. The initial default shared build
  lacked29 exported builtin initializers and was rejected. The repaired private
  candidate matched exported names/types, data object sizes and needed libraries.
  This is a compatibility check, not proof of every ABI behavior.
- Native file-API saved home/tmp/regular-stdin calls are refused for ordinary and
  root callers; recorded file, typed-string and pipe controls run. Canonical
  two-boot and optional package removal checks are required before handoff.
  Static libpython archives, other Python versions and a custom program that
  reads bytes itself then submits a string remain outside this specific repair.
- Native compilation used the host packages listed in the retained provenance;
  clean ConfOS builds use the pinned prebuilt reader component. No system package
  or live installation was copied as the source of the new runtime payload.

## Revision47 optional shared Perl library

- Apply the existing Perl lexer descriptor checks to the native shared library
  from the pinned Debian5.40.1 source. Replace only the exact original target
  when libperl5.40 is selected; unknown payloads fail assembly. Its removal
  removes the override. Prior46 reader entries remain byte/mode/link identical.
- Use Debian's shared configuration, generated patchlevel header and SONAME.
  Extract DB build dependencies privately and name their search paths explicitly;
  no host package installation. Failed configurations remain in provenance.
- Compare exported names, types, data sizes and native dependencies before
  guest execution. This is a finite compatibility check, not an ABI proof.
- Require ordinary/root home/tmp/regular-stdin refusals and recorded/typed/pipe
  controls, two boots, removal, smoke, updates, archived-source equality and
  outside inventory before handoff. The custom compile/exec reader observed in46
  remains open; these library checks do not establish universal P4.

## Revision48 native dependency version fallback

- Preserve successful default APT resolutions. On native simulation failure,
  retry solver3 with --no-strict-pinning so a named older release can obtain
  compatible dependencies from the same committed archives. All package lines
  and base component versions stay explicit mandatory arguments. Reject any
  solution that omits or changes an explicit request. Use the same solver for
  download and retain the existing exact selected-archive checks.
- This adds no dependency-line requirement and records no inferred line. Native
  APT chooses dependencies; their package line covers them under S8.2-16.
- Original failure and native comparison: SOLVER-PRIVATE.md and
  records/lo-solver-private. Canonical gates include APT recording of Writeru9,
  unchanged pre-apply state, idempotence, pending/applied power cuts, native
  package versions, two document revisions and removal, plus standard gates.
- Existing reader payloads are byte/mode/link identical to47. The saved Basic
  profile-library failure reported in IMPOSSIBLE.md is not repaired by this change.

## Revision 49: package files keep their paths; recording tools are called by name

- Choice (Section 8.5 leaves the mechanism to the system): the recording entry of a
  tool is a file of the runtime package, `/usr/lib/confos/commands/NAME`, linked
  from `/usr/local/bin/NAME`, which precedes `/usr/bin` and `/usr/sbin` in the path
  of a login, of a non-interactive SSH command and of `sudo`. The package's own
  executable stays at its path with its bytes.
- Why: P2, S8.3-2, “Everything recorded in the declaration is in force on the
  computer as its line requires.” Releases 0.34–0.48 moved the package executables
  to `/usr/lib/confos/native` and linked their paths to the recording entries. A
  comparison of the machine with the packages that the lines name then found, in
  every installation, 10 package files missing at their paths, one package link
  changed, and the moved copies as objects that follow from no line.
- Consequence for S8.3-7: a request made through the tool's name is recorded, also
  with superuser privileges. The package executable called by its full path
  (`/usr/bin/apt-get install X`) does not record: the session confinement refuses to
  start it, and nothing changes. `visudo` by full path starts inside the
  confinement and cannot write the read-only system part.
- A way to make the full path record as well without changing the package file
  (a mount over the path in the running system) was not taken: the stored file
  would equal the package while the file in force at that path would not.
- Rows of the table above are unchanged except the column of the request: read
  every tool there as called by name.
- Flatpak reader replacements are bound to ref, commit and the checksum of each
  replaced object, not to one bundle file (two exports of one commit differ as
  files). Requirement on a declaration removed, none added.
- Regressions: records/prepare-paths-0.49.log (package objects compared with the
  downloaded archives), records/other-export-0.49.log, records/recording-apt-0.49.log,
  records/configuration-recording-0.49.log, records/language-recording-0.49.log,
  records/podman-recording-0.49.log, records/flatpak-recording-0.49.log.

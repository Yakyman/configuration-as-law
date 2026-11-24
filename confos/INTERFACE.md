# ConfOS interface, revision 49

Revision 49 changes where the recording tools are, not what they do.

- Every package file keeps its own path and bytes. `/usr/bin/apt`, `apt-get`, `pip`,
  `pip3`, `flatpak`, `podman`, `systemctl`, `hostnamectl`, `timedatectl`,
  `/usr/sbin/sysctl`, `useradd`, `usermod`, `userdel`, `visudo` are the objects of
  their Debian packages and `/usr/bin/npm` is the package's link. The folder
  `/usr/lib/confos/native` no longer exists. Every statement below that original
  bytes "move to `/usr/lib/confos/native/NAME`" or that a `/usr/bin` path "becomes a
  link" describes releases 0.34–0.48 only.
- A recording tool is called by its NAME: `apt-get install X`, `sudo -n apt-get
  install X`. `/usr/local/bin/NAME` is a link to the runtime package's entry
  `/usr/lib/confos/commands/NAME`; `/usr/local/bin` is first in the path of a login,
  of a non-interactive SSH command and of `sudo`. Reply, place of the line and the
  wait are unchanged: `RECORDED SHA256; run confos apply` on standard output, the
  line in `/state/declaration.conf`, then `sudo confos apply` and `confos status`
  printing `APPLIED SHA256`.
- Called by its own full path (`/usr/bin/apt-get install X`, with or without
  `sudo`) the package executable is refused by the session confinement
  (`Permission denied`); it records nothing and changes nothing. The same holds for
  the full paths of the other tools listed above except `visudo`, whose package
  executable stays reachable inside the confinement and cannot write the read-only
  system part. Queries by name are unchanged.
- A `flatpak` line may name any export (bundle file) of a ref and commit for which
  the runtime package carries reader replacements. The replacements are bound to
  the ref, the commit and the checksum of each replaced object; up to 0.48 they were
  bound to one bundle file, and a declaration naming another export of the same
  commit could not be built (`Flatpak reader bundle checksum mismatch`).

No declaration syntax changes. Release gates and observed limitations are in
STATE.md; independent acceptance remains separate.

Revision48 retries failed native package resolutions with APT's all-version
solver. Every explicitly requested version remains mandatory. Successful default
resolutions are unchanged; the same selected solver performs package download.
No declaration syntax or installer-recording protocol changes. Release gates and
observed limitations are in STATE.md; independent acceptance remains separate.

Revision47 extends the saved-file checks to the exact optional Debian
libperl5.40 shared library. Original payload checksums gate the replacement.
The declaration grammar and installer recording/apply protocol are unchanged.
Scope is the tested native perl_parse/perl_run file routes; arbitrary string
readers, static archives and independently supplied libraries remain unclaimed.
Exact provenance: interpreter-inputs/libperl-private/metadata.json. Actual
release gates and independent acceptance status are recorded in STATE.md.

Revision46 extends saved-file checks to the exact optional Debian shared
libpython3.13 library, through an original-checksum-guarded reader override.
The declaration grammar, recording tools and apply protocol are unchanged.
The filename API refuses unrecorded regular input while recorded files, typed
strings and pipes remain available. This covers the tested shared-library API,
not every embedding interface, static archive or independently supplied copy.
Exact provenance: interpreter-inputs/libpython-private/metadata.json; release
gates and evidence are in STATE.md. Independent acceptance remains separate.

Revision45 records a finite nmcli static Wi-Fi request subset into the existing
network line and a checksummed JSON input. It never invokes NetworkManager or
changes a live radio. Success prints RECORDED SHA256; run confos apply. Wait for
confos status to print APPLIED SHA256 before treating the request as in force.
Only accounts already authorized to edit the declaration may record requests.
The request requires an existing simulated radio-fixture and its explicit pinned
packages. Bluetooth pairing remains available by manual declaration lines.
Exact supported properties and refusal limits are in CHOICES.md; guest evidence
and release status are in STATE.md. No declaration grammar was changed.

Revision44 adds visudo recording for one /etc/sudoers.d/NAME snippet per
request (default confos-local). The native editor and validator remain confined.
Successful edits record a file row with0440 root ownership and checksum input;
visudo --remove [-f /etc/sudoers.d/NAME] removes that row. A native zero-length
edit remains unchanged. RECORDED is durable pending text only; confos apply and
APPLIED retain their existing meanings. Invalid/generated targets and includes
refuse; full policy validation is performed at apply. See CHOICES.md for limits.
Exact native OpenSSH saved configuration reads are guarded; typed options and
explicit producer pipes remain available. The original/candidate and ordinary
connection controls are described in SSH-READER-RESULTS.md. Other copies and
versions remain unclaimed. Release status and actual gates are in STATE.md.

Revision43 records a supported native nft request subset as existing rule rows:
sudo nft add rule inet confos input tcp dport PORT accept|drop, and delete rule
inet confos input handle HANDLE when native state maps uniquely to an applied
declared rule. Ordinary authority checks precede native queries. RECORDED means
durable text only; confos apply changes native rules. Other expressions, unknown
handles and ambiguous ownership refuse explicitly. Details: CHOICES.md.
The exact Debian ed1.21.1-1 command reader checks actual regular stdin before
executing commands; recorded input, terminals, pipes and document data remain
available. Its original red launcher bytes/restrictions are preserved. Unknown
original bytes fail assembly. Actual gates/status are in STATE.md; this is not
independent acceptance or a claim about every editor/embedded reader.

Revision42 guards native pdb startup files, gyp main/include files and
curl configuration inputs through their actual opened descriptor. Original-file
checksum preconditions require the exact supported Debian input bytes; a different
original fails assembly explicitly. Existing inherited overrides are unchanged.
Native apt/dpkg/cron stores reject direct writes while queries remain readable;
supported installer requests still record lines and require apply. These denials
do not add hold/auto/manual/crontab line kinds or recorder support. Full scope and
compatibility limits are in CHOICES.md; actual evidence/status is in STATE.md.

Revision41 adds exact native mpv/libmpv/LuaJIT payload overrides for
app/io.mpv.Mpv/x86_64/stable commit
13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc.
No declaration syntax changes. The existing flatpak line still names its original
bundle and commit; the base reader component records the replacement checksums.
Original OSTree object bytes are retained with explicit execution/mapping denials.
Initial Lua/JavaScript files and nested Lua loaders/JavaScript require consult the
actual opened descriptor. Explicit data reads/evaluation and ordinary media remain
available. Other applications/versions and native plugin routes are not newly
claimed by this change. Exact provenance, compatibility limits and tested/pending
controls are in MPV-041-DOCUMENTATION.md and STATE.md. Also allow root to read
the radio readiness JSON for external inventory, retaining all write denials;
source40's one unread-checksum inventory error is preserved in its evidence.

Revision40 adds recorded simulated radios. These rows require the exact
native packages in radio-public-fixture/packages.conf and checksum-pinned files
below the declaration directory. radio-public-fixture/radio-draft.conf is a
public radio-row fragment; combine it with base/snapshot/account/key rows and
packages.conf. Its test keys are intentionally non-secret. The fixture builder
build-radio-fixture-040.py generates complete normal/systemd declarations.

| Kind | Syntax | Sentence | Effect |
|---|---|---|---|
| Fixture | radio-fixture NAME SHA256 RELATIVE_JSON | S8.2-11–13 | Two hwsim radios/AP and a native btvirt controller pair with fixed identities. |
| Saved network | network NAME SHA256 RELATIVE_JSON | S8.2-11–13 | Exact SSID bytes, WPA2-PSK, IPv4 address and fixture association. |
| Saved pairing | bluetooth-pair ADAPTER PEER SHA256 RELATIVE_INFO | S8.2-11–14 | Exact native BlueZ bond/key input; two reciprocal rows permit mutual authenticated traffic. |

The renderer validates every field; exact schema and package requirements are in
radio_declaration.py. One fixture/client is supported. The fixture remains when
client/bond rows are removed. Startup does not generate pairing keys: it restores
the declared bytes and requires native traffic before APPLIED. These forms require
manual text edits; network/pairing command recording is still unfinished.

Radio controls and BlueZ storage occupy a trusted private mount namespace.
Ordinary/sudo/Flatpak sessions cannot change those controls. Their code and native
tools remain named package payloads. Normal PID1 monitors the supervisor; optional
systemd owns it as a Type=notify service with dependent readiness/user managers.
Radio failure revokes readiness. The same declaration drives boot and apply.

Native read-only inspection: sudo confos radio-inspect wifi|bluetooth|files.
This root-only fixed broker enters the supervisor mount namespace, accepts no
caller command/path/address/environment, and reads actual native state. wifi
returns native iw/ip command output for the client and AP; bluetooth returns
BlueZ GetManagedObjects properties, including Adapter1 Address and Device1 Paired;
files enumerates private runtime/BlueZ paths, types, modes, owners and checksums.
It never reads the runtime READY report to infer these values and never outputs
bond key contents. No arbitrary native command or bus mutation is exposed.

Real hardware support and generic radio managers are not claimed. Private caches,
bus identifiers, logs and the runtime PID are listed in RADIO-040-DOCUMENTATION.md;
UNDERIVED enumerates the baseline inventory separately. Native probes and their
remaining limitations are in STATE.md; this interface is not an acceptance result.

Revision39 adds exact source-built Bash/sh, Python and libpython replacements
for the recorded org.freedesktop.Platform/x86_64/26.08 runtime commit
 df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c.
The existing named code-reader component supplies compressed payloads and a static
manifest. Existing flatpak lines remain unchanged; the bundle SHA, original file
SHA, repository inode, replacement SHA and mode must all match that manifest.
Other runtime refs/commits are not covered by this override set. A matching commit
with a different bundle checksum is refused rather than silently substituted.

Deployment files are replaced with separate inodes, preserving original repository
object bytes. Exact original-object execution and executable mapping are denied
in both session and Flatpak profiles, including their /run/host aliases. Their
bytes remain readable as material. Removing the runtime removes its deployment
and alias restrictions; removing only the application retains its named runtime.

The guarded readers preserve declared, typed, piped and data use. Native mpv Lua,
MuJS and other unpatched/unknown embedded readers remain open. The builder's
namespace probes cover specified bwrap/unshare attempts only; they are not a
claim about every namespace construction. Source and ABI differences, including
unproven whole SDK build parity, are recorded in the packaged provenance drafts.

Revision38 adds explicit configuration request recording. Authorized root
invocations of hostnamectl set-hostname, timedatectl set-timezone (UTC/Etc/UTC),
sysctl -w, systemctl enable/disable of existing declared services and
systemctl --user enable/disable of existing caller-owned units edit declaration
lines only. The RECORDED/separate confos apply/APPLIED protocol is unchanged.
Automatic query-only sudo does not authorize recording; --user mutations require
an explicit sudo origin matching the declared account.

useradd [-m] [-u UID] [-g GID] [-G GROUPS] [-s SHELL] [-d HOME] NAME writes a full
account line. Unspecified new-account defaults are the first ID >=1000 unused as
any declared UID/GID, primary GID equal to UID, no supplementary groups, /bin/bash,
and /home/NAME. Existing accounts retain unspecified fields on repeated requests.
usermod supports those field options and -a -G / -aG to append groups. userdel
removes an unreferenced account line; material in its home is not deleted.
Identity changes/removal with declared references require explicit dependent edits.
Numeric groups and named supplementary groups follow existing account semantics.

Configuration queries hostnamectl --static and timedatectl show -p Timezone read
immutable applied files; sysctl reads kernel values. Original native helpers,
when installed, remain at /usr/lib/confos/native/NAME and cannot be invoked
directly from a confined session. Query forwarding has a finite allowlist.
Unsupported timezone values/options, unknown units, groupadd, nft mutations,
visudo editing and the other unfinished mappings remain refused as listed in
CHOICES. No new line kinds or automatic observation of installed state exist.

Revision37 adds root `podman pull REGISTRY/NAME[:TAG]` and `podman rmi` for one
fully qualified image name. `sudo` targets the declared ordinary SUDO_USER;
direct root supplies `--account USER`. Missing tag means latest; repeated pulls
reuse the exact recorded input, not a refreshed tag. Native Podman pulls/saves
into private scratch without running an image; the adapter records the existing
container line and checksum-bound OCI archive. RECORDED/separate APPLIED applies.
Short names, digest/transport references, multiple images, alternate flags,
private authentication and other mutation verbs remain unsupported/refused.
Original native Podman bytes move to `/usr/lib/confos/native/podman`; direct
session execution is denied. Rootless recorded-image run behavior is unchanged.
Guest regression is pending; handover status is in STATE.md.

Revision36 adds root `flatpak install --bundle LOCALFILE` and `flatpak uninstall
ID|REF`, with optional `-y`, `--assumeyes`, `--system`. They record the existing
flatpak line and use the same RECORDED/separate-apply protocol. Native Flatpak
imports frozen bundle bytes into isolated scratch to obtain exact ref/commit;
the adapter writes the line and durably retains the input beside the declaration.
An application requires its runtime already recorded. Removing a runtime still
required by another line is refused. Repeats preserve equivalent handwritten lines.
Named-remote installs, remote-add, user installs, other flags and mutation verbs
are refused; no remote line kind exists. Original native Flatpak bytes move to
`/usr/lib/confos/native/flatpak`, inaccessible to direct session execution.
Guest add/repeat/removal, pre-apply nonchange and pending/applied power-cut
regression passed; release status is in STATE.md.

Revision35 adds pip/npm recording with the same root authority,
primary declaration, RECORDED/APPLIED protocol and separate application as APT.
`pip install NAME[==VERSION]...` or local `.whl` inputs resolves binary wheels;
each dependency gets an exact `pip` line. `pip uninstall [-y|--yes] NAME...`
removes named lines unless another pip line still needs them. The harmless
`--break-system-packages` flag is accepted. `npm install -g NAME[@VERSION]`
and `npm uninstall -g NAME` support one unscoped root; `--global` is equivalent.
Bare install names resolve once; repeated requests preserve the recorded version.
Native npm writes its exact package lock with lock-only mode and lifecycle scripts
disabled. The adapter writes ConfOS line syntax. Pip uses binary-only native
resolution. Inputs are fsynced under `/state/recorded-inputs/SHA256/` before text
commit; removal leaves these source materials available for reuse. No installed
state is scanned. Relative wheel paths are relative to the invoking directory.
Direct `/usr/bin` aliases and `python3 -m pip` share the recorder. Original pip
entry bytes move to `/usr/lib/confos/native/pip{,3}`; native pip/npm implementation
modules remain inaccessible to ordinary confined sessions. Queries still work.
Requests outside the existing grammar are refused: version ranges/tags, editable
or source builds, requirements files, VCS/URL requirements, alternate registries,
target/prefix/user overrides, scoped npm names, per-project npm, arbitrary flags,
and conflicts with remaining declared dependencies. CHOICES lists the restrictions.
Guest recording/add/repeat/removal and pending/applied power-cut regression passed;
release/handoff status is recorded separately in STATE.md.

Revision34 adds explicit APT request recording. Both `apt` and
`apt-get`, including `/usr/bin` and `/bin` paths, accept root requests
`install NAME[=VERSION]...`, `remove NAME...`, `purge NAME...` and optional
`-y`, `--yes`, `--assume-yes`, `-q`, `-qq`. Install resolves the selected archive
and writes `package NAME VERSION`; remove/purge removes that explicit line.
A remaining base/dependency owner prevents removal and is reported as an error.
The tool prints exactly `RECORDED SHA256; run confos apply` after durable text
replacement at `/state/declaration.conf`. Exit0 reports only recording. It does
not apply, reboot, install files or change the identity returned by status.
Run `sudo confos apply`, reconnect, and wait for `confos status` to return
`APPLIED SHA256`. Only that is the machine's success report. Repeating the same
request preserves the text. Non-root requests explain that the account may not
change the declaration; use an authorized root invocation. Other options/commands
are refused; `--version` remains a native read-only query.

Original APT executable bytes move from `/usr/bin/apt{,-get}` to
`/usr/lib/confos/native/apt{,-get}`; the original paths become links to the
runtime package's command entries. Confined sessions cannot execute the native
helpers directly. The trusted recorder only requests native metadata/simulation,
with an empty status and fixed options; application alone downloads/unpacks.
No recorder examines installed files or monitors downloads to infer lines.
Original component data `archive-sources.json` names each snapshot's sources.
T2 adds security snapshot20261124T000000Z to main20261123T000000Z and pins the
kernel to6.12.118-1; T0/T1 stay as before. All request/assembly/initramfs resolvers
use the same source map. Native APT has no mode that emits ConfOS package lines;
the recording adapter is implementation code, reported as such under plan9.3.

Revision33 changes retained in34: Flatpak app processes enter confos-flatpak through a
fixed runtime /usr/bin/sh entry before their command; the runtime must supply that
shell. Original app metadata supplies the default command. Native BusyBox vi .exrc
startup inputs require recorded immutable files, retaining original owner/mode checks.

Revision32 applies exact-AppImage reader overrides from original component data
at /usr/lib/confos/appimage-reader-overrides/manifest.json. Each record names
archive_sha256, relative target, original_sha256, gzip payload, raw sha256 and
integer mode. Members live beside the manifest. Only a matching declared archive
activates an override, after its original bytes are checked. Neovim0.10.4 replaces
its binary, Lua loader and AppRun; the entry fixes VIMRUNTIME to that archive.
The original component and AppImage suffice to derive every resulting byte.

Revision31 adds conditional Git payloads for all13 original native ELF paths,
including git-core helpers and scalar. Existing symlink aliases retain their
targets. Git code-valued configuration requires recorded immutable files; the
exact key list is in the original component's git-code-policy.h. Direct config
writes of those values are refused, including through sudo. Typed -c values and
ordinary repository data remain usable. No declaration syntax change.

Revision30 extends the conditional reader manifest to native Node20: nodejs
activates /usr/bin/node and libnode115 activates its native shared library.
The library mediates CJS/ESM/startup/stdin/REPL readers and package.json when
obeyed as resolver configuration. Record such configuration with file lines.
Ordinary JSON data reads/imports and typed/pipe code remain available. Prototype
results are in CODE-READERS.md; native/restart/removal results are in STATE.md.
The immutable input rule also covers snapshot builders/configurations/blobs,
native environment files and policy manifests. Record a generated snapshot's
checksum with a file line before loading it.

Published before the first image. Commands below run in the source directory on the
worker. Implementation status is in STATE.md; this contract does not claim completion.

Revision29 adds conditional reader payloads to the original confos-code-readers
package. `/usr/lib/confos/reader-overrides/manifest.json` is an array of records:
`package`, `source_version`, `target`, `payload`, `mode` (integer), `sha256` (raw bytes).
`payload` names a gzip member beside the manifest. If `package` is selected by
the declaration/base closure, its existing native target is replaced by those
exact decompressed bytes/mode. Otherwise the member remains compressed data.
This table and the original package suffice to derive the override; no installation
inventory is used. Entries cover dash, mawk, gawk, sed and make. The base already
owns mawk and BusyBox command aliases; those owners remain when an optional line
is removed. Source29 includes original reader component28 as a fixed build input.

Revision28 adds BusyBox ash/sh, awk and sed program-file enforcement to the
original `confos-code-readers` component, replacing `/usr/bin/busybox` and its
existing command aliases. Typed commands and data reads remain available.

Revision27 added the original component `confos-code-readers=VERSION`, archive
`packages/confos-code-readers_VERSION_amd64.deb`, retained with its SHA256 companion
under `/system/base-packages/`. It replaces `/usr/bin/bash`, `/usr/bin/python3.13`,
`/usr/bin/perl`, the Perl version alias, Python's matching standard-library extensions,
and its sourceless-loader source with
source-built Debian versions that check code inputs. This supersedes the general
statement below about retaining every native executable's bytes. Patches and original
Debian source archives are included in the source release. Boot/apply interface and
declaration syntax are unchanged. Other interpreters remain open (CODE-READERS.md).
All staged tools now use private proc/dev mounts; util-linux is a pinned base
component. STATE.md names the released image and checksum when handoff is complete.

Revision26 adds `confos-initramfs=VERSION+TIMESTAMP` to each snapshot component
lock. The original archive is `packages/confos-initramfs_VERSION+TIMESTAMP_amd64.deb`.
It supplies `/usr/lib/confos/initramfs/initramfs`, `kernel-release` beside it, and
the matching `/usr/lib/modules/RELEASE/modules.*` indexes. Clean build and apply
copy its initramfs unchanged to `/system/generations/IDENTITY/initramfs`; no host
depmod or cpio runs. The package builder uses original pinned Debian archives and
authored early-init, never an installed root. All three snapshot packages and
their SHA256 companions are retained in `/system/base-packages/` to permit both
updates. Only the active snapshot's package is unpacked into the root. Boot/apply
commands and the APPLIED success report are unchanged. This does not resolve all
generated forms or the independent Understanding check.

Revision25 rejects account names root, _apt, wheel and nogroup, reserved UIDs0/42
and repeated UIDs before assembly. Numeric IDs use ASCII digits in0..4294967294.
Shell/home fields cannot contain colon separators or control characters; shell
paths are absolute without .., and homes remain immediate children of /home.
Native account lookup is checked before readiness. These are additional declaration
constraints; rejected apply preserves the last committed identity.

Revision24 validates hostname and sysctl:kernel.hostname together before assembly.
Values require 1..64 ASCII letters/digits/dots/hyphens, starting with a letter or
digit; both forms may coexist only with the same value. Either form supplies
/etc/hostname, /etc/hosts and the running hostname. With neither, the base default
is confos. Boot preparation checks the running value before readiness. Invalid
values/conflicts fail apply without changing the committed declaration identity.

Revision23 names confos-boot=VERSION as a component alongside confos-runtime.
Both original archives and their checksums are in packages/ of the source release
and /system/base-packages of a clean disk. confos-boot_VERSION_amd64.deb supplies
/usr/lib/confos/boot/BOOTX64.EFI; the disk's /EFI/BOOT/BOOTX64.EFI is an exact copy.
The fixed boot release remains the same across T0/T1/T2 updates. Clean builds use
these packaged bytes and do not invoke the host GRUB generator. package-boot.py,
boot-components.txt and boot-grub.cfg publish its inputs and build method.
Revision23 also fixes optional command discovery: Flatpak/Podman/pip/npm links
are created only when their native executable is installed. The private broker
programs remain runtime-package payloads; these optional links are generated
bindings and remain a separate derivation obligation. Native package prerequisites
must be declared before their commands are available.

Revision22 puts built-in nft, systemctl, Flatpak, Podman, pip/pip3 and npm/npx
entries in /usr/local/bin, linked to packaged files in /usr/lib/confos/commands.
The session and sudo PATH select these entries. Original Debian programs retain
their original paths/bytes; direct execution of mediated native entries is
refused in a session. Query/run brokers and declaration application invoke them
in trusted contexts. Absolute /usr/bin/systemctl etc. are no longer public query
entries; use command names or /usr/local/bin/NAME. Python's pip module entry is a
fixed runtime-package override. Package prerequisites are unchanged.

| Operation | Interface |
|---|---|
| Clean installation | `./build.sh DECLARATION OUTPUT.qcow2` |
| Boot | `./boot.sh DISK SSH_PORT MEMORY_MIB SERIAL_LOG [QMP_SOCKET]` (foreground; stop its process to cut power). Default QMP socket: `SERIAL_LOG.qmp`. Network backend ID `n`. |
| Firmware | QEMU x86_64 UEFI; the EFI executable, kernel and initramfs are on the disk |
| Edit | `/state/declaration.conf`, ordinary UTF-8 text, editable by root with an editor or file replacement |
| Apply | `sudo confos apply`; reboot completes application and ends the connection |
| Success | After reconnect, `confos status` prints exactly `APPLIED SHA256`, with the hash of the declaration bytes in force. No earlier progress message is success. |
| Failure | Nonzero exit before reboot, or `confos status` without APPLIED; previous successful identity remains authoritative |
| Login | An `account` line sets the account and an `authorized-key` line its public key; SSH port is forwarded by boot.sh |
| Privilege | Accounts with group `wheel` may run `sudo -n COMMAND`; root direct key login is also declarable |
| Package change | Edit `package NAME VERSION`; apply rebuilds the complete root, then reboots |
| Slots | boot.sh acquires one of the six common worker slot locks; 2 vCPU, memory at most 8192 MiB |

Disk: GPT partition 1, FAT EFI system partition (boot executable and boot configuration);
partition 2, ext4 labelled CONFOS-SYSTEM (kernel, initramfs, root image and committed
declaration); partition 3, ext4 labelled CONFOS-DATA (material, declaration candidate and
staging). Runtime `/` is a read-only squashfs. `/state` is partition 3, mounted
nosuid,nodev,noexec. `/home` is backed by `/state/home`; volatile `/run`, `/tmp`, `/var`
are tmpfs. Declared `file` objects below `/home` use read-only executable bind mounts
from the immutable root; other home files remain on noexec storage. Since 0.7 a
top-level home directory containing declared files is bound as a whole, to prevent
an ordinary user renaming their mutable ancestors. A top-level file is bound alone.
The immutable root is also visible at `/run/root-view` for these bindings.
The system store is mounted at `/system` read-only during ordinary operation.
No encrypted or private filesystem format: guestfish can mount each partition and
download the squashfs, and unsquashfs lists its files without implementation records.

Application stages all payloads before changing the boot selection. The final status
must follow durable storage and a successful boot of the selected root. This remains
an implementation obligation, not a statement that power-cut cases have passed.

Runtime keys are not shipped in the source. A clean build requires the declaration's
authorized public key. Initial host keys are ephemeral and listed in UNDERIVED.md.

Source 0.2 adds `confos services` (NAME STATE PID, one line per service); service unit
descriptors are `/etc/confos/units/NAME.json`. `nft list ruleset` reads effective rules.
Applying a changed ConfOS base release requires a clean build with matching source;
in-place ConfOS-runtime upgrades are not implemented. Debian archive-state updates
within one base release are described below.

0.3 confines ordinary SSH sessions and service children even after `sudo` changes
their UID to zero. Root identity does not grant unrestricted kernel administration.
`sudo confos rules` runs the native nftables read-only query with the required
authority; direct nft mutation commands are intended to be refused. The native output
is returned unchanged. This inspection path does not read an ownership ledger.
`confos apply` is the privileged transition path; its interpreter ignores environment
imports and site files. Saved interpreted input is still an open P4 defect.

0.4 repairs sudo initialization when additional packages supply PAM configuration.
Both `sudo -n COMMAND` and `sudo -n -i COMMAND` use the declared wheel permission.
The hosts file follows the declared hostname. UTC timezone accepts `UTC` or `Etc/UTC`.

0.5 changes partition 2's boot layout: `/boot.cfg` is the atomic generation selector.
`/generations/SHA256/` contains `root.sqfs`, `declaration.conf`, `vmlinuz`, and
`initramfs`. There is no `/current` file or top-level kernel/initramfs. GRUB loads
the selected kernel and initramfs, passing the same generation identity to early
init. Application durably writes all four files before replacing boot.cfg.
The partition numbering, filesystems, login, editing and success interfaces are unchanged.

Snapshot states `20260801T000000Z`, `20261001T000000Z`, and `20261123T000000Z` have
published complete base locks in `components/TIMESTAMP.txt`. Changing the snapshot
line and any explicit package versions applies that archive state, including its
kernel, on the next boot. A package line conflicting with the base lock is rejected.

0.6 adds `sudo confos kernel-log`, a read-only native kernel-log query. TLS trust is
the deterministic concatenation of shipped CA certificates and declared local CA
files. LibreOffice's shipped registry default is copied to its expected configuration
path. The pip/npm input forms and installed command names are in DECLARATION.md.
Rootless clean builds with these kinds also require `unshare` and enabled user
namespaces on the build host; the installers run in the staged root, not on the host.

0.7 protects the default `.bashrc`, `.profile`, `.bash_profile`, `.bash_login`,
`.bash_logout`, `.inputrc`, `.gitconfig`, and `.ssh/rc` of each account as empty
immutable base files. A `file` line may supply their exact contents. Login public
keys are in the immutable `.ssh` subtree. Account homes must be immediate children
of /home. Other material belongs outside managed subtrees: for example, keep source
projects in ~/src and declared executables in ~/bin; outgoing SSH private keys can
live outside the managed ~/.ssh. Underlying material is retained but hidden while
an immutable subtree is mounted over its name. Saved interpreter input remains an
unresolved P4 defect despite protection of these automatic startup paths.

0.8 supports `sudo nft [-a|-n|-j] list ruleset` and `sudo nft list tables` through
a read-only broker returning native nft output. Mutations require declaration rules.
From0.22 the original binary remains /usr/sbin/nft, denied to direct session execution;
the broker is selected through /usr/local/bin/nft. Sudo has a fixed PATH including
/usr/local/bin. A `compile` line builds recorded C source
with the staged declared GCC. During apply, native installers use a temporary
executable bind at /run/confos-installer-root; ordinary sessions cannot access it
or write the frozen staging tree. The bind is removed before application continues.

0.9 adds pinned native Flatpak bundles and a read/run command entry;
DECLARATION.md gives syntax and additional package requirements. System Flatpak
payloads reside at /usr/lib/confos/flatpak; /var/lib/flatpak is a symlink to that
immutable store. /run/user/UID is an account-owned volatile runtime directory.
Staged Flatpak installation additionally uses private mount/PID namespaces with
proc and device mounts, discarded when the native installer exits. The current
released source/image version and observed tests are in STATE.md.

0.10 adds AppImage extraction at assembly time, an immutable shared
payload at /opt/confos/appimages/SHA256, and declared launcher paths. The checksum
names the source image; the launcher is a derived file. No FUSE mount is needed.
See DECLARATION.md for input-format restrictions and STATE.md for observed tests.

0.11 adds account-specific native rootless Podman images from pinned OCI archives.
Archives are immutable at /usr/lib/confos/container-images/SHA256. Boot prepares
native stores at /run/confos-containers/USER/store and read-only execution views at
/run/confos-container-ro/USER/IMAGE_SHA before APPLIED. These paths and native Podman
metadata under /run/user/UID are volatile; they are regenerated at boot. The JSON
mapping /etc/confos/containers.json follows from declaration rows and image defaults.
See DECLARATION.md for the restricted command interface and subordinate-ID mapping.

0.12 adds native `user-unit` service/timer declarations. Exact unit files and enable
links are under /etc/confos/user-units/USER/systemd/user; fixed system-manager units
are under /etc/confos/systemd-system. When present, native systemd takes over PID 1
after base preparation; SSH and APPLIED wait until the user managers and enabled
units are ready. No distribution unit search path or generators are enabled.
`systemctl [--user]` supports read-only status/show/cat/is-active/is-enabled,
list-units/list-unit-files/list-timers/list-jobs/is-system-running operations.
The wrapper sets the ordinary account's runtime/configuration paths; callers need
not set XDG_RUNTIME_DIR. A narrowly scoped sudo entry provides native query access
to mode-000 manager sockets. Direct session manager mutation remains restricted even
through sudo, whose session profile does not grant DAC write override. From 0.18,
root retains DAC read/search for inventory of private runtime records.
The older `confos services` interface and legacy service descriptors remain available.

0.13 sets the base login/service locale to C.UTF-8 and adds the matching pinned
libc-bin component for all three snapshots. Dropbear receives a fixed environment
and passes it to sessions, including noninteractive SSH commands. /run and /var are
mode 0755. Standard /dev/fd and stdio links are created at boot. Native firewall
rules contain exactly the recorded text, without a generated comment carrying the
line's name. No build/boot/login/apply pathname or success interface changes.

0.14 preserves numeric archive ownership of unchanged Debian payloads in the
immutable image. It also supplies libc6-i386's fixed /lib32 and 32-bit loader links.
Generated object ownership and the declaration syntax otherwise remain unchanged.

0.15 provides fixed native pip/npm inspection entries; direct installation and npx
must use declaration/application instead. python3 -m pip delegates to the same entry.
Sessions cannot import the built-in installers' private modules or bootstrap pip
through venv. Native staged installation is unchanged. See DECLARATION.md for the
supported inspection arguments. General saved interpreter input remains unresolved.

0.16 supports declared native sudo rules as exact /etc/sudoers.d/NAME file lines.
Invalid candidates fail native policy validation and do not replace the active
generation. Failed application removes its staging and unselected partial generation
and restores /system read-only. The active declaration identity remains unchanged.

0.17 permits native root inspection of other accounts' /proc/PID/exe links. AppArmor
grants read/readby, not trace/tracedby; debugger attachment and process-memory access
remain refused. Inspection still uses native tools, not an implementation ledger.

0.18 adds linuxgsm bundle lines. PATH/wetserver is the native launcher; run it as
the named ordinary account, e.g. `bash /home/user/game/wetserver start` and `stop`.
Installation and a recorded launcher-version update run the native upstream tools
during apply. The code subtree is immutable and owned by that account. Logs, locks
and temporary records live below /run/confos-games and vanish on reboot; the native
temporary launcher cache is a read-only bind of recorded source. Direct mutable
self-update is not the application interface. See DECLARATION.md for bundle inputs.

0.19 accepts standard read-only systemctl property/type filters, unit-name escaping
and the `--` separator used by outside inspection. A missing declared user manager
is reported explicitly. Clean disk assembly and boot wait when all shared VM slots
are occupied; they retain the same six-slot limit and may be cancelled while queued.
A persistent harness may reserve a guest slot across restarts and pass its inherited
descriptor as CONFOS_SLOT_FD. boot.sh verifies that it names one of the six shared
lock files and locks it before launching QEMU. This permits a harness to reserve a
second slot for an outside-inventory appliance without exhausting the pool mid-run.

0.20 ships the fixed runtime/default files as the genuine data archive
`packages/confos-runtime_0.20_all.deb`, listed in every base component lock. Its
SHA256 companion is shipped with it. The package is unpacked after Debian payloads;
its Replaces field identifies overlapping default providers. The disk keeps the
archive and checksum below `/system/base-packages/` for later application. The
source build creates the package from source if it is absent; published source
releases include it. No installation snapshot or declaration recorder is used.
Only packages selected by the current native dependency resolution are unpacked;
old cached archives do not contribute files to a later clean build.

0.21 adds an optional explicit numeric owner to file lines:
`file PATH MODE UID:GID SHA256 SOURCE`. The original five-field form still uses
0:0. Explicit values are written to the immutable filesystem metadata; native sudo
rule files require 0:0. Source/checksum handling, apply and success reporting are
unchanged. The development example spells out 0:0 for its recorded script.

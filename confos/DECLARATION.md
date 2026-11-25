# Declaration syntax, revision 55 (source 0.55)

Revision 55 changes no syntax.

Revision 54 changes no syntax. A `package` line that brings libreoffice-core must resolve to one of its
three guarded releases (INTERFACE.md, revision 54).

Revision 50 adds one kind of line, `group NAME GID`, and one setting,
`setting module:NAME loaded`; both are in the table of kinds below. Nothing else
changes.

Revision 49 changes no syntax. A `flatpak` line may name any export of a pinned ref
and commit (see INTERFACE.md, revision 49); the SHA256 field is still the checksum
of the bundle file the line names.

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

From32 the original reader component can override exact AppImage payloads using
its static appimage-reader-overrides manifest. The appimage line still names the
original archive digest. That line and component data jointly determine the result.
Neovim's code inputs must be recorded immutable files; Lua disk bytecode caching
uses the original checked file loader. Last-owner removal removes the full tree.

From31 Git code-valued configuration must be a recorded immutable file. This
includes aliases and credential/filter/tool sections plus the explicit executable
keys in git-code-policy.h. A file line can supply the configuration and hooks;
typed -c settings and repository data are separate. Conditional overrides affect
only paths owned by the selected git package, including native helper binaries.

From30 native Node code readers and resolver package.json files follow the same
immutable-code input rule. A package.json whose settings are obeyed must be
supplied by a package or recorded file line. JSON read explicitly as data remains
available. Node executable/library payloads activate only with nodejs/libnode115.
Startup snapshot/configuration, environment and policy files likewise require
recorded immutable inputs; generated snapshot outputs use ordinary file lines.

UTF-8; blank lines and lines beginning `#` ignored. Shell-style quoted fields, no
expansion, no execution. Duplicate identities and unknown kinds fail application.
Content source paths must be relative, without `..`, below the declaration directory.
They resolve beside the declaration at build time; runtime files
resolve beside `/state/declaration.conf`. All versions and SHA256 values are exact.
From34 a person may write a line or request it through an adapted built-in tool.
APT install/remove/purge edits package lines only, before any application, and
prints `RECORDED SHA256; run confos apply`. The declaration in force is unchanged
until application reports `APPLIED SHA256`. See INTERFACE.md for supported requests.
The resulting line has exactly the syntax and derivation of a handwritten line.
From35 pip install/uninstall and global npm install/uninstall edit their existing
line kinds. Exact wheel/lock inputs live beside the declaration under
`recorded-inputs/SHA256/`; the line names their relative path and checksum.
Native npm writes the unchanged lock bytes, and the adapter writes the ConfOS
line. Inputs and text are durable before RECORDED. Details/refusals are in
INTERFACE.md and CHOICES.md. From36 Flatpak bundle install/uninstall likewise edit
the existing flatpak line and retain checksum-bound input bytes. No remote line
kind is added; remote-add/named-remote installs remain refused.
From37 Podman pull/rmi record/remove container lines for a declared ordinary
account. The native OCI archive is retained verbatim as a checksum-bound input.
The account is explicit via --account or validated from sudo's caller identity.
Exact accepted requests and repeat semantics are in INTERFACE.md.

From29 the native reader component's static `reader-overrides/manifest.json`
selects exact compressed payloads for installed dash, mawk, gawk, sed and make
packages. Targets, modes and raw checksums are explicit component data. This is
an additional package-composition rule, documented in INTERFACE.md; it writes
no declaration lines. Optional executables are absent when no owner selects them.

From27 the component lock names `confos-code-readers=VERSION`. Its package supplies
patched native Bash/Python/Perl code readers, overriding those paths of the original
Debian packages. No new line kind or recorder is introduced. In confined sessions,
saved code inputs for those readers must be on immutable executable mounts. Declared
source files with mode0644 are allowed; mutable files remain readable as data.
This is not a claim that every interpreter route is closed; see CODE-READERS.md.
From28 the same component also supplies BusyBox and checks ash/sh, awk and sed
program inputs through all their existing command aliases.

From26 the selected snapshot component lock also names
`confos-initramfs=VERSION+TIMESTAMP`. Its package contains the exact initramfs and
native kernel module indexes; all three original snapshot archives are retained
on the system partition for updates. The package's build-input list and authored
init source describe build inputs, not declaration lines or an installed-system
manifest. Package locators and disk placement are in INTERFACE.md.

Hostname values (`hostname` and `sysctl:kernel.hostname`) require 1..64 ASCII
letters, digits, dots or hyphens, starting with a letter or digit. Both lines must
agree if present. Either supplies `/etc/hostname`, the local `/etc/hosts` entry
and the running hostname. Neither present means the base default `confos`.
These are implementation constraints; invalid/conflicting lines fail before commit.

Account names cannot collide with root, _apt, wheel or nogroup. UIDs must be unique
and cannot be0 or42. UID/GID use ASCII integers in0..4294967294. Shell/home cannot
contain colon separators or controls; shell is absolute without .., and home is
immediately below /home. These additional restrictions are checked before assembly.

From22 query/run entries are packaged files with /usr/local/bin links; native
Debian executables retain their original bytes and paths. See INTERFACE.md. The
fixed Python pip module entry is supplied by confos-runtime, which declares its
replacement of python3-pip. Generated settings remain a separate derivation gap.
From23 optional Flatpak/Podman/pip/npm command links appear only with their native
package. The broker program bytes are packaged; these conditional link objects
are generated bindings and are not claimed independently derived under D3.

| Kind and syntax | Meaning | Specification | Example |
|---|---|---|---|
| `base VERSION` | ConfOS runtime and boot data packages, default files and pinned component closure; must match source VERSION | S8.2-7, S8.2-16, S8.2-17 | `base 0.23` |
| `snapshot TIMESTAMP` | Debian archive and published base component lock selected for this application | S8.2-16 | `snapshot 20261123T000000Z` |
| `package NAME VERSION` | Unpack a Debian package and its dependency closure; no maintainer scripts | S8.2-7, S8.2-16 | `package hello 2.10-5` |
| `pip NAME VERSION SHA256 WHEEL` | Install the exact wheel with native pip; relative input beside the declaration | S8.2-7, S8.2-16 | `pip cowsay 6.1 HEX cowsay-6.1-py3-none-any.whl` |
| `npm NAME VERSION SHA256 LOCK` | Install through native npm ci with a pinned package-lock.json input | S8.2-7, S8.2-16 | `npm cowsay 1.6.0 HEX cowsay-package-lock.json` |
| `flatpak REF COMMIT SHA256 BUNDLE` | Native Flatpak installation from a pinned bundle, with exact OSTree commit | S8.2-7, S8.2-16 | `flatpak app/io.mpv.Mpv/x86_64/stable COMMIT HEX mpv.flatpak` |
| `appimage PATH MODE SHA256 SOURCE` | Extract the content-addressed AppImage release and install an immutable launcher | S8.2-7, S8.2-16 | `appimage /home/user/bin/nvim 0755 HEX nvim.appimage` |
| `container USER NAME IMAGE_SHA ARCHIVE_SHA SOURCE` | Native rootless Podman image for one account; configuration digest and OCI archive checksum pin its release | S8.2-7, S8.2-16 | `container user docker.io/library/alpine:3.20.3 CONFIG_HEX ARCHIVE_HEX alpine.oci.tar` |
| `linuxgsm USER PATH RELEASE SHA256 BUNDLE` | Native LinuxGSM and ET 2.60b package, installed/updated in staging from a pinned input bundle | S8.2-7, S8.2-16 | `linuxgsm user /home/user/game 26.5.0 HEX linuxgsm-wet-26.5.0.tar` |
| `user-unit USER NAME STATE SHA256 SOURCE` | Native user .service/.timer unit, exact source bytes and enabled/disabled startup state | S8.2-13, S8.2-17 | `user-unit user cases-tick.timer enabled HEX cases-tick.timer` |
| `account NAME UID GID GROUPS SHELL HOME` | Exact account; GROUPS is comma-separated names or `-` | S8.2-13 | `account user 1000 1000 wheel /bin/bash /home/user` |
| `authorized-key NAME TYPE KEY` | Login public key; no optional comment | S8.2-13 | `authorized-key user ssh-ed25519 AAAA...` |
| `file PATH MODE [UID:GID] SHA256 SOURCE` | Immutable exact bytes and optional explicit numeric owner, including one's own programs and settings | S8.2-9, S8.2-13, S8.2-16, S8.2-19 | `file /usr/local/bin/mine 0755 1000:1000 HEX mine.sh` |
| `compile PATH MODE SHA256 SOURCE [FLAG ...]` | Compile exact C source with the staged declared GCC; immutable output | S8.2-9, S8.2-16 | `compile /home/user/bin/demo 0755 HEX demo.c -O2` |
| `group NAME GID` | From 0.50. A group of its own; GID 1..4294967294, used by no account and no other group; usable in GROUPS of any account line, wherever the line stands | S8.2-13 | `group project 1001` |
| `setting module:NAME loaded` | From 0.50. A loadable module of the pinned kernel, loaded at every start; `loaded` is the only value | S8.2-11–14 | `setting module:dummy loaded` |
| `setting NAME VALUE` | hostname, timezone (UTC or Etc/UTC), or `sysctl:KEY` | S8.2-11–14, S8.2-17 | `setting sysctl:kernel.printk '4 4 1 7'` |
| `service NAME STATE EXECUTABLE [ARG ...]` | enabled/disabled service and exact argv | S8.2-13 | `service demo enabled /usr/bin/sleep 600` |
| `rule NAME TEXT` | Exact nftables rule text | S8.2-13 | `rule input 'add rule inet confos input tcp dport 22 accept'` |
| `network NAME SHA256 SOURCE` | Exact saved network configuration | S8.2-13 | `network wifi HEX wifi.conf` |

The first implementation may reject kinds not yet implemented; see STATE.md. Such a
rejection is an unfinished requirement, never a passing ordinary-work case. A `file`
line does not claim that unrelated mutable files are recorded. Permissions are octal.
Numeric IDs, exact releases and content checksums are extra requirements for reproducibility.

LinuxGSM bundles currently pair launcher 26.5.0 or 26.6.0 with ET server 2.60b.
USER is a declared ordinary account (UID 1..60000); PATH is one immediate child
of its /home/NAME, with letters/digits/hyphens/underscores only. No other file,
compile or AppImage line may overlap that workspace. Declare the native prerequisites
listed in game-packages.conf. BUNDLE is a tar containing manifest.json, initial.tar.gz,
target.tar.gz, game.tar.xz, common.cfg and wetserver.cfg. The manifest names the
initial/target source commits, exact releases and the three inner archive checksums.
prepare-game-sources.py and prepare-game-bundles.py construct example inputs from
pinned upstream archives and authored default configurations; they write no lines
and never inspect installed output. The 26.6.0 bundle runs native update-lgsm from
the included initial 26.5.0 source. Native output bytes/modes are checked against
the game archive; launcher identity fields are checked against the target source.
Final code/configuration and the default-config cache are immutable, owned by the
declared account. The native instance identifier is the first eight hex digits of
SHA256(PATH concatenated with the bundle SHA256), followed by a newline. Logs,
locks and scratch space are volatile. This does not resolve general saved-code P4.

Source 0.16 also permits file lines immediately below /etc/sudoers.d. Names contain
only letters, digits, hyphens and underscores; mode must be 0440. Further include
directives are rejected. Native visudo validates the complete policy before the
candidate becomes active. Removing the file line removes its native policy entry.
Source 0.7 requires account homes immediately below /home. A nested home file makes
its entire top-level subtree immutable (e.g. a line for ~/bin/tool manages ~/bin).
Default automatic shell/SSH startup files and .gitconfig are empty immutable base
objects unless a file line supplies their contents. See INTERFACE.md for the list.
Source 0.5 supports the three T0/T1/T2 snapshot timestamps in INTERFACE.md; other
timestamps require a new published component lock. `components.txt` enumerates the
T2 base closure; `components/TIMESTAMP.txt` enumerates each state's exact closure.
An explicit package line for a base component must agree with that snapshot's lock.
From 0.20 the lock includes `confos-runtime=VERSION`. This genuine Debian data
package is in `packages/confos-runtime_VERSION_all.deb` of the published source,
with a `.deb.sha256` companion. It supplies fixed native defaults and runtime code
with explicit modes/owners; it is unpacked last. Native Debian packages still come
from the named snapshot. Account/setting overrides and other generated objects
remain subject to independent derivation; this is not a blanket D1–D7 repair.
From23 each lock also names confos-boot=VERSION, supplied as
packages/confos-boot_VERSION_amd64.deb with its checksum. Its EFI program is built
from original Debian GRUB2.12-9+deb13u4 archives in snapshot20261123T000000Z, using
the complete boot-components.txt build-input lock and fixed boot-grub.cfg. These
build dependencies are not installed into the running root; the compiled package
payload is. Exact EFI bytes are copied to the disk's EFI system partition. This
pins the boot program; dynamic initramfs/module indices and disk IDs remain separate.
Source 0.14 preserves archive numeric UID/GID for unchanged Debian payload objects.
Generated objects retain UID/GID 0 unless the documented runtime account setup
changes them. From 0.21 a file line may explicitly state UID:GID (each 0..4294967294),
addressing the missing file-owner fields in D5. Omitting the field keeps 0:0; the
harder derivation reading may still reject that omission. Native sudo-rule files
require 0:0. Other generated objects and their ownership remain separate gaps.
For libc6-i386, the two loader compatibility links specified by its shipped postinst
are materialized deterministically; arbitrary maintainer scripts are still not run.

Pip requires the Debian python3-pip package. Wheel metadata must match NAME/VERSION;
dependencies need their own pip wheel lines. Native pip installs into the Python
minor release's `/usr/local/lib/python3.X/dist-packages`, without bytecode, downloads
or source builds; console scripts are linked in `/usr/local/bin` (e.g. `cowsay`).
Npm requires Debian nodejs/npm packages. The lock is version 2 or 3, with exactly
`{NAME: VERSION}` as its root dependencies; every dependency has an HTTPS resolved
URL and SHA256/SHA512 integrity. Native npm ci installs at `/opt/confos/npm/NAME`,
with lifecycle scripts disabled. Commands are named `npm-BIN` in /usr/local/bin
(e.g. `npm-cowsay`) to avoid Python/npm command collisions. Caches and staged inputs
are discarded; these tools never write declaration lines. Source 0.15 limits direct
pip/pip3 (including python3 -m pip) to version, list and show; npm to version and
ls/list with an optional /opt/confos/npm/NAME prefix. npx is refused. Native installer
implementation modules and pip bootstrap wheels are inaccessible to sessions;
python3 -m venv is also refused. Native installation remains available during apply.
These are additional restrictions, not a general solution to saved interpreted code.

Compile requires declared Debian gcc and libc6-dev packages. SHA256 pins the source,
not the resulting executable; the compiler and dependency releases determine that
output. SOURCE is one C file, compiled at /tmp/confos-install/source.c. Allowed flags
are -O0/-O1/-O2/-O3/-Os/-Og/-Oz, -Wall/-Wextra/-Werror/-pedantic and
-std=c89/c99/c11/c17/c23 or the corresponding gnu dialect. Unsupported compiler
options are rejected. PATH has the same limits as file; MODE must be executable
without special bits. Duplicate file/compile destinations are rejected. Compilation
uses SOURCE_DATE_EPOCH=1795392000 and TZ=UTC. Edit the source and its checksum line,
then apply to rebuild. No compiler command writes declaration lines.

Source 0.9 adds Flatpak; see STATE.md for validation status. REF is a complete
`app/ID/x86_64/BRANCH` or `runtime/ID/x86_64/BRANCH`. COMMIT is its 64-character OSTree
commit; SHA256 pins the single-file bundle. Existing native `flatpak build-bundle`
can export a bundle; the person writes its line. Runtime dependencies require their
own lines and are installed before applications. Only one ref per ID is supported.
Declare Debian flatpak, util-linux, gpg and gpg-agent packages as well. Rootless build
hosts need private mount/PID namespaces in addition to user namespaces.
The immutable system store is /usr/lib/confos/flatpak, linked at /var/lib/flatpak.
`flatpak list`, `flatpak info ID`, and `flatpak run [--command=COMMAND] ID [ARG ...]`
are exposed; ID must be declared for info/run. From36 supported bundle requests
record lines before separate application; other mutations remain refused.
Native Flatpak executes the install and launch operations;
launch requires an ordinary account. The user store is fixed to the immutable empty
/usr/lib/confos/flatpak-user directory so a user override cannot change that entry.
Read/run requests do not write declaration lines. General saved-code enforcement
and complete Flatpak reproducibility remain unverified.

Source 0.10 adds AppImage; validation status is in STATE.md. SHA256 names the
exact content release of the input image. Only type-2, little-endian ELF64 images
with squashfs immediately after the section table are supported. Native unsquashfs
extracts payloads without xattrs at /opt/confos/appimages/SHA256. The generated PATH
launcher sets APPDIR and starts AppRun; PATH's bytes differ from the input image.
PATH/MODE restrictions are the same as compile. Two lines with the same SHA256 share
one immutable extracted payload, rebuilt while any owner remains. FUSE and runtime
extraction are not used. AppImage runtime switches such as --appimage-extract are
not launcher operations; subsequent arguments go to AppRun/the application.
Inputs are preserved beside the declaration for later apply, as with file/compile.

Source 0.11 adds containers; validation status is in STATE.md. USER must name a
declared ordinary account with UID 1..60000. NAME is its native fully qualified
image name; IMAGE_SHA is the 64-character image configuration digest. SOURCE is a
Linux amd64 OCI archive exported by native `podman save --format oci-archive`.
Declare Debian podman, uidmap, slirp4netns and util-linux packages. Boot loads and
verifies the image with native rootless Podman before readiness. Subordinate IDs
start at 100000+UID*65536, with 65536 entries per account. Native image ownership is
preserved through this mapping. Stores and runtime metadata are volatile.
Before the read-only bind, absent etc/hosts, etc/hostname, etc/resolv.conf and
run/.containerenv mount targets are created as empty 0644 files owned by image root.
These fixed additions follow from the base recipe; existing image files are retained.
The native configuration and XDG configuration directory are fixed immutable paths.
`podman images`, `image ls`, `image inspect NAME`, `ps [-a|--all]`, `--version`, and
`run [--rm] NAME [ARG ...]` are exposed. Run uses the image's entrypoint, environment,
working directory and user; arguments replace its command. Runs are read-only,
without network, added mounts, capabilities or new privileges; cgroups are disabled.
Other command forms are refused. Only this account's recorded images may run.
Direct native entry is denied to sessions. This limited interface does not establish
general P4 or full container reproducibility; no command writes declaration lines.

Source 0.3 restricts `file` targets to `/home/`, `/usr/local/` and `/etc/confos/user/`;
declaration file rows cannot replace the trusted application machinery or its libraries.

Source 0.12 adds native user units; validation status is in STATE.md. USER is a
declared ordinary account. NAME ends in .service or .timer; STATE is enabled or
disabled. Declare systemd and util-linux packages. Unit bytes are copied unchanged
to /etc/confos/user-units/USER/systemd/user/NAME. A generated drop-in adds
WantedBy=default.target; service drop-ins also set AppArmorProfile=confos-session.
Enabled units have a default.target.wants symlink. Disabled means no automatic
startup link; a timer may still activate its disabled companion service.
The manager's unit/configuration paths are fixed there; generators are disabled.
Native systemd becomes PID 1 only when user-unit lines exist, with a minimal fixed
system target and one user manager per declared owner. The system's machine-id is
the first 32 hex characters of SHA256("ConfOS declared native managers v1").
Readiness waits for native manager jobs, enable state and enabled unit startup.
Native systemctl read operations are exposed through a fixed sudo query entry.
Mutation commands require edited declaration text and apply. Before SSH starts,
manager private sockets become mode 000. Confined sessions, including sudo, lack
DAC write override; only the read-only query entry can cross those socket permissions.
From 0.18 root retains DAC read/search for private runtime-record inspection.
This is an additional restriction on root commands accessing other users' files.

Legacy `service` lines have immutable JSON unit descriptors in `/etc/confos/units/NAME.json`;
`confos services` shows their enabled state and current PID. Enabled services run
as root with a fixed environment and restart after exit. This is a minimal service
manager. Native user units are the separate `user-unit` form above.
In 0.3, service children and SSH sessions inherit the same kernel confinement.
Rules are single `add rule inet confos input ...` statements (no semicolon,
newline, braces or includes), applied in name order. The base creates an accepting
input chain. This restricted rule language is an additional requirement.
Source 0.13 writes each rule's exact text without appending a name comment.
The base login/service locale is C.UTF-8; libc-bin supplies its pinned locale files
in every supported snapshot. /run and /var start with mode 0755. Standard /dev/fd,
/dev/stdin, /dev/stdout and /dev/stderr links support ordinary shell process substitution.

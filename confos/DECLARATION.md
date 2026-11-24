# Declaration syntax, revision 32 (source 0.32)

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
Every line is written by a person. No recording command is supplied.

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
are exposed; ID must be declared for info/run. Direct installation/configuration is
refused by this entry. Native Flatpak executes the install and launch operations;
launch requires an ordinary account. The user store is fixed to the immutable empty
/usr/lib/confos/flatpak-user directory so a user override cannot change that entry.
the read/run entry does not write declaration lines. General saved-code enforcement
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

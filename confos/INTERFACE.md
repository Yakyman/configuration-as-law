# ConfOS interface, revision 32

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

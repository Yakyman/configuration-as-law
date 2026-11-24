# ConfOS

ConfOS is an experimental operating system assembled from a person's declaration.
It starts with an empty filesystem and extracts pinned Debian 13 package payloads
and their dependencies. It does not run package installation scripts. Its own small
boot and application runtime is the genuine confos-runtime package of the declared
base release (matching VERSION), shipped in packages/ with fixed file metadata.
Its EFI program is supplied by the named confos-boot package, built from a pinned
GRUB release and copied byte-for-byte onto the disk.
The per-snapshot confos-initramfs package similarly supplies the exact boot archive
and native module indexes, built from pinned Debian inputs and authored early-init.
Release27 adds a source-built code-reader component for native Bash, Python
and Perl; release28 adds BusyBox ash/sh, awk and sed. Tested saved-code routes
are refused; other readers remain open.
Release29 supplies conditional native dash/mawk/gawk/sed/make overrides described
by static data in that component; optional executables disappear with their owners.
Release30 adds native Node and libnode readers, including startup snapshots,
package resolver settings, environment files and policy files.
Release32 adds exact-AppImage Neovim native code readers, a Lua loader override
and an immutable runtime entry, derived from the reader component's static data.
Release31 adds native Git code-configuration checks across its executable
and helper paths. Implementation coverage and open routes are in CODE-READERS.md.

On a Debian worker with apt, dpkg-deb, squashfs-tools, cpio, kmod,
libguestfs and QEMU/KVM installed, with rootless user/mount/PID namespaces enabled,
run `./build.sh DECLARATION OUTPUT.qcow2`. Staged tools run in a private chroot with
kernel-context mounts. Provide pinned inputs for pip/npm/compile declarations.
Flatpak bundles require their runtime
dependencies are separate lines. Development status is recorded in STATE.md.
AppImage lines extract checksum-pinned payloads and create immutable launchers.
Container lines pin OCI archives for native rootless Podman with read-only roots.
User-unit lines load exact native systemd service/timer files for an ordinary account.
LinuxGSM lines pin native launcher/game inputs for staged installation and updates;
game code remains immutable while logs and scratch records live in volatile storage.
Run `./boot.sh OUTPUT.qcow2 22401 2048 serial.log` to boot it. Add an account and
public login key in the declaration first. See INTERFACE.md and DECLARATION.md.

The root filesystem is read-only; material and records live on a separate disk
partition. `sudo confos apply` rebuilds the root from edited text and reboots;
`confos status` identifies the declaration in force after startup. No command adds
declaration lines for the person. STATE.md describes what has actually been run,
and IMPOSSIBLE.md records observed unmet requirements. This is a work in progress,
not an accepted implementation of the hypothesis. The independent cases provide
acceptance; smoke.sh is only the builder's short regression check.

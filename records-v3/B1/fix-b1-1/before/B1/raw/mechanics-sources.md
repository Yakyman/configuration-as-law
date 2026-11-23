# Mechanics source ledger

Access date: 2026-11-22 UTC. Documentation research only; no probe commands or outputs exist because documented behavior answered the mechanism questions.

- https://man7.org/linux/man-pages/man2/fsync.2.html — “an explicit fsync() on a file descriptor for the directory is also needed.”
- https://man7.org/linux/man-pages/man2/rename.2.html — “If newpath already exists, it will be atomically replaced”
- https://ostreedev.github.io/ostree/atomic-upgrades/ — “If the system crashes or you pull the power, you will have either the old system, or the new one.”
- https://ostreedev.github.io/ostree/deployment/ — “updating the bootloader is also delayed.”
- https://docs.kernel.org/6.12/admin-guide/cgroup-v2.html — “Killing a cgroup tree will deal with concurrent forks appropriately and is protected against migrations.”
- https://www.freedesktop.org/software/systemd/man/257/systemd.kill.html — “If set to none, no process is killed (strongly recommended against!).”
- https://man7.org/linux/man-pages/man2/unlink.2.html — “processes which have the object open may continue to use it.”
- https://man7.org/linux/man-pages/man2/mmap.2.html — “the file descriptor, fd, can be closed immediately without invalidating the mapping.”
- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html — “systemctl may be used to introspect and control the state”
- https://networkmanager.dev/docs/api/latest/nmcli.html — “create, display, edit, delete, activate, and deactivate network connections”
- https://www.netfilter.org/projects/nftables/manpage.html — “Check commands validity without actually applying the changes.”
- https://man7.org/linux/man-pages/man7/capabilities.7.html — “capabilities, which can be independently enabled and disabled.”
- https://www.debian.org/releases/trixie/release-notes/whats-new.en.html — “Linux kernel”; “6.12 series”; “Systemd”; “257”.

Version limits: Linux 6.12 and systemd 257 documentation directly checked. Debian 13 release notes identify families only. No running distribution, kernel package build, or composed transaction was measured.

- https://www.gnu.org/software/emacs/manual/html_node/emacs/Package-Installation.html — “then downloads and installs it.” Primary search result consulted after direct open timed out.

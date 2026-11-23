# Void installation choices

Recorded before installation; cutoff: 2026-11-23T01:19:00Z.

- Official current image: 20250202, x86_64 glibc base live image. The official download page offers base and Xfce images, and glibc and musl variants; the task fixes base/glibc/x86_64. https://voidlinux.org/download/
- Package source: Local, retaining the image's installer-selected packages. https://docs.voidlinux.org/installation/live-images/guide.html describes the Local and Network alternatives. No repository update is performed.
- Partitioning: BIOS, MBR, one ext4 root partition using the 24 GiB virtual disk. The installation guide states: “Void does not provide a preset partition scheme”. This explicitly requires a check choice. Same source, Partition section.
- Keyboard: us; timezone: Etc/UTC; ordinary login and descriptive name: user. The guide requires selecting keyboard, timezone and user details. Its prescribed default login is changed to user as the task requires. The default supplementary group selection includes wheel; the answer file retains that selection. Locale and hostname settings are omitted, preserving installer fallback behavior.
- Root and ordinary-user setup passwords: void-lab-install, limited to this isolated disposable lab. The installer requires passwords; there is no prescribed password value.
- GRUB: install onto /dev/vda, preserving graphical-terminal default. Services checklist is cancelled, preserving its existing selection.
- Instrument access only: a lab SSH public key is installed for user; the sshd service is enabled; a dedicated sudoers entry allows noninteractive root execution. These are explicit instrument additions after the unchanged void-installer completes.
- Unattended interface: a PATH-local dialog shim supplies Install, affirmative installation confirmation, default-preserving services cancellation, no reboot, then Exit. It does not save dialog text. The official program itself is executed unchanged. The recipe uses its configuration interface documented in the public upstream source: https://github.com/void-linux/void-mklive/blob/master/installer.sh .
- Initial transport: blind serial login uses the documented live root password. Bytes received from the console are discarded into /dev/null, never decoded or retained. The public serial setup implementation is https://github.com/void-linux/void-mklive/blob/master/dracut/vmklive/getty-serial.sh . Subsequent lab use is SSH.

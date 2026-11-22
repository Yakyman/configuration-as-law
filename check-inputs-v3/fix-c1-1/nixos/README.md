# Replacement NixOS installation input

This replaces the incomplete declaration capture in `C1/install/nixos/` without
modifying it. Release, ISO, top-level declaration, BIOS, 32 GiB virtio disk, two
vCPUs and 4 GiB RAM are unchanged. No extra packages or services are requested.
Original verified media and extracted boot files are reused read-only.

Source: https://nixos.org/manual/nixos/stable/#sec-installation-manual .
The documented generator precedes installation; `install.sh` copies its generated
hardware declaration to the output share immediately after generation, before
copying the top-level declaration and running `nixos-install`. This is capture of
an installation input, not inspection of an installed machine.

Server paths below are relative to the laboratory root. `prepare.sh` creates only
`C1/fix-c1-1/nixos/base-attempt2.qcow2`. `launch.sh` uses a free shared slot lock and the
original ISO's extracted kernel/initrd. Input share is read-only; the separate
output share retains the generated input and installation exit statuses. Installer
standard output and standard error go to `/dev/null`; the serial driver discards
console output. Both long-lived commands run as user service units.

Initial launch exited 127 before VM creation because the service lacked its
working directory; the driver exited 1 because no socket existed. Adding the
working directory corrected orchestration; no installation had started and no
probe of the installed system was repeated.

The first driver start after correcting the working directory raced socket
creation and exited 1 before sending installation commands. The driver now waits
for the socket before connecting. This corrected driver initiated installation
on the still-empty fresh disk.

The first installation exited 32 before hardware capture; only that exit status
was recorded, so its exact failed step is not established. A later direct mount
in the installer succeeded. The next recipe adds `udevadm settle` and stage
labels; the failed disk was removed and a fresh `base-attempt2.qcow2` created.
The driver now waits for an installer shell prompt, replacing its fixed delay:
on the second disk the initial command had been sent before shell readiness and
created no status record. Waiting for readiness allowed partition, format,
mount and generator to succeed. The generated input was saved before installation.
No installation package output was saved.

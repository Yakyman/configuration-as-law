# Experiments of assessment c2 (check 4) — expectations written before each run

Times UTC, 2026-11-22. VMs: `d4c2-nixos` (system `nixos`), `d4c2-guix` (system `guix`), created with the runner
`lab-fx-c1-1.sh` (SHA256 0439b403…34db, checked on the host) named by the final inputs. One experiment per fact.
Scripts: `raw/scripts/`; raw outputs: `raw/<id>-*.txt`.

Documentation already answers, so NOT probed: nix-env installs past configuration.nix (NixOS manual, Ad-Hoc Package
Management); accounts added by useradd survive activation on NixOS (option `users.mutableUsers`, default true);
`guix package` acts on per-user profiles beside the system packages (Guix manual 5.2, 11.x Globally-Visible
Packages); Guix accounts created or modified by useradd and similar commands exist until reconfiguration or reboot
(Guix manual 11.7). See `../ASSESS.md` for the quotes.

## N0 / G0 — which candidate built-in tools are present on the clean installation; declaration identity
Fact left open by the documentation: the release documentation does not list the programs of a default installation.
Expected N0: present: nixos-rebuild, nix-env, nix-shell, nix-channel, systemctl, useradd, usermod, userdel,
groupadd, gpasswd, passwd, iptables, ip, loginctl; absent: crontab. Root channel list names a nixos-26.05 channel.
SHA256 of /etc/nixos/configuration.nix = 45f4f0c5…9901 and of hardware-configuration.nix = cebc3637…d7d5 (inputs).
Expected G0: present: guix, herd, passwd, ip; useradd/userdel/gpasswd presence unknown (expected present, shadow in
base packages); absent: systemctl, crontab. SHA256 of /etc/config.scm = 442f088a…b886 (input).

## N1 / G1 — recorded lines in force after a completed application, including an immediate power cut (S3-3, S3-5)
Fact left open: the documentation describes what application does, not a record of the state after it.
Procedure: as root apply the unchanged declaration (`nixos-rebuild switch` / `guix system reconfigure
/etc/config.scm`), record exit status and output tail; immediately `kill` (SIGKILL of the VM) and `start`; then check
each recorded line of the declaration.
Expected: application exits 0 with no error; after the new boot every checked line is in force:
NixOS — kernel parameter console=ttyS0,115200n8 in /proc/cmdline; time zone UTC; locale en_US.UTF-8; DHCP client
enabled and an address on 10.0.2.0/24; account `user` exists, normal (uid ≥ 1000), member of wheel; root file system
on by-uuid 57eb3ffe… ext4; no swap; GRUB in the MBR of /dev/vda; x86_64.
Guix — host name cal; time zone UTC; locale en_US.utf8; console=ttyS0,115200n8 in /proc/cmdline; GRUB in the MBR of
/dev/vda; / on label root, ext4; account `user`, group users, supplementary wheel and netdev, password hash equal to the
declared one; DHCP client service running with an address on 10.0.2.0/24; agetty on ttyS0 present.

## N2 — a recorded line after a built-in account tool acts after application (NixOS only)
Fact left open: the NixOS manual says /etc/group is merged "on system activation" when users.mutableUsers is true,
but does not state what happens to a declared membership removed by an imperative command between activations.
(For Guix the manual answers it: 11.7 "modifications made by directly invoking commands such as useradd are lost upon
reconfiguration or reboot" — so not probed.)
Procedure: as root, after N1's application: `gpasswd -d user wheel`; record `getent group wheel` and `id -nG user`;
then restore with `gpasswd -a user wheel` (to keep the runner's sudo path) and record again.
Expected: gpasswd exits 0; after removal `user` is not in wheel (declared line `extraGroups = [ "wheel" ]` not in
force) and stays so with no application; after restore it is back.

## Results log (written after each run)

- N0 06:52Z: as expected, plus `nix` present and `nft` absent (`N0-output.txt`).
- G0 06:52Z: as expected; useradd, usermod, userdel, groupadd, gpasswd present; iptables, nft, loginctl, systemctl,
  crontab absent (`G0-output.txt`).
- N1 06:52–06:53Z: as expected in every checked line (`N1-output.txt`).
- N2 06:54Z: as expected. The script also re-read the state 30 s after the removal (written into the script before the
  run) (`N2-output.txt`).
- G1 06:52–07:02Z: NOT as expected. `guix system reconfigure /etc/config.scm` exited 1. The backtrace ends in
  `display-hint "Use @option{--allow-downgrades} to fo…"` followed by
  `In procedure terminal-window-size: Inappropriate ioctl for device`: reconfigure refused what it treats as a
  downgrade, and printing the hint then failed because output went to a file. This is a reported failed application;
  by S3-4 the previous declaration stays in force, and that is the installed `/etc/config.scm`, byte-identical to the
  file used (G0). The VM was killed at once (07:02:18Z) and started again; the lines were then checked against that
  declaration (`G1-output-part1.txt`, `G1-output-part2.txt`). No retry with other options: that would be a
  second probe of the same fact. In the check script, `getent` is absent on Guix, so the account lines failed; those
  checks were run again with `grep` on /etc/passwd, /etc/group, /etc/shadow (`scripts/G1c-account.sh`,
  `G1-output-part3.txt`), after the serial workaround was repeated (two root agettys, pids 356 and 357; 357 was
  stopped with `sudo kill -STOP` from tty1; screen `d4c2-s4.png`). Result: every checked line in force against the
  declaration in force (host name cal; UTC; LANG en_US.utf8; console=ttyS0,115200n8; GRUB in the MBR; / = vda1, label
  root, ext4; `user` uid 1000, group users, in wheel and netdev, password hash equal to the declared one; Shepherd
  services `networking`, `term-ttyS0`, `term-console` started; address 10.0.2.15/24).
- Cleanup: d4c2-nixos destroyed 06:54:40Z, d4c2-guix destroyed 07:04:30Z (`raw/vm-destroy-*.txt`); script copies on
  the host removed.

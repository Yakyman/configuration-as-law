# Experiments of assessment c2 (expected results written before each run)

Rule: an experiment only for a fact the documentation leaves open; one experiment per fact; raw commands and
output under `raw/`. Times UTC.

## E-N2 — NixOS, fact for P2 (written 2026-11-23T11:14:48Z by file time, before the run at 11:14:53Z guest clock)

Fact left open by the documentation: whether a recorded line of the declaration — here
`users.users.user.extraGroups = [ "wheel" ];` of the installed `/etc/nixos/configuration.nix` — stays in force
at a moment after a completed application when a built-in account-management program (`gpasswd`, shadow suite)
changes it, without writing directly to files; and what the next application does.

Steps (one root script, `raw/e-n2.sh`): print release; `nixos-rebuild switch` (application; exit status = its
report); `id -nG user`; `gpasswd -d user wheel`; `id -nG user`; `grep -c` of the declaration line (declaration
unchanged); `nixos-rebuild switch` again; `id -nG user`; restore with `gpasswd -a user wheel` if still absent.

Expected: first application exits 0; `wheel` present; `gpasswd -d` exits 0 and `wheel` absent afterwards while the
declaration still contains the line (recorded line not in force after a completed application, no breaking);
second application exits 0 and `wheel` is present again. If `nixos-rebuild switch` cannot run (no channel or
network), the application status is recorded as is and the clean installation's installation-time application is
the completed application.

Result (`raw/e-n2.out`, runner status 0): as expected. Application 1 `nixos-rebuild switch` status 0, "Done. The
new configuration is …"; `id -nG user` = `users wheel`; `gpasswd -d user wheel` status 0; then `users` only, while
the declaration line is unchanged (count 1); application 2 status 0; then `users wheel` again.

## E-G2 — Guix System, fact for P2 (written 2026-11-23T11:15:37Z, before the run)

Fact left open by the documentation: whether a recorded line of the declaration — here
`(supplementary-groups '("wheel" "netdev"))` of the account `user` in the installed declaration — stays in force at
a moment after a completed application when a built-in account-management program (`gpasswd`, shadow suite) changes
it, without writing directly to files. No reconfiguration is run (it would need substitutes from the network over the
slow serial transport); the completed application is the installation's `guix system init` and boot activation.

Steps (one root script, `raw/e-g2.sh`): print `guix --version` first line and the system profile; `id -nG user`;
`gpasswd -d user wheel`; `id -nG user`; the declaration's `supplementary-groups` line from `/etc/config.scm` (or
from the running system's configuration file); restore with `gpasswd -a user wheel`.

Expected: `wheel` present before; `gpasswd -d` exits 0; `wheel` absent afterwards while the declaration still records
it (recorded line not in force after a completed application, no breaking).

Result (`raw/e-g2.out`, runner status 0): as expected. `guix (GNU Guix) 1.5.0`; `/etc/config.scm` line 20
`(supplementary-groups '("wheel" "netdev")))`; `id -nG user` = `users wheel netdev`; `gpasswd` =
`/run/current-system/profile/bin/gpasswd`, `gpasswd -d user wheel` status 0; then `users netdev`; restored with
`gpasswd -a user wheel` (status 0).

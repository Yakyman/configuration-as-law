# Check 4 — assessment c2 of NixOS and GNU Guix System

Assessed 2026-11-22 UTC by c2, independently of c1. Inputs: `GATES/INPUTS-4-PUSHED` (commit 43594a47…), final input
file (not published: outside selected checks and direct evidence), installations exactly as selected there (NixOS 26.05.14979.94c3211b0ee8, Guix
1.5.0), runner `lab-fx-c1-1.sh` SHA256 0439b403…34db (verified on the host before use). Documentation quotes with
URLs: `raw/docs.md` (cited as D-…). Experiments with expectations written before the runs: `raw/EXPERIMENTS.md`;
outputs `raw/N0-output.txt`, `raw/N1-output.txt`, `raw/N2-output.txt`, `raw/G0-output.txt`, `raw/G1-output*.txt`.
Instrument defect on Guix (two gettys on ttyS0) and its workaround: `raw/instrument-guix-serial.md`.

## Mapping common to the cases

**Declaration (S2.1-1, S2.1-2).**
- NixOS: `/etc/nixos/configuration.nix` together with `/etc/nixos/hardware-configuration.nix` — the files the
  installation input designates ("The NixOS declaration includes both configuration.nix and the exact generated
  hardware-configuration.nix", `inputs-check-4.md`); D-N1: "The file /etc/nixos/configuration.nix contains the current
  configuration of your machine." On the clean installation both files have the input checksums (`raw/N0-output.txt`).
- Guix: `/etc/config.scm`, the saved `config.scm` of the input (checksum equal, `raw/G0-output.txt`).

**Application and its success report (S2.1-5, S3-3).**
- NixOS: `nixos-rebuild switch` — "build the new configuration, make it the default configuration for booting, and try
  to realise the configuration in the running system" (D-N1). Report: the command ends with "Done. The new
  configuration is …" and exit status 0 (`raw/N1-output.txt`).
- Guix: `guix system reconfigure /etc/config.scm` — "Build the operating system described in file, activate it, and
  switch to it" (D-G1). Report: exit status 0; a non-zero exit is a failure report. On the clean installation the
  unchanged declaration's reconfigure exited 1 (`raw/G1-output-part1.txt`), so by S3-4 the declaration in force stayed
  that of the installation (`guix system init` of the same `config.scm`, (not published: outside selected checks and direct evidence)).

**Built-in tools (S2.1-6, S3-6…S3-8), decided from each program's own documentation; presence on the clean
installation from `raw/N0-output.txt`, `raw/G0-output.txt`.** Examined programs only; this is not an inventory of all
programs.

| System | Program | Documented purpose (source) | By S3-6/S3-7 |
|---|---|---|---|
| NixOS | `nixos-rebuild` | builds and realises the configuration (D-N1) | built-in tool; changes through the declaration |
| NixOS | `nix-env` | "manipulate or query Nix user environments" (D-X1); "install, upgrade and uninstall packages" (D-N2, D-N3) | built-in tool: package manager |
| NixOS | `systemctl` | "Control the systemd system and service manager" (D-M4) | built-in tool: service manager |
| NixOS | `useradd`, `userdel`, `usermod`, `groupadd`, `gpasswd` | create / delete user accounts; administer /etc/group (D-M1…D-M3, D-N4) | built-in tools: account and rights management |
| NixOS | `nix-shell` | "start an interactive shell based on a Nix expression"; builds the dependencies of a derivation, `-p` packages (D-X2) | **not decided — counterexample by S3-8, recorded, not decided** (see NixOS × P4) |
| Guix | `guix` (`guix package`, `guix install`) | "the tool that allows users to install, upgrade, and remove packages" (D-G2, D-G3) | built-in tool: package manager (`guix system` is the application) |
| Guix | `herd` | lists services, starts and stops them (D-G6) | built-in tool: service manager |
| Guix | `useradd`, `userdel`, `usermod`, `groupadd`, `gpasswd` | as above (D-M1…D-M3); D-G5 names useradd as a command that creates or modifies accounts | built-in tools: account and rights management |

None of these is a general-purpose program of S3-7, so a change made with them is not breaking (S2.1-7: breaking is
a change "outside the built-in tools").

**Time scope (S2.3-1).** "The properties concern the computer after a completed application of the declaration,
provided there was no breaking." Read literally, this covers the computer at any moment after the last completed
application while it is the declaration in force (S3-3), not only the moment of the success report; restricting it
to that moment would add a word ("immediately") that the sentence does not contain. The alternative reading is
written down for the author in `QUESTIONS.md`; the facts for both moments are given below.

## NixOS × P1

**Demand.** S2.3-4: everything that must be recorded (Section 2.2) and is in force is recorded in
configuration.nix/hardware-configuration.nix, after a completed application without breaking (S2.3-1). Accounts must
be recorded (S2.2-15); a program in the home directory or a user profile must be recorded (S2.2-9); an account is in
force when it exists, a program when it can be started (S2.1-3).

**Facts.** D-N5: `users.mutableUsers` "Default:true" (the declaration does not set it); "If set to true, you are free to
add new users and groups to the system with the ordinary useradd and groupadd commands. On system activation, the
existing contents of the /etc/passwd and /etc/group files will be merged with the contents generated from the
users.users and users.groups options." D-N4: "to create a user account named alice: # useradd -m alice". `useradd` is
present (`raw/N0-output.txt`). Also D-N3: `nix-env -iA …` installs a package into a per-user or default profile, not
into configuration.nix.

**Decision: does not have.** An account created with the built-in tool `useradd` exists (in force) and is not in
the declaration; by D-N5 the next application merges /etc/passwd instead of replacing it, so the account stays in
force after a completed application, with no breaking. This holds under both readings of the time scope. One
established counterexample suffices.

## NixOS × P2

**Demand.** S2.3-5: everything recorded is in force as its line requires, after a completed application without
breaking (S2.3-1), checked against the declaration in force (S3-3) and also after an immediate power cut and new boot
(S3-5).

**Facts.**
- N1 (record): `nixos-rebuild switch` exit 0, "Done. The new configuration is …"; SIGKILL of the VM at once
  (06:52:53Z), new boot; every checked line in force: `console=ttyS0,115200n8` in /proc/cmdline; time zone UTC; LANG
  en_US.UTF-8; dhcpcd enabled, address 10.0.2.15/24; `user` uid 1000, normal, in wheel; / = vda1 = by-uuid 57eb3ffe…,
  ext4; no swap; GRUB in the MBR; x86_64; booted system = the applied generation (`raw/N1-output.txt`).
- N2 (record): after that application, the built-in tool `gpasswd -d user wheel` (exit 0) removed the declared
  membership (`extraGroups = [ "wheel" ]`, the right to become superuser, S2.2-15); `wheel:x:1:` and `id -nG user` =
  `users`, unchanged 30 s later with no application; then restored with `gpasswd -a` (`raw/N2-output.txt`).

**Decision: does not have.** After a completed application (N1) and with no breaking (gpasswd is a built-in tool of
account and rights management, D-M3, so S2.1-7 does not apply), the recorded line `extraGroups = [ "wheel" ]` was not
in force (N2). S2.3-5 is violated in the time scope of S2.3-1 read literally. Examined: the state right after the
success report and after a power cut (N1) satisfied every checked line; under the alternative reading
(`QUESTIONS.md`) the decision would rest on N1 alone.

## NixOS × P4

**Demand.** S2.3-6, S2.3-7: no path for changing, past the declaration, anything that must be recorded; built-in tools,
also as superuser, change it only through the declaration ("an installer does not install a program past the
declaration but adds it to the declaration").

**Facts.** D-N2: "Ad hoc, where you install, upgrade and uninstall packages via the nix-env command. … It’s the only
choice for non-root users." D-N3: the package "ends up in /nix/var/nix/profiles/per-user/username/profile" (or the
default profile as root); nothing is added to configuration.nix. D-N4/D-N5: `useradd`, `userdel`, `usermod`, groupadd
are available while `users.mutableUsers` is true (default). Presence: `raw/N0-output.txt`. Record N2: `gpasswd`
changed a recorded right past the declaration.

**Decision: does not have.** The built-in package manager `nix-env` installs a program (to be recorded, S2.2-9) past
the declaration; the account tools create, delete and modify accounts past it (N2 is one recorded instance).
S2.3-7 is violated. Recorded, not decided: `nix-shell` (D-X2) has a documented purpose — building dependencies and
starting a shell with packages (`-p`) made available — and S3-6 does not decide whether a program that makes packages
runnable without installing them in a profile is a "package manager"; by S3-8 this is a counterexample to the
definitions.

## Guix × P1

**Demand.** As for NixOS × P1, with the declaration /etc/config.scm.

**Facts.** D-G2: `guix package`/`guix install` install packages in "a user profile … $HOME/.guix-profile … The
command operates only on the user’s own profile". D-G4: the system's `packages` field is visible "in addition to the
per-user profiles". D-G5: "account or group creations or modifications made by directly invoking commands such as
useradd are lost upon reconfiguration or reboot" — that is, they exist until then. `guix`, `useradd` present
(`raw/G0-output.txt`).

**Decision: does not have.** After a completed application, a program installed with the built-in package manager
`guix install` is in the user's profile and PATH (can be started, in force) and is not in config.scm; an account
created with `useradd` exists until the next reconfiguration or reboot and is not in config.scm. Neither is breaking.
Both violate S2.3-4 in the time scope of S2.3-1 read literally. Not established: whether a per-user package remains
in force across a later reconfiguration (no source examined states it; not probed, since the decision does not
depend on it under the literal reading — see `QUESTIONS.md`).

## Guix × P2

**Demand.** As for NixOS × P2, with `guix system reconfigure` as application.

**Facts.**
- G1 (record): `guix system reconfigure /etc/config.scm` exited 1. It refused what it treats as a downgrade (hint
  "--allow-downgrades"), and printing the hint then failed with "terminal-window-size: Inappropriate ioctl for device".
  That is a failure report, so by S3-4 the declaration in force stays the installed, byte-identical `/etc/config.scm`.
  The VM was killed at once and booted again, and every checked line was in force: host name cal; UTC; LANG
  en_US.utf8; console=ttyS0,115200n8; GRUB in the MBR; / = vda1, label root, ext4; `user` uid 1000, group users, in
  wheel and netdev, password hash equal to the declared one; `networking` (DHCP client), `term-ttyS0` and
  `term-console` started; address 10.0.2.15/24 (`raw/G1-output-part2.txt`, `raw/G1-output-part3.txt`).
- D-G5: "account or group creations or modifications made by directly invoking commands such as useradd are lost
  upon reconfiguration or reboot" — a modification of a declared account made with the account tools stands until
  the next reconfiguration or reboot. `gpasswd`, `usermod` present (`raw/G0-output.txt`). Not probed: the
  documentation answers it.

**Decision: does not have.** After a completed application, a built-in account tool (e.g. `gpasswd -d user wheel`,
`usermod`) can modify the declared account `user` (supplementary groups wheel, netdev); by D-G5 that modification
stays in force until reconfiguration or reboot, so the recorded line is not in force, with no breaking. S2.3-5 is
violated in the time scope of S2.3-1 read literally. Examined: the state after a power cut, checked against the
declaration in force (G1). No reconfigure that reported success was obtained (`QUESTIONS.md` items 1 and 4).

## Guix × P4

**Demand.** As for NixOS × P4.

**Facts.** D-G2, D-G3: `guix package` "is the central tool to manage packages … It operates on the per-user profiles,
and can be used with normal user privileges"; it writes $HOME/.guix-profile, not config.scm. D-G5: useradd and similar
commands create or modify accounts outside the declaration (until reconfiguration or reboot). D-G6: `herd stop`
stops services. Presence: `raw/G0-output.txt`.

**Decision: does not have.** The built-in package manager installs programs that must be recorded (S2.2-9) without
adding them to the declaration, and the account tools create and modify accounts past it; S2.3-7 is violated. No
program among those examined was left undecided by S3-6 (the shell feature `guix shell` belongs to the program
`guix`, a package manager by its documentation).

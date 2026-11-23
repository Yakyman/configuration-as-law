# c2, part 3 of A1 — notes

Input: `../in/part-3.tsv` (989 rows, all from the NixOS testbed). Output: `part-3.tsv`.
Script: `scripts/classify_part3.py` (rules plus row-by-row tables); check: `scripts/verify_part3.py`;
sample for hand checks: `scripts/sample_rules.py`. Documentation fetched (NixOS module sources, public):
`raw/nixpkgs/` (from https://github.com/NixOS/nixpkgs, branch master).

Decided only from Section 2.2 and S3-1/S3-2. Nothing was removed; the removal test of S2.2-2 is applied by reasoning.
A row whose `members` is 1 is decided as one object even when it holds several files: if removing the whole object
stops something and no exemption covers it, it is MUST. `S2.2-2` ("The test is removal") is read as the test in
both directions: when removal stops nothing and makes nothing impossible, the decision is NOT.

## Scripted rules (homogeneous kinds)

Each rule follows from the cited sentences; 10 rows per rule were checked by hand and fit.

| Rule | Applies to | Decision | Sentences | Hand-checked ids |
|---|---|---|---|---|
| R1 documentation | store objects named `*-man`, `*-doc`, `*-info`, `nix-manual-*`, `nixos-manual-html`, `nixos-configuration-reference-manpage` (67) | NOT | S2.2-3, S2.2-4 | nixos-0177932701 nixos-0a13ae5a7a nixos-416ffb5472 nixos-7200207b9e nixos-968d8c6726 nixos-9c16488f61 nixos-a14447ec97 nixos-b25ffba23e nixos-bda7e60399 nixos-d5ed866a9f |
| R2 unit file | store objects `unit-*` except `unit-script-*` (80) | MUST | S2.2-1, S2.2-2 | nixos-5509f9e3c7 nixos-5d74d8f865 nixos-73a2f6b715 nixos-8ae37bbede nixos-b5b2489160 nixos-dabe515248 nixos-dbe5c3e289 nixos-e8accb85d9 nixos-ee951771a5 nixos-fa7ae4e8c6 |
| R3 unit script | store objects `unit-script-*` (12) | MUST | S2.2-10, S2.2-13 | nixos-0e91f5020a nixos-231a055875 nixos-2f63f83cb7 nixos-566881f135 nixos-76aab70b52 nixos-76b7740691 nixos-884611d475 nixos-a28ce7d679 nixos-c9275ff52c nixos-f22aa42b3a |
| R4 restart triggers | store objects `X-Restart-Triggers-*` (13) | NOT | S2.2-2 | nixos-12077741ee nixos-37c734ac44 nixos-492095dabf nixos-9989d9c066 nixos-99dc8e74de nixos-a738960c81 nixos-aca93a4a49 nixos-cf6b4465c0 nixos-ddcd5982bd nixos-ed89bf30d9 |
| R5 PAM | store objects `*.pam` (20) | MUST | S2.2-15, S2.2-2 | nixos-092af32a4b nixos-26f82d689d nixos-2c18b0fa79 nixos-70030c0912 nixos-7478014d7a nixos-8e0557dedc nixos-9b832188b2 nixos-b862214766 nixos-e224f7015d nixos-fe5462495e |
| R6 program/library | every other store object of the system closure not in the row tables (297: binaries, libraries, wrappers, kernel, initrd) | MUST | S2.2-2, S2.2-9, S2.2-10 | nixos-67f8ba787a nixos-82edfa09d9 nixos-92635149c3 nixos-95f66f25a0 nixos-9ee574bb9a nixos-a7b34c54bf nixos-b0c5a03e2f nixos-da26d00a9b nixos-e85650147f nixos-fc8836fa30 |
| R7 loaded unit | kinds `system-unit`, `user-unit` with a unit file (139) | MUST | S2.2-1, S2.2-2 | nixos-0f129a3ae1 nixos-2e48b3e05f nixos-31e52e5ea2 nixos-45d171a6ca nixos-5b7d77ae5d nixos-74749c1401 nixos-7abafbc845 nixos-7c603aff27 nixos-9cb1a3f789 nixos-feed84b43d |
| R8 kernel module | kind `kernel-module` (92) | MUST | S2.2-10, S2.2-2 | nixos-059d892980 nixos-179dc4c0ad nixos-22f28dcc06 nixos-3447cda9d6 nixos-565f1af2e2 nixos-6e6c501a44 nixos-7fdc5c58fa nixos-85f23d3cfe nixos-9cde69ca11 nixos-da0ca0afae |
| R9 process | kind `process` (19) | MUST | S2.2-9 | nixos-18a2277378 nixos-344126e1ba nixos-4bb4fc6dbf nixos-633b8ceb2c nixos-68eab14191 nixos-791fcf298c nixos-89ce5c5668 nixos-8d6e82c019 nixos-ab5afd3d29 nixos-d59e2c228f |
| R10 account | kind `account` (12) | MUST | S2.2-15 | nixos-1525133242 nixos-27d89cb149 nixos-54ef0687f4 nixos-96a19ba1e6 nixos-9911292f99 nixos-af2a58bec6 nixos-cbaf0b4232 nixos-dbea3590f8 nixos-e7927b082e nixos-ee17e5a4df |

Why each rule follows from the text:
- R1: man/info/HTML pages are documents; S2.2-4 says documents need not be recorded because after removal "only
  the content itself is unavailable".
- R2, R7: a unit file is what lets systemd start a service, mount, socket or target. Removing it makes starting the
  unit impossible (S2.2-2), and its effect reaches beyond systemd, so S2.2-7 does not apply.
- R3: shell scripts executed by an interpreter (S2.2-10, S2.2-13).
- R4: the nixpkgs source (`nixos/lib/systemd-lib.nix`: `X-Restart-Triggers = "${pkgs.writeText
  "X-Restart-Triggers-${name}" ...}"`) shows that only the file's path is written into the unit file. No program
  reads the file while the system runs, so removing it stops nothing.
- R5: PAM files hold authentication rules, including whether password login is allowed and who may use su/sudo
  (S2.2-15). Removing one makes that program's login path impossible (S2.2-2).
- R6: programs (S2.2-9) and libraries whose code programs run with their own rights (S2.2-10).
- R8: kernel modules are code that the kernel runs with its own rights (S2.2-10).
- R9: S2.2-9, "a program that runs on the computer must be recorded".
- R10: S2.2-15, "accounts ... must be recorded".

## Row-by-row decisions (non-homogeneous) — recurring readings

- Settings read by several programs (fstab, nsswitch, hosts, sysctl.d, modprobe.d, login.defs, locale, CA bundles,
  tzdata, and similar): S2.2-7 exempts only a setting "in force only inside one program", so it does not apply.
  Removal changes what the computer does. Decision: MUST.
- Settings that affect only one program's own interface (nanorc, man_db.conf, lessconfig, issue, GRUB theme, GRUB
  font): NOT under S2.2-7.
- HOLE, S2.2-7 vs S2.2-1/S2.2-2: a setting read by one program whose effect reaches beyond that program. Examples:
  journald/logind/oomd/sleep/timesyncd/coredump/system/user .conf files, presets, nix.conf, the flake registry,
  dhcpcd.conf, resolvconf.conf, nscd.conf, lvm.conf, fuse.conf, ssh_config, ssh_known_hosts, useradd defaults,
  logrotate.conf, tmpfiles.d, binfmt.d, modules-load.d, the D-Bus configuration, udev rules, switch inhibitors,
  generator environment, shutdown-ramfs contents, environment.d, nix-defexpr, and nix-channels. The text allows two
  readings of "in force only inside one program": (a) read by only one program, which gives NOT; (b) its effect
  stays inside that program's own interface, like the browser examples, which gives MUST through S2.2-2. No
  sentence chooses between them.
- HOLE, appearance: icon theme, sound theme, DejaVu fonts, and fontconfig configuration are shared by many programs.
  S2.2-7 covers only one program's theme, and the text does not say whether shared appearance counts as behaviour
  under S2.2-1.
- HOLE: the Nix database (`/nix/var/nix/db`). S2.2-4 exempts "the contents of databases", but removing this one
  makes package operations impossible (S2.2-2).
- HOLE: `/etc/nixos`, the system's own configuration. Removing it makes rebuilding impossible, but the text does not
  say whether the declaration itself must be recorded.
- HOLE: device units (system and user view). They exist only as systemd's reflection of kernel devices, so there is
  no object to remove apart from the hardware.
- UNKNOWN (S3-2): the store paths named only `systemd`, `hostname`, `getty` (2), and `multiuser.nix`, `sandbox.nix`,
  `relaxedsandbox.nix`. Their content is not in the inventory and no source was found. Also `linux-headers-static`
  and `zlib-static`, for which no run-time user was established. Also `/etc/mtab` and `/var/lock`, for which it was
  not established whether any program on the machine uses the legacy path.
- MIXED: `nixos-bfd49e603a`, the store outside the system closure. MUST: the user-profile program (hello) and the
  root channel nixpkgs. NOT: .drv files, sources, and build-time outputs, which are re-fetched or rebuilt on demand
  (S2.2-5).
- Regenerated identifiers and state: machine-id, dhcpcd DUID/lease, systemd random seed/clock/timer stamps, and the
  linger flag are recreated by their programs, so removal is negative under S2.2-2. Decision: NOT. SSH host keys
  sit inside `/etc/ssh`, which is MUST as a whole because of the authorized keys and sshd_config (S2.2-15).
- `/home/census/.vimrc`: NOT. It is editor code (S2.2-10), but no vim is installed (`../in/raw/nixos/system-closure.txt`
  and `user-closure.txt` contain none), so no program runs it.
- Unit names with no unit file (`*.not-found`): NOT. There is nothing to remove and nothing stops.

Doc sources used for specific rows (all at https://github.com/NixOS/nixpkgs/blob/master/):
`nixos/modules/system/activation/switchable-system.nix` (inhibitors), `nixos/modules/services/hardware/udev.nix`
(udev-path, firmware, hwdb.bin, udev-rules), `nixos/modules/system/boot/stage-2.nix` (local-cmds),
`nixos/modules/services/networking/dhcpcd.nix` (migrate-dhcpcd), `nixos/modules/config/console.nix` (console-env),
`nixos/modules/config/networking.nix` (hosts, `netgroup.text = lib.mkDefault ""`),
`nixos/modules/system/boot/kernel.nix` (nixos.conf = modules-load.d),
`nixos/modules/services/networking/ssh/sshd.nix` (sshd.conf-final, ssh-root-provision), `nixos/lib/systemd-lib.nix`
(X-Restart-Triggers).

# D1 / c2 / part fedora — notes

Classification c2 of `../in/part-fedora.tsv` (5887 rows). Output: `part-fedora.tsv`. Working files: `fedora-work/`
(scripts, decision tables, raw dumps). Only Sections 2.2 and 3 of `../../TEXT.md` (with S2.1-3 where it names in-force
objects) were used. Nothing was removed anywhere; no probe was run on any machine.

## Sources of "what the object does"

- Inventory files under `D1/in/raw/fedora/raw/` (accounts, groups, units, processes, modules, drivers, ports, nftables,
  NetworkManager, sudo, polkit, containers, flatpak).
- The rpm file ownership query of the inventory returned nothing (`113-ownership-rpm.out` is empty). File lists,
  summaries and dependencies of every installed rpm were therefore taken from the public Fedora 45 repository metadata
  (`releases/45/Everything` and `updates/45/Everything` at https://dl.fedoraproject.org/pub/fedora/linux/), matched by
  name, arch, version and release (1976 of 1977 matched exactly; `gpg-pubkey` is not a repository package). Extract:
  `fedora-work/raw/fedora-rpm-meta.jsonl.gz`; per-package category: `fedora-work/raw/rpmcat.tsv`. Each rpm row cites
  `https://packages.fedoraproject.org/pkgs/<source>/<name>/` as basis.
- Every rpm is listed twice by the inventory (root and user query of the same rpm database); both rows of one package
  get the same decision.
- Documentation quoted for rules: groupadd(8) "creates a new group account"
  (https://man7.org/linux/man-pages/man8/groupadd.8.html); polkit(8): actions "correspond to operations that clients can
  request the mechanism to carry out", with implicit authorizations `allow_any/allow_inactive/allow_active`
  (https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html); systemctl(1) unit-file states
  (https://www.freedesktop.org/software/systemd/man/latest/systemctl.html); flatpak-metadata(5) `versions`
  (https://docs.flatpak.org/en/latest/flatpak-command-reference.html), which does not say which of several installed
  branches of one extension is mounted; x86 microcode loader disabled when the CPUID hypervisor bit is set
  (https://git.zx2c4.com/linux-rng/plain/arch/x86/kernel/cpu/microcode/core.c).
- Hardware of the machine, from `078-driver.out` and `077-module.out`: i440fx/PIIX chipset, virtio net and block,
  bochs display, ATAPI CD, no sound card, no wireless, no GPU needing firmware, no EFI device. Boot mode (BIOS or
  UEFI) is not recorded anywhere in the inventory.

## Reading applied throughout

- S2.2-2 is read as deciding both ways: if removal stops nothing and makes nothing impossible, the object need not be
  recorded. Basis: S2.2-2 calls removal "the test", and S2.2-4/S2.2-5 justify their exemptions by exactly this outcome.
- S2.2-3 to S2.2-7 are read as exceptions to the test (otherwise S2.2-7 could never apply: removing a browser's home
  page also changes what the browser does). A data file read as values is a setting (S2.2-13); it is exempt by S2.2-7
  only if it is in force inside one program; read by several programs it is not exempt.
- Where S2.2-4 names the category ("the contents of databases") but its stated rationale ("the computer does and can do
  the same") is false for the object, the case is a HOLE: the text does not say whether the list or the rationale
  defines content.

## Scripted rules (each checked by hand on the ids in `fedora-work/raw/handcheck-ids.txt`, listed by rule there)

| Rule | Kind / selector | Decision | Sentences |
|---|---|---|---|
| R-ACCOUNT | L1:account | MUST | S2.2-15 |
| R-GROUP | L1:group (group account per groupadd(8)) | MUST | S2.2-15 |
| R-ACCESS | L1:access-rule (sudo `(ALL) ALL`) | MUST | S2.2-15 |
| R-PORT | L1:port | MUST | S2.2-15 |
| R-FW-RULE | L1:firewall-rule | MUST | S2.2-15 |
| R-FW-OBJ | firewall chain/table/ct helper (hold rules) | MUST | S2.2-15, S2.2-2 |
| R-PROCESS | L1:process; pids without exe link were printed on one line with the next process by the listing script | MUST | S2.2-9, S2.2-12 |
| R-MODULE | loaded kernel module (kernel code with kernel rights) | MUST | S2.2-10, S2.2-2 |
| R-DRIVER | device bound to a kernel driver | MUST | S2.2-10, S2.2-2 |
| R-POLKIT | polkit action declaration | MUST | S2.2-1, S2.2-2, S2.2-15 |
| R-SERVICE | loaded system/user service | MUST | S2.1-3, S2.2-1, S2.2-2 |
| R-SERVICE-NF | service `not-found` (a referenced name without unit file) | NOT | S2.2-1, S2.2-2 |
| R-UNITFILE | unit file in any present state (alias, static, indirect, disabled, enabled, enabled-runtime, generated); masked would be HOLE but none occurs | MUST | S2.1-3, S2.2-1, S2.2-2 |
| R-TIMER | system/user timer | MUST | S2.1-3, S2.2-1, S2.2-2 |
| R-NETWORK | NetworkManager profile: Wi-Fi by S2.2-14; others because addressing/routing depend on them | MUST | S2.2-14 / S2.1-3, S2.2-1, S2.2-2 |
| R-LINK | network interface listed by networkctl | MUST | S2.2-1, S2.2-2 |
| R-RPM-CODE | rpm whose file list contains executables, libraries, kernel modules, interpreted code, EFI binaries, generators, profile.d or dracut scripts (paths under /usr/share/doc, licenses, man, help excluded) | MUST | S2.2-2, S2.2-9, S2.2-10 |
| R-RPM-FONT | `google-noto-*-fonts`, `urw-base35-*-fonts` without code | MUST | S2.2-1, S2.2-2, S2.2-7, S2.2-13 |
| R-RPM-META | `default-fonts-*` (only an AppStream metainfo file) | NOT | S2.2-1, S2.2-2 |

The R-RPM-CODE hand check also opened the file lists of the ten sampled packages (each contains binaries, libraries
or scripts). Code packages that need another answer are overridden row by row (below).

## Decided row by row

All 374 rpm packages without code, the rpm packages with special code (EFI, guest firmware, browser-confined help),
the 7 Flatpak rows, container and image. Decisions with sentences and reasons: `fedora-work/tables/rpm-manual.tsv`
(using the shorthands of `fedora-work/tables/macros.tsv`) and `fedora-work/tables/flatpak.tsv`. Reverse
dependencies used to tell one-program from several-program data: repository metadata `requires` tables.

## HOLE and UNKNOWN cases (rows; each package counts twice)

- HOLE 44 — firmware for absent hardware (linux-firmware and split firmware packages, CPU microcode, b43): S2.2-16
  requires device firmware the system can change; the removal test changes nothing on this machine unless attachable
  devices count; the text decides neither.
- HOLE 6 — device-specific data for absent hardware (libwacom-data, alsa-ucm, usb_modeswitch-data): the removal test
  does not say whether devices that could be attached count.
- HOLE 14 — databases read by several programs (tzdata, ncurses-base terminfo, publicsuffix list, osinfo-db,
  gweather-locations and -common, mobile-broadband-provider-info): S2.2-4 list vs. its rationale.
- HOLE 10 — guest firmware run inside QEMU (seabios, seavgabios, ipxe ROMs, OVMF, EFI shell): S2.2-11 vs. S2.2-2.
- HOLE 4 — program pictures (fedora-logos, adwaita-icon-theme-legacy): the text does not say whether pictures shown by
  programs are content (S2.2-4) or what the programs depend on (S2.2-2).
- UNKNOWN 14 — UEFI boot binaries and capsule-update images (shim, grub2-efi, cdboot, fwupd capsule data): boot mode not
  established.
- UNKNOWN 2 — the two installed branches of the Flatpak GL extension: documentation does not say which is mounted.

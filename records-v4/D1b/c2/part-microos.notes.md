# c2, part microos: notes

2026-11-23 UTC. Input `D1b/in/part-microos.tsv`, 747 rows. Inventory files read from `D1b/handoff/microos/`.
Scripts are in (not published: scratch) ((not published: orchestration or scratch), `units.py`, (not published: orchestration or scratch), `classify.py`, (not published: orchestration or scratch), `verify.py`, `handcheck.py`).

## Facts about the machine used throughout

- The running root is btrfs snapshot 2; `/etc` is the subvolume `@/.snapshots/2/snapshot/etc` mounted at `/etc`
  (`raw/0155-s4-microos-mounts.out`, `raw/0156-s4-microos-subvolume.out`). The `/etc` subvolume was created
  2026-11-23 07:56:39 UTC as a snapshot of the `/etc` subvolume of snapshot 1 (Parent UUID, `raw/0156`).
- `/.snapshots/1/snapshot` is the older root snapshot 1. It has its own RPM database; its file list, sizes, digests and
  modes are in `raw/0062-s4-snapshot-rpm.out`, and the comparison of each stored member with it is in
  `s4-microos-snapshot-files.tsv`.
- Enablement and alias links of units in `/etc/systemd/system` are separate inventory objects (stored groups
  `/etc/systemd/system/*.wants` etc. in `objects.tsv`), so an `L1:unit-file` row stands for the unit file that
  `systemctl list-unit-files` lists, not for its enablement.

## Rules applied by script

**R1 — package files in snapshot 1** (456 rows → `INSTALLED-PACKAGE`; S8.2-7, S8.2-8, S8.2-16).
A stored group or a single code row whose every entry lies under `/.snapshots/1/snapshot/` and is either a regular file
whose comparison with the snapshot-1 RPM database is `equal` and whose mode equals the mode in that database, or a
directory listed in that database (`directory-membership-only`) with an equal mode. Such an entry “was obtained as part
of” a package installed on the computer (the package is recorded as installed in the RPM database of that root on this
disk) “and remains as received”: question 1 answers yes and decides, whether or not the file is code (the order of
S8.2-6). The line is the package's (S8.2-16). Ownership of entries is not compared by any inventory table, for files or
directories; the inventory's own fact for “changed since installation” is content (and here mode).
Hand-checked: d1b-microos-95747cc2f5a7b9fcd729b97e, d1b-microos-59dbb4574ca756e67cf11110,
d1b-microos-61e2e158bd6aa4e1117a6e3c, d1b-microos-abe6ebf035df3f1573703d40, d1b-microos-e497e7c25f6e6792e8685786,
d1b-microos-b9e9d50175215dac89b1df64, d1b-microos-76d1b9d2598ea072a9193040, d1b-microos-e018af2544e059c6f93dcfc8,
d1b-microos-682e28aa5d10dfa5fa12406f, d1b-microos-5d8ca9b40a13e612f9e1ed86 (full digest of each member equals the
`raw/0062` digest; mode equals the `raw/0062` mode).

**R2 — unit files from packages** (255 rows → `INSTALLED-PACKAGE`; S8.2-7, S8.2-8, S8.2-16).
An `L1:unit-file` or `L1:user-unit-file` row whose selected unit properties (`s4-microos-unit-selected.tsv`, query exit 0)
name a FragmentPath, drop-ins and source files that are all package files recorded `unchanged` in `package-files.tsv`;
for an alias row, the alias name itself must also be a package file recorded `unchanged` in the unit directory.
The unit file is a default setting value obtained with the package and remains as received: question 1 decides.
Hand-checked: d1b-microos-bfe7776470af255d18edaf17, d1b-microos-be1083c983eef45e1beb1744,
d1b-microos-1ac18ba13c0491664d3ace62, d1b-microos-7f5f7f9871694866c757fb2e, d1b-microos-263a88e4552aa12f19cfd8f9,
d1b-microos-4728d3d635adfcf9feb69fa7, d1b-microos-f4da1cb3ef270c4a4cb83a01, d1b-microos-a8fbbb56d14e7ed227b2b125,
d1b-microos-0122332f4e2ff7a78bb0b6c4, d1b-microos-edbf48bc2948213f33e72e79.

**R3 — system accounts and groups** (22 rows → `UNKNOWN`; S8.2-11, S8.2-13, S8.2-17).
Every account and group row of this part has a definition in a packaged, unchanged `/usr/lib/sysusers.d/*.conf`
(`s4-microos-sources.tsv`). An account is a setting (S8.2-13). Whether its record was created from that package default
during installation (S8.2-17: `SETTING-DEFAULT`) or chosen by a person (`SETTING-OWN`) depends on the creation event,
which the inventory does not record (“no per-object chooser-event table is emitted”, `S4/COLLECT.md`). Package
scriptlet text that would create such accounts is source text, not an execution event.
Hand-checked: d1b-microos-c66c458f233bdb6b71f4070d, d1b-microos-d0539891a063419a85b5d842,
d1b-microos-66d0e9ea25ab679e8e06236b, d1b-microos-f7b1d820eddaaeef43091105, d1b-microos-a793e6e9a67d825a8471403f,
d1b-microos-b69cc83687bff05e397c2916, d1b-microos-0a3a40b7fc3652cc69a3cce5, d1b-microos-207ead305cdde7ba1031464a,
d1b-microos-62e69634eb677cc7b715d241, d1b-microos-3663e1d2597d977b6b38e435.

## Rows decided one by one (14)

- Five alias rows whose alias name is a link in `/etc/systemd/system` or `/etc/systemd/user`
  (`s4-microos-unit-links.tsv`), not a package file: `UNKNOWN` (creator of the link: preset at installation or a person).
- Root's sudo right `(ALL : ALL) ALL`: the line `root ALL=(ALL:ALL) ALL` of `/usr/etc/sudoers`, a file of package
  sudo recorded unchanged; no `/etc/sudoers` among the recorded sudo sources: `INSTALLED-PACKAGE`.
- `/etc` (subvolume row): the directory `/etc` is listed in package filesystem with mode 040755, found mode 0755;
  `INSTALLED-PACKAGE`. Its contents are separate rows; the mount exists only while running (S8.2-5).
- Snapshot-1 groups with members of different kinds: `/etc/audit`, `/etc/crypto-policies`, `/etc/selinux`,
  `/etc/ssl` → `MIXED`; `/etc/audit/rules.d` (one member) and `/etc/selinux/targeted/policy` (`policy.35`, differs
  from the packaged copy) → `UNKNOWN`. RPM records no digest for `audit.rules`, `rules.d/audit.rules`,
  `crypto-policies/config`, `selinux/config` (ghost entries), so they are not “as received”; their creator is not recorded.
  `rules.d/audit.rules` equals the packaged `/usr/share/audit-rules/10-no-audit.rules` with mode 0600, and
  `crypto-policies/config` holds `DEFAULT\n` (SHA-256 ecae097f…), matching the package scripts' text
  (`raw/0154-s4-microos-scriptlet-sources.out`), but script text is not an execution record.
- `/boot/grub2` → `MIXED`: `grubenv` is an environment block in the format written by grub2-editenv with no variables
  (`s4-microos-sources.tsv`): `RECORD`; the four directories belong to no package and their creator is not recorded:
  `UNKNOWN`.

## Documentation consulted

- https://en.opensuse.org/Portal:MicroOS/SELinux — a relabel is triggered by creating `/etc/selinux/.autorelabel`
  and rebooting (used only to describe `.autorelabel`; its creator stays unknown).

## Gaps

None found in this part; `meaning-microos.tsv` holds only its header.

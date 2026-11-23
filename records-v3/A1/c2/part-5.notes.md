# Classification c2, part 5 of A1 — notes

Input: `../in/part-5.tsv` (479 rows; machines alpine, arch, silverblue, ubuntu). Output: `part-5.tsv`.
Script: `scripts/part5_decide.py` (rules below, then a row-by-row table keyed by machine and name).

The inventory files named in `evidence` (`raw-E6/…`, `raw-X1/…`) are not present under `A1/in/raw/` for these four
machines, so every decision rests on the evidence text and on public documentation. No probe was run.

## General reading applied to every row

- A row is one object (the `members` column is 1 everywhere). For a directory group, the removal test of S2.2-2 is
  applied to the whole group as it stands: if removing the group makes the computer stop doing something or makes
  something impossible, the group must be recorded, even when some members alone would not be. So MIXED is not used.
- Where only the first samples of a group are visible and they already decide MUST, the unseen members cannot change
  the decision. Where the visible samples do not decide and the unseen members could, the decision is UNKNOWN (S3-2).
- When removal changes nothing and no sentence of 2.2 points to dependence (S2.2-1), the decision is NOT with
  S2.2-1, S2.2-2.
- A setting whose current value is not visible is decided by what the setting does (its kind), not by a guess at
  its value.

## Rules applied by script (each follows from the cited sentences)

| Rule | Applies to | Decision | Sentences | Rows | Hand-checked ids |
|---|---|---|---|---|---|
| A | kind `account` | MUST | S2.2-15 (“accounts … must be recorded”) | 129 | alpine-c6df412fe9, alpine-ecfab3dd45, arch-4900fca16b, arch-1525133242, silverblue-4c29fefef0, silverblue-ecfab3dd45, silverblue-4e223d43b0, silverblue-cff9eec648, ubuntu-707e10c2e4, ubuntu-dbea3590f8 |
| L | stored object under `/var/log/` (except the `README` link) | NOT | S2.2-6 (records of the past: logs, history) | 36 | alpine-4156dc1632, alpine-293699acd1, arch-e6b33c3854, silverblue-4ee9ecb0b7, silverblue-e6b33c3854, ubuntu-83df02e6eb, ubuntu-2954505d9d, ubuntu-e6b33c3854, ubuntu-b47fdf8545, alpine-d6ce9987c3 |
| B | `/etc/{group,passwd,shadow,gshadow,subuid,subgid}-` backup copies | NOT | S2.2-2, S2.2-6 | 21 | alpine-d3bb1c2fce, alpine-9ed4eb3a99, arch-42b0af3cd4, arch-9ed4eb3a99, arch-a2bc9043e2, silverblue-42b0af3cd4, silverblue-9ed4eb3a99, silverblue-a2bc9043e2, ubuntu-42b0af3cd4, ubuntu-9ed4eb3a99 |
| S | shell startup files (`.bashrc`, `.bash_profile`, `.bash_logout`, `.profile`, `/etc/profile`) | MUST | S2.2-10 (names shell startup files) | 15 | arch-30d35f7d67, arch-d74bcd1e9f, arch-194f69ba23, arch-3787beb4db, arch-7138629d33, arch-2d36998dd6, silverblue-0ef3eb01b3, silverblue-be57689b36, silverblue-661587021d, ubuntu-3543b3a205 |
| K | `.ssh` directory of an account whose evidence shows `authorized_keys` | MUST | S2.2-15 (keys used to log in) | 6 | all 6: alpine-c3a3dd6c9b, alpine-351644c1fd, arch-c3a3dd6c9b, silverblue-b2b64aaca8, ubuntu-c3a3dd6c9b, ubuntu-351644c1fd |
| U | `/etc/sudoers.d`, `/etc/doas.d` | MUST | S2.2-15 (right to become superuser) | 5 | all 5: alpine-8aab7ad250, alpine-09d09204d8, arch-09d09204d8, silverblue-09d09204d8, ubuntu-09d09204d8 |
| C | stored object under `/var/cache/` except `debconf` and `pollinate` (decided by row) | NOT | S2.2-5 (cache) | 11 | alpine-f2fcdd0583, arch-2b7dd179b7, arch-b618c77d89, silverblue-418d5e5b2b, ubuntu-f447463411, ubuntu-869a3e13d4, ubuntu-2b7dd179b7, ubuntu-54ff9bafac, ubuntu-382c94b98b, ubuntu-426fc3d9ff |

Results of the hand check: every checked row fits its rule. The accounts are entries of the account database. Every
`/var/log` member checked is a log, a boot-message dump, an installer log or a login record. The backups are copies
that shadow tools write before an edit. The startup files are the ones bash reads. Each `.ssh` group contains
`authorized_keys`. The sudo and doas files grant the right to become superuser. Each `/var/cache` group checked is
downloaded indexes, packages or compiled data (an AppArmor policy cache, man indexes) that its program rebuilds.
Two `/var/cache` objects are not plain caches (`debconf` holds configuration answers; `pollinate/seeded` is a
one-time marker), so they are kept out of the rule and decided by row.

## Recurring readings in the row-by-row part (where the text leaves two readings: HOLE)

1. **Databases whose removal disables a tool** (the pacman, dpkg and apt databases, the alternatives
   registry, pam-auth-update, update-shells, ucf, command-not-found, debconf): S2.2-4 names “the contents of
   databases” as content that need not be recorded. Its own justification (“the computer does and can do the same”)
   is false here, and S2.2-2 then gives must. Which one prevails is not stated. The apk database is MUST instead,
   because its `scripts.tar.gz` holds package scripts that apk runs as root (S2.2-10).
2. **Stamp and marker files** whose absence makes a program repeat a one-time action (`/etc/.updated`,
   `/var/.updated`, the shown-once markers, the pollinate seed marker, the rpm-ostree shadow-mode stamp,
   `/var/.ostree-selabeled`, the authselect checksum copy, the landscape account marker): S2.2-6 (records of the past, need not)
   against S2.2-1 (what the computer does depends on them, must).
3. **Appearance settings shared by several programs** (newt palette, console colour map): S2.2-7 exempts settings of
   *one* program only, and S2.2-1 requires what behaviour depends on. The text does not say whether appearance is
   behaviour. Settings shared by several programs that change what can be done (readline key bindings, locale,
   keymap, dconf defaults) are decided MUST, because S2.2-7 does not fit them and S2.2-1 does.

## Identity values

Host keys, the DHCP DUID and secret, the NVMe host NQN and the iSCSI initiator name are decided MUST by S2.2-1: the
identity the computer presents depends on them. No sentence exempts them; S2.2-14 and S2.2-15 exempt only the network
password and the account password.

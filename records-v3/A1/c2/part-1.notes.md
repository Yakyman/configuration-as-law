# c2, part 1 of A1: notes

Input: `../in/part-1.tsv`, 1222 rows, all from the `coreos` machine (Fedora CoreOS 44, a QEMU VM booted by BIOS).
Output: `part-1.tsv`. Decisions use only S2.2-* and S3-1/S3-2.

## Readings applied throughout

1. **Removal test in both directions.** S2.2-1 sets the scope of the obligation ("whatever the computer's behaviour
   depends on"), and S2.2-2 and S3-1 make removal the deciding test. So if removal changes nothing, the decision is
   NOT (cited as S2.2-1,S2.2-2). Examples: empty directories, files that hold only comments, files that no installed
   program reads, metapackages with no files.
2. **"Something becomes impossible"** (S2.2-2) counts even for a capability that is not used right now. Examples:
   unused keymaps, time zones, terminfo entries, and units that are installed but not started.
3. **Settings read by one program (HOLE pattern H7).** A file that a program only reads as values is a setting
   (S2.2-13). S2.2-7 exempts "settings that are in force only inside one program". When a single program reads the
   file, and the file's effect reaches beyond that program (network, time, logs, accounts created, boot), two readings
   exist:
   - (a) the setting is applied only inside that program, so it is exempt: NOT;
   - (b) its effect is not confined to the program, so the removal test applies: MUST (S2.2-2).

   No sentence says which reading prevails, so the decision is HOLE. Where an explicit consequence decides, it is
   applied instead:
   - S2.2-15 decides sshd ports and the password-login rule, sudoers, PAM, accounts, login keys and firewall rules;
   - S2.2-10 decides code.

   If several programs read the file, S2.2-7 does not apply and the removal test decides. If the effect stays inside
   the program's own interface (colours, editor settings, display lists), both readings give NOT.
4. **Items of the S2.2-3 list that have no criterion attached (HOLE).** S2.2-5 attaches the criterion "the computer
   does the same, only more slowly" to cache, and S2.2-6 names records of the past with no criterion. Two cases
   follow:
   - `/etc/ld.so.cache` is called a cache, yet without it programs fail (libraries under llvm18 are not found);
   - `/var/log/journal` and systemd timer stamp files are records, yet removing them changes behaviour (journald stops
     keeping logs across reboots; missed timer runs are no longer caught up).

   In both, S2.2-2 says MUST and the list item says NOT: HOLE.
5. **The removal test detects only less, not more (HOLE).** Some stamps make a unit run again when they are removed:
   ConditionNeedsUpdate stamps, the coreos-populate-lvmdevices stamp, and the ostree SELinux-label marker. S2.2-1 says
   behaviour depends on them. The S2.2-2 test counts only "stops doing" or "becomes impossible". The text does not say
   whether that test exhausts S2.2-1. Stamps checked only by disabled units are NOT.
6. **Objects generated from hardware or by the kernel (HOLE).** Device units and the rpc_pipefs entries exist exactly
   while the hardware or kernel interface exists. The removal test cannot be applied to them, and Section 2.2 does not
   say whether such objects must be recorded.
7. **Runtime groupings.** Scopes and implicit slices are MUST: stopping them stops their processes (S2.2-2), and no
   sentence exempts them. Mounts are MUST, because unmounting stops things.
8. **Directories.** A directory row is decided by removing the directory together with whatever it contains. Contents
   that sit in another row are still taken into account, because removing a directory removes them. The `members`
   column was ignored: groups were expanded from `files.tsv` intersected with `package-files.txt` (owned rows), or
   from `unowned-groups.json` and `directory-only-groups.json` (stored rows).
9. **Content claims.** A file was called "comments only" or "empty" only in one of two cases. Either its size in
   `files.tsv` is 0, or a public default file of the same byte size was fetched and saved under `c2/raw/dist/`. In
   every other case the file was decided by its documented role, without assuming anything about its content.
10. **Device firmware** (firmware packages, microcode) is MUST by S2.2-16 read literally. These are device firmware
    images that the system installs and updates. Whether the device is present on this VM was not used.
11. **Group rows** are MIXED when their members get different decisions. This includes groups where a README or an
    example file is NOT and the other members are not.

## Rules applied by script (`work/rules.py`)

- **R-ACC** (40 rows). `account` → MUST, S2.2-15 ("accounts … must be recorded"; system accounts are not exempt).
  Checked by hand: coreos-37c52140e1, coreos-cff9eec648, coreos-8d1e409524, coreos-3d437d2b28, coreos-64c4ab9fc8,
  coreos-4900fca16b, coreos-245a92fd3e, coreos-03b6505825, coreos-28c046fc91, coreos-0b2fc8af1f.
- **R-MOD** (59 rows). Loaded `kernel-module` → MUST, S2.2-10: code that the kernel runs with the kernel's own rights.
  Checked: coreos-fc0b6e9d58, coreos-8145bd0747, coreos-d2f8794f5b, coreos-be057bae4b, coreos-c34a0eb60b,
  coreos-9cde69ca11, coreos-427cf60e35, coreos-22f28dcc06, coreos-7952346e8b, coreos-c770486c38.
- **R-PROC** (27 rows). `process` → MUST, S2.2-9 (a program that runs). This includes the processes of the inventory
  session itself (bash, sudo, ps, sshd-session) and kernel threads.
  Checked: coreos-42c14762fe, coreos-e0e91241c3, coreos-d5aa6b47fd, coreos-89ce5c5668, coreos-b66da72753,
  coreos-d8ee8908a9, coreos-b012186e55, coreos-7b2f0c0e4f, coreos-ce95966cbb, coreos-f37ac4244d.
- **R-UNIT** (287 system and 20 user units, each with a unit file under /usr/lib/systemd). → MUST, S2.2-1,S2.2-2:
  removing the unit file makes starting the unit impossible and stops what it starts. The one masked unit,
  systemd-repart.service, is MUST because the mask decides that it never starts.
  - Checked, system units: coreos-b150ceaef3, coreos-f246d39885, coreos-956040fa23, coreos-0c2a19e310,
    coreos-67ef1dc40f, coreos-83ed8fc3be, coreos-5ee5076e2d, coreos-bcb29587e2, coreos-2de5cf9b82,
    coreos-272d6f3f09.
  - Checked, user units: coreos-d135e9ffa0, coreos-9acc52d8ae, coreos-f6c4311396, coreos-beed948983,
    coreos-9ffeccd130, coreos-7abafbc845, coreos-e98c397756, coreos-7901db011f, coreos-a3b8750b9f,
    coreos-47f8ab446b.
- **R-PKG** (421 of 483 packages). The package's public file list
  (`https://mdapi.fedoraproject.org/f44/files/<name>`, saved in `c2/raw/mdapi/`) contains at least one executable,
  shared library, kernel module or systemd unit. → MUST, S2.2-2 and S2.2-9: removal makes running these programs
  impossible.
  Checked: coreos-569595199e, coreos-dee40d049d, coreos-aef7954f0c, coreos-1bdc71dae5, coreos-3bce7fb26f,
  coreos-7909659263, coreos-794a26732a, coreos-8909dee021, coreos-2daeff0083, coreos-e2c6ab9a77.
  The other 62 packages were decided row by row in `work/pkgmanual.py`.

The f44 file lists are those of the current repository version, which can differ slightly from the installed build.
Only the presence of an executable or library was used from them.

Decided row by row:
- package-owned paths: `work/batch1.py` to `work/batch4.py`;
- stored paths and the directory remainder: `work/batch4.py`;
- unit groups: `work/unitgroups.py`.

`work/emit.py` checks every row's word limits and decision word as it appends. `work/verify.py` checks that the
output ids match the input ids.

## Sources fetched (saved under `c2/raw/`)

- Package file lists: mdapi f44 (`c2/raw/mdapi/`).
- Default files compared by size with the inventory (`c2/raw/dist/`):
  - from Fedora dist-git: NetworkManager.conf, rsyncd.conf, printcap, aliases, host.conf, inittab, sysctl.conf;
  - from upstream repositories: dracut.conf, idmapd.conf, nfsmount.conf, nfs.conf, toolbox.conf;
  - fuse.conf (cited by URL).

  nfs.conf differs in size from the upstream file, so it was decided by its role.
- The fedora-repos spec (`archive_enabled=1` on stable releases).
- bootupd `src/efi.rs`: the ESP is mounted on a temporary mount when none is mounted.

## Independence

At about 04:40 UTC on 22 November, a mistyped shell command ran `grep` over the wildcard `*` in `A1/` instead of in
this folder. It printed six lines from the beginning of `../c1/packages-fetch.py`: imports and the code that opens
the input file. It also printed a few lines from `part-2.tsv`, which is this classification's other part, and
from `A1/in/`. No decision of c1 was shown, and nothing of c1 was read afterwards.

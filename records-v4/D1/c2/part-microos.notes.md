# c2 — part microos: rules, facts used, hand checks

Classification c2 of `D1/in/part-microos.tsv` (6522 rows). Output: `D1/c2/part-microos.tsv`.
All rows were produced by the scripts in `D1/c2/tools/` (`facts.py`, `classify.py`, `main.py`); every rule below is
implemented there. Check of the output: `tools/verify.py` (ids equal, decisions valid, field limits, sentence IDs exist).
Paths below are relative to `D1/in/raw/microos/`.

## Facts established from the inventory (with evidence)

- F1. The running root `/` is snapshot 2: `/` and `/.snapshots/2/snapshot` have the same device (41) and inode (256)
  in `raw/0004-filesystem.out`. `/.snapshots/1/snapshot` is a different subvolume (device 76; its `/etc` device 77),
  created 2026-11-22 03:07 UTC (image build); snapshot 2 was created 2026-11-23 07:56 UTC. Snapshot 1 is therefore an
  inactive earlier root generation stored on a persistent filesystem. The inventory traversed snapshot 1 completely;
  the live root's `/etc` (device 42) was NOT expanded (row `/etc`, `expanded: false`).
- F2. For every snapshot-1 path whose relative path is in the rpm file list (`raw/0010-package-files-rpm.out`), the
  copy was compared with the rpm record:
  - file ≤ 4096 bytes: the inventory signature (`sha256-prefix4096`, `signature_bytes == size`) is the full SHA-256 and
    is compared with the rpm FILEDIGEST, plus the mode;
  - larger file: accepted as unchanged only if the snapshot-1 copy and the live file have the same inode and the same
    nanosecond ctime, and the live file is `unchanged` in `package-files.tsv`. ctime is changed by the kernel on every
    write or inode change (doc: https://man7.org/linux/man-pages/man7/inode.7.html, “Last status change timestamp
    (ctime) … changed by writing or by setting inode information”), so neither copy was written since they were one
    file, and the live one equals the rpm digest;
  - directory: mode equals the rpm FILEMODES; symlink: target equals FILELINKTOS.
  Anything else in the rpm list is “not as received” (ghost entries without digest, or a differing digest/mode), or
  “unverified” (larger file without the inode/ctime proof — mostly the snapshot-1 `/etc`, whose live counterpart was
  not traversed).
- F3. `/home/user/.bashrc` and `.profile` are byte-identical (full signature) to bash's `/usr/etc/skel/` files
  (rpm digest). The ESP files `bootx64.efi`, `MokManager.efi`, `grub.efi` have the same size and first-4096-byte
  signature as packaged `/usr/share/efi/x86_64/shim-opensuse.nx.efi`, `/usr/share/efi/x86_64/MokManager.efi`,
  `/usr/share/grub2/x86_64-efi/grub.efi`; 320 of 322 entries of `/boot/grub2/i386-pc` match `/usr/share/grub2/i386-pc`
  (the two others are the generated `core.img` and `load.cfg`).
- F4. Unit enablement: `raw/0022-unit-file.out` gives state and vendor preset; alias links in `/etc/systemd/system`
  point to their unit (targets visible in snapshot 1, `raw/0004-filesystem.out`).
- F5. MicroOS had no ordinary person actions (control records show only `new`, `collector`, `destroy`); person-chosen
  objects are those of provisioning: account/group `user`, its `authorized_keys`, a sudo rule.
- Not obtainable: the openSUSE package sources (src.opensuse.org and build.opensuse.org returned HTTP 403), so the
  content of `system-group-hardware.conf` and the default sudoers file could not be read. Groups/accounts not matched
  by a sysusers.d file named after them, and all sudo lines except the NOPASSWD rule for `user`, are UNKNOWN.

## Readings applied (sentence-based; see QUESTIONS.md for the questions only the author can decide)

- Q1 (S8.2-7) is read by provenance: an object “obtained as part of” an installed package is one written by the
  installer when installing that package. Snapshot-1 files were written by rpm when the packages were installed into
  that root (the image build installs into snapshot 1; snapshot 2 is a snapshot of it). With F2 they are INSTALLED-PACKAGE.
  Copies made later by other programs (ESP, `/boot/grub2`, home skeleton) are not obtained as part of the package.
- Generated lists (MIME database, depmod indexes, ld.so.cache, SELinux store, audit rules, CA bundles, journal
  catalog): GAP-TWO, RECORD (Q4, S8.2-15, “cache”; order S8.2-6) vs INSTALLED-DERIVED (S8.2-16 names “a generated list”
  among what is installed, covered by the line from which the system built it). No sentence says which prevails:
  S8.2-6 orders the questions; it does not rank S8.2-16.
- Person-chosen values and enablement links inside snapshot 1 (passwd, fstab, sysconfig, repos, pam, `*.wants` links…):
  GAP-TWO, setting (S8.2-12 “whatever file stores it”; SETTING-OWN, or SETTING-DEFAULT for preset links) vs RECORD
  (Q3 requires a value “that the computer as a whole obeys”; the running system does not read snapshot 1, it obeys it
  only after a rollback). Section 8.5 leaves “generations and rollback” as design questions, but it does not take
  objects stored in a generation out of S8.2-3; the classification question remains.
- Runtime (S8.2-5): files on runtime filesystems (`persistence: runtime`), loaded units, timers, ports, processes,
  `/sys/module` and driver entries, NetworkManager profiles kept only in `/run`, and `systemd-private-*` directories
  in `/var/tmp` (removed when the service stops: https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html,
  PrivateTmp=).
- Service enablement is a setting (S8.2-13, S8.1-11). State equal to the vendor preset → SETTING-DEFAULT (S8.2-17).
  Enabled while the preset is disabled → UNKNOWN (what created the link). Static/indirect units: the object is the
  packaged unit file → INSTALLED-PACKAGE. Values inside an unchanged packaged file (polkit actions, policy files) →
  INSTALLED-PACKAGE by Q1 (S8.2-8 “default setting values”).
- Packages: `reason` from the inventory: explicit → INSTALLED-OWN; dependency → INSTALLED-DERIVED (S8.2-16).

## Rules applied by script, with the 10 rows checked by hand for each

- R1 package reason → INSTALLED-OWN / INSTALLED-DERIVED. Checked: microos-fd6cfddfbd0cf9ba6c72a75b,
  microos-49d27858fb88274124143dff, microos-aed34f44820ee449c8d3503f, microos-bc07f4544f56a5a56d0d67e0,
  microos-c5ac902e30dd4f56b211317e, microos-ffdc2b6601230d35d4870569, microos-64d3bb84d8a39f4aef3f3e16,
  microos-b4a55b066a62a76363c6dcd1, microos-cda53232ab37f30105589505, microos-987b7f2ba81668278f9644cd.
- R2 snapshot-1 entries as received (F2) → INSTALLED-PACKAGE (groups: all members; code rows). Checked (member-level
  rpm record vs signature/inode/ctime printed by `tools/handcheck.py`): microos-6129b70660d0d93658d81de7,
  microos-7b6c690f4124770fe039d075, microos-6a11548a8d9ca15190d901c9, microos-5e864edb1880c7c2df70335b,
  microos-4e82e504c9327344877db3ac, microos-db97d66190ae82279b84643b, microos-a6c4c5dbfb98994bbba025d3,
  microos-62001c4dc396c61abaaed5e8, microos-ee37a29f605a2a5f35c6d5db, microos-b67d51dbb77e5761a77a2c23
  (also microos-64247d7edbec5053395327d1, microos-2c51c2d1d16dcd5852e79329, microos-4058544786e92eb50613d25d).
- R3 unverified copies → UNKNOWN (group UNKNOWN when all other members share one decision). Checked:
  microos-4206a11af0d4e570f9f89aa9, microos-eb734fd4265fc8a45305b36a, microos-b4fcf84dc2e42727d2e4341e,
  microos-fdd8ef53688161124ef86a82, microos-4bcbc87b23fe7584caa54abe, microos-7f7eb38717f4034f80c62b17,
  microos-f5ca77420f2d4a98f88f8272, microos-c474de188f2c35ce23030328, microos-fd55b1b6a71ab7869ccad6f8,
  microos-6f8e648be204e967da817cd9.
- R4 runtime groups → RUNTIME with creator by path prefix. Checked: microos-3ea32b01f37800e324f862a5,
  microos-0892f7bf4b9a6582a88fb9cd, microos-9c815c410ccc3c953dfcad89, microos-a73c2b28190fedd5647b7268,
  microos-06031e6b72fc9dd6f12dc740, microos-950bc53d1cfd1c601351948e, microos-69b766b9eca45f01a41d6503,
  microos-7ea3796712ff653f4dd19185, microos-4d8409855f3af909d235b7ae, microos-5b813b0150e9d2fd0379fe2b.
- R5 unit files by state. Checked: microos-a8e49be54b12c1732ccf50c2, microos-72d36a972be4a77fda2dfb08,
  microos-6724f9b1fffd474aa5147cc8, microos-d5bc7b0a0cf854ef311c64bb, microos-ecc23c7ef01f7afc746174fe,
  microos-a30856d5291b769875d0348a, microos-e09678a09e0afb731847b2b9, microos-767ebd392c9db00d82cd10bf,
  microos-a53e33b5f95e1daa36e92c36, microos-bba1c75b231781725aff5de2.
- R6 polkit action → its unchanged packaged policy file → INSTALLED-PACKAGE. Checked: microos-b851d63fa7eada38a718a1c6,
  microos-da6b6f0282afd4df50793b1d, microos-87f35ab0205084969dbb4870, microos-0ac3898fc36aeb9c2223f74d,
  microos-52976ba9ffa98f46d5ecc503, microos-a610bd16f8c5b5a83bd917e4, microos-ef79389980f989a302de6836,
  microos-6f756978323fcb9ffdaf2910, microos-1a2d5d656631cfa3ffe79253, microos-dc4ec100541c63ce8f9d29c8.
- R7 processes, modules, drivers, services, timers → RUNTIME. Checked: microos-e2359cdd958c0f5480742f59,
  microos-40a84871436063dd3dd232ad, microos-859878a9d2a68abc5907c1f2, microos-9bba4798e6837ba3371a4758,
  microos-80ee4cb14bb1ea7e2ed5292e, microos-2fa21364697eb6b79fb37c2e, microos-d634e17b6a524fa7fcd9c219,
  microos-d425dd4c8c043dbe23b415bd, microos-3fc0ac6023823173726c9895, microos-29600ef78d09babce827dd7e.
- R8 generated lists / settings copies in snapshot 1 → GAP-TWO. Checked: microos-694303c3e26c4258aea1d9c7,
  microos-cfb3363718fdffa8e2decf3b, microos-39fc4d3ee2703d92a368043c, microos-dff1c566adf705f3f3824455,
  microos-a192180c3d10540a68eae9cb, microos-94020c7897f882d477fd6049, microos-f3a472e18e86eaf9c836e215,
  microos-ecec91868cb25d97a677babb, microos-8368bc682b446128ce7776dc, microos-dcce813055fa256ed012c87a.
- R9 accounts and groups. Checked: microos-7a484066ae23f5c54fcffbbb, microos-720e0c9428d0bce6f46089d5,
  microos-753c3566866e942ffcdec2cb, microos-27d81f98abfda1e6ea4c29de, microos-b1ffef304d49aa9a0493a8f8,
  microos-5ef7f7db82f64f320f82cfb7, microos-9c29a818f6824f36fff0df44, microos-090dcd1f3058cb9b77deafaf,
  microos-de28890d79883dd590cf799e, microos-95924826484154a7cab19e72.

Decided row by row (no shared rule): the 2 opaque subvolume rows (`/etc`, `/.snapshots/2/snapshot`), the sudo lines,
saved networks, ports, the 36 MIXED groups (member classes listed in each reason; full member lists in
`members/<id>.tsv`), the live `/boot`, `/home`, `/root`, `/var`, `/usr` stored groups.

## Limits

- MIXED reasons with many classes give counts only; the class of every member follows from the rules above
  (`tools/classify.py: mdec`).
- `/etc` and `/.snapshots/2/snapshot` were not expanded by the inventory; their MIXED decision rests on members
  known from `package-files.tsv` (unchanged and changed `/etc` files) and on the other rows.

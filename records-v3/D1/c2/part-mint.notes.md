# D1 c2 — part mint: notes

Input: `../in/part-mint.tsv`, 2031 rows (48 accounts, 78 groups, 1905 dpkg packages, every package status `ii`,
every row one member). Output: `part-mint.tsv`. Decided only from Section 2.2 and indicator S3-1/S3-2.

## What the objects do: sources

- Accounts and groups: the inventory lines themselves (`../in/raw/mint/raw/001-accounts.out`, `002-groups.out` under `D1/in/`).
- Packages: the inventory gives name, version, status only; its file-ownership query failed (`104-ownership-dpkg-query.err`:
  serial login timeout). File lists were therefore taken from the public archive indexes of the release the machine runs
  (Linux Mint 22.3 "zena", based on Ubuntu 24.04 "noble"): `http://archive.ubuntu.com/ubuntu/dists/{noble,noble-updates,noble-security}/Contents-amd64.gz`,
  their `binary-amd64/Packages.xz`, and `http://packages.linuxmint.com/dists/zena/{main,upstream,import,backport}/` Contents and Packages.
  All 1905 packages were found. Derived tables: `raw/mint/pkgclass.tsv` (per package: file counts, first code path, archive,
  whether the archive version equals the installed one), `raw/mint/pkgfiles.tsv.gz` (package → path), checksums of the indexes
  in `raw/mint/index-sha256.txt`. Files are listed per package name across pockets, so a path list may include files of a
  neighbouring version. Scripts: `scripts/mint/` (`scripts/mint/pkgfiles.py` builds the tables, `scripts/mint/assemble.py` writes the output,
  `verify.py` checks it).
- Group meanings: Debian base-passwd `users-and-groups.sgml` (https://sources.debian.org/src/base-passwd/3.6.8/doc/users-and-groups.sgml/),
  CUPS build rules (system groups root lpadmin), Debian wiki SaneOverNetwork (saned in group scanner), nemo-share README.Debian (sambashare).
- GSettings: https://docs.gtk.org/gio/ctor.Settings.new.html — "It is an error for the schema to not exist: schemas are an essential part of a program".
- GObject introspection: https://gi.readthedocs.io/en/latest/ — typelib "stores the information on disk in a binary format", read by libgirepository.

## Rules applied by script (each checked by hand on 10 rows)

- **R1 account → MUST** (48 rows). S2.2-15: "accounts … must be recorded". Every row is an existing line of the account database.
- **R2 package shipping executable code → MUST** (1568 rows). A package with at least one file, outside documentation
  directories, that is a program (`bin`, `sbin`, `libexec`, `usr/games`), a shared object (`.so`), a kernel module, firmware,
  a script or interpreter module (`.py`, `.pl`, `.sh` …, `usr/lib/python3*`, `usr/share/perl*`), a systemd unit directory
  file, an init script, boot or GRUB files. S2.2-9 (a program that runs must be recorded regardless of how it was installed),
  S2.2-10 (code another program runs with its own rights), S2.2-2 (removal makes the function impossible).
- **R3 library typelib in the shared typelib directory → MUST** (65 rows). Read as values (setting, S2.2-13) by any
  GObject-introspection program, so not "in force only inside one program" (S2.2-7 does not apply); a program importing the
  namespace cannot start without it (S2.2-2). The first check found 2 misfits (private Muffin and Xviewer typelibs) and a second
  sample 2 more application typelibs (Rhythmbox, Nemo); these and Xreader's were taken out of the rule and decided by hand
  (one-program data, HOLE). The final sample fits 10/10.
- **R4 group with no listed members → UNKNOWN** (69 rows; group `users` with a member is decided by hand, also UNKNOWN).
  Removing a group line removes only the name→gid mapping and the listed members; numeric ownership stays. What stops then depends on
  which udev rules, tmpfiles lines, unit files or PAM rules on this machine resolve the name; the inventory's filesystem query
  failed, so this is not established (S3-2).

Hand-checked ids per rule (seeded sample, `raw/mint/handcheck-samples.txt`):
`{"R1-account": ["mint-c9f690bf9826de648b8baf01","mint-3e6ff6afc6238d7f8abecc07","mint-fb4db94e9917016c40645a0f","mint-098c1b13c73785adbd792921","mint-811bb0167d5526ddfc928ec0","mint-11dbd70973c9f5b21ea7580a","mint-f9dd740c06843ced4c93e8b7","mint-3aae329f99ecb850d1bbf6c1","mint-e7ca7271a4ae59d0f37673c2","mint-20f5b68601112a9237416757"],"R4-group-no-members": ["mint-42152dfde33260586ffb999f","mint-b966d498b90e318e0e6977bb","mint-d06b02b4460fd7dbcc735106","mint-f44f658acc0af5772b584cbc","mint-64463c67fca26847c353780a","mint-fe618e3d57a5eb7fc041b503","mint-fed793d380c59af7dbc9cfc8","mint-531494b94b66c14f935ffa8e","mint-2a697ae47f7d42128a6612ce","mint-adbd53098b0f8d759d2d6631"],"R2-code": ["mint-b33b146b526f68f0a1a33f54","mint-20c3a6dd2ca94224d2828338","mint-a823e8cb31c60e632e06d5db","mint-790c3516e883cd0981ea48d9","mint-dd3affb0527b721839bcbda3","mint-dbfa434f23ea19b6241686ef","mint-a45246537561af70202f912f","mint-d1f9d5892ba4b38c12596f2a","mint-2ba6a194b244a3386c326c52","mint-424a3e2205a2664bdf1e0ba0"],"R3-typelib": ["mint-12f4b10e579860c608a27e59","mint-3b60abb072e8489221d50f7e","mint-038b4193155dc3c5ea298c71","mint-82cf7afa6839da2780d967e6","mint-3b1bdbfc5e75ed274fc0af28","mint-9667bb0c93739b60ba28765d","mint-16829ea269a2c04e57fee085","mint-b92c7475329fa4a19130e933","mint-4e5b7714216ce80aca95d489","mint-a2add8db0e28a2d396cd9fda"]}`

## Decided row by row (`work/mint/hand-packages.tsv`, `work/mint/hand-groups.tsv`)

272 packages without executable code in the archive file list, plus 9 groups with members. Each got one of these readings
(the reason column states it per row):

- MUST, data read as values by several programs or the system whose removal makes a stated function impossible
  (S2.2-1, S2.2-2, S2.2-13): e.g. xkb-data, libasound2-data, fontconfig-config,
  media-types, netbase, container policy files, dictionaries, ICC and Ghostscript resources, schemas of shared libraries.
- MUST, files executed as code (S2.2-10, S2.2-13): Xsession.d fragment, system crontab, Samba helper scripts; polkit rules.
- MUST, apt keyrings (removal makes installing from the signed repository impossible).
- MUST groups with members: adm, cdrom, dip, plugdev, lpadmin, scanner, sambashare (documented rights, S2.2-2); sudo (S2.2-15).
- NOT: documentation (S2.2-4 "documents"), wallpapers (S2.2-4 "photographs"), empty packages with no dependency
  (S2.2-1/S2.2-2: after removal the computer does and can do the same), language-pack extensions of Firefox/Thunderbird
  and other values in force inside one program that change only its look (S2.2-7), JavaScript run inside web pages (S2.2-11).
- UNKNOWN: configuration or data files whose effect after removal is not established from documentation (e.g. whether the
  file only repeats defaults, or whether any installed program reads it), and yelp-xsl (whether yelp confines the stylesheets).

## Holes found (the text, not the machine)

1. **Appearance shared by many programs** (50 rows: icon, cursor and GTK themes, fonts, sound theme, system-wide translations;
   S2.2-1, S2.2-7, S2.2-13). S2.2-7 exempts theme-like settings only inside one program. Whether a change only in look, sound or
   message language is a change of "what the computer does" is not said; reading 1 gives MUST, reading 2 gives NOT.
2. **Metapackages and transitional packages** (31 rows; S2.2-1, S2.2-2). Removal stops nothing at once; only later package-manager
   runs autoremove or stop upgrading the dependencies (e.g. kernel metapackages pull new kernels). The text gives no time frame for
   the removal test.
3. **Data a single program needs to work** (21 rows: one program's UI files, schemas, private typelibs; S2.2-2, S2.2-7, S2.2-13).
   S2.2-7 exempts settings in force only inside one program; S2.2-2 requires them because the program fails without them. No
   sentence says which prevails.
4. **Detached debug symbols** (13 rows; S2.2-2, S2.2-4). Removal makes symbolic debugging impossible, yet only the data itself
   becomes unavailable, which is how S2.2-4 justifies "content"; content is defined only by examples.
5. **Reference databases read by programs** (12 rows: tzdata, PCI/USB ID databases, terminfo, magic database, GeoIP, provider
   database, netconfig; S2.2-2, S2.2-4, S2.2-13). S2.2-4 exempts "the contents of databases", S2.2-13 makes files read as values
   settings, and removal stops a function. No precedence.

## Counts

MUST 1783, HOLE 127, UNKNOWN 86, NOT 35, MIXED 0 (2031 rows).

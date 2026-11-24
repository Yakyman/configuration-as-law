# S2-a2 — do the agreed decisions follow from the text? Notes (party 2)

Inputs: `S2/sample/sample-D1.tsv`, `S2/sample/sample-A3.tsv` (600 rows). Facts: `D1/in/`, `A3/in/` inventories.
Result: `S2/a2/sample.tsv`. Counts: (not published: orchestration or scratch).

## Method

1. (not published: orchestration or scratch) joins every sampled row to its collector row (`objects.tsv`), its member list (`members/<id>.tsv`),
   the persistence record (`raw/0004-filesystem.out`) and `package-files.tsv`. Output: `raw/facts.jsonl` (all 600 rows
   found).
2. (not published: orchestration or scratch), (not published: orchestration or scratch), (not published: orchestration or scratch) look up the package and integrity facts (owner lookup also tries
   `/lib`, `/lib64`, `/bin`, `/sbin` because the inventories show these as symlinks to `usr/...`:
   `raw/evidence.txt`). Outputs: `raw/integrity-l1.txt`, `raw/polkit-files.txt`, `raw/stored-ownership.txt`.
   (not published: orchestration or scratch) prints every stored row with its members: `raw/stored-members.txt`.
3. (not published: orchestration or scratch) applies the rules below and writes `sample.tsv`. Every stored-object row (about 150) was read by
   hand in `raw/stored-members.txt` before the rules were written. A rule that met an unexpected row stopped with
   `CHECK`; none remained.

Each row was decided in the order of the four questions. S8.2-5 decides first for objects that exist only while
the computer runs. The agreed decision counts as following only if each of its parts follows from a sentence read
literally: what the object is, and which line covers it. The facts come from the inventory. That two classifications
agreed was not used.

## Rules (each applied only where its facts hold)

| Agreed decision / kind | Finding | Facts required | Sentences |
|---|---|---|---|
| RUNTIME: process, port, socket, mount, mount-resource, network-state, module-name (`/sys/module`), driver (`/sys/bus/*/drivers`), firewall-* (`nft -j list ruleset`, `iptables-save`), service (`list-units`), timer (`list-timers`) | FOLLOWS | query scripts `raw/NNNN-*.sh` show kernel or manager runtime state | S8.2-5 |
| RUNTIME, unit-file `NetworkManager-wait-online-initrd.service` | FOLLOWS | only a generator symlink in `/run` (runtime, target `/dev/null`) | S8.2-5 |
| RUNTIME, stored groups | FOLLOWS | directory and all members persistence `runtime` (tmpfs). Two exceptions where the collector says `persistent`: rpc_pipefs (magic 0x67596969) and nsfs (0x6e736673), both in-memory kernel pseudo filesystems (sources below) | S8.2-5 |
| INSTALLED-OWN, package | FOLLOWS | reason `explicit` (all 54 rows) | S8.2-7, S8.2-8, S8.2-16 |
| INSTALLED-DERIVED, package | FOLLOWS | reason `dependency` (all 69 rows) | S8.2-7, S8.2-8, S8.2-16 |
| INSTALLED-PACKAGE, python/npm metadata | FOLLOWS | `native_package_ids` lists the RPM, and every file under the location is `unchanged` | S8.2-7, S8.2-8, S8.2-16 |
| INSTALLED-PACKAGE, polkit-action, unit-file, user-unit-file, access-rule, image | FOLLOWS | the file (for an action, the `.policy` file defining it) is in a package manifest and `unchanged` | S8.2-7, S8.2-8, S8.2-16 |
| INSTALLED-PACKAGE, kernel module directories | FOLLOWS | every `.ko.xz` member is listed as `/lib/modules/...` in a kernel-modules RPM and `unchanged` | S8.2-7, S8.2-8, S8.2-16 |
| PROGRAM-DERIVED, `__pycache__` | FOLLOWS | no `.pyc` is in any manifest; every source `.py` is packaged and `unchanged` | S8.2-7, S8.2-9, S8.2-10, S8.2-16 |
| RECORD | FOLLOWS | members are directory entries only (subdirectories are separate rows: checked with (not published: orchestration or scratch)), or value files written by a program as it ran: npm index buckets, Go `-a` entries (175 bytes = one entry line), man-db cache, logs, bun manifest cache, git reflogs, kubectl cache, CNI IPAM, timesyncd clock, kubelet pull record. None is in a manifest | S8.2-15 (S8.2-23) |

The rows checked by hand included all stored rows, all 10 python/npm rows, all 17 polkit rows, all 9 unit-file rows,
all 6 access-rule rows and the image row. For the L1 runtime kinds, at least 10 rows per kind were checked where the
sample has that many (fewer kinds have fewer rows), and the query script of each kind was read.

## Rows that do not follow (17)

- **FACT-UNKNOWN, pip `http-v2` entries with a `.body` file (6 rows).** pip stores each response as a header file
  plus `<key>.body` (pip `src/pip/_internal/network/cache.py`: `body_path = metadata_path + ".body"`; caching docs
  https://pip.pypa.io/en/stable/topics/caching/). The inventory keeps only a hash of the first 4096 bytes, so it does
  not show whether a body is an index or metadata page or a downloaded wheel or sdist. If it is an index or metadata
  page, the file holds values only and the row is RECORD. If it is a downloaded package, Q1 (a retained package
  archive) and Q2 (a zip that the interpreter can import) have readings that decide differently.
- **FACT-UNKNOWN, npm `_cacache/content-v2` blobs (3 rows).** The inventory does not show whether a blob is registry
  metadata or the tarball of an installed package.
- **DOES-NOT-FOLLOW, GAP-TWO, `/usr/lib/cups/backend` and `/usr/lib/cups/backend/snmp` (2 rows).** These paths are in
  no manifest, but each is a hard link: it has the same inode as the packaged, unchanged
  `/usr/lib/cups/backend-available/*` (`raw/evidence.txt`). The text does not say whether such a link is "obtained as
  part of" the package (INSTALLED-PACKAGE) or a program the system created from the package (PROGRAM-DERIVED).
- **DOES-NOT-FOLLOW, GAP-TWO, k3s data binaries (3 rows).** The k3s binary is outside any package
  (`/usr/local/bin/k3s`, kind `executable-code-outside-packages`) and extracts its embedded binaries itself
  (k3s `cmd/k3s/main.go`: `stageAndRun` calls `extract(dataDir)`, which untars the embedded asset into
  `data/<name>/`). PROGRAM-DERIVED needs "a line from which the system itself built or obtained it". Whether an
  extraction by a non-system program counts as the system obtaining it has two readings: PROGRAM-DERIVED or
  PROGRAM-OWN.
- **DOES-NOT-FOLLOW, GAP-TWO, Steam `package/*.zip.vz.*` archives (3 rows).** These are package archives that the
  Steam client's built-in installer (S8.1-5) keeps after installing them. Q1 may read the retained archive as
  "a package installed on the computer", which gives an installed object. If it does not, Q2 is no for a compressed
  archive and Q4 gives RECORD. The text has no word for retained package archives.

## Documentation used

- rpc_pipefs magic: https://raw.githubusercontent.com/torvalds/linux/master/net/sunrpc/rpc_pipe.c —
  `#define RPCAUTH_GSSMAGIC 0x67596969`, `sb->s_magic = RPCAUTH_GSSMAGIC;`, `.name = "rpc_pipefs"`.
- nsfs magic: the host's `/usr/include/linux/magic.h` line 96, `#define NSFS_MAGIC 0x6e736673`.
- Bun manifest cache: https://raw.githubusercontent.com/oven-sh/bun/main/src/install/npm.rs —
  `package_manifest::Serializer::manifest_file_name`: `name.extend_from_slice(b".npm");`, with the header
  `bun-npm-manifest-cache-v0.0.8`. The file is loaded by `load_by_file_id`, so it is read as values.
- k3s extraction: https://raw.githubusercontent.com/k3s-io/k3s/master/cmd/k3s/main.go — `getAssetAndDir`, `extract`.
- pip HTTP cache: see above.

## Limits stated, not decided

- INSTALLED-DERIVED rows rely on the inventory reason `dependency`, which means the package was installed as a
  dependency. The inventory has no reverse-dependency fact, so it does not show that the package that required it is
  still installed. This is recorded in `QUESTIONS.md` and was not used against any row.

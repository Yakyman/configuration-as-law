# Formats shared by `inventory`, `derive`, `compare` and `run`

All files are UTF-8 JSON Lines: one JSON object per line, sorted by (`kind`, `id`). Paths are absolute paths inside
the guest. Times are UTC. A program that cannot read something writes an object of kind `error` instead of skipping
it; an error is never silent.

## Inventory (`inventory` output, one directory per inventory)

`inventory --disk DISK.qcow2 [--ssh-port PORT --ssh-key KEY --user USER --root-cmd 'sudo -n'] --out DIR`

- `DIR/stored.jsonl` — every stored object of every filesystem of the disk, read from outside with libguestfs
  (`virt-ls --csv --checksum=sha256 --uids --time-t -lR` or `guestfish`), the disk opened read-only (`--ro`). Taken
  while the machine runs, after `sync` in the guest, so that the inventory does not restart the machine (CASES.md,
  `INV`); libguestfs documents `--ro` on a live disk as safe but possibly inconsistent, and the inventory records
  that in `meta`.
  `{"kind":"file"|"dir"|"symlink"|"other", "id":PATH, "mode":"0755", "uid":0, "gid":0, "size":N,
    "sha256":HEX|null, "target":LINK_TARGET|null, "exec":true|false, "exec_reason":"elf"|"shebang"|"mode"|"suffix"|null}`
- `DIR/executables.jsonl` — the subset of `stored.jsonl` with `"exec": true` (ELF magic, `#!` first line, any
  execute bit, or a suffix of a file that an interpreter executes: `.sh .bash .py .pl .rb .js .lua .desktop .service
  .timer .socket .path` and the startup files `.bashrc .profile .bash_profile .bash_login .bash_logout`).
- `DIR/force.jsonl` — what is in force, asked over SSH with the standard tools of the system (nothing of ConfOS):
  - `package` (`dpkg-query -W -f '${Package}\t${Architecture}\t${Version}\t${db:Status-Abbrev}\n'`), id `NAME:ARCH`,
    `value: {"version":…, "status":…}`;
  - `unit` (`systemctl list-unit-files --no-legend --full`, `systemctl list-units --all --no-legend --full`), id
    `system/NAME` or `user/ACCOUNT/NAME`, `value: {"enabled":…, "active":…, "sub":…, "fragment":PATH}`; timers are
    units; user units are asked for every account with a running user manager and for every account with lingering;
  - `process` (`ps -eo user=,pid=,args=` and `readlink /proc/PID/exe`), id `EXE_PATH` (kernel threads: `[kthread]`),
    `value: {"users":[…], "count":N, "args":[…]}` — PIDs are not part of the id;
  - `account` (`getent passwd`), `group` (`getent group`), id = name, value = all fields; `shadow` (`getent shadow`)
    value = sha256 of the hash field only;
  - `access` — effective sudo rules (`sudo -l -U ACCOUNT` for every account), and the files of `/etc/sudoers`,
    `/etc/sudoers.d/`, `/etc/security/`, `/etc/pam.d/`, polkit rules, `~/.ssh/authorized_keys` of every account
    (sha256 of content);
  - `module` (`/proc/modules`), id = module name;
  - `port` (`ss -H -tulpn`), id `PROTO/ADDR:PORT`, value = owning executable;
  - `firewall` (`nft -j list ruleset`, and `iptables-save`/`ip6tables-save` if present), id = table/chain/handle-free
    rule text;
  - `network` — saved networks (`nmcli -t -f NAME,UUID,TYPE,FILENAME connection show` if NetworkManager is present,
    `networkctl list` and the files under `/etc/systemd/network`, `/run/systemd/network`, `/etc/network/`), addresses
    (`ip -j addr`), routes (`ip -j route`);
  - `mount` (`findmnt -J -o TARGET,SOURCE,FSTYPE,OPTIONS`);
  - `crontab` (`crontab -l -u ACCOUNT` for every account, the files of `/etc/cron*`), `flatpak`
    (`flatpak list --all --columns=application,version,origin,installation` for root and every account),
    `container` (`podman ps -a --format json`, `podman images --format json`, for root and every account),
    `language-package` (`pip list --format json` of every Python found under `/usr` and the home directories;
    `npm ls -g --json` of every prefix found).
  - `meta` — boot id, kernel release, time of the inventory.

## Derivation (`derive` output)

`derive --declaration DIR_OR_FILE --cache CACHE_DIR --out derived.jsonl`

Each object the declaration requires, with the line that records it:
`{"kind":…, "id":…, "line":LINE_ID, "value":{…}}` — same kinds and ids as the inventory. For a package line: the
package (`package`, version) and every file of its `data.tar` with sha256, mode, uid, gid (`file`/`dir`/`symlink`),
its maintainer scripts and conffiles as given by the package; default setting values come with the package
(S8.2-17). For a setting line: the object and value the line states. A value that the derivation cannot determine
from the declaration and the packages its lines name is written as `{"kind":…, "id":…, "line":…, "value":null,
"underived":REASON}`. A line that takes a list from outside the declaration: `{"kind":"external-list", "id":LINE_ID,
"source":SOURCE}` (S8.2-18).

## Comparison (`compare` output)

`compare --inventory DIR --derived derived.jsonl --declaration DIR_OR_FILE --decide decide.tsv --out compare.tsv`
`compare --inventory DIR --baseline OTHER_INVENTORY_DIR …` (the self-test, and Reproducibility between two machines)

One line per object, tab-separated: `VERDICT  KIND  ID  DETAIL`, where VERDICT is

- `UNRECORDED` — on the machine and follows from no line (and `decide.tsv` does not classify it as not needing a
  line, see below);
- `DIFFERS` — follows from a line and differs (DETAIL: `field machine=… derived=…`, and the line ID);
- `MISSING` — follows from a line and is not on the machine (P2);
- `UNDERIVED` — the derivation could not determine the value (counts as a difference for Understanding);
- `BOTHWAYS` — unrecorded, and `decide.tsv` classifies it as one that the text decides both ways.

Objects that `decide.tsv` classifies as not needing a line are written to `compare-excluded.tsv` with the rule and
the sentence ID, never dropped silently. Exit status: 0 if `compare.tsv` is empty, 1 otherwise, 2 on error.

## Decisions (`decide.tsv`)

The case party decides objects under Paper 4, Section 8.2, and quotes the sentence (plan, Section 9.3, “How objects
are decided”). `decide.tsv` lines: `PATTERN  CLASS  SENTENCE_ID  REASON`, where PATTERN is a kind and a glob
(`file:/var/log/**`), CLASS is `program-record`, `material`, `runtime` (S8.2-5: belongs to the program or setting that
creates it, decided with it), or `bothways`. An executable object (`exec: true`) is never excluded by a rule
(S8.2-9/10: “a program, whoever wrote it and wherever it came from”). Every exclusion is listed for the review.

## Results (`run` output)

`runs/<name>/results.tsv`: `CASE_ID  PART  OUTCOME  EVIDENCE_FILE` with OUTCOME one of `pass`, `fail`,
`unobserved`, `undecided`. PART is one of `P1 P2 P4 REM REPRO UND OW`.

## Derivation: additions of `derive` (appended by the derivation; binding for `compare`)

Command: `derive --declaration DIR_OR_FILE --cache CACHE_DIR --out derived.jsonl [--components components.txt]`.
`--components` is the published component list of the base (`build/components.txt`); a `VERSION` file beside it,
if present, is the published base version. Exit status 0 when no `error` object was written, 2 otherwise (an unknown
kind, a wrong field count, a duplicate identity, a source whose sha256 differs from its line, a disk image given as
input). A directory as declaration means every `*.conf` file in it, in name order.

- `line` is `FILE:LINENO KIND NAME`, FILE relative to the declaration directory. A component of the base has the
  `line` of the `base` line and `"via": "components.txt:N"`.
- One object per (`kind`, `id`). When several lines give the same object with the same value, the first line is
  `line` and the others are in `also_lines` (`"LINE (NAME:ARCH)"` for package data). When they give different
  values, the object is underived with reason `lines give different values for this object` and the candidates in
  `conflicting`.
- Objects of package data carry `"package": "NAME:ARCH"`. Their `value`: `mode` (4-digit octal), `uid`, `gid`,
  `owner`, `group`, `size`, `sha256` (files; for a hard link the sha256 of its target, and `hardlink`), `target`
  (symlinks).
- `package` objects: id `NAME:ARCH`, value `version`, `architecture`, `status` (`ii`: the line requires it
  installed), `url` and `index` (where it was read), `deb_sha256`, `depends`, `pre_depends`, `provides`,
  `maintainer_scripts` (`{NAME: {sha256, mode, size}}`, as data; `maintainer_scripts_run: false`), `conffiles`,
  `md5sums_sha256`. A dependency that no line names and that is not a component: id = the package name(s) of the
  relation without version (`libc6`, `debconf | debconf-2.0`), `value: null`,
  `underived: "dependency not named by a line"`, `relation` (`PKG Depends: TEXT`), `also_relations`.
- `underived_fields`: an object whose line states some fields and not others carries the stated fields in `value`
  and `{FIELD: REASON}` for the others. `compare` treats each listed field as `UNDERIVED`. Used by: `account`
  (`gecos`, `password`), `group` named by an account line (`gid`, `members`; value `members_include`), `file`
  (`uid`, `gid`), `setting` (`form`), `unit` (`unit_id`, `fragment`, `account`, `active`), `firewall` (`tables`,
  `handle_free_text`), `network` (`path`), `authorized-key` (`file`).
- Kinds and ids per line: `snapshot` → `release`/`snapshot`; `base` → `release`/`base` (version, components) and the
  objects the base recipe generates as underived (QUESTIONS-derive.md, D3); `account NAME …` → `account`/NAME,
  `group`/`gid:GID` (underived), `group`/G for each supplementary group, `dir`/HOME (underived);
  `authorized-key NAME TYPE KEY` → `authorized-key`/`NAME/TYPE`; `file PATH …` → `file`/PATH (value `mode`,
  `sha256`, `size`, `source`); `setting NAME VALUE` → `setting`/NAME; `service NAME STATE EXE ARG…` →
  `unit`/`service:NAME` (value `enabled`, `argv`) and, if enabled, `process`/EXE (underived); `rule NAME TEXT` →
  `firewall`/TEXT (value `name`, `text`); `network NAME SHA256 SOURCE` → `network`/NAME.
- `error` objects: id and `line` = the line ID (or `-`), `error` = the message.
- `CACHE_DIR/derive-reads.log`: JSON Lines written by an audit hook of the interpreter: `open`, `write`
  (path), `listdir` (path), `exec` (argv), `request` (url), `connect` (address), `fetch` (url, final_url, status,
  bytes, sha256), `start`, `end`. A file of a disk image or a device is refused before anything is read.

## Inventory, comparison and decisions: additions of `inventory` and `compare` (appended; binding)

**When the stored level is read.** As `CASES.md` (`INV`) says, the stored level is read while the machine runs:
the force level first, then `sync` in the guest, then the live disk opened read-only with libguestfs (`--ro`,
which works on a temporary overlay). libguestfs documents this as safe but possibly inconsistent when the guest
writes during the read; `meta.stored_level_note` records it. Without `--ssh-port` only the stored level is taken
(a stopped machine). Further options: `--ssh-host` (default `127.0.0.1`), `--format` (default `qcow2`),
`--timeout`. Exit 0, or 2 if the inventory could not be completed (an `error` object `inventory/fatal` is written).

**Ids of stored objects.** Each filesystem of each partition is named `@partN`. If the guest has it mounted with
`FSROOT` `/` (matched by filesystem UUID from `findmnt`), ids are the runtime paths (`/etc/passwd`,
`/boot/efi/EFI/...`); otherwise `@partN/PATH`. Every stored object carries `fs` (`@partN` or the image id) and
`fs_path` (the path inside that filesystem); `runtime` (a list) gives further runtime paths of the object (bind
mounts with another `FSROOT`, and the mount point of an image). Directory and symlink `size` is 0 (the target is the
content of a symlink). `kind: other` carries `type` (`char`, `block`, `fifo`, `socket`, `partition-table`,
`boot-code`, `raw-partition:FSTYPE`) and `rdev` for devices. A hard link carries `hardlink_to`.

**Disk objects.** `@disk/partition-table` (`value`: the partition list with GPT types, GUIDs and names; `sha256`
of that text), `@disk/boot-code` (first 440 bytes of the disk; `exec: true`, `exec_reason: boot-code` when not all
zero), and for a partition without a mountable filesystem `@partN` with the sha256 of its whole content
(`exec: true`, `exec_reason: raw`: it may hold boot code, so no rule excludes it).

**Filesystem images.** A regular file whose content starts like a filesystem (squashfs magic `hsqs`, ext2/3/4
magic at byte 1080, ISO 9660 `CD001` at 32769, FAT boot sector) is opened with guestfish `mount-loop` inside the
appliance (full ownership, modes and device nodes; `unsquashfs` on the host is the fallback for squashfs when the
appliance cannot mount it, because an extraction by an ordinary account loses ownership and device nodes). Objects
inside have id `IMAGE_ID!INNER_PATH` and `runtime: [MOUNT_POINT/INNER_PATH]` when the guest has the image mounted:
matched by the sha256 of the loop device's content (read in the guest), else by the loop back-file path. Images
inside images are opened to depth 2. `meta.images` lists each image, its sha256 and how its runtime mount was found.

**Volatile objects** (force level, read over SSH): every object of every mounted `tmpfs`, `ramfs` and `devtmpfs`
(device nodes of `devtmpfs` are not listed), kinds `vfile`, `vdir`, `vsymlink`, `vother`, with the fields of stored
objects and `fs` = the filesystem type. Executable ones are also in `executables.jsonl` (which therefore holds
every object of `stored.jsonl` and `force.jsonl` with `exec: true`). `meta.volatile_mounts` lists the mounts read.

**Force-level values beyond the list above.** `unit`: `enabled`, `active`, `sub`, `load`, `fragment`, `source`,
`dropins`, `transient`, and for a transient unit `members` (executables of the processes in its control group);
user units are asked with `runuser -u ACCOUNT -- systemctl --user` (the `-M ACCOUNT@` form failed on Debian 13).
`process`: id `[kthread]` for kernel threads, `[exe-unreadable]` when `/proc/PID/exe` cannot be read; an executable
that was deleted keeps the ` (deleted)` suffix. `port`: `value.exe` is the list of executables holding it.
`account`: `fields` and `name`, `password`, `uid`, `gid`, `gecos`, `home`, `shell`, `groups` (supplementary groups
from the group database); `group`: `fields`, `name`, `password`, `gid`, `members`. `authorized-key`: id
`ACCOUNT/TYPE` (`#N` for a second key of the same type), value `account`, `type`, `key`, `key_sha256`, `file`,
`options`. `setting`: `hostname` (`/proc/sys/kernel/hostname`) and `timezone` (the zone `/etc/localtime` points to,
else `/etc/timezone`, else `UTC`), value `name`, `value`. `module`: `size`, `file` (`modinfo -n`). `mount`: `source`,
`fstype`, `options`, `fsroot`, `uuid`, `label`, `creator` (the `SourcePath` or `FragmentPath` of its mount unit),
and for a loop device `loop_back_file`, `loop_sha256`, `loop_offset`; a second mount on the same target has id
`TARGET#2`. `firewall`: nft ids `nft/table FAMILY NAME`, `nft/chain FAMILY TABLE/NAME`,
`nft/rule FAMILY TABLE/CHAIN/EXPR-JSON`, `nft/set …`; iptables ids `iptables/TABLE/LINE` (counters removed).
`network`: `addr/IFNAME/ADDRESS/PREFIX` (life times removed), `route/…` (`expires` removed), `link/NAME`
(`networkctl`), `nmcli/NAME`, and `file:PATH` with the sha256 of the files under `/etc/systemd/network`,
`/run/systemd/network`, `/etc/network`, `/etc/netplan`, `NetworkManager/system-connections`. `language-package`:
`pip list` when the Python has pip, else `importlib.metadata` (`value.tool` says which; `pip:PYTHON` with
`{"pip": "absent"}` marks the fallback). A standard tool that is not installed gives one object with
`{"tool": "absent"}` (ids `dpkg`, `ss`, `nft`, `iptables`, `ip6tables`, `nmcli`, `networkctl`, `crontab`, `flatpak`,
`podman`, `sudo`). Tools that would create their own storage are not run where it does not exist: `podman` for an
account without `~/.local/share/containers` (root: `/var/lib/containers`), `flatpak --user` without
`~/.local/share/flatpak`. Pythons run with `-I -B` (no bytecode is written), npm with logs off. `meta`: `boot_id`,
`kernel_release`, `time_utc`, `hostname`, `pid1_exe`, `inventory_session` (the login session of the inventory
itself), `user_managers`, `linger`, `synced`, `stored_filesystems`, `stored_devices`, `images`, `volatile_mounts`,
`counts`.

**decide.tsv patterns.** `KIND[,KIND…]:GLOB[#FIELD[,FIELD…]]`. KIND `*` matches every kind. In GLOB `**` matches any
characters including `/`, `*` any characters except `/`, `?` one character except `/`; the glob is matched against
the id. The first matching rule wins; lines starting with `#` are comments. A rule with `#FIELD…` applies only to
`DIFFERS` and removes differences in the named fields (`value.active` or `active`); the object is still reported if
another field differs. A `runtime` rule applies to the kinds `process`, `port`, `mount`, `module`, `unit`: compare
resolves the creator (process: its executable; `[kthread]`: the stored kernel image named after the running
release; port: the executables holding it; module: its module file; mount: the loop back-file, else `creator`;
transient unit: the executables of its members; other unit: its fragment) through the ids and `runtime` paths of the
inventory, following symlinks; the object goes to `compare-excluded.tsv` only if every creator is in the inventory
and is not itself reported; otherwise it is reported with `creator … is UNRECORDED`/`not in the inventory`/`not
determinable` in DETAIL. A `program-record` or `material` rule excludes an object whatever its verdict
(`UNRECORDED`, `DIFFERS`, `MISSING`). No rule excludes an object with `exec: true` (on either side of the comparison).

**Comparison details.** DETAIL of `DIFFERS` is `FIELD machine=JSON derived=JSON line=LINE` (`baseline=` in
`--baseline` mode); `value.F` names a field of `value`. Baseline mode compares, per (kind, id), the fields `kind`,
`mode`, `uid`, `gid`, `size`, `sha256`, `target`, `exec`, `type`, `rdev`, `value`; `meta` is not compared. Derived
mode: a derived `file`/`dir`/`symlink`/`other` id is matched with the inventory id or a `runtime` path; for these
kinds the fields `mode`, `uid`, `gid`, `size`, `sha256`, `target` are compared, for other kinds every field of the
derived `value` that the inventory's `value` has, and `members_include` as a subset of `members`; each field in
`underived_fields` gives one `UNDERIVED` line (`field F: REASON`); `value: null` gives `UNDERIVED` and the object
on the machine counts as following from the line. An `external-list` object may carry `covers` (a decide.tsv
pattern): inventory objects it matches count as recorded (written to the excluded list with `S8.2-18`); without
`covers` it has no effect. `--declaration` must exist; `--excluded PATH` overrides the name of the excluded list
(default: `compare.tsv` → `compare-excluded.tsv`). `compare-excluded.tsv` lines: `KIND  ID  VERDICT  PATTERN  CLASS
SENTENCE_ID  DETAIL`.

## Additions of 2026-11-24, before 11:45 UTC (binding)

- **Runtime paths by owning mount.** In `stored.jsonl`, `runtime` lists the paths at which the object is in force.
  A path belongs to the mount with the longest target containing it (of stacked mounts on one target, the last).
  The object is in force at the path only if that mount shows the object's own filesystem (partition by number or
  UUID, image by the SHA256 of its loop device) at the object's own path (`fs_path`, relative to the mount's
  `fsroot`). A stored object whose filesystem is mounted but which no mount shows has `"shadowed": true` and no
  `runtime`. `meta.runtime_paths` states the rule and how many objects it changed.
- **Firewall read through a fallback.** `inventory --firewall-fallback CMD`: if `nft -j list ruleset` fails in the
  guest, CMD is run there as root and its output is parsed as the native nft text. Objects: `nft/table FAM NAME`,
  `nft/chain FAM TABLE/NAME` (value `text`: its `type`/`policy` lines), `nft/rule FAM TABLE/CHAIN/text:TEXT`
  (value `family`, `table`, `chain`, `text`); every value carries `via` = CMD; `meta.firewall_source` holds the
  refusal of nft and CMD. Without the option, or if CMD fails too, the refusal is an `error` object as before.
- **Verdict `UNVERIFIED`** (comparison with a derivation): a `service` line whose process is seen only as a command
  line equal to its argv, the executable being unreadable (`process` `[exe-unreadable]`). It is never `ok`. In
  `results.tsv`, a row that would pass but for `UNVERIFIED` rows is `unobserved` (QUESTIONS.md Q8).
- **A rule in force with an added `comment "..."`** and otherwise the exact text of a `rule` line is `DIFFERS`
  (`value.text` machine and derived), not `MISSING` (QUESTIONS.md Q7).
- **Derived `release` objects** (`base`, `snapshot`) are not compared: no object of a machine is a release; their
  content is compared through the package objects they expand into. The base lock read for a `base` line is
  `components/SNAPSHOT.txt` of the release when the declaration has a snapshot line and that file exists, else
  `components.txt`.
- **The inventory leaves itself out.** Processes whose command line carries the per-run token of the collector (its
  own `bash -s -- TOKEN …` and the `sudo` that started it) are not listed. Under ConfOS 0.7 the executables of
  processes are unreadable and the login session id is unset, so without this the collector made two inventories
  of one untouched machine differ (experiment `p4test`, P4-T-NOOP, 2026-11-24 05:31 UTC).
- **P4: the effect of an attempt** (`attempt-delta.tsv`, `attempt-effect.tsv` in the case's evidence): the delta is
  the output of `compare --baseline` of the inventory after the attempt against `INV <ID>-pre`; the effect lines are
  `attempt:VERDICT_OF_DELTA` (or `attempt:line`) followed by the line of `compare.tsv` after the attempt.
- **Kinds of DECLARATION.md revisions 6–12 in `derive`** (the values the line states; the rest underived, D4/D5):
  `pip NAME VERSION SHA256 WHEEL` → `language-package` `pip:*/NAME` (PEP 503 name), value `version`;
  `npm NAME VERSION SHA256 LOCK` → `language-package` `npm:*/NAME`, value `version`;
  `flatpak REF COMMIT SHA256 BUNDLE` → `flatpak` `*/ID/*`, value `id`, `kind`, `arch`, `branch`, `commit`;
  `appimage PATH MODE …` and `compile PATH MODE …` → `file` PATH, value `mode` (the bytes at PATH are made by the
  system: `sha256` underived); `container USER NAME IMAGE_SHA …` → `container` `USER/image/IMAGE_SHA`, value `names`;
  `user-unit USER NAME STATE …` → `unit` `user/*/NAME`, value `enabled` (`enabled`/`disabled`). Every line's source
  file is checked against the line's checksum.
- **Ids with `*` in `compare`**: matched (fnmatch, `*` crosses `/`) against the inventory objects of the same kind;
  pip names are compared in PEP 503 form; every match is compared on the fields the line states and the machine
  shows (a Flatpak commit printed shortened counts as equal when the full commit starts with it); no match is
  `MISSING`.
- **Inventory, restricted native commands**: when `flatpak list --all --columns=…` is refused, the plain
  `flatpak list` gives the IDs and `flatpak info ID` each one's ref, commit, branch, arch and installation (value
  `tool: flatpak info`); when `podman images|ps --format json` is refused for an account, the plain `podman images`
  gives the names and `podman image inspect NAME` the full id (`tool: podman image inspect`), and plain
  `podman ps -a` the containers. `npm ls --json --prefix DIR` is taken for every `DIR/node_modules/.package-lock.json`
  under `/usr`, `/opt`, `/srv` (`npm:DIR/NAME`). `--raw FILE` (runner: environment `CASES_INVENTORY_RAW=1`) keeps the
  collector's raw output for diagnosis.

## Additions of 2026-11-24, 11:45–13:50 UTC ([n2-1] … [n2-7]; binding)

- **`derive`: files that other lines determine** (item 2). Where an `account` line is present, the package files
  `/etc/passwd`, `/etc/shadow`, `/etc/group`, `/etc/gshadow`, `/etc/subuid`, `/etc/subgid`; where `setting hostname`
  (or `setting sysctl:kernel.hostname`) is present, `/etc/hostname`, `/etc/hosts`; where `setting timezone` is present,
  `/etc/localtime`, `/etc/timezone` — unless a `file` line of their own names them — are written with `value: null`,
  `underived` naming the lines, `determined_by` (the line IDs) and `package_default` (the value the package gives).
- **`compare --reference INV_DIR`** (derived mode, item 1): an object of the inventory whose verdict would be
  `UNRECORDED` or `DIFFERS` and that equals the object with the same kind and id in the reference inventory (the
  fields of baseline mode, field rules of `decide.tsv` applied) goes to the excluded list with
  `reference  reference-equal  S8.2-16`. The runner calls it `compare-p1.tsv`.
- **`compare --made FILE`** (item 3): `PATTERN  TYPE  STATE  EVIDENCE`, PATTERN as in `decide.tsv` (matched against the
  id and every `runtime` path), TYPE `data` or `obeyed`, STATE `obeyed`/`not-obeyed` for `obeyed`, else `-`. For an
  object that would be `UNRECORDED` (never `DIFFERS`: a recorded object changed is never material), the first
  matching entry decides: a directory is material; a file that a direct route executes (`--routes`) or an `obeyed`
  entry whose STATE is `obeyed` is reported with the reason first in DETAIL, whatever rule of `decide.tsv` matches; a
  file whose routes are `data-only` or `any-only` is `QUESTION`; a file whose routes are `refused`, or that is not code
  in form (no execute flag, or for an `obeyed` entry only a suffix), is excluded as `PATTERN  material  S8.2-15`; a
  file that is code in form and was given to no route is reported (“code in form … and no route was tried”).
- **`compare --routes FILE`** (item 4): `PATH  RESULT  EVIDENCE`, RESULT `executes`, `refused`, `data-only`
  (Q11), `any-only` (Q12). PATH is matched against the id and the `runtime` paths. An object with `exec: true`
  counts as not code when its routes are `refused`, and when its execute flag comes only from its mode on a
  filesystem that stores no modes (`vfat`, `msdos` in `meta.stored_filesystems`): then the rules of `decide.tsv`
  apply to it. When its routes are `data-only` or `any-only`, an object that a rule would decide is `QUESTION`.
- **`compare.tsv` beside it: `compare-exec-blocked.txt`**: the guest paths of objects that a `program-record`,
  `material` or `runtime` rule would decide but whose execute flag keeps them reported; the runner gives them to the
  routes and compares again.
- **Verdict `QUESTION`**: the object is decided only under one reading of Q11 or Q12; it makes P1 and P4 rows
  `undecided` (never `fail`, never `pass`).
- **Field rules with a pattern**: `KIND:GLOB#FIELD~REGEX[,FIELD…]` removes a difference in FIELD only when the two
  values (as JSON) are equal after every match of REGEX is deleted from both. Used for the random filesystem UUIDs
  and partition GUIDs that the build chooses (S8.2-17) and the sizes of devtmpfs (S8.2-5).
- **DIFFERS of a rule with an added comment** is written with the field name `value.text[Q7]`; the runner counts it
  as `DIFFERS-Q7` (a P2 row whose only differences are these is `undecided`, Q7).
- **The runner's files per inventory** (`runs/<name>/<case>/inv-<tag>/`): `made.tsv`, `routes.tsv`, `routes-raw.tsv`
  (`PATH GROUP WHO:ROUTE EXIT EXECUTED ERROR`), `compare.tsv` (derivation, with made and routes: P2, the harder
  reading of UND, the effect of P4), `compare-p1.tsv` (with `--reference`: P1), `compare-und-reference.tsv`
  (`--baseline REF`: the easier reading of UND). `runs/<name>/_reference/<sha256[:16]>/`: the reference installation
  of a declaration — `reference.json` (`ok`, `status`, reasons), `inventory/`, the commands of its build and boot.
  Per P4 case: `pre-probes.json` (every probe before the attempt, its exit and whether it held). OW-7, OW-8:
  `direct.json` (the person's own commands, REVIEW.md R2).
- **`tools/redecide.py --from NAME --name NEW --source TAR`**: decides a finished run again from its stored
  inventories and command outputs with the programs as they are now (same decision code as `run`); the inventories
  of NAME are linked, never changed; rows it cannot decide again are copied with a note.

## Additions of 2026-11-24, 13:55–15:50 UTC ([n3-A] … [n3-D]; binding)

- **`compare --questions`** (item A). The runner gives it to every comparison of an installation (`compare.tsv`,
  `compare-p1.tsv`, `compare-und-reference.tsv`), not to the plain comparison of two inventories of one machine
  (`attempt-delta.tsv`) nor to the planted-object test of `inventory`. It applies to an object of a stored kind
  (`file dir symlink other` and their volatile `v…` forms) in the **writable area** — a volatile object, or an object
  of a stored filesystem or image that has a runtime mount whose options contain `rw` (the `mount` objects of the
  inventory; `meta.stored_filesystems[].runtime_mounts`, `meta.images[].runtime_mount`) — whose verdict is
  `UNRECORDED` (in baseline mode also `DIFFERS`), after the reference check and the person's own objects (`--made`).
  The four questions of S8.2-6, in order; the first affirmative answer decides:
  1. a `store` rule of `decide.tsv` matches (a package manager's store): `UNRECORDED`, DETAIL `question 1 (S8.2-7):
     REASON (rule PATTERN)`;
  2. the object is code in form (`exec: true`, not a mode on FAT): routes `executes` → `UNRECORDED`, DETAIL
     `question 2 (S8.2-9): code; a direct route executed it (…)`; `data-only`/`any-only` → question 2 is open
     (Q11/Q12): question 3 is still asked — in force → `UNRECORDED` (it counts under both readings), otherwise
     `QUESTION`; no routes → **`UNROUTED`** and the path is written to `compare-routes-wanted.txt`; `refused` → go on;
  3. a `program-record` or `material` rule naming the program that recorded it → excluded with that rule; a
     `bothways` rule → `BOTHWAYS`; a `carrier/PROBE` rule matches → its probe: in force → `UNRECORDED`, DETAIL
     `question 3 (S8.2-11): REASON; in force: EVIDENCE`; no probe made → **`UNPROBED`**; not in force → go on. Probes:
     `carrier/unit` a unit of the inventory has the object (any runtime path) as FragmentPath, SourcePath or drop-in
     with `load=loaded` (a symlink in a `.wants`/`.requires`/`.upholds` folder: a unit of that name not disabled);
     unprobed if the account's service manager was not running; `carrier/cron` a running cron daemon (process) and a
     `crontab` object of the file or account; `carrier/key` an `authorized-key` object whose `file` is the object;
     `carrier/route` the routes of the object (`executes` = in force; none tried → `UNPROBED`, path to
     `compare-routes-wanted.txt`); `carrier/none` always `UNPROBED`;
  4. otherwise: excluded as `-  four-questions  S8.2-15` with DETAIL `S8.2-15: none of the first three questions is
     answered yes` and what questions 2 and 3 found.
  Objects of the read-only stored system part are not decided this way: whatever equals neither the derivation nor
  the reference installation stays `UNRECORDED`. With `--questions` no `UNRECORDED` line has an empty DETAIL: an object
  of the system part says so (`the stored, read-only system part …`), an object of the level of what is in force says
  `in force: observed by the inventory …`.
- **New `decide.tsv` classes** `store`, `carrier/unit`, `carrier/cron`, `carrier/key`, `carrier/route`,
  `carrier/none`; ignored without `--questions`.
- **Verdicts `UNROUTED` and `UNPROBED`** (item B): the object's deciding observation was not made. A P1, UND, P4 or
  REM row whose objects that could count against it are only such objects is `unobserved` (order of outcomes: `fail`
  if any object counts against with its observation made, then `unobserved`, then `undecided`, then `pass`). The
  person's own file that is code in form and was given to no route (`--made`) is `UNROUTED` too.
- **`derive`: reader overrides of a component** (builder's entry 49; build/INTERFACE.md revision 29). A package of
  the derivation that ships `/usr/lib/confos/reader-overrides/manifest.json` (the component `confos-code-readers`)
  is read once more: for each record whose `package` is named by a line or by the base lock, a `file` object of the
  record's `target` with `mode` (octal of the integer), `size` and `sha256` of the decompressed gzip member named by
  `payload` (it must equal the record's `sha256`, otherwise the object is underived), `override: true`,
  `override_of: PACKAGE`; it replaces the package's own object of that path in the merge, keeping its owner and
  group (`replaced` names the package).
- **`compare-routes-wanted.txt`** beside every comparison: the guest paths of `UNROUTED` and `carrier/route`
  objects; the runner gives them to the routes of their form (scope as for the person's own files) while the machine
  runs, and compares again.
- **`derive`: the `linuxgsm USER PATH RELEASE SHA256 BUNDLE` line** (build/DECLARATION.md revision 18; added 15:45 UTC,
  [f2]): the bundle's checksum is checked; a `dir` object PATH (mode, uid, gid underived: the line names the
  account but not its UID) and an underived `file` object `PATH/**` (the layout inside PATH is the launcher's
  convention, D4).

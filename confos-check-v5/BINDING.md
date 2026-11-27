# Binding addendum: release 0.67

2026-11-26 UTC. Binds the portable cases to the builder's interface of release 0.67
(`INTERFACE.md`, `EXECUTORS.md`, `FORMAT.md`, `declarations/base.conf`; their SHA-256
values are recorded in `bindings/*.json`). First written for 0.60 before any release was
named for a run; regenerated for 0.65 and corrected after trials on it (CORRECTIONS 2);
regenerated for 0.66, which updates the system through the declaration, and for 0.67,
which keeps on the system partition only what the lines bring (CORRECTIONS 3). No operating-system result is reported here.

The adapter is `adapter.py` + `adapter_native.py` + `adapter_disk.py`: the only code
that knows how the system is built, booted, reached and read. The checking programs
(`core.py`, `engine.py`) are unchanged in what they judge, except the additions listed in
`CORRECTIONS.md`.

## 1. Generated binding files

| file | generator | content |
|---|---|---|
| `bindings/release-0.67.json` | `tools/make_bindings.py --interface FILE --base-conf FILE` | every binding slot of `declarations/*.json` → native lines and input files, or `unsupported` with the reason; release layout and derivation table (section 4) |
| `bindings/commands-0.67.json` | `tools/make_commands.py --interface FILE --executors FILE --base-conf FILE` | tokens and preludes, the command of every variant (94 variants of 21 cases), probes, X-REC requests, removal and change targets, server files |

Both record the SHA-256 of the payload files they use; the adapter refuses to start if
a payload changed after the freeze.

## 2. Declarations

- Native lines are those of INTERFACE 5. A semantic declaration is rendered into one
  file `declaration.conf` with its inputs beside it (recipes, sources, `files/<id>`).
  The split case writes `include programs.conf`.
- `base-source-lock` = the `base`, `package` and `network` lines of the release's
  `base.conf` (62 packages). Its account, sudo file and key file are replaced by:
- `test-account-and-login`: `account user 1000 1000 users /bin/bash /home/user`, one
  `authorized-key` line for `user` and one for `root` (the key is private, `local.env`),
  `open /home/user/control`, `open /root/control` — the opened folders of the positive
  controls (A18) — and `rule case-ssh 'add rule inet confos input tcp dport 22 accept'`,
  the recorded rule of G-FIREWALL "remove recorded rule".
  Role `user` = SSH as `user` (no sudo rule); role `root` = SSH as root (INTERFACE 4).
- Case packages are `package NAME VERSION RECIPE` with recipes in `payloads/`
  (`case-probe-1`, `case-small-1/2`, `case-extra-a/b`, `case-extra-service`,
  `case-sleeper`), compiled inside the system by `confos apply`/`confos-assemble`.
- The identity is computed by the adapter by INTERFACE 5 and must equal the
  `BUILT ... identity` line, `confos check`, the `CONFOS READY` line and `confos status`.
  A fixture test checks the adapter's parser and identity against the release's own
  `Declaration` class.
- Unsupported in 0.67, so their cases stay unobserved (reason in the row): latest
  selector (W3d-LATEST), account server (Q9-SOURCE), saved Wi-Fi/Bluetooth (X-WIFI,
  X-BT, OW-10, OW-11, G-SAVED-NETWORK), shared dependency between package lines
  (REM-4), prohibition line (W4c-DEFAULT second half), container (G-CONTAINER),
  network transfer during installation (OW-9,
  P2-NET-1: `confos apply` reads recipe and sources beside the declaration), loadable
  modules (G-MODULE, X-REC-MODULE), per-user services/timers/linger (several variants).
- Update states (INTERFACE 9; OW-2, then OW-3 on the same installation): T0 is the release
  itself (`base 0.67`); T1 and T2 are the builder's tags `0.67.1` and `0.67.2`. The slots
  `T1`/`T2` hold the native lines `base RELEASE rel-RELEASE TREESUM` and the package lines
  that differ from T0 (`tools/make_bindings.py --update STATE RELEASE TREE`, TREE = `git
  archive` of the tag; TREESUM by the release's own `confpkg treesum`, as INTERFACE 9 tells a
  person to do), one SHA-256 over every file of the tree (path, content, executable or not)
  with the file count, and the sources the changed recipes add. The edit replaces the base line and those package lines and writes the tree beside
  the declaration (`rel-RELEASE/`, executable files 0755); the tree and sources of an
  earlier update leave the folder. OW-2 hands its disk to OW-3 (synced, powered down by
  the power button, booted again by OW-3).

## 3. Lifecycle and transport

| operation | 0.67 binding |
|---|---|
| fresh | render; copy the clean package store by hard links (originals unchanged); run `python3 /confos/tools/confos-assemble /decl/declaration.conf /packages /confos /sources /out/disk.raw` inside the clean bootstrap root, entered as root of a user namespace (PROCEDURE 3 and 6); the identity of the `BUILT` line must equal the adapter's |
| boot | QEMU exactly as `scripts/boot.sh` (q35, OVMF, virtio disk, user networking, SSH forwarded on 127.0.0.1) plus one QMP socket; a machine slot (1–4) is taken first; at most 8 GiB and 4 vCPU; wait for `CONFOS READY <identity>`, then SSH |
| command | `ssh -i KEY -p PORT ACCOUNT@127.0.0.1 CASE_MARKER=... sh -c TEXT`; host key not pinned (INTERFACE 3: a new key at every boot); exit 255 or a timeout is a transport failure, never a refusal; a session with a terminal (`-tt`, startup routes) gets an open, empty input and must print an end marker |
| put-material | `cat > TARGET` with the bytes on standard input, then `sha256sum` read back |
| edit / record | root writes every candidate file under `/data/confos` (one tar on standard input, extracted with `--no-same-owner`) and reads back the SHA-256 of every file |
| read-law candidate | root reads the files back (one tar, base64); `confos check` is recorded beside the adapter's identity |
| read-law committed | external read of the raw disk, without the system: `debugfs -R 'cat /boot.cfg' DISK?offset=135266304`, the generation named by `confos.generation=`, its `declaration/` files and `state/applied` |
| apply | `confos apply` as root; on `SELECTED <identity>` wait for a new boot identity and `confos status` = `APPLIED <identity>` |
| apply-cut | the same; the power is cut (SIGKILL of QEMU) at the first `APPLIED` status after the restart (INTERFACE 6: the report of success to wait for) |
| restart | `reboot` as root; if the session may not, QMP `system_powerdown` and a new start; the method is recorded |
| network | QMP `set_link n off/on` |
| inventory | live capture (one typed script as root: processes with `sha256sum /proc/PID/exe`, sockets, accounts, groups, rights, keys, services, addresses, routes, mounts, modules, kernel parameters, locale, time, host name, the packet filter in force (`confos rules`, one object per statement), radios, files in `/tmp`, `/var`, `/dev/shm`, `/run`) and the external disk read (`adapter_disk.read_disk`: GPT, ext4 by debugfs with journal replay on a copy, squashfs by unsquashfs; owners and modes from the image) |

## 4. Independent derivation (what a line promises)

From the declaration and the named packages only (Table 9; QUESTIONS 4): package
objects from the independently built package store (the passport and every member,
checked by `adapter_disk.read_confpkg`); account, group, key, rights, service, rule,
setting and opening objects from the lines; INTERFACE 5 defaults for an absent host
name, time zone and locale. The base's own contributions are derived from the sources
of the named base packages, never from a machine: base accounts and groups
(`BASE_PASSWD`, `BASE_GROUPS` of the confos program), the mounts of `rc.boot` and
`initramfs-init.c`, the rendered paths of `render()` and the startup files. Rendered
paths replace package files of the same path, so for them only presence is derived;
the values they carry are compared as account/setting/… objects observed live.

Data classification (FORMATS "Independent inventory", 5.3 "Data"): material the case
put keeps its observed routes; any other file in a writable place is material with a
data route whose evidence is the live `noexec` mount entry; files in an `exec` mount
(an opened folder) are opened material. Nothing is dropped.

What the lines bring onto the system partition (INTERFACE 7, 8 and 9; 5.3 "written") is
derived and compared like any other object: for every `package` line the archive
`/system/packages/NAME-VERSION.confpkg` (its passport: name, version, recipe and sources;
the bytes are not promised, rule 4); for the `base` line the tree of the named release
(the SHA-256 of a manifest of `recipes/`, `files/` and `tools/`: path, content, executable
or not), read from the case party's copy of the tag, and every source file a recipe of that
release names by a plain file name (INTERFACE 7); the generation of the declaration in force, `boot.cfg` selecting it and
`state/applied` naming it. The disk reader gives one object per archive, per tree
(`/system/tree` named by the release in its own `files/base-files/etc/os-release`,
`/system/trees/RELEASE` by its folder) and per source. What no line names — the
generation before, archives, trees and sources of earlier declarations, other entries —
is `undecided` (QUESTIONS 9); it was asked of the builder (REQUESTS 14–17, repaired in 0.67). Kernel
link-local addresses are `undecided` (QUESTIONS 10).

## 5. Variants, probes, controls

Every variant of every case is in `bindings/commands-0.67.json`: a command, or
`unsupported` with the document and line, or `covered_by` (two cross-reference
variants whose route is a variant of another case). Probe protocol: exit 0 present,
1 absent, anything else unobservable. A missing tool makes the case unobserved, never
a refusal. Positive controls: the same payload and command in `/home/user/control` or
`/root/control`, with the role of the attempt (marker routes), or the probe reading the declared state correctly (settings).

## 6. Case-controlled server

`make_server_files` builds, on the host, from frozen payload sources: a static marker
program (`payload`), its tar, a self-extracting script, a Python payload, the
persistent script, `case-small.c`, a document, a second build of `case-probe`, and the
package `case-small-2.confpkg` built in the clean bootstrap root. These are foreign
material brought into the system by the cases; none is part of the system. The server
listens on the host loopback; the guest reaches it as `10.0.2.2` (QEMU user network).
Every fetch is logged with a monotonic time.

## 7. Before run 1

`local.env` (unpublished) gains a `native` section: release name, tree commit, source
manifest, clean package store, bootstrap root, subordinate id, slots folder, SSH key,
port, server port. Run: `./run --native local.env --all --out DIR` inside
`confos.slice`. Each run records the records commit `1619b5bc`, `CORRECTIONS.md`,
this addendum's checksums and the release identity.

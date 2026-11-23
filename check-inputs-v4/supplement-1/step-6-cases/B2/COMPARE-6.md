# Step 6: committed comparison queries

Recorded 2026-11-23 UTC. These are preparation inputs, not observations or outcomes. Use the immutable declarations, fresh guests and once-only sequence in [CASES-6.md](CASES-6.md). The executable query list is [build/bc4-compare.py](build/bc4-compare.py); its installation path is `/usr/local/lib/stand/bc4-compare.py`. It does not import the testbed's verifier or infer actual state from the requested line. A successful collector exit only means evidence was emitted.

Appendix A.4.4 requires “every value the line states” as well as the listed program, service, account and rule observations. The queries retain complete requested rows and complete filesystem declarations, including timestamps, size and extended attributes. Do not remove a difference because it looks volatile. The hardware exception in Appendix A.4.4 is limited to drivers, firmware or device files of hardware present on one machine and absent on the other, with evidence of that difference. Raw evidence, unavailable queries, source identities and all differences are retained for the separate review.

## Complete readback

The committed host bundle and `blobs.json` are staged under `/var/lib/stand/bc4-inputs/NAME/`, outside the mediated roots. Each path selects a fixed input, not a declaration reconstructed from the guest. At the corresponding stage the controller invokes exactly one of these readback commands (case 1 and case 2a each use the same command on their two fresh guests):

```sh
python3 -B /usr/local/lib/stand/bc4-compare.py snapshot --bundle /var/lib/stand/bc4-inputs/case-1/declaration.json
python3 -B /usr/local/lib/stand/bc4-compare.py snapshot --bundle /var/lib/stand/bc4-inputs/case-2a/declaration.json
python3 -B /usr/local/lib/stand/bc4-compare.py snapshot --bundle /var/lib/stand/bc4-inputs/case-3-before/declaration.json
python3 -B /usr/local/lib/stand/bc4-compare.py snapshot --bundle /var/lib/stand/bc4-inputs/case-3-after/declaration.json
python3 -B /usr/local/lib/stand/bc4-compare.py snapshot --bundle /var/lib/stand/bc4-inputs/case-4-both/declaration.json
python3 -B /usr/local/lib/stand/bc4-compare.py snapshot --bundle /var/lib/stand/bc4-inputs/case-4-one/declaration.json
python3 -B /usr/local/lib/stand/bc4-compare.py snapshot --bundle /var/lib/stand/bc4-inputs/case-4-none/declaration.json
```

These are stage-specific calls, not a sequence to run on one guest. The full application commands, copy-in commands, output filenames and one-attempt discipline are fixed in CASES-6. There is no case-2b bundle or application command.

Keep stdout on the host. Writing evidence under a guest's mediated filesystem would itself change its complete declaration. The output contains:

- `requested_machine_sha256`, `current_machine_sha256` and `current_machine_byte_identical`.
- Every literal required machine row and its native observations under `rows`.
- Every required filesystem declaration, selected declaration bytes and SHA-256, selected-byte equality, success identity, every declared path's native values, all declared-field mismatches, hard-link equivalence classes, native account semantics and whether the declaration changed during collection.
- The exact argv, exit, stdout and stderr for subprocess queries under `evidence.commands`; failure is retained, never converted to absence or success.

For each pair, save the collector outputs as two JSON files and run on the host:

```sh
python3 -B build/bc4-compare.py diff LEFT.json RIGHT.json
```

`LEFT.json` and `RIGHT.json` mean the fixed pair outputs identified in CASES-6. This returns *all* differences, including raw diagnostics, and makes no hypothesis decision. Compare required values with their native observations as well as comparing the two guests: matching errors or matching wrong states do not meet a line's requirement. The separate case report must list each mismatch, unavailable value and explanation; equal hashes alone do not settle fulfillment.

## Exact queries behind each line

The collector reads the bundle's `machine.jsonl`, resolves its referenced `base-files.json`, and applies the following queries to every line, including inherited base lines. These loops are implemented literally in the committed script; names and paths come only from the fixed declaration.

| Line/value | Query and returned fact |
|---|---|
| Every line's literal input, metadata, source, version, manifest identity, payload and options | Preserve the complete required row; SHA-256 and byte-compare the selected `machine.jsonl` with the committed one. A manifest is read from the committed bundle and hashed. Source/payload digests bind the fixed recipe/artifacts; they are not guessed from execution output. |
| Every installed program/base/code file | `os.lstat(path)` supplies type, permission bits, UID, GID and size; `os.listxattr`/`os.getxattr` preserve extended permission metadata including any ACL/capability bytes; `hashlib.file_digest(open(path,'rb'),'sha256')` supplies regular-file checksum; `os.readlink(path)` supplies a symlink target. Every path listed by either inline files or the external manifest is queried. |
| Native package name, version, architecture, installed status | `/usr/bin/dpkg-query -W '-f=${Package}\t${Version}\t${Architecture}\t${db:Status-Status}\n' NAME`. Preserve exit and output. |
| Stand package and dependency identities | Read `/var/lib/stand/objects.json`; select actual package registrations by backend/name, retaining status-bearing registration, version and every origin. Never synthesize a registration from the proposed line. |
| Account name, UID, primary GID, all groups, shell, home and GECOS | `pwd.getpwnam(NAME)`; `os.getgrouplist(NAME, primary_gid)`; `grp.getgrgid(GID)`. Keep both sorted numeric and named group sets. Missing group names are explicit `UNRESOLVED_GID` values. |
| Group name, GID, member names | `grp.getgrnam(NAME)`; retain the complete returned tuple with sorted member names. |
| Service/timer/socket enablement | `/usr/bin/systemctl is-enabled UNIT`; for `scope=user-global`, `/usr/bin/systemctl --global is-enabled UNIT`. Preserve exit and effective text. |
| Unit checksum, text, active requirement | `/usr/bin/systemctl show UNIT -p FragmentPath -p LoadState -p ActiveState`; hash and read the actual `FragmentPath`; `/usr/bin/systemctl cat UNIT` preserves effective unit text including drop-ins. A global unit uses its exact declared `unit_path`. Compare active state when the line states it. |
| Privilege and login-key text, permissions, UID/GID | Read declared `path` in full and apply `lstat`; preserve exact text and file hash. |
| Password-login effective values | `/usr/sbin/sshd -T`; retain `passwordauthentication` and `kbdinteractiveauthentication`, with the full command result. |
| Network rule effective text and expression | `/usr/sbin/nft list table inet stand` and `/usr/sbin/nft -j list table inet stand`. Retain full raw outputs; select rules by the exact line ID comment. Keep all expression text and structured attributes. Handle/index metadata is omitted only from the structured rule view, still retained in raw output. |
| Firewall chain | The same two `nft` queries; select the declared chain and compare family, table, name, type, hook, priority and policy. Retain the entire effective table text. |
| Mount rule options | `/usr/bin/findmnt -n -o OPTIONS --target PATH`; preserve the complete option set and require all declared options. |
| DAC rule | `lstat`, file hash and symlink queries for every declared path, as for installed files. |
| Code-boundary rule | Read `/sys/kernel/security/apparmor/profiles`, `/sys/module/apparmor/parameters/enabled`, every exported kernel `policy/profiles/**/name`, `mode` and `raw_data`, plus `/etc/apparmor.d/stand-*` and `/etc/stand/launch.tsv`. Preserve exact loaded policy bytes as base64 and SHA-256. The prose requirement has the limitation below. |
| Listener protocol, address and listening state | `/usr/bin/ss -H -lnt` or `/usr/bin/ss -H -lnu`, selected by the line's protocol; compare the exact declared address and retain all reported listeners. |
| Native setting | `/usr/sbin/sysctl -n NAME`; preserve the returned value. |
| Saved network/profile, if present | Read `/etc/NetworkManager/system-connections/stand-ID.nmconnection`; `/usr/bin/nmcli -g all connection show UUID`. |
| Bluetooth profile, if present | Read `/var/lib/bluetooth/ADAPTER/ADDRESS/info`; `/usr/bin/bluetoothctl info ADDRESS`. |
| Boot requirement | Read `/proc/cmdline`; separately retain the host's actual VM argv and firmware/image identities from the case launch record. The guest cannot independently report a host-fixed boot order. |
| Complete filesystem object | `os.lstat`: `st_mode`, `st_uid`, `st_gid`, `st_size`, `st_atime`, `st_mtime`, `st_ctime`, `st_nlink`; regular-file SHA-256 or symlink target; `os.listxattr` and `os.getxattr` with base64 bytes. Compare every declared field, including all timestamps and xattrs; do not round or normalize a mismatch away. |
| Filesystem path/inode relationships | Group observed paths by actual `(st_dev,st_ino)` and retain all hard-link groups. Declaration inode keys, generation and next-inode allocation values are checked as exact selected declaration bytes; they are interpreter identifiers, not assertions that Linux's numeric inode/device IDs equal them. |
| Filesystem account/settings rows | The same independent NSS account/group queries; exact base64 database contents and SHA-256 for every `account-database` setting. Preserve the declared source/recording fields. |

For file payload `content_b64`, compare its decoded SHA-256 with the required checksum and the installed file checksum; for `unit_text`, compare its exact text and SHA-256 with the unit file. A recorded source URL or source hash is provenance: the fixed recipe and artifact identities establish that input, while installed file bytes establish the realized output. It would be circular to call copying `source` from the declaration an independent runtime observation. Managed/type/ID/schema metadata are checked as selected input identity and determine the corresponding query. Any unsupported field must remain an explicit unresolved obligation in the review; it is never a passing default.

## Case 2 accounts

For each guest, the complete snapshot includes the two account-own lines plus account-package and filesystem rows. The following additional exact diagnostic commands expose the A.4.4 account tuple without relying on the testbed verifier:

```sh
getent passwd bc4alpha bc4beta
id bc4alpha
id bc4beta
getent group bc4alpha bc4beta
```

Read the UID, GID, group memberships, shell and home from these outputs and the full independent snapshot. Case 2a requires both the fixed values and pairwise equality. The opposite order is produced only by the package commands in CASES-6; the final complete declaration must be byte-identical. Case 2b has no executable case if the format requires numeric identifiers; its non-expressibility is recorded in BUILD-4 and CASES-6, with no invented defaults.

## Case 3 removal queries

Before removal, retain the successful program launch output and the service worker's exact process identity. These are observations performed once by the controller, not extra repetitions:

```sh
/usr/bin/systemctl show stand-development.service -p MainPID -p ActiveState -p UnitFileState -p FragmentPath
python3 -B /usr/local/lib/stand/bc4-compare.py processes /opt/stand/pkgs/dev-worker/bin/worker
```

The `processes` query scans `/proc` and records every holder whose executable, argument vector or mappings contain the exact worker path, including deleted executables. It records PID, `/proc/PID/stat` starttime, process state, argv and mappings. Preserve the former service PID/starttime before removing the lines; after removal, compare that identity rather than using PID existence alone. A reused PID is not the former process; a zombie is not running. Unreadable processes and interrupted scans are evidence limits.

After the single removal application, run the same process query and these commands once, retaining every exit code, stdout and stderr even for expected failures:

```sh
/usr/bin/systemctl is-enabled stand-development.service
/usr/bin/systemctl show stand-development.service -p MainPID -p ActiveState -p UnitFileState -p FragmentPath
/usr/sbin/nft list table inet stand
/usr/sbin/nft -j list table inet stand
stat /opt/stand/pkgs/dev-worker/bin/worker
stat /etc/systemd/system/stand-development.service
```

The executable launch attempt is the exact ordinary-shell command committed in CASES-6, with no `--wait` argument; it tests whether the removed executable can start. Preserve its exit and output. A failed `stat` or absent ledger row alone is insufficient: inspect former process identity, all path holders, executable launch result, service enablement and the complete effective rule set. The worker service's executable is `/opt/stand/pkgs/dev-worker/bin/worker`; the removed rule is `tcp dport 17777 drop` with comment `dev-rule`, in `inet stand input`. Look for equivalent residual rule text even if its comment changed. The full after snapshot checks the remaining lines as well.

## Case 4 shared installed package

Before removal, after removing `bc4:owner-a`, and after removing `bc4:owner-b`, run:

```sh
python3 -B /usr/local/lib/stand/bc4-compare.py package bc4-shared
python3 -B /usr/local/lib/stand/bc4-compare.py package bc4-owner-a
python3 -B /usr/local/lib/stand/bc4-compare.py package bc4-owner-b
```

Also preserve the complete snapshot and raw `/var/lib/stand/objects.json`. The chosen object is the dependency-only Stand package `bc4-shared`, version `1`; it has no file payload or executable. This installer's registration is its installation state, so no nonexistent payload check is invented. The first state should have both origins, the intermediate state the remaining package's origin, and the last state no shared registration. Review the remaining line's required dependency against the actual registration and full snapshot, not merely the absence of the removed line. The checks preserve erroneous residual registrations even if their origin names are stale.

## Limits that cannot become passing observations

The collector is a finite readback tool. It does not prove the inherited code-boundary prose for every possible execution, reconstruct provenance merely from current bytes, prove physical-hardware behavior, or establish the external firmware boot order from inside the guest. Inherited code-boundary sources and loaded kernel policy bytes permit an exact implementation comparison, not a theorem about the prose. Any such unresolved obligation must remain explicit when judging case 1. Kernel profile listing order, process IDs, nft handles and command diagnostics may differ without themselves being declared values, but the raw differences are retained and require an explained disposition; declared timestamps and values cannot be discarded on that ground. A generation change during snapshot means the observation was not stable; it is not a pass or permission to retry a once-only case. Outcomes and the definition-only argument required for any `0` belong to the second party and separate reviewer.

# S5-O log (second party, supplement 1 step 5)

All times UTC. The host = the server laboratory; paths relative to the night folder or to the laboratory `stand/` folder.

## 2026-11-23T17:08:16Z pre-checks (before any case)

- Gate (not published: orchestration or scratch): seal SHA-256 `2bbc5cad…5dce62` and `check-inputs-v4/supplement-1/step-5-cases/CASES-5.md` SHA-256 `cf01619e…819c2b9` both match the local and the host copies.
- Image `base/stand.qcow2` on the host: `5641c3c3…b3cb79` = top of CASES-5. Offline complete declaration: `4fd6f7ac…33bda57` = top of CASES-5. All files named in the seal match (two of them exist only in the local export). Evidence: `S5/raw/00-identity-checks.txt`.
- The frozen controller `bc3-selftest.py` (`68cf3372…`) and fixture manifest (`1277fed5…`) are the ones the frozen declaration lists (`B2/raw/round-3/final-1/installed-source-identities.json`, offline declaration).
- Commands vs round 1: all fifteen way commands in CASES-5 and in the manifest are byte-identical to the round-1 `expected` rows (shell.jsonl lines 23/25/27/29/31/33; direct.jsonl 27/29/32/35/37; extra.jsonl 7/12/35/49); account argv identical to tools.jsonl line 178. Fixture bytes, sizes and modes equal the round-1 fixture rows; round-1 controller working directories (`/home/stand`, `cd /home/stand/v4-direct; `, `cd /tmp/v4-extra-7z89hz2f && `) are kept. Difference in setup only: round 1 wrote the direct/extra fixtures as root from the controller, round 3 writes them through the ordinary account's shell; the shell-way fixture (saved.txt) in round 1 was left by the SAVED-SCRIPT command, here it is written by the controller in a fresh copy. No way is weakened in its command. Evidence: `S5/raw/01-round1-command-comparison.json`, `B2/raw/round-1/final-2-supplement-inputs/v4-direct-selftest.py` lines 113–123.

## Expected observation for every way case (01–15), written before the first run

Mechanism read before the runs: `B2/build/bc3_filesystem.py` (single-threaded FUSE; every create/write/truncate/chmod commits a full new declaration generation with `success.json` and switches `current` before the in-memory state used by `read` changes). Expected for each way: the attempt is NOT refused; it exits 0 and prints its marker; the saved source appears in the after-attempt filesystem declaration (`home` or `tmp`) as a path→inode→object row with the manifest SHA-256, under a generation whose `success.json` hashes that declaration; the audit since the before-snapshot shows the write generations of that source and no other path changes besides the fixture/command's own files; the primary `machine.jsonl` is unchanged (except DISPATCHER-SAVED setup, which adds the dispatcher row before the before-snapshot). Then the permitted action (same literal command) finds the source already covered, exits 0 and prints the marker. Expected outcome by the rule of `SUP1/step-5.md`: 1, provided reading the declarations confirms the coverage.

## Case runs

- 2026-11-23T17:08:41Z case 01 SAVED-SCRIPT — commands = round-1 shell.jsonl line 23 (checked). Expected: inline write of `/home/stand/saved.txt` (17415cef…) recorded by home-FS generations (create, truncate/write) before `bash saved.txt` reads it; attempt exit 0 + `SAVED_CODE_RAN`, not refused; permitted: same command, rewrite of identical bytes audited, exit 0 + marker. Outcome expected 1.
- 2026-11-23T17:09:44Z case 02 SAVED-PIPE — commands = round-1 shell.jsonl line 25. Expected: controller writes `/home/stand/saved.txt` (17415cef…) as the ordinary account, recorded in home-FS; `cat saved.txt | bash` exit 0 + `SAVED_CODE_RAN`, not refused; source covered before and after; permitted same. Outcome expected 1.
- 2026-11-23T17:09:44Z case 03 SAVED-SOURCE — round-1 shell.jsonl line 27. Expected as 02 with `source saved.txt`. Outcome expected 1.
- 2026-11-23T17:09:44Z case 04 STARTUP-ENV — round-1 shell.jsonl line 29. Expected as 02 with `BASH_ENV="$HOME/saved.txt" bash -c :`. Outcome expected 1.
- 2026-11-23T17:09:44Z case 05 PYTHON-IMPORT — round-1 shell.jsonl line 31. Expected: inline write of `loose_module.py` (7f938b43…) recorded before import; exit 0 + `IMPORTED_UNRECORDED`; no `__pycache__` (-B); permitted rewrite audited. Outcome expected 1.
- 2026-11-23T17:09:44Z case 06 PICKLE-CODE — round-1 shell.jsonl line 33. Expected: inline Python write of `serialized` (b26a48df…) recorded before `pickle.load`; exit 0 + `PICKLE_EXECUTED`; permitted same. Outcome expected 1.
- 2026-11-23T17:09:44Z case 07 DIRECT-REDIRECT-STDIN — round-1 direct.jsonl line 27. Expected: `/home/stand/v4-direct/saved.sh` (43d50a29…, 0755) recorded with the directory; `bash < saved.sh` exit 0 + `SAVED_DIRECT_RAN`. Outcome expected 1.
- 2026-11-23T17:09:44Z case 08 DIRECT-PROC-FD — round-1 direct.jsonl line 29. Expected as 07 via `/proc/self/fd/3`. Outcome expected 1.
- 2026-11-23T17:09:44Z case 09 DIRECT-READ-EXEC — round-1 direct.jsonl line 32. Expected: `saved.py` (85ff61eb…) recorded; exit 0 + `READ_EXEC_RAN`. Outcome expected 1.
- 2026-11-23T17:09:44Z case 10 DIRECT-AWK-FILE — round-1 direct.jsonl line 35. Expected: `saved.awk` (c6d3872b…) recorded; exit 0 + `AWK_FILE_RAN`. Outcome expected 1.
- 2026-11-23T17:09:44Z case 11 DIRECT-SCRIPT-HELPER — round-1 direct.jsonl line 37. Expected as 07 via `find … -exec bash saved.sh`. Outcome expected 1.
- 2026-11-23T17:09:44Z case 12 RC-STARTUP — round-1 extra.jsonl line 7. Expected: `/tmp/v4-extra-7z89hz2f/startup.rc` (a829afcc…, 0600) recorded in tmp-FS; exit 0 + `SAVED_RC_EXECUTED` (stderr job-control notes as in round 1). Outcome expected 1.
- 2026-11-23T17:09:44Z case 13 EDITOR-SAVED-COMMANDS — round-1 extra.jsonl line 12. Expected: `commands.ed` (83f83d4d…) recorded in tmp-FS; exit 0 + `SAVED_EDITOR_COMMAND_EXECUTED`. Outcome expected 1.
- 2026-11-23T17:09:44Z case 14 JIT-SAVED-INPUT — round-1 extra.jsonl line 35. Expected: `machine.bytes` (11db5348…) recorded in tmp-FS; exit 0 + `JIT_SAVED_INPUT_EXECUTED 42`. Outcome expected 1.
- 2026-11-23T17:09:44Z case 15 DISPATCHER-SAVED — round-1 extra.jsonl line 49. Expected: setup installs the dispatcher row through `stand-pkg` (primary machine.jsonl changes before the before-snapshot); `instructions.ops` (08a7984a…) recorded in tmp-FS; exit 0 + `DISPATCHER_SAVED_EXECUTED`. Outcome expected 1.
- 2026-11-23T17:09:44Z case 16 root-native-account-bypass — round-1 tools.jsonl line 178. Expected: `useradd` as root exit 0; account tuple v4raw/1998/1998/[v4raw]/`/home/v4raw`/''/`/usr/sbin/nologin`; etc-FS declaration changes and its `account_rows` hold an own row matching the tuple under a matching success; no `/home/v4raw` created (-M). Outcome expected 1.
- 2026-11-23T17:12:53Z case 17 ordinary-work — commands fixed in CASES-5 section 17 and in the frozen controller `ordinary_work`. Network fixture active (`S5/raw/02-network-fixture.txt`). Expected: one `stand-shell` session, exit 0; outputs `TWO WORDS`, `PERSONAL_SCRIPT_OK:ordinary argument`, `Hello, world!`, `BC3 NETWORK PAGE`, `Edited document`, `BC3_ORDINARY_COMPLETE`; document bytes `Edited document\n`; primary declaration gains the `bc3-personal` row and a row for the repository `hello` package; home-FS declaration gains `document.txt` and `page.html` (material, voluntarily recorded). Outcome expected 1.

## Runs (each once, each on its own fresh copy `bc3-peer-NN`, destroyed by the replay sequence)

- 17:08:41–17:09:23 case 01 alone (replay sequence of CASES-5 verbatim: `S5/tools/replay.sh`). Exit 0.
- 17:09:44–17:13:20 cases 02–16, four copies at a time (`xargs -P 4`), each holding one slot through `lab.py`. All exit 0; host output `S5/raw/04-batch-host-output.txt` holds only unit/creation lines, no error.
- 17:13:30–17:15:06 case 17 with the network fixture active (checked `active` and the page immediately before). Exit 0. Network fixture stopped after it (`inactive`).
- After the runs: no guest in `stand/vms/`, no `stand-*`/`bc3*` user units, all 12 slots free; host scratch folder removed. The case outputs stay where CASES-5 puts them (`stand/raw/round-3/second-party/`); the local copy is byte-identical (`S5/raw/06-host-after-cleanup.txt`).
- No case was repeated, nothing was repaired, no command other than the frozen controller ran inside any copy.

## Observed vs expected

- Every observation matched the expectation written above (attempt not refused, marker printed, saved source covered in the designated filesystem declaration under a matching success report; permitted action succeeded; account row own and matching; ordinary work complete). Details: `S5/raw/05-cases-summary.txt`, (not published: record outside selected evidence).
- Not foreseen: in case 13 `ed` created, renamed to `.fuse_hidden…` and unlinked a scratch file in `/tmp`; each step committed a tmp-filesystem generation (68–70, 71–73). In case 17 the package/script installs also rewrote five `/etc/stand…` files through the etc filesystem (generations 166–237) and the home declaration gained `.w3m/`, `document.txt`, `page.html`.
